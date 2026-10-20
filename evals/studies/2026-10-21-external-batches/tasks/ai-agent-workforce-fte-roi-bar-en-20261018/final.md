# AI Agent Workforce Claims: Evidence Bar for FTE Replacement ROI Through 2027

**Audience:** Enterprise IT/ops buyers and CFO / workforce-planning sponsors  
**Materials:** Synthetic source pack S1–S4 only (disclosed). No live web retrieval. No independent review was performed.  
**Question:** For enterprise buyers evaluating “AI agent workforce” / digital-employee vendors, does evidence of demo or pilot task completion support production claims of FTE replacement / headcount ROI through 2027—or must buyers treat headcount-replacement claims as a false proposition without workflow ownership, exception handling, and auditable override trails?

---

## 1. Judgment in brief

**Demo or pilot task-completion rates do not support production FTE-replacement or headcount-ROI claims through 2027** on the evidence in this pack. Vendor materials advertise “digital employees,” pilot task-completion **≥90%**, and a slide that claims **replace 12 FTEs in G&A within 9 months**, backed by a recorded demo and a six-week pilot scorecard (S1). Internal notes in the same pack show the pilot was pre-scoped, exceptions routed to an unnamed human queue, no production end-to-end SLA ownership, and a non-exportable override trail—plus an FTE model that assumed zero rework and ignored exception-handling labor (S1).

Buyer evaluation worksheets and a CFO memo align on a three-tier bar (S2, S3): (1) demo/pilot completion is necessary but not sufficient; (2) production ownership requires a named workflow owner, exception SOP, and auditable overrides; (3) FTE replacement is only after sustained production metrics **net of exception labor**. A single-buyer 90-day shadow shows autonomous close at **47%**, an exception queue about **0.4 FTE**, and override reason completeness at only **62%** (S4). Ops also found a shadow Slack exception channel staffing about **2.5 FTE** during the pilot that vendor ROI excluded (S2).

**Kill rule:** missing workflow ownership, exception handling costed in, or auditable override trails → treat headcount-replacement marketing as a **false proposition** through 2027 (S3). Buyers may still fund assistive or partial-automation pilots; they should not book headcount savings from demo/pilot completion alone.

## 2. Evidence tiers (what each layer can and cannot claim)

### Tier 1 — Demo / pilot completion

S1’s external claims sit entirely here: scripted demo workflows (ticket triage, invoice extraction), pilot task-completion ≥90%, ROI slide with a 12-FTE / 9-month narrative, proof points limited to recorded demo plus a six-week scorecard. S2 maps the buyer gap cleanly: demo completion is not production ownership; a 91% pilot rate on a curated set hides human exceptions; FTE ROI spreadsheets lack workflow owners and audit trails; “human-in-the-loop available” is not an immutable exportable log.

Tier 1 evidence is useful for **capability screening**. It is not an accounting basis for headcount plans. The pack’s internal notes (S1) already admit pre-scoping and unnamed exception routing—exactly the failure mode Tier 1 marketing papers over.

### Tier 2 — Production ownership

S3 defines the minimum production bar: named workflow owner, exception SOP, and auditable overrides. Until those exist, the buyer—not the vendor—still owns SLA risk and exception labor. S4’s shadow deployment illustrates the gap: only 47% of tickets closed autonomously; the remainder were human-touched; exception median handle time was 11 minutes at roughly 0.4 FTE equivalent; 62% of human edits lacked reason codes. That is production-adjacent observation, not Tier-3 FTE proof—and it is a single unaudited deployment with vendor promo discounts in the ROI (S4).

### Tier 3 — FTE replacement / headcount ROI

Only after sustained production metrics **net of exception labor** (S3). The vendor’s 12-FTE claim fails this tier on pack evidence: it assumed zero rework, ignored exception labor (S1), and excluded a ~2.5 FTE shadow queue found by ops (S2). Net of disclosed exception labor alone, the pilot’s implied “replacement” is not a clean headcount cut; booking it as G&A savings would misstate workforce cost.

## 3. ROI claim mapping (vendor slide → buyer ledger)

| Vendor claim layer (S1/S2) | Pack evidence | Buyer ledger treatment |
| --- | --- | --- |
| Demo completion / video | Scripted run (S1, S2) | Screening only; $0 headcount savings |
| Pilot task rate ≥90% / 91% curated | Pre-scoped; hidden exceptions (S1, S2) | Quality signal under curation; not FTE |
| “Replace 12 FTEs in 9 months” | Assumed zero rework; ignored exception labor (S1) | Reject as production ROI without Tier 2–3 |
| Human-in-loop “available” | No immutable exportable override log (S1, S2) | Control gap; compliance/ops risk |
| Shadow exception Slack ~2.5 FTE | Excluded from vendor ROI (S2) | Must be costed into any net ROI |
| 90-day: 47% autonomous; 0.4 FTE exceptions; 62% override completeness | Single buyer, not audited, promo fees in ROI (S4) | Partial automation metrics; not headcount cut |

The mapping’s rule of thumb: **move right on the table only when evidence moves down the tier stack.** Skipping from Tier 1 to Tier 3 is how false FTE propositions enter workforce plans.

## 4. Counter-evidence buyers must weight

1. **Hidden human exception queues.** Ops’ shadow Slack channel (~2.5 FTE) during the pilot was excluded from vendor ROI (S2). Any headcount model that omits parallel human queues invents savings.  
2. **Pre-scoped pilots.** S1 admits tasks were pre-scoped; high completion rates on curated sets do not transfer to messy production taxonomies.  
3. **Override trail gaps.** Non-exportable trails (S1) and 62% missing reason codes in shadow (S4) block auditability required for production ownership (S3).  
4. **Promo-distorted ROI.** S4 notes vendor fee discounts inside the ROI; finance should recompute at list or contracted run-rate.  
5. **Single-deployment limits.** S4 is one buyer, unaudited—useful as a cautionary measurement, not a universal FTE coefficient.

None of these say agents never reduce labor. They say **labor reduction must be measured net of exceptions under owned workflows**, not inferred from demo scores.

## 5. Kill criteria for FTE-replacement marketing (through 2027)

Per S3, treat headcount-replacement claims as a **false proposition** when any of the following is missing:

- **Workflow ownership** — named production owner and end-to-end SLA (absent in S1).  
- **Exception handling costed in** — SOP plus labor in the ROI denominator (contradicted by S1 assumptions and S2’s 2.5 FTE shadow queue; S4’s 0.4 FTE exception load shows residual work remains).  
- **Auditable override trails** — immutable, customer-exportable logs with reason codes (failed by S1 non-exportable trail and S4’s 62% completeness).

Additional buyer kill switches consistent with the pack:

- Vendor ROI that assumes zero rework or excludes known exception channels.  
- Pilot evidence limited to curated task sets without a production shadow net of human touch.  
- “Human-in-the-loop” language without exportable override audit.

If kill criteria fire, buyers may still proceed on an **assistive / co-pilot** framing with explicit non-replacement language. They should not approve workforce plans that subtract FTEs from the vendor’s Tier-1 slide.

## 6. Practical buyer posture through 2027

1. **Contract language:** ban or tightly condition “FTE replacement,” “digital employee,” and headcount-ROI warranties unless Tier-2 artifacts are deliverables (owner matrix, exception SOP, override export).  
2. **Measurement:** require a production shadow (or equivalent) reporting autonomous close rate, human-touched share, exception FTE-equivalent, and override completeness—net of promo pricing (pattern in S4).  
3. **Finance gate:** CFO sponsors accept savings only after Tier-3 evidence; Tier-1 pilots capitalize as learning cost, not headcount reduction.  
4. **Ops gate:** IT/ops refuse production cutover without named workflow ownership and exception SOP (S3).  
5. **Revisit trigger:** if a vendor later shows sustained net-of-exception metrics with exportable overrides under a named owner, re-open Tier-3 discussion; until then, keep replacement claims killed.


### 6.1 Procurement checklist (compact)

Before any pilot is labeled “workforce replacement ready,” require written answers to: Who owns the production workflow and SLA? Where is the exception SOP, and what FTE-equivalent did the last thirty days of exceptions consume? Can the buyer export an immutable override log with reason codes for every human edit? Does the ROI spreadsheet include shadow queues (pattern: ~2.5 FTE Slack channel in S2) and exclude promotional fee discounts (S4)? If any answer is missing, keep the engagement in Tier 1 learning mode and strike FTE-replacement language from SOWs and executive decks. This checklist is procedural hygiene drawn from the pack—not an industry standard beyond S1–S4.

## 7. What would change the judgment

- Sustained production metrics with autonomous close high enough that **exception labor is costed and still nets documented FTE reduction**, under a named owner (Tier 3 as defined in S3).  
- Immutable, customer-exportable override trails with high reason-code completeness (repairing S1/S4 gaps).  
- Vendor ROI restated to include shadow exception queues like the ~2.5 FTE channel (S2) and to remove promo-fee distortion (S4).  
- Pilots that are not pre-scoped curated sets, with completion measured on production-like distributions (addressing S1).

Absent those, the pack’s kill criteria remain binding through 2027.

## 8. Limitations

All evidence is **synthetic** (S1–S4). No live web retrieval and **no independent review** were performed. Figures (90%/91% pilot rates, 12 FTE / 9 months, ~2.5 FTE shadow queue, 47% autonomous close, 0.4 FTE exceptions, 62% override completeness, 11-minute median handle time) are pack-internal. S4 is one deployment and not audited. This memo is not a vendor bake-off, not HR/legal advice, and not a forecast of agent labor markets beyond the pack’s procurement bar.

## Source ledger (synthetic)

| ID | Role in this memo |
| --- | --- |
| S1 | Vendor pitch: ≥90% pilot, 12 FTE claim; internal: pre-scope, unnamed queue, no SLA ownership, non-exportable overrides, zero-rework ROI |
| S2 | Buyer worksheet gaps; shadow Slack ~2.5 FTE excluded from vendor ROI |
| S3 | Three evidence tiers; kill criteria for FTE-replacement marketing |
| S4 | 90-day shadow metrics; promo-discount and single-deployment limits |
