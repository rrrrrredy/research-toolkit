# 外层 Grok 评价（Lite 产物）

> **评价类型：** 外层独立质量评价（评测员/复核员另开上下文对照任务与合成来源）。  
> **非 Full 内部评审 / 非 Astra：** 不记作 Full 档位，不替代 Lite 用户流程中跳过的正式评审。  
> **成本：** 单列；本评价调用用量 **unknown**（无单独模型用量回执）。  
> **角色：** Toolkit复核员；不替作者改稿；不另加验收层。

---

## 元信息

| 项 | 值 |
| --- | --- |
| 任务目录 | `runs/2026-10-19-confirmed/hospital-llm-clinical-doc-coding-bar-en-20261019` |
| 题号 | EN-N2（新题） |
| 题面 | Hospital LLM clinical docs into coding/billing: evidence bar; when assistive-only |
| 模式 | Lite（profile=lite） |
| Toolkit | VERSION `1.3.1`，commit `e245b90a324933f53fddf0deea039a7715708005`（据 RUN_LOG） |
| 交付稿 | `final.md`（whitespace words 1509） |
| 来源范围 | 仅 `sources/` 合成包 S1–S4；不联网 |
| 评价日期 | 2026-10-19（Asia/Shanghai） |
| 评价口径 | 对照 brief/选题约定：必答内容、篇幅、合成来源边界、证据纪律、反证与 Kill、落地与未决；checklist/check_delivery 通过不认证语义质量 |

---

## 结论

****达标。** Relative to this Lite brief (must-answer, length, synthetic-source boundary, evidence discipline), the delivery is acceptable; key claims match S1–S4; no substantive semantic defect requiring return.**

---

## 对照任务约定的检查点

| 约定 | 实测 | 判定 |
| --- | --- | --- |
| Length ≥1500 words (suggested 1500–2500) | `checks/length.md` and independent recount **1509** | 通过 |
| Core judgment | §1: assistive-only until immutable exportable override + raw-draft sampling + omission monitoring | 通过 |
| Work-product tiers | §2: Tier1 draft assist vs Tier2 coding/necessity claim | 通过 |
| Evidence bar / override controls | §3–§5: raw vs cleaned; reason-coded exportable logs; dual-read omission | 通过 |
| Counter-evidence | §4: three allergy/contraindication drops excluded from KPI; 61% vs 91% | 通过 |
| Kill criteria through 2027 | §6: omission / weak overrides / cleaned-only concordance → assistive-only | 通过 |
| Do not treat draft acceleration as coding-consistency proof | Header + §§1–3 | 通过 |
| Disclose synthetic; no independent review | Header + §9 | 通过 |

软件侧（RUN_LOG）：start/save/check-draft/finish/check_delivery 均成功。本外层评价补语义/来源对照，不回填脚本分数。

---

## 来源一致性

对照 `sources/S1–S4`、`data/claims_registry.csv` 抽核：

| 主张要点 | 来源 | 一致性 |
| --- | --- | --- |
| ≥90% marketing; internal low-acuity / omission / non-exportable / cleaned-note concordance | S1 | 一致 |
| 91% curated vs cleaned; three flowsheet drops excluded as out of scope | S2 | 一致 |
| Tiers + kill → assistive-only | S3 | 一致 |
| Raw-draft 61% vs 91%; 54% edits lack reason codes; 7/100 omission flags | S4 | 一致 |
| Judgment: cleaned ≥90% cannot support coding/necessity claims | C5–C6 / §1 | 与材料同向 |

未发现关键数量或因果相对合成来源的误读或捏造。

---

## 主要问题

**无实质新问题**（相对任务约定与合成来源；不为凑缺陷硬找）。

观察（不构成不达标，亦不要求作者改稿）：

1. Word count 1509 at the floor but meets bound — not a defect.
2. Payer-liaison posture (§8) correctly refuses repeating vendor ≥90% as hospital fact.
3. No Toolkit method/engineering fix suggested.

---

## 保留未决（材料内，报告已诚实披露）

- Shadow metrics n=1 unaudited pilot with fee discounts in ROI (disclosed).
- Three omission drafts are illustrative snippets, not a measured rate (disclosed).

---

## 用量

| 项 | 值 |
| --- | --- |
| 作者侧（研究/CLI） | unknown（RUN_LOG：本机 CLI，无模型用量回执） |
| 本外层评价 | unknown（单列成本；非 Full/Astra） |

---

## 一句话交付判断

Relative to this Lite brief: **达标，可交负责人收口**; outer review listed separately; not Full.
