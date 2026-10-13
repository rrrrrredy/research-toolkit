# Development protocol v2: outputs, masking and task design

[English](eval-protocol-v2.md) · [简体中文](eval-protocol-v2.zh-CN.md)

This is an opt-in extension of the [fixed-source Lite pilot](eval-protocol.md). It changes prospective execution, not the frozen October 10 study. The original protocol change supplied no quality results; subsequent dated connectivity and calibration records remain separate evidence. Schema 1 remains supported. Schema 2 currently accepts `prospective_development` only; an exposed task pack cannot become held out by changing its label.

## What is frozen

Start from [the empty v2 template](../evals/templates/blinded-study.v2.json), or inspect the [five-family fictional development pack](../evals/tasksets/development-v2-synthetic/README.md). Set author/judge endpoints, requested models, accepted returned model IDs and snapshot limitations. Use different author and judge identities; overlapping declared IDs are rejected. This does not independently attest provider identity or model-family independence. Freeze a separate plan per author model, retaining shared family IDs across model strata.

Each role declares `output_protocol` and `allow_json_fence`; HTTP roles also declare `response_format`. `response_format: text` omits the API format option; `json_object` sends that explicit option and requires provider support. Check current provider documentation before choosing it. There is no automatic provider detection, format fallback or retry. Both author conditions use the same protocol, model settings and limits.

The default author protocol, `markdown_notes_v1`, requires the complete Markdown report followed by exactly one own-line separator:

```text
<<<RESEARCH_NOTES_V1>>>
```

Everything before that separator is the report, preserved without trimming or editing. Everything after it is working notes. Missing/multiple separators are format failures. Alternatively, `json_object_v1` requires `report` and `notes` strings. The judge uses `json_object_v1` with the existing five-dimension schema. When `allow_json_fence` is true, one whole-output fence with no language tag or the exact tag `json` is accepted; surrounding prose, concatenated objects and duplicate fields are rejected. Nothing searches arbitrary prose for a plausible JSON object. This policy is declared before generation, not applied later to rescue preferred results.

All API response bytes remain in `response.json`; successful message extraction additionally produces `content.txt`, `parse.json` (protocol, method on success, content hash and status), and `parsed.json` or `invalid.json`. Transport failures use `execution.json.failure_kind`: HTTP, transport, timeout, response envelope/size, model identity, missing usage, token budget, truncation, incomplete finish or empty content. These are execution/format outcomes, not research-quality defects. Oversized replies retain a bounded prefix and say so. Total tokens and wall time are checked after return; they are not guaranteed billing caps or remote cancellation.

`max_retries` is zero. `max_requests` must equal three requests per family, or four with `position_swap: true`: two authors, one primary judge and optionally one swapped judge. Missing author output skips both judges for that pair; a missing primary judgment does not cancel its predeclared swap. `request_plan` freezes these ceilings and results record attempted calls. Running four models on five families with swaps would allow **80** requests, not 20; this pack only supports offline inspection; actual execution follows a separately frozen plan. The separate improvement plan's at-most-five-call connectivity phase comes first.

`prepare` freezes source/brief text hashes, design records, instructions, rubric, code hash, assignments and limits. `execute` checks the commitment and, for schema 2, refuses a changed harness before making calls. Inputs are frozen as UTF-8 text after Python universal-newline reading; these are text hashes, not original source-file byte hashes. Git must be on PATH. A new harness requires a new study directory. A started run cannot be silently resumed or overwritten.

```bash
python scripts/run_blinded_evals.py prepare --study evals/tasksets/development-v2-synthetic/study.json --seed 20261012 --output evals/runs/v2-inspection
```

This inspection command makes zero model calls. The supplied model/endpoint values are placeholders; a real run needs verified settings and a separately frozen plan. Never put credentials in configs, source material, command arguments or public artifacts. Only environment-variable names belong in endpoint configuration.

## 2026-10-13 prospective instruction correction

New freezes use the actual Lite stage guide in the author method bundle, replacing the Full workflow reference previously injected by this instruction-only harness. JSON instructions now explicitly require string-valued `report` and `notes`; the parser was already strict and is not relaxed. A common final envelope reminder in both conditions keeps process disclosures in notes and preserves the brief's length/citation contract. These changes address concrete [October 12 failures](../evals/studies/2026-10-12-lite-four-models/README.md); old code, packets, failures and scores remain frozen. The new [eight-request feedback diagnostic](../evals/diagnostics/2026-10-13-feedback-probes/README.md) uses two new fictional tasks and is not an efficacy study.

## Task admission and information separation

Each of the 5–10 distinct families requires a design JSON path containing `role: development`, `material_kind`, `rationale`, `provenance`, `exclusions`, `expected_judgments` and `exposure`. The last two fields are nonempty lists. Design records stay in `coordinator/frozen.json`; authors receive only the brief/sources and assigned instructions. Judges receive only the brief, identical sources, rubric and reports A/B. The expected judgments are coordinator annotations, not author hints or automatic judge scores. Schema checks cannot prove a task is independent or its sources sufficient; review those claims before freezing.

Use three distinct pools:

| Pool | Purpose | Current material |
| --- | --- | --- |
| Development | Diagnose defects and tune methods | Five exposed fictional families, 3 English and 2 Chinese |
| Judge calibration | Check specific known errors, valid controls and position sensitivity | Four separate English/Chinese families: arithmetic, causation, attribution and decision constraints; each has a swap and identical-valid tie |
| Future held-out study | Assess a frozen change on inputs unused for tuning | [Independent intake design](independent-task-design.md) supplied; no admitted external tasks or held-out efficacy claimed |

These are purposive examples, not a representative workload sample. Translations, different author models and label swaps do not add independent families. Synthetic tasks check protocol behavior; real research evaluation also needs rights-cleared real sources, provenance, cutoffs and live retrieval when essential to the question. Retain rejected candidate IDs and reasons before outcomes, and retain all admitted failures afterward.

## Masking and calibration

Reports are passed verbatim; never remove revealing or unfavorable sentences after seeing outputs. `coordinator/masking-observations.json` records literal occurrences of a small set of Toolkit/condition/model terms and each report hash. This advisory scan neither excludes reports nor proves successful blinding. It misses paraphrases, aliases and stylistic clues. The judge's existing `condition_clues` field supplies an additional observation after rating.

Only `judge-inputs/` goes to a judge context. Keep coordinator keys, development answers, author requests/notes, metadata, the repository and this design conversation inaccessible there. The optional [Codex judge adapter](native-judge.md) starts fresh tool-disabled native contexts and records its isolation and identity limits. HTTP remains the author transport. Native adapter code is frozen and checked alongside the main harness. A model that authored a report must not serve as its independent judge. Separate fresh calls alone do not establish statistical independence.

When swaps are enabled, both orientations use fresh requests. All first judgments/failures lock before decoding. Primary results remain primary; `position_swap` records the swapped preference, decoded condition and consistency (`null` when either outcome is unresolved). Disagreement cannot be repaired by selecting the favorable orientation, averaging it away or rerunning it. Swaps are sensitivity observations within the same family.

Before any quality study, use the [separate calibration packets](../evals/tasksets/judge-calibration-v3/README.md) without their coordinator manifest. Four public development families cover English arithmetic/decision constraints and Chinese causation/source attribution; they reuse the unchanged v2 arithmetic inputs. Require located evidence for each known error, stable identification after swaps and no invented substantive difference in identical-valid pairs. Preserve failures and adjudicate explanations against sources. [The October 12 Astra calibration](../evals/diagnostics/2026-10-12-astra-calibration/README.md) retains all 12 first attempts and source adjudication, including dimension-score drift. A new judge/model setting still requires its own separately frozen 12-request calibration budget, in addition to connectivity calls. Four families are not 12 independent observations. Passing these controls does not establish five-dimension judge reliability or Toolkit efficacy.

## Offline acceptance

```bash
python scripts/check_blinded_evals.py
python scripts/check_blinded_protocol_v2.py
python scripts/check_judge_calibration.py --self-test
python scripts/check_live_execution.py
python scripts/check_study_verification.py
python scripts/check_development_evidence.py --self-test
python scripts/check_feedback_probes.py --self-test
```

These checks exercise parsing controls, raw retention, API options, aliases, failures, frozen-code rejection, task admission, metadata isolation and swapped-outcome decoding. They make no real model calls and establish software behavior only.
