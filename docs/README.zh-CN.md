# 文档

[English](README.md) · [简体中文](README.zh-CN.md) · [Research Toolkit](../README.zh-CN.md)

## 使用 Research Toolkit

- [开始研究](quickstart.zh-CN.md)：一套完整研究入口，按任务展开长文、深度分析、修订与更新。

- [使用与接入](usage-modes.zh-CN.md)：仓库、文件与文本输入，可选的 Skill、插件、MCP，以及审阅配置。
- [在你的 Agent 中使用](../agents/README.zh-CN.md)：通用输入方式、纯聊天边界与各工具的接入。
- [更新安装](installation-versioning.zh-CN.md)：选择和替换预期的软件包副本。

## 按当前工作找方法

这些是同一项研究中按需使用的入口，不是启动时要读完的文档清单。

| 正在做什么 | 直接读哪里 |
| --- | --- |
| 理解请求、确定需要展开的问题 | [研究需求与深度规划](../references/research-workflow.zh-CN.md)；首次使用可看[研究指南](research-guide.zh-CN.md)。 |
| 阅读材料、比较和解释 | [来源与主张](../references/research-standard.zh-CN.md#8-来源与主张) · [按问题选择分析方法](../references/optional-analysis-lenses.zh-CN.md) |
| 委派独立研究、接收可用成果 | [实质研究与交接](../references/subagents-and-review-loop.zh-CN.md#实质研究与交接) · [共同上下文与实际调用](usage-modes.zh-CN.md#研究委派与成果交接) |
| 写出完整报告、统稿与修订 | [写作规范](../references/writing-style.zh-CN.md) · [组稿](../references/research-workflow.zh-CN.md#9-组稿) |
| 接续任务或落实新要求 | [任务接续](../references/task-continuity.zh-CN.md) · [当前主稿与需求变更](usage-modes.zh-CN.md#当前主稿与需求变更) |
| 完成独立审阅、审计与验收 | [审阅方法](../references/subagents-and-review-loop.zh-CN.md#按视角分工) · [完成条件](../references/quality-gates.zh-CN.md)；工具记录细节见下方“审阅与评测”。 |

遇到具体问题时再查[常见研究问题](../references/gotchas.zh-CN.md)，无需另起一套流程。

## 报告与案例

- [已有研究报告的实际更新](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/index.zh-CN.html): 从旧稿到来源核对、具体修订与原始证据，保留实验限制。

- [国内办公 Agent 调研档案](case-study/office-agents/README.md)：初稿、定稿、来源与主张记录，以及修改取舍。
- [完整报告](case-study/report.zh-CN.md)：2026 年 9 月报告的中文读者版。
- [案例说明](case-study/README.zh-CN.md)：表达、结构、产品关系与模型信息的修改。

## 审阅与评测

- [审阅完成条件](review-completion.zh-CN.md)：完整输入、版本绑定、有效回复与失败恢复。
- [交付检查](delivery-verification.zh-CN.md)：当前稿件、未解决要求与完成条件。
- [未达标与修正](failure-handling.zh-CN.md)：来源核对、稿件预检、PR 验收与停止规则。
- [报告评测标准](report-evaluation-standard.zh-CN.md)：区分稿件质量、交付状态和工具效果研究。
- [必要缺陷标签](necessary-defects.zh-CN.md)：稳定类别、有证据的处置和版本化诊断索引。
- [评测集](../evals/README.zh-CN.md)：题目、对照样例、回归样例、诊断与离线检查。
- [评测现状](evaluation-status.zh-CN.md)与[评测计划](evaluation-roadmap.zh-CN.md)：已有证据与待完成工作。
- [评测数据审计](evaluation-data-audit.zh-CN.md)：公开数据的组成与证据范围。
- [来源提取](source-extraction.zh-CN.md)：来源记录与原文留存。

## 开发

目录按内容用途保留，研究职责通过共用实现连接：

| 位置 | 维护内容 |
| --- | --- |
| `SKILL.md` 与 `references/` | 统一入口、研究规范及按需方法。 |
| `scripts/` | CLI／MCP 共用逻辑；`task_context.py` 组织工作输入，`research_records.py` 保存记录与成果，`research_workflow.py` 连接研究、评审与交付操作。 |
| `docs/` 与 `agents/` | 使用说明、网站与宿主接入；宿主负责 Agent 的运行和消息。 |
| `plugins/research-toolkit/` | 从共享源文件生成的安装包内容，不单独维护另一套方法。 |
| `examples/` 与 `evals/` | 调用示例、实际研究记录及相应检查；历史证据保持原样。 |

- [DSH 接入维护](dsh-adapter-validation.zh-CN.md)：已有加载检查，与普通研究分开。
- [网站发现与维护（英文）](site-maintenance.md)：静态构建、静态页面检查、部署后验证、数据口径与站长接入步骤。

[历史改进计划](improvement-plan.zh-CN.md)：早期优先级、研究设计及当时结果。

[贡献指南](../CONTRIBUTING.zh-CN.md) · [更新记录](../CHANGELOG.zh-CN.md) · [插件包](../plugins/research-toolkit/README.zh-CN.md) · [脚本](../scripts/) · [MIT 许可](../LICENSE)
