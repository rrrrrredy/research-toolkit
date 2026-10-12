# 研究设计经验

[English](postmortem-lessons.md) | [简体中文](postmortem-lessons.zh-CN.md)

本页归纳常见研究失误及应对方式，不代表对工具箱效果的量化测定。

## 任务连续性与证据

- 当前状态应简明，足以恢复目标、未决问题和下一步。
- 区分来源、主张和不确定性，让重要判断可追溯、可质疑。
- 需要深入分析时，按边界明确的单元写作。
- 对评审发现给出有证据的处置：委托报告中的已确认缺陷应修正，不采纳无依据或可选建议时说明理由；评测样本的缺陷保留，用于改进工具箱。
- 反证会改变结论时，将其纳入论证。

## 常见失误

- 将文章任务扩成系统设计。
- 在正文暴露后台编号、日志或工作过程。
- 将某个题目的结构当作通用方法。
- 评审者重复作者假设，没有核查证据。
- 将登记表规模或文件检查通过当作内容深度的证明。
- 完成局部里程碑后宣称整个任务完成。
- 跨轮次丢失重要补充要求。
- 增加无法改善成果或状态准确性的管理机制。

## 面向读者的质量

报告需要清楚的论点、相关证据、与问题相称的细节、明确的不确定性、有用的参考资料和易读的分析。预期深度应在写作前确定；验收时检查实际正文，不能依赖文件数量或状态标签。

## 十月 Lite 试点评测的教训

以下保留样本用于解释方法修改的依据，不证明修改已经有效。它们来自不同采集阶段，不能合并计算新的胜率。

- [DeepSeek 银行简报，原始 pair 03](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/runs/deepseek/coordinator/author/pair-03/with_toolkit/parsed.json)：报告含标题按空白分词为 913 词，超过需求的 600–800 词。交付前应统计实际篇幅。
- [Kimi 银行简报，格式补充 pair 05 的报告 B](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/format-supplement/kimi/judge-inputs/pair-05.json)：开头声称失败率高，但投诉个例不足以证明发生率；同时把预期损害写成已发生结果，并提出没有理由支撑的转人工比例上限。应保留来源范围和语气，解释决策条件的依据并检查激励后果。
- [DeepSeek 内存安全简报，完成补充 pair 01](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/completion-supplement/deepseek/authors/pair-01/with_toolkit/report.md)：一处转述颠倒外部依赖与开源软件的关系，还将缺失外部报告视为无法评估厂商自身依赖风险的理由。应核对关系方向，区分缺失外部证据与决策者可以取得的内部证据。

对应方法见[来源与主张](research-standard.zh-CN.md#8-来源与主张)、[写作风格](writing-style.zh-CN.md#篇幅与决策用途)和 [Lite 指南](lite-workflow.zh-CN.md)。效果须由另行冻结的对照评测验证；现有试点的输入、输出和评判保持原样。

## 交付边界

研究记录支持追溯，最终报告向读者呈现论证与有用证据，两者不能互相替代。

当前要求、全文评审、已接受的限制、文件哈希和交付声明必须一致。局部成果可以按准确范围交付。评测是否完成取决于冻结的评测要求和结果保留情况，无须把每份受评报告修好。
