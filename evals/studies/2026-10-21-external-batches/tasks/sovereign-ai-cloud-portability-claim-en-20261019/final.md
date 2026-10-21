# Sovereignty + open-weight portability: procurement evidence bar through 2027

**Audience:** Enterprise cloud procurement, CISO, and AI platform owners  
**Evidence standard:** Synthetic source pack only (S1–S4). All materials are fictional test evidence. No live web research. No independent review was performed. This memo is not legal advice and is not a cloud SKU bake-off.

## 1. Judgment

Enterprise buyers should **not** accept “sovereignty + open-weight model-portability” as a **jointly true** marketing proposition through 2027 unless three portable-ops controls exist together and have survived **customer-owned** migration drills: (1) an **exportable toolchain** that is not dependent on proprietary tool/API glue; (2) a **portable eval harness** that customers can export and reproduce—not a marketing PDF that differs from production; and (3) an **auditable residency kill-switch** with customer-readable immutable logs—not a ticket queue. On the synthetic pack, the vendor’s public proof points (region map, open-weight SKU list, portable-eval one-pager) fail against internal notes and a buyer worksheet: open-weight inference still rides proprietary glue, the kill-switch is ticket-based, and the marketed harness is not the exportable harness (S1–S3). A ninety-day one-buyer shadow reinforces the gap: 38% cross-region config export without vendor professional services, 4.5-hour median kill-switch ticket latency without immutable customer logs, and 9–14 percentage-point score delta between marketing and production harnesses (S4). **Missing any of the three portable-ops controls → treat the joint claim as a false proposition through 2027** (S3).

## 2. Separating three claim layers

Procurement must score layers independently before testing the joint claim (S2, S3).

**Layer A — Residency / sovereignty marketing.** Region maps and MSA residency clauses are necessary. They are not sufficient for a sovereignty claim that implies customer-controllable data-location enforcement. The buyer worksheet flags that the kill-switch is not customer-auditable (S2). Internal vendor notes confirm ticket-based operation (S1). Residency marketing without an auditable kill-switch is a compliance story, not an operational sovereignty control.

**Layer B — Open-weight SKU presence.** Listing open-weight model IDs is evidence of model *choice*, not of *portability*. Internal notes state that open-weight inference still routes through proprietary tool/API glue and that toolchain export is incomplete (S1). The worksheet records the same gap (S2). Buyers who equate “open weights on the price sheet” with “we can leave with our stack” are conflating license posture with operational exit rights.

**Layer C — Portability.** True portability requires an exportable toolchain, a reproducible eval harness the customer owns, and migration paths that do not mandate vendor professional services for routine moves (S3). The PoC showed the same open-weight model ID with incompatible tool schemas across regions; migrating a RAG pipeline required vendor PS—not customer self-port (S2). That is API lock-in behind an open-weight label.

**Joint claim.** Marketing slides that assert Layers A+B+C together without a joint evidence pack through 2027 fail the platform-owner tier model (S2, S3). Joint truth is not the sum of three brochures; it is sustained customer-owned drills that exercise all three controls on the same delivery path.

## 3. Evidence tiers (acceptance ladder)

Use the platform-owner memo’s three tiers as the procurement ladder (S3):

1. **Residency marketing** — necessary, not sufficient for sovereignty claims. Accept as *intent* and contractual geography only.
2. **Portable open-weight ops** — requires exportable toolchain, portable eval harness, and auditable residency kill-switches. Accept as *technical eligibility* only when buyers can run export and kill drills without vendor mediation.
3. **Joint claim through 2027** — only after sustained customer-owned migration drills that keep residency enforcement and model/tool portability intact across regions and time.

Do not skip from Tier 1 marketing to Tier 3 joint acceptance because an RFP response includes an open-weight SKU list. Tier gates are sequential for the joint claim even if individual products may be bought for narrower uses (for example, residency-only inference with no portability promise).

## 4. Counter-evidence already in the pack

**Proprietary glue behind open weights.** Vendor internal notes and the CISO worksheet agree: tool/API glue remains proprietary; toolchain export is incomplete (S1, S2). Open-weight model IDs therefore do not imply portable serving stacks.

**Non-exportable “portable eval.”** Marketing uses a portable-eval one-pager / PDF harness that is not the customer-exportable harness and is not reproducible against production (S1, S2). Shadow metrics measured a 9–14pp score delta on the same prompts between marketing and production harnesses (S4). Using the marketing harness as acceptance evidence is a false positive risk for model quality and for portability claims.

**Ticket-based kill-switch.** Kill-switch drills showed median 4.5 hours of ticket latency and no customer-readable immutable log (S4). Combined with the worksheet gap (“not customer-auditable”) and internal “ticket-based” note (S1, S2), residency enforcement is operator-mediated, not buyer-verifiable in real time.

**Self-port failure in PoC.** Same model ID, incompatible tool schemas across regions; RAG migration needed vendor PS (S2). Cross-region config export succeeded only 38% of the time without vendor PS in the shadow period (S4). These are existence proofs of lock-in mechanics, not a multi-tenant rate—but they are enough to refuse the joint marketing claim.

**TCO distortion.** Promo credits appeared in TCO slides; metrics were not audited (S4). Price comparisons that embed credits cannot validate long-run portability economics.

## 5. Kill criteria through 2027

Adopt the platform-owner kill line as a hard procurement rule (S3):

> If portable eval harnesses, exportable toolchains, **or** auditable residency kill-switches are missing → treat “sovereignty + model-portability” as a **false proposition** through 2027.

Operationalize as follows:

- **Kill joint RFP language** that asserts both sovereignty and model-portability as simultaneously proven.
- **Allow narrow buys** only with explicit carve-outs: e.g., residency-constrained inference *without* portability warranties, or open-weight experimentation *without* sovereignty marketing—never the joint claim.
- **Re-open joint claim** only after documented customer-owned drills: (a) export toolchain and re-instantiate serving in a second region without vendor PS; (b) run the customer harness with score parity within an agreed band versus production; (c) trigger residency kill and obtain an immutable customer-readable log within an agreed SLA (hours measured in the shadow were 4.5 median—buyers should set a stricter contractual bar).
- **Ongoing kill:** if any quarterly drill fails, or if glue/schemas diverge again across regions, suspend joint-claim language in renewals even if prior drills passed.

## 6. Joint-claim mapping for procurement packets

| Marketing assertion | Minimum evidence | Pack status |
| --- | --- | --- |
| Residency-first / sovereign regions | MSA geography + customer-auditable kill-switch with immutable logs | Region map present; kill-switch ticket-based / not auditable (S1, S2, S4) |
| Open-weight model choice | SKU list + exportable serving/tool schemas | SKU list present; glue proprietary; schemas incompatible across regions (S1, S2) |
| Portable eval | Customer-exportable harness = production harness | Marketing harness ≠ production; 9–14pp delta (S1, S4) |
| Joint sovereignty + portability through 2027 | Sustained customer-owned migration drills covering all three controls | No joint evidence pack; PoC required vendor PS (S2, S3) |

Procurement should attach this table to the scorecard and refuse “jointly true” checkmarks until the right-hand column flips with buyer-held artifacts—not vendor PDFs.

## 7. Recommended buyer actions (next two quarters)

1. **Rewrite acceptance tests** around export, harness parity, and kill-switch auditability; stop accepting region maps and SKU lists as joint proof.
2. **Contract for drill rights:** quarterly customer-owned migration and kill drills; failure triggers fee credits and suspension of joint marketing references in the account.
3. **Separate commercial SKUs** in the MSA: residency SKU vs portable-ops SKU; forbid bundling language that implies joint achievement without Tier-3 evidence.
4. **Shadow metrics discipline:** exclude promo credits from portability TCO; require immutable logs for kill events; treat single-site 38% export success as a red flag, not a baseline to celebrate.
5. **CISO veto:** any production workload that needs both residency enforcement and future exit/portability inherits the joint-claim kill until drills pass.


## 7a. What “good enough” looks like in contracts

A residency MSA clause plus an open-weight appendix is not a portability warranty. Contract language should require (i) machine-readable export of tool schemas and serving configs; (ii) delivery of the production eval harness as a runnable customer artifact with version pins; (iii) kill-switch events written to a customer-held immutable log within a stated minute/hour SLA; and (iv) the right to run quarterly migration drills without professional-services fees counting as “success.” Until those clauses exist and drills pass, procurement should score the joint claim as **not proven** regardless of region maps or SKU aesthetics.

## 8. Limitations

Sources S1–S4 are **synthetic**. Shadow metrics are one unaudited deployment with promo credits in TCO slides (S4). The PoC is a single pipeline anecdote (S2). Kill criteria and tiers are judgments from a synthetic platform memo, not a regulator’s rulebook (S3). No multi-vendor survey and **no independent review** were performed. Do not generalize failure rates beyond this pack; do treat the *structure* of the gaps (glue, harness mismatch, ticket kill-switch) as sufficient to refuse the joint marketing claim through 2027 for offerings that match this pattern.

## Source ledger (synthetic)

| ID | Title | Role |
| --- | --- | --- |
| S1 | Sovereign / residency-first AI cloud pitch (2026-06) | External joint claim vs internal glue/kill/harness gaps |
| S2 | Enterprise procurement / CISO worksheet (2026-07) | Layer gaps; PoC schema lock-in |
| S3 | AI platform owner memo (2026-08) | Evidence tiers; kill criteria |
| S4 | 90-day residency/portability shadow metrics (2026-09) | Export %, kill latency, harness delta; limitations |

---

*Lite profile under Research Toolkit 1.3.1. Tool checklist pass is not semantic certification.*
