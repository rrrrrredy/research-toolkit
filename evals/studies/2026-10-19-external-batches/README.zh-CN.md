# 外部评测批次：2026-10-16-v1 与 2026-10-17-v2

[English](README.md) | [简体中文](README.zh-CN.md)

**2026-10-19 结果更正：**本批次的预测性维护、引导基金、Scope-3 RFQ 和信贷备忘录四篇原稿存在重复段落，部分还混入离题模板。原作者的“合格”自检结论与正文不符，四篇原稿不能继续列为质量达标；原机械结果仍按历史记录保留。另存的[四篇修订稿与变化说明](../../repairs/2026-10-19-reader-edit/README.zh-CN.md)复用原来源，不增加运行次数，也不构成 Toolkit 核心能力升级。下表展示原运行结果，不表示当前质量认可。

Song 授权将这 12 次已执行的 Lite 运行计入研究评测集。它们在冻结的 Toolkit 提交上完成，此处保留原语言题面、合成来源包、终稿和机械检查输出。

任务身份是研究问题。本目录里的 12 段题面彼此不同。其中两段与已经入库的[10 月 16 日外部批次](../2026-10-16-external-batches/README.zh-CN.md)题面相同。本说明里对英文题的中文转述只是导读，不另计任务。

## 冻结提交

| 批次 | Toolkit 提交 | 版本 | 运行 |
|---|---|---|---|
| 2026-10-16-v1 | `f31345c5a994a8f1574d946388ee58fe1177ede2` | 1.1.0 | Lite × 6 |
| 2026-10-17-v2 | `fedf7cde832139c86cad585883cb5ec2f666427f` | 1.3.0 | Lite × 6 |

2026-10-16-v1 与 2026-10-15-v1 使用同一冻结提交。2026-10-17-v2 冻结在 v1.3.0。tokens 与费用未测（`unknown`）。批次原件：[2026-10-16 简报](batches/2026-10-16-confirmed/DAILY_BRIEF.md)、[2026-10-17 简报](batches/2026-10-17-confirmed/DAILY_BRIEF.md)。

## 来源与评审

每个来源包都是合成材料。来源文件用自身语言写明：名称、数字和文书是构造的。这些包是工作流证据，不是事实权威；原语言报告是首要记录。

四道复测原样复制更早的合成来源包。`sources/COPY_PROVENANCE.txt` 写明来源。动力电池与银行聊天机器人两道复测改写了题面。银行理财与开源权重两道复测保持原先题面。

Lite 运行保留作者自检。`checklist_complete` 表示 Lite 机械清单通过，不认证语义质量。本目录没有 Toolkit 独立评审。独立评审后端不可用，而这些 Lite 运行也不要求独立评审。

六次 2026-10-17-v2 运行另保留 `review/outer_grok_review.md`。那是另开上下文的外层 Grok 阅读笔记，不是 Toolkit Full 评审，不是 Astra 评审，也不替代 Lite 跳过的正式评审。批次索引见 [OUTER_REVIEW_BATCH_SUMMARY.md](batches/2026-10-17-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md)。六份笔记均对照各自 Lite 题面记下达标。该记录不把 Lite 清单变成语义认证，也不能支持普遍质量结论。

未入库：对比小品 `runs/2026-10-14/_superseded-vs-compare`，一页纸选题重做 `runs/2026-10-14/_superseded-topic-redo-short`，已被取代的 `2026-10-17-v1` 选题闸门，以及下一入库窗口的 `2026-10-18-v1`。

## 原运行记录

| 任务 | 批次 | 档位 | 种类 | 篇幅 | 修订 | 评审 |
|---|---|---|---|---|---:|---|
| [`ev-battery-second-life-business-zh-20261016-retest`](tasks/ev-battery-second-life-business-zh-20261016-retest/final.md) | 2026-10-16-v1 | Lite | retest | 3038 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`iIoT-predictive-maintenance-arr-zh-20261016`](tasks/iIoT-predictive-maintenance-arr-zh-20261016/final.md) | 2026-10-16-v1 | Lite | new | 3081 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`guide-fund-hardtech-return-ratio-zh-20261016`](tasks/guide-fund-hardtech-return-ratio-zh-20261016/final.md) | 2026-10-16-v1 | Lite | new | 3056 非空白字（目标 3000–5000） | 0 | 作者自检 |
| [`bank-chatbot-deflection-evidence-en-20261016-retest`](tasks/bank-chatbot-deflection-evidence-en-20261016-retest/final.md) | 2026-10-16-v1 | Lite | retest | 750 词（目标 600–900） | 0 | 作者自检 |
| [`scope3-factor-rfq-evidence-en-20261016`](tasks/scope3-factor-rfq-evidence-en-20261016/final.md) | 2026-10-16-v1 | Lite | new | 1501 词（目标 1500–2500） | 0 | 作者自检 |
| [`regional-bank-llm-credit-memo-controls-en-20261016`](tasks/regional-bank-llm-credit-memo-controls-en-20261016/final.md) | 2026-10-16-v1 | Lite | new | 1521 词（目标 1500–2500） | 0 | 作者自检 |
| [`bank-wm-structured-marketing-zh-20261017-retest`](tasks/bank-wm-structured-marketing-zh-20261017-retest/final.md) | 2026-10-17-v2 | Lite | retest | 3009 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/bank-wm-structured-marketing-zh-20261017-retest/review/outer_grok_review.md) |
| [`personal-ai-false-proposition-zh-20261017`](tasks/personal-ai-false-proposition-zh-20261017/final.md) | 2026-10-17-v2 | Lite | new | 3154 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/personal-ai-false-proposition-zh-20261017/review/outer_grok_review.md) |
| [`bank-llm-explainability-production-bar-zh-20261017`](tasks/bank-llm-explainability-production-bar-zh-20261017/final.md) | 2026-10-17-v2 | Lite | new | 3007 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/bank-llm-explainability-production-bar-zh-20261017/review/outer_grok_review.md) |
| [`open-weight-saas-lockin-en-20261017-retest`](tasks/open-weight-saas-lockin-en-20261017-retest/final.md) | 2026-10-17-v2 | Lite | retest | 1861 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/open-weight-saas-lockin-en-20261017-retest/review/outer_grok_review.md) |
| [`law-firm-llm-signed-advice-bar-en-20261017`](tasks/law-firm-llm-signed-advice-bar-en-20261017/final.md) | 2026-10-17-v2 | Lite | new | 1859 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/law-firm-llm-signed-advice-bar-en-20261017/review/outer_grok_review.md) |
| [`explainable-ai-procurement-evidence-bar-en-20261017`](tasks/explainable-ai-procurement-evidence-bar-en-20261017/final.md) | 2026-10-17-v2 | Lite | new | 1563 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/explainable-ai-procurement-evidence-bar-en-20261017/review/outer_grok_review.md) |

篇幅取自批次汇总中的非空白计数。每行链接到 `final.md`。同目录还有案例元数据、请求、任务说明、`finish.json` 和 `check_delivery.out`。合成来源在 `sources/`，`sources/manifest.json` 标明 `factual_authority: false`。

## 研究问题

1. `ev-battery-second-life-business-zh-20261016-retest` — 动力电池梯次利用商家：回收—拆解—重组环节的利益分配与可持续加工费模式是否成立？
2. `iIoT-predictive-maintenance-arr-zh-20261016` — 工业互联网平台向离散制造企业售卖「预测性维护」多年订阅时，传感器与产线数据权属、停机 SLA 与违约金条款，能否支撑平台侧的 ARR 定价与客户侧的采购审批？
3. `guide-fund-hardtech-return-ratio-zh-20261016` — 地方政府引导基金直投硬科技项目时，「返投比例」考核与退出通道（并购／回购／二级市场）的证据，能否支撑财政与社会 LP 对「既要产业落地又要财务回报」的同期表述？
4. `bank-chatbot-deflection-evidence-en-20261016-retest` — Bank retail chatbot “deflection” metrics: does the published evidence support replacing tier-1 human handling based on no-handoff rates?
5. `scope3-factor-rfq-evidence-en-20261016` — How should mid-market manufacturers set an evidence bar for third-party Scope-3 emissions factors before using them in customer RFQ sustainability questionnaires through 2027?
6. `regional-bank-llm-credit-memo-controls-en-20261016` — What operational and disclosure controls should regional banks require before allowing relationship managers to use third-party LLM copilots when drafting credit memos?
7. `bank-wm-structured-marketing-zh-20261017-retest` — 银行理财子公司「含权」产品营销话术与底层波动：投教材料与适当性流程能否支撑销售端对回撤的承诺表述？
8. `personal-ai-false-proposition-zh-20261017` — 面向 C 端与知识工作者的「Personal AI / 个人超级助手」产品与融资叙事中，关于持续记忆、跨设备一致性、个人数据权属与付费转化的证据门槛，能否支撑「已实现个人 AI」的定位主张？该主张对用户体验、投资人 DD、隐私/合规三方各自是否构成伪命题？
9. `bank-llm-explainability-production-bar-zh-20261017` — 商业银行将第三方大模型接入授信审批或反欺诈决策辅助时，「事后自然语言解释报告」与「事前可审计特征/规则/日志」两类证据，能否支撑模型风险与采购问卷中「已可解释部署」的结论并进入生产？
10. `open-weight-saas-lockin-en-20261017-retest` — How do open-weight model releases change mid-market SaaS vendors’ lock-in and pricing power through 2027?
11. `law-firm-llm-signed-advice-bar-en-20261017` — Before a mid-market law firm allows associates to use third-party LLM tools on client contract review and draft advice memos, what evidence bar and operational/disclosure controls are required so that tool outputs can support partner-signed advice or client disclosure duties through 2027—and when must the firm treat “AI legal research” claims as insufficient for signed work product?
12. `explainable-ai-procurement-evidence-bar-en-20261017` — For enterprise buyers and model-risk reviewers evaluating vendor “explainable AI” claims for high-stakes workflows (including adverse-action or customer-facing decision support), does post-hoc natural-language explanation evidence suffice versus requiring pre-deployment audit trails of features/rules/logs—and can that bar support production procurement and questionnaire answers through 2027?

`bank-wm-structured-marketing-zh-20261017-retest` 与 `bank-wm-structured-marketing-zh-20261015` 题面相同。`open-weight-saas-lockin-en-20261017-retest` 与 `open-weight-saas-lockin-en-20261014` 题面相同。二者都是 Toolkit 1.3.0 上的原条件 Lite 复测，更早的合成来源包按原件复制。更早的运行仍留在 10 月 16 日入库。

`ev-battery-second-life-business-zh-20261016-retest` 与 `bank-chatbot-deflection-evidence-en-20261016-retest` 分别复制 `ev-battery-second-life-business-zh-20261014` 和 `bank-chatbot-deflection-evidence-en-retest-20261014` 的 Day-1 合成来源包。两道题面是改写后的原条件复测，因此本目录记下实际运行的题面。

英文题的中文导读：零售银行聊天机器人的 no-handoff 分流率能否支撑替换一线人工处理；制造商在 2027 年前把第三方 Scope-3 因子写入客户 RFQ 问卷前应设的证据门槛；区域银行允许客户经理用第三方大模型起草信贷备忘录前应要求的运营与披露控制；开源权重到 2027 年如何改变中型 SaaS 的锁定与定价权；中型律所在合伙署名意见或客户披露前，对第三方大模型合同审阅与备忘录应设的证据门槛；高风险流程采购「可解释 AI」时，事后自然语言解释是否足以替代上线前特征、规则与日志审计。

## 检查

`python evals/studies/2026-10-19-external-batches/verify.py` 核对 12 个 id、两枚冻结提交、合成披露、复制来源包的字节、Lite 机械结果、2026-10-17-v2 外层笔记措辞，以及 [artifact-hashes.json](artifact-hashes.json) 中的字节哈希。它不调用模型，也不给研究质量打分。id 与提交索引见 [manifest.json](manifest.json)。
