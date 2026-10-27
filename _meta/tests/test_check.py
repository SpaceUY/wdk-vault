import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

META = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check", META / "check.py")
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


def note(type_: str, source: str = "repo-a/file.md", extra: str = "", body: str = "Una afirmacion.\n") -> str:
    return f"---\ntype: {type_}\nstatus: shipped\nsource:\n  - {source}\n{extra}---\n# T\n\n{body}"


class CheckTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name) / "workspace"
        self.vault = self.workspace / "vault"
        (self.workspace / "repo-a").mkdir(parents=True)
        (self.workspace / "repo-a" / "file.md").write_text("x", encoding="utf-8")
        (self.vault / "_meta").mkdir(parents=True)
        shutil.copy(META / "relations.md", self.vault / "_meta" / "relations.md")
        self.write("concepts/A.md", note("concept"))

    def write(self, rel: str, text: str) -> None:
        path = self.vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_check(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return check.main(self.vault, self.workspace)

    def test_clean_vault_passes(self) -> None:
        self.assertEqual(self.run_check(), 0)

    def test_failures_reset_between_calls(self) -> None:
        self.write("concepts/Bad.md", note("concept", "repo-a/missing.md"))
        self.assertEqual(self.run_check(), 1)
        (self.vault / "concepts" / "Bad.md").unlink()
        self.assertEqual(self.run_check(), 0)

    def test_missing_source_path_fails(self) -> None:
        self.write("concepts/A.md", note("concept", "repo-a/missing.md"))
        self.assertEqual(self.run_check(), 1)

    def test_unknown_repo_prefix_fails(self) -> None:
        self.write("concepts/A.md", note("concept", "repo-typo/file.md"))
        self.assertEqual(self.run_check(), 1)

    def test_https_source_passes(self) -> None:
        self.write("concepts/A.md", note("concept", "https://example.com/doc"))
        self.assertEqual(self.run_check(), 0)

    def test_service_without_detect_fails(self) -> None:
        self.write("services/S.md", note("service"))
        self.assertEqual(self.run_check(), 1)

    def test_service_with_detect_passes(self) -> None:
        self.write("services/S.md", note("service", extra="detect:\n  - '@moonpay/sdk'\n"))
        self.assertEqual(self.run_check(), 0)

    def test_unknown_package_fails(self) -> None:
        (self.vault / "_meta" / "versions.json").write_text(
            json.dumps({"packages": ["@tetherto/wdk"]}), encoding="utf-8"
        )
        self.write("systems/wdk-nope.md", note("system", extra="package: '@tetherto/nope'\n"))
        self.assertEqual(self.run_check(), 1)

    def test_known_package_passes_with_quotes(self) -> None:
        (self.vault / "_meta" / "versions.json").write_text(
            json.dumps({"packages": ["@tetherto/wdk"]}), encoding="utf-8"
        )
        self.write("systems/wdk.md", note("system", extra="package: '@tetherto/wdk'\n"))
        self.assertEqual(self.run_check(), 0)

    def test_package_check_skipped_without_versions_json(self) -> None:
        self.write("systems/wdk.md", note("system", extra="package: '@tetherto/anything'\n"))
        self.assertEqual(self.run_check(), 0)

    def test_can_replace_is_structural(self) -> None:
        self.write("concepts/B.md", note("concept", body="## Associative\n- can replace → [[A]]\n"))
        self.assertEqual(self.run_check(), 1)

    def test_can_replace_under_structural_passes(self) -> None:
        self.write("concepts/B.md", note("concept", body="## Structural\n- can replace → [[A]]\n"))
        self.assertEqual(self.run_check(), 0)

    def test_structural_cycle_fails(self) -> None:
        self.write("concepts/A.md", note("concept", body="## Structural\n- requires → [[B]]\n"))
        self.write("concepts/B.md", note("concept", body="## Structural\n- requires → [[A]]\n"))
        self.assertEqual(self.run_check(), 1)

    def test_dot_directories_are_ignored(self) -> None:
        self.write(".superpowers/notes/bad.md", "## Structural\n- bogus → [[Nope]]\n")
        self.write(".obsidian/bad.md", "## Structural\n- bogus → [[Nope]]\n")
        self.assertEqual(self.run_check(), 0)


if __name__ == "__main__":
    unittest.main()
