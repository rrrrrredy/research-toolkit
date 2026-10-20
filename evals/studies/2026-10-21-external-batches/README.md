# External eval batches, 2026-10-18-v1 and 2026-10-19-v1

[English](README.md) | [简体中文](README.zh-CN.md)

Song authorized these 12 recorded Lite runs for the research evaluation set. They were executed on frozen Toolkit commits and are stored here with the original-language brief, synthetic source pack, final report, and mechanical check output.

Task identity is the research question. The 12 question texts in this folder are distinct from one another. Four of them repeat a question already stored in an earlier ingest. An English gloss of a Chinese question is a guide in this note, not a second task.

## Freeze

| Batch | Toolkit commit | Version | Runs |
|---|---|---|---|
| 2026-10-18-v1 | `fedf7cde832139c86cad585883cb5ec2f666427f` | 1.3.0 | Lite × 6 |
| 2026-10-19-v1 | `e245b90a324933f53fddf0deea039a7715708005` | 1.3.1 | Lite × 6 |

2026-10-18-v1 uses the same freeze as the ingested 2026-10-17-v2 batch. 2026-10-19-v1 is frozen on v1.3.1. Tokens and cost were not measured (`unknown`). Original batch notes: [2026-10-18 brief](batches/2026-10-18-confirmed/DAILY_BRIEF.md), [2026-10-19 brief](batches/2026-10-19-confirmed/DAILY_BRIEF.md).

## Sources and review

Every source pack is synthetic. The source files say so in their own language: names, figures, and documents are constructed. These packs are workflow evidence. They are not factual authority, and the original-language report remains the primary record.

Four retests copy an earlier synthetic pack unchanged. `sources/COPY_PROVENANCE.txt` names that pack. All four keep the earlier question text.

Lite runs record an author self-check. `checklist_complete` means the Lite mechanical checklist passed. It does not certify semantic quality. No run in this folder has a Toolkit independent review. The independent review backend was unavailable, and these Lite runs did not require one.

All 12 runs also keep `review/outer_grok_review.md`. That note is an outer Grok reading in a separate context. It is not a Toolkit Full review, not an Astra review, and not a substitute for the formal review Lite skips. Three 2026-10-18-v1 English notes use an English heading; the other nine notes use the Chinese heading. The batch indexes are [2026-10-18 outer summary](batches/2026-10-18-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md) and [2026-10-19 outer summary](batches/2026-10-19-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md). Each note records 达标 against its Lite brief. That record does not turn the Lite checklist into a semantic certificate, and it does not support a general quality claim.

Not in this folder: the compare-puzzle set `runs/2026-10-14/_superseded-vs-compare`, the one-pager topic redo `runs/2026-10-14/_superseded-topic-redo-short`, the superseded `2026-10-17-v1` topic gate, and `2026-10-20-v2` (the next window; default not for this ingest).

## Run records

| Task | Batch | Profile | Kind | Length | Revisions | Review |
|---|---|---|---|---|---:|---|
| [`dongshu-xisuan-training-procurement-zh-20261018-retest`](tasks/dongshu-xisuan-training-procurement-zh-20261018-retest/final.md) | 2026-10-18-v1 | Lite | retest | 3125 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/dongshu-xisuan-training-procurement-zh-20261018-retest/review/outer_grok_review.md) |
| [`chip-tooling-localization-bottleneck-claim-zh-20261018`](tasks/chip-tooling-localization-bottleneck-claim-zh-20261018/final.md) | 2026-10-18-v1 | Lite | new | 3153 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/chip-tooling-localization-bottleneck-claim-zh-20261018/review/outer_grok_review.md) |
| [`consumer-finance-llm-collection-compliance-kpi-zh-20261018`](tasks/consumer-finance-llm-collection-compliance-kpi-zh-20261018/final.md) | 2026-10-18-v1 | Lite | new | 3028 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/consumer-finance-llm-collection-compliance-kpi-zh-20261018/review/outer_grok_review.md) |
| [`saas-frontier-ai-pricing-residency-en-20261018-retest`](tasks/saas-frontier-ai-pricing-residency-en-20261018-retest/final.md) | 2026-10-18-v1 | Lite | retest | 1616 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/saas-frontier-ai-pricing-residency-en-20261018-retest/review/outer_grok_review.md) |
| [`ai-agent-workforce-fte-roi-bar-en-20261018`](tasks/ai-agent-workforce-fte-roi-bar-en-20261018/final.md) | 2026-10-18-v1 | Lite | new | 1588 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/ai-agent-workforce-fte-roi-bar-en-20261018/review/outer_grok_review.md) |
| [`pc-insurance-llm-fnol-consistency-bar-en-20261018`](tasks/pc-insurance-llm-fnol-consistency-bar-en-20261018/final.md) | 2026-10-18-v1 | Lite | new | 1533 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/pc-insurance-llm-fnol-consistency-bar-en-20261018/review/outer_grok_review.md) |
| [`guide-fund-hardtech-return-ratio-zh-20261019-retest`](tasks/guide-fund-hardtech-return-ratio-zh-20261019-retest/final.md) | 2026-10-19-v1 | Lite | retest | 3180 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/guide-fund-hardtech-return-ratio-zh-20261019-retest/review/outer_grok_review.md) |
| [`industrial-software-cad-plm-replacement-claim-zh-20261019`](tasks/industrial-software-cad-plm-replacement-claim-zh-20261019/final.md) | 2026-10-19-v1 | Lite | new | 3077 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/industrial-software-cad-plm-replacement-claim-zh-20261019/review/outer_grok_review.md) |
| [`broker-research-llm-publish-bar-zh-20261019`](tasks/broker-research-llm-publish-bar-zh-20261019/final.md) | 2026-10-19-v1 | Lite | new | 3057 non-space Chinese characters (band 3000–5000) | 0 | author self-check; [outer Grok note](tasks/broker-research-llm-publish-bar-zh-20261019/review/outer_grok_review.md) |
| [`tokenized-deposit-cash-equivalent-en-20261019-retest`](tasks/tokenized-deposit-cash-equivalent-en-20261019-retest/final.md) | 2026-10-19-v1 | Lite | retest | 1549 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/tokenized-deposit-cash-equivalent-en-20261019-retest/review/outer_grok_review.md) |
| [`sovereign-ai-cloud-portability-claim-en-20261019`](tasks/sovereign-ai-cloud-portability-claim-en-20261019/final.md) | 2026-10-19-v1 | Lite | new | 1568 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/sovereign-ai-cloud-portability-claim-en-20261019/review/outer_grok_review.md) |
| [`hospital-llm-clinical-doc-coding-bar-en-20261019`](tasks/hospital-llm-clinical-doc-coding-bar-en-20261019/final.md) | 2026-10-19-v1 | Lite | new | 1509 words (band 1500–2500) | 0 | author self-check; [outer Grok note](tasks/hospital-llm-clinical-doc-coding-bar-en-20261019/review/outer_grok_review.md) |

Length figures are the recorded non-whitespace counts from the batch summaries. Each row links to `final.md`. Case metadata, the request, the task spec, `finish.json`, and `check_delivery.out` sit beside it. Synthetic sources are in `sources/`, with `sources/manifest.json` marking `factual_authority: false`.

## Research questions

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

`dongshu-xisuan-training-procurement-zh-20261018-retest` repeats the question text of `dongshu-xisuan-training-procurement-zh-20261015`. `saas-frontier-ai-pricing-residency-en-20261018-retest` repeats the question text of `saas-frontier-ai-pricing-residency-en-20261015`. Both are original-condition Lite retests on Toolkit 1.3.0, with the earlier synthetic pack copied unchanged. The earlier runs stay in the [October 16 external batches](../2026-10-16-external-batches/README.md).

`tokenized-deposit-cash-equivalent-en-20261019-retest` repeats the question text of `tokenized-deposit-cash-equivalent-en-20261015`. It is an original-condition Lite retest on Toolkit 1.3.1, with the earlier synthetic pack copied unchanged. The earlier run stays in the October 16 ingest.

`guide-fund-hardtech-return-ratio-zh-20261019-retest` repeats the question text of `guide-fund-hardtech-return-ratio-zh-20261016`. It is an original-condition Lite retest on Toolkit 1.3.1, with the earlier synthetic pack copied unchanged. The earlier run stays in the [October 19 external batches](../2026-10-19-external-batches/README.md). That ingest later recorded that the 20261016 original does not meet report-quality requirements. This folder keeps the 20261019 retest as its own Lite run. It does not replace that correction.

English guide to the Chinese questions: whether western green-power data centers already offer a replicable training-procurement pattern for eastern customers; whether a “key equipment localization has removed the line bottleneck” claim is supported for investors and fab buyers; whether collection QA pass-rates support a consumer-finance “compliance achieved” claim; whether guide-fund return-investment ratios support a joint “industry landing and financial return” statement; whether domestic CAD/CAE/PLM evidence supports “already replaces the overseas primary seat and the line can switch”; whether lexicon filtering supports a broker-research “ready to publish / send to clients” claim.

## Check

`python evals/studies/2026-10-21-external-batches/verify.py` checks the 12 ids, both freeze commits, synthetic disclosure, copied-pack bytes, Lite mechanical outcomes, outer-note wording on all 12 runs, and byte hashes in [artifact-hashes.json](artifact-hashes.json). It does not call a model or score research quality. The index of ids and commits is [manifest.json](manifest.json).
