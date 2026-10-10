# Claims and evidence limits

[Claim registry CSV](data/claims_registry.csv) · [Source records](sources.md) · [Report](report.md)

## C01 — Choose an execution route per business operation, accounting for coverage, authorization, verification and recovery.

Type: author judgment.

Sources: S01, S04, S08, S11.

Counter-evidence or counterexample: A single route can be sufficient for a small complete workflow.

Limit: This is a design inference, not a measured ranking.

## C02 — Stripe API v1 response replay and key retention do not give unlimited retry protection.

Type: fact.

Sources: S01, S02.

Counter-evidence or counterexample: API v2 has different behavior.

Limit: Other providers and endpoints have their own contracts.

## C03 — Stripe API v2 has a 30-day replay scope and can retry failed work while preserving successful work.

Type: source claim.

Sources: S03.

Counter-evidence or counterexample: Some requests cannot be successfully replayed.

Limit: Applies only within documented same-key/API/account-or-sandbox conditions.

## C04 — An actionability-checked browser click does not by itself verify the application business state.

Type: interpretation.

Sources: S04, S11.

Counter-evidence or counterexample: Some low-consequence read-only tasks can be checked entirely through displayed content.

Limit: The required outcome evidence depends on the application.

## C05 — DOM automation and visual model control have different interaction and maintenance surfaces.

Type: interpretation.

Sources: S05, S10.

Counter-evidence or counterexample: A model may generate DOM actions; real systems can combine methods.

Limit: The categories describe mechanisms, not mutually exclusive products.

## C06 — An API does not remove injection risk when the model interprets untrusted text returned by that API.

Type: interpretation.

Sources: S09.

Counter-evidence or counterexample: Deterministic consumers that do not interpret text as instructions have a different threat model.

Limit: No comparative incident rate is available in the reviewed sources.

## C07 — Browser session isolation and application authorization address different boundaries.

Type: interpretation.

Sources: S06, S08, S10.

Counter-evidence or counterexample: An application may provide a dedicated restricted browser account.

Limit: No universal browser-versus-API permission ranking follows.

## C08 — A hybrid workflow needs recorded identities and a recovery boundary before another external write.

Type: author judgment.

Sources: S02, S04, S11.

Counter-evidence or counterexample: A fully covered API-only or DOM-only workflow can avoid this extra boundary. New API coverage alone does not establish that migrating an existing hybrid is worth its cost.

Limit: The support-ticket walkthrough is illustrative and untested.

## C09 — Cost comparisons should include verification, failed attempts, maintenance and human exceptions over a common workload.

Type: author judgment.

Sources: S07, S10.

Counter-evidence or counterexample: A low-volume browser workflow can avoid disproportionate integration work.

Limit: No throughput, price or completion-rate measurements were collected.

## C10 — HTTP 202 reports acceptance rather than completed processing.

Type: fact.

Sources: S11.

Counter-evidence or counterexample: Not recorded.

Limit: The meaning of other success codes and the business outcome depends on the endpoint.
