# 长研究 benchmark：2026 年 11 月基线

[English](README.md) · [简体中文](README.zh-CN.md)

本次沿当前 Research Toolkit 研究路径执行 **13 个独立问题、15 份报告任务**。主语言报告为 7 中文、6 英文；另以同题冻结材料独立完成微短剧英文与推理时计算中文报告，写作时不读取另一语言的答案。

数量来自实际覆盖：用户提出的 11 个方向，加上两道新的首页研究题，不设固定题数配额。修订、另一语言、另一模型或另一次运行都不增加独立问题数。

## 选题与研究目的

| 问题 | 主语言 | 正文需要解释什么 |
|---|---|---|
| 中国微短剧市场 | 中文，另有独立英文稿 | 增长口径、分发模式、平台竞争及产业链资金流 |
| 推理时计算 | 英文，另有独立中文稿 | 生成、选择、验证及 Agent 执行在明确推理条件下的取舍 |
| 模型 benchmark 比较 | 英文 | 覆盖、实际评测协议、可复现条件及任务选择含义 |
| Personal Agent | 中文 | 国内外路线怎样承接长期任务、记忆、授权与执行 |
| 可验证的自我改进 | 英文 | 反馈闭环、实际改动对象、选择机制、留出结果与泛化 |
| 端侧模型 | 英文 | 硬件、内存、持续任务与端云分工 |
| Token 经济学 | 英文 | 价格口径、工作负载、服务成本与价值分配 |
| 具身智能部署 | 中文 | 物理任务、模型与数据反馈、部署条件及经营经济 |
| 即时零售前置仓 | 中文 | 区域密度、履约、单仓经济、库存与现金 |
| AI 制药 | 英文 | AI 的具体贡献、实验、临床人群与合作条款 |
| 后训练人才 mapping | 中文 | 有日期的公开贡献、专长、任职与团队联系 |
| 新能源汽车电池 | 中文 | 材料体系、整包设计、使用条件、体系成本与量产 |
| 字节广告商业化 | 中文 | 推荐、竞价、转化归因、商家经济与增量增长 |

完整要求见[题目文件](../../cases/)。题目要求展开研究，不以固定章节数或孤立短答替代成稿；完整报告可以附执行摘要。

## 怎样执行下一次运行

1. 选定题目文件与 Toolkit 版本，在运行记录中保留原题面、选题范围和模型／运行配置。既有 runner 支持重复传入 `--case`；不指定时仍执行全部案例。
2. 按题目声明的材料模式执行。主语言题检索截止日之前的公开资料；冻结语言题只用同题已取得原件，不提供另一语言答案。保留实际访问失败、发布／版本日期、原始文件及哈希。改变截止日或材料集合时另记一个运行版本。
3. 沿既有研究入口规划、调研、展开实质研究单元并组稿。保留第一份完整稿、作者自检、单元成果和必要修订。独立上下文可以通过 Agent 工具或 API 执行。
4. 完成既有七项内容视角、适用领域专审、独立审计与单独最终验收。首次审阅输入包括原问题、完整当前稿和相关原件，不带其他首次意见或预期结论。修订回到负责该视角的上下文，保留其实际旧输入与旧判断。
5. 首次提交的发现与修订验收分别记录。每项必要修正对应正文位置、来源或要求；解释结果时沿用[五项研究质量维度](../../../docs/report-evaluation-standard.zh-CN.md)。总分可选，不替代具体发现。
6. 对实际完成的任务运行现有机械 evaluator。本批把 `reports/current.md` 登记为交付主稿，并向 evaluator 导出正文相同的 `final.md`。保留真实完成返回和原始失败，不生成占位状态。

执行数据说明实际发生了什么，研究质量及停止判断以要求、证据和当前完整产出为准。与旧版或原生 Agent 比较属于另外明确设计的研究；本次基线提供后续可持续使用的题目和实际结果。

## 材料与历史

[公开来源包](../../source_packs/)保存已识别的出版物、网址、实际阅读说明及原件哈希。本次完整下载原件保存在留存的执行文件中。元数据或访问失败记录不能代替来源正文；已有事实来源检查要求相应原件及匹配哈希。仅通过网页读取的局部记录如实列出读取范围。

原七道中文题逐字节保存在[退役目录](../../diagnostics/2026-11-09-retired-cases/README.md)。原五道短题保留在历史研究的冻结输入中，从活跃题目中移除。历史结果不改称当前题集的结果。

[初始题目文件](initial-case-definitions/)保留产物路径配置调整前的版本；[路径映射记录](artifact-path-mapping.json)将既有交付检查选项指向实际登记主稿，不改变问题、来源选择或实质判定标准。

本次先使用 `gpt-6-astra`／`xhigh` Responses API；收到明确的额度耗尽返回后，按授权由 Codex 原生子 Agent 从留存工作接续。执行身份和首次输出分别保留，不把整次运行描述为固定 Astra 模型的版本对照。

## 已交付结果

15 份报告均已完成当前版本的独立内容职责、审计和单独验收，并由现有交付操作返回 `completed: true`。共 8 份中文、7 份英文报告，对应 13 个独立问题。每篇目录分别保留首稿、计算、实际阅读记录、首次意见与修改；交付记录标明验收版本。

| 完整报告 | 语言 | 首稿与原始意见 |
|---|---|---|
| [AI Drug Discovery: From Research Workflows to Clinical Progress and Partnerships](reports/ai_drug_discovery_en/final.md) | en | [原始记录](reports/ai_drug_discovery_en/README.md) |
| [字节广告与商业化体系研究：从推荐、竞价到转化归因与电商增长](reports/bytedance_advertising_zh/final.md) | zh | [原始记录](reports/bytedance_advertising_zh/README.md) |
| [具身智能的部署路径：模型、数据与现实任务之间的工程闭环](reports/embodied_deployment_zh/final.md) | zh | [原始记录](reports/embodied_deployment_zh/README.md) |
| [新能源汽车电池研究：体系成本、使用性能与量产路径的比较](reports/ev_batteries_zh/final.md) | zh | [原始记录](reports/ev_batteries_zh/README.md) |
| [国内本地生活前置仓研究：区域密度、履约网络与单仓经济](reports/instant_retail_warehouses_zh/final.md) | zh | [原始记录](reports/instant_retail_warehouses_zh/README.md) |
| [China's Microdrama Market: Growth Structure, Platform Competition, and Value Distribution](reports/microdrama_market_en/final.md) | en | [原始记录](reports/microdrama_market_en/README.md) |
| [中国微短剧市场研究：增长结构、平台竞争与产业链价值分配](reports/microdrama_market_zh/final.md) | zh | [原始记录](reports/microdrama_market_zh/README.md) |
| [Comparing Model Benchmarks: Coverage, Reproducibility, and Real-Task Relevance](reports/model_benchmarks_en/final.md) | en | [原始记录](reports/model_benchmarks_en/README.md) |
| [On-Device Models: Hardware Constraints, Task Fit, and Edge–Cloud Design](reports/on_device_models_en/final.md) | en | [原始记录](reports/on_device_models_en/README.md) |
| [国内外Personal Agent研究：长期任务如何跨越记忆、授权与执行边界](reports/personal_agents_zh/final.md) | zh | [原始记录](reports/personal_agents_zh/README.md) |
| [全球模型后训练人才Mapping：研究专长、团队演化与能力网络](reports/post_training_talent_zh/final.md) | zh | [原始记录](reports/post_training_talent_zh/README.md) |
| [Test-Time Compute for Reasoning Models and Agents: Methods, Scaling Behavior, and Design Trade-offs](reports/test_time_compute_en/final.md) | en | [原始记录](reports/test_time_compute_en/README.md) |
| [推理模型与Agent的推理时计算：方法、扩展行为与设计权衡](reports/test_time_compute_zh/final.md) | zh | [原始记录](reports/test_time_compute_zh/README.md) |
| [Token Economics: From Model Costs and Pricing to Workload Value](reports/token_economics_en/final.md) | en | [原始记录](reports/token_economics_en/README.md) |
| [Verifiable Self-Improvement: Feedback Loops, Evaluators, and Generalization](reports/verifiable_self_improvement_en/final.md) | en | [原始记录](reports/verifiable_self_improvement_en/README.md) |

### 正文发生了哪些变化

- **微短剧：**中文稿解释增长时区分观察期间和统计人群，并准确保留北大规模估计不含出海收入的口径。英文稿独立形成论证，修正资料说明中的单位等表述。
- **推理时计算：**英文稿补清过度思考与准确率下降的单位，并让执行结果回到决策树的完成判断。网站排版检查还发现原验收漏掉了内部引用标签，作者将其改为论文名称，保留URL、版本和实质正文；此前交付及漏检记录保留在 `report-history/`。中文算例说明期望费用与逐题硬上限的区别，补出第二次前置处理假设。已有计算结果直接复用。
- **模型 benchmark：**审计在内容审阅之后发现 τ-bench 动作/输出奖励及确认政策盲点、原实验生成/执行/费用条件遗漏。对应正文已修订，原负面审计保留。
- **Personal Agent：**把一般架构说明展开为国内外产品在旅行与费用任务中的具体比较，连接授权、已支持动作、任务状态和产物。
- **新能源汽车电池：**需求审阅发现成熟路线的实际应用证据、体积维度比较不足。修订补入具名交付与装机材料，以及明确标为假设的包级体积算例，并连接车型选择。
- **前置仓与 AI 制药：**前置仓稿把原计算已有的投流和爬坡假设写明；制药稿改正化合物数量与迭代轮次混用。其他修订删除正文中的生产叙述，同时保留日期、版本和影响科学或经营判断的条件。

这些结果对应具体稿件的修改。本轮是开发基线：从基于 v2.3.4 的工作树开始，运行中完成本次记录的修复；Astra 返回明确余额耗尽后，由已获授权的 Codex 原生 Agent 接续。各输出保留实际执行身份，不作为固定模型的版本对照，也未据此估计整体研究质量或返工减少。

### 执行与工程记录

现有机械评估结果与独立内容判断分别保存。[必要验证](verification/)保留 CLI 使用场景、来源 ID 精确映射、二进制原件恢复、CSV 归一化、仓库强制检查，以及首次失败和对应修正。仍适用的已通过结果复用；相同输入和实际执行者的已导入意见不重复计为新评审。

[旧办公报告的编辑修订](office-editorial-revision/README.zh-CN.md)单独保留 11 月 5 日原文、修改和独立意见，不计为本轮第 16 份报告或新的独立问题。

首次机械汇总中13篇通过，2篇误报：中文微短剧稿重复出现的Markdown表格分隔线、英文推理时计算稿多次引用的含问号论文标题，被误当成重复正文。修复解析后，只重查这两篇并通过，正文未改；3项现有重复检测对照仍能识别真正的重复正文。原汇总与定向结果保存在 `verification/final-artifact-checks/`。
