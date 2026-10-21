# LLM-Drafted FNOL Summaries: Consistency Evidence Bar and Assistive-Only Kill Line Through 2027

**Audience:** P&C claims ops, actuarial, and compliance  
**Materials:** Synthetic source pack S1–S4 only (disclosed). No live web retrieval. No independent review was performed.  
**Question:** Before a mid-market P&C insurer allows LLM-drafted first-notice-of-loss (FNOL) summaries into adjuster workflows, what evidence bar and human-override controls are required so outputs can support regulatory / actuarial consistency claims—and when must “AI claims acceleration” marketing be treated as assistive-only?

---

## 1. Judgment in brief

On this pack’s evidence, **LLM-drafted FNOL summaries may enter adjuster workflows only as draft assist** unless the insurer can show coverage-trigger completeness checks, immutable override/audit, and sampling reconciled to actuarial coding (S3). A pilot charter that markets “AI claims acceleration” while implying faster cycle time does not, by itself, support **regulatory / actuarial consistency** claims (S1). Dual review found silent omission of prior-damage language, wrong peril coding, and—crucially—cycle time up about **8%** while reserve variance widened, leading actuarial to refuse “consistency” language (S2). A 60-day dashboard shows **71%** draft adoption, **22%** full human rewrite, override reasons captured on only **48%** of edits, and coverage-trigger auto-pass **81%** with manual fails catching **+6pp** omissions—limited to a single auto LOB and not regulator-facing (S4).

**Kill rule through 2027:** silent omission of coverage triggers, missing override audit, or unreconciled coding drift → marketing must stay **assistive-only**; no regulatory/actuarial consistency claim (S3). Human override required in policy but not enforced in UI (S1) is already a control failure under that rule.



Mid-market insurers in this pack should also separate **product marketing** from **actuarial sign-off**. Sales or vendor success may want “AI claims acceleration” language for cycle-time narratives; actuarial and compliance own whether any FNOL artifact may be cited for regulatory or consistency purposes. When those functions diverge—as they do when cycle time rises and reserve variance worsens (S2)—the stricter function wins. That governance split is part of the evidence bar, not optional change management.

## 2. Work-product tiers

### Tier 1 — Draft assist

LLM text for adjuster edit with **no consistency claim** (S3). This is the only tier the pack’s pilot can honestly occupy today: summaries land in the adjuster queue (S1), adoption is high (71%, S4), and some drafts match adjusters (Claim C in S2). Acceleration marketing, if used at all, must be framed as assistive throughput—not as certified consistency of FNOL content for regulatory or actuarial use.

### Tier 2 — Consistency-supporting

Requires, per S3: (1) coverage-trigger completeness checks; (2) immutable override/audit; (3) sampling versus actuarial coding. The pack shows partial movement toward (1)—an auto checklist at 81% pass with manual review catching +6pp omissions (S4)—but override reason capture at 48% fails a serious audit bar, and S2’s peril miscodes plus widened reserve variance show sampling/coding reconciliation is not in place. UI non-enforcement of required human override (S1) blocks Tier 2 regardless of model quality.

Until Tier 2 controls exist and hold under sampling, outputs must not be described as supporting regulatory or actuarial consistency.

## 3. Required evidence bar and human-override controls

### 3.1 Coverage-trigger completeness

S1’s internal notes: coverage-trigger fields sometimes omitted when caller language was ambiguous. S2 Claim A: LLM summary omits prior-damage mention material to reserve—classic silent omission. S4: checklist auto-pass 81%; manual fails add 6pp omission catch. **Bar:** FNOL drafts that can support consistency claims need automated completeness checks on coverage-trigger fields **plus** mandatory human confirmation when ambiguity or checklist fail occurs. Auto-pass alone is insufficient while manual review still finds material omissions.

### 3.2 Immutable override / audit trail

Policy draft required human override but UI did not enforce it (S1). S4: override reason captured on only 48% of edits. **Bar:** every human edit that changes coverage triggers, peril codes, or reserve-relevant narrative must write an immutable reason code into an exportable audit log before the summary is treated as adjuster-accepted work product. “Override available” without enforcement and without reason capture fails the bar.

### 3.3 Sampling vs actuarial coding

S2 Claim B maps to the wrong peril code (actuarial coding drift / consistency fail). Cycle-time +8% with widened reserve variance led actuarial to refuse consistency language. **Bar:** stratified sampling of LLM-assisted FNOLs against actuarial coding and reserve outcomes, with stop-the-line rules when drift or reserve variance worsens. Throughput gains that coincide with reserve quality loss are evidence against—not for—consistency claims.

### 3.4 Control summary for cutover

| Control | Pack signal | Tier-2 gate |
| --- | --- | --- |
| Coverage-trigger checklist + human confirm on fail/ambiguity | Omissions in S1/S2; +6pp manual catch (S4) | Required |
| UI-enforced human override | Required in policy, not in UI (S1) | Required |
| Immutable reason-coded audit export | 48% reason capture (S4) | Required |
| Actuarial sampling on peril codes & reserve variance | Wrong peril; +8% cycle / worse reserves (S2) | Required |
| LOB / regulator scope disclosure | Single auto LOB; not regulator-facing (S4) | Disclose; do not generalize |

## 4. Counter-evidence

1. **Silent omission of coverage triggers** — prior-damage dropped when material to reserve (S2 Claim A); ambiguous caller language omits fields (S1).  
2. **Coding drift** — wrong peril code (S2 Claim B) breaks actuarial consistency even when prose looks fluent.  
3. **Throughput vs quality** — cycle time +8% with widened reserve variance; actuarial refuses consistency language (S2).  
4. **Override theater** — policy requires override; UI does not enforce (S1); reasons missing on 52% of edits (inferred from 48% capture, S4).  
5. **Scope limits** — 60-day dashboard is mid-market auto LOB only, not regulator-facing (S4); Claim C “clean draft” does not cancel A/B failures.

These points do not ban FNOL drafting tools. They ban **promoting draft assist as consistency-certified claims acceleration**.

## 5. Kill criteria through 2027 (assistive-only line)

Per S3, marketing must stay **assistive-only**—no regulatory/actuarial consistency claim—when any of the following holds:

- Silent omission of coverage triggers remains unmitigated.  
- Override audit is missing, incomplete, or not immutable/exportable.  
- Coding drift is unreconciled to actuarial sampling.

Operationalizing those kills for mid-market P&C buyers in this pack:

- If UI does not enforce required human override → assistive-only (S1).  
- If override reason capture stays near ~50% → assistive-only (S4).  
- If reserve variance widens while cycle time improves → refuse consistency language (S2).  
- If peril-code sampling fails → refuse consistency language (S2 Claim B).  

“AI claims acceleration” copy is allowable only as **assistive draft speed** under Tier 1, with explicit denial of consistency certification. It becomes false advertising relative to this pack’s compliance question if it implies regulatory or actuarial consistency without Tier-2 controls.

## 6. Recommended posture through 2027

1. **Claims ops:** enable LLM FNOL drafts as Tier-1 assist; hard-gate acceptance on checklist pass or documented human confirm; enforce override in UI before queue advancement.  
2. **Compliance:** prohibit consistency / regulatory reliance language in vendor and internal marketing until Tier-2 controls and sampling pass.  
3. **Actuarial:** own peril-code and reserve-variance sampling; hold stop authority when drift or variance worsens despite cycle-time gains (S2 pattern).  
4. **Vendor management:** contractually separate “draft assist” from any consistency warranty; require audit-log export and UI enforcement as acceptance criteria.  
5. **Expansion:** do not generalize auto-LOB pilot results (S4) to other LOBs or regulator-facing processes without new evidence.


### 6.1 Claims desk operating rules (compact)

For day-to-day FNOL handling under this pack: (1) treat every LLM summary as editable draft until checklist pass or documented human confirm on coverage triggers; (2) block queue advancement if override UI is not completed with a reason code; (3) route peril-code changes and reserve-relevant narrative edits to actuarial sampling queues; (4) keep “acceleration” dashboards separate from consistency dashboards so an 8% cycle-time gain cannot be mistaken for actuarial approval (S2). Train adjusters that fluent prose is not evidence of completeness—Claim A’s omitted prior-damage language is the teaching example. These rules implement Tier-1 honesty while Tier-2 controls are built; they do not create a consistency claim by themselves.

## 7. What would change the judgment

- UI-enforced override with immutable, high-completeness reason codes (repairing S1/S4).  
- Coverage-trigger completeness such that manual omission catches fall to negligible levels under sampling (improving on S4’s +6pp).  
- Actuarial sampling showing stable or improved peril coding and reserve variance alongside any cycle-time gain (reversing S2’s refuse posture).  
- Multi-LOB, regulator-aware evidence beyond the single auto book (S4 limit).

Until then, keep consistency claims killed and marketing assistive-only.

## 8. Limitations

All evidence is **synthetic** (S1–S4). No live web retrieval and **no independent review** were performed. Figures (8% cycle-time, 71% adoption, 22% full rewrite, 48% override reasons, 81% auto-pass, +6pp manual omission catch) are pack-internal and mid-market auto-LOB scoped. This memo is not legal or actuarial advice, not a claims-chatbot bake-off, and not a regulatory filing standard beyond the pack’s stated bar.

## Source ledger (synthetic)

| ID | Role in this memo |
| --- | --- |
| S1 | Pilot charter; acceleration marketing vs consistency question; omission risk; override not UI-enforced |
| S2 | Dual review cases A–C; +8% cycle / worse reserves; actuarial refuses consistency language |
| S3 | Draft-assist vs consistency-supporting tiers; kill criteria → assistive-only |
| S4 | 60-day dashboard metrics; single auto LOB; not regulator-facing |
