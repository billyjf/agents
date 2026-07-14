from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "bin" / "agents-install"


class AgentsInstallTest(unittest.TestCase):
    def run_installer(
        self,
        *arguments: str,
        env: dict[str, str] | None = None,
        expected: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(INSTALLER), *arguments],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            expected,
            completed.returncode,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        return completed

    def test_project_install_preserves_instructions_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "CLAUDE.md").write_text("# Existing Claude guidance\n", encoding="utf-8")
            (target / "AGENTS.md").write_text("# Existing Codex guidance\n", encoding="utf-8")

            self.run_installer(str(target))
            self.run_installer(str(target), "--check")
            second = self.run_installer(str(target))

            self.assertNotIn("create", second.stdout)
            self.assertNotIn("update", second.stdout)
            claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
            codex = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Existing Claude guidance", claude)
            self.assertIn("# Existing Codex guidance", codex)
            self.assertEqual(1, claude.count("<!-- agentic-delivery:begin -->"))
            self.assertEqual(1, codex.count("<!-- agentic-delivery:begin -->"))

            with (target / ".codex/agents/qa.toml").open("rb") as handle:
                qa = tomllib.load(handle)
            self.assertEqual("qa", qa["name"])
            self.assertEqual("read-only", qa["sandbox_mode"])
            self.assertIn("independent quality owner", qa["developer_instructions"])

            lock = json.loads(
                (target / ".agents/agentic-delivery.lock.json").read_text(encoding="utf-8")
            )
            self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), lock["version"])
            self.assertEqual(["antigravity", "claude", "codex"], lock["harnesses"])

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = self.run_installer(str(target), "--dry-run")
            self.assertIn("Would install", result.stdout)
            self.assertEqual([], list(target.iterdir()))

    def test_modified_generated_file_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.run_installer(str(target))
            qa_path = target / ".claude/agents/qa.md"
            qa_path.write_text(qa_path.read_text(encoding="utf-8") + "\nmanual edit\n", encoding="utf-8")

            conflict = self.run_installer(str(target), expected=2)
            self.assertIn("Refusing to overwrite", conflict.stderr)
            self.run_installer(str(target), "--check", expected=1)
            self.run_installer(str(target), "--force")
            self.run_installer(str(target), "--check")
            self.assertNotIn("manual edit", qa_path.read_text(encoding="utf-8"))

    def test_global_install_uses_harness_native_locations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            env = os.environ.copy()
            env["HOME"] = str(home)
            self.run_installer("--global", env=env)
            self.run_installer("--global", "--check", env=env)

            self.assertTrue((home / ".claude/agents/qa.md").is_file())
            self.assertTrue((home / ".codex/agents/qa.toml").is_file())
            self.assertTrue((home / ".agents/skills/qa/SKILL.md").is_file())
            self.assertTrue(
                (home / ".gemini/config/plugins/agentic-delivery/plugin.json").is_file()
            )

    def test_harness_subset_updates_accumulate_in_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.run_installer(str(target), "--harness", "claude")
            self.run_installer(str(target), "--harness", "codex")
            lock = json.loads(
                (target / ".agents/agentic-delivery.lock.json").read_text(encoding="utf-8")
            )
            self.assertEqual(["claude", "codex"], lock["harnesses"])
            self.assertIn(".claude/agents/qa.md", lock["files"])
            self.assertIn(".codex/agents/qa.toml", lock["files"])
            self.run_installer(str(target), "--harness", "claude", "--check")


if __name__ == "__main__":
    unittest.main()
