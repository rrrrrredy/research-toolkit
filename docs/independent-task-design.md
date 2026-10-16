# Task selection and rechecking

[English](independent-task-design.md) · [简体中文](independent-task-design.zh-CN.md)

Existing and future user tasks, development tasks, reference tests and cases are real independent tasks; tests actually executed are real tests. Model execution and evaluation also provide a user perspective: judge usefulness from actual context use, extra reading, time, rework and research results. Human participation is not a prerequisite; describe the observed benefit and its task scope. Task identity follows the research question, so repeated runs of one task remain repeated runs. Source materials retain their stated provenance, including supplied or constructed data. Astra in a separate context can review independently; no outside person, different model vendor or additional external material is required. Changes to task assignment, reviewer inputs or acceptance criteria require targeted revalidation.

## Select and record tasks

1. Select the specific problem from existing tasks and reports; identify expected behavior, the observed error and relevant sources.
2. Distinguish different research questions. Renaming, translating, changing the model or rerunning one question does not create an additional task.
3. Retain the actual task, sources, version and relevant date range. Record reuse of development cases without excluding them for that reason.
4. For ordinary software changes, compile or build affected code and run mandatory repository checks. Add necessary tests only for an explicit task requirement or concrete failure. Reuse passed, unaffected results and stop once these conditions are met. Select subsequent tasks for useful unresolved questions across domains; another company in the same report is not a different research domain.

## Astra review

Astra is an available independent reviewer for this project. It reads the task, complete report and sources in a review context separate from the author. The same model may author and review in separate contexts; an author's confirmation in its original conversation is not a separate review. No outside person, second vendor or fixed four-model panel is required.

For paired evaluation, use the same task and source conditions for both reports. The judge receives only the brief, sources, rubric and A/B report text, without author notes, condition mappings or answer keys. Preserve original judgments and resolve specific disagreements against sources.

## Repair verification and optional comparisons

Routine work follows problem, repair and recheck. Fix tool defects in PRs and report errors in revised drafts, then verify affected behavior. Review follows the selected Lite/Full profile and task requirements, without adding a reviewer by default. Retain original failures separately from revisions so changes are visible; original cases remain useful regressions.

An effect comparison simply compares results with and without the Toolkit. When that question is relevant, specify tasks, versions, resources and the comparison before running. It is not a prerequisite for repairs or merges. A specific claim to use previously unused held-out tasks needs an accurate usage history; record that study-specific usage label alongside the real task’s identity.

The [task-selection template](../evals/templates/heldout-intake.json) is optional. Its legacy filename preserves links; it does not indicate missing tasks or require outside authors. The [improvement plan](improvement-plan.md) lists concrete repair work.
