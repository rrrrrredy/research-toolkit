# Multi-turn research continuity plan

[English](task-continuity-plan.md) | [简体中文](task-continuity-plan.zh-CN.md)

2026-10-21. Scope: generic product defects and workflow continuity. No private manuscripts, tasks, feedback, excerpts or renamed derivatives enter the repository. Tests use independently constructed minimal tasks. Implementation and publication are separate; the subsequently authorized release is described in the [v1.4.0 notes](releases/v1.4.0.md).

| Order | Work | Evidence required |
| --- | --- | --- |
| 1 | Validate reading requirements at save; separate imported reviews, self submissions and model invocations; align documentation | Invalid batches do not partially write; import time is not model time; old calls remain compatible |
| 2 | Add optional main-artifact selection and partial brief updates to save; expose implementation identity and resume references | New work does not inherit an old delivery; reference drafts do not replace the main; current requirements are visible; reads preserve history |
| 3 | Document project entry, applied feedback, full comparison, bounded revision and manual-task recovery | Check actual text; reuse evidence without rebinding old approval; do not manufacture history or force profile upgrades |
| 4 | Construct generic semantic diagnostics and a three-mode comparison | Distinguish structure from semantics; retain scope and mechanisms; permit withdrawn criticism and no-change; mark unexecuted evaluations clearly |
| 5 | Review changes, run affected contracts and synchronize plugin | Preserve existing APIs; no parallel ledger, required new fields or semantic acceptance gates; report observed results and limits |

## Decisions

Use stable existing requirement IDs and evidenced finding dispositions. Accepted edits remain open until checked. Explicitly select the main file rather than guessing from timestamps. Current input/review binding stays in force. No automatic semantic approval or background monitoring is added.

Project instructions cover resume, substantive change and delivery only, through a short reusable reference. Methods-only use remains valid; absence of CLI/MCP calls is not itself a failure.

Code tests establish API, persistence and binding behavior, not quality gains. Compare ordinary reasoning, methods-only use and methods plus tools under the same model, material and initial conditions. Preserve first outputs and distinguish requirement omissions, fact errors, applied edits, unnecessary rework and returned usage from file or PASS counts. Future independent tasks not used for prompt development can test generalization; public development cases are not held-out evidence.

## Exclusions

No private case copies, feedback platform, large banned-word list, fixed reviewer panel, forced historical normalization, copied approval or telemetry-based delivery gates.

## Execution

Baseline: 1.3.3 at a clean worktree. All five stages of source changes, documentation and local validation were executed; the plugin copy was synchronized without a version bump or release. See the [validation note](task-continuity-validation.md) and separate [review record](task-continuity-review.md). The Chinese plan maps each problem to its implementation, existing contract or documentation treatment.

## Why continuity breaks and what project instructions can do

Method instructions do not intercept direct file edits. During repeated drafting, an agent may update the manuscript and conversation while leaving a readable but stale specification. A later chapter save can be mistaken for the main artifact. An outdated entry can also prevent existing capabilities from being used. These are different failure modes, not evidence that every validator failed.

This change connects substantive updates to the existing save operation and exposes current references at resume. A short project instruction covers resume, substantive change and delivery; the author checks affected requirements against the actual text. Code prevents a registered main from using the wrong historical delivery and rejects invalid or partially written batches. It cannot certify understanding, applied feedback or host compliance. Those remain execution responsibilities.

Installed-entry upgrades, private historical-task migration and longitudinal held-out trials are outside this round. Recovery instructions preserve originals and do not silently upgrade user environments. The generic diagnostic catalog was structurally validated; actual model runs covered three short tasks and do not establish long-task benefits.
