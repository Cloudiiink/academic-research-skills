"""Unit tests for guided_mentor_agent.md content compliance."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestGuidedMentorAgent(unittest.TestCase):
    """Test guided_mentor_agent.md protocol compliance."""

    def setUp(self) -> None:
        self.path = REPO_ROOT / "academic-paper" / "agents" / "guided_mentor_agent.md"
        self.content = self.path.read_text(encoding="utf-8")

    def test_round_1_commitment_question(self) -> None:
        self.assertIn("COMMITMENT", self.content)
        self.assertIn("hardest part", self.content.lower())

    def test_round_2_options_mechanism(self) -> None:
        self.assertIn("2-3", self.content)
        self.assertIn("Pros", self.content)
        self.assertIn("Cons", self.content)

    def test_round_3_draft_label(self) -> None:
        self.assertIn("[DRAFT: review required]", self.content)

    def test_round_4_feedback_dimensions(self) -> None:
        self.assertIn("Logic", self.content)
        self.assertIn("Evidence", self.content)
        self.assertIn("Expression", self.content)

    def test_feedback_restraint(self) -> None:
        self.assertIn("max 3", self.content.lower())


if __name__ == "__main__":
    unittest.main()
