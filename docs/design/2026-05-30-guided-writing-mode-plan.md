# Guided-Writing Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `guided-writing` mode to the `academic-paper` skill — a mentor-type mode where AI guides users through section-by-section drafting via Socratic dialogue, options, and dynamic feedback.

**Architecture:** Reuse existing pipeline infrastructure (`intake_agent`, `structure_architect_agent`, `argument_builder_agent`, `formatter_agent`) with mode-specific context prepended by orchestrator. Two new agents (`guided_mentor_agent`, `guided_reviewer_agent`) replace `draft_writer` and `peer_reviewer` for this mode. Zero existing agent files modified.

**Tech Stack:** Markdown (agent specs), Python 3 (lint + tests), GitHub Actions (CI)

---

## File Structure

| File | Role |
|------|------|
| `commands/ars-guided-writing.md` | Slash command definition for `/ars-guided-writing` |
| `academic-paper/agents/guided_mentor_agent.md` | Core mentor agent — per-section 5-round protocol |
| `academic-paper/agents/guided_reviewer_agent.md` | Conversational review agent — 5-class dynamic triggering |
| `academic-paper/references/guided_mode_protocol.md` | Canonical protocol — 6-step flow, activation rules, handoff |
| `academic-paper/examples/guided_mode_example.md` | Usage example demonstrating full guided-writing flow |
| `scripts/check_guided_mode_protocol.py` | CI lint — validates agent files + protocol + registry |
| `scripts/test_guided_mode_protocol.py` | Unit tests for lint script |
| `MODE_REGISTRY.md` | Add `guided-writing` row to `academic-paper` table |
| `academic-paper/SKILL.md` | Add mode description, routing, trigger keywords |

---

### Task 1: Create `guided-writing` branch

- [ ] **Step 1: Create and checkout branch**

```bash
git checkout -b guided-writing
```

Expected: branch created, now on `guided-writing`

- [ ] **Step 2: Commit design doc**

```bash
git add docs/design/2026-05-30-guided-writing-mode-design.md
git commit -m "docs: add guided-writing mode design spec"
```

---

### Task 2: Add `guided-writing` to `MODE_REGISTRY.md`

**Files:**
- Modify: `MODE_REGISTRY.md` (academic-paper table)

- [ ] **Step 1: Insert new mode row**

Add after the `plan` row in the `## academic-paper` table:

```markdown
| `guided-writing` | Originality | Complete draft via mentor-guided section-by-section drafting | Very High | "guided writing", "write with me", "help me draft", "guide my drafting", "mentor mode writing", "引導我寫", "一起寫論文", "導師模式", "陪寫論文", "逐段寫", "引导我写", "一起写论文", "导师模式", "陪写论文", "逐段写" |
```

Update header count: "**10 modes**" -> "**11 modes**" in the `## academic-paper` section header.
Update "Last updated" to current date.

- [ ] **Step 2: Verify MODE_REGISTRY renders correctly**

Open `MODE_REGISTRY.md` and confirm the table aligns.

- [ ] **Step 3: Commit**

```bash
git add MODE_REGISTRY.md
git commit -m "feat: register guided-writing mode in MODE_REGISTRY"
```

---

### Task 3: Create slash command `commands/ars-guided-writing.md`

**Files:**
- Create: `commands/ars-guided-writing.md`

- [ ] **Step 1: Write command file**

```markdown
---
description: ARS academic-paper `guided-writing` mode — mentor-guided section-by-section drafting
model: sonnet
---

Trigger the `academic-paper` skill in `guided-writing` mode. AI acts as a writing mentor: presents argument options, drafts reference paragraphs for user review, and gives conversational feedback. User makes all creative decisions and revisions. Originality-spectrum, very-high oversight.

Mode reference: `MODE_REGISTRY.md` § academic-paper.
Skill entry: `academic-paper/SKILL.md`.
```

- [ ] **Step 2: Verify file exists and has frontmatter**

```bash
head -4 commands/ars-guided-writing.md
```

Expected: `---`, `description:`, `model:`, `---`

- [ ] **Step 3: Commit**

```bash
git add commands/ars-guided-writing.md
git commit -m "feat: add /ars-guided-writing slash command"
```

---

### Task 4: Write `academic-paper/references/guided_mode_protocol.md`

**Files:**
- Create: `academic-paper/references/guided_mode_protocol.md`

- [ ] **Step 1: Write protocol document**

See design spec §3.3 and §5 for content. The document must contain:
- 6-step flow diagram (Step 0-6)
- Per-step input/output specification
- Activation rules (when to trigger `guided-writing` vs `plan` vs `full`)
- Convergence criteria (when to advance to next step)
- Handoff rules (what to pass to `guided_mentor_agent` from Step 2)
- Abort conditions (user can switch to `full` at any time)

- [ ] **Step 2: Verify 6-step flow is present**

```bash
grep -c "Step [0-6]:" academic-paper/references/guided_mode_protocol.md
```

Expected: 7 (Steps 0-6)

- [ ] **Step 3: Commit**

```bash
git add academic-paper/references/guided_mode_protocol.md
git commit -m "feat: add guided mode protocol reference"
```

---

### Task 5: Write `academic-paper/agents/guided_mentor_agent.md`

**Files:**
- Create: `academic-paper/agents/guided_mentor_agent.md`

- [ ] **Step 1: Write agent document**

See design spec §4.1. Must include:
- Frontmatter (`name`, `description`)
- Role definition (mentor, not drafter)
- 5-Round per-section protocol
- `[DRAFT: review required]` requirement in Round 3
- Options mechanism (2-3 paths) in Round 2
- Commitment-feedback loop (Round 1 + Round 4)
- Feedback restraint (max 3 points)

- [ ] **Step 2: Verify `[DRAFT: review required]` is present**

```bash
grep "\[DRAFT: review required\]" academic-paper/agents/guided_mentor_agent.md
```

Expected: at least 1 match

- [ ] **Step 3: Commit**

```bash
git add academic-paper/agents/guided_mentor_agent.md
git commit -m "feat: add guided_mentor_agent"
```

---

### Task 6: Write `academic-paper/agents/guided_reviewer_agent.md`

**Files:**
- Create: `academic-paper/agents/guided_reviewer_agent.md`

- [ ] **Step 1: Write agent document**

See design spec §4.2. Must include:
- Frontmatter (`name`, `description`)
- Role definition (revision mentor, no scoring)
- 5-Step conversational review protocol
- Detection Heuristics subsection with 5 LLM-prompted detection rules
- Dynamic Question Bank table (5 classes × 12 questions)
- Severity priority: Evidence > Logic > Expression > Structure > Deepening
- "No issues detected" fallback (1 positive + 1 gentle probe)

- [ ] **Step 2: Verify all 5 question classes are present**

```bash
for cls in Logic Evidence Expression Structure Deepening; do
  grep -q "$cls" academic-paper/agents/guided_reviewer_agent.md && echo "OK: $cls" || echo "MISSING: $cls"
done
```

Expected: 5 OK lines

- [ ] **Step 3: Commit**

```bash
git add academic-paper/agents/guided_reviewer_agent.md
git commit -m "feat: add guided_reviewer_agent with dynamic triggering"
```

---

### Task 7: Write `academic-paper/examples/guided_mode_example.md`

**Files:**
- Create: `academic-paper/examples/guided_mode_example.md`

- [ ] **Step 1: Ensure examples directory exists**

```bash
mkdir -p academic-paper/examples
```

- [ ] **Step 2: Write example document**

A complete walkthrough showing:
- User trigger: "引导我写论文"
- Step 0: Intent alignment (3 mentor-style questions)
- Step 1: Decoupling (argument unit breakdown)
- Step 2: Blueprint (2-3 paths for Introduction)
- Step 3: Mentor rounds for one section (Round 1-5)
- Step 5: Reviewer feedback (2 triggered questions)
- Final output

- [ ] **Step 3: Commit**

```bash
git add academic-paper/examples/guided_mode_example.md
git commit -m "docs: add guided-writing usage example"
```

---

### Task 8: Modify `academic-paper/SKILL.md`

**Files:**
- Modify: `academic-paper/SKILL.md`

- [ ] **Step 1: Update frontmatter metadata**

Update `metadata.version` from `"3.1.2"` to `"3.1.3"`.
Update `metadata.last_updated` to `"2026-05-30"`.

Update `description` to include `guided-writing`:
```
description: "12-agent academic paper writing pipeline. 11 modes (full/plan/guided-writing/..."
```

- [ ] **Step 2: Add trigger keywords**

In the `### Trigger Keywords` section, add `guided-writing` triggers (must match design spec §5.1 exactly):
- EN: `guided writing`, `write with me`, `help me draft`, `guide my drafting`, `mentor mode writing`
- zh-TW: `引導我寫`, `一起寫論文`, `導師模式`, `陪寫論文`, `逐段寫`
- zh-CN: `引导我写`, `一起写论文`, `导师模式`, `陪写论文`, `逐段写`

- [ ] **Step 3: Add mode description section**

Add after the `plan` mode section:

```markdown
### Guided-Writing Mode Activation

Activate `guided-writing` mode when the user wants AI as a writing mentor — guiding them through drafting section by section rather than producing a finished paper automatically.

**Intent signals:**
1. User explicitly asks for "guided writing", "write with me", "导师模式"
2. User has a blueprint/plan and wants to draft with mentor support
3. User wants to focus on argument quality rather than prose generation

**Default rule**: When intent is ambiguous between `plan` and `guided-writing`, prefer `plan` if the user has no structure yet; prefer `guided-writing` if the user already knows what they want to write.

> See `references/guided_mode_protocol.md` for the full 6-step mentor-guided drafting flow.
```

- [ ] **Step 4: Add `guided-writing` to mode comparison / workflow**

In the orchestration workflow section, add `guided-writing` as a parallel path to `full` after planning.

- [ ] **Step 5: Update examples list**

Add `guided_mode_example` to the examples list (line 363 area).

- [ ] **Step 6: Commit**

```bash
git add academic-paper/SKILL.md
git commit -m "feat: integrate guided-writing mode into academic-paper SKILL.md"
```

---

### Task 9: Write CI lint `scripts/check_guided_mode_protocol.py`

**Files:**
- Create: `scripts/check_guided_mode_protocol.py`

- [ ] **Step 1: Write lint script**

The lint must check:
1. `guided_mode_protocol.md` exists and contains Steps 0-6
2. `guided_mentor_agent.md` exists and contains `[DRAFT: review required]`
3. `guided_reviewer_agent.md` exists and contains all 5 question classes + Detection Heuristics
4. `MODE_REGISTRY.md` contains `guided-writing` entry
5. `commands/ars-guided-writing.md` exists with valid frontmatter (`description`, `model`)

Exit code 0 on pass, 1 on any failure.

- [ ] **Step 2: Run lint against current repo**

```bash
python3 scripts/check_guided_mode_protocol.py
```

Expected: PASS (once all files above are created)

- [ ] **Step 3: Commit**

```bash
git add scripts/check_guided_mode_protocol.py
git commit -m "feat: add guided mode protocol CI lint"
```

---

### Task 10: Write unit tests `scripts/test_guided_mode_protocol.py`

**Files:**
- Create: `scripts/test_guided_mode_protocol.py`

- [ ] **Step 1: Write tests**

Tests using `unittest`:
1. `test_protocol_has_all_steps` — verifies Steps 0-6 present
2. `test_mentor_has_draft_label` — verifies `[DRAFT: review required]` present
3. `test_reviewer_has_all_classes` — verifies 5 question classes present
4. `test_reviewer_has_detection_heuristics` — verifies Detection Heuristics subsection
5. `test_registry_has_entry` — verifies MODE_REGISTRY.md row
6. `test_command_has_frontmatter` — verifies command file frontmatter
7. `test_lint_passes_on_valid_repo` — runs lint, expects rc=0

- [ ] **Step 2: Run tests**

```bash
python3 -m unittest scripts.test_guided_mode_protocol -v
```

Expected: 7 tests PASS

- [ ] **Step 3: Commit**

```bash
git add scripts/test_guided_mode_protocol.py
git commit -m "test: add guided mode protocol unit tests"
```

---

### Task 10b: Write `scripts/test_guided_mentor_agent.py`

**Files:**
- Create: `scripts/test_guided_mentor_agent.py`

- [ ] **Step 1: Write tests**

Tests using `unittest`:
1. `test_round_1_commitment_question` — verifies commitment question exists
2. `test_round_2_options_mechanism` — verifies 2-3 paths presentation
3. `test_round_3_draft_label` — verifies `[DRAFT: review required]` in Round 3
4. `test_round_4_feedback_dimensions` — verifies Logic/Evidence/Expression feedback
5. `test_feedback_restraint` — verifies max 3 feedback points

- [ ] **Step 2: Run tests**

```bash
python3 -m unittest scripts.test_guided_mentor_agent -v
```

Expected: 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add scripts/test_guided_mentor_agent.py
git commit -m "test: add guided_mentor_agent unit tests"
```

---

### Task 10c: Write `scripts/test_guided_reviewer_agent.py`

**Files:**
- Create: `scripts/test_guided_reviewer_agent.py`

- [ ] **Step 1: Write tests**

Tests using `unittest`:
1. `test_five_question_classes_present` — verifies Logic/Evidence/Expression/Structure/Deepening
2. `test_detection_heuristics_subsection` — verifies Detection Heuristics heading
3. `test_severity_priority_order` — verifies Evidence > Logic > Expression > Structure > Deepening
4. `test_no_issues_fallback` — verifies positive feedback + gentle probe
5. `test_question_bank_count` — verifies at least 12 questions total

- [ ] **Step 2: Run tests**

```bash
python3 -m unittest scripts.test_guided_reviewer_agent -v
```

Expected: 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add scripts/test_guided_reviewer_agent.py
git commit -m "test: add guided_reviewer_agent unit tests"
```

---

### Task 10d: Write `scripts/test_guided_routing.py`

**Files:**
- Create: `scripts/test_guided_routing.py`

- [ ] **Step 1: Write tests**

Tests using `unittest`:
1. `test_en_triggers_present` — verifies EN trigger keywords in SKILL.md
2. `test_zhtw_triggers_present` — verifies zh-TW trigger keywords in SKILL.md
3. `test_zhcn_triggers_present` — verifies zh-CN trigger keywords in SKILL.md
4. `test_mode_differentiation_from_plan` — verifies guided-writing is distinct from plan
5. `test_mode_differentiation_from_full` — verifies guided-writing is distinct from full

- [ ] **Step 2: Run tests**

```bash
python3 -m unittest scripts.test_guided_routing -v
```

Expected: 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add scripts/test_guided_routing.py
git commit -m "test: add guided-writing routing unit tests"
```

---

### Task 11: Integrate lint into CI workflow

**Files:**
- Modify: `.github/workflows/spec-consistency.yml`

- [ ] **Step 1: Add lint step**

Add after the last existing lint step (after line 340):

```yaml
      - name: Validate guided-writing mode protocol
        run: python3 scripts/check_guided_mode_protocol.py
```

- [ ] **Step 2: Add test to pytest manifest**

Append to `scripts/_ci_pytest_manifest.toml`:

```toml
[[pytest]]
id = "guided-writing-protocol"
path = "scripts/test_guided_mode_protocol.py"

[[pytest]]
id = "guided-writing-mentor"
path = "scripts/test_guided_mentor_agent.py"

[[pytest]]
id = "guided-writing-reviewer"
path = "scripts/test_guided_reviewer_agent.py"

[[pytest]]
id = "guided-writing-routing"
path = "scripts/test_guided_routing.py"
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/spec-consistency.yml scripts/_ci_pytest_manifest.toml
git commit -m "ci: add guided-writing lint to spec-consistency workflow"
```

---

### Task 12: Final verification

- [ ] **Step 1: Run new test suite**

```bash
python3 -m unittest scripts.test_guided_mode_protocol scripts.test_guided_mentor_agent scripts.test_guided_reviewer_agent scripts.test_guided_routing -v
python3 scripts/check_guided_mode_protocol.py
```

Expected: all pass

- [ ] **Step 2: Run existing test suite (regression check)**

```bash
python3 scripts/run_ci_pytest_manifest.py
```

Or if manifest runner unavailable:
```bash
python3 -m unittest discover scripts -v 2>&1 | tail -20
```

Expected: No new failures compared to `main` branch baseline.

- [ ] **Step 3: Verify branch status**

```bash
git log --oneline guided-writing | head -20
```

Expected: ~15 commits on `guided-writing` branch

- [ ] **Step 4: Push branch (optional)**

```bash
git push -u origin guided-writing
```

---

### Task 13: Update `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add entry under next version**

Add under the current version section (or create `## [3.9.5]` if new version):

```markdown
- **Guided-Writing Mode** (academic-paper): New `guided-writing` mode — AI acts as writing mentor via Socratic dialogue, presents 2-3 argument paths per section, drafts reference paragraphs with `[DRAFT: review required]`, and gives conversational feedback via 5-class dynamic triggering. 2 new agents (`guided_mentor_agent`, `guided_reviewer_agent`), 1 protocol doc, 1 example, 4 test files, 1 CI lint. Zero existing agent files modified.
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for guided-writing mode"
```

---

## Acceptance Criteria

- [ ] `guided-writing` mode registered in `MODE_REGISTRY.md`
- [ ] `/ars-guided-writing` command file exists with valid frontmatter
- [ ] `guided_mode_protocol.md` documents 6-step flow
- [ ] `guided_mentor_agent.md` implements 5-round protocol with `[DRAFT: review required]`
- [ ] `guided_reviewer_agent.md` implements 5-class dynamic triggering with Detection Heuristics
- [ ] `academic-paper/SKILL.md` updated with triggers, routing, and mode description
- [ ] `scripts/check_guided_mode_protocol.py` lint passes
- [ ] `scripts/test_guided_mode_protocol.py` all 7 tests pass
- [ ] CI workflow includes guided-writing lint
- [ ] All existing tests still pass (no regression)
- [ ] All commits on `guided-writing` branch
