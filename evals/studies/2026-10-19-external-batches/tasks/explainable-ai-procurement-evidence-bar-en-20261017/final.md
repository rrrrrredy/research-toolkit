# Explainable AI Procurement: Post-Hoc NL vs Pre-Hoc Audit Trails Through 2027

**Audience:** Enterprise AI procurement, model risk, and vendor security/compliance  
**Materials:** Synthetic source pack S1–S4 only (disclosed). No live web. No independent review was performed.  
**Question:** For enterprise buyers and model-risk reviewers evaluating vendor “explainable AI” claims for high-stakes workflows (including adverse-action or customer-facing decision support), does post-hoc natural-language explanation evidence suffice versus requiring pre-deployment audit trails of features/rules/logs—and can that bar support production procurement and questionnaire answers through 2027?

---

## 1. Judgment in brief

**Post-hoc natural-language (NL) explanations alone do not suffice** for production approval on high-stakes or adverse-action workflows through 2027. Buyers should map RFP “explainable AI = Yes” answers to an **evidence tier**:

- **Tier 1 — Post-hoc NL explanation:** Generated after the decision; readable; may not match features/rules actually used.  
- **Tier 2 — Pre-deployment / pre-hoc auditability:** Versioned features/rules/prompts, input/output hashes, replay scripts, change control.

For adverse-action or customer-facing decision support, questionnaire Q14 “Yes” should require **Tier 2 evidence** (or explicit wording that explanations are **assistive only**, not faithful decision-path evidence). Tier 1 alone is insufficient for production approval on those paths (S2). Bake-off evidence shows NL fluency can coexist with mismatched triggers and unstable rationales (S3). Kill/hold criteria should revoke explainability “Yes” answers when replay fails or faithfulness samples fail (S4).

All materials are synthetic. This is a procurement/model-risk planning memo, not a regulator text.

## 2. What RFPs are actually asking

The enterprise AI procurement RFP excerpt (S1) highlights three linked questions:

- **Q14:** Does the system provide explainable AI for adverse or customer-facing decisions?  
- **Q15:** Are explanations faithful to the actual decision path?  
- **Q16:** Can the buyer reproduce decisions from logged features/rules/model versions?

Vendor marketing often answers Q14 “Yes” based on **post-hoc natural-language explanations only** (S1). That is the core procurement failure mode: a readability claim is treated as a faithfulness and reproducibility claim.

Q15 and Q16 are the corrective lenses. A complete explainability answer for high-stakes use must address faithfulness (Q15) and reproducibility from logs/versions (Q16), not only the presence of an NL story (Q14).

## 3. Evidence tiers under model-risk review

Model-risk review notes (S2) define the two tiers under discussion:

1. **Post-hoc NL explanation** — after-the-fact narrative; may not match features/rules actually used.  
2. **Pre-deployment audit trails** — versioned features/rules/prompts, input/output hashes, replay scripts, change control.

### 3.1 Reviewer stance (draft, from S2)

For high-stakes workflows through 2027, Q14 “Yes” should require Tier-2 evidence **or** explicit “assistive explanation only” wording. Tier-1 alone is insufficient for production approval on adverse-action paths.

That stance should become procurement policy language:

- **Production + adverse-action / customer-facing decision support:** Tier 2 required.  
- **Assistive UX explanations** (helping a human understand a suggestion, with human final decision and no adverse-action automation): Tier 1 may be acceptable if questionnaires **do not** claim faithful decision-path explainability.  
- **Never** allow Tier 1 evidence to answer Q15/Q16 affirmatively without separate faithfulness and replay tests.

## 4. Bake-off evidence: fluency ≠ faithfulness

Synthetic bake-off notes for three anonymized vendors (S3, n=3):

| Vendor | Explanation offering | Audit trail | Bake-off finding |
| --- | --- | --- | --- |
| V1 | Rich NL stories | Minimal logs | 4/10 explanations mismatched triggers |
| V2 | Sparse NL + feature attributions | Full replay package | Aligns on sampled cases |
| V3 | NL only; “LLM rationales” | Prompt logs only | Rationales changed under paraphrase |

**Counter-evidence stated in S3:** NL fluency correlated poorly with faithfulness in V1/V3.

### 4.1 Procurement reading

- **V1** would likely pass a naive Q14 check (rich NL) and fail a Q15 sample (4/10 mismatched triggers) and Q16 (minimal logs).  
- **V2** is the pattern to prefer for high-stakes: sparser NL, feature attributions, **full replay package**, alignment on sampled cases.  
- **V3** shows a distinct failure: LLM rationales that change under paraphrase—unstable “explanations” even when prompt logs exist. Prompt logs alone are not Tier 2 as defined in S2 (missing versioned features/rules, hashes, replay scripts, change control).

Do not treat n=3 as a market share study. Treat it as mechanism evidence: **post-hoc NL can look excellent while failing faithfulness and stability tests.**

## 5. Questionnaire mapping (how to answer and how to score)

Map S1 questions to evidence tiers and bake-off tests:

| RFP item | Tier 1 (post-hoc NL) alone | Tier 2 (pre-hoc auditability) | Suggested buyer scoring |
| --- | --- | --- | --- |
| Q14 Explainable AI for adverse/customer-facing | Insufficient for production “Yes” | Supports production “Yes” if replay works | Require Tier 2 or force “assistive only” wording |
| Q15 Faithful to actual decision path | Not established by fluency (V1/V3) | Test via sampled trigger alignment (V2) | Mandatory faithfulness sample before “Yes” |
| Q16 Reproduce from features/rules/versions | Cannot without logs/replay | Requires replay package + version bumps | Fail vendors who cannot replay sampled decisions |

**Vendor-facing rule:** If marketing says “explainable AI” based only on NL, procurement should score Q14 as **conditional / assistive**, not production-ready for adverse-action paths—unless Tier 2 artifacts are delivered and tested.

**Internal questionnaire hygiene:** Do not let sales-engineered “Yes” on Q14 auto-propagate to security/model-risk sign-off. Gate sign-off on Q15/Q16 evidence.

## 6. Kill / hold criteria through 2027

Security/compliance kill-criteria draft (S4) proposes:

1. **Cannot produce pre-hoc replay for a sampled decision** → no production on adverse-action workflows.  
2. **Explanation faithfulness sample fail rate above threshold** → revoke questionnaire “Yes” on explainability.  
3. **Vendor changes prompt/model without buyer-visible version bump affecting explanations** → incident + freeze.

S4 limitation: not a regulator text; maps internal appetite to RFP language only. Buyers still need to set the numerical faithfulness threshold for (2) in their model-risk standard—this pack does not prescribe a universal percentage. The V1 bake-off finding (4/10 mismatched) is an existence proof that failures occur at high rates for NL-heavy, log-light systems; use it to calibrate, not as a universal threshold.

### 6.1 Operationalizing kill criteria

- **Replay gate:** Before production on adverse-action paths, require successful replay on a pre-agreed sample (features/rules/versions → same decision). Failure = hold (S4).  
- **Faithfulness gate:** Run periodic samples comparing NL (or attributions) to logged triggers; breach of threshold revokes explainability “Yes” until remediated (S4; mechanism support from S3).  
- **Change-control gate:** Any prompt/model change that affects explanations without a buyer-visible version bump is an incident and freeze trigger (S4). This closes the gap where NL text silently drifts (illustrated by V3 paraphrase instability in S3).

## 7. Can this bar support production procurement through 2027?

**Yes, as an internal evidence bar**—if procurement, model risk, and security align on tier language and refuse to equate post-hoc NL with auditable decision paths.

Conditions for the bar to work:

1. RFP templates separate Q14/Q15/Q16 and ban collapsing them into one marketing “Yes” (S1 problem statement).  
2. Contracts require delivery of Tier-2 artifacts (versioned features/rules/prompts, hashes, replay tooling, change notification)—not only a demo of chatty explanations (S2 definition).  
3. Bake-off or onboarding tests include faithfulness and paraphrase-stability checks, not only readability (S3).  
4. Kill/hold criteria are written and enforceable (S4).

What this bar does **not** do: replace jurisdiction-specific adverse-action notice law, fairness testing, or model performance validation. Explainability evidence is necessary for the questionnaire claims in scope; it is not sufficient for full production risk acceptance.

## 8. Counter-evidence and uncertainties

- Some workflows may legitimately use NL explanations as **human assist** without claiming faithful path reconstruction; the bar must allow that labeling rather than forcing every NL feature into Tier 2 theater.  
- V2-style sparse NL + attributions may be less “impressive” in sales demos; procurement must resist fluency bias (S3 counter-evidence).  
- n=3 bake-off; synthetic RFP and review notes; no regulator text (S4).  
- Faithfulness threshold numeric value not specified in pack—must be set internally.  
- Prompt logs (V3) can look like audit trails while failing stability; define Tier 2 tightly (S2).  
- No independent review; synthetic sources only.

## 9. Recommendations (decision-ready)

1. Adopt Tier 1 / Tier 2 definitions in procurement and model-risk standards.  
2. For adverse-action / customer-facing decision support, require Tier 2 (or explicit assistive-only wording that blocks production automation claims).  
3. Score Q14/Q15/Q16 separately; forbid Q14 “Yes” based solely on post-hoc NL.  
4. Prefer vendors who can ship replay packages and feature attributions (V2 pattern) over rich-NL/minimal-log vendors (V1) or paraphrase-unstable LLM rationales (V3).  
5. Encode S4 kill/hold criteria; empower model risk to revoke explainability questionnaire answers.  
6. Disclose to stakeholders that this bar is internal appetite mapped to RFP language, not a regulator safe harbor (S4).

## 10. Limitations

Synthetic pack S1–S4 only. Not a regulatory interpretation. Bake-off n=3. Kill criteria are drafts for internal mapping. No independent review. Through-2027 applicability assumes vendors continue to market NL explanations as “explainable AI”; if industry norms shift toward mandatory replay bundles, update questionnaire scoring but keep faithfulness testing.

---

### Source ledger (synthetic)

| ID | Title (short) | Type |
| --- | --- | --- |
| S1 | Enterprise AI procurement RFP excerpt — explainable AI (2026-04) | synthetic RFP excerpt |
| S2 | Model-risk review — post-hoc NL vs pre-hoc audit trails (2026-05) | synthetic MR review |
| S3 | Bake-off notes — three vendors (anonymized) | synthetic n=3 bake-off |
| S4 | Security/compliance kill-criteria draft (2026-07) | synthetic kill-criteria draft |
