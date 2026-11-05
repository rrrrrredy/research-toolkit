# APIs, browser scripts or visual control: choosing how an enterprise agent acts

*5 November 2026*

For recurring business work, start with a supported API when it exposes the required operation, suitable permissions and a usable result. Use a prepared browser script for a stable interface workflow that the available API does not adequately cover. Use model-directed visual interaction where interpreting the current screen adds necessary capability. Combine routes when different steps need different interfaces, with a clear way to recover each unfinished operation.

The decision belongs to the individual operation. An agent may read a ticket through an API, generate a document through an administrative screen and attach the result through another API. Calling the whole system an “API agent” or a “browser agent” tells an operations lead little about whether a failed run can be resumed without repeating work.

The useful comparison is the effort required to reach the same verified business result: executing the action, observing what happened, recovering uncertain outcomes and maintaining the route. The recommendations below are design judgments grounded in current documentation. They do not establish a measured reliability or cost ranking.

## 1. Choose the operation and its completion evidence together

A service can have an extensive API and still lack the operation a team needs. “Prepare this customer record” might require changing a field, generating a document, attaching it and moving a ticket to the next state. Check coverage against those actual effects, including the account and permissions available to the integration.

| Route | When it fits recurring work | What the team must be able to maintain and verify |
| --- | --- | --- |
| Supported API | The documented endpoint covers the exact operation with appropriate authority and result semantics. | Request parameters, endpoint versions, limits, replay rules and evidence of the intended effect. |
| Deterministic DOM automation | The necessary UI path has identifiable controls and sufficiently stable steps to encode in advance. | Locator and workflow changes, the target record, submission behavior and saved state. |
| Model-directed visual interaction | The step needs interpretation of a screen or a variation that a prepared path does not cover economically. | Model-selected actions, observations, execution limits and whether the resulting business state can be established. |
| Hybrid | A specific action or observation is better served by a different route. | Shared record identity, partial completion and recovery at the handoff. |

Here, a supported API means an interface documented and intended for integration. Browser automation means operating the application's UI. Within that UI, deterministic automation uses prepared control logic; visual interaction lets a model select actions from what it sees. These are execution mechanisms that can coexist in one product.

Define completion at the same level as the assignment. An API response may establish that a field was saved, while the business job still needs a generated document. HTTP `202 Accepted` is particularly clear: processing has been accepted but is unfinished and might never occur. Other successful responses can establish that their specified operation completed. The endpoint contract determines whether the response itself is sufficient or a job status, event or later observation is needed. [RFC 9110, successful responses](https://www.rfc-editor.org/rfc/rfc9110.html#name-successful-2xx)

The equivalent browser question is whether the application saved the intended result. Playwright's normal click checks include a unique match, visibility, stability, event reception and enabled state. Its assertions can wait for specified conditions. These help execute an interaction; the implementer still has to choose a condition that identifies the correct record and required result. A generic success banner may be insufficient, while a displayed document ID and final job status may provide useful evidence. [Playwright auto-waiting](https://playwright.dev/docs/actionability)

Verification does not require a second request after every successful write. If a synchronous response already guarantees the relevant saved state and identifies the object, use it. Where another observation is needed, its route can differ from the action route: a UI-only creation step might still expose an API readback. The aim is enough evidence to resolve the actual job.

## 2. Browser scripts and visual agents move different work into runtime

A prepared DOM script identifies page elements through names, labels, roles or explicit identifiers. Playwright recommends user-facing attributes and explicit locator contracts, and resolves a fresh element each time a locator acts. A named control can therefore remain usable after a layout change. Long CSS or XPath chains tied to page structure are more vulnerable to structural changes. Treating all DOM automation as coordinate replay misses this distinction. [Playwright locators](https://playwright.dev/docs/locators)

For a stable recurring path, encoding the steps once can avoid asking a model to reinterpret the same controls on every run. The maintenance obligation remains: a renamed control, a new required field or a changed approval step can invalidate the prepared flow. The relevant stability is the path and its meaning, not whether the page looks identical.

A visual agent interprets the current screen and proposes actions. That makes it a candidate for necessary visual judgments or infrequent interface variations that would be expensive to encode individually. It also adds interpretation during execution. Anthropic's documentation identifies possible coordinate and tool-selection mistakes, as well as latency limitations. Its computer-use integration leaves the application responsible for running actions and returning observations. These are reasons to examine the local task, not evidence that visual control always performs worse than a script. [Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

The boundary is not the programming library. OpenAI's current guide describes both model-generated code and structured computer actions; the application executes those requests and owns the environment and permissions. A model generating Playwright code at runtime still supplies the controlling decisions. A model calling a fixed “attach this document to this ticket” function can instead rely on prepared execution inside that function. The same guide notes that a computer call's `completed` status means generation of the call finished; the application must still execute it. [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use)

This distinction changes how to handle a failure. If a locator no longer matches before any write, visual interpretation may help locate the permitted control or diagnose the changed page. If submission may already have happened, a more flexible model does not settle that uncertainty. Nor does it supply missing permission. Keep those cases separate so a fallback repairs the failure that actually occurred.

## 3. A resumed run must recognize the same business operation

An idempotent operation can be repeated without adding the same effect again under its contract. The contract's scope matters. Stripe API v1 saves the first status and response body after endpoint execution begins, including `500` errors. A replay with the same key returns that saved response. Keys may be removed after they are at least 24 hours old; reuse after removal can start a new request. Changed parameters are rejected, and some failures before execution do not create a saved result. [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)

Stripe API v2 behaves differently. A replay uses the same key for the same API, within the same account or sandbox and within 30 days. It skips successful work and can retry failed or partially failed work, returning an updated response or an explanatory error. This is why an integration needs the rules for its actual namespace and endpoint. A generic instruction to “retry idempotently” omits the information needed to decide what the retry will do. [Stripe API v2 idempotency](https://docs.stripe.com/api-v2-overview#idempotency)

An uncertain outcome is the important operational case. A dropped connection does not reveal whether the server acted. Stripe's v1 guidance treats a `500` as potentially having side effects, limits unresolved same-key retries to the first 24 hours, and then calls for reconciliation through the relevant object, request records or events. It also explicitly recommends persisting an operation's key across separate SDK calls or process restarts. [Stripe advanced error handling](https://docs.stripe.com/error-low-level)

For an enterprise workflow, retain the logical operation, its parameters, destination account and any returned identifiers outside the model's conversation. A restarted agent should recover that attempt rather than create a new identity because it received the same assignment again. A saved retry count alone cannot establish what already happened.

Changing routes has the same problem. If an API submission times out, pressing Submit in the browser does not automatically inherit the API's duplicate protection. The browser may help inspect the existing result; a new write needs a reason to be safe. A shared business key enforced across both routes, or a documented state-setting operation that can safely be repeated, may provide that reason. Without such a mechanism, reconcile the original attempt first. This is an architectural inference from the scoped contracts, not a claim that every API/UI pair creates duplicates.

Even readback needs its own interpretation. Stripe documents that v2 lists are eventually consistent by default, so an immediate empty list need not prove that an earlier creation failed. The observation used for recovery must distinguish absence from delayed visibility. When the available interface cannot settle the outcome, retain the unresolved state and hand it to someone who can investigate it. [Stripe API v2 overview](https://docs.stripe.com/api-v2-overview)

## 4. Compare the authority actually granted

An API is useful when its authorization model fits the task. GitHub Apps illustrate the distinction: endpoint documentation specifies required permissions; a user access token is constrained by both the user's and the app's permissions, while an installation token depends on the app's permissions. The existence of a token does not establish access to every required operation. [GitHub App permissions](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app)

A browser session carries the authority of its signed-in account. Playwright warns that saved authentication state can contain cookies and headers usable to impersonate that account. Isolating browser contexts separates sessions; it does not reduce permissions in the application. Consequently, a broadly privileged API token can be a worse fit than a narrowly restricted browser account. Compare actual identities, allowed records and operations, rather than treating either transport as inherently safe. [Playwright authentication](https://playwright.dev/docs/auth)

The origin of content matters separately. A customer's instruction embedded in a ticket remains customer content whether it arrives as JSON or rendered text. It cannot authorize changes to another account or redirect an attachment to a new destination. OWASP describes indirect injection through issue descriptions and other external material, and recommends enforcing permissions and validating tool parameters outside the model. Applying that guidance here means the execution component restricts the target and change to the authorized job. Prompt wording alone does not enforce that restriction. [OWASP prompt-injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

Provider requirements also affect how much work can run unattended. OpenAI's computer-use integration guidance distinguishes actions requiring confirmation at execution time, specified actions for which explicit initial permission can suffice, and actions requiring human takeover. Its action-time examples include sending to a third party and confirming financial transactions; its prior-permission examples include specified uploads and data use. Those rules belong to that integration. They neither impose approval before every click on all systems nor disappear because a company calls a workflow internal. [OpenAI confirmation and consent guidance](https://developers.openai.com/api/docs/guides/tools-computer-use-integration#handle-user-confirmation-and-consent)

Plan human handling around the particular interruption: an approval, an authentication challenge, missing authority or an unresolved write. Give the person the proposed action or the last known result so they can make the needed decision. A repeated generic confirmation prompt adds work without necessarily clarifying either permission or completion.

## 5. Follow one hybrid job through an interrupted submission

Consider a hypothetical support ticket requesting a service-summary PDF in the customer's preferred language. The agreed job is to save the document-language preference, generate the PDF, attach it to that ticket and mark the ticket ready for a reply. Sending the customer that reply is a separate operation.

Assume the supported API covers ticket and customer reads, the preference update, attachment and internal ticket status. A company-operated document generator exposes creation only through its UI. Assume it accepts a request reference and provides a history view that can identify pending and completed jobs by that reference. These are scenario assumptions to check in the chosen application. The history view does not, by itself, make creation idempotent.

The workflow owner authorizes the specified preference change and the document's destination in the support system. Any confirmation required by the selected integration still occurs at the relevant action. An existing job record retains the ticket and customer IDs, the requested language, the request revision, the generation reference and the results already confirmed. Only one worker owns the current attempt, so two runs do not independently submit its unresolved generation step.

**Read and update through the API.** Retrieve the exact ticket and customer, then change the allowed preference field. Record evidence that the update succeeded, using the endpoint's actual result and replay semantics. If the request has changed since the job began, re-evaluate the remaining work; an earlier language choice is not automatically the customer's current instruction.

**Generate through the browser.** A prepared DOM path is a reasonable starting point for stable, named controls. It opens the correct customer, selects the language and template, and submits the retained reference. If the layout has changed before submission, a visual model may help interpret it, provided the exact target and permitted action remain checkable. If it is only a renamed known control, repairing the script may be the simpler ongoing solution.

Now suppose the browser disconnects immediately after submission. The preference update is complete; generation is unresolved. Restarting the whole job would discard that distinction. On resumption, inspect history for the same reference. A matching completed job supplies the document ID. A pending job should be followed to its outcome. Another submission is justified only by authoritative evidence that the earlier attempt did not start, or by a documented mechanism that makes repetition safe. If history is ambiguous, the support operator receives the ticket ID, reference and last known state to investigate the existing attempt.

**Attach and finish the internal job.** Check that the resulting document belongs to the intended customer and uses the requested language and template. Attach that exact document to the original ticket. If the attachment result is lost, reconcile that operation before attaching again. Move the ticket to ready only once the required attachment is confirmed. A failure here leaves document generation complete and attachment or status unresolved; it does not require generating another PDF.

This design uses a browser for one coverage gap. Visual control is an option where interpretation helps, rather than a required addition to every step. An entirely browser-based implementation could still be preferable for a small workload with stable paths, suitable permissions and inexpensive verification, if maintaining a separate API integration would cost more than it saves. Conversely, if the UI cannot expose enough state to recover generation, broadening the model's freedom does not repair the missing evidence.

## 6. Let completion and maintenance costs decide the local choice

APIs have operating obligations too. GitHub recommends webhooks where possible, paced requests and explicit handling of rate-limit responses. UI paths need maintenance when controls or business steps change. Visual interaction adds model execution and observations; all routes can incur verification, retries and human handling. Documentation establishes these responsibilities without measuring their size in a particular team. [GitHub REST API best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)

Compare routes over the same eligible workload and period using a proposed accounting model:

**Cost per verified completed job = (attributed setup and migration cost + maintenance cost + all execution and verification cost + human handling cost) / verified completed jobs.**

Include failed attempts in execution cost. Include required approvals, authentication interruptions, reconciliation and corrections in human cost. Assisted completions can count as completed jobs when their full labor is included, but show their share separately from automatic completions. Also report unresolved and incorrectly completed cases; dropping difficult work must not make a route appear cheap. If no job meets the completion definition, the ratio is undefined. This is an accounting proposal, not a measured result.

Start a bounded pilot with one recurring workflow whose expected results the operations owner can inspect. The engineer maps its actual operations and permissions to the candidate routes. Alongside routine cases, include an interrupted submission and restart, and any interface change or permission problem that is material to this workflow. Record verified outcomes, elapsed time, human effort and maintenance work. Show initial integration effort separately from recurring effort, then compare both over a common planning period. Set acceptable completion and turnaround requirements from the team's service needs; these sources provide no universal target.

Revisit the route when a specific condition changes. If the document generator gains a suitable supported endpoint, compare the avoided browser maintenance and recovery work with migration and revalidation effort. If a frequently used visual path becomes predictable, encoding its stable steps may reduce repeated interpretation. Preserve the identity and state of unfinished jobs during either change, or complete them through their existing route, so migration does not repeat an unresolved write.

The practical default is an API for operations it adequately supports, prepared DOM automation for stable UI gaps, and visual interpretation where it supplies necessary capability. A hybrid earns its extra coordination when it closes a real gap and preserves a recoverable business result across the handoff.

*This analysis uses primary documentation read on 5 November 2026. The support workflow is hypothetical; no installed-product trial, production deployment or comparative performance measurement was conducted. [Source notes](source-notes.md) identify the relevant passages and their limits.*
