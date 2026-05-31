#!/usr/bin/env python3
"""Static audit for ARS guided-writing mode protocol.

Checks that all guided-writing mode files exist, contain required content,
and follow the protocol specification.

Exit codes: 0 on pass, 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ERRORS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)
    print(f"FAIL: {msg}")


def check_protocol() -> None:
    path = REPO_ROOT / "academic-paper" / "references" / "guided_mode_protocol.md"
    if not path.exists():
        error("guided_mode_protocol.md does not exist")
        return

    content = path.read_text(encoding="utf-8")

    # Check Steps 0-6
    steps = [f"Step {i}:" for i in range(7)]
    missing = [s for s in steps if s not in content]
    if missing:
        error(f"guided_mode_protocol.md missing steps: {missing}")
    else:
        print("OK: guided_mode_protocol.md contains Steps 0-6")

    # Check v3.6.6 exemption note
    if "exempt from the generator-evaluator contract" not in content:
        error("guided_mode_protocol.md missing v3.6.6 contract exemption note")
    else:
        print("OK: guided_mode_protocol.md contains v3.6.6 exemption")


def check_mentor() -> None:
    path = REPO_ROOT / "academic-paper" / "agents" / "guided_mentor_agent.md"
    if not path.exists():
        error("guided_mentor_agent.md does not exist")
        return

    content = path.read_text(encoding="utf-8")

    if "[DRAFT: review required]" not in content:
        error("guided_mentor_agent.md missing '[DRAFT: review required]'")
    else:
        print("OK: guided_mentor_agent.md contains draft label")

    # Check 5 rounds
    rounds = ["Round 1:", "Round 2:", "Round 3:", "Round 4:", "Round 5:"]
    missing = [r for r in rounds if r not in content]
    if missing:
        error(f"guided_mentor_agent.md missing rounds: {missing}")
    else:
        print("OK: guided_mentor_agent.md contains all 5 rounds")


def check_reviewer() -> None:
    path = REPO_ROOT / "academic-paper" / "agents" / "guided_reviewer_agent.md"
    if not path.exists():
        error("guided_reviewer_agent.md does not exist")
        return

    content = path.read_text(encoding="utf-8")

    classes = ["Logic", "Evidence", "Expression", "Structure", "Deepening"]
    missing = [c for c in classes if c not in content]
    if missing:
        error(f"guided_reviewer_agent.md missing question classes: {missing}")
    else:
        print("OK: guided_reviewer_agent.md contains all 5 question classes")

    if "Detection Heuristics" not in content:
        error("guided_reviewer_agent.md missing 'Detection Heuristics' subsection")
    else:
        print("OK: guided_reviewer_agent.md contains Detection Heuristics")

    # Check severity priority
    priority_pattern = r"Evidence\s*\>\s*Logic\s*\>\s*Expression\s*\>\s*Structure\s*\>\s*Deepening"
    if not re.search(priority_pattern, content):
        error("guided_reviewer_agent.md missing severity priority order")
    else:
        print("OK: guided_reviewer_agent.md contains severity priority")


def check_registry() -> None:
    path = REPO_ROOT / "MODE_REGISTRY.md"
    content = path.read_text(encoding="utf-8")

    if "guided-writing" not in content:
        error("MODE_REGISTRY.md missing 'guided-writing' entry")
    else:
        print("OK: MODE_REGISTRY.md contains guided-writing")

    # Check that count was updated
    if "## academic-paper (11 modes)" not in content:
        error("MODE_REGISTRY.md academic-paper header not updated to 11 modes")
    else:
        print("OK: MODE_REGISTRY.md mode count updated")


def check_command() -> None:
    path = REPO_ROOT / "commands" / "ars-guided-writing.md"
    if not path.exists():
        error("commands/ars-guided-writing.md does not exist")
        return

    content = path.read_text(encoding="utf-8")

    if "description:" not in content:
        error("commands/ars-guided-writing.md missing 'description:' frontmatter")
    else:
        print("OK: commands/ars-guided-writing.md has description frontmatter")

    if "model:" not in content:
        error("commands/ars-guided-writing.md missing 'model:' frontmatter")
    else:
        print("OK: commands/ars-guided-writing.md has model frontmatter")


def main() -> int:
    print("Checking guided-writing mode protocol...\n")

    check_protocol()
    check_mentor()
    check_reviewer()
    check_registry()
    check_command()

    print()
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s)")
        return 1

    print("PASSED: All checks OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
