# Task selection and rechecking

[English](independent-task-design.md) · [简体中文](independent-task-design.zh-CN.md)

Existing and future user tasks, development tasks, reference tests and cases are real independent tasks; tests actually executed are real tests. Task identity follows the research question, so repeated runs of one task remain repeated runs. Source materials retain their stated provenance, including supplied or constructed data. Astra in a separate context can review independently; no outside person, different model vendor or additional external material is required. Changes to task assignment, reviewer inputs or acceptance criteria require targeted revalidation.

Existing user and development tasks can be used directly for product improvements and rechecking. A real task remains real after use in development. Distinct research questions can be independent tasks without outside authors. The project has tasks for repair work; outside contributions, a task custodian and a new dataset are not prerequisites.

## Select and record tasks

1. Select the specific problem from existing tasks and reports; identify expected behavior, the observed error and relevant sources.
2. Distinguish different research questions. Renaming, translating, changing the model or rerunning one question does not create an additional task.
3. Retain the actual task, sources, version and relevant date range. Record reuse of development cases without excluding them for that reason.
4. Recheck the original failure after a repair, then use relevant existing tasks to check for regressions. Add a task only when existing cases miss a concrete problem, not to reach an arbitrary count.

## Astra review

Astra is an available independent reviewer for this project. It reads the task, complete report and sources in a review context separate from the author. The same model may author and review in separate contexts; an author's confirmation in its original conversation is not a separate review. No outside person, second vendor or fixed four-model panel is required.

For paired evaluation, use the same task and source conditions for both reports. The judge receives only the brief, sources, rubric and A/B report text, without author notes, condition mappings or answer keys. Preserve original judgments and resolve specific disagreements against sources.

## Repair verification and optional comparisons

Routine work follows problem, repair and recheck. Fix tool defects in PRs and report errors in revised drafts, then use applicable checks and Astra review. Retain original failures separately from revisions so changes are visible; original cases remain useful regressions.

An effect comparison simply compares results with and without the Toolkit. When that question is relevant, specify tasks, versions, resources and the comparison before running. It is not a prerequisite for repairs or merges. A specific claim to use previously unused held-out tasks needs an accurate usage history; that special label does not determine whether existing real tasks are independent or usable.

The [task-selection template](../evals/templates/heldout-intake.json) is optional. Its legacy filename preserves links; it does not indicate missing tasks or require outside authors. The [improvement plan](improvement-plan.md) lists concrete repair work.
