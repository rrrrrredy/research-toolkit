# Taste Anchors

[English](README.md) | [简体中文](README.zh-CN.md)

Taste anchors are human-readable examples used to calibrate the evaluation loop. They are not gold answers and should not be treated as model training data. They illustrate criteria for distinguishing mechanical conformance from useful research; they do not establish that an example is publishable or factually current.

The filename `high_quality.md` is an editorial example label, not a validated quality score. In particular, the AI Agent landscape sample uses undated historical summaries with unavailable original provenance; it is not a current market report or factual answer key. See the [source-data audit](../../docs/evaluation-data-audit.md). Synthetic anchors remain fictional even when their structure is useful. Do not use these development examples as held-out test tasks.

## Anchors

- [`ai_agent_market_landscape_zh/high_quality.md`](./ai_agent_market_landscape_zh/high_quality.md): a reader-facing, thesis-led Chinese sample for the AI Agent market landscape case.
- [`ai_agent_market_landscape_zh/baseline_vs_anchor.md`](./ai_agent_market_landscape_zh/baseline_vs_anchor.md): comparison between a template-compliant baseline and the taste anchor.
- [`model_company_pipeline_long_horizon_zh/high_quality.md`](./model_company_pipeline_long_horizon_zh/high_quality.md): a fictional eight-company pipeline report that preserves late requirements, company-specific mechanisms, and delivery limitations.
- [`model_company_pipeline_long_horizon_zh/baseline_vs_anchor.md`](./model_company_pipeline_long_horizon_zh/baseline_vs_anchor.md): comparison focused on primary-object drift, lost corrections, process sprawl, and false completion.
- [`figurative_load_zh/baseline.md`](./figurative_load_zh/baseline.md): a synthetic Chinese paragraph that preserves the factual payload but stacks unrelated metaphors.
- [`figurative_load_zh/high_quality.md`](./figurative_load_zh/high_quality.md): the same facts and conclusion with one explicit, useful analogy and a recoverable literal interpretation.
- [`figurative_load_zh/baseline_vs_anchor.md`](./figurative_load_zh/baseline_vs_anchor.md): a focused reader-review comparison for figurative load; it is an editorial anchor, not a metaphor-rate threshold.
- [`source_instruction_boundary_zh/high_quality.md`](./source_instruction_boundary_zh/high_quality.md): a fictional report used by the source-boundary positive fixture; its figures are not real market evidence.

## How To Use

1. Use the nearest relevant anchor to explain a specific review criterion.
2. Compare the actual task, output and sources; retain valid uncertainty and task-specific differences.
3. Record LLM review findings and disagreements separately from mechanical checks.
4. Change the Toolkit only for an evidenced gap. Add a deterministic fixture only when the behavior can be checked mechanically; do not turn every stylistic preference into a rule or another review round.

## 中文说明

Taste anchor 用来校准“像不像一篇真正的研究报告”。它不是标准答案，也不是训练集。自动 runner 检查配置中的流程和结构信号；taste anchor 帮助 LLM 评审解释主张、机制、综合判断和读者体验的具体差别，不构成人工评审前提。文件名 `high_quality.md` 是示例标签，不是经过验证的质量分数。
