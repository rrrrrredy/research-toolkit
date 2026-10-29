# Continuing an existing research task

[English](task-continuity.md) | [简体中文](task-continuity.zh-CN.md)

Use the existing task and records when a user supplies new material, requests a comparison, changes scope or asks for revision. A new report filename is not a new research task. These instructions apply at resume, substantive change and delivery, not after every sentence edit.

## Project entry

A project's existing agent instructions can point here without copying the toolkit or adding a tracker:

> Resume from the effective user requirements, current report, relevant sources and unfinished work. Reuse valid research, preserve earlier versions when revising, and check the actual result before declaring completion. Follow the task's agreed review requirements.

Skill-only work can recover this information from the conversation, supplied files and existing notes. When handing off or changing sessions, preserve what would otherwise be lost; no fixed registry, version log or receipt is required. New user instructions replace conflicting old ones; goals that were not cancelled remain effective. Accepting feedback does not establish that the report has been corrected.

For a CLI/MCP-managed task, use its task ID and workspace as described below. `start/status.runtime` identifies the local implementation and available entry file, not the Skill actually loaded by the host. If the installed entry is suspect, use the existing installation comparison against an explicit revision; do not add a routine health check or silently upgrade an ongoing task.

## Resume and save

This section applies to CLI/MCP-managed tasks; Skill-only work uses the existing material described above.

`research_status` returns `current_work`: specification and requirement paths, open requirement records, an explicitly selected artifact, and a separate last-delivery reference when present. Read relevant existing notes and the actual documents; a summary or author reply does not substitute for them. Check supplied local paths before declaring an attachment unavailable. If it is genuinely unavailable, describe the comparison's actual scope and continue unaffected work.

Use `research_save` to update only affected fields and records. Optional `brief` is a partial update to the six brief fields and writes `state/task_spec.md` with `progress.brief` together. Save changed requirements with stable IDs in the same request where practical. New user instructions replace conflicting old instructions; goals that were not cancelled remain effective. Keep the user's actual scope decision when waiving a requirement.

Brief updates preserve manually added specification sections. If a field was edited directly and no longer matches its saved value, reconcile that field before retrying; the batch is rejected without overwriting other content. An explicit scope decision may retire a legacy reading obligation without rewriting its historical metadata; reopening it requires a valid reading requirement. Use `save.current_work` to inspect the returned state instead of immediately repeating the same status query.

Register a current main artifact with `draft.main=true`. Optional `draft.kind` identifies `report`, `comparison` or `review`; it describes what this task is delivering, not the maturity of a different document being reviewed. `complete=true` records a complete draft, not completed delivery. A partial/reference draft never becomes the main artifact just because it was saved later. Saving the registered main path updates its observed hash. Review and finish must name that path. Legacy tasks without a registered main retain their existing behavior; no newest-file guess is made.

Acceptance of feedback is not proof of repair. Keep accepted changes pending until the actual text and relevant context have been checked; then save specific evidence with the existing requirement or finding disposition. Do not create a second feedback ledger. For a comparison or review delivery, distinguish a completed assessment from revisions still needed in the assessed document.

## Review the necessary scope

- **Full comparison:** read both supplied current documents across the requested scope. Differences in summaries are leads, not the comparison itself. Preserve valid complementary explanations without concatenating both texts or forcing one author's organization.
- **Bounded revision with a valid baseline:** inspect the complete diff, changed passages and context, affected sources/requirements and any open findings. Reuse unchanged evidence already read. For tool-managed review, use the existing `revision=true` path and make a real judgment of the current complete report with its frozen input; never copy the old PASS, replace its hash or infer global approval from a local check. A separate reviewer still receives the complete required assignment.
- **Missing or unreliable baseline:** identify the uncovered scope and read enough to assess it. Do not retrospectively certify intervening versions. A last small edit does not make an unreviewed earlier revision approved.

Self-review is not independent review. An explicit independent requirement needs a separate context. Existing adapter imports must preserve the actual execution identity, original response and exact assignment; when marked `capture.import_only=true`, the import is accounted separately from model calls. This flag neither verifies independence nor relaxes review binding. Do not fabricate an execution identity, duration or token count for old feedback.

Withdraw criticisms resolved by the new text. Use optional or evidenced no-change decisions for preference differences. Once required issues are resolved and the declared checks pass, stop; an unchanged result does not need another reviewer simply to find something new.

## Editing without losing the analysis

Remove repeated exposition and process narration while retaining dates, prediction status, experimental conditions and the limits of each source. Check attribution across entities, product versions and research stages. Presence of a term or section proves neither correct explanation nor application to the conclusion.

For decision-oriented research, preserve the recommendation, its reasons, alternative costs and conditions that would change it. Explain relevant technical mechanisms and cooperation incentives where the question requires them. Avoid inventing internal teams, resources or schedules. A request to stop assigning responsibilities does not remove the need to analyze the relevant ecosystem. Titles and section counts follow the current user's request, not a universal report template.

## Recover a manual or stale project

Read the existing specification, effective user changes, available drafts and unresolved feedback. Preserve originals; resolve contradictory references using actual contents and user decisions, not directory timestamps. Select the current artifact explicitly. Repair only records needed to continue. For tool-managed collections, `replace` retains backups. Do not normalize every historical file, infer unobserved reading or reconstruct past execution receipts.

Preserve existing completion requirements and use [historical task compatibility](../docs/usage-modes.md#historical-task-compatibility). Reuse valid materials without rewriting history.

These practices can reduce specific omissions; deterministic checks and diagnostic cases do not establish a general improvement in report quality or time saved.


`current_work.effective_requirements` retains applicable rows, including satisfied ones; `open_requirements` continues to list unfinished work and `scope_decisions` retains scope decisions. `research_outputs` recovers registered analyses, host references and input changes. Use existing `status.work` for readable handoff/revision input; see [research handoff](../docs/usage-modes.md#research-delegation-and-handoff). A satisfied requirement can still constrain revision; changed input does not require repeating all previous work.
