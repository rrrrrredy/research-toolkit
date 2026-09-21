# 参考写作样例

[English](README.md) | [简体中文](README.zh-CN.md)

这些易读示例帮助说明评审标准，区分机械符合与有用研究。它们不是标准答案，不应作为模型训练数据，也不证明示例已可发表或事实仍然有效。

`high_quality.md` 是编辑示例标签，不是已验证质量分数。AI Agent 市场示例基于缺少日期和原始出处的历史摘要，不能当作当前市场报告或事实答案；见[来源核定](../../docs/evaluation-data-audit.zh-CN.md)。合成例子仍是虚构，不可作为留出测试任务。

## 示例

- [AI Agent 市场正文](ai_agent_market_landscape_zh/high_quality.md)：论点驱动的中文示例；[与模板式基线比较](ai_agent_market_landscape_zh/baseline_vs_anchor.md)。
- [八家虚构公司的长周期报告](model_company_pipeline_long_horizon_zh/high_quality.md)：补充要求、公司机制与交付限制；[范围偏移、遗漏与过早完成的比较](model_company_pipeline_long_horizon_zh/baseline_vs_anchor.md)。
- [比喻堆叠段落](figurative_load_zh/baseline.md)、[相同事实的明确类比](figurative_load_zh/high_quality.md)及[读者审阅比较](figurative_load_zh/baseline_vs_anchor.md)：用于解释表达负担，不设比喻比例阈值。
- [来源指令边界正文](source_instruction_boundary_zh/high_quality.md)：正例夹具中的虚构报告，数字不是现实市场证据。

## 使用方式

选择最相关的例子解释具体标准，对照实际任务、输出和来源，保留合理不确定性与任务差异。LLM 发现和分歧独立于机械结果记录。只有发现有证据的缺口时才修改工具箱；能机械检查的行为才加入夹具，不把每个风格偏好变成规则或新一轮评审。使用这些例子没有人工评审前提。
