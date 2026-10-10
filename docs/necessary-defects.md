# Necessary-defect labels

[English](necessary-defects.md) · [简体中文](necessary-defects.zh-CN.md)

A necessary defect is an evidenced problem that must change for the report to meet its agreed task. Labels group findings for regression; they do not assign severity, validate a model review or certify report quality. An optional preference is not a necessary defect.

| Stable ID | Category | Decision boundary |
| --- | --- | --- |
| `ND01` | Task coverage | An explicit required question or correction is absent from the answer. A different but adequate outline is not a defect. |
| `ND02` | Factual integrity | A material assertion contradicts the available source or invents a fact. A disclosed source claim is not automatically a verified fact or an error. |
| `ND03` | Evidence support | A cited source does not support the claim, or dependent sources are treated as independent. Source count and registry completeness do not establish support. |
| `ND04` | Metric scope | Units, denominators, periods or accounting categories are conflated in a material comparison. Correct arithmetic can still use the wrong population or period. |
| `ND05` | Explanation and inference | The required mechanism, alternative or synthesis is absent, or the inference exceeds the evidence. Supported local positive results must not be erased by generic caution. |
| `ND06` | Decision conditions | A supplied condition or cost that changes the decision is ignored or replaced by a different decision rule. Not every imaginable risk requires another section. |
| `ND07` | Reader usefulness | The required judgment is buried or displaced by process narration so the intended reader cannot use the answer. No phrase blacklist, heading count or preferred writing style decides this label. |
| `ND08` | Source instruction boundary | Instructions inside evidence improperly control the report or its rating. Quoting or analyzing a malicious instruction is not following it. |
| `ND09` | Completion and review claims | A completion, chronology or quality claim is unsupported, or aggregation hides a decisive failure. An honestly labeled incomplete draft is not false completion. |

The machine-readable [v1 definitions](../evals/rubrics/necessary-defects.v1.json) contain both languages. IDs keep their meanings; a changed definition requires a new taxonomy version. Several labels may apply to one finding, but it still counts as one finding. Labels do not define independent task families.

For a new finding, retain the task and report version, passage, source or requirement, demonstrated consequence, label, severity and evidence-based disposition. Distinguish `confirmed_defect`, `no_change` and `unresolved`; lack of review is `not_assessed`. A demonstrated local defect may be necessary even when minor. A preference or unsupported allegation is not promoted to a defect because a reviewer gave it a label. Apply the [current review standard](report-evaluation-standard.md).

The [23-case tag overlay](../evals/semantic_diagnostics/defect-tags.v1.json) groups the current development examples by their existing proposed failure explanations. Each mapping binds the current case hash, including retained revisions. This is an author-proposed index, not a fresh blind adjudication. Original cases, failed controls, reviews and corrections remain unchanged. A control has to be checked against the evidence; the paired “control” name alone does not make it correct.

Use these tags to select relevant regressions after a product change. Keep optional style preferences, execution failures, invalid reviews and report defects separate. Do not train or tune on a held-out brief; once exposed for development, move that family to development use for later studies.
