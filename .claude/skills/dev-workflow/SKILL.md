---
name: dev-workflow
description: Execute a complete, production-grade development workflow using the planner, coder, reviewer, and tester subagents. This skill orchestrates all four agents in sequence, enforces structured handoffs between phases, handles failures with automatic retry, and requires human confirmation at critical gates. Invoke this skill when the user wants to implement a new feature, fix a bug, or complete any non-trivial development task that requires planning, implementation, review, and testing.
---

## Workflow Overview

```
[User Input]
     │
     ▼
┌─────────────┐
│   PLANNER   │  → Structured plan + acceptance criteria (testable behaviors)
└─────────────┘
     │
     ▼
⚑ CHECKPOINT #1 — Plan Approval (mandatory, always wait)
     │
     ▼
┌─────────────┐
│    CODER    │  → Implementation + unit tests for all core modules
└─────────────┘
     │
     ▼
⚑ CHECKPOINT #2 — Implementation Verification (mandatory, always wait)
     │
     ▼
┌─────────────┐
│  REVIEWER   │  → Static analysis, quality gate
└─────────────┘
     │
  PASS? ──No──► [CODER retry, max 3 times]
     │                │
     │           3rd failure ──► ⚑ CHECKPOINT #4
     │
     ▼ Yes
┌─────────────┐
│   TESTER    │  → Execute tests + validate acceptance criteria + add edge cases
└─────────────┘
     │
  PASS? ──No──► [CODER retry, max 3 times]
     │                │
     │           3rd failure ──► ⚑ CHECKPOINT #4
     │
     ▼ Yes
  ✅ DONE — Completion summary reported
```

## Execution Instructions

Follow these instructions precisely. Do not skip steps, do not merge phases, and do not proceed past a checkpoint without explicit user confirmation.

---

### PHASE 1 — PLANNING

Invoke the **planner** subagent with the user's original request.

The planner must produce output in exactly this format:

```
## Task Summary
[One-paragraph description of what will be built and why]

## Scope
- In scope: [list what will be implemented]
- Out of scope: [list what is explicitly excluded]
- Assumptions: [list any assumptions made]

## Implementation Tasks
- [ ] Task 1: [description] — [affected files or modules]
- [ ] Task 2: [description] — [affected files or modules]
- [ ] Task N: [description] — [affected files or modules]

## Unit Test Requirements
[For each core module or function in the implementation tasks, specify what
unit tests the coder must write. Focus on: happy path, known edge cases,
and error handling. This is the Coder's test specification, not the
acceptance criteria.]

- [ ] Module/function: [name]
  - Test: [behavior to test]
  - Test: [behavior to test]

## Acceptance Criteria
[Testable behavior descriptions from the user's perspective. Each criterion
must be specific enough for the tester to verify without ambiguity.
Written as: "Given [context], when [action], then [expected outcome]."]

- [ ] AC1: Given [...], when [...], then [...]
- [ ] AC2: Given [...], when [...], then [...]
- [ ] ACN: Given [...], when [...], then [...]

## Risks & Notes
[Known risks, tricky areas, or decisions that need human judgment before
implementation begins.]
```

After displaying the planner output, **stop completely** and present this message:

```
─────────────────────────────────────────────────────
⚑ CHECKPOINT #1 — Plan Approval

Please review the plan, unit test requirements, and
acceptance criteria above before implementation begins.

Reply with:
  • "confirmed" — proceed to implementation
  • "change: [your feedback]" — revise the plan first
─────────────────────────────────────────────────────
```

Do not proceed until the user explicitly confirms. If the user requests changes, re-invoke the planner with the original request plus the feedback, then present the updated plan for approval. Repeat until confirmed.

---

### PHASE 2 — IMPLEMENTATION

Invoke the **coder** subagent with:

1. The full confirmed plan from Phase 1
2. The original user request
3. This explicit instruction: **"Implement all tasks in the Implementation Tasks list. For each module or function listed in Unit Test Requirements, write the specified unit tests. Do not skip unit tests."**

BEFORE WRITING ANY CODE, you must complete these steps in order:

Step 1 — Run `git status`. If the working tree is not clean, stop
immediately and report to the user. Do not proceed until resolved.

Step 2 — Confirm the current branch is NOT main or master. If it is,
create a new branch now using the appropriate prefix (feat/, fix/,
etc.) based on the task type.

Only after both steps are confirmed, begin implementation.
Git commit after completing each task in the Implementation Tasks list.

The coder must produce output in this format:

```
## Implementation Summary

### Files Created
- [filepath]: [purpose]

### Files Modified
- [filepath]: [what changed and why]

### Unit Tests Written
- [test file]: covers [module/function] — [list of test cases written]

### Deviations from Plan
- [any deviation from the approved plan and the reason]
  (If none: "None — implemented as planned")
```

Pass this summary directly to Phase 3. Do not display it to the user yet.

─────────────────────────────────────────────────────
⚑ CHECKPOINT #2 — Implementation Verification

Please run the Streamlit app and verify the UI effects and functionality:

```bash
streamlit run src/app.py
# or for multi-page apps:
streamlit run app.py --server.sidecar something
```

Then confirm:
• All Streamlit elements render correctly (st.title, st.dataframe, st.button, etc.)
• Page navigation works as expected
• Session state is properly initialized
• No Python errors in the console

Reply with:
• "confirmed" — proceed to code review
• "change: [your feedback]" — return to implementation
─────────────────────────────────────────────────────

---

### PHASE 3 — CODE REVIEW

Initialize: `review_attempts = 0`, max = 3.

Invoke the **reviewer** subagent with:

1. The Acceptance Criteria from the approved plan
2. The Unit Test Requirements from the approved plan
3. The Implementation Summary from Phase 2
4. This instruction: **"Review all created and modified files. Pay attention to: correctness against the plan, code quality, security, error handling, and whether unit tests adequately cover the Unit Test Requirements."**

The reviewer must produce output in this format:

```
## Review Result: [PASS | FAIL]

### Critical Issues (must fix — blocks proceeding)
- [issue description] — [file:line if applicable]

### Warnings (should fix — does not block)
- [issue description] — [file:line if applicable]

### Suggestions (optional improvements)
- [suggestion]

### Unit Test Assessment
[Did the coder write tests as specified in Unit Test Requirements?
Flag missing tests as Critical Issues. Flag inadequate tests as Warnings.]
```

**If PASS:** automatically proceed to Phase 4 (no manual approval required).

**If FAIL:**

- Increment `review_attempts`
- If `review_attempts < 3`:
  - Invoke the **coder** subagent with the original plan + the reviewer's full output
  - Instruct the coder: **"Fix all Critical Issues listed in the review. Do not change anything else."**
  - Re-invoke the **reviewer** with the same instructions as before
  - Repeat the loop
- If `review_attempts == 3`: stop and present this message:

```
─────────────────────────────────────────────────────
⚑ CHECKPOINT #3 — Review Gate Failed

Critical issues remain after 3 attempts.

Last reviewer report:
[insert full reviewer output]

Reply with:
  • "override" — accept current code and proceed to testing
                 (override will be noted in the final summary)
  • "retry: [your instruction]" — one more coder attempt
                                  with your specific guidance
  • "abort" — stop the workflow, preserve all current changes
─────────────────────────────────────────────────────
```

Wait for user response. Apply the chosen action before continuing.

---

### PHASE 4 — TESTING

Initialize: `test_attempts = 0`, max = 3.

Invoke the **tester** subagent with:

1. The Acceptance Criteria from the approved plan
2. The Unit Test Requirements from the approved plan
3. The Implementation Summary from Phase 2 (including unit tests written)
4. The final reviewer report from Phase 3
5. This instruction: **"First, run all existing unit tests written by the coder. Then, validate each Acceptance Criterion. Finally, identify and execute additional edge case and error handling tests that the coder did not cover. Report all results."**

The tester must produce output in this format:

```
## Test Result: [PASS | FAIL]

### Unit Tests (written by Coder)
- [test name]: [PASS | FAIL]
- [failure detail if applicable]

### Acceptance Criteria Validation
- AC1: [PASS | FAIL] — [brief evidence or failure reason]
- AC2: [PASS | FAIL] — [brief evidence or failure reason]
- ACN: [PASS | FAIL] — [brief evidence or failure reason]

### Additional Edge Cases (added by Tester)
- [test description]: [PASS | FAIL]
- [failure detail if applicable]

### Overall Assessment
[Summary of what passed, what failed, and confidence level in the implementation]
```

**If PASS (all AC validated, no critical failures):** proceed to Phase 5.

**If FAIL:**

- Increment `test_attempts`
- If `test_attempts < 3`:
  - Invoke the **coder** subagent with the original plan + the tester's full output
  - Instruct the coder: **"Fix the failing tests listed below. Do not change passing tests or unrelated code."**
  - Re-invoke the **tester** with the same instructions as before
  - Repeat the loop
- If `test_attempts == 3`: stop and present this message:

```
─────────────────────────────────────────────────────
⚑ CHECKPOINT #4 — Test Gate Failed

Tests are still failing after 3 attempts.

Last test report:
[insert full tester output]

Reply with:
  • "override" — accept current state and mark workflow complete
                 (override will be noted in the final summary)
  • "retry: [your instruction]" — one more coder attempt
                                  with your specific guidance
  • "abort" — stop the workflow, preserve all current changes
─────────────────────────────────────────────────────
```

Wait for user response. Apply the chosen action before continuing.

---

### PHASE 5 — COMPLETION

All gates passed (or overridden). Present this summary:

```
─────────────────────────────────────────────────────
✅ WORKFLOW COMPLETE

Task: [original user request]

── Results ──────────────────────────────────────────
Review attempts : [N] / 3  [PASSED | OVERRIDDEN]
Test attempts   : [N] / 3  [PASSED | OVERRIDDEN]

── Files Changed ────────────────────────────────────
Created  : [list]
Modified : [list]

── Acceptance Criteria ──────────────────────────────
✅ AC1: [criterion text]
✅ AC2: [criterion text]
✅ ACN: [criterion text]

── Overrides (if any) ───────────────────────────────
[List any checkpoints that were overridden and the
user's stated reason. If none: omit this section.]

── Out of Scope / Follow-up ─────────────────────────
[Items marked out-of-scope in the plan that may need
follow-up. If none: omit this section.]
─────────────────────────────────────────────────────
```

After presenting the summary, automatically:

1. **Update README.md** — Invoke a general-purpose agent to update the project README.md to reflect the new features, commands, or project structure introduced by the task.

2. **Git commit** — Run `git add` for all changed files and create a commit with a message following the pattern:

   ```
   [type]: [short description]

   [optional longer description]

   - Created: [list]
   - Modified: [list]
   - ACs validated: [list]
   ```

   Use the commit type based on task context: `feat` for new features, `fix` for bug fixes, `refactor` for refactoring, `docs` for documentation changes, `test` for test changes.

   If there are no meaningful changes to commit (e.g., only override was used and no code changed), skip the commit and note it in the summary.

## Standing Rules

**Phase isolation.** Planner, coder, reviewer, and tester are always invoked as separate subagents in separate calls. Never ask one subagent to perform another's role. Never combine phases.

**Checkpoint #1 and #2 are always mandatory.** Even if the plan looks straightforward, always present it to the user and wait for explicit confirmation before any code is written.

**Structured output is required.** If any subagent fails to produce output in the required format, re-invoke it once with an explicit instruction to follow the format. If it fails again, report the failure to the user and halt.

**Retry scope is limited.** When re-invoking the coder after a review or test failure, instruct it to fix only the reported issues. Do not re-implement the entire task.

**Abort behavior.** If the user says "abort" at any checkpoint, stop immediately. Do not undo or clean up any changes. Report current state:

```
Workflow aborted at: [phase name]
Changes preserved in current working state.
Files affected: [list from Implementation Summary]
To resume: re-run /dev-workflow with your original request.
```

**Override logging.** Any override must be recorded in the final completion summary. This ensures the team has a clear audit trail of which quality gates were bypassed and why.
