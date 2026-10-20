# LLM clinical documentation into coding workflows: evidence bar and assistive-only kill line

**Audience:** Hospital clinical ops, HIM/coding, compliance, and payer liaison  
**Evidence standard:** Synthetic source pack only (S1–S4). All materials are fictional test evidence. No live web research. No independent review was performed. This memo is not clinical, coding, billing, or legal advice and is not an EHR feature bake-off.

## 1. Judgment

A regional hospital system should **not** allow LLM-drafted clinical documentation to support **medical-necessity or coding-consistency claims** in billing workflows until three controls are jointly true: (1) **immutable, payer-exportable override/audit trails** with reason codes on HIM edits; (2) **concordance and sampling measured against raw LLM drafts**, not only coder-cleaned notes; and (3) **active detection of silent omission** of acuity, allergies, and contraindications against independent sources such as nurse flowsheets. On the synthetic pack, vendor marketing of “AI documentation acceleration” with “coding / medical-necessity consistency ≥90%” rests on an ambient demo and an eight-week scorecard that internal notes admit was low-acuity pre-selected, sometimes omitted contraindications, lacked payer-exportable override trails, and scored concordance against cleaned notes rather than raw drafts (S1). The HIM worksheet and a ninety-day shadow make the gap operational: curated concordance 91% collapses to **61% raw-draft vs final-code**; **54%** of HIM edits lacked reason codes; omission flags ran **7 per 100** notes in a nurse dual-read sample; and vendor concordance excluded allergy/contraindication dropouts as “out of scope” (S2, S4). Until the bar is met, treat acceleration marketing as **assistive-only**—mandatory human attestation, no coding-consistency or medical-necessity claim language in payer or board materials (S3).

## 2. Work-product tiers

Clinical ops should separate two product classes (S3):

**Tier 1 — Assistive draft only.** LLM produces a draft; a credentialed clinician attests; coding proceeds from the attested note under ordinary HIM rules. Acceleration may be discussed as throughput assistance. No claim that the model “achieved” coding or medical-necessity consistency.

**Tier 2 — Coding / medical-necessity claim.** Outputs are used to support consistency or necessity assertions toward payers, quality programs, or executive ROI. This tier requires override/audit evidence, sampling versus **raw** drafts, and controls against silent omission of acuity/contraindications (S3). Ambient demos and curated scorecards do not unlock Tier 2 (S1, S2).

Crossing from Tier 1 to Tier 2 without the evidence bar is the primary governance failure mode in this pack.

## 3. Evidence bar before Tier-2 language

Map the HIM/compliance worksheet gaps to hard gates (S2):

| Claim layer | Vendor evidence in pack | Required buyer evidence |
| --- | --- | --- |
| Draft assist | Ambient demo | Acceptable for Tier 1 only; not a coding claim |
| Concordance | 91% on curated set vs cleaned notes | Blind sampling of raw drafts vs final codes; disclose exclusions |
| Medical necessity | Marketing KPI | Dual-read or flowsheet cross-check for acuity/allergy/contraindication omission |
| Override | “Human review available” | Immutable, payer-exportable edit log with reason codes |

Internal vendor notes already falsify several marketing implications: low-acuity selection, omitted contraindications, non-exportable overrides, cleaned-note concordance (S1). Buyers should treat those notes as the operative design, not the external slide.

## 4. Counter-evidence: silent omission and metric design

Coding review found three drafts that dropped allergy/contraindication lines present in nurse flowsheets; the vendor concordance set excluded those encounters as out of scope (S2). That pattern is decisive: **excluding the failure mode from the KPI does not eliminate the clinical or billing risk.** Shadow metrics reinforce the measurement problem—raw-draft concordance 61% versus the 91% cleaned-note figure—and show omission flags at 7 per 100 notes in a nurse dual-read sample (S4). Weak override hygiene (54% of HIM edits without reason codes) means the hospital cannot reconstruct who changed what for payer audit (S4). Fee discounts embedded in ROI slides further inflate the commercial case for acceleration without proving coding integrity (S4).

## 5. Human-override and audit controls

For any production path that touches coding or billing, require:

1. **Mandatory clinician attestation** before the note is coding-eligible (Tier 1 floor) (S3).
2. **Immutable override log** capturing author, timestamp, field-level change, and reason code; exportable to payer audit without vendor mediation (S1 gap, S2 gap, S3 requirement, S4 completeness failure).
3. **Sampling protocol** that scores raw LLM drafts against final codes on a rolling basis, with pre-registered exclusion rules that **cannot** drop allergy/contraindication failures as “out of scope” after the fact (S2, S4).
4. **Omission surveillance** against nurse flowsheets or equivalent independent documentation for acuity, allergies, and contraindications; threshold breaches trigger pause of Tier-2 claims (S2, S3, S4).
5. **ROI discipline:** strip vendor fee discounts from any board or payer-facing consistency narrative (S4).

“Human review available” without immutable export is not an override control (S2).

## 6. Kill criteria through 2027

Adopt the clinical-ops kill line (S3):

> Silent omission of contraindications or acuity, weak immutable overrides, **or** concordance measured only against cleaned notes → treat “AI documentation acceleration” marketing as **assistive-only**.

Operationalize:

- **Immediate:** Prohibit Tier-2 language in contracts, payer packets, and executive ROI while any kill condition is true.
- **Pilot continuation:** Allow Tier-1 assistive drafts with attestation and HIM oversight.
- **Re-entry to Tier 2:** Only after two consecutive quarters of (a) raw-draft concordance within an agreed band with transparent exclusions; (b) override log completeness above an agreed threshold with reason codes; (c) omission-flag rates below an agreed ceiling on dual-read samples; (d) successful payer-export drill of the audit trail.
- **Ongoing kill:** Any recurrence of silent contraindication/acuity omission in production sampling, or loss of exportable override integrity, returns the program to assistive-only even if prior quarters passed.

## 7. Decision framework for clinical ops / HIM / compliance / payer liaison

| Decision | Do now | Do not do |
| --- | --- | --- |
| Work-product class | Tier 1 assistive draft + attestation | Tier 2 coding/necessity claims |
| Metrics | Publish raw-draft concordance beside any curated figure | Cite 91% cleaned-note score alone |
| Overrides | Reason-coded immutable exportable logs | “Human review available” checkbox |
| Safety | Dual-read omission surveillance vs flowsheets | Let vendor exclude omission cases from KPI |
| Commercial | Separate throughput benefits from coding integrity | Bake fee discounts into consistency ROI |


## 7a. Implementation sequence (ninety days)

Week 1–2: freeze Tier-2 language in vendor statements of work and internal ROI decks; confirm attestation gates in the EHR path. Week 3–6: stand up immutable override logging with mandatory reason codes and a payer-export dry run; instrument raw-draft sampling beside any curated concordance the vendor still cites. Week 7–10: run nurse dual-read omission surveillance on a pre-registered sample; investigate every allergy/contraindication dropout instead of excluding it from the KPI. Week 11–12: compliance and payer liaison jointly decide whether any Tier-2 pilot language is warranted; default remains assistive-only if raw-draft concordance, override completeness, or omission rates miss agreed thresholds. Throughout, strip fee discounts from any slide that claims coding or medical-necessity consistency.

## 7b. Roles and accountability

Clinical ops owns attestation workflow integrity. HIM owns coding sampling design and reason-code completeness. Compliance owns the assistive-only vs Tier-2 classification and the kill-switch decision. Payer liaison owns external wording so that vendor ≥90% claims are not repeated as hospital fact. Vendors may supply tooling; they do not own the definition of medical-necessity consistency for the system. When incentives conflict—throughput pressure versus omission risk—the kill criteria in Section 6 take precedence over acceleration marketing.

## 8. Payer-liaison posture

Until Tier-2 evidence exists, payer communications should describe the tool as documentation assistance under clinician attestation—not as a validated coding-consistency engine. If asked about the vendor’s ≥90% figure, disclose that the hospital’s shadow raw-draft concordance was 61% and that curated metrics excluded material omission cases in the synthetic evaluation materials used for this governance review (S1, S2, S4). Do not argue medical necessity from model concordance alone.

## 9. Limitations

Sources S1–S4 are **synthetic**. Shadow metrics cover one unaudited regional pilot with vendor fee discounts in ROI slides (S4). The three omitted-contraindication drafts are an illustrative counter-evidence snippet, not a measured rate (S2). Kill criteria and tiers come from a synthetic clinical-ops memo, not a regulator bulletin (S3). **No independent review** was performed. Do not generalize 61%/54%/7-per-100 as industry benchmarks; do treat the *structure* of cleaned-note inflation, non-exportable overrides, and silent omission as sufficient to keep acceleration marketing assistive-only for deployments that match this pattern through 2027.Hospitals evaluating live vendors should commission their own raw-draft audits rather than relying on this synthetic pack.

## Source ledger (synthetic)

| ID | Title | Role |
| --- | --- | --- |
| S1 | Hospital LLM clinical documentation vendor pitch (2026-06) | ≥90% claim; internal low-acuity/omission/override/cleaned-note gaps |
| S2 | HIM / compliance / payer worksheet (2026-07) | Layer gaps; omission counter-evidence |
| S3 | Clinical ops memo on documentation → coding bar (2026-08) | Tiers; kill criteria |
| S4 | 90-day shadow metrics (2026-09) | 61% raw concordance; 54% missing reason codes; 7/100 omissions |

---

*Lite profile under Research Toolkit 1.3.1. Tool checklist pass is not semantic certification.*
