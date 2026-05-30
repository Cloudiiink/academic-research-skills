"""Unit tests for guided-writing routing in SKILL.md."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestGuidedWritingRouting(unittest.TestCase):
    """Test guided-writing trigger keywords and mode differentiation."""

    def setUp(self) -> None:
        self.path = REPO_ROOT / "academic-paper" / "SKILL.md"
        self.content = self.path.read_text(encoding="utf-8")

    def test_en_triggers_present(self) -> None:
        en_triggers = [
            "guided writing",
            "write with me",
            "help me draft",
            "guide my drafting",
            "mentor mode writing",
        ]
        for trigger in en_triggers:
            self.assertIn(trigger, self.content, f"Missing EN trigger: {trigger}")

    def test_zhtw_triggers_present(self) -> None:
        zhtw_triggers = [
            "引導我寫",
            "一起寫論文",
            "導師模式",
            "陪寫論文",
            "逐段寫",
        ]
        for trigger in zhtw_triggers:
            self.assertIn(trigger, self.content, f"Missing zh-TW trigger: {trigger}")

    def test_zhcn_triggers_present(self) -> None:
        zhcn_triggers = [
            "引导我写",
            "一起写论文",
            "导师模式",
            "陪写论文",
            "逐段写",
        ]
        for trigger in zhcn_triggers:
            self.assertIn(trigger, self.content, f"Missing zh-CN trigger: {trigger}")

    def test_mode_differentiation_from_plan(self) -> None:
        # guided-writing should be mentioned as distinct from plan
        self.assertIn("Guided-Writing Mode Activation", self.content)
        self.assertIn("plan", self.content)

    def test_mode_differentiation_from_full(self) -> None:
        # full mode should still be referenced
        self.assertIn("full", self.content)


if __name__ == "__main__":
    unittest.main()
