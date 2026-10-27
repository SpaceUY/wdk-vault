import contextlib
import http.client
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

META = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("versions", META / "versions.py")
versions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(versions)

GIT_ID = ["-c", "user.name=Test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false"]


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *GIT_ID, *args], cwd=repo, capture_output=True, text=True, check=True)


def make_repo(root: Path, name: str, subjects: list[str]) -> Path:
    repo = root / name
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    for subject in subjects:
        git(repo, "commit", "-q", "--allow-empty", "-m", subject)
    return repo


def commit_files(repo: Path, files: dict[str, str], subject: str) -> None:
    for rel, text in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", subject)


def lock(version: str) -> str:
    return json.dumps({"packages": {"node_modules/@tetherto/wdk-wallet-evm": {"version": version}}})


def state(name: str = "repo-a", **overrides: object) -> "versions.RepoState":
    fields = dict(
        name=name, branch="main", analyzed_ref="origin/main", head="a" * 40, head_date="2026-07-01",
        local_head="a" * 40, local_head_date="2026-07-01",
        origin_head=None, behind_origin=None, ahead_origin=None,
        release=None, release_commit=None, release_date=None,
        ahead_of_release=None, package_version=None, dirty=False,
    )
    fields.update(overrides)
    return versions.RepoState(**fields)


CHANGELOG = """\
### October 06, 2026

**Changes**
- **wdk-wallet** ([v1.0.0-beta.22](https://github.com/tetherto/wdk-wallet/releases/tag/v1.0.0-beta.22)): [Breaking] Add required `IDisposable.disposed` and export [DisposalError](/x).
- **Rhino.fi SDA** ([v1.1.0](https://www.npmjs.com/package/@rhino.fi/wdk-protocol-sda-rhinofi/v/1.1.0)): Use the shared error hierarchy.
"""


class VersionKeyTest(unittest.TestCase):
    def test_version_key_orders_prereleases(self) -> None:
        shuffled = ["1.0.0", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0-beta.9", "v1.0.0-beta.20"]
        self.assertEqual(
            sorted(shuffled, key=versions.version_key),
            ["1.0.0-beta.9", "1.0.0-beta.11", "v1.0.0-beta.20", "1.0.0-rc.1", "1.0.0"],
        )

    def test_compare_verdicts(self) -> None:
        self.assertEqual(versions.compare("1.0.0-beta.9", "1.0.0-beta.11"), "atrás")
        self.assertEqual(versions.compare("1.0.0-beta.11", "1.0.0-beta.11"), "al día")
        self.assertEqual(versions.compare("1.0.0-beta.20", "1.0.0-beta.11"), "adelante")


class RepoStateTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def test_repo_state_counts_commits_after_release(self) -> None:
        repo = make_repo(self.root, "r", ["init", "Release: v0.3.1 (#140)", "a", "b"])
        result = versions.repo_state(repo)
        self.assertEqual(result.release, "v0.3.1")
        self.assertEqual(result.ahead_of_release, 2)
        self.assertEqual(len(result.head), 40)
        self.assertFalse(result.dirty)
        self.assertIsNone(result.origin_head)

    def test_repo_state_merge_release_subject(self) -> None:
        repo = make_repo(self.root, "r", ["init", "Merge pull request #137 from tetherto/release/v0.4.3"])
        result = versions.repo_state(repo)
        self.assertEqual(result.release, "v0.4.3")
        self.assertEqual(result.ahead_of_release, 0)

    def test_repo_state_without_release(self) -> None:
        repo = make_repo(self.root, "r", ["init", "feat: something"])
        result = versions.repo_state(repo)
        self.assertIsNone(result.release)
        self.assertIsNone(result.ahead_of_release)

    def test_repo_state_ignores_docs_commit_mentioning_a_release(self) -> None:
        repo = make_repo(self.root, "r", ["init", "Update Swidge documentation to release 1.3.0", "x"])
        result = versions.repo_state(repo)
        self.assertIsNone(result.release)
        self.assertIsNone(result.ahead_of_release)

    def test_repo_state_newest_release_wins(self) -> None:
        repo = make_repo(self.root, "r", ["Release: v0.3.0", "Release: v0.3.1", "x"])
        self.assertEqual(versions.repo_state(repo).release, "v0.3.1")

    def test_revert_of_release_is_not_a_release(self) -> None:
        repo = make_repo(self.root, "r", ["Release: v0.3.1", 'Revert "Release: v0.4.0"',
                                          'Revert "Merge pull request #9 from tetherto/release/v0.5.0"'])
        self.assertEqual(versions.repo_state(repo).release, "v0.3.1")
        self.assertIsNone(versions.RELEASE_RE.search('Revert "Release: v0.4.0"'))

    def test_repo_state_and_lockfiles_follow_origin_not_local_main(self) -> None:
        src = make_repo(self.root, "src", [])
        commit_files(src, {"package.json": '{"version": "0.3.1"}', "package-lock.json": lock("1.0.0-beta.11")},
                     "Release: v0.3.1")
        origin = self.root / "origin.git"
        git(self.root, "clone", "-q", "--bare", str(src), str(origin))
        local = self.root / "wdk-x"
        git(self.root, "clone", "-q", str(origin), str(local))
        old_head = versions._git(local, "rev-parse", "HEAD")
        git(src, "remote", "add", "origin", str(origin))
        commit_files(src, {"package.json": '{"version": "0.4.0"}', "package-lock.json": lock("1.0.0-beta.20")},
                     "Release: v0.4.0")
        git(src, "push", "-q", "origin", "main")
        git(local, "fetch", "-q", "origin")

        result = versions.repo_state(local)
        self.assertEqual(result.analyzed_ref, "origin/main")
        self.assertEqual(result.release, "v0.4.0")
        self.assertEqual(result.ahead_of_release, 0)
        self.assertEqual(result.package_version, "0.4.0")
        self.assertEqual(result.head, result.origin_head)
        self.assertEqual(result.local_head, old_head)
        self.assertEqual(result.behind_origin, 1)
        self.assertEqual(result.ahead_origin, 0)
        found, _ = versions.scan_lockfiles(local, result.head)
        self.assertEqual(found["@tetherto/wdk-wallet-evm"], ["1.0.0-beta.20"])

    def test_repo_state_without_origin_flags_local_ref(self) -> None:
        repo = make_repo(self.root, "r", ["init"])
        result = versions.repo_state(repo)
        self.assertEqual(result.analyzed_ref, "main (sin origin)")
        text = versions.render_last_sync([result], {}, "2026-10-26")
        self.assertIn("analyzed_ref: main (sin origin)", text)

    def test_repo_state_reports_dirty_and_package_version(self) -> None:
        repo = make_repo(self.root, "r", ["init"])
        (repo / "package.json").write_text('{"version": "0.2.0"}', encoding="utf-8")
        git(repo, "add", "package.json")
        git(repo, "commit", "-q", "-m", "add pkg")
        (repo / "untracked.txt").write_text("x", encoding="utf-8")
        result = versions.repo_state(repo)
        self.assertEqual(result.package_version, "0.2.0")
        self.assertTrue(result.dirty)


class DocsTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.docs = Path(tmp.name) / "wdk-docs"

    def write(self, rel: str, text: str) -> None:
        path = self.docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_callout_without_package_name_inferred(self) -> None:
        rel = "content/docs/sdk/wallet-modules/wallet-ton-gasless/index.mdx"
        self.write(rel, "These pages reflect `v1.0.0-beta.13`. Managers share clients.\n")
        found = versions.docs_callouts(self.docs)
        self.assertEqual(list(found), ["@tetherto/wdk-wallet-ton-gasless"])
        self.assertEqual(found["@tetherto/wdk-wallet-ton-gasless"].version, "1.0.0-beta.13")
        self.assertEqual(found["@tetherto/wdk-wallet-ton-gasless"].source, f"callout:{rel}")

    def test_callout_with_package_name_and_special_folders(self) -> None:
        self.write("content/docs/sdk/wallet-modules/wallet-evm/index.mdx",
                   "These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.20`. More.\n")
        self.write("content/docs/sdk/core-module/index.mdx", "These pages reflect `v1.0.0-beta.18`.\n")
        self.write("content/docs/cli/index.mdx", "These pages reflect `v1.0.0-beta.6`.\n")
        found = versions.docs_callouts(self.docs)
        self.assertEqual(found["@tetherto/wdk-wallet-evm"].version, "1.0.0-beta.20")
        self.assertEqual(found["@tetherto/wdk"].version, "1.0.0-beta.18")
        self.assertEqual(found["@tetherto/wdk-cli"].version, "1.0.0-beta.6")

    def test_changelog_entries_github_and_npm_links(self) -> None:
        entries = versions.changelog_entries(CHANGELOG)
        self.assertEqual(len(entries), 2)
        wallet, rhino = entries
        self.assertEqual((wallet.package, wallet.version), ("@tetherto/wdk-wallet", "1.0.0-beta.22"))
        self.assertTrue(wallet.breaking)
        self.assertEqual(wallet.date, "2026-10-06")
        self.assertEqual((rhino.package, rhino.version), ("@rhino.fi/wdk-protocol-sda-rhinofi", "1.1.0"))
        self.assertFalse(rhino.breaking)
        self.assertEqual(rhino.date, "2026-10-06")
        self.assertNotIn("](", wallet.summary)
        self.assertNotIn("`", wallet.summary)
        self.assertLessEqual(len(wallet.summary), 160)

    def test_changelog_generic_github_forms(self) -> None:
        text = (
            "### September 30, 2026\n"
            "- **swidge-symbiosis** ([v1.3.0](https://github.com/symbiosis-finance/wdk-protocol-swidge-symbiosis/tree/v1.3.0)): Execute routes.\n"
            "- **rgb-lightning** ([v0.1.0-beta.15](https://github.com/UTEXO-Protocol/wdk-rgb-lightning/releases/tag/v0.1.0-beta.15)): Add module.\n"
        )
        entries = versions.changelog_entries(text)
        self.assertEqual(
            [(e.package, e.version) for e in entries],
            [("github:symbiosis-finance/wdk-protocol-swidge-symbiosis", "1.3.0"),
             ("github:UTEXO-Protocol/wdk-rgb-lightning", "0.1.0-beta.15")],
        )
        self.assertEqual(versions.changelog_unmapped(text), [])

    def test_changelog_monorepo_tag_form(self) -> None:
        text = (
            "### September 20, 2026\n"
            "- **lending-morpho-evm** ([v1.0.5](https://github.com/morpho-org/sdks/releases/tag/%40morpho-org/wdk-protocol-lending-morpho-evm-v1.0.5)): Raise sdk.\n"
        )
        (entry,) = versions.changelog_entries(text)
        self.assertEqual((entry.package, entry.version), ("@morpho-org/wdk-protocol-lending-morpho-evm", "1.0.5"))

    def test_changelog_unmapped_link_is_reported_and_rendered(self) -> None:
        text = (
            "### September 20, 2026\n"
            "- **mystery** ([v2.0.0](https://example.com/releases/2.0.0)): Something.\n"
            "- **plain** no version link here.\n"
        )
        self.assertEqual(versions.changelog_entries(text), [])
        unmapped = versions.changelog_unmapped(text)
        self.assertEqual(len(unmapped), 1)
        self.assertIn("https://example.com/releases/2.0.0", unmapped[0])
        self.assertIn("2026-09-20", unmapped[0])
        rendered = versions.render_versions_md([state()], {}, {}, [], {}, unmapped)
        section = rendered.split("## Entradas del changelog sin paquete reconocido", 1)[1]
        self.assertIn("https://example.com/releases/2.0.0", section)

    def test_changelog_top_date_with_anchor(self) -> None:
        self.assertEqual(versions.changelog_top_date("### October 14, 2026 [#october-14-2026]\n"), "2026-10-14")
        self.assertEqual(versions.changelog_top_date("intro\n### October 14, 2026\n"), "2026-10-14")

    def test_changes_between_is_half_open(self) -> None:
        entries = [
            versions.ChangelogEntry("2026-09-01", "@tetherto/wdk-wallet-evm", "1.0.0-beta.11", False, "a"),
            versions.ChangelogEntry("2026-09-10", "@tetherto/wdk-wallet-evm", "1.0.0-beta.20", True, "b"),
            versions.ChangelogEntry("2026-09-10", "@tetherto/wdk-wallet", "1.0.0-beta.15", False, "c"),
            versions.ChangelogEntry("2026-10-01", "@tetherto/wdk-wallet-evm", "1.0.0-beta.21", False, "d"),
        ]
        found = versions.changes_between(entries, "@tetherto/wdk-wallet-evm", "1.0.0-beta.11", "1.0.0-beta.20")
        self.assertEqual([e.version for e in found], ["1.0.0-beta.20"])

    def test_documented_versions_callout_wins_over_changelog(self) -> None:
        self.write("content/docs/overview/changelog.mdx", CHANGELOG)
        self.write("content/docs/sdk/wallet-modules/wallet-evm/index.mdx",
                   "These pages reflect `@tetherto/wdk-wallet@1.0.0-beta.20`.\n")
        found = versions.documented_versions(self.docs)
        self.assertEqual(found["@tetherto/wdk-wallet"].version, "1.0.0-beta.20")
        self.assertTrue(found["@tetherto/wdk-wallet"].source.startswith("callout:"))
        self.assertEqual(found["@rhino.fi/wdk-protocol-sda-rhinofi"].version, "1.1.0")
        self.assertEqual(found["@rhino.fi/wdk-protocol-sda-rhinofi"].source, "changelog:2026-10-06")

    def test_install_packages_filters_to_wdk(self) -> None:
        self.write("content/docs/tools/mcp.mdx",
                   "```bash\nnpm install @tetherto/wdk-mcp-toolkit @modelcontextprotocol/sdk @x402/fetch\n```\n"
                   "```js\nimport { X } from '@tetherto/wdk-wallet/protocols'\n```\n")
        self.write("content/docs/other.md", "pnpm add @tetherto/wdk-wallet@1.0.0 @langchain/core\n")
        found = versions.docs_install_packages(self.docs)
        self.assertEqual(set(found), {"@tetherto/wdk-mcp-toolkit", "@tetherto/wdk-wallet"})
        self.assertEqual(found["@tetherto/wdk-mcp-toolkit"], "content/docs/tools/mcp.mdx")
        self.assertEqual(found["@tetherto/wdk-wallet"], "content/docs/other.md")

    def test_placeholder_scopes_excluded(self) -> None:
        self.write("content/docs/a.mdx",
                   "npm install @your-org/wdk-module-preferences @acme/wdk-x @myorg/wdk-y @tetherto/wdk-real\n"
                   "import M from '@example/wdk-wallet-example'\nimport N from '@my-org/wdk-z'\n")
        self.assertEqual(set(versions.docs_install_packages(self.docs)), {"@tetherto/wdk-real"})

    def test_removed_diff_lines_ignored(self) -> None:
        self.write("content/docs/a.mdx",
                   "```diff\n- import { A } from '@tetherto/wdk-old'\n+ import { A } from '@tetherto/wdk-new'\n```\n"
                   "```js\n- not a diff '@tetherto/wdk-kept'\nimport x from '@tetherto/wdk-after'\n```\n")
        self.assertEqual(set(versions.docs_install_packages(self.docs)),
                         {"@tetherto/wdk-new", "@tetherto/wdk-after"})

    def test_install_flags_and_line_continuation(self) -> None:
        self.write("content/docs/a.mdx",
                   "npm install -D @tetherto/wdk-x\nnpm i --save @a/wdk-y @b/other\n"
                   "npm install \\\n  @tetherto/wdk-z\n")
        self.assertEqual(set(versions.docs_install_packages(self.docs)),
                         {"@tetherto/wdk-x", "@a/wdk-y", "@tetherto/wdk-z"})

    def test_wdk_must_be_in_name_not_scope(self) -> None:
        self.write("content/docs/a.mdx", "npm install @wdk/tools @tetherto/wdk-ok\n")
        self.assertEqual(set(versions.docs_install_packages(self.docs)), {"@tetherto/wdk-ok"})

    def test_unscoped_wdk_protocol_package_collected(self) -> None:
        self.write("content/docs/sdk/swidge-modules/swidge-orchestra/guide.mdx",
                   "```bash\nnpm install wdk-protocol-swidge-orchestra @tetherto/wdk-wallet@1.0.0-beta.11\n"
                   "npm install wdk-cli wdk-foo wdk-wallet-custom\n```\n")
        found = versions.docs_install_packages(self.docs)
        self.assertIn("wdk-protocol-swidge-orchestra", found)
        self.assertIn("wdk-wallet-custom", found)
        self.assertNotIn("wdk-cli", found)
        self.assertNotIn("wdk-foo", found)

    def test_version_mention_used_when_no_callout_or_changelog(self) -> None:
        self.write("content/docs/ai/x402.mdx",
                   "The `@semanticio/wdk-wallet-evm-x402-facilitator@1.0.0-beta.2` package depends on "
                   "`@x402/evm@2.2.0` and `@your-org/wdk-x@9.9.9`.\n"
                   "```diff\n- `@tetherto/wdk-old@1.0.0`\n```\n")
        self.write("content/docs/ai/other.md", "Also `@semanticio/wdk-wallet-evm-x402-facilitator@1.0.0-beta.1`.\n")
        mentions = versions.docs_version_mentions(self.docs)
        self.assertEqual(set(mentions), {"@semanticio/wdk-wallet-evm-x402-facilitator"})
        found = versions.documented_versions(self.docs)["@semanticio/wdk-wallet-evm-x402-facilitator"]
        self.assertEqual(found.version, "1.0.0-beta.2")
        self.assertEqual(found.source, "mention:content/docs/ai/x402.mdx")

    def test_version_mention_never_overrides_callout_or_changelog(self) -> None:
        self.write("content/docs/overview/changelog.mdx", CHANGELOG)
        self.write("content/docs/sdk/wallet-modules/wallet-evm/index.mdx",
                   "These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.20`.\n")
        self.write("content/docs/ai/x402.mdx",
                   "Uses `@tetherto/wdk-wallet-evm@1.0.0-beta.99`, `@tetherto/wdk-wallet@1.0.0-beta.99` "
                   "and `wdk-protocol-swidge-orchestra@2.0.0`.\n")
        found = versions.documented_versions(self.docs)
        self.assertEqual(found["@tetherto/wdk-wallet-evm"].version, "1.0.0-beta.20")
        self.assertEqual(found["@tetherto/wdk-wallet"].version, "1.0.0-beta.22")
        self.assertEqual(found["@tetherto/wdk-wallet"].source, "changelog:2026-10-06")
        self.assertEqual(found["wdk-protocol-swidge-orchestra"].source, "mention:content/docs/ai/x402.mdx")

    def test_beta_callout_version_for_known_package(self) -> None:
        callout = ('<Callout type="warn">\n**Beta** - This package is in active development (`v1.0.0-beta.1`). '
                   'APIs may change.\n</Callout>\n')
        self.write("content/docs/ai/mcp-toolkit/index.mdx", callout)
        self.write("content/docs/ai/unknown-thing/index.mdx", callout)
        self.write("content/docs/ai/mcp-toolkit/setup.mdx", "npm install @tetherto/wdk-mcp-toolkit\n")
        found = versions.documented_versions(
            self.docs, versions.docs_install_packages(self.docs))
        toolkit = found["@tetherto/wdk-mcp-toolkit"]
        self.assertEqual(toolkit.version, "1.0.0-beta.1")
        self.assertEqual(toolkit.source, "callout-beta:content/docs/ai/mcp-toolkit/index.mdx")
        self.assertNotIn("@tetherto/wdk-unknown-thing", found)
        self.assertEqual(list(found), ["@tetherto/wdk-mcp-toolkit"])


class LockedPackagesTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = make_repo(Path(tmp.name), "repo", ["init"])

    def commit(self) -> None:
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "fixture")

    def test_locked_packages_npm_and_git_pin(self) -> None:
        lock = {"packages": {
            "": {"name": "x"},
            "node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.11"},
            "node_modules/@tetherto/wdk-wallet-evm-erc-4337/node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.9"},
            "node_modules/@tetherto/wdk-wallet-evm-erc-4337": {"version": "1.0.0-beta.5"},
            "node_modules/ethers": {"version": "6.14.4"},
        }}
        (self.repo / "package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
        self.commit()
        found = versions.locked_packages(self.repo)
        self.assertEqual(found["@tetherto/wdk-wallet-evm"], ["1.0.0-beta.11", "1.0.0-beta.9"])
        self.assertEqual(found["@tetherto/wdk-wallet-evm-erc-4337"], ["1.0.0-beta.5"])
        self.assertNotIn("ethers", found)

        app = self.repo / "apps" / "app"
        app.mkdir(parents=True)
        (app / "package.json").write_text(json.dumps({"dependencies": {
            "@tetherto/wdk-react-native-core": "github:tetherto/x#temp-rw-patch"}}), encoding="utf-8")
        nested = self.repo / "node_modules" / "dep"
        nested.mkdir(parents=True)
        (nested / "package.json").write_text(json.dumps({"dependencies": {
            "@tetherto/ignored": "github:tetherto/y#nope"}}), encoding="utf-8")
        git(self.repo, "add", "-A", "-f")
        git(self.repo, "commit", "-q", "-m", "pins")
        found = versions.locked_packages(self.repo)
        self.assertEqual(found["@tetherto/wdk-react-native-core"], ["git:temp-rw-patch"])
        self.assertNotIn("@tetherto/ignored", found)
        self.assertEqual(versions.compare("git:temp-rw-patch", "1.0.0-beta.21"), "git")

    def test_git_pins_multiple_files_keep_analysed_ref(self) -> None:
        for folder, tag in (("a", "v1.2.3"), ("b", "v9.9.9")):
            path = self.repo / folder / "package.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"dependencies": {
                f"@tetherto/wdk-{folder}": f"github:tetherto/wdk-{folder}#{tag}"}}), encoding="utf-8")
        self.commit()
        analysed = versions._git(self.repo, "rev-parse", "HEAD")
        with mock.patch.object(versions, "_show", wraps=versions._show) as show:
            found = versions.locked_packages(self.repo, analysed)
        self.assertEqual(found["@tetherto/wdk-a"], ["git:v1.2.3"])
        self.assertEqual(found["@tetherto/wdk-b"], ["git:v9.9.9"])
        pin_reads = [c.args[1] for c in show.call_args_list if c.args[2].endswith("package.json")]
        self.assertEqual(pin_reads, [analysed, analysed])

    def test_locked_packages_pnpm(self) -> None:
        text = (
            "lockfileVersion: '9.0'\n\n"
            "patchedDependencies:\n"
            "  '@tetherto/wdk-react-native-core@1.0.0':\n    path: p.patch\n\n"
            "packages:\n\n"
            "  '@tetherto/wdk-wallet@1.0.0-beta.17':\n    resolution: {integrity: x}\n\n"
            "  '@tetherto/wdk-react-native-core@https://codeload.github.com/tetherto/wdk-react-native-core/tar.gz/abc':\n    x: y\n\n"
            "snapshots:\n\n"
            "  '@tetherto/wdk-wallet@1.0.0-beta.17': {}\n\n"
            "  '@tetherto/pear-wrk-wdk@1.0.0-beta.8(bare-buffer@3.4.4)':\n    dependencies: {}\n"
        )
        (self.repo / "pnpm-lock.yaml").write_text(text, encoding="utf-8")
        self.commit()
        found = versions.locked_packages(self.repo)
        self.assertEqual(found, {
            "@tetherto/pear-wrk-wdk": ["1.0.0-beta.8"],
            "@tetherto/wdk-wallet": ["1.0.0-beta.17"],
        })

    def test_malformed_package_lock_is_reported_not_empty(self) -> None:
        (self.repo / "package-lock.json").write_text("{not json", encoding="utf-8")
        self.commit()
        found, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual(found, {})
        self.assertEqual([f for f, _ in problems], ["package-lock.json"])
        text = versions.render_versions_md(
            [state("repo")], {"repo": found}, {}, [], {}, lock_problems={"repo": problems})
        self.assertIn("lockfile ilegible: package-lock.json", text)
        self.assertNotIn("Sin paquetes", text)

    def test_lockfile_v1_without_packages_is_reported(self) -> None:
        (self.repo / "package-lock.json").write_text('{"lockfileVersion": 1, "dependencies": {}}', encoding="utf-8")
        self.commit()
        _, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual(len(problems), 1)
        self.assertIn("lockfileVersion 1", problems[0][1])

    def test_unsupported_pnpm_lock_is_reported(self) -> None:
        (self.repo / "pnpm-lock.yaml").write_text("lockfileVersion: '6.0'\n", encoding="utf-8")
        self.commit()
        _, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual([f for f, _ in problems], ["pnpm-lock.yaml"])

    def test_lockfile_scan_ignores_working_tree(self) -> None:
        (self.repo / "package-lock.json").write_text(lock("1.0.0-beta.11"), encoding="utf-8")
        self.commit()
        (self.repo / "package-lock.json").write_text(lock("1.0.0-beta.99"), encoding="utf-8")
        self.assertEqual(versions.locked_packages(self.repo), {"@tetherto/wdk-wallet-evm": ["1.0.0-beta.11"]})

    def test_clean_repo_without_lockfile_has_no_problems(self) -> None:
        self.assertEqual(versions.scan_lockfiles(self.repo), ({}, []))
        text = versions.render_versions_md([state("repo")], {"repo": {}}, {}, [], {})
        self.assertIn("Sin paquetes", text)


class RenderTest(unittest.TestCase):
    def documented(self) -> dict:
        return {
            "@tetherto/wdk-wallet-evm": versions.DocVersion("@tetherto/wdk-wallet-evm", "1.0.0-beta.20", "callout:x/index.mdx"),
            "@tetherto/wdk-swidge-lifi": versions.DocVersion("@tetherto/wdk-swidge-lifi", "1.0.0", "changelog:2026-10-01"),
        }

    def entries(self) -> list:
        return [
            versions.ChangelogEntry("2026-09-10", "@tetherto/wdk-wallet-evm", "1.0.0-beta.20", True, "Accept gas overrides"),
            versions.ChangelogEntry("2026-09-01", "@tetherto/wdk-wallet-evm", "1.0.0-beta.11", False, "old"),
        ]

    def test_catalog_lists_uninstalled_packages(self) -> None:
        text = versions.render_versions_md(
            [state()], {"repo-a": {"@tetherto/wdk-wallet-evm": ["1.0.0-beta.11"]}},
            self.documented(), self.entries(), {"@tetherto/wdk-swidge-lifi": "1.0.0"},
        )
        catalog = text.split("Catálogo: todos los paquetes documentados", 1)[1]
        rows = [line for line in catalog.splitlines() if "@tetherto/wdk-swidge-lifi" in line]
        self.assertEqual(len(rows), 1)
        self.assertIn("no instalado", rows[0])
        evm = [line for line in catalog.splitlines() if "@tetherto/wdk-wallet-evm" in line]
        self.assertIn("repo-a", evm[0])
        self.assertNotIn("[[", text)

    def test_install_only_package_in_catalog(self) -> None:
        pkg = "@tetherto/wdk-mcp-toolkit"
        documented = {**self.documented(), pkg: versions.DocVersion(pkg, "", "install:content/docs/tools/mcp.mdx")}
        text = versions.render_versions_md([state()], {"repo-a": {}}, documented, self.entries(), {pkg: "1.2.3"})
        catalog = text.split("Catálogo: todos los paquetes documentados", 1)[1]
        rows = [line for line in catalog.splitlines() if pkg in line]
        self.assertEqual(len(rows), 1)
        self.assertIn("— (install:content/docs/tools/mcp.mdx)", rows[0])
        self.assertIn("1.2.3", rows[0])
        self.assertIn("no instalado", rows[0])

    def test_github_id_merged_with_npm_name(self) -> None:
        gh, npm = "github:symbiosis-finance/wdk-protocol-swidge-symbiosis", "@symbiosis-finance/wdk-protocol-swidge-symbiosis"
        entries = [versions.ChangelogEntry("2026-09-20", gh, "1.0.0-beta.2", False, "x")]
        documented = {npm: versions.DocVersion(npm, "", "install:content/docs/a.mdx"),
                      gh: versions.DocVersion(gh, "1.0.0-beta.2", "changelog:2026-09-20")}
        text = versions.render_versions_md([state()], {}, documented, entries, {})
        catalog = text.split("Catálogo: todos los paquetes documentados", 1)[1]
        rows = [line for line in catalog.splitlines() if "wdk-protocol-swidge-symbiosis" in line]
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0].startswith(f"| {npm} |"))
        self.assertIn(f"1.0.0-beta.2 (changelog:2026-09-20 via {gh})", rows[0])

    def test_changelog_github_id_beats_mention_of_same_module(self) -> None:
        gh, npm = "github:acme-labs/wdk-protocol-x", "@acme-labs/wdk-protocol-x"
        documented = {npm: versions.DocVersion(npm, "1.0.0", "mention:content/docs/a.mdx"),
                      gh: versions.DocVersion(gh, "1.1.0", "changelog:2026-09-20")}
        catalog = versions._merge_github_ids(dict(documented))
        self.assertEqual(list(catalog), [npm])
        self.assertEqual(catalog[npm].version, "1.1.0")

    def test_empty_documented_version_not_compared(self) -> None:
        pkg = "@tetherto/wdk-mcp-toolkit"
        documented = {pkg: versions.DocVersion(pkg, "", "install:content/docs/a.mdx")}
        text = versions.render_versions_md([state()], {"repo-a": {pkg: ["0.1.0"]}}, documented, [], {})
        row = [line for line in text.splitlines() if line.startswith(f"| {pkg} | 0.1.0")][0]
        self.assertIn("| sin versión documentada |", row)
        catalog = text.split("Catálogo: todos los paquetes documentados", 1)[1]
        self.assertIn("repo-a 0.1.0", [line for line in catalog.splitlines() if pkg in line][0])

    def test_repo_section_shows_range_and_breaking(self) -> None:
        text = versions.render_versions_md(
            [state()], {"repo-a": {"@tetherto/wdk-wallet-evm": ["1.0.0-beta.11"]}},
            self.documented(), self.entries(), {},
        )
        row = [line for line in text.splitlines() if line.startswith("| @tetherto/wdk-wallet-evm |")][0]
        self.assertIn("| atrás |", row)
        self.assertIn("1, 1 breaking: 2026-09-10", row)
        self.assertIn("Cambios breaking entre mi versión y la documentada", text)
        self.assertIn("Accept gas overrides", text)

    def test_repos_table_reports_release_plus_commits(self) -> None:
        s = state("wdk-indexer-wrk-base", release="v0.3.1", release_commit="b" * 40,
                  release_date="2026-06-15", ahead_of_release=49,
                  origin_head="a" * 40, behind_origin=0, ahead_origin=0)
        text = versions.render_versions_md([s, state("no-release")], {}, {}, [], {})
        base = [line for line in text.splitlines() if line.startswith("| wdk-indexer-wrk-base")][0]
        self.assertIn("v0.3.1 + 49 commits", base)
        other = [line for line in text.splitlines() if line.startswith("| no-release")][0]
        self.assertIn("origin/main", other)

    def test_repo_section_says_local_checkout_is_behind_origin(self) -> None:
        s = state("wdk-x", origin_head="b" * 40, behind_origin=3, ahead_origin=0, local_head="c" * 40)
        text = versions.render_versions_md([s, state("wdk-y", origin_head="a" * 40, behind_origin=0, ahead_origin=0)],
                                           {}, {}, [], {})
        row = [line for line in text.splitlines() if line.startswith("| wdk-x |")][0]
        self.assertIn("ccccccc", row)
        self.assertIn("aaaaaaa", row)
        section = text.split("## wdk-x\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("tu checkout local está 3 commits detrás de origin/main; "
                      "las versiones de esta tabla son las de origin/main", section)
        other = text.split("## wdk-y\n", 1)[1].split("\n## ", 1)[0]
        self.assertNotIn("tu checkout local", other)

    def test_catalog_flags_documented_newer_than_npm(self) -> None:
        pkg = "@tetherto/wdk-mcp-toolkit"
        documented = {**self.documented(), pkg: versions.DocVersion(pkg, "1.0.0-beta.1", "callout-beta:x/index.mdx")}
        npm = {pkg: "0.0.0", "@tetherto/wdk-wallet-evm": "1.0.0-beta.24", "@tetherto/wdk-swidge-lifi": "no publicado (404)"}
        text = versions.render_versions_md([state()], {}, documented, self.entries(), npm)
        catalog = text.split("Catálogo: todos los paquetes documentados", 1)[1]
        row = [line for line in catalog.splitlines() if line.startswith(f"| {pkg} |")][0]
        self.assertIn("| documentada no publicada en npm |", row)
        for other in ("@tetherto/wdk-wallet-evm", "@tetherto/wdk-swidge-lifi"):
            line = [line for line in catalog.splitlines() if line.startswith(f"| {other} |")][0]
            self.assertNotIn("documentada no publicada", line)

    def test_git_pin_is_not_compared(self) -> None:
        text = versions.render_versions_md(
            [state()], {"repo-a": {"@tetherto/wdk-wallet-evm": ["git:temp-rw-patch"]}},
            self.documented(), self.entries(), {},
        )
        row = [line for line in text.splitlines() if line.startswith("| @tetherto/wdk-wallet-evm |")][0]
        self.assertIn("git:temp-rw-patch", row)
        self.assertIn("| git |", row)

    def test_last_sync_format(self) -> None:
        s = state("wdk-indexer-wrk-base", release="v0.3.1", release_commit="b" * 40,
                  release_date="2026-06-15", ahead_of_release=49,
                  origin_head="a" * 40, behind_origin=0, ahead_origin=0)
        docs = state("wdk-docs")
        site = {"site_changelog_top": "2026-10-14", "repo_changelog_top": "2026-10-14", "site_matches_repo": "yes"}
        text = versions.render_last_sync([s, docs], site, "2026-10-26")
        sections = text.split("\n## ")
        base = sections[1].splitlines()
        self.assertEqual(base[0], "wdk-indexer-wrk-base")
        self.assertEqual(base[1], "branch: main")
        self.assertEqual(base[2], f"commit: {'a' * 40}")
        self.assertEqual(base[3], "date: 2026-07-01")
        self.assertEqual(base[4], "analyzed_ref: origin/main")
        self.assertIn("deployed_release: v0.3.1", base)
        self.assertIn("ahead_of_release: 49", base)
        self.assertIn("analyzed_on: 2026-10-26", base)
        doc = sections[2]
        self.assertIn("deployed_release: none (origin/main)", doc)
        self.assertIn("site_matches_repo: yes", doc)
        self.assertNotIn("site_matches_repo", sections[1])
        self.assertIn("privados", text)


class DocsSiteTest(unittest.TestCase):
    def decide(self, site_top: str, repo_top: str) -> dict:
        with mock.patch.object(versions, "_site_changelog_top", return_value=site_top):
            return versions._docs_site(repo_top)

    def test_site_matches_repo_after_normalizing_anchor(self) -> None:
        site_top = versions.changelog_top_date("### October 14, 2026 [#october-14-2026]\n")
        repo_top = versions.changelog_top_date("### October 14, 2026\n")
        self.assertEqual(self.decide(site_top, repo_top)["site_matches_repo"], "yes")

    def test_site_differs_from_repo(self) -> None:
        result = self.decide("2026-10-14", "2026-10-07")
        self.assertEqual(result["site_matches_repo"], "no")
        self.assertEqual(result["site_changelog_top"], "2026-10-14")
        self.assertEqual(result["repo_changelog_top"], "2026-10-07")

    def test_unknown_when_site_unreachable_or_repo_empty(self) -> None:
        self.assertEqual(self.decide("unknown", "2026-10-14")["site_matches_repo"], "unknown")
        self.assertEqual(self.decide("2026-10-14", "")["site_matches_repo"], "unknown")


class SiteFetchTest(unittest.TestCase):
    def test_site_http_exception_returns_unknown(self) -> None:
        with mock.patch.object(versions.urllib.request, "urlopen", side_effect=http.client.BadStatusLine("x")):
            self.assertEqual(versions._site_changelog_top(), "unknown")

    def test_site_request_sends_a_user_agent(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b"### October 14, 2026 [#october-14-2026]\n"
        with mock.patch.object(versions.urllib.request, "urlopen", return_value=response) as opened:
            top = versions._site_changelog_top()
        self.assertEqual(top, "2026-10-14")
        request = opened.call_args.args[0]
        self.assertTrue(request.get_header("User-agent"))


class NpmTest(unittest.TestCase):
    def run_npm(self, returncode: int, stdout: str = "", stderr: str = "") -> str:
        done = subprocess.CompletedProcess([], returncode, stdout, stderr)
        with mock.patch.object(versions.subprocess, "run", return_value=done):
            return versions._npm_latest_one("@tetherto/x")[1]

    def test_npm_cells_distinguish_version_404_and_error(self) -> None:
        self.assertEqual(self.run_npm(0, "1.2.3\n"), "1.2.3")
        self.assertEqual(self.run_npm(1, stderr="npm error code E404\nnpm error 404 Not Found"), "no publicado (404)")
        self.assertEqual(self.run_npm(1, stderr="npm error code ETIMEDOUT"), "error")
        with mock.patch.object(versions.subprocess, "run", side_effect=OSError("no npm")):
            self.assertEqual(versions._npm_latest_one("@tetherto/x")[1], "error")


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name)
        self.vault = self.workspace / "wdk-vault"
        (self.vault / "_meta").mkdir(parents=True)

    def run_main(self, argv: list[str], npm: dict | None = None) -> tuple[int, str]:
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err), \
                mock.patch.object(versions, "_site_changelog_top", return_value="2026-10-06"), \
                mock.patch.object(versions, "_fetch_npm_latest", return_value=npm or {}) as fetch:
            code = versions.main(argv, self.vault)
        if "--npm" not in argv:
            fetch.assert_not_called()
        return code, err.getvalue()

    def make_docs(self) -> Path:
        docs = make_repo(self.workspace, "wdk-docs", [])
        commit_files(docs, {
            "content/docs/sdk/wallet-modules/wallet-evm/index.mdx":
                "These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.20`.\n",
            "content/docs/overview/changelog.mdx": CHANGELOG,
            "package-lock.json": json.dumps({"packages": {
                "node_modules/@tetherto/docs-seo-x": {"version": "1.0.0"}}}),
        }, "docs")
        return docs

    def write_repos_txt(self, text: str) -> None:
        (self.vault / "_meta" / "repos.txt").write_text(text, encoding="utf-8")

    def read(self, name: str) -> str:
        return (self.vault / "_meta" / name).read_text(encoding="utf-8")

    def section(self, name: str) -> str:
        return self.read("last-sync.md").split(f"\n## {name}\n", 1)[1].split("\n## ", 1)[0]

    def test_checkpoint_named_repo_only_advances_that_repo(self) -> None:
        a = make_repo(self.workspace, "wdk-a", ["init", "Release: v0.3.1"])
        b = make_repo(self.workspace, "wdk-b", ["init"])
        self.make_docs()
        self.write_repos_txt("wdk-a\nwdk-b\nwdk-docs docs-only\n")
        self.assertEqual(self.run_main(["--checkpoint"])[0], 0)
        old_b = self.section("wdk-b")
        old_b_lines = [line for line in old_b.splitlines() if line.startswith(("commit:", "date:", "analyzed_on:"))]
        self.assertEqual(len(old_b_lines), 3)
        text = self.read("last-sync.md").replace("analyzed_on: ", "analyzed_on: 1999-01-01 was ")
        (self.vault / "_meta" / "last-sync.md").write_text(text, encoding="utf-8")
        git(a, "commit", "-q", "--allow-empty", "-m", "Release: v0.4.0")
        git(b, "commit", "-q", "--allow-empty", "-m", "Release: v9.9.9")

        code, _ = self.run_main(["--checkpoint", "wdk-a"])
        self.assertEqual(code, 0)
        new_a, new_b = self.section("wdk-a"), self.section("wdk-b")
        self.assertIn(f"commit: {versions._git(a, 'rev-parse', 'HEAD')}", new_a)
        self.assertIn("deployed_release: v0.4.0", new_a)
        self.assertNotIn("1999-01-01", new_a)
        for line in old_b_lines:
            expected = line.replace("analyzed_on: ", "analyzed_on: 1999-01-01 was ")
            self.assertIn(expected + "\n", new_b + "\n")
        self.assertNotIn(f"commit: {versions._git(b, 'rev-parse', 'HEAD')}", new_b.splitlines())
        self.assertIn("deployed_release: v9.9.9", new_b)
        self.assertIn("1999-01-01", self.section("wdk-docs"))

    def test_checkpoint_unknown_repo_exits_2(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        self.make_docs()
        code, err = self.run_main(["--checkpoint", "wdk-nope"])
        self.assertEqual(code, 2)
        self.assertIn("wdk-nope", err)
        self.assertFalse((self.vault / "_meta" / "last-sync.md").exists())

    def test_npm_header_and_values_kept_without_npm(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        self.make_docs()
        npm = {"@tetherto/wdk-wallet-evm": "1.0.0-beta.24", "@tetherto/wdk-wallet": "no publicado (404)"}
        self.assertEqual(self.run_main(["--npm"], npm)[0], 0)
        today = versions.date.today().isoformat()
        self.assertIn(f"npm consultado: sí ({today})", self.read("versions.md"))
        data = json.loads(self.read("versions.json"))
        self.assertEqual(data["npm"], {"queried_on": today, "latest": npm})

        data["npm"]["queried_on"] = "2026-10-01"
        (self.vault / "_meta" / "versions.json").write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(self.run_main([])[0], 0)
        text = self.read("versions.md")
        self.assertIn("npm consultado: no", text)
        self.assertIn("valores npm del 2026-10-01", text)
        row = [line for line in text.split("Catálogo", 1)[1].splitlines()
               if line.startswith("| @tetherto/wdk-wallet-evm |")][0]
        self.assertIn("| 1.0.0-beta.24 |", row)
        self.assertEqual(json.loads(self.read("versions.json"))["npm"]["queried_on"], "2026-10-01")

    def test_npm_header_without_any_values(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        self.make_docs()
        self.run_main([])
        text = self.read("versions.md")
        self.assertIn("npm consultado: no", text)
        self.assertNotIn("valores npm del", text)

    def test_unanalyzable_repo_reported_and_skipped(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        make_repo(self.workspace, "wdk-empty", [])
        self.make_docs()
        self.write_repos_txt("wdk-a\nwdk-empty\nwdk-docs\n")
        code, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("wdk-empty: no analizable:", err)
        self.assertIn("wdk-empty: no analizable:", self.read("versions.md"))
        self.assertEqual(sorted(json.loads(self.read("versions.json"))["repos"]), ["wdk-a", "wdk-docs"])
        (self.vault / "_meta" / "last-sync.md").write_text(
            "# last-sync\n\n## wdk-empty\nbranch: main\ncommit: abc\ndate: 2026-01-01\nanalyzed_on: 2026-01-02\n",
            encoding="utf-8")
        self.assertEqual(self.run_main(["--checkpoint"])[0], 0)
        self.assertEqual(self.section("wdk-empty").split(),
                         ["branch:", "main", "commit:", "abc", "date:", "2026-01-01", "analyzed_on:", "2026-01-02"])

    def test_repos_txt_limits_discovery(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        make_repo(self.workspace, "client-project", ["init"])
        self.make_docs()
        self.write_repos_txt("# repos del vault\nwdk-a\n\nwdk-docs docs-only  # solo doc\n")
        code, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertNotIn("repos.txt", err)
        self.assertEqual(sorted(json.loads(self.read("versions.json"))["repos"]), ["wdk-a", "wdk-docs"])

    def test_missing_repos_txt_warns_and_autodiscovers(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        make_repo(self.workspace, "client-project", ["init"])
        self.make_docs()
        code, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("warning: falta _meta/repos.txt", err)
        self.assertEqual(sorted(json.loads(self.read("versions.json"))["repos"]),
                         ["client-project", "wdk-a", "wdk-docs"])

    def test_docs_only_repo_skips_lockfile_scan(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        self.make_docs()
        self.write_repos_txt("wdk-a\nwdk-docs docs-only\n")
        self.run_main([])
        data = json.loads(self.read("versions.json"))
        self.assertEqual(data["repos"]["wdk-docs"]["locked"], {})
        self.assertNotIn("@tetherto/docs-seo-x", data["packages"])
        self.assertIn("docs-only", self.read("versions.md").split("## wdk-docs\n", 1)[1].split("\n## ", 1)[0])
        self.write_repos_txt("wdk-a\nwdk-docs\n")
        self.run_main([])
        self.assertIn("@tetherto/docs-seo-x", json.loads(self.read("versions.json"))["packages"])

    def test_docs_read_from_analyzed_ref(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        docs = self.make_docs()
        (docs / "content/docs/sdk/wallet-modules/wallet-evm/index.mdx").write_text(
            "These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.99`.\n", encoding="utf-8")
        self.run_main([])
        catalog = self.read("versions.md").split("Catálogo", 1)[1]
        row = [line for line in catalog.splitlines() if line.startswith("| @tetherto/wdk-wallet-evm |")][0]
        self.assertIn("1.0.0-beta.20", row)

    def test_main_fails_cleanly_without_docs(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        code, err = self.run_main([])
        self.assertEqual(code, 2)
        self.assertIn("wdk-docs", err)

    def test_main_writes_md_and_json(self) -> None:
        repo = make_repo(self.workspace, "wdk-a", ["init", "Release: v0.3.1", "a"])
        (repo / "package-lock.json").write_text(json.dumps({"packages": {
            "node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.11"}}}), encoding="utf-8")
        docs = make_repo(self.workspace, "wdk-docs", [])
        commit_files(docs, {
            "content/docs/sdk/wallet-modules/wallet-evm/index.mdx":
                "These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.20`.\n"
                "npm install @tetherto/wdk-mcp-toolkit @langchain/core\n",
            "content/docs/overview/changelog.mdx": CHANGELOG,
        }, "docs")
        code, _ = self.run_main([])
        self.assertEqual(code, 0)
        data = json.loads((self.vault / "_meta" / "versions.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(data), ["generated", "npm", "packages", "repos"])
        self.assertEqual(sorted(data["repos"]), ["wdk-a", "wdk-docs"])
        self.assertEqual(data["repos"]["wdk-a"]["release"], "v0.3.1")
        self.assertEqual(data["packages"], sorted(set(data["packages"])))
        for expected in ("@tetherto/wdk-wallet-evm", "@tetherto/wdk-wallet", "@rhino.fi/wdk-protocol-sda-rhinofi",
                         "@tetherto/wdk-mcp-toolkit"):
            self.assertIn(expected, data["packages"])
        self.assertNotIn("@langchain/core", data["packages"])
        self.assertTrue((self.vault / "_meta" / "versions.md").exists())
        self.assertFalse((self.vault / "_meta" / "last-sync.md").exists())


if __name__ == "__main__":
    unittest.main()
