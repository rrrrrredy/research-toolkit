# Toolkit 专用七题：真实报告复验

[English](README.md) | [简体中文](README.zh-CN.md)

七道原始 Toolkit 研究题均已使用完整题面来源实际运行。每题由全新上下文中的 Astra 写作，再由另一个全新 Astra 上下文评审。程序按完整 Markdown 正文的非空白 Unicode 字符计数；评审收到相同题目、完整来源和出处，不收到作者身份或私有来源使用笔记。直接复用原题。

**实际调用 15 次：**七次写作、七次首评、一次修改稿复评。六份首稿篇幅合格且首评通过；管线报告首稿为 6,020 字符，超过 6,000 上限。维护者删除一句重复总结，共 33 字符，修订稿为 5,987 字符并经 Astra 复评通过。原首稿与负评保留，没有对未改稿件反复抽样求通过。

| 题目 | 原定范围 | 首稿字符数 | 首评 | 选用稿件及范围 |
|---|---:|---:|---|---|
| AI Agent 市场格局 | 3,000–5,000 | 4,437 | 通过 | [首稿](authors/ai_agent_market_landscape_zh/initial/report.md)，题面来源内的任务验收通过 |
| AI 视频投资备忘录 | 2,500–4,500 | 3,826 | 通过 | [首稿](authors/ai_video_generation_investment_memo_zh/initial/report.md)，题面来源内的任务验收通过 |
| 八家公司研发管线 | 3,500–6,000 | 6,020 | 需压缩 | [修订稿 5,987](authors/model_company_pipeline_long_horizon_zh/repair-1/report.md)，仅作阶段稿 |
| 模型价格战 | 2,500–4,500 | 3,958 | 通过 | [首稿](authors/model_price_war_competitive_analysis_zh/initial/report.md)，题面来源内的任务验收通过 |
| AI 月度综合 | 2,500–4,500 | 4,020 | 通过 | [首稿](authors/monthly_observation_synthesis_zh/initial/report.md)，题面来源内的任务验收通过 |
| 推理模型竞争 | 2,500–4,500 | 3,977 | 通过 | [首稿](authors/reasoning_model_competition_zh/initial/report.md)，题面来源内的任务验收通过 |
| 来源指令边界 | 900–1,500 | 1,295 | 通过 | [首稿](authors/source_instruction_boundary_zh/initial/report.md)，题面来源内的任务验收通过 |

## 管线题的交付范围

管线题累计要求包含具名模型发布节点、原始技术报告及多渠道核验（R04/R05）。本次输入提供八份匿名公司档案，这些档案本身不完成上述原文研究。修订正文及[交付说明](authors/model_company_pipeline_long_horizon_zh/repair-1/delivery_message.md)保留未闭环要求；[实际复评](judges/model_company_pipeline_long_horizon_zh/repair-1/parsed.json)明确记录 `full_task_complete: false`、`stage_delivery_appropriate: true`。因此，七份正文在各自声明范围内获认可，其中六份作为题面来源内的报告任务验收，一份只作为阶段稿；不把管线题标成完整研究任务完成，也不豁免要求。

本轮按全部给定要求生成完整正文。13 轮历史要求作为同一份要求记录提供，没有运行实时 13 轮对话或 agent 文件／MCP 操作测试；软件检查另列。本轮也没有重跑四家模型矩阵或比较有无 Toolkit。题面中的虚构公司事实、来源日期和出处按原样记录，不改变任务身份或实际调用的真实性。

## 证据与核验

`plan.json`、`plan-hash.json`保存调用前的输入、指令、来源、设置及执行脚本哈希。`authors/`、`judges/`包含原始请求、CLI 原始返回、执行信息、解析结果与稿件版本绑定；`summary.json`把每份选用正文关联到实际评审。`edit.json`记录管线稿的精确删除内容；修稿复评另检查实际阶段交付说明，具体指令保存在 `request.json`。

CLI 请求模型为 `gpt-6-astra`，返回用量和执行事件，不认证服务端实际模型 ID。累计记录输入 283,614 token、输出 27,966 token，推理用量另按执行返回记录。公开副本仅把诊断事件中的本地账户名替换为 `<LOCAL_USER>`，文件清单见 `summary.json`。重复便捷文件 `packet.json`、`content.txt`未再复制，完整相同输入／输出已在请求、事件和解析结果中保留；本地原件不改。driver 文件是执行快照，归档不会触发新调用。

在仓库根目录执行：

```bash
python evals/diagnostics/2026-10-13-dedicated-seven/verify.py
```

只读核验覆盖文件及哈希、冻结计划、作者与评审来源完全一致、模型实际返回、计数、首评、精确修改、当前稿件与评审绑定、调用／用量合计及阶段范围，不调用模型。本记录补齐此前笼统完成声明未能证明的七题实际模型覆盖；PR #38 当时只修正了提示／配置并做离线回归。
