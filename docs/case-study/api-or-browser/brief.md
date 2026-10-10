# Research brief

## Question

When should an enterprise AI agent use a supported API, browser automation, or a combination for recurring business workflows?

## Audience and use

Operations and engineering leads choosing an execution route for repeatable work in existing business software. The report supports a bounded local pilot and an operation-by-operation design decision.

## Scope

Original English research, using primary English documentation read on 10 October 2026. Compare supported APIs, deterministic DOM automation, and model-directed visual interaction through action coverage, completion, retry behavior, authority, recovery, and operating cost.

The support-ticket workflow is a hypothetical illustration. There is no proprietary customer material, installed-product experiment, production deployment, vendor ranking, measured cost comparison, or controlled estimate of Research Toolkit's effect.

## Evidence and review

Read relevant sections of official documentation and record each source's use and limitations. Separate documented behavior, author judgment, and scenario assumptions. Retain the original English draft, a separate-context review of the complete article and evidence, and the decisions on that review.

## Outline

1. **Choose a route per action, then define completion.** An interface only matters if it exposes the needed operation and permits checking the resulting state. Clarify supported API, DOM automation and visual agent interaction.
2. **APIs make operation boundaries explicit; retries still need a business identity.** Establish actual endpoint behavior, idempotency scope, authentication and limits. Avoid equating HTTP success with end-to-end completion.
3. **Browsers cover application workflows that an available API may not expose.** Separate deterministic DOM automation from visual model control. Explain what actionability checks establish and what a business-state check must still prove.
4. **Authorization and untrusted content remain workflow problems.** Bound credentials, sessions, input authority and actions according to the data/action in question rather than assuming either transport solves safety.
5. **A useful hybrid has a recoverable boundary.** Trace a hypothetical support-ticket workflow, record the business identifier and result of each externally visible write, and specify escalation on ambiguous outcomes. A scenario explains the design; it is not a field result.
6. **Compare cost per verified completion.** Include run costs, failed attempts, change maintenance and human exception handling. Give an unmeasured formula and a practical pilot decision; do not make up performance numbers.

Final artifact: native English report with source links, a compact route-selection table and clear limits. Research records and review notes live outside the report prose. One case demonstrates an actual use of the Toolkit; it does not prove general research-quality improvement.
