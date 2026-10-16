# Private-credit on-chain settlement pilots: operational and disclosure risks for LP reporting (Full original-condition retest)

Audience: private-credit GP operations/compliance and LP due-diligence readers. This retest reuses the synthetic Northbridge Credit IV pilot charter, compliance issues list, LP questionnaire excerpt, and 90-day metrics dashboard from the 2026-10-14 pack without changing the prompt or sources. The workflow profile is Full with a declared independent-review requirement. **The judgment remains that on-chain settlement can be described to LPs as an operational reconciliation experiment with material exception and oracle risks—not as real-time NAV truth, not as a change to LPA economic rights, and not as proof that NAV disputes disappear.** Clean-deal toil may fall, but disclosure complexity rises until oracle SLA, failover, and off-chain approval attachment mature. Synthetic materials. In this execution environment no independent reviewer backend is configured; a same-session critical review is recorded separately and must not be labelled independent.

## What the pilot is—and explicitly is not

The charter limits scope to intra-fund interest and fee settlements among SPVs on a permissioned chain. Investor capital calls are out of scope. Oracles combine bank cash confirmation with a NAV tape lagged T+2. Custody uses HSM-backed chain keys with dual control; legal title remains with the traditional administrator. Stated goals are faster reconciliation and richer timestamps for LP reporting narrative. Explicit non-goals include public-chain settlement, tokenized LP interests, and automatic waterfall changes without counsel sign-off.

That boundary is the first disclosure control. Marketing language that collapses the pilot into “we are on-chain now” invites LPs to infer tokenization, altered redemption rights, or live NAV—none of which the charter supports. Counsel’s questionnaire answers state that LPA economic rights do not change in the pilot and that reporting should annotate activity as an operational experiment. Positions are not tokenized. Full-profile discipline adds an insistence that non-goals appear in the same LP pack as any efficiency claim, not in a footnote engineers forget to export.

## Risk map that actually touches LP reporting

Compliance’s issues list is the actionable core for LP-facing language.

Valuation timing mismatch: on-chain settlement marks at oracle time, while fair-value policy uses administrator NAV as-of month-end. Dual marks without a reconciliation narrative confuse LPs and examiners. Operational key risk: loss or compromise of HSM roles could halt settlements; the contingency path is still “email the admin,” and a full failover drill is not evidenced as completed. Oracle dependency: stale bank cash confirmation can show settled on-chain while cash has not moved, or the reverse; the pilot recorded a six-hour delay and a duplicate confirmation caught manually. Marketing overclaim: a draft that said “real-time on-chain NAV” was struck by compliance—correctly—because NAV remains admin-controlled. Audit-trail export: chain logs cover on-chain events but omit off-chain legal approvals unless manually attached, leaving an exam-readiness gap.

A peer fund’s public blog claim that “on-chain eliminates NAV disputes” is explicitly rejected by Northbridge compliance as unsupported for private credit with lagged oracles. LPs reading that blog should not treat it as transferable evidence. Relative to a Lite pass that already named these risks, Full review pressure should ask whether the report keeps admin NAV authority visible beside every operational metric—an overclaim failure mode Day-1 mechanical checks cannot certify.

## What the 90-day metrics say about efficiency

Dashboard extract: 128 settlements attempted; 109 auto-matched; 19 manual exceptions. Exception roots: oracle lag 8, metadata mismatch 6, key-ceremony delay 3, other 2. Versus the baseline spreadsheet process, time-to-reconcile improved about 28% median on clean deals but worsened about 40% on exception deals because new tooling lengthened triage. Capital-account methodology did not change. Ops’ own note is the right headline for LPs: the pilot reduces clean-deal toil but increases disclosure complexity; it is not yet a net win for LP reporting clarity.

Efficiency theater that quotes only the −28% clean-deal figure without the +40% exception path and without remaining open oracle incidents would be a disclosure failure even if technically “true.” Full delivery should treat asymmetric metric quotation as a content defect, not as optional polish.

## Recommendations for LP reporting and DD answers

1. Describe the initiative as a permissioned-chain operational reconciliation pilot for intra-fund settlements, with admin NAV remaining authoritative for official reporting.
2. Use dual presentation when chain marks appear: oracle-timed operational mark versus admin month-end NAV, plus an explicit bridge. Never market “real-time on-chain NAV.”
3. Publish exception rates, oracle incident counts, and kill-switch/failover status in the same reporting pack that mentions the pilot.
4. Attach off-chain legal approvals to the exportable audit bundle; chain completeness alone is insufficient.
5. State non-goals clearly: no LP tokenization, no capital-call settlement on chain in this phase, no LPA economic-rights change.
6. Reject peer slogans that on-chain eliminates NAV disputes under lagged oracles.

Change toward a stronger claim (“production settlement layer”) only if oracle SLA is proven under drill, failover is tested, exception rates fall without hiding issues, and counsel rewrites the reporting basis with exam-ready trails. Until then, stronger claims are not supported.

## Counter-evidence and humility

Counter-evidence includes the genuine −28% clean-deal improvement and the legitimate desire for timestamped audit narratives. Those points justify continued piloting, not expansive LP marketing. Single-fund, 90-day synthetic metrics cannot generalize to private credit as an asset class. Contingency processes remain partially untested. This memo does not assess tax, regulatory capital, or jurisdiction-specific token rules because the charter excluded tokenization.

## Building an LP appendix that survives examination

An exam-oriented appendix should walk a quarter-end in order. First, list every on-chain settlement in the period with oracle timestamps and counterpart SPVs. Second, map each to cash-movement confirmations and flag lags or duplicates, including the known six-hour delay pattern as a monitored risk rather than a hidden incident. Third, show the admin NAV table used for official fair value and a reconciliation bridge to any operational marks an LP might see in dashboards. Fourth, inventory HSM role holders, dual-control events, and whether a failover drill occurred in the period (if not, say so). Fifth, attach counsel sign-offs for waterfall-affecting decisions so off-chain approvals are not merely asserted.

This appendix structure follows directly from the compliance issues list and the metrics dashboard; it does not invent new control objectives. It also prevents a common failure mode: engineering teams demo a live chain explorer to LPs while finance still closes books on admin NAV, leaving sophisticated LPs to notice the seam before management explains it. Transparency about the seam is safer than glossy unity language.

For DD questionnaires, short answers beat slogans. “Are you tokenized?” → “No.” “Does this change my rights?” → “No LPA economic-rights change in pilot; activity annotated as operational experiment.” “What breaks?” → “Settlement halt and manual catch-up; mis-statement risk if reports quote chain marks without admin NAV bridge; mitigations include dual NAV disclosure, kill switch, monthly reconciliations.” Those answers already exist in the synthetic questionnaire excerpt and should remain stable until charter scope changes.

## Board and LP meeting choreography

When the pilot is raised in an LPAC or annual meeting, sequencing matters as much as vocabulary. Open with charter scope and non-goals so tokenization rumors die early. Present the 109/128 auto-match rate next to the 19 exceptions and their root causes; do not lead with the −28% clean-deal headline. Show one worked example of dual NAV bridging for a single SPV settlement, including how a six-hour oracle lag would have appeared. State failover drill status honestly. Close with the disclosure commitments: admin NAV authoritative, no real-time on-chain NAV marketing, off-chain approvals attached, kill switch criteria.

That choreography is deliberately boring. Boring is the point. Private-credit LPs are not asking for a chain demo; they are asking whether operational experiments create silent valuation or control failures. Compliance already struck the “real-time on-chain NAV” phrase. Ops already admitted exception paths are slower. Counsel already denied LPA rights changes. The reporting task is to keep those three truths visible in the same room rather than letting investor-relations polish reassemble them into a transformation story.

If a competitor markets elimination of NAV disputes, respond with the lagged-oracle fact pattern rather than with reciprocal hype. If an LP asks whether capital accounts will move on-chain next, answer with the charter non-goal and the conditions listed earlier for any production claim. If metrics improve for two consecutive quarters on exceptions and drills, bring back a scoped proposal—not a brand refresh. Until then, the accurate LP sentence remains: permissioned-chain reconciliation pilot; useful on clean deals; disclosure-heavy on exceptions; admin NAV still governs official truth.

## Evidence bounds specific to this Full retest

Supported by the pack and safe for LP language: pilot scope and non-goals; admin NAV authority; presence of oracle lag and duplicate-confirmation incidents; exception counts and asymmetric time-to-reconcile; counsel statements on LPA rights and non-tokenization; rejection of the peer “eliminates NAV disputes” slogan for lagged-oracle private credit.

Not supported and must not be claimed: production readiness; real-time NAV; elimination of valuation disputes; completed full failover proof; exam-ready trails without manual off-chain attachments; generalization beyond one synthetic fund-quarter.

The Full original-condition change versus Day-1 Lite is the review tier, not a license to invent stronger operational success. If formal review is incomplete because no independent backend is available, that incompleteness itself is a delivery fact for the evaluation brief: do not silently relabel degraded same-session review as independent.



## Interim kill / pause criteria grounded in the pack

The Day-1 Lite memo and early Full draft mentioned a kill switch without numeric interim triggers. Using only this pack, treat the following as **interim** ops/compliance pause triggers for escalating LP marketing language (not as LPA amendments): (a) manual exception rate above the observed 19/128 (~15%) for a subsequent measurement window without root-cause burn-down; (b) any repeat of multi-hour oracle lag or duplicate cash confirmation without a documented detection control; (c) continued absence of a full HSM failover drill while LP materials increase on-chain branding. Hitting any trigger pauses stronger production claims and requires the dual-NAV appendix before the next LP touchpoint. These triggers are interpretations of S2–S4, labelled as interim until counsel/ops ratify.

## Limitations

Synthetic fixtures; no live web; independent reviewer backend unavailable in this run—same-session review only, not independent. Replace with fund-specific admin policies before sending language to LPs. Finance/tech depth for this confirmed task remains disclosure discipline under operational experimentation—not a crypto product pitch. Keep production records, checklist status, and local paths out of the LP letter body; reader-facing prose should stay decisions, risks, metrics, and disclosure commitments.

Finally, GPs tempted to compete on “on-chain” branding should note the metrics paradox: automation helps when it works and hurts cycle time when it fails, while disclosure obligations expand either way. That is a reason to keep pilots narrow and language narrower—not a reason to avoid tooling. The recommendation stands: operational experiment framing, authoritative admin NAV, explicit exceptions, no real-time NAV marketing, no borrowed peer claims about ending disputes under lagged oracles. Until oracle SLA drills pass, failover is evidenced, exception rates fall without concealment, and counsel-approved trail exports exist, stronger production language remains unsupported by this synthetic pack.

## Worked disclosure sentences for the quarterly letter

Use these as constrained templates, not slogans. “During the quarter the Fund continued a permissioned-chain pilot for intra-fund interest and fee settlements among SPVs; investor capital calls were not in scope.” “Official fair value continues to follow administrator NAV; any operational chain marks are presented only with an explicit bridge and are not real-time NAV.” “Of 128 pilot settlements, 109 auto-matched and 19 required manual exception handling; oracle lag and metadata mismatch were the leading exception roots.” “A full failover drill of HSM role loss has not been completed; contingency remains manual coordination with the administrator.” “LPA economic rights are unchanged; interests are not tokenized; peer claims that on-chain settlement eliminates NAV disputes are not adopted for lagged-oracle private credit.”

Each sentence is traceable to the charter, compliance list, metrics dashboard, or questionnaire excerpt. If IR proposes deleting the exception sentence while keeping the auto-match sentence, compliance should treat that edit as an overclaim even when every retained clause is literally true. Full review is meant to catch exactly that class of omission. Because this run cannot invoke a separate independent reviewer service, the evaluation record must show same-session review with degraded strength rather than inventing an independent PASS.
