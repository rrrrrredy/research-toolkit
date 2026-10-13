# Problem repair and verification roadmap

[English](evaluation-roadmap.md) | [简体中文](evaluation-roadmap.zh-CN.md)

Current work fixes observed problems and checks the result. Use existing real tasks with Astra as the independent reviewer. Outside reviewers, outside task collection and a fixed four-model panel are not required. See the [report checking and repair standard](report-evaluation-standard.md).

<a id="current-report-and-review-plan"></a>

## Current order

1. Locate the problem in existing reports and execution records; distinguish software defects, missing methods, missed instructions and draft errors.
2. Fix reproducible software failures, add relevant regressions and submit a PR. Change instructions when a method is actually missing; do not turn every model error into more rules.
3. Correct inaccurate facts, recommendations, omissions or length in failing drafts. Check the current file and have Astra compare it with the task and sources.
4. Deliver or merge after necessary issues are resolved and relevant checks pass. Keep original failures and repaired versions separately.

This work does not wait for an additional research project. Tests verify a change rather than repeatedly sample for a favorable result.

## Existing material and checks

[Evaluation status](evaluation-status.md) records real research tasks, development reports, diagnostics and model reviews. Development use does not invalidate a real task; different questions remain distinct tasks. Renaming, translating or changing models does not add tasks.

Software regressions check inputs, state, parsing, version bindings and delivery rules. Astra checks report judgments against sources. A mechanical pass describes the tested software behavior; content acceptance follows the actual review. Routine repair requires no additional review team, custodian or admission project.

## Remaining problems

The [improvement plan](improvement-plan.md) tracks concrete errors: missed length requirements, choices that contradict the supplied numbers, and unrecorded conditions described as observed changes. Record the correction, recheck and completion for each; an abstract semantic-reliability study is not a substitute for repair.

<a id="track-b-held-out-real-task-efficacy"></a>
<a id="next-study-freeze-the-design-then-collect-new-evidence"></a>

## Optional: compare results with and without the Toolkit

Earlier references to an effect study meant comparing Toolkit and baseline results. This is optional, not a prerequisite for current repair, acceptance or merging. It requires neither outside tasks nor outside people. When useful, use existing real tasks, specify versions, review and resources before running, preserve first and revised reports separately, and use Astra for review.

The [paired template](../evals/templates/paired-study.json) and [task-selection guide](independent-task-design.md) organize that comparison; filling them is not a gate to ordinary work. Explain results for the actual completed tasks. Preserve original failures and do not present revisions as first drafts.

## Historical records and publication

Preserve older experiments with their actual models, reviewer counts, scales, attempts and failures. Do not backfill new rules; historical four-model configurations are not current defaults. Publish shareable material with necessary source and version information. Merge verified repair PRs without waiting for an extra comparison.
