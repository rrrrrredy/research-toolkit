# Working outline: choosing an execution route for recurring business work

Created: 2026-11-05 04:03:54 UTC. Main writer: native agent `/root/case_en_author`.

## Question, reader and delivery

When should enterprise AI agents use supported APIs, deterministic DOM automation, model-directed visual browser interaction, or a hybrid for recurring business workflows? The reader is an operations or engineering lead choosing a route per operation and planning a bounded local pilot. Deliver a native-English public report with usable primary-source links and a compact selection table. Current documentation will be verified on 5 November 2026; evidence published later cannot establish earlier availability.

Required coverage: exact action coverage; business completion rather than interaction success; retries, duplicate effects and idempotency scope; permissions and untrusted input; recovery after partial execution; operating and maintenance effort; migration; human handling; one coherent hypothetical workflow. No installed-product test, vendor/benchmark ranking, invented performance or cost figures, or claim that this case demonstrates general Toolkit benefit. The prior October brief/report supply scope and history only.

## Proposed argument and sequence

1. **Start with the business operation and its completion evidence.** Define the three execution mechanisms without conflating a model orchestrator with the interface it controls. A supported API is a candidate when the required operation, authorization and observable result are present. Compare all routes on the same business outcome.
2. **Choose what the software can execute and what it can confirm.** Compact table: API, deterministic DOM, visual model interaction, hybrid; fitting conditions, what each can establish, and resulting maintenance/recovery obligations. Explain the causal distinction between stable contracts, locators and model-selected actions. Examine a reasonable countercase to an API default: a low-volume stable UI operation whose API integration work buys little.
3. **Make repeat execution safe for the specific operation.** Separate request acknowledgement, completed action and completed business job. Verify endpoint-specific idempotency, time windows and uncertain outcomes. Explain why operation identity must survive a restarted agent and why changing route must not create a second write.
4. **Match authority and recovery to the action.** Compare actual token scopes with browser-account privileges; session isolation versus application permission. Treat API text and rendered text according to their provenance. Human handling is needed for unavailable authority, authentication challenges and outcomes that cannot be reconciled, rather than as an inflated universal approval process.
5. **Trace one recoverable hybrid workflow.** Hypothetical support-ticket/document workflow with explicit assumed coverage, stable identifiers, result checks, a timeout after a consequential UI action, a resumed attempt and a human exception. Show what each mechanism does and why, including when to keep a DOM path and when model-directed visual help could earn its cost. No invented claim about a named product's coverage.
6. **Decide with local completion and maintenance costs.** Proposed unmeasured accounting model over equal workload/period, covering integration, execution, verification, retries, maintenance and human exceptions. Give a bounded pilot path and migration triggers: API expansion, stable repeated visual path, changing UI, inaccessible completion evidence. Distinguish design recommendations from measured comparisons.

## Analysis units and dependencies

| Unit | Question and planned originals | Output | Dependencies |
| --- | --- | --- | --- |
| A: completion and retries | HTTP semantics; a current provider's documented idempotency, error handling and event behavior | Evidence plus reasoned operation identity/recovery argument | Independent evidence/domain scrutiny before scenario relies on its claims |
| B: browser mechanisms | Playwright locators/actionability/authentication; current Anthropic and OpenAI computer-use documentation | Distinctions, action/result limits, permissions and maintenance comparison | No dependence on A; current model names/features must not be inferred from old report |
| C: route and authority | Provider permission guidance; model/tool security guidance where directly useful | Decision conditions and bounded human responsibilities | Relevant A/B premises checked before final recommendations |
| D: coherent workflow and economics | Explicit scenario assumptions; synthesis from A–C | Developed hypothetical sequence and unmeasured cost/pilot/migration framework | A–C consequential premises independently examined |

## Work and review boundary

Source originals, retrieval metadata and full substantive unit analyses will be preserved locally. Public source notes will paraphrase relevant passages and give locators without republishing whole copyrighted pages. `first-draft.md` will be immutable after creation; `report.md` will hold revisions, with evidence-linked explanations outside the report. No complete draft will be assembled until the lead returns requirements/structure scrutiny. The lead arranges seven independent content perspectives, domain review, audit and final acceptance; author checks do not substitute for them.

Unresolved research questions: current documented computer-use mechanisms and limitations; whether any selected sources changed since October; provider-specific recovery conditions; how much evidence warrants preferring a route without a local test. These remain research questions, not assumed findings.
