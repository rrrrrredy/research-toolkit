# Report checking and repair standard

[English](report-evaluation-standard.md) | [简体中文](report-evaluation-standard.zh-CN.md)

This page defines how the project checks reports, fixes problems and verifies changes. Use existing real tasks; model execution and evaluation provide a user perspective. Research delivery follows the independent roles in the shared method; maintenance comparisons use their declared study design. Preserve original reports, reviewer counts and results from older experiments; their configurations are not defaults for new work.

<a id="报告评测现行标准"></a>
<a id="report-evaluation-current-standard"></a>

## What to check

When scores are useful, retain five dimensions scored **0–4** or `not_assessed`: task fidelity, facts and evidence, explanation and synthesis, counterevidence and boundaries, and reader usefulness. The anchors are: 0, essential requirements absent; 1, major defects make the aspect unusable; 2, substantive changes needed; 3, meets the task; 4, fully developed with concrete support. Use `not_assessed` when no assessment occurred. Give located reasons; an aggregate score must not hide an actual error.

Routine repair does not require scoring for its own sake. Identifying the problematic passage, requirement or code, its consequence and the needed correction is sufficient to start work.

## Act on a problem

1. **Confirm it:** check the task and source; reproduce code failures with a minimal case. When review advice is mistaken, record the specific evidence instead of applying it automatically.
2. **Repair it:** maintainers fix code, parsing, checker or workflow defects in PRs. Authors correct report facts, recommendations, omissions and length. More warnings, scores or proposed tests are not a substitute for a fix.
3. **Verify the change:** compile or build affected code and run mandatory repository checks. Add necessary tests only for explicit task requirements or concrete failures; do not repeat passed, unaffected checks. For a report, read changed passages and their context against sources, measure any agreed length, then complete affected independent assessment under the current research contract.
4. **Complete delivery:** resolve necessary issues and pass relevant checks through the task's existing delivery process; merge ready PRs. Stop when requirements are met, without demanding that reviewers can never suggest optional edits.

| Confirmed problem | Action |
| --- | --- |
| Fabrication, factual contradiction, wrong recommendation or missing required output | Correct the content and affected conclusions, then recheck. |
| Length, format or omitted requirement | Revise the actual draft, recount and check coverage. |
| Broken citation or imprecise local wording | Correct it with the other edits; small errors still merit repair. |
| Optional style preference or mistaken allegation | Record a concrete no-change reason; do not start endless revision. |
| Invocation or parsing failure | Preserve it, fix configuration or implementation, then try again; do not call it a zero-quality report. |

Existing repair authorization covers ordinary revisions and relevant rechecking. Ask only when an actual scope or access change needs the user's decision.

## Review arrangement

Ordinary research follows the [independent role methods](../references/subagents-and-review-loop.md) and [review contract](review-completion.md): separate content perspectives, domain review, independent audit and final acceptance. This maintenance document does not replace them with one reviewer.

An explicitly designed product comparison may use a smaller anonymous judging assignment to answer its own evaluation question. Preserve that design and distinguish it from accepting the research report itself. Give the judge the original task, complete report and necessary evidence, withholding condition mappings and irrelevant author notes.

Verify important findings against original material. Re-examine affected work, preserving valid unchanged results. Keep historical evaluation protocols and originals intact; continued research completes the current contract.

## Originals and revisions

Retain the first report and judgment, and save revisions separately. An error can be repaired while its original failure remains recorded. Evaluation originals are not overwritten, but that does not prohibit repairing reports or products within authorized improvement work.

A failed check calls for diagnosis and a change, not identical repeated tests until a favorable result appears. If the same error recurs, inspect whether the correction addressed its cause and change approach. Continue the actual source, code or prose correction; a generic time or call cap does not decide whether the work is complete. Do not call unresolved work complete or keep iterating on optional polish.

## Optional comparison of Toolkit use

An effect comparison simply compares results with and without the Toolkit. Run one only to answer that additional question; it is not a prerequisite for repairs, acceptance or merging. Existing user and development tasks are usable with their reuse recorded; outside task collection is not required.

Keep task, sources and resources comparable: first drafts against first drafts, revisions against revisions. Preserve failures, extra feedback and actual calls; do not equate a repeatedly repaired report with a single-generation baseline. Count different questions separately, without adding independent tasks for translations, reruns or model changes. When using blinded review, provide Astra only the brief, sources, rubric and anonymous reports.

Product work delivers the specific problem, actual change, relevant verification and merge record; see [failure handling](failure-handling.md) and the [historical improvement record](improvement-plan.md).
