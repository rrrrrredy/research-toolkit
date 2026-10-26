# Handling failed checks and reports

[English](failure-handling.md) | [简体中文](failure-handling.zh-CN.md)

Preserve the failure, identify its cause, make a specific correction, and verify that correction. Repeatedly generating or judging an unchanged sample until it passes is not a repair. Distinguish ordinary report delivery from frozen evaluation evidence.

## Route the failure

| Observed problem | Action and owner | Acceptance evidence |
| --- | --- | --- |
| Reproducible runtime, parsing, state or checker defect | Maintainer: reproduce with a minimal case, fix in a PR, retain a valid control, run relevant tests and CI, then merge. | The failure is caught or corrected, the valid control still works, and the merged commit is identified. |
| Draft violates a declared length range | Author: measure the actual artifact, edit for the agreed coverage and range, then recheck. | Current-file counts meet the original rule; required content remains covered. A short but wrong report still fails content review. |
| Wrong recommendation, calculation, attribution or causal claim | Author and applicable reviewer: compare the exact passage with sources, correct the decision and affected claims/citations, then review the new version. | Located source evidence and a justified decision; a model PASS or agreement between models alone is insufficient. |
| Reviewer error or label/order disagreement | Check the underlying passage and source. Retain the original judgment and use an evidenced disposition for ordinary delivery; report disagreement in an evaluation. | The reason and material evidence are recorded. Do not discard a negative review because it is inconvenient. |
| Timeout, quota, missing access or malformed output | Preserve raw output and execution status; diagnose before another attempt. | Any later attempt is separately identified and within the declared budget; it does not replace the failure. |

## Check before delivery

For a managed task, call `research_check_draft(task, artifact="final.md")`, or save `{"task":"comparison","artifact":"final.md"}` as a request file and run:

```bash
python scripts/research_workflow.py check-draft --workspace ../research-work --request check-draft.json
```

This local command checks the brief fields, source/claim record prerequisites, readable nonempty draft and explicit `length_constraint` records. It returns whole-artifact word/character counts, `length_checks`, errors and warnings. CLI exit 1 means these checks failed. `ok: true` means only these checks passed: `semantic_quality` and `delivery_status` remain `not_assessed`. Other requirements, source truth and actual reading still need the normal checks. No range is inferred from prose; an absent range produces a warning. Register only the actual agreed rule; body-only limits need a separate appropriate measurement. See the [counting contract](delivery-verification.md#explicit-length-requirements).

The check uses the shared task lock and changes no progress, report, review or receipt. The normal empty lock file may be created for an older task. It does not call a model, revise text, satisfy a pending requirement or authorize delivery. Results describe the checked version, not a later edit; `finish` recomputes its own checks.

For an ordinary report:

1. Preserve the original review and identify the defect, report version, passage, requirement/source, consequence and proposed correction in existing task records. Keep a separate draft copy before editing if an original report is not already retained.
2. Correct the affected text and claims, then run `check-draft`. Resolve pending ledger entries using evidence; never change the agreed bounds merely to make the count pass.
3. Check the final decision against the same numbers and conditions as the comparison. Treat missing observations as unknown. Inspect required coverage after shortening.
4. call `research_review` with `revision: true` for the changed version, resolve necessary findings and call `finish`. Already authorized repairs need no extra permission. Independent review is required only when the task declares it.

## Bound the loop

Before another paid repair or review batch, record the change hypothesis, relevant defect IDs, new version, acceptance criteria and request/token/time ceiling. Use the existing review and task records; no extra service is required. The draft checker does not enforce a paid-call budget.

Do not rerun an unchanged valid negative judgment. If a targeted correction leaves the same necessary defect, inspect the source and correction directly and change the strategy instead of repeating the same prompt. Use a reviewer appropriate to the declared tier or perform a source-based correction within the existing authorization. Stop additional paid attempts when the declared budget is exhausted or the next attempt has no specific corrective hypothesis. Keep necessary issues open and report the remaining work; do not claim completion. Ask the user only if progress needs a real scope/access/budget decision. Optional polish does not justify an endless loop, and a disclosed limitation does not waive a required task.

In a frozen evaluation, leave the original report, first valid judgment, missing outcomes and budget accounting untouched. Create product regressions or clearly labeled editorial examples separately. After a method change, recheck the original failure and relevant existing tasks, recording the new version. Keep original failures and repaired outcomes separate; routine repair does not require a new held-out dataset.

## Current failures and source checks

The [eight feedback probes](../evals/diagnostics/2026-10-13-feedback-probes/README.md) are exposed development evidence: eight parsed, three met length, all four Toolkit reports missed the range. These findings remain open as model-quality limitations even after the tool PR is merged.

| Failure | Concrete source check for a correction | What remains unproven |
| --- | --- | --- |
| Storage recommendation says no option qualifies, including the false comparison 14 < 12 | In the fictional Maple sources, C costs 6 + 2 = 8 within the cap 10, holds 14 TB against current 12 TB, and restores in 3 hours within 4. A costs 11; B takes 5 hours. Next year's 16 TB forecast does not invalidate today's eligibility; expansion terms remain unknown. | Whether an unseen model draft reliably applies this method. |
| Rinsing report converts unlogged soil conditions into an observed change | Brook sources: both months use 180,000 L; 1,200 to 1,500 boxes means 150 to 120 L/box, a 20% intensity reduction. July soil is unlogged; changed staffing and missing quality data prevent a nozzle-only causal claim and approval. | Causal benefit and unchanged quality cannot be established from these sources. |
| Over/under-length reports with plausible self-check claims | Run the real artifact through the declared rule, preserve a failing result, then edit and measure again. Five archived failures are rejected and two separately labeled editorial controls pass in offline tests. | Passing the length check does not validate the report's factual claims. |

Both corrected reports passed [Astra review in separate contexts](../evals/repairs/2026-10-13-astra/README.md). The storage repair retains its initial negative review and the later pass after completing the comparison. The [improvement plan](improvement-plan.md) tracks concrete errors, changes and acceptance without outside-reviewer or task-collection prerequisites.
