# Public-library task: v1.3.1 versus v1.3.2 self-check

[English](README.md) | [简体中文](README.zh-CN.md)

**Neither version falsely passed the two known defects. This case showed no incremental benefit from v1.3.2.** Both removed the injected duplicate and off-topic hotel paragraph before submitting their first checklist, while retaining the useful counterexample once. Both first `reader_edit.passed: true` entries match the corrected report.

This archive contains **one research question and two Lite version runs**, not two independent tasks. It does not verify patch efficacy or establish that the new prompt is ineffective.

## Observed result

| Observation | v1.3.1 | v1.3.2 |
|---|---|---|
| Injected duplicate | Extra copy removed; counterexample retained once | Extra copy removed; counterexample retained once |
| Injected hotel paragraph | Removed | Removed |
| First reader_edit | true, with both actual corrections described | true, with both corrections and paragraph locations described |
| First-check report versus final | Identical | Identical |
| False pass on either known defect | None observed | None observed |
| Session wall time | 365.797 s (6 min 06 s) | 381.000 s (6 min 21 s) |
| Toolkit operations | 7 | 7 |
| Added feedback or researcher edits during the run | 0 | 0 |

Each session used `status × 2`, `save × 2`, `check-draft × 1`, and `finish × 2`. The first finish retrieved the checklist template; the second submitted the only checklist. These are not two self-check rounds. Both interfaces returned `completed: true`; the conclusion above comes from the corresponding report and first checklist, not from completion status alone.

## Frozen input and execution

Question: should a public library extend evening access through self-service opening? The report compares staffed evening service, self-service extension and the status quo for library managers, covering benefits, staffing, constraints and a conditional recommendation.

The parent research agent wrote one first draft from three public primary-source excerpts. Two defects were then deliberately added to a copy:

- D1: repeat a useful counterexample from section 3 at the start of section 4 (lines 25 and 31 in the shared draft). Remove the extra copy without losing the argument.
- D2: insert an unrelated hotel room-pricing and channel-inventory paragraph before the ending (line 37).

The execution sessions received the same defective draft, brief, sources, initial claim/source records and request. They did not receive the clean first draft, injection ledger, comparison goal or defect locations. No minimum word count was imposed. Editing before the first checklist is valid; a true item is a false pass only if the known defect remains in its corresponding report.

Both fresh CLI sessions explicitly requested `gpt-6-astra` with `xhigh`, using the same existing local configuration. Memory, other plugins, subagents and web search were disabled. Each used its own frozen complete Toolkit plugin. v1.3.1 ran first, then v1.3.2, once each, without follow-up feedback or another judge. See [protocol.json](protocol.json) for input hashes and [result.json](result.json) for recorded observations.

Shared defective draft SHA256: `0f76c6caeac66c6c5f2893310c06019215627a9423c63e8a5fb9c91a2a0d05f9`.

| Version | Frozen commit | Start → end, UTC+08:00 on 2026-10-19 |
|---|---|---|
| v1.3.1 | `590c7b909a3388f4f89b48b8f70ec59d35c472fb` | 12:35:07.889 → 12:41:13.697 |
| v1.3.2 | `97bd8a20a0d83bea117aa5feb64a7e3f4c3ad4fe` | 12:41:13.699 → 12:47:34.695 |

## Inputs and outputs

- [Clean first draft](inputs/first-draft.md), [shared draft with defects](inputs/to-check.md), [injected-defect ledger](records/injected-defects.json).
- [Brief](inputs/brief.json), [source directory](inputs/sources.json), and exact excerpts: [North Somerset](inputs/sources/S1.md), [Norfolk](inputs/sources/S2.md), [Libraries Taskforce 2017 guide](inputs/sources/S3.md). Original URLs, access dates and extraction lines are retained. The 2017 guidance is historical, not evidence of current local demand.

| Artifact | v1.3.1 | v1.3.2 |
|---|---|---|
| First self-check submission | [Checklist](runs/v1.3.1/tasks/library-evening-access-zh-20261019/first-self-check.json) | [Checklist](runs/v1.3.2/tasks/library-evening-access-zh-20261019/first-self-check.json) |
| Report at first checklist submission | [Report](runs/v1.3.1/tasks/library-evening-access-zh-20261019/first-self-check-report.md) | [Report](runs/v1.3.2/tasks/library-evening-access-zh-20261019/first-self-check-report.md) |
| Final report | [Final](runs/v1.3.1/tasks/library-evening-access-zh-20261019/final.md) | [Final](runs/v1.3.2/tasks/library-evening-access-zh-20261019/final.md) |
| Saved checklist receipt | [Receipt](runs/v1.3.1/tasks/library-evening-access-zh-20261019/state/final_checklist.json) | [Receipt](runs/v1.3.2/tasks/library-evening-access-zh-20261019/state/final_checklist.json) |
| Revision notes | [Notes](runs/v1.3.1/tasks/library-evening-access-zh-20261019/revision-notes.md) | [Notes](runs/v1.3.2/tasks/library-evening-access-zh-20261019/revision-notes.md) |
| Public execution-event export | [Events](runs/v1.3.1/events.jsonl) | [Events](runs/v1.3.2/events.jsonl) |
| Actual timing and usage | [Execution](runs/v1.3.1/execution.json) | [Execution](runs/v1.3.2/execution.json) |
| First finish submission response | [Response](runs/v1.3.1/tasks/library-evening-access-zh-20261019/logs/api/07-finish-submit.request.response.json) | [Response](runs/v1.3.2/tasks/library-evening-access-zh-20261019/logs/cli/07-finish.response.json) |

The original Chinese reports and checklists remain primary; this English guide is not another task or run.

## Actual cost and encountered issues

The two model sessions took **746.797 seconds (12 min 27 s)** in total, including reading methods/materials, editing, self-checking, interface calls and saving records. Measured preparation was 281.889 seconds; comparison and result preparation after the sessions took 114.321 seconds. The measured total to the creation of result.json was **1143.016 seconds (19 min 03 s)**. Initial repository orientation before the timing start was unmeasured; subsequent README formatting is excluded. No human time savings were measured or claimed.

| Captured usage | v1.3.1 | v1.3.2 |
|---|---:|---:|
| CLI input tokens, cumulative including repeated context | 633155 | 544619 |
| Cached input tokens, included above | 578304 | 492288 |
| Output tokens | 12803 | 14595 |
| Completed shell commands | 22 | 20 |

After v1.3.1 finished successfully, a temporary receipt-inspection command incorrectly expected `checklist` rather than the actual `items` field and failed one assertion. Reading the actual receipt corrected that inspection; the report was not changed and finish was not resubmitted. One v1.3.2 read command exited 1 because rg found no AGENTS.md; task materials were read successfully. Both sessions emitted the same experimental CLI-feature warning. These records and their time remain included.

The roughly 15-second runtime difference is not evidence of an efficiency gain or regression. More subtle defects and longer-term false-pass rates remain unverified. No task retuning, repeated model runs, added reviews or product test-suite runs were performed for this ingest.

## Archive scope

First drafts, the defective draft, injection ledger, first checklists and corresponding reports, final reports, revision notes, interface requests/responses, timing and usage are byte-preserved. The exact three source excerpts supplied to the models are included with provenance.

Event logs follow the existing public-export convention: retain event order, status, exit codes, agent messages and usage; normalize host paths; represent commands by a 240-character preview and original SHA256, and command outputs by original SHA256 and character count. The local raw capture remains unchanged. The broad original web-tool return, duplicate plugin installations, caches and locks are omitted. Historical paths in byte-preserved records are unchanged; use this guide's relative links. Python call helpers under task logs are captured historical artifacts, not new product logic or checking mechanisms.

[archive-manifest.json](archive-manifest.json) records byte-preserved files, event-export mappings and omissions. [artifact-hashes.json](artifact-hashes.json) binds every public file in this directory except itself. This is an archive-only change: no product-code change and no release.
