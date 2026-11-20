# How a long GPAI report reached delivery

[English](README.md) · [简体中文](README.zh-CN.md)

The research question asked how a Chinese model provider should sequence its obligations when entering the EU in 2026–27. The Chinese report uses materials through 18 November 2026. These records cover the 19 November Codex run on the DeepSeek draft.

| What happened | Inspect the record |
| --- | --- |
| The task received the initial manuscript and its length and source requirements | [Original draft](reports/initial.md) · [CLI replay of task creation and blocked delivery](replay.json) |
| Four content reviews returned 39 findings. The independent auditor issued nine individual and eight grouped decisions and required revision | [Evidence review](live/originals/evidence_and_reasoning.json) · [Decisions and reasons](live/originals/audit.json) · [All originals and manuscript bindings](records.json) |
| An independent agent rechecked the revised manuscript. The delivery receipt binds the final 4,000-nonwhitespace-character report | [Final review](live/originals/acceptance.json) · [Final report](reports/final.md) · [Actual completion response](live/finish.json) · [Original receipt](live/receipt.json) |

Line 19 of the original treated the Union representative rule as generally applicable. The audit checked eligibility. Line 23 of the final report includes the qualifying open-source exemption. [Original passage](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/v3-review/reports/initial.md#L19) · [Audit](live/originals/audit.json) · [Revised passage](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/v3-review/reports/final.md#L23). [Two retained review summaries](live/review-summary.json) show a recorded submission both while delivery remained blocked and after the independent final check passed.

**Two available slots.** The host ran with a concurrency cap of two. The [native event extract](live/turn-events.json) preserves starts, completions and timestamps by invocation. The observed peak in each invocation was at most two. Three interrupted logs lack a total of four corresponding completion events. Read the counts within each host process. The run included restarts and multiple revisions.

**A separate disagreement control.** Four seeded reviews of the same manuscript each contained one genuine defect and one incorrect objection. A fresh auditor checked the source, upheld the four observations about the Article 54(6) exemption in one decision and dismissed all four date objections in another. This control remained open for revision. [Seeded review](control/originals/evidence_and_reasoning.json) · [Two decisions and their evidence](control/originals/audit.json)

The public subset contains the manuscripts, responses, receipt and turn events supporting these observations. Response hashes use the original tool's LF normalization. Two local filenames in the first live audit were replaced with the public manuscript path. The manifest identifies the original and published hashes. The CLI replay is labeled separately. A controlled comparison of whole-task quality, cost and time remains open.
