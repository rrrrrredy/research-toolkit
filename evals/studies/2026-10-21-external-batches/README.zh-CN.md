# 外部评测批次：2026-10-18-v1 与 2026-10-19-v1

[English](README.md) | [简体中文](README.zh-CN.md)

**2026-10-21 结果更正：**FTE 与券商研报原稿把缺少原因码的比例写成完整度，作者自检和外层 Grok 评审均漏检。两篇原稿的无条件达标及批次全部达标结论已由[更正说明与两篇另存修订稿](../../repairs/2026-10-21-source-polarity/README.zh-CN.md)取代。历史原件不变，其他十篇未在本轮重新判定通过；仍为 12 次运行，含 8 道新题和 4 次复测。

Song 授权将这 12 次已执行的 Lite 运行计入研究评测集。它们在冻结的 Toolkit 提交上完成，此处保留原语言题面、合成来源包、终稿和机械检查输出。

任务身份是研究问题。本目录里的 12 段题面彼此不同。其中四段与更早入库的题面相同。本说明里对中文题的英文转述、以及对英文题的中文转述只是导读，不另计任务。

## 冻结提交

| 批次 | Toolkit 提交 | 版本 | 运行 |
|---|---|---|---|
| 2026-10-18-v1 | `fedf7cde832139c86cad585883cb5ec2f666427f` | 1.3.0 | Lite × 6 |
| 2026-10-19-v1 | `e245b90a324933f53fddf0deea039a7715708005` | 1.3.1 | Lite × 6 |

2026-10-18-v1 与已入库的 2026-10-17-v2 使用同一冻结提交。2026-10-19-v1 冻结在 v1.3.1。tokens 与费用未测（`unknown`）。批次原件：[2026-10-18 简报](batches/2026-10-18-confirmed/DAILY_BRIEF.md)、[2026-10-19 简报](batches/2026-10-19-confirmed/DAILY_BRIEF.md)。

## 来源与评审

每个来源包都是合成材料。来源文件用自身语言写明：名称、数字和文书是构造的。这些包是工作流证据，不是事实权威；原语言报告是首要记录。

四道复测原样复制更早的合成来源包。`sources/COPY_PROVENANCE.txt` 写明来源。四道复测都保持原先题面。

Lite 运行保留作者自检。`checklist_complete` 表示 Lite 机械清单通过，不认证语义质量。本目录没有 Toolkit 独立评审。独立评审后端不可用，而这些 Lite 运行也不要求独立评审。

十二次运行另保留 `review/outer_grok_review.md`。那是另开上下文的外层 Grok 阅读笔记，不是 Toolkit Full 评审，不是 Astra 评审，也不替代 Lite 跳过的正式评审。2026-10-18-v1 的三份英文笔记使用英文标题，其余九份使用中文标题。批次索引见 [2026-10-18 外层摘要](batches/2026-10-18-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md) 与 [2026-10-19 外层摘要](batches/2026-10-19-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md)。每份笔记均对照各自 Lite 题面记下达标。该记录不把 Lite 清单变成语义认证，也不能支持普遍质量结论。

未入库：对比小品 `runs/2026-10-14/_superseded-vs-compare`，一页纸选题重做 `runs/2026-10-14/_superseded-topic-redo-short`，已被取代的 `2026-10-17-v1` 选题闸门，以及下一窗口的 `2026-10-20-v2`（本次入库默认不含）。

## 运行记录

| 任务 | 批次 | 档位 | 种类 | 篇幅 | 修订 | 评审 |
|---|---|---|---|---|---:|---|
| [`dongshu-xisuan-training-procurement-zh-20261018-retest`](tasks/dongshu-xisuan-training-procurement-zh-20261018-retest/final.md) | 2026-10-18-v1 | Lite | retest | 3125 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/dongshu-xisuan-training-procurement-zh-20261018-retest/review/outer_grok_review.md) |
| [`chip-tooling-localization-bottleneck-claim-zh-20261018`](tasks/chip-tooling-localization-bottleneck-claim-zh-20261018/final.md) | 2026-10-18-v1 | Lite | new | 3153 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/chip-tooling-localization-bottleneck-claim-zh-20261018/review/outer_grok_review.md) |
| [`consumer-finance-llm-collection-compliance-kpi-zh-20261018`](tasks/consumer-finance-llm-collection-compliance-kpi-zh-20261018/final.md) | 2026-10-18-v1 | Lite | new | 3028 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/consumer-finance-llm-collection-compliance-kpi-zh-20261018/review/outer_grok_review.md) |
| [`saas-frontier-ai-pricing-residency-en-20261018-retest`](tasks/saas-frontier-ai-pricing-residency-en-20261018-retest/final.md) | 2026-10-18-v1 | Lite | retest | 1616 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/saas-frontier-ai-pricing-residency-en-20261018-retest/review/outer_grok_review.md) |
| [`ai-agent-workforce-fte-roi-bar-en-20261018`](tasks/ai-agent-workforce-fte-roi-bar-en-20261018/final.md) | 2026-10-18-v1 | Lite | new | 1588 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/ai-agent-workforce-fte-roi-bar-en-20261018/review/outer_grok_review.md) ; [达标结论已更正](../../repairs/2026-10-21-source-polarity/README.zh-CN.md) |
| [`pc-insurance-llm-fnol-consistency-bar-en-20261018`](tasks/pc-insurance-llm-fnol-consistency-bar-en-20261018/final.md) | 2026-10-18-v1 | Lite | new | 1533 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/pc-insurance-llm-fnol-consistency-bar-en-20261018/review/outer_grok_review.md) |
| [`guide-fund-hardtech-return-ratio-zh-20261019-retest`](tasks/guide-fund-hardtech-return-ratio-zh-20261019-retest/final.md) | 2026-10-19-v1 | Lite | retest | 3180 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/guide-fund-hardtech-return-ratio-zh-20261019-retest/review/outer_grok_review.md) |
| [`industrial-software-cad-plm-replacement-claim-zh-20261019`](tasks/industrial-software-cad-plm-replacement-claim-zh-20261019/final.md) | 2026-10-19-v1 | Lite | new | 3077 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/industrial-software-cad-plm-replacement-claim-zh-20261019/review/outer_grok_review.md) |
| [`broker-research-llm-publish-bar-zh-20261019`](tasks/broker-research-llm-publish-bar-zh-20261019/final.md) | 2026-10-19-v1 | Lite | new | 3057 非空白字（目标 3000–5000） | 0 | 作者自检；[外层 Grok 笔记](tasks/broker-research-llm-publish-bar-zh-20261019/review/outer_grok_review.md) ; [达标结论已更正](../../repairs/2026-10-21-source-polarity/README.zh-CN.md) |
| [`tokenized-deposit-cash-equivalent-en-20261019-retest`](tasks/tokenized-deposit-cash-equivalent-en-20261019-retest/final.md) | 2026-10-19-v1 | Lite | retest | 1549 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/tokenized-deposit-cash-equivalent-en-20261019-retest/review/outer_grok_review.md) |
| [`sovereign-ai-cloud-portability-claim-en-20261019`](tasks/sovereign-ai-cloud-portability-claim-en-20261019/final.md) | 2026-10-19-v1 | Lite | new | 1568 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/sovereign-ai-cloud-portability-claim-en-20261019/review/outer_grok_review.md) |
| [`hospital-llm-clinical-doc-coding-bar-en-20261019`](tasks/hospital-llm-clinical-doc-coding-bar-en-20261019/final.md) | 2026-10-19-v1 | Lite | new | 1509 词（目标 1500–2500） | 0 | 作者自检；[外层 Grok 笔记](tasks/hospital-llm-clinical-doc-coding-bar-en-20261019/review/outer_grok_review.md) |

篇幅取自批次汇总中的非空白计数。每行链接到 `final.md`。同目录还有案例元数据、请求、任务说明、`finish.json` 和 `check_delivery.out`。合成来源在 `sources/`，`sources/manifest.json` 标明 `factual_authority: false`。

## 研究问题

1. `dongshu-xisuan-training-procurement-zh-20261018-retest` — 中国「东数西算」与大模型训练算力采购：西部绿电数据中心对东部训练客户，在时延、弃电、合同履约上是否已形成可复制的采购范式？
2. `chip-tooling-localization-bottleneck-claim-zh-20261018` — 国内先进制程晶圆厂与关键设备商在对外融资／客户 DD 材料中，关于「关键设备国产化已解除产线瓶颈」的主张，现有证据门槛能否支撑？该主张对战略投资人与产线采购各自是否构成过度承诺？
3. `consumer-finance-llm-collection-compliance-kpi-zh-20261018` — 消费金融公司将 LLM 同时用于催收话术生成与合规质检时，「质检通过率」类 KPI 能否支撑对外「催收合规已达标」口径？何种失效模式必须把该口径降为「辅助质检、人工终责」？
4. `saas-frontier-ai-pricing-residency-en-20261018-retest` — How should mid-market B2B software vendors price and govern AI features that call third-party frontier models when vendor margins and customer data-residency clauses conflict through 2027?
5. `ai-agent-workforce-fte-roi-bar-en-20261018` — For enterprise buyers evaluating “AI agent workforce” / digital-employee vendors, does evidence of demo or pilot task completion support production claims of FTE replacement / headcount ROI through 2027—or must buyers treat headcount-replacement claims as a false proposition without workflow ownership, exception handling, and auditable override trails?
6. `pc-insurance-llm-fnol-consistency-bar-en-20261018` — Before a mid-market P&C insurer allows LLM-drafted first-notice-of-loss (FNOL) summaries into adjuster workflows, what evidence bar and human-override controls are required so outputs can support regulatory / actuarial consistency claims—and when must “AI claims acceleration” marketing be treated as assistive-only?
7. `guide-fund-hardtech-return-ratio-zh-20261019-retest` — 地方政府引导基金直投硬科技项目时，「返投比例」考核与退出通道（并购／回购／二级市场）的证据，能否支撑财政与社会 LP 对「既要产业落地又要财务回报」的同期表述？
8. `industrial-software-cad-plm-replacement-claim-zh-20261019` — 国内工业软件（CAD/CAE/PLM）厂商与集成商在融资／大客户 DD 材料中，关于「已可替代海外主力位、产线可切换」的主张，现有证据门槛能否支撑？该主张对战略投资人与工厂 IT／工艺部门各自是否构成过度承诺？
9. `broker-research-llm-publish-bar-zh-20261019` — 券商／资管将 LLM 用于投研底稿与报告草稿时，「模型生成 + 合规词表过滤」能否支撑对外「研报已可发布／可外发客户」口径？何种失效模式必须把该口径降为「辅助起草、人工署名终责」？
10. `tokenized-deposit-cash-equivalent-en-20261019-retest` — What evidence should corporate treasuries require before treating tokenized deposit pilots as operational cash equivalents for working-capital reporting?
11. `sovereign-ai-cloud-portability-claim-en-20261019` — For enterprise buyers evaluating “sovereign / residency-first AI cloud” offerings that also advertise open-weight model choice, what evidence bar is required before procurement can accept sovereignty + model-portability marketing as jointly true through 2027—and when must buyers treat the joint claim as a false proposition without portable eval harnesses, exportable toolchains, and auditable residency kill-switches?
12. `hospital-llm-clinical-doc-coding-bar-en-20261019` — Before a regional hospital system allows LLM-drafted clinical documentation into coding / billing workflows, what evidence bar and human-override controls are required so outputs can support medical-necessity / coding consistency claims—and when must “AI documentation acceleration” marketing be treated as assistive-only?

`dongshu-xisuan-training-procurement-zh-20261018-retest` 与 `dongshu-xisuan-training-procurement-zh-20261015` 题面相同。`saas-frontier-ai-pricing-residency-en-20261018-retest` 与 `saas-frontier-ai-pricing-residency-en-20261015` 题面相同。二者都是 Toolkit 1.3.0 上的原条件 Lite 复测，更早的合成来源包按原件复制。更早的运行仍留在[10 月 16 日外部批次](../2026-10-16-external-batches/README.zh-CN.md)。

`tokenized-deposit-cash-equivalent-en-20261019-retest` 与 `tokenized-deposit-cash-equivalent-en-20261015` 题面相同。这是 Toolkit 1.3.1 上的原条件 Lite 复测，更早的合成来源包按原件复制。更早的运行仍留在 10 月 16 日入库。

`guide-fund-hardtech-return-ratio-zh-20261019-retest` 与 `guide-fund-hardtech-return-ratio-zh-20261016` 题面相同。这是 Toolkit 1.3.1 上的原条件 Lite 复测，更早的合成来源包按原件复制。更早的运行仍留在[10 月 19 日外部批次](../2026-10-19-external-batches/README.zh-CN.md)。该次入库后来记下：20261016 原稿不符合报告质量要求。本目录把 20261019 复测作为另一次 Lite 运行保留，不替代那次更正。

英文题的中文导读：中型 SaaS 在利润率与客户数据驻留条款冲突时，如何为调用前沿模型的 AI 功能定价与治理（至 2027）；企业采购「AI agent 劳动力」时，演示或试点完成度能否支撑 FTE 替代与人头 ROI，还是在缺少流程所有权、例外处理和可审计覆盖前应视为伪命题；中型财险把 LLM 草拟的 FNOL 摘要送入理赔流程前，何种证据门槛与人工覆盖才能支撑监管或精算一致性主张；企业财资在把代币化存款试点当作营运资金现金等价物前应要求的证据；采购「主权／驻留优先且可选开放权重」云时，何种证据门槛才能同时接受主权与可移植宣传（至 2027）；区域医院把 LLM 临床文书送入编码或计费前，何种证据门槛与人工覆盖才能支撑医疗必要性或编码一致性主张。

## 检查

`python evals/studies/2026-10-21-external-batches/verify.py` 核对 12 个 id、两枚冻结提交、合成披露、复制来源包的字节、Lite 机械结果、全部 12 次运行的外层笔记措辞，以及 [artifact-hashes.json](artifact-hashes.json) 中的字节哈希。它不调用模型，也不给研究质量打分。id 与提交索引见 [manifest.json](manifest.json)。
