"""Unit tests for check_guided_mode_protocol.py (ARS guided-writing lint)."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestGuidedModeProtocol(unittest.TestCase):
    """Test guided-writing mode protocol compliance."""

    def test_protocol_has_all_steps(self) -> None:
        path = REPO_ROOT / "academic-paper" / "references" / "guided_mode_protocol.md"
        content = path.read_text(encoding="utf-8")
        for i in range(7):
            self.assertIn(f"Step {i}:", content, f"Missing Step {i}")

    def test_mentor_has_draft_label(self) -> None:
        path = REPO_ROOT / "academic-paper" / "agents" / "guided_mentor_agent.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("[DRAFT: review required]", content)

    def test_reviewer_has_all_classes(self) -> None:
        path = REPO_ROOT / "academic-paper" / "agents" / "guided_reviewer_agent.md"
        content = path.read_text(encoding="utf-8")
        for cls in ("Logic", "Evidence", "Expression", "Structure", "Deepening"):
            self.assertIn(cls, content, f"Missing class: {cls}")

    def test_reviewer_has_detection_heuristics(self) -> None:
        path = REPO_ROOT / "academic-paper" / "agents" / "guided_reviewer_agent.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("Detection Heuristics", content)

    def test_registry_has_entry(self) -> None:
        path = REPO_ROOT / "MODE_REGISTRY.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("guided-writing", content)
        self.assertIn("## academic-paper (11 modes)", content)

    def test_command_has_frontmatter(self) -> None:
        path = REPO_ROOT / "commands" / "ars-guided-writing.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("description:", content)
        self.assertIn("model:", content)

    def test_lint_passes_on_valid_repo(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/check_guided_mode_protocol.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"Lint failed:\n{result.stdout}\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
