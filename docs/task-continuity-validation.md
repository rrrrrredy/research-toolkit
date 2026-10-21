# Task continuity validation

[English](task-continuity-validation.md) | [简体中文](task-continuity-validation.zh-CN.md)

2026-10-21. Generic changes against a 1.3.3 working tree. No private study documents, tasks, feedback or renamed derivatives were added. See the [plan](task-continuity-plan.md) and separate [review record](task-continuity-review.md). This record preserves pre-release validation and the version recommendation; the subsequently authorized release is described in the [v1.4.0 notes](releases/v1.4.0.md).

## Code and integration

Passed: 14 continuity tests, 12 record-workflow tests, 79 workflow tests, 35 profile/reviewer tests, the packaged stdio MCP contract, and 28 existing semantic-diagnostic tests. The workflow tests use synthetic reviewers and establish execution contracts, not model judgment quality. The existing 23 diagnostic pairs were not rewritten.

Of 24 plugin-build/installation tests, 17 passed and seven Windows symlink tests were skipped. Two junction tests passed with the necessary local permissions. Version consistency, bilingual Skill/HTML synchronization, generated plugin consistency, static-site checks and diff formatting also passed.

Windows needed a writable short workspace temporary path, an extended path for deeply nested review fixtures, and authorized execution for junctions, the local HTTP mock and MCP stdio. Environment failures were retained as such; product checks were not disabled. Changed behavior was retested, without repeatedly rerunning an unchanged full workflow. A separate installation-test defect was fixed: working-tree staging must be compared with the working-tree files it copied, while Git-reference tests remain separate.

## Actual model probe

Three independently constructed short tasks covered a library pilot and unapproved proposal, a four-dimension bike-storage comparison, and a depot count with a stale total. Each run received the same source, old text, current text and request. First outputs and execution traces were retained outside the repository.

The native run read task inputs only. The methods run also read the current Skill and continuity guide. The managed run additionally used the real CLI to save assessments, select the current artifact and update requirements. All used the same signed-in Codex default configuration, without a model override. Host instructions/environment were inherited; this was not a fully isolated experiment.

| Mode | Wall seconds | Returned input tokens | Cached input subset | Output tokens | Commands |
| --- | ---: | ---: | ---: | ---: | ---: |
| Native | 64.14 | 39,356 | 32,512 | 1,358 | 1 |
| Methods | 65.44 | 44,780 | 32,512 | 1,582 | 2 |
| Methods and tools | 282.38 | 385,114 | 340,096 | 6,039 | 21 |

All three handled the key facts, superseded requirement, remaining repair and review scope correctly. No answer-quality advantage was observed on this small bundle. The managed run additionally persisted the assessments and pending repairs without claiming that the assessed documents were fixed; all 12 original inputs remained unchanged.

Managed execution cost more time and tokens. It performed persistence work absent from the other arms and repeated status queries, so the difference is not all avoidable overhead or a universal latency estimate. The guide now recommends reusing `save.current_work` and methods-only use for short assessments that need no persistent state. Usage is not billing; cached input is a subset of input, not an additional total.

This was one bundle per mode, without randomized order or an old-versus-new comparison. It does not establish longitudinal continuity, open-web research quality, real Full model-review performance or reduced user reminders.

## Boundaries and release

The 12 new independent cases in `evals/semantic_diagnostics/task-continuity-cases.json` were structurally validated, not all evaluated by a model. Labels are author-proposed and uncalibrated; the cases are not held out. Runtime references and project instructions cannot prove host compliance or semantic quality. Installed-entry upgrades, private historical-task migration, all-platform symlink behavior and long-term effects remain unverified.

Source and local plugin copies were synchronized. Version remains 1.3.3; no release or installed-entry change was made. The compatible optional API features justify consideration for the next feature release, recommended as 1.4.0, subject to release authorization.
