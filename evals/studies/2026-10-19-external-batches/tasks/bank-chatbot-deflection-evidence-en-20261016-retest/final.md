# Bank retail chatbot deflection: does no-handoff evidence support replacing tier-1 human handling?

Audience: retail-bank digital CX and model-risk / compliance. Using only the synthetic HarborAssist pilot report, the internal risk memo, and the ops queue extract, **the judgment is that the vendor’s 62% “deflection” figure does not support authorizing replacement of tier-1 human handling on the basis of no-handoff rates.** It can support, at most, continuing a bounded pilot with remetered success definitions. All materials are synthetic evaluation fixtures; there was no independent review. This run is an original-condition retest on Toolkit 1.1.0 (Day-1 baseline was 1.0.0).

## What “62% deflection” actually measures

The vendor pilot window ran from 2026-02-01 to 2026-04-30 in one retail region. The headline metric is that 62% of chatbot sessions ended without a human handoff. Fine print in the same pack shows why the headline is not a replacement case. The denominator is sessions that opened the chatbot widget; customers who dialed the phone queue directly never enter it. “Deflection” counts sessions with no handoff-button click, including users who abandoned after a wrong answer. There is no linkage to formal complaint tickets closed with customer confirmation. During weeks 3–5, escalation to a human was disabled for password-reset intents as an ops experiment, which inflates deflection for that intent cluster.

In short, the metric mixes unresolved abandonment, experimentally blocked escalation, and a self-selected widget population. Treating it as proof that tier-1 labor can be removed confuses “did not click handoff” with “issue resolved under an approved taxonomy.” Model risk and compliance should refuse any expansion memo that equates no-handoff rate with approved automation of retail handling.

## Counter-signals already in the pilot region

The same vendor-adjacent ops extract notes that formal complaints tagged “bot wrong answer” rose 14% versus the prior quarter in the pilot region. CSAT for chatbot-resolved sessions was 3.1/5 against 4.2/5 for human tier-1 (ops-stated n≈1,104 chatbot and 890 human; the vendor slide did not disclose n cleanly). These are not definitive causal proofs that the bot caused the complaint rise, but they are material counter-evidence against a replacement narrative that presents deflection as customer-beneficial automation.

The internal risk memo responds with gates rather than enthusiasm: redefine deflection as confirmed resolution or ticket auto-closure under an approved taxonomy; keep regulatory-exposed intents (collections, hardship, fraud dispute) human-first until dual-control QA meets a high monthly bar; require written risk approval and a kill switch before any A/B that disables escalation. A secondary credit-union citation with ~55% deflection and stable complaints is explicitly flagged as non-comparable because it used confirmed-resolution denominators and kept fraud intents human-only. Borrowing that 55% as comfort for HarborAssist’s 62% would repeat the metric error.

## Coverage: even a “fixed” 62% would not map to all tier-1 demand

Ops weekly averages in the pilot region show about 18,400 phone tier-1 contacts, 9,700 chatbot sessions, 3,680 chatbot-to-human handoffs, and 11,200 direct phone contacts that never opened the bot. The vendor denominator therefore excludes a large phone-first population. Even if widget-session deflection were remetered and improved, replacing tier-1 still requires a plan for customers who never touch the widget—staffing, divert messaging, and complaint handling included. The 62% number does not travel to “all tier-1.”

Abandonment patterns reinforce caution: phone abandon is about 6.2%, while roughly 21% of chatbot sessions show no-handoff and no confirmation—the bucket vendor marketing labels deflected. Without confirmed-resolution coding, that bucket is not a labor-savings ledger entry for CX or a clean control for model-risk attestation.

## Recommendation and conditions that would change it

Do not authorize replacing tier-1 human handling on the strength of the 62% no-handoff claim. Keep the pilot bounded. Immediately remetric to confirmed resolution (or approved auto-closure), restore escalation for experiments that disabled it, and report complaint and CSAT trends beside any automation rate. Regulatory intents stay human-first until the risk memo’s QA gate is met with evidence.

Change the recommendation only if, after remetering, deflection-as-confirmed-resolution is stable across intents, complaint rates tagged to bot errors are flat or down, CSAT gaps narrow without suppressing escalation, and the staffing model explicitly covers the direct-phone population outside the widget denominator. A clean vendor slide that still uses no-handoff click as success should not count as satisfying those conditions.

## Limitations

Synthetic sources only; single region; incomplete public n on some vendor slides; no independent review. This memo retests evidence discipline on banking-chatbot deflection claims for Toolkit version regression without inventing live-web facts. Production decisions need the bank’s own ticket taxonomy and complaint ledger, not this fixture pack.
