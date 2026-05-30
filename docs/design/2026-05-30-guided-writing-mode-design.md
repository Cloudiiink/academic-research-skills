# Guided Writing Mode Design

**Date**: 2026-05-30
**Version**: v3.9.5 (target)
**Scope**: `academic-paper` skill — new `guided-writing` mode
**Principle**: Zero existing agent file modification — add new agents, do not touch existing agent files. `SKILL.md` and `MODE_REGISTRY.md` are the only allowed exceptions for mode registration.

---

## 1. Problem Statement

The existing `academic-paper` skill operates on two extremes:

- **`plan` mode**: Socratic dialogue for paper structure planning, stops at outline
- **`full` mode**: Fully automated pipeline — AI writes the entire paper

There is no mode for users who want AI as a **writing mentor** — guiding them through drafting section by section, helping them focus on argument quality, theoretical coherence, and structural soundness rather than the mechanical labor of prose generation.

This design introduces `guided-writing` mode: a mentor-type skill that treats the human as the creativity and deep-thinking module, while AI handles guidance, option presentation, and quality feedback.

---

## 2. Design Philosophy

Inspired by `superpowers:brainstorming`:

1. **Analyze needs first** — software engineering always starts with requirements alignment
2. **Decouple** — break the paper into independent argument units with well-defined interfaces
3. **Options with trade-offs** — present 2-3 approaches, analyze pros/cons, recommend one with reasoning
4. **Human makes decisions** — AI stops at the right place, guiding the user to think about the most interesting/core parts

The human's unique value:
- Best understands their own research needs
- Can form deep thinking through modifying neural networks (actual writing)

---

## 3. Architecture

### 3.1 File Changes

| Operation | Path | Description |
|-----------|------|-------------|
| **Add** | `academic-paper/agents/guided_mentor_agent.md` | Section-by-section writing mentor |
| **Add** | `academic-paper/agents/guided_reviewer_agent.md` | Conversational review agent |
| **Add** | `academic-paper/references/guided_mode_protocol.md` | Protocol specification |
| **Modify** | `academic-paper/SKILL.md` | Add `guided-writing` mode description, routing, triggers |
| **Modify** | `MODE_REGISTRY.md` | Add `guided-writing` mode row to `academic-paper` table |
| **Add** | `commands/ars-guided-writing.md` | Slash command file for `/ars-guided-writing` trigger |
| **Add** | `academic-paper/examples/guided_mode_example.md` | Usage example demonstrating guided-writing flow |

### 3.2 Zero Existing Agent File Modification Principle

The following existing agent files are **completely untouched**:

- `draft_writer_agent.md` — remains for `full` mode
- `peer_reviewer_agent.md` — remains for `full` mode
- `socratic_mentor_agent.md` — remains for `plan` mode
- All other 9 agents remain unchanged

Routing is handled at the orchestration layer (`SKILL.md`) by mode selection.

**Steps 0-2 agent invocation**: Existing agents (`intake_agent`, `structure_architect_agent`, `argument_builder_agent`) are invoked with mode-specific system prompt overrides passed at call time by the orchestrator. No agent file is modified; the orchestrator prepends `guided-writing` context to the system prompt at invocation.

### 3.3 6-Step Core Flow

```
Step 0: Intent Alignment    -> intake_agent (with guided-writing context prepended)
Step 1: Decoupling Design   -> structure_architect_agent (with guided-writing context prepended)
Step 2: Blueprint Building  -> argument_builder_agent (with guided-writing context prepended)
Step 3: Section-by-Section  -> guided_mentor_agent
Step 4: Integrity Check     -> argument_builder_agent (stress test, with guided-writing context)
Step 5: Refinement Feedback -> guided_reviewer_agent
Step 6: Format Output       -> formatter_agent
```

---

## 4. Agent Designs

### 4.1 `guided_mentor_agent`

**Role**: Academic writing mentor. Does not write for the user; guides them to write through Socratic questioning and structured feedback. Core task: expose uncertainty, strengthen arguments, improve expression.

**Per-Section Protocol (5 Rounds)**:

```
Round 1: Preparation
  - State the section's "argument goal" (1 sentence)
  - Ask: "Before you write, what do you think will be the hardest part of this section?"
  - Extract [COMMITMENT: section: user's prediction]

Round 2: Options
  - Based on Step 2 blueprint, present 2-3 argument paths
  - Analyze pros/cons of each
  - Ask: "Which path do you prefer? Or do you have a fourth idea?"
  - User decides -> lock path

Round 3: Drafting
  - AI drafts a reference paragraph based on locked path
  - Label: [DRAFT: review required]
  - Note: "This is a reference draft. Please check: Is the argument accurate? Is evidence sufficient? Does the expression match your style?"
  - User modifies or rewrites

Round 4: Feedback
  - Three dimensions (max 2 questions each, max 3 total feedback points):
    a) Logic: Is the argument chain complete? Hidden assumptions?
    b) Evidence: Is evidence strong enough? Counterexamples unaddressed?
    c) Expression: Is it academic? Any AI-typical phrasing?
  - Compare draft vs. user's version: "What writing judgment does the difference reflect?"
  - Ask: "Pass, or revise another round?"

Round 5: Revision
  - User modifies
  - Optional: "Help me draft" -> AI provides draft, user must review and confirm
  - Loop until user says "next section"
```

**Key Design Points**:

1. **Options mechanism** (Round 2): Must present 2-3 paths. Core of software-engineering thinking — let the user make an informed choice rather than invent from zero.

2. **Commitment-feedback loop** (Round 1 + Round 4): User predicts difficulty, later checks against reality — similar to `plan` mode's SCR but applied to writing.

3. **Semi-automatic safety valve**: User can say "help me draft", but this is not the default. AI drafts must carry `[DRAFT: review required]`; user must review sentence by sentence.

4. **Feedback restraint**: Max 3 feedback points per section. Prevents the mentor from becoming an editor and the user from becoming a typist.

### 4.2 `guided_reviewer_agent`

**Role**: Revision mentor. No scores, no formal review report. Works like a PhD advisor marking a student's draft — points out issues and asks "How do you think this should be fixed?"

**Conversational Review Protocol**:

```
Step 1: Overall Impression
  - "The point that confused me most after reading this chapter..."
  - "The clearest part of this chapter..."
  - Max 2 impressions, max 3 sentences total

Step 2: Per-Section Questions (Dynamic Triggering)
  For each paragraph, run 5-class quality detection, then ask 0-1 question
  from the triggered class:

  Class A: Logic (Argument Coherence)
    - "From sentence A to sentence B, I couldn't follow. What's the reasoning?"
    - "This conclusion seems to rest on an unstated premise. Can you make it explicit?"

  Class B: Evidence (Evidence Sufficiency)
    - "If this claim were challenged, what evidence would you use to respond?"
    - "Is there a counterexample you haven't addressed?"

  Class C: Expression (Writing Quality)
    - "You used 'delve into' here — is that the most precise word for your meaning?"
    - "This paragraph has 5 consecutive sentences of 20-25 words. Can you vary the rhythm?"
    - (From writing_quality_check.md: throat-clearing openers, em dash overuse, synonym cycling)

  Class D: Structure
    - "If this paragraph were deleted, what would the reader lose?"
    - "This section follows the exact same structure as the previous one. Is that intentional?"

  Class E: Deepening (Originality + Methodological Rigor)
    - "You claim this is the 'first' study of X. Are you certain no prior work exists?"
    - "What methodological assumption are you relying on that a reviewer might challenge?"

  Trigger rules:
  - Run detection per class; only ask if issue detected in that class
  - Max 3 questions per paragraph (1 per triggered class, severity-prioritized)
  - Severity priority: Evidence > Logic > Expression > Structure > Deepening
  - If no issues detected in any class:
    -> 1 positive feedback + 1 gentle probe:
       "This argument is clear. If a reviewer had to nitpick, what would you worry about most?"

Step 3: User Response
  - User chooses which question to address first
  - User modifies or explains
  - AI confirms "This resolves my concern" or "One more step needed"

Step 4: Cross-Chapter Consistency
  - "You mentioned X in the Introduction but didn't return to it in Discussion. Intentional?"
  - "Methodological assumptions stated in Methods — are they acknowledged in Limitations?"

Step 5: Close
  - Summarize revision points (max 3)
  - Ask: "Start next chapter review, or handle remaining issues first?"
```

**Detection Heuristics**:

Each class uses a prompt-based detection heuristic (LLM-prompted, not regex). The `guided_reviewer_agent` runs a lightweight internal scan:

```
For each paragraph, run 5 parallel detection prompts:
- Logic: "Does this paragraph contain an unstated premise or a logical gap?"
- Evidence: "Does this paragraph make any claim without supporting evidence or citation?"
- Expression: "Does this paragraph contain AI-typical phrasing, throat-clearing openers, or uniform sentence length?"
- Structure: "Does this paragraph have a clear function? Does it mirror the structure of adjacent paragraphs mechanically?"
- Deepening: "Does this paragraph make an originality claim that is unverified? Does it hide a methodological assumption?"
```

Output: binary trigger per class (`triggered` / `clean`). Only `triggered` classes proceed to question selection.

**Dynamic Question Bank**:

| Class | Detection Source | Question Count |
|-------|-----------------|----------------|
| Logic | `peer_reviewer_agent` Argument Coherence dimension | 2 questions |
| Evidence | `peer_reviewer_agent` Evidence Sufficiency dimension | 2 questions |
| Expression | `writing_quality_check.md` sections A (High-Frequency Terms), C (Throat-Clearing Openers), E (Burstiness) | 4 questions |
| Structure | `writing_quality_check.md` section D (Structure Pattern Warnings) | 2 questions |
| Deepening | `peer_reviewer_agent` Originality + Rigor dimensions | 2 questions |
| **Total** | | **12 questions** |

**Difference from `peer_reviewer_agent`**:

| Aspect | `peer_reviewer` | `guided_reviewer_agent` |
|--------|----------------|------------------------|
| Output | Formal review report | Conversational probing |
| Tone | Objective, anonymous, critical | Mentor-style, constructive, empathetic |
| Scoring | 5-dimension scores | No scores |
| User role | Receive review comments | Actively explain and modify |
| Goal | Find problems | Cultivate user's self-review ability |

---

## 5. Routing and Triggers

### 5.1 Trigger Keywords

| Language | Keywords |
|----------|----------|
| EN | `guided writing`, `write with me`, `help me draft`, `guide my drafting`, `mentor mode writing` |
| zh-TW | `引導我寫`, `一起寫論文`, `導師模式`, `陪寫論文`, `逐段寫` |
| zh-CN | `引导我写`, `一起写论文`, `导师模式`, `陪写论文`, `逐段写` |

### 5.2 Routing Rules

```
User input -> Intent detection
  |- Explicit "guided writing" / "导师" / "一起写" -> Route to guided-writing mode
  |- "引导我写论文" (existing plan trigger) -> Prefer guided-writing (user wants to "write" not just "plan")
  |- "help me plan my paper" (existing plan trigger) -> Keep plan mode
  |- Ambiguous -> Clarify: "Do you want to plan structure first (plan), or draft section by section (guided-writing)?"
```

### 5.3 Mode Comparison

| Mode | Coverage | User Role | AI Role |
|------|----------|-----------|---------|
| `plan` | Structure planning only | Answer structure questions | Socratic questioner |
| `guided-writing` | Structure -> Full draft | Make decisions, review drafts, focus on argument quality | Mentor: present options, draft references, give feedback |
| `full` | Fully automated | Configure + receive成品 | Automated writer |

### 5.4 Pipeline Integration

- `guided-writing` mode can be an optional Stage 2 path in `academic-pipeline`
- If user selects `guided-writing`, Stage 2 runs `guided-writing` instead of `full`
- Stage 3 (reviewer) can still be invoked; reviewer sees a "human+AI collaborative" manuscript

### 5.5 v3.6.6 Generator-Evaluator Contract Interaction

`guided-writing` mode is **exempt from the v3.6.6 generator-evaluator contract**. The contract applies to `full` mode where AI is the sole generator. In `guided-writing` mode, the human is the generator; AI's role is mentor and reviewer. Therefore:

- No Phase 4a/4b split (no writer contract needed)
- No Phase 6a/6b split (no in-pair evaluator needed)
- `guided_reviewer_agent` performs review inline during Step 5, not as a separate evaluator phase
- Material Passport checkpoints occur at Step 2 (blueprint complete) and Step 5 (refinement complete)
- If user invokes `academic-pipeline` with `guided-writing`, Stage 2 uses `guided-writing` mode; Stage 3 dispatches `academic-paper-reviewer` for external editorial review as normal

---

## 6. Testing Strategy

### 6.1 New Test Files

| Test File | Coverage |
|-----------|----------|
| `scripts/test_guided_mode_protocol.py` | 6-step flow completeness, per-step input/output format |
| `scripts/test_guided_mentor_agent.py` | Round 1-5 cycle, options mechanism, draft labeling |
| `scripts/test_guided_reviewer_agent.py` | 5-class triggering logic, quality detection |
| `scripts/test_guided_routing.py` | EN/zh-TW/zh-CN triggers, discrimination from plan/full |

### 6.2 CI Integration

- Extend `.github/workflows/spec-consistency.yml` with `guided-writing` mode lint
- Add lint script: `scripts/check_guided_mode_protocol.py`
  - Check `guided_mode_protocol.md` 6-step completeness
  - Check `guided_mentor_agent.md` Round 3 contains `[DRAFT: review required]`
  - Check `guided_reviewer_agent.md` covers all 5 question classes + detection heuristics
  - Check `MODE_REGISTRY.md` contains `guided-writing` entry
  - Check `commands/ars-guided-writing.md` exists and has valid frontmatter

### 6.3 Manual Verification Checklist

1. Trigger with `"引导我写论文"` -> enters guided-writing mode
2. Verify Round 2 presents 2-3 argument paths
3. Verify Round 3 draft carries `[DRAFT: review required]`
4. Verify high-quality paragraph receives only 1 gentle probe
5. Verify low-quality paragraph receives 2-3 targeted questions

---

## 7. Naming Clarification

The existing `academic-paper/SKILL.md` lists `plan_mode_guided_writing` as an example file. This is a **`plan` mode example** — it demonstrates Socratic planning dialogue. The new **`guided-writing` mode** is a separate mode that extends beyond planning into actual drafting. The two are distinct; users should not conflate them.

---

## 8. Acceptance Criteria

- [ ] `guided-writing` mode can be triggered by EN/zh-TW/zh-CN keywords
- [ ] `guided_mentor_agent` presents 2-3 options before drafting
- [ ] AI drafts carry `[DRAFT: review required]` label
- [ ] `guided_reviewer_agent` dynamically triggers questions based on quality detection
- [ ] High-quality paragraphs receive <= 1 question
- [ ] Low-quality paragraphs receive 2-3 targeted questions
- [ ] All existing modes (`full`, `plan`, `revision`, etc.) remain byte-identical
- [ ] All 4 new test files pass
- [ ] CI lint passes
