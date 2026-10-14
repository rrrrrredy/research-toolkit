# 完整研究结果前后比较：未观察到稳定的总体提升

[English](README.md) · [简体中文](README.zh-CN.md)

按用户确认，整改前取 2026 年 10 月 12 日实际使用的提交 `422b437169e609b94c16087c65fdd68a83ad0ca4`，整改后取 v1.0.0 的 `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`。本次用两版方法重新生成完整研究报告，比较同一资料与资源条件下的输出；没有把旧短稿与新增长稿混作配对。

首轮于 10 月 13 日执行，修复与复验于 10 月 14 日完成。七道原有真实独立任务加三道新题，共 **10 题、20 篇完整报告、20 次独立上下文 Astra 盲评**。作者也使用 Astra，先分析，再用两至三次调用分段写作。首轮共 62 次作者阶段调用和 20 次评审调用，全部完成。

## 首轮结果

| 指标 | 整改前 | v1.0.0 |
|---|---:|---:|
| 首评均分（100 分制） | 100 | 99.5 |
| 七道原题均分 | 100 | 99.29 |
| 三道新题均分 | 100 | 100 |
| 首评偏好 | 2 题 | 4 题 |
| 交换顺序后的偏好 | 3 题 | 3 题 |
| Astra 首评判为通过 | 10/10 | 10/10 |
| 篇幅符合原任务 | 10/10 | 10/10 |

首评与交换评审各有 4 题平手。配对平均差为 **−0.5 分**，中位差为 0；7 题的偏好在交换后保持一致，3 题变化。稳定结果为新版胜 2 题、旧版胜 2 题、3 题平手，另 3 题对顺序敏感。不能从首评“4 比 2”推导总体提升，更不能把评分变化写成质量提升百分比。

评分采用仓库现行五维 0–4 标准，等权换算为 100 分。高分出现明显上限效应；它是本轮 Astra 的评价，不是事实正确率。**随后检查导出文本另发现新版一篇的引用缺陷，初评两个方向均漏检**，见下文。原始通过判断与得分完整保留。

## 逐题完整报告与原始评审

分数链接直接打开对应完整报告；每行是一道任务，交换顺序不增加任务数。

| 研究题目 | 旧版 | 新版 | 首评 / 交换偏好 | 原始评审 |
|---|---:|---:|---|---|
| AI Agent 市场格局行业报告 | [100](authors/ai_agent_market_landscape_zh/before/report.md) | [100](authors/ai_agent_market_landscape_zh/after/report.md) | 新版 / 旧版 | [首评](reviews/ai_agent_market_landscape_zh/primary/parsed.json) · [交换](reviews/ai_agent_market_landscape_zh/swap/parsed.json) |
| AI 视频生成市场投资 Memo | [100](authors/ai_video_generation_investment_memo_zh/before/report.md) | [100](authors/ai_video_generation_investment_memo_zh/after/report.md) | 新版 / 新版 | [首评](reviews/ai_video_generation_investment_memo_zh/primary/parsed.json) · [交换](reviews/ai_video_generation_investment_memo_zh/swap/parsed.json) |
| 八家模型公司的研发管线与组织协作研究 | [100](authors/model_company_pipeline_long_horizon_zh/before/report.md) | [100](authors/model_company_pipeline_long_horizon_zh/after/report.md) | 平手 / 新版 | [首评](reviews/model_company_pipeline_long_horizon_zh/primary/parsed.json) · [交换](reviews/model_company_pipeline_long_horizon_zh/swap/parsed.json) |
| 大模型降价潮竞品分析 | [100](authors/model_price_war_competitive_analysis_zh/before/report.md) | [100](authors/model_price_war_competitive_analysis_zh/after/report.md) | 新版 / 平手 | [首评](reviews/model_price_war_competitive_analysis_zh/primary/parsed.json) · [交换](reviews/model_price_war_competitive_analysis_zh/swap/parsed.json) |
| AI 行业月度观察综合 | [100](authors/monthly_observation_synthesis_zh/before/report.md) | [100](authors/monthly_observation_synthesis_zh/after/report.md) | 平手 / 平手 | [首评](reviews/monthly_observation_synthesis_zh/primary/parsed.json) · [交换](reviews/monthly_observation_synthesis_zh/swap/parsed.json) |
| Reasoning Model 竞争技术路线研究 | [100](authors/reasoning_model_competition_zh/before/report.md) | [95](authors/reasoning_model_competition_zh/after/report.md) | 旧版 / 旧版 | [首评](reviews/reasoning_model_competition_zh/primary/parsed.json) · [交换](reviews/reasoning_model_competition_zh/swap/parsed.json) |
| 外部来源指令边界测试 | [100](authors/source_instruction_boundary_zh/before/report.md) | [100](authors/source_instruction_boundary_zh/after/report.md) | 平手 / 平手 | [首评](reviews/source_instruction_boundary_zh/primary/parsed.json) · [交换](reviews/source_instruction_boundary_zh/swap/parsed.json) |
| 中文企业知识助手：RAG、长上下文还是混合路线？ | [100](authors/rag_long_context_decision_zh/before/report.md) | [100](authors/rag_long_context_decision_zh/after/report.md) | 新版 / 新版 | [首评](reviews/rag_long_context_decision_zh/primary/parsed.json) · [交换](reviews/rag_long_context_decision_zh/swap/parsed.json) |
| 推理算力怎样分配才值得？ | [100](authors/test_time_compute_decision_zh/before/report.md) | [100](authors/test_time_compute_decision_zh/after/report.md) | 平手 / 平手 | [首评](reviews/test_time_compute_decision_zh/primary/parsed.json) · [交换](reviews/test_time_compute_decision_zh/swap/parsed.json) |
| 编程智能体的排行榜能支持什么采购判断？ | [100](authors/coding_benchmark_decision_zh/before/report.md) | [100](authors/coding_benchmark_decision_zh/after/report.md) | 旧版 / 旧版 | [首评](reviews/coding_benchmark_decision_zh/primary/parsed.json) · [交换](reviews/coding_benchmark_decision_zh/swap/parsed.json) |

新版稳定胜出的题目是 AI 视频投资与 RAG 选型；旧版稳定胜出的是推理模型竞争与编程评测解读。推理题的差距在于 OpenAI 的信息获取、网页理解和引用核查没有充分进入三方比较；编程题的差距在于旧版的试点起点、顺序和调整条件更具体。所有判断均可对照表中原文及评审理由。

## 问题、修改与针对性复验

新版编程评测原稿含 6 个私有浏览引用标记，在独立 Markdown 中无法定位来源。这是 1 个原因对应的 6 处引用问题，标签为 ND03/ND07。首轮评审没有发现它；后续明确交付格式的匿名复评确认了该问题。初评结果不因此被删除或重写。

已同步修改中英文研究工作流、写作风格、评审说明及插件副本：比较时使用已有的区分性证据；任务要求执行计划时给出可着手的范围、角色、假设和决策条件；导出引用对应实际标题和网址，并在交付格式中核查。没有新增外部评审者、材料门槛、固定面板或软件接口。

两篇当前稿完成修订，Astra 在独立上下文中匿名比较原稿与修改稿，两次都偏好修改稿。推理稿通过；编程稿仍需补入现成的仓库分层成绩，已核对 Scale 原文、补入并限定为历史结果，再由一个新 Astra 上下文检查当前全文，现已通过。推理稿一次 4,557 字符的超长修订稿及编程稿一次未通过的复评均保留，未重复评审未修改稿来获取有利结论。

- [Reasoning Model 竞争技术路线研究：当前修订稿](repairs/reasoning_model_competition_zh/report-final.md)，4494 个非空白字符；[Astra 当前稿评审](repairs/reasoning_model_competition_zh/review/parsed.json)通过。
- [编程智能体的排行榜能支持什么采购判断？：当前修订稿](repairs/coding_benchmark_decision_zh/report-final-v2.md)，3758 个非空白字符；[Astra 当前稿评审](repairs/coding_benchmark_decision_zh/review-2/parsed.json)通过。

修复阶段新增 2 次作者调用、2 次匿名比较及 1 次修改稿复查，共 5 次；与首轮合计 **87 次实际模型调用**。后续评审对同一原稿的分数和缺陷判断也有变化，原样保留，不用于重新估计首轮增益。修订稿另计，不能替换首轮均分 −0.5 分或作为版本效果增益。[具体问题与处置](source-adjudication.json) · [方法修改](method-change.json) · [修复结果与完整记录](repair-summary.json)。

## 比较范围与材料

本次比较六份真实方法文件的两个版本，作者模型、资料、阶段安排和输出预算保持一致。评审只收到任务、同一来源正文、完整匿名报告和程序字数；没有作者笔记、方法文本、版本映射或其他评审意见。两种顺序使用新上下文，全部首轮评审结束后统一解盲。引用格式的后续澄清只用于明示的修复复验，不能倒灌首轮分数。

七道原题保留其任务身份和来源性质。管线题使用已完成的具名公司续作材料，两版均获得同一原始论文／技术文档及多渠道材料；没有把匿名 A–H 反推为真实公司。三道新题分别研究 RAG 与长上下文、推理算力分配、编程智能体评测。来源正文和完整请求在本地保留；公开记录含原始网址、阅读摘录范围、来源性质及哈希，仓库自有来源记录完整公开，第三方全文不重复分发。

这回答的是 **Astra 在同一资料及分阶段执行条件下的完整报告质量**。共同的资料取得、分段执行及计数不能归功于某一个版本；本轮没有比较实时检索策略、MCP 状态流转、Lite 或此前四个作者模型。无需为本轮结论另加外部人员或新题门槛。

## 证据复核

[固定协议与任务](protocol.json)、[首次评审前的评分标准对齐](review-standard-amendment.json)、[原始统计](initial-summary.json)、[调用及输入绑定](calls.json)、[评审绑定](review-bindings.json)、[执行代码快照](code/)。原始 CLI 返回、完整报告、评审和失败修订均保留。Astra 为实际请求的模型；CLI 保留调用和用量记录，不提供独立的返回型号证明。首轮用量为 3,321,918 输入 token、143,962 输出 token；缓存字段是输入的子项，不另加总量。

运行 `python evals/studies/2026-10-13-before-after/verify.py` 可核对字节、原始回复提取、报告与评审对应及分数计算，模型调用数为 0。该程序不能代替内容评审。
