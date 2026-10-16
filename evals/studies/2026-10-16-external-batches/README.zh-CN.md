# 外部评测批次：2026-10-14 与 2026-10-15-v1

[English](README.md) | [简体中文](README.zh-CN.md)

Song 授权将这 12 次已执行运行计入研究评测集。它们在冻结的 Toolkit 提交上完成，此处保留原语言题面、合成来源包、终稿和机械检查输出。

任务身份是研究问题。两道 Full 记录重复 Day-1 的同一问题，因此本目录是 **12 次运行、10 个不同问题**。本说明里对英文题的中文转述只是导读，不另计任务。

## 冻结提交

| 批次 | Toolkit 提交 | 版本 | 运行 |
|---|---|---|---|
| 2026-10-14 confirmed | `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3` | 1.0.0 | Lite × 6 |
| 2026-10-15-v1 | `f31345c5a994a8f1574d946388ee58fe1177ede2` | 1.1.0 | Lite × 4，Full × 2 |

Day-2 在上述 Day-1 提交上快进后冻结。tokens 与费用未测（`unknown`）。批次原件：[2026-10-14 简报](batches/2026-10-14-confirmed/DAILY_BRIEF.md)、[2026-10-15 简报](batches/2026-10-15-confirmed/DAILY_BRIEF.md)。

## 来源与评审

每个来源包都是合成材料。来源文件用自身语言写明：名称、数字和文书是构造的。这些包是工作流证据，不是事实权威；原语言报告是首要记录。

Lite 运行保留作者自检。`checklist_complete` 表示 Lite 机械清单通过，不认证语义质量。本目录的 Lite 运行没有另设评审。

两道 Full 运行要求独立评审。独立评审后端不可用（未配置 `RESEARCH_TOOLKIT_REVIEW_BACKEND`；评审发现结果仅为 `self_available`）。每道 Full 保留同一次会话的 `review/same_session_review.md`。评审强度为 degraded。这些评审不是独立评审。两道 Full 各做了一轮针对性修订。Full 交付检查记下机械通过，并把限制披露的覆盖留给语义审阅。

未入库的被取代批次：对比小品 `runs/2026-10-14/_superseded-vs-compare`，以及一页纸选题重做 `runs/2026-10-14/_superseded-topic-redo-short`。

## 运行

| 任务 | 批次 | 档位 | 种类 | 篇幅 | 修订 | 评审 |
|---|---|---|---|---|---:|---|
| [`api-price-war-cloud-bundling-zh-retest-20261014`](tasks/api-price-war-cloud-bundling-zh-retest-20261014/final.md) | 2026-10-14 | Lite | retest | 2687 非空白字（目标 2500–4500） | 0 | 作者自检 |
| [`enterprise-kb-llm-liability-zh-20261014`](tasks/enterprise-kb-llm-liability-zh-20261014/final.md) | 2026-10-14 | Lite | new | 3083 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`ev-battery-second-life-business-zh-20261014`](tasks/ev-battery-second-life-business-zh-20261014/final.md) | 2026-10-14 | Lite | new | 3019 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`bank-chatbot-deflection-evidence-en-retest-20261014`](tasks/bank-chatbot-deflection-evidence-en-retest-20261014/final.md) | 2026-10-14 | Lite | retest | 697 词（目标 600–900） | 0 | 作者自检 |
| [`open-weight-saas-lockin-en-20261014`](tasks/open-weight-saas-lockin-en-20261014/final.md) | 2026-10-14 | Lite | new | 1579 词（目标 1500–2500） | 0 | 作者自检 |
| [`private-credit-onchain-settlement-en-20261014`](tasks/private-credit-onchain-settlement-en-20261014/final.md) | 2026-10-14 | Lite | new | 1506 词（目标 1500–2500） | 0 | 作者自检 |
| [`enterprise-kb-llm-liability-zh-20261015-full`](tasks/enterprise-kb-llm-liability-zh-20261015-full/final.md) | 2026-10-15-v1 | Full | retest | 3491 非空白字（目标 3000–5000） | 1 | [同会话 degraded](tasks/enterprise-kb-llm-liability-zh-20261015-full/review/same_session_review.md) |
| [`dongshu-xisuan-training-procurement-zh-20261015`](tasks/dongshu-xisuan-training-procurement-zh-20261015/final.md) | 2026-10-15-v1 | Lite | new | 3074 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`bank-wm-structured-marketing-zh-20261015`](tasks/bank-wm-structured-marketing-zh-20261015/final.md) | 2026-10-15-v1 | Lite | new | 3077 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`private-credit-onchain-settlement-en-20261015-full`](tasks/private-credit-onchain-settlement-en-20261015-full/final.md) | 2026-10-15-v1 | Full | retest | 2038 词（目标 1500–2500） | 1 | [同会话 degraded](tasks/private-credit-onchain-settlement-en-20261015-full/review/same_session_review.md) |
| [`saas-frontier-ai-pricing-residency-en-20261015`](tasks/saas-frontier-ai-pricing-residency-en-20261015/final.md) | 2026-10-15-v1 | Lite | new | 1529 词（目标 1500–2500） | 0 | 作者自检 |
| [`tokenized-deposit-cash-equivalent-en-20261015`](tasks/tokenized-deposit-cash-equivalent-en-20261015/final.md) | 2026-10-15-v1 | Lite | new | 1523 词（目标 1500–2500） | 0 | 作者自检 |

篇幅取自批次汇总中的非空白计数。每行链接到 `final.md`。同目录还有案例元数据、请求、任务说明、`finish.json` 和 `check_delivery.out`。合成来源在 `sources/`，`sources/manifest.json` 标明 `factual_authority: false`。

## 研究问题

成对的题目共用一个问题。较晚的 id 是 Toolkit 1.1.0 上的 Full 复测，Day-1 合成来源包按原件复制、未改写。

1. `api-price-war-cloud-bundling-zh-retest-20261014` — 大模型 API 降价潮下，云厂商捆绑销售对独立模型公司毛利的挤压到了何种程度？商业战略上应如何应对？
2. `enterprise-kb-llm-liability-zh-20261014` 与 `enterprise-kb-llm-liability-zh-20261015-full` — 企业把内部知识库接到大模型后，幻觉与越权回答的责任应如何在法务、安全、业务之间分配？
3. `ev-battery-second-life-business-zh-20261014` — 中国新能源车动力电池梯次利用：回收商、车企与储能集成商的利益分配是否已形成可持续商业模式？
4. `bank-chatbot-deflection-evidence-en-retest-20261014` — Bank chatbot pilots that cite complaint deflection rates: what evidence actually supports replacing tier-1 human queues?
5. `open-weight-saas-lockin-en-20261014` — How do open-weight model releases change mid-market SaaS vendors’ lock-in and pricing power through 2027?
6. `private-credit-onchain-settlement-en-20261014` 与 `private-credit-onchain-settlement-en-20261015-full` — Private-credit funds piloting on-chain settlement: what operational and disclosure risks matter for LP reporting?
7. `dongshu-xisuan-training-procurement-zh-20261015` — 中国「东数西算」与大模型训练算力采购：西部绿电数据中心对东部训练客户，在时延、弃电、合同履约上是否已形成可复制的采购范式？
8. `bank-wm-structured-marketing-zh-20261015` — 银行理财子公司「含权」产品营销话术与底层波动：投教材料与适当性流程能否支撑销售端对回撤的承诺表述？
9. `saas-frontier-ai-pricing-residency-en-20261015` — How should mid-market B2B software vendors price and govern AI features that call third-party frontier models when vendor margins and customer data-residency clauses conflict through 2027?
10. `tokenized-deposit-cash-equivalent-en-20261015` — What evidence should corporate treasuries require before treating tokenized deposit pilots as operational cash equivalents for working-capital reporting?

英文题的中文导读：银行聊天机器人投诉分流率能否支撑替换一线人工队列；开源权重到 2027 年如何改变中型 SaaS 的锁定与定价权；私募信贷链上结算试点对 LP 报告的运营与披露风险；前沿模型毛利与数据驻留冲突时的 AI 功能定价与治理；司库把代币化存款试点记作营运现金等价物前应要求的证据。价格战复测与专用案例 `model_price_war_competitive_analysis_zh` 不是同一道题。

## 检查

`python evals/studies/2026-10-16-external-batches/verify.py` 核对 12 个 id、两枚冻结提交、合成披露、Full 运行的同会话评审措辞，以及 [artifact-hashes.json](artifact-hashes.json) 中的字节哈希。它不调用模型，也不给研究质量打分。id 与提交索引见 [manifest.json](manifest.json)。
