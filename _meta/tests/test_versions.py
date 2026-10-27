import contextlib
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


def state(name: str = "repo-a", **overrides: object) -> "versions.RepoState":
    fields = dict(
        name=name, branch="main", head="a" * 40, head_date="2026-07-01",
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


class LockedPackagesTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "repo"
        self.repo.mkdir()

    def test_locked_packages_npm_and_git_pin(self) -> None:
        lock = {"packages": {
            "": {"name": "x"},
            "node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.11"},
            "node_modules/@tetherto/wdk-wallet-evm-erc-4337/node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.9"},
            "node_modules/@tetherto/wdk-wallet-evm-erc-4337": {"version": "1.0.0-beta.5"},
            "node_modules/ethers": {"version": "6.14.4"},
        }}
        (self.repo / "package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
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
        found = versions.locked_packages(self.repo)
        self.assertEqual(found["@tetherto/wdk-react-native-core"], ["git:temp-rw-patch"])
        self.assertNotIn("@tetherto/ignored", found)
        self.assertEqual(versions.compare("git:temp-rw-patch", "1.0.0-beta.21"), "git")

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
        found = versions.locked_packages(self.repo)
        self.assertEqual(found, {
            "@tetherto/pear-wrk-wdk": ["1.0.0-beta.8"],
            "@tetherto/wdk-wallet": ["1.0.0-beta.17"],
        })

    def test_malformed_package_lock_is_reported_not_empty(self) -> None:
        (self.repo / "package-lock.json").write_text("{not json", encoding="utf-8")
        found, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual(found, {})
        self.assertEqual([f for f, _ in problems], ["package-lock.json"])
        text = versions.render_versions_md(
            [state("repo")], {"repo": found}, {}, [], {}, lock_problems={"repo": problems})
        self.assertIn("lockfile ilegible: package-lock.json", text)
        self.assertNotIn("Sin paquetes", text)

    def test_lockfile_v1_without_packages_is_reported(self) -> None:
        (self.repo / "package-lock.json").write_text('{"lockfileVersion": 1, "dependencies": {}}', encoding="utf-8")
        _, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual(len(problems), 1)
        self.assertIn("lockfileVersion 1", problems[0][1])

    def test_unsupported_pnpm_lock_is_reported(self) -> None:
        (self.repo / "pnpm-lock.yaml").write_text("lockfileVersion: '6.0'\n", encoding="utf-8")
        _, problems = versions.scan_lockfiles(self.repo)
        self.assertEqual([f for f, _ in problems], ["pnpm-lock.yaml"])

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
    def test_site_request_sends_a_user_agent(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b"### October 14, 2026 [#october-14-2026]\n"
        with mock.patch.object(versions.urllib.request, "urlopen", return_value=response) as opened:
            top = versions._site_changelog_top()
        self.assertEqual(top, "2026-10-14")
        request = opened.call_args.args[0]
        self.assertTrue(request.get_header("User-agent"))


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name)
        self.vault = self.workspace / "wdk-vault"
        (self.vault / "_meta").mkdir(parents=True)

    def run_main(self, argv: list[str]) -> tuple[int, str]:
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = versions.main(argv, self.vault)
        return code, err.getvalue()

    def test_main_fails_cleanly_without_docs(self) -> None:
        make_repo(self.workspace, "wdk-a", ["init"])
        code, err = self.run_main([])
        self.assertEqual(code, 2)
        self.assertIn("wdk-docs", err)

    def test_main_writes_md_and_json(self) -> None:
        repo = make_repo(self.workspace, "wdk-a", ["init", "Release: v0.3.1", "a"])
        (repo / "package-lock.json").write_text(json.dumps({"packages": {
            "node_modules/@tetherto/wdk-wallet-evm": {"version": "1.0.0-beta.11"}}}), encoding="utf-8")
        docs = make_repo(self.workspace, "wdk-docs", ["init"])
        page = docs / "content" / "docs" / "sdk" / "wallet-modules" / "wallet-evm" / "index.mdx"
        page.parent.mkdir(parents=True)
        page.write_text("These pages reflect `@tetherto/wdk-wallet-evm@1.0.0-beta.20`.\n"
                        "npm install @tetherto/wdk-mcp-toolkit @langchain/core\n", encoding="utf-8")
        (docs / "content" / "docs" / "overview").mkdir()
        (docs / "content" / "docs" / "overview" / "changelog.mdx").write_text(CHANGELOG, encoding="utf-8")
        code, _ = self.run_main([])
        self.assertEqual(code, 0)
        data = json.loads((self.vault / "_meta" / "versions.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(data), ["generated", "packages", "repos"])
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
