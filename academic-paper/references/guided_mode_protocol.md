# Guided-Writing Mode Protocol

**Version**: v3.9.5
**Scope**: `academic-paper` skill — `guided-writing` mode
**Principle**: Human is the generator; AI is the mentor. Zero existing agent files modified.

---

## Overview

`guided-writing` mode bridges the gap between `plan` (Socratic planning only) and `full` (fully automated drafting). In this mode, AI acts as a senior doctoral advisor, guiding the user through section-by-section drafting via structured dialogue, option presentation, and dynamic feedback.

**Core flow**: Intent Alignment → Decoupling Design → Blueprint Building → Section-by-Section Drafting → Integrity Check → Refinement Feedback → Format Output

---

## 6-Step Flow

```
Step 0: INTENT ALIGNMENT
  -> intake_agent (with guided-writing context prepended)
  -> Output: Paper Configuration Record + mentor-style intake notes

Step 1: DECOUPLING DESIGN
  -> structure_architect_agent (with guided-writing context prepended)
  -> Output: Decoupled argument units with well-defined interfaces

Step 2: BLUEPRINT BUILDING
  -> argument_builder_agent (with guided-writing context prepended)
  -> Output: Argument Blueprint (claim-evidence chains per unit)

Step 3: SECTION-BY-SECTION DRAFTING
  -> guided_mentor_agent
  -> Output: Draft sections (human-authored, AI-guided)

Step 4: INTEGRITY CHECK
  -> argument_builder_agent (stress test, with guided-writing context)
  -> Output: Cross-section consistency report

Step 5: REFINEMENT FEEDBACK
  -> guided_reviewer_agent
  -> Output: Conversational review + revision points

Step 6: FORMAT OUTPUT
  -> formatter_agent
  -> Output: LaTeX / DOCX-via-Pandoc / PDF / Markdown
```

---

## Step 0: Intent Alignment

**Goal**: Understand the user's research, anxieties, target audience, and writing goals.

**Mentor-style questions** (appended to standard intake):
- "What part of writing this paper makes you most anxious?"
- "Who is your ideal reader? A specialist in your subfield, or a broader audience?"
- "Do you already have a clear structure in mind, or do you need help figuring that out first?"

**Handoff to Step 1**: Paper Configuration Record + mentor notes

---

## Step 1: Decoupling Design

**Goal**: Break the paper into independent argument units.

**Conversational interaction**:
- AI proposes argument units based on the paper type and research question
- User confirms, rejects, or restructures units
- Each unit must answer: What claim does it make? What evidence supports it? What does it depend on?

**Convergence criteria**: User confirms the unit breakdown.

---

## Step 2: Blueprint Building

**Goal**: Design claim-evidence chains for each unit.

**Option presentation**:
- For each unit, AI presents 2-3 possible claim-evidence configurations
- Analyzes pros/cons of each (e.g., "Path A is safer but less novel; Path B is bold but requires stronger evidence")
- User selects or proposes a fourth option

**Handoff to Step 3**: Locked Argument Blueprint (one configuration per unit)

---

## Step 3: Section-by-Section Drafting

**Goal**: Write each section with mentor guidance.

**Per-section protocol** (see `guided_mentor_agent.md`):
- Round 1: Commitment — "What will be hardest about this section?"
- Round 2: Options — 2-3 argument paths
- Round 3: Drafting — AI drafts `[DRAFT: review required]`, user modifies
- Round 4: Feedback — max 3 points (Logic / Evidence / Expression)
- Round 5: Revision — loop until user says "next section"

**Abort condition**: User can say "switch to full mode" at any time; orchestrator hands off to `draft_writer_agent`.

---

## Step 4: Integrity Check

**Goal**: Verify cross-section consistency and argument chain closure.

**Stress test questions**:
- "Does the Introduction's gap claim match what the Discussion concludes?"
- "Does every claim in the Discussion have supporting evidence in Results?"
- "Are methodological assumptions stated in Methods acknowledged in Limitations?"

---

## Step 5: Refinement Feedback

**Goal**: Conversational review of the complete draft.

**Per-paragraph review** (see `guided_reviewer_agent.md`):
- 5-class dynamic triggering (Logic / Evidence / Expression / Structure / Deepening)
- Only triggered classes produce questions
- Max 3 questions per paragraph
- High-quality paragraphs: 1 positive feedback + 1 gentle probe

---

## Step 6: Format Output

**Goal**: Produce final formatted document.

Standard formatter_agent invocation. No mode-specific changes.

---

## Activation Rules

### Trigger `guided-writing` when:
1. User explicitly says "guided writing", "write with me", "导师模式", etc.
2. User has a plan/outline and wants mentor-supported drafting
3. User wants to focus on argument quality, not prose generation

### Prefer `plan` when:
- User has no structure yet and needs help figuring out the paper architecture

### Prefer `full` when:
- User wants a finished draft with minimal interaction

---

## Material Passport Checkpoints

- **Checkpoint 1**: After Step 2 (Blueprint complete) — user can resume from here
- **Checkpoint 2**: After Step 5 (Refinement complete) — user can resume from here

---

## v3.6.6 Contract Exemption

`guided-writing` mode is **exempt from the generator-evaluator contract**. The contract applies to `full` mode where AI is the sole generator. In `guided-writing` mode, the human is the generator; AI's role is mentor and reviewer. Therefore:

- No Phase 4a/4b split
- No Phase 6a/6b split
- `guided_reviewer_agent` performs review inline during Step 5
