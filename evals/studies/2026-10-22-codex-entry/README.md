# Codex architecture: v1.4.0 versus v1.4.1 research-entry comparison

[English](README.md) | [简体中文](README.zh-CN.md)

**This case showed no observed v1.4.1 gain in requirement understanding, instruction following or research quality. The newer version took longer: 603.484 seconds versus 473.265 seconds, a difference of 130.219 seconds. Existing interface diagnostics helped correct metadata, but that behavior is identical in both versions and is not a v1.4.1 benefit.**

This archive contains **one real research question and two Lite runs**, one per version. The user changed the topic from direct-to-cell satellite service to Codex, specifying technical architecture, Agent operation and design tradeoffs. No satellite task was run. There were no injected defects, extra research reviewers, follow-up prompts or manual edits during either run.

## Reports and observed result

- [v1.4.1 final report](runs/v1.4.1/tasks/codex-architecture-zh-20261022/final.md)
- [v1.4.0 final report](runs/v1.4.0/tasks/codex-architecture-zh-20261022/final.md)
- [Original Chinese comparison](comparison.zh-CN.md), [shared brief](inputs/brief.md), [source catalog](inputs/sources.json), [frozen protocol](protocol.json), [recorded results](results.json).

The executing research agent compared the shared requirements, sources, first drafts, first self-checks and final reports directly. No additional review agent or scoring round was introduced.

| Focus | v1.4.0 | v1.4.1 | Observed comparison |
|---|---|---|---|
| Requirement understanding | Follows a bug-fixing request through Thread, Turn, Item, tool feedback and approvals; explains responsibilities for product designers | Follows the same execution chain and explains capability, cost and experience | Both answer how the architecture works and why it is designed that way; no observed new-version gain |
| Instruction following | Chinese report, cutoff date, approximately 2,000-character body, one comparison table, six sources; no installation tutorial or competitor survey | Meets the same main requirements and adds a direct resume/fork citation in the final revision | No clear overall improvement |
| Explanation | Separates conversation history, model-visible context and workspace files; restoring a conversation does not roll back work | Makes the same distinctions | Substantially equivalent |
| Comparison and tradeoffs | Compares CLI/SDK, local app-server and three Agents API environment options, with selection implications | Covers the same options and separates hosted Harness from executor responsibility | Both provide useful comparisons; no clear analysis advantage |
| Evidence and inference | Retains historical long-task model, access and non-production conditions; does not infer success rates, cost or causal effects | Retains those conditions and more explicitly separates model, Harness and task-design contributions | Different emphasis, similar evidence discipline |
| Readability | Conventional numbered references and smoother prose | Frequent S1/L locators help auditing but interrupt reading | No observed readability gain |

The newer report explicitly says a protocol completion status cannot itself prove a bug was fixed. The older report already notes failed/interrupted completion and judges value from artifacts and task outcomes. This is a difference in emphasis, not a clear overall quality win.

## Method loading and execution conditions

Both independent Codex CLI `0.163.0-alpha.10.2` sessions explicitly used `gpt-6-astra`, `xhigh`, `service_tier=default`, the same natural-language brief and the same six official-source excerpts frozen on October 22, 2026. They did not inherit the parent conversation or receive a prefilled interpretation. Each began with its released plugin's `toolkit/SKILL.zh-CN.md` and selected further methods on demand. v1.4.0 ran first, then v1.4.1, once each. Full commands are retained in each run's `command.json`.

| Version | Frozen commit | Start → end, UTC+08:00 on 2026-10-22 |
|---|---|---|
| v1.4.0 | `31daf72b63eb9eb395bdbfb15f8e13f495fd5177` | 12:19:39.099 → 12:27:32.375 |
| v1.4.1 | `f39e091c52d6e5fd1896385e32e3a5d39f96bad7` | 12:27:32.378 → 12:37:35.865 |

| Observation | v1.4.0 | v1.4.1 |
|---|---:|---:|
| Shell commands containing method reads/searches | 7 | 4 |
| Toolkit calls | 9 | 10 |
| Completed shell commands | 18 | 30 |
| Session wall time | 473.265 s (7 min 53 s) | 603.484 s (10 min 03 s) |
| Cumulative input tokens | 983,547 | 909,203 |
| Cached input tokens, included above | 912,128 | 827,392 |
| Output tokens | 14,810 | 20,526 |
| Follow-up prompts / manual report edits during run | 0 / 0 | 0 / 0 |

Method counts are complete shell commands, not distinct files or tokens. One command may read several files or also read sources. Stage guidance is retained in Toolkit responses and is not counted again as a file read. The older run searched guides and printed selected sections, then read optional analysis lenses and writing style. The newer run requested entire Lite and usage guides and optional analysis lenses, with no separate writing-style read observed. Fewer read commands did not produce a better report or shorter execution in this case.

Both used same-dimension comparisons, mechanism explanations and conditional choices after reading optional analysis methods. There was no without-Toolkit arm, so this does not attribute all of that analysis to Toolkit. Memory, other plugins, subagents and online search were disabled, but the host still exposed system Skill entries: the older run read `openai-docs/SKILL.md`; the newer one did not. This observed difference is retained without a rerun or configuration change.

## First self-checks and encountered issues

**v1.4.0:** all six first self-check items were true. The first draft, report at first self-check and final report are byte-identical. The direct comparison found no key architecture conclusion requiring correction. A mistyped `claim_registry.csv` read was followed by the correct `claims_registry.csv` read; an AGENTS.md search returned no match. The first finish-template response listed seven pending requirements, after which the Agent saved completion evidence and submitted successfully. These events are preserved.

**v1.4.1:** the first self-check set `claims_and_sources` and `limitations` to false. It subsequently added direct resume/fork source lines and an author-check disclosure outside the report body. The final body differs only by added citation line numbers; see [the original diff](runs/v1.4.1/draft-to-final.diff). The analysis and comparison table were not rewritten.

The newer run also used an invalid `reading_requirement` value and combined explanatory text with a `read_evidence` path. Existing responses identified the allowed values and the correct field/path usage. The Agent corrected the records without user intervention. These validators are unchanged between versions; their useful recovery behavior is not a new-version gain. The newer run's truthful false items also do not establish reduced false passes, because the older report did not show a corresponding false pass.

## Retained artifacts

| Artifact | v1.4.0 | v1.4.1 |
|---|---|---|
| First complete draft | [Draft](runs/v1.4.0/tasks/codex-architecture-zh-20261022/first-draft.md) | [Draft](runs/v1.4.1/tasks/codex-architecture-zh-20261022/first-draft.md) |
| First self-check | [Checklist](runs/v1.4.0/tasks/codex-architecture-zh-20261022/first-self-check.json) | [Checklist](runs/v1.4.1/tasks/codex-architecture-zh-20261022/first-self-check.json) |
| Report at first self-check | [Report](runs/v1.4.0/tasks/codex-architecture-zh-20261022/first-self-check-report.md) | [Report](runs/v1.4.1/tasks/codex-architecture-zh-20261022/first-self-check-report.md) |
| Final report | [Final](runs/v1.4.0/tasks/codex-architecture-zh-20261022/final.md) | [Final](runs/v1.4.1/tasks/codex-architecture-zh-20261022/final.md) |
| Revision notes | [Notes](runs/v1.4.0/tasks/codex-architecture-zh-20261022/revision-notes.md) | [Notes](runs/v1.4.1/tasks/codex-architecture-zh-20261022/revision-notes.md) |
| Full method-read commands and event IDs | [Reads](runs/v1.4.0/observed-method-reads.json) | [Reads](runs/v1.4.1/observed-method-reads.json) |
| Interface requests and responses | [Calls](runs/v1.4.0/research-records/toolkit-calls/) | [Calls](runs/v1.4.1/records/toolkit-calls/) |
| Public execution-event export | [Events](runs/v1.4.0/events.jsonl) | [Events](runs/v1.4.1/events.jsonl) |
| Actual timing and usage | [Execution](runs/v1.4.0/execution.json) | [Execution](runs/v1.4.1/execution.json) |

The two sessions total **1,076.749 seconds (17 min 57 s)**, including reads, analysis, drafting, self-checks, metadata errors and corrections. Preparation from the measured start to the first run took 261.099 seconds. The recorded preparation-to-delivery window was **1,561.266 seconds (26 min 01 s)**; some comparison work overlapped the second run. Earlier topic/repository orientation and some source lookup were unmeasured. These intervals must not be added again; see [timing.json](timing.json). Ingestion time is outside the research timing window.

CLI token usage is not a bill, and cached input is a subset of total input. New-version input was lower, but output and wall time were higher; this case supports no overall time/cost saving. The observed time difference is not a causal estimate of the patch's stable runtime effect.

## Archive scope

First drafts, first self-checks and corresponding reports, final outputs, revision notes, full method-read commands, interface requests/responses, timings, usage, common inputs and the original Chinese comparison are byte-preserved. Six exact model-input excerpts retain source URLs, retrieval dates, original line locators and hashes. Frozen input and plugin-file hashes are in `protocol.json`; the original run comparison recorded no input or plugin changes.

Event logs follow the existing public-library archive convention: retain event order, status, exit codes, agent messages and usage; normalize host paths; retain a 240-character command preview plus original hash, and command-output hashes and character counts. Full method-read commands remain separately available in `observed-method-reads.json`. Original local event captures are unchanged. Event links in the byte-preserved Chinese comparison resolve to these public exports in this archive.

Full webpage snapshots, local preparation/launch scripts, duplicate plugin installations, caches and locks are not copied. The omitted webpage snapshots and local scripts are listed by hash and reason. Historical paths in preserved records are provenance, not portable links; use this guide's relative links. Python helpers under `runs/` are captured execution artifacts, not new product code.

[archive-manifest.json](archive-manifest.json) records preserved files, exports and omissions. [artifact-hashes.json](artifact-hashes.json) binds every archive file except itself. This ingest does not modify product code, add a review, rerun models or previously passed tests, or release a version.
