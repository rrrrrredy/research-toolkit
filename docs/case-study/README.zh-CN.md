# 一份报告，三处修改

这份 AI 客服历史报告保留了原稿、审阅意见和修订稿。以下展示实际修改，并不构成有无工具箱的对照实验，也不能证明工具普遍提升报告质量。

[Interactive case](https://rrrrrredy.github.io/research-toolkit/?lang=zh#case) · [Full English report](report.en.md) · [中文原文](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md) · [Review](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/reviews/astra-initial.json)

## 1. 把判断放到前面

读者先知道，下一步该做什么。

**原稿**

> AI 客服已在高频、规则明确的业务中进入生产，企业下一阶段应投资于可持续解决问题的能力。

**修订稿**

> 未来一个季度，AI 客服预算应优先投向两类工作：一类是订单查询、票据获取、订阅变更等规则明确、可以核对业务结果的高频请求；另一类是由人工作最终决定的检索、回复建议和工单整理。

原稿已经有判断。修订稿进一步把投入方向和适用边界放到开篇，让读者更快找到行动起点。

好的结论还要回答：先做什么，适用于谁，什么情况下需要停下来。

*开篇原文节选。完整段落及相邻限制说明见原文链接。*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L1) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L7)

## 2. 把资料变成分析

平均有收益，谁会例外？

**原稿**

> 2025 年《经济学季刊》的研究利用 5,172 名客服人员的分阶段采用数据，发现 AI 辅助使每小时解决问题数平均提高约 15%，较少经验人员受益更大。

**修订稿**

> 低经验、低技能员工获益更明显，经验和技能最高的员工速度提升较小，质量还略有下降。因此，“辅助人工”值得作为投入路线，但应按员工经验与任务难度检查收益，不能拿平均值要求所有员工采用相同方式。

原稿已经提到收益差异。修订稿补入高技能员工的负面结果，并区分总样本与使用 AI 后的观察样本，让差异真正影响建议。

把结果、例外和选择联系起来，分析才能超出对资料的转述。

*历史报告原文节选；后文摘录合并了同一段中的两句话。此处不代表重新核验研究结果。*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L49) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L75)

## 3. 让结论守住证据边界

有引用，还要看它能证明什么。

**原稿**

> 按 Zendesk 发布的客户案例，到 2025 年第二季度，其自动解决率达到 51.5%，AI 客服满意度从 34% 升至 70%。

**修订稿**

> SeatGeek 的客户案例提供了一种具体的落地路径：先处理“我的票在哪里”，从可认证的已登录用户开始，再通过实时接口读取订单。
> 
> 其历史数字与证据限制列在文末来源说明，不进入三家效果排名。

原稿已经注明客户自报和没有对照组。审阅指出，原始页面无法直接复核的限制还不够醒目；修订稿把历史数字移到来源说明，正文收窄到部署路径。

引用的价值，取决于它能支撑多强的判断。

*报告原文节选，省略同一段中的中间一句。原始页面无法直接复核的限制保留在完整报告中。*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L27) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L45)

## 复制这份研究请求

请求改编自案例任务。新的研究可能得出不同报告；它用于发起研究，并非复现历史结果的承诺。

```text
本次研究请使用 Research Toolkit：
https://github.com/rrrrrredy/research-toolkit

研究 AI 客服如何从试点进入生产。
比较 Intercom、Zendesk、Salesforce 的产品机制、采用证据、
实施条件和失败风险。面向企业 AI 产品负责人写作，
给出未来一个季度值得采取的行动和可观察的判断指标。

以 [日期] 为信息截止日。重要判断附来源，区分公司说法与
独立证据，并说明哪些反证可能改变结论。

先读 SKILL.md，澄清缺失的研究需求，确认提纲后再搜集资料。
```
