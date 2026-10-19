# External eval batches, 2026-10-16-v1 and 2026-10-17-v2

[English](README.md) | [简体中文](README.zh-CN.md)

**Result correction, 2026-10-19:** The predictive-maintenance, guide-fund, Scope-3 RFQ and credit-memo originals contain repeated passages; some also contain off-topic templates. The author's qualified/pass descriptions conflict with the prose: these four originals do not meet the report-quality requirements. Original mechanical outcomes remain historical records. [Four separate revisions and change notes](../../repairs/2026-10-19-reader-edit/README.md) reuse the source packs; they add no runs and are not a Toolkit core-capability upgrade. The table below records original runs, not current quality approval.

Song authorized these 12 recorded Lite runs for the research evaluation set. They were executed on frozen Toolkit commits and are stored here with the original-language brief, synthetic source pack, final report, and mechanical check output.

Task identity is the research question. The 12 question texts in this folder are distinct from one another. Two of them repeat a question already stored in the [October 16 external batches](../2026-10-16-external-batches/README.md). An English gloss of a Chinese question is a guide in this note, not a second task.

## Freeze

| Batch | Toolkit commit | Version | Runs |
|---|---|---|---|
| 2026-10-16-v1 | `f31345c5a994a8f1574d946388ee58fe1177ede2` | 1.1.0 | Lite × 6 |
| 2026-10-17-v2 | `fedf7cde832139c86cad585883cb5ec2f666427f` | 1.3.0 | Lite × 6 |

2026-10-16-v1 uses the same freeze as the 2026-10-15-v1 batch. 2026-10-17-v2 is frozen on v1.3.0. Tokens and cost were not measured (`unknown`). Original batch notes: [2026-10-16 brief](batches/2026-10-16-confirmed/DAILY_BRIEF.md), [2026-10-17 brief](batches/2026-10-17-confirmed/DAILY_BRIEF.md).

## Sources and review

Every source pack is synthetic. The source files say so in their own language: names, figures, and documents are constructed. These packs are workflow evidence. They are not factual authority, and the original-language report remains the primary record.

Four retests copy an earlier synthetic pack unchanged. `sources/COPY_PROVENANCE.txt` names that pack. The battery and chatbot retests restate the question. The bank-wealth and open-weight retests keep the earlier question text.

Lite runs record an author self-check. `checklist_complete` means the Lite mechanical checklist passed. It does not certify semantic quality. No run in this folder has a Toolkit independent review. The independent review backend was unavailable, and these Lite runs did not require one.

The six 2026-10-17-v2 runs also keep `review/outer_grok_review.md`. That note is an outer Grok reading in a separate context. It is not a Toolkit Full review, not an Astra review, and not a substitute for the formal review Lite skips. The batch index is [OUTER_REVIEW_BATCH_SUMMARY.md](batches/2026-10-17-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md). Each of those six notes records 达标 against its Lite brief. That record does not turn the Lite checklist into a semantic certificate, and it does not support a general quality claim.

Not in this folder: the compare-puzzle set `runs/2026-10-14/_superseded-vs-compare`, the one-pager topic redo `runs/2026-10-14/_superseded-topic-redo-short`, the superseded `2026-10-17-v1` topic gate, and `2026-10-18-v1` (the next three-day window).

## Original run records

| Task | Batch | Profile | Kind | Length | Revisions | Review |
|---|---|---|---|---|---:|---|
| [`ev-battery-second-life-business-zh-20261016-retest`](tasks/ev-battery-second-life-business-zh-20261016-retest/final.md) | 2026-10-16-v1 | Lite | retest | 3038 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`iIoT-predictive-maintenance-arr-zh-20261016`](tasks/iIoT-predictive-maintenance-arr-zh-20261016/final.md) | 2026-10-16-v1 | Lite | new | 3081 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`guide-fund-hardtech-return-ratio-zh-20261016`](tasks/guide-fund-hardtech-return-ratio-zh-20261016/final.md) | 2026-10-16-v1 | Lite | new | 3056 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`bank-chatbot-deflection-evidence-en-20261016-retest`](tasks/bank-chatbot-deflection-evidence-en-20261016-retest/final.md) | 2026-10-16-v1 | Lite | retest | 750 words (band 600–900) | 0 | author self-check |
| [`scope3-factor-rfq-evidence-en-20261016`](tasks/scope3-factor-rfq-evidence-en-20261016/final.md) | 2026-10-16-v1 | Lite | new | 1501 words (band 1500–2500) | 0 | author self-check |
| [`regional-bank-llm-credit-memo-controls-en-20261016`](tasks/regional-bank-llm-credit-memo-controls-en-20261016/final.md) | 2026-10-16-v1 | Lite | new | 1521 words (band 1500–2500) | 0 | author self-check |
| [`bank-wm-structured-marketing-zh-20261017-retest`](tasks/bank-wm-structured-marketing-zh-20261017-retest/final.md) | 2026-10-17-v2 | Lite | retest | 3009 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/bank-wm-structured-marketing-zh-20261017-retest/review/outer_grok_review.md) |
| [`personal-ai-false-proposition-zh-20261017`](tasks/personal-ai-false-proposition-zh-20261017/final.md) | 2026-10-17-v2 | Lite | new | 3154 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/personal-ai-false-proposition-zh-20261017/review/outer_grok_review.md) |
| [`bank-llm-explainability-production-bar-zh-20261017`](tasks/bank-llm-explainability-production-bar-zh-20261017/final.md) | 2026-10-17-v2 | Lite | new | 3007 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/bank-llm-explainability-production-bar-zh-20261017/review/outer_grok_review.md) |
| [`open-weight-saas-lockin-en-20261017-retest`](tasks/open-weight-saas-lockin-en-20261017-retest/final.md) | 2026-10-17-v2 | Lite | retest | 1861 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/open-weight-saas-lockin-en-20261017-retest/review/outer_grok_review.md) |
| [`law-firm-llm-signed-advice-bar-en-20261017`](tasks/law-firm-llm-signed-advice-bar-en-20261017/final.md) | 2026-10-17-v2 | Lite | new | 1859 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/law-firm-llm-signed-advice-bar-en-20261017/review/outer_grok_review.md) |
| [`explainable-ai-procurement-evidence-bar-en-20261017`](tasks/explainable-ai-procurement-evidence-bar-en-20261017/final.md) | 2026-10-17-v2 | Lite | new | 1563 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/explainable-ai-procurement-evidence-bar-en-20261017/review/outer_grok_review.md) |

Length figures are the recorded non-whitespace counts from the batch summaries. Each row links to `final.md`. Case metadata, the request, the task spec, `finish.json`, and `check_delivery.out` sit beside it. Synthetic sources are in `sources/`, with `sources/manifest.json` marking `factual_authority: false`.

## Research questions

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

`bank-wm-structured-marketing-zh-20261017-retest` repeats the question text of `bank-wm-structured-marketing-zh-20261015`. `open-weight-saas-lockin-en-20261017-retest` repeats the question text of `open-weight-saas-lockin-en-20261014`. Both are original-condition Lite retests on Toolkit 1.3.0, with the earlier synthetic pack copied unchanged. The earlier runs stay in the October 16 ingest.

`ev-battery-second-life-business-zh-20261016-retest` and `bank-chatbot-deflection-evidence-en-20261016-retest` copy the Day-1 synthetic packs of `ev-battery-second-life-business-zh-20261014` and `bank-chatbot-deflection-evidence-en-retest-20261014`. Their briefs restate the question, so this folder records the question that was run.

English guide to the Chinese questions: second-life battery processing fees and allocation; predictive-maintenance data rights, downtime SLAs, and ARR; guide-fund return-investment ratios versus financial return; structured bank-wealth marketing versus drawdown language; whether a “personal AI already exists” claim meets memory, consistency, ownership, and conversion evidence; whether post-hoc explanations support a bank “explainable deployment” production claim.

## Check

`python evals/studies/2026-10-19-external-batches/verify.py` checks the 12 ids, both freeze commits, synthetic disclosure, copied-pack bytes, Lite mechanical outcomes, outer-note wording on the 2026-10-17-v2 runs, and byte hashes in [artifact-hashes.json](artifact-hashes.json). It does not call a model or score research quality. The index of ids and commits is [manifest.json](manifest.json).
