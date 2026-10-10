# Sources and reading notes

Eleven primary English sources support this article. These are reading notes from the relevant sections, not copies of complete web pages. The documentation was read on 10 October 2026; most pages are living documentation without a publication date.

[Source registry CSV](data/source_registry.csv) · [Claim records](claims.md) · [Report](report.md)

## S01 — Idempotent requests

Publisher: Stripe. Publication date: Undated living documentation.

[Original source](https://docs.stripe.com/api/idempotent_requests)

Reading scope: API v1 response replay, key retention and validation behavior.


**Reading notes**

API v1 saves an executed request response for replay, including errors. Keys can be pruned after at least 24 hours; reuse after pruning starts a new request. Parameter mismatch is rejected. The page expressly distinguishes API v2.


**Limits**

Only Stripe API v1 behavior is established; idempotency is not an all-service or end-to-end completion guarantee.


## S02 — Advanced error handling

Publisher: Stripe. Publication date: Undated living documentation.

[Original source](https://docs.stripe.com/error-low-level)

Reading scope: Network errors, server errors and POST retry guidance.


**Reading notes**

A dropped connection can leave the request outcome unknown. A 500 can have side effects. API v1 replays cached errors; changing the key can cause another operation. The guide recommends retrieving objects and using events to reconcile uncertain outcomes.


**Limits**

Guidance is scoped to Stripe API v1; it does not establish empirical failure rates or prescribe every provider’s recovery rules.


## S03 — API v2 overview

Publisher: Stripe. Publication date: Undated living documentation.

[Original source](https://docs.stripe.com/api-v2-overview#idempotency)

Reading scope: Idempotency and differences between API v1 and API v2.


**Reading notes**

API v2 skips successful work and attempts failed work again where possible. Replay uses the same key and API, within the same account or sandbox and within 30 days. POST and DELETE accept keys. Responses can be updated rather than replaying an earlier error unchanged.


**Limits**

The version distinction matters. It is not a promise that every unresolved request can recover or a comparison of production reliability.


## S04 — Auto-waiting

Publisher: Playwright. Publication date: Undated living documentation.

[Original source](https://playwright.dev/docs/actionability)

Reading scope: Introduction, click checks, forcing actions and assertions.


**Reading notes**

A normal locator click requires one matching target that is visible, stable, enabled and receiving events. Assertions retry their conditions. Force can bypass some actionability checks.


**Limits**

These are interaction and assertion semantics, not proof that a downstream business workflow finished.


## S05 — Locators

Publisher: Playwright. Publication date: Undated living documentation.

[Original source](https://playwright.dev/docs/locators)

Reading scope: Locating elements, role locators, test IDs and CSS/XPath discussion.


**Reading notes**

Role, label and test-ID locators can provide explicit ways to find elements. Playwright resolves the current element on each action. The guide warns that long CSS/XPath chains can break with DOM changes.


**Limits**

Recommendations do not establish a universal maintenance advantage or guarantee that a third-party application exposes stable locators.


## S06 — Authentication

Publisher: Playwright. Publication date: Undated living documentation.

[Original source](https://playwright.dev/docs/auth)

Reading scope: Introduction, stored authentication warning and shared-account conditions.


**Reading notes**

Browser contexts can reuse saved authenticated state. The saved state may contain cookies or headers that permit account impersonation. Shared accounts are unsuitable for parallel tests that alter conflicting server-side state.


**Limits**

Browser isolation does not establish narrow business permissions. Authentication examples describe test setups, not a production security certification.


## S07 — Best practices for using the REST API

Publisher: GitHub. Publication date: Undated living documentation.

[Original source](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)

Reading scope: Avoid polling/concurrent requests, mutative pacing and rate-limit errors.


**Reading notes**

GitHub recommends webhooks where possible, efficient conditional polling otherwise, serial requests to reduce secondary-rate-limit pressure and honoring retry/reset information. Errors require handling rather than an assumption of unlimited throughput.


**Limits**

The advice applies to GitHub. It supplies an example of API operating constraints, not a numerical API/browser cost comparison.


## S08 — Choosing permissions for a GitHub App

Publisher: GitHub. Publication date: Undated living documentation.

[Original source](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app)

Reading scope: About permissions and choosing REST API access.


**Reading notes**

GitHub App permissions govern allowed API operations and webhook subscriptions. The guide recommends the minimum required permissions; endpoint documentation identifies required permissions.


**Limits**

Permission models differ across services; this does not prove every API offers sufficiently narrow scopes.


## S09 — LLM Prompt Injection Prevention Cheat Sheet

Publisher: OWASP. Publication date: Undated living documentation.

[Original source](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

Reading scope: Indirect injection, structured prompt limits, agent-specific defenses and least privilege.


**Reading notes**

Untrusted issue descriptions, documents and web content can contain hostile instructions. The guidance calls for validating tool calls against permissions and session context, validating parameters and limiting privileges. Prompt formatting alone does not authorize actions or establish resistance.


**Limits**

Security guidance is not a measured prevention rate; it does not justify a blanket safe/unsafe ranking of APIs and browsers.


## S10 — Computer use tool

Publisher: Anthropic. Publication date: Undated living documentation.

[Original source](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

Reading scope: Security considerations, computing environment, implementation loop and screenshot history.


**Reading notes**

The application executes requested computer actions and returns screenshots/results to the model. The documentation describes isolation, constrained access and human confirmation for consequential actions, while acknowledging prompt-injection exposure. Screenshot history adds model input and context-management work.


**Limits**

Vendor documentation describes one implementation. It provides neither an independent reliability comparison nor a cost forecast for another product.


## S11 — RFC 9110: HTTP Semantics

Publisher: IETF. Publication date: 2022-06.

[Original source](https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted)

Reading scope: Section 15.3.3, 202 Accepted.


**Reading notes**

HTTP 202 indicates acceptance for processing before that processing is complete; the operation might not ultimately be performed. A response should indicate status or monitoring information.


**Limits**

A status-code definition does not establish a specific application’s lifecycle; endpoint-specific completion information is still required.
