# Compressed-air efficiency: v1.4.1 versus v1.4.2 save guidance

[English](README.md) | [简体中文](README.zh-CN.md)

**Both first saves succeeded. This case showed no observed v1.4.2 reduction in initial field-entry errors or save-related rework. The newer run took longer: 606.187 seconds versus 540.125 seconds, a difference of 66.062 seconds.** One newer-run `research_start.language` correction is recorded separately, not counted as a save-field error.

October 22, 2026: **one real research question, two Lite runs, once per version**. The task asks when a factory should prioritize compressed-air leak repair, pressure and control optimization, or compressor replacement. Both runs used the same model, configuration and fixed materials. No defects were injected, and no follow-up prompts, manual report edits or extra reviewers were added. Ingestion did not rerun the research.

## Reports and result

- [v1.4.2 final brief](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/final.md)
- [v1.4.1 final brief](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/final.md)
- [Original Chinese comparison](comparison.zh-CN.md), [structured results](results.json), [shared brief](inputs/brief.md).

Both reports compare measures, applicability, interactions, sequencing and required site data. They explain why reduced airflow is not necessarily proportional electricity savings, critical endpoint pressure limits, and replacement/load matching. Neither invents plant measurements, payback or guaranteed savings. Within each run, the first and final drafts are byte-identical; there was no report revision.

| Observation | v1.4.1 | v1.4.2 |
| --- | ---: | ---: |
| First `research_save` | Succeeded | Succeeded |
| Initial source / required-reading field errors | 0 / 0 | 0 / 0 |
| Failed saves / corrective save calls | 0 / 0 | 0 / 0 |
| All save calls | 5 | 5 |
| Process start to first successful save | 144.796 s | 161.281 s |
| Shell commands reading or searching methods | 5 | 3 |
| All Toolkit MCP calls | 10 | 12 |
| Other tool-parameter corrections | 0 | 1: `research_start.language` |
| Draft checks / first author self-checks | 1 each | 1 each |
| Full session wall time | 540.125 s | 606.187 s |

Each first save submitted two sources and seven requirements, including two required-reading obligations. Both correctly paired `full_text` / `relevant_sections` with `required_source_ids`. The older run used page descriptions in `read_evidence` and a separate `evidence_path`, a supported existing form. The newer run used file paths in `read_evidence` and page/reading notes in `locator`, as recommended by the added guidance. Subsequent checks did not expose errors in those saved fields. The recommended form was used, but the older run had already saved correctly on its first attempt, so no reduction in save rework was observed.

The newer run initially passed `language: "zh-CN"` to `research_start`; after the tool required `en/zh`, it changed the value to `zh`. Error response to corrected success took **10.812 seconds**, including the Agent's response and call, with no intervening method read. This is included in total time and preserved in the [correction record](runs/v1.4.2/records/corrections.json), with links to both original requests and returns. It does not explain the entire 66.062-second total difference.

Both runs first requested the final checklist template while five requirements were still pending, then saved completion evidence after the first author self-check and submitted the checklist. This normal finishing sequence is not a save-parameter error or two self-check rounds. Each called `check-draft` once, without replay. The warning about no hard whole-artifact length range is preserved; the task specified only an approximate 1,500-character body target.

## Conditions, methods and timing

Independent sessions ran sequentially with `gpt-6-astra`, `xhigh`, `service_tier=default`, the same request and frozen sources. Each exported released plugin served its own native MCP tools; calls were real, not replayed or simulated. Each started with `toolkit/SKILL.zh-CN.md` and loaded further methods on demand. Actual commands are retained in each run's `command.json`; version and input hashes are in [protocol.json](protocol.json).

| Version | Frozen commit | Start → end, UTC+08:00 |
| --- | --- | --- |
| v1.4.1 | `f39e091c52d6e5fd1896385e32e3a5d39f96bad7` | 14:54:09.785 → 15:03:09.925 |
| v1.4.2 | `dacce3af5f483f93c3a2991491c9b560eb346f90` | 15:03:09.928 → 15:13:16.125 |

Materials were 20 specified pages from DOE's third-edition compressed-air sourcebook and the full two-page December 2000 DOE *Minimize Compressed Air Leaks* tip sheet, naturally requiring relevant-section and full-text reading respectively. PDFs were retrieved from public ORNL and ENERGY STAR hosts before either run. Both runs then used the same fixed materials. Retained files include the [source catalog](inputs/sources.json), [retrieval record](raw/fetch-records.json), [S1 PDF](inputs/sources/S1.pdf) / [chapter text](inputs/sources/S1.md), and [S2 PDF](inputs/sources/S2.pdf) / [full text](inputs/sources/S2.md). Failed preparation URLs and the source replacement are recorded; materials were not changed in response to run outcomes.

The older run read the entry, Lite and usage guides and made two field searches; one search included a nonexistent document path but also returned source-code matches. The newer run read the entry and Lite guide, then searched the usage guide. The 5 / 3 counts are complete read/search commands, not distinct files, tokens or time savings; commands may name multiple files. Automatic stage guidance is retained separately in tool responses. Two fewer method commands did not reduce save errors or rework in this case.

Session wall time runs from process launch to exit, including reading, reasoning, calls, corrections, drafting, self-checking and the final message. First-save latency includes preceding reading/preparation, not just field entry; event timestamps record receipt. Shared preparation took 366.785 seconds, both runs totaled 1146.312 seconds, and original delivery organization took 349.729 seconds: 1862.854 measured seconds overall. Opening/orientation before the first clock reading was unmeasured. These are original research-delivery timings, not this ingestion's duration; see [timing.json](timing.json). No monetary cost is inferred.

## Retained records

| Artifact | v1.4.1 | v1.4.2 |
| --- | --- | --- |
| First save request / response | [Request](runs/v1.4.1/records/toolkit-calls/02-research_save.request.json) / [response](runs/v1.4.1/records/toolkit-calls/02-research_save.response.json) | [Request](runs/v1.4.2/records/toolkit-calls/03-research_save.request.json) / [response](runs/v1.4.2/records/toolkit-calls/03-research_save.response.json) |
| Corrections and normal finish classification | [Record](runs/v1.4.1/records/corrections.json) | [Record](runs/v1.4.2/records/corrections.json) |
| First draft | [Draft](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-draft.md) | [Draft](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-draft.md) |
| First author self-check | [JSON](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-self-check.json) | [JSON](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-self-check.json) |
| Material at self-check | [Checked report snapshot](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-self-check-report.md) | [Check explanation and checked-report hash](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-self-check-report.md) |
| Final output and revision notes | [Final](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/final.md) / [notes](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/revision-notes.md) | [Final](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/final.md) / [notes](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/revision-notes.md) |
| Full method-read commands | [Reads](runs/v1.4.1/observed-method-reads.json) | [Reads](runs/v1.4.2/observed-method-reads.json) |
| Complete request / response index | [Index](runs/v1.4.1/records/call-index.json) | [Index](runs/v1.4.2/records/call-index.json) |
| Public execution-event export | [Events](runs/v1.4.1/events.jsonl) | [Events](runs/v1.4.2/events.jsonl) |
| Per-event timestamps | [Times](runs/v1.4.1/event-times.jsonl) | [Times](runs/v1.4.2/event-times.jsonl) |
| Actual session timing and usage | [execution.json](runs/v1.4.1/execution.json) | [execution.json](runs/v1.4.2/execution.json) |

The newer `first-self-check-report.md` is an explanation containing the checked report's hash. That report remains available as the unchanged first and final drafts; the explanation is not described as a body snapshot.

## Archive scope

Research artifacts, full MCP requests/responses, method commands, event timestamps, source/requirement records, shared inputs, original comparison and timings are byte-preserved. Event logs follow the existing public-export format: event order, IDs, status, exit codes, messages and usage retained; host paths normalized; shell commands represented by previews and original hashes, outputs by hashes and character counts. Full method commands and MCP requests/responses are also stored separately. Local original events are untouched; event links in the original comparison resolve to the public exports here.

Duplicate raw PDFs, intermediate extraction/renderings, local preparation/launch/organization helpers, duplicate plugin installations, caches and locks are omitted. Actual PDFs and texts in the shared and per-run inputs remain. [archive-manifest.json](archive-manifest.json) records omissions, original hashes and export mappings; [artifact-hashes.json](artifact-hashes.json) binds every public file except itself. Historical local paths remain provenance; use relative navigation links.

This change only archives existing results and synchronizes entry points. It changes no product code, adds no runs, checking mechanism or review, and publishes no release.
