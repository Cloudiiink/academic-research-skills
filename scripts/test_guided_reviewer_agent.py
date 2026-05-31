"""Unit tests for guided_reviewer_agent.md content compliance."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestGuidedReviewerAgent(unittest.TestCase):
    """Test guided_reviewer_agent.md protocol compliance."""

    def setUp(self) -> None:
        self.path = REPO_ROOT / "academic-paper" / "agents" / "guided_reviewer_agent.md"
        self.content = self.path.read_text(encoding="utf-8")

    def test_five_question_classes_present(self) -> None:
        for cls in ("Logic", "Evidence", "Expression", "Structure", "Deepening"):
            self.assertIn(cls, self.content, f"Missing class: {cls}")

    def test_detection_heuristics_subsection(self) -> None:
        self.assertIn("Detection Heuristics", self.content)

    def test_severity_priority_order(self) -> None:
        pattern = r"Evidence\s*>\s*Logic\s*>\s*Expression\s*>\s*Structure\s*>\s*Deepening"
        self.assertRegex(self.content, pattern, "Severity priority order not found")

    def test_no_issues_fallback(self) -> None:
        self.assertIn("positive feedback", self.content.lower())
        self.assertIn("gentle probe", self.content.lower())

    def test_question_bank_count(self) -> None:
        # Count question marks in the Dynamic Question Bank table area
        bank_start = self.content.find("Dynamic Question Bank")
        self.assertGreater(bank_start, -1, "Missing Dynamic Question Bank")
        bank_section = self.content[bank_start:bank_start + 2000]
        questions = bank_section.count('"')
        # Each question is in quotes, so count quote pairs
        self.assertGreaterEqual(questions, 24, "Expected at least 12 questions (24 quotes)")


if __name__ == "__main__":
    unittest.main()
