# APIs or browsers: how to choose an execution route for an AI agent

*10 October 2026*

The useful starting point for a business agent is the operation it must complete: update a record, attach a document, change an account setting or submit a request. Choose the interface for that operation, then decide what evidence will show that it finished. A workflow can require several routes even when its user experiences one application.

Use a supported API when it exposes the required operation, appropriate permissions and a result that can be checked. Use browser automation where the relevant workflow is available only through the interface, or where a small task does not justify a separate integration. Distinguish a script that targets named page elements from a model that selects actions from screenshots. Their failure modes and operating costs are different.

The central trade-off is how much work remains after sending a command: checking the resulting state, resolving uncertain outcomes and maintaining the integration when the application changes. That work determines whether a successful demonstration becomes a repeatable business process.

| Route | A useful starting condition | What still needs checking |
| --- | --- | --- |
| Supported API | The endpoint exposes the exact operation and a suitable authorization model. | Completion semantics, retry behavior, limits and permissions for the specific endpoint. |
| DOM-based browser automation | The workflow has identifiable controls and a sufficiently stable interaction path. | Target identity, saved application state and changes to the page contract. |
| Model-directed visual interaction | The task requires interpreting an interface that a prepared script does not cover. | Each consequential action, resulting state and the scope available to the session. |
| A combination | One necessary operation is missing from the otherwise suitable route. | The handoff, durable record identifiers and recovery after partial completion. |

This is a public-source analysis of interface behavior and workflow design. The examples below are illustrative; no production deployment or comparative performance experiment was conducted. The sources establish documented mechanisms, not a universal reliability or cost ranking.

## 1. API availability is an operation-level question

An application having an API says little about whether the agent can complete a particular assignment through it. A usable integration needs the right operation, access to the right object, sufficient permissions and a way to inspect what happened. “Update this customer” may hide several operations: changing a field, recording the reason, attaching supporting material and triggering an approval. Coverage has to be checked against that actual sequence.

The same distinction applies to authentication. Possessing a token does not establish that an integration can perform every required action. GitHub Apps, for example, configure permissions for API access and webhook subscriptions; GitHub recommends selecting the minimum needed and consulting endpoint requirements. That is a useful model for evaluating access, not proof that every service provides equally precise controls. [GitHub App permissions](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app)

A team's first decision should therefore be a small inventory of required operations and observable results. If the API covers the entire assignment, adding a browser can create extra credentials, failure paths and maintenance without adding capability. If it misses a required administrative operation, browser access may fill that gap. The recommendation follows from coverage and control rather than the presence of an API logo or a convincing screen demonstration.

A further distinction is acceptance versus completion. HTTP `202 Accepted` explicitly allows a server to acknowledge a request before processing is finished, and the operation might ultimately not occur. The interface contract must explain what to inspect next. A job identifier and a status endpoint may be more important than the initial successful response. [HTTP Semantics, §15.3.3](https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted)

## 2. A retry needs an identity and a recovery rule

An API can make retries easier to reason about by documenting how repeated requests are handled. Idempotency means that repeating an operation does not add the same effect again within the contract's conditions. It is still necessary to identify which requests represent the same business operation.

Stripe shows why the details matter. For API v1, an idempotency key replays the saved status and body after execution begins, including error responses. Keys can be removed after they are at least 24 hours old; reuse after removal can initiate another request. A key with changed parameters is rejected. “Use an idempotency key” is therefore incomplete advice unless the application also preserves its parameters and understands the retention window. [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)

API v2 has different replay semantics. Within its documented same-key, same-API and same-account-or-sandbox scope, a replay can skip successful work and retry failed work, returning an updated response. Its window is 30 days. These differences make the API generation part of the integration design; a rule copied from an older implementation may describe the wrong behavior. [Stripe API v2 overview](https://docs.stripe.com/api-v2-overview#idempotency)

The difficult case is an uncertain outcome. A network timeout does not tell the client whether the server acted. Stripe's API v1 guidance also treats a `500` response as potentially having side effects. Starting again with a fresh key can repeat the operation. Its documented recovery methods include inspecting the relevant object and reconciling events. This is a provider-specific example of a broader design requirement: separate an unsuccessful response from a confirmed unsuccessful action. [Stripe advanced error handling](https://docs.stripe.com/error-low-level)

For a business agent, the practical consequence is to retain an operation identity outside the model's conversational memory. A restarted run needs to recognize that it is recovering an earlier attempt. If it cannot establish the outcome, the next step is reconciliation or an exception queue, not another unconstrained attempt to satisfy the user's original request.

## 3. Browser automation contains two different operating models

A deterministic browser script can locate a control by its role, label or explicit test identifier and execute a prepared sequence. Playwright recommends user-facing attributes and explicit locator contracts, while warning that long CSS or XPath paths can break as the page structure changes. This can make a stable, repeated workflow practical without asking a model to reinterpret every screen. It does not guarantee that another company's interface will remain stable. [Playwright locators](https://playwright.dev/docs/locators)

A visual computer-use agent works through an observation-and-action loop. In Anthropic's documented implementation, the host application executes the requested actions and returns screenshots or other results to the model. This can cover interactions that are not already encoded in a prepared script. It also leaves the host responsible for the environment, action execution and subsequent observations. [Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

Real systems can combine these mechanisms: a model may interpret a request while a browser script performs the known steps. Calling both approaches “browser agents” can hide a consequential difference. A label change may require updating a locator; an unfamiliar page may require renewed model interpretation. The operational response depends on which part supplies the action.

Neither mechanism turns a completed click into proof of a business result. Playwright's normal click checks concern a uniquely matched, visible, stable, enabled element that receives events. Its assertions can wait for a specified condition. Those capabilities help make interactions deliberate, but the team must still specify a condition that represents the actual outcome. A button being clickable does not show that the intended record was saved. [Playwright auto-waiting](https://playwright.dev/docs/actionability)

For a record update, that condition should identify the record and the intended value after submission. For a request that starts a background job, it should address the job's completion. Where the application's available evidence cannot settle the result, the workflow needs an explicit uncertain state. A final screenshot can be useful evidence; its value depends on what the displayed state actually establishes.

## 4. Transport does not decide who may act

An API token and an authenticated browser session both convey authority, but through different mechanisms. A narrowly scoped API integration can restrict which operations are available. A browser session operates with the permissions of its account. The right comparison is the access actually granted, including whether a dedicated restricted account is possible.

Playwright's authentication guidance warns that saved browser state can contain cookies or headers usable for account impersonation. Isolating browser contexts helps separate sessions; it does not reduce the application's permissions for the signed-in account. A session with administrative access remains consequential even inside a clean container. [Playwright authentication](https://playwright.dev/docs/auth)

The route also does not decide whether information is trustworthy. A support-ticket description returned as JSON can contain the same hostile instructions as its rendered page. OWASP describes indirect injection through issue descriptions, documents and web content, and recommends checking tool calls against user permissions and session context. Moving the transport to an API does not make free-form customer text an instruction from the operator. [OWASP prompt-injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

A useful separation is to let the model interpret relevant content while the action interface enforces the allowed operations and parameters. Instructions found inside a ticket should not expand which accounts may be changed or where attachments may be sent. Consequential actions may require a person to inspect the actual proposed change. These controls add work; they are part of the workflow's operating cost and should be included in the comparison.

## 5. Combine routes only at a boundary that can be recovered

Consider an illustrative support workflow: read a request, update a customer record, create a document through an administrative screen, attach it to the ticket and move the ticket to the next state. Assume the supported API covers ticket and customer operations, while the document-generation action is available only in the interface. These are scenario assumptions, not claims about a named product.

The API can retrieve the exact ticket and customer identifiers. The agent can draft the proposed update, while a restricted action interface checks the target and allowed fields. After the update is confirmed, a browser can perform the document action. The returned document and its relationship to the ticket must be checked before the workflow attaches it and changes the ticket's state.

The handoff should carry the ticket identity, the completed update and the remaining operation. If document generation times out, restarting the entire workflow would repeat work that may already have succeeded. Resume from the unresolved operation and inspect whether its result exists before creating another one. If the administrative interface cannot reveal enough state to settle that question, route the case to a person.

This boundary matters more than whether the model can narrate the sequence. The workflow should be able to report which operation is complete, which is uncertain and what observation would allow it to continue. “The agent finished” is too coarse when several systems have accepted different parts of the job.

There is no benefit in preserving this split if the API later covers document generation with adequate permissions and result checking. Conversely, a low-volume workflow with a stable interface and simple verification may be cheaper to maintain entirely in the browser. The extra route should earn its place by completing a necessary operation or improving a relevant control.

## 6. Compare the cost of verified completion

A model's per-call price is only one part of an automated workflow. A run also consumes infrastructure, retries, verification and exception-handling effort. Integrations need maintenance when an endpoint, page, permission model or operating policy changes. Browser agents may incur repeated observation costs; APIs may require work to handle asynchronous operations and rate limits.

GitHub's REST guidance illustrates why programmatic access should not be modeled as unlimited throughput. It recommends webhooks where possible, appropriate pacing and explicit handling of rate-limit responses. Those are integration responsibilities, even though the action is structured. [GitHub REST best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)

A useful comparison over the same workload and accounting period is:

**Cost per verified completion = (integration and maintenance cost + execution and verification cost + human exception-handling cost) / verified completed jobs.**

This is a proposed accounting model, not a measured result. The numerator should include the cost of unsuccessful attempts rather than considering only the clean demonstrations. The denominator needs the same definition of completion for each route. Track unresolved and incorrectly completed work separately; a route that quietly drops difficult cases can appear cheap without meeting the assignment.

A practical pilot can use a bounded workload with known expected results and realistic access conditions. Include an ambiguous submission, a changed interface, a permission denial and an interrupted run, alongside routine tasks. Record how often the expected result is verified, where people intervene and how much recovery work is required. Those observations are more useful for the local decision than a general claim that APIs or visual agents are always cheaper.

The strongest default is to choose the route that exposes the needed action and lets the team verify and recover its result with acceptable effort. Add another route for a specific coverage or control gap. Keep responsibility for completion visible across the whole workflow, including the cases the agent cannot finish by itself.
