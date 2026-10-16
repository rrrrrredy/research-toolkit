# External eval batches, 2026-10-14 and 2026-10-15-v1

[English](README.md) | [简体中文](README.zh-CN.md)

Song authorized these 12 recorded runs for the research evaluation set. They were executed on frozen Toolkit commits and are stored here with the original-language brief, synthetic source pack, final report, and mechanical check output.

Task identity is the research question. Two Full records repeat a Day-1 question, so this folder holds **12 runs and 10 distinct questions**. An English gloss of a Chinese question is a guide in this note, not a second task.

## Freeze

| Batch | Toolkit commit | Version | Runs |
|---|---|---|---|
| 2026-10-14 confirmed | `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3` | 1.0.0 | Lite × 6 |
| 2026-10-15-v1 | `f31345c5a994a8f1574d946388ee58fe1177ede2` | 1.1.0 | Lite × 4, Full × 2 |

Day-2 was frozen after a fast-forward from the Day-1 commit above. Tokens and cost were not measured (`unknown`). Original batch notes: [2026-10-14 brief](batches/2026-10-14-confirmed/DAILY_BRIEF.md), [2026-10-15 brief](batches/2026-10-15-confirmed/DAILY_BRIEF.md).

## Sources and review

Every source pack is synthetic. The source files say so in their own language: names, figures, and documents are constructed. These packs are workflow evidence. They are not factual authority, and the original-language report remains the primary record.

Lite runs record an author self-check. `checklist_complete` means the Lite mechanical checklist passed. It does not certify semantic quality. Lite runs in this folder have no separate review.

The two Full runs required an independent reviewer. The independent review backend was unavailable (`RESEARCH_TOOLKIT_REVIEW_BACKEND` was unset; reviewer discovery reported `self_available` only). Each Full run keeps `review/same_session_review.md` from that same session. The review strength is degraded. These reviews are not independent reviews. Each Full run then applied one targeted revision. The Full delivery checker recorded a mechanical pass and still left limitation-disclosure coverage for semantic review.

Superseded batches are not in this folder: the compare-puzzle set `runs/2026-10-14/_superseded-vs-compare` and the one-pager topic redo `runs/2026-10-14/_superseded-topic-redo-short`.

## Runs

| Task | Batch | Profile | Kind | Length | Revisions | Review |
|---|---|---|---|---|---:|---|
| [`api-price-war-cloud-bundling-zh-retest-20261014`](tasks/api-price-war-cloud-bundling-zh-retest-20261014/final.md) | 2026-10-14 | Lite | retest | 2687 non-space Chinese characters (band 2500–4500) | 0 | author self-check |
| [`enterprise-kb-llm-liability-zh-20261014`](tasks/enterprise-kb-llm-liability-zh-20261014/final.md) | 2026-10-14 | Lite | new | 3083 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`ev-battery-second-life-business-zh-20261014`](tasks/ev-battery-second-life-business-zh-20261014/final.md) | 2026-10-14 | Lite | new | 3019 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`bank-chatbot-deflection-evidence-en-retest-20261014`](tasks/bank-chatbot-deflection-evidence-en-retest-20261014/final.md) | 2026-10-14 | Lite | retest | 697 words (band 600–900) | 0 | author self-check |
| [`open-weight-saas-lockin-en-20261014`](tasks/open-weight-saas-lockin-en-20261014/final.md) | 2026-10-14 | Lite | new | 1579 words (band 1500–2500) | 0 | author self-check |
| [`private-credit-onchain-settlement-en-20261014`](tasks/private-credit-onchain-settlement-en-20261014/final.md) | 2026-10-14 | Lite | new | 1506 words (band 1500–2500) | 0 | author self-check |
| [`enterprise-kb-llm-liability-zh-20261015-full`](tasks/enterprise-kb-llm-liability-zh-20261015-full/final.md) | 2026-10-15-v1 | Full | retest | 3491 non-space Chinese characters (band 3000–5000) | 1 | [same-session degraded](tasks/enterprise-kb-llm-liability-zh-20261015-full/review/same_session_review.md) |
| [`dongshu-xisuan-training-procurement-zh-20261015`](tasks/dongshu-xisuan-training-procurement-zh-20261015/final.md) | 2026-10-15-v1 | Lite | new | 3074 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`bank-wm-structured-marketing-zh-20261015`](tasks/bank-wm-structured-marketing-zh-20261015/final.md) | 2026-10-15-v1 | Lite | new | 3077 non-space Chinese characters (band 3000–5000) | 0 | author self-check |
| [`private-credit-onchain-settlement-en-20261015-full`](tasks/private-credit-onchain-settlement-en-20261015-full/final.md) | 2026-10-15-v1 | Full | retest | 2038 words (band 1500–2500) | 1 | [same-session degraded](tasks/private-credit-onchain-settlement-en-20261015-full/review/same_session_review.md) |
| [`saas-frontier-ai-pricing-residency-en-20261015`](tasks/saas-frontier-ai-pricing-residency-en-20261015/final.md) | 2026-10-15-v1 | Lite | new | 1529 words (band 1500–2500) | 0 | author self-check |
| [`tokenized-deposit-cash-equivalent-en-20261015`](tasks/tokenized-deposit-cash-equivalent-en-20261015/final.md) | 2026-10-15-v1 | Lite | new | 1523 words (band 1500–2500) | 0 | author self-check |

Length figures are the recorded non-whitespace counts from the batch summaries. Each row links to `final.md`. Case metadata, the request, the task spec, `finish.json`, and `check_delivery.out` sit beside it. Synthetic sources are in `sources/`, with `sources/manifest.json` marking `factual_authority: false`.

## Research questions

Repeated pairs share one question. The later id is a Full retest on Toolkit 1.1.0, with the Day-1 synthetic pack copied unchanged.

1. `api-price-war-cloud-bundling-zh-retest-20261014` — 大模型 API 降价潮下，云厂商捆绑销售对独立模型公司毛利的挤压到了何种程度？商业战略上应如何应对？
2. `enterprise-kb-llm-liability-zh-20261014` and `enterprise-kb-llm-liability-zh-20261015-full` — 企业把内部知识库接到大模型后，幻觉与越权回答的责任应如何在法务、安全、业务之间分配？
3. `ev-battery-second-life-business-zh-20261014` — 中国新能源车动力电池梯次利用：回收商、车企与储能集成商的利益分配是否已形成可持续商业模式？
4. `bank-chatbot-deflection-evidence-en-retest-20261014` — Bank chatbot pilots that cite complaint deflection rates: what evidence actually supports replacing tier-1 human queues?
5. `open-weight-saas-lockin-en-20261014` — How do open-weight model releases change mid-market SaaS vendors’ lock-in and pricing power through 2027?
6. `private-credit-onchain-settlement-en-20261014` and `private-credit-onchain-settlement-en-20261015-full` — Private-credit funds piloting on-chain settlement: what operational and disclosure risks matter for LP reporting?
7. `dongshu-xisuan-training-procurement-zh-20261015` — 中国「东数西算」与大模型训练算力采购：西部绿电数据中心对东部训练客户，在时延、弃电、合同履约上是否已形成可复制的采购范式？
8. `bank-wm-structured-marketing-zh-20261015` — 银行理财子公司「含权」产品营销话术与底层波动：投教材料与适当性流程能否支撑销售端对回撤的承诺表述？
9. `saas-frontier-ai-pricing-residency-en-20261015` — How should mid-market B2B software vendors price and govern AI features that call third-party frontier models when vendor margins and customer data-residency clauses conflict through 2027?
10. `tokenized-deposit-cash-equivalent-en-20261015` — What evidence should corporate treasuries require before treating tokenized deposit pilots as operational cash equivalents for working-capital reporting?

English guide to the Chinese questions: cloud bundling and independent-model gross margin; allocation of hallucination and unauthorized-answer responsibility; EV battery second-life commercial allocation; East-Data-West-Compute training procurement; structured bank-wealth marketing versus drawdown language. The price-war retest is a distinct question from the dedicated Toolkit case `model_price_war_competitive_analysis_zh`.

## Check

`python evals/studies/2026-10-16-external-batches/verify.py` checks the 12 ids, both freeze commits, synthetic disclosure, same-session review wording on the Full runs, and byte hashes in [artifact-hashes.json](artifact-hashes.json). It does not call a model or score research quality. The index of ids and commits is [manifest.json](manifest.json).
