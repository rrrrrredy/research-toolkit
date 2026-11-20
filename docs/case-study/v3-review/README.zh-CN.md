# 一份通用 AI 模型报告怎样完成审阅、改稿和交付

[English](README.md) · [简体中文](README.zh-CN.md)

研究问题是中国模型公司在 2026–2027 年进入欧盟市场时，应按什么顺序落实通用模型义务。报告使用截至 2026-11-18 的资料。这里保留 11 月 19 日 Codex 处理 DeepSeek 原稿的可核查记录。

| 实际发生的事 | 打开记录 |
| --- | --- |
| 研究任务接收原稿，核对篇幅与来源要求 | [原稿](reports/initial.md) · [任务创建和交付拦截的 CLI 回放](replay.json) |
| 四份内容评审共提出 39 条意见。独立审计 Agent 做了 9 项单独裁定和 8 项合并裁定，要求修改 | [证据评审](live/originals/evidence_and_reasoning.json) · [逐项和合并裁定](live/originals/audit.json) · [所有原件与稿件绑定](records.json) |
| 改稿后由独立 Agent 复查。最终稿为 4,000 个非空白字符，交付回执绑定这份文件 | [复查意见](live/originals/acceptance.json) · [最终报告](reports/final.md) · [实际完成返回](live/finish.json) · [原始回执](live/receipt.json) |

原稿第 19 行把欧盟授权代表要求写成了通则。审计查了适用条件，成稿第 23 行补上合格开源且无系统性风险模型的豁免。[原稿段落](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/v3-review/reports/initial.md#L19) · [裁定](live/originals/audit.json) · [修订段落](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/v3-review/reports/final.md#L23)。[两份实际收件状态](live/review-summary.json)显示，同样是“已收件”，一份仍待处理，另一份已可交付。

**两名额的执行记录。** 宿主执行时并发上限为二。[原生事件摘录](live/turn-events.json)保留每次执行中的开始、完成和时间。各次执行可观察到的并发峰值均不超过二。三次中断的日志共缺少四条对应的结束事件，应按各次宿主进程读数。整个过程中发生过中断接续和多轮修订。

**单独验证四路相同意见。** 给同一份原稿配了四份预设评审，每份各有一条真实缺陷和一条错误质疑。新的独立审计 Agent 查原文后，对四条第 54(6) 条豁免意见作一次确认，对四条日期质疑作一次驳回。这个测试保留在待修改状态。[一份预设回复](control/originals/evidence_and_reasoning.json) · [两项裁定及依据](control/originals/audit.json)

本页公开用于核查以上结论的稿件、回复、回执及执行事件。回复哈希按原工具的 LF 换行口径计算。首轮真实审计中两处本机绝对文件名已改成公开稿相对路径，清单同时列出原始与公开哈希。命令回放有单独来源标记。完整流程的质量、成本和耗时收益仍需同条件对照。
