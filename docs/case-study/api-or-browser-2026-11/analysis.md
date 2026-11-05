# Full research contributions

The original saved analyses appear below with their contemporaneous context and status. These are working contributions; the report carries the complete current argument.

<details><summary>A-completion-retry.md</summary>

# Unit A: completion, replay and ambiguous outcomes

Saved 2026-11-05 04:06:38 UTC by `/root/case_en_author`. Research contribution for independent premise scrutiny, not a completed report or review. Sources were retrieved and relevant sections read on 5 November; saved HTTP responses and actual web-tool outputs are in `../originals/`. The later S09 capture correction distinguishes its regional-unavailability HTTP responses from readable official-document text; see `../revisions.md` and `../originals/S09.web-capture-metadata.json`.

## Evidence and exact scope

- **S01, RFC 9110**, [§15.3.3](https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted), original `S01.original.txt`: a 202 response acknowledges processing acceptance; processing is unfinished and might never occur. Read §15.3.3 and its neighboring 200/201/204 definitions. Those neighboring definitions matter: it would be wrong to imply every successful API response is only an acknowledgement. An endpoint can establish that its particular operation completed; it cannot by itself establish every later operation in a business workflow.
- **S02, Stripe idempotent requests**, [current documentation](https://docs.stripe.com/api/idempotent_requests), original `S02.original.md`, relevant substantive section read in full: v1 records the first result after endpoint execution begins and replays it, including 500; keys may be removed once at least 24 hours old; changed parameters produce an error. Validation or concurrent execution conflicts can occur before a result is saved. This is a Stripe v1 contract, not a property of all APIs.
- **S03, Stripe API v2 overview**, [Idempotency](https://docs.stripe.com/api-v2-overview#idempotency), original `S03.original.md`: a repeated same-key request to the same API, within the same account/sandbox and within 30 days is a replay. Successful work is skipped; failed or partially failed work is re-executed where possible, producing an updated response or explanatory error. Read the namespace comparison, idempotency and differences sections. The overview also states v2 lists are eventually consistent by default. Thus absence in an immediate list is not universally decisive evidence of no previous effect.
- **S04, Stripe advanced error handling**, [Network errors, Server errors, POST requests, Sending idempotency keys](https://docs.stripe.com/error-low-level), original `S04.original.md`: a recovered connection does not settle whether an earlier request executed. For v1, same-key/same-parameter retries are bounded to the first 24 hours; after that, reconcile rather than restart. A 500 can have side effects. The source identifies object retrieval, dashboard request inspection and webhooks as reconciliation routes. It explicitly recommends generating and persisting a key across SDK calls or process restarts. Read these sections plus content-error behavior. Provider reconciliation is not guaranteed to settle every operation.

## Developed reasoning

The first design question is the business result, then the observation that establishes it. Creating a document resource, attaching that document to a particular ticket and moving that ticket to a ready state are three effects. An endpoint's successful response can establish the first effect when the contract says so; it cannot silently stand in for the other two. Conversely, requiring a second read after every synchronous response would add unnecessary work when the response already identifies the object and guarantees the required state. Verification should use the strongest available evidence relevant to the operation, not an arbitrary extra request.

Retry behavior belongs to an operation's contract. The v1/v2 comparison defeats the broad claim that idempotency simply means replaying the same response. The business need is preventing duplicate effects while recovering an attempt, and providers can implement that differently. The integration must bind a durable local operation identity to the exact remote request, its parameters, destination account and any server identifiers. A resumed agent that generates a fresh key because it has forgotten the earlier attempt is creating a new operation, even if its natural-language assignment is unchanged.

The same issue crosses routes. If an API submission times out, opening the application and pressing its submit button does not inherit the API key's duplicate protection. A hybrid can be used to inspect the existing result, but a write through another interface needs reconciliation first. This is an inference from the endpoint-scoped contracts, not a statement that every UI/API pair duplicates work. Some products expose a common business key or naturally idempotent state-setting operation; those concrete mechanisms can make a retry safe if their conditions hold.

Readback has limits too. A missing item in an eventually consistent list can mean delayed visibility, permission filtering, wrong account or actual absence. The documentation for the chosen observation must settle which inference is justified. When it does not, a human handling path preserves the unresolved operation identity and evidence rather than resetting the job. This is a design recommendation, not an observed exception rate.

## Consequential premises for independent review

1. A route is useful only if it covers both the action and a sufficient completion observation; that observation can be its synchronous response, a status endpoint, an event or meaningful displayed state. No universal demand for redundant polling.
2. Safe replay depends on specific endpoint scope, time and parameter rules. Stripe examples should stay provider/version-bound.
3. A route switch is not a recovery policy by itself; unresolved writes must retain their identity and be reconciled before a new write.
4. A hypothetical support workflow must assume either a unique searchable generation reference plus authoritative terminal status, or explicitly hand ambiguous generation to a person. An immediate empty list alone is inadequate.

These premises feed Unit D only after the lead arranges independent evidence/domain scrutiny. No local production test has occurred.


</details>

<details><summary>B-browser-mechanisms.md</summary>

# Unit B: browser mechanisms, what changes and what remains

Saved 2026-11-05 04:06:38 UTC by `/root/case_en_author`. Standalone research contribution; downstream synthesis awaits independent premise scrutiny.

## Evidence and reading coverage

- **S05, Playwright Locators**, [Locating elements and Locate by CSS or XPath](https://playwright.dev/docs/locators): preferred locators use user-facing attributes or explicit contracts; a locator resolves the current element each time it acts. Long DOM/CSS/XPath chains are vulnerable to structural changes. Read introduction, locating elements, role/label/test-ID approaches, CSS/XPath caution and filtering examples. Stored HTML: `../originals/S05.original.txt`; readable retrieval: `browser-web-output.txt` and subsequent detail outputs.
- **S06, Playwright Auto-waiting**, [Introduction, Forcing actions and Assertions](https://playwright.dev/docs/actionability): a normal click requires one matching element, visibility, stability, event reception and enabled state; assertions wait for specified conditions. These are interaction checks. A forced click can suppress checks. Relevant sections read in full; original `S06.original.txt`.
- **S07, Playwright Authentication**, [Core concepts](https://playwright.dev/docs/auth): browser contexts isolate sessions; persisted state may contain impersonation-capable cookies/headers. Read introduction, core concepts and shared-account limitations. A clean context does not change server-side permissions or make two writes to one account independent. Original `S07.original.txt`.
- **S08, OpenAI Computer use**, [Use the SDK; Use the API directly; Use code execution; Use the computer tool; Run safely](https://developers.openai.com/api/docs/guides/tools-computer-use): current docs expose screenshot/mouse control, structured browser operations and code execution. The application owns the environment/session/permissions and executes model requests. A computer call marked completed is finished generation of the call, not execution of the action. The guide calls for actual outcome checks and treats screen/tool-result text as untrusted. Read these sections directly in the live page and saved official Markdown `S08.original.txt`; examples not executed. Avoid deriving a new feature's launch date from this undated current page.
- **S09, Anthropic Computer use**, [The computing environment; Understand the agent loop; Handle errors; Limitations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool): application runs actions and returns observations; current docs acknowledge coordinate/tool-selection mistakes and latency. After an action fails, the documented computer-use batch handler stops all remaining calls in that batch and returns error results for them, rather than deciding which remaining calls seem independent. This condition does not say to stop unrelated work outside that batch. Relevant sections read: original numbered lines 267–340, 484–617 and 792–801, plus current-version/migration descriptions. Correct source capture: `../originals/S09.web-original-180.txt` through `S09.web-original-930.txt` preserve six complete actual web-tool outputs; `S09.web-numbered-text.txt` is their deduplicated readable extraction, covering every numbered line 0–1073; `S09.web-capture-metadata.json` records method, URL, UTC time and individual ranges. The earlier `S09.original.txt` and `.md` are preserved regional-unavailability HTTP responses, not documentation originals. No benchmark or model ranking follows.

## Developed comparison

For a stable repeated path, a deterministic script encodes which element and branch to use in advance. User-facing locators can survive layout moves because they locate meaningfully named controls rather than fixed pixels. That narrows, but does not remove, maintenance: renamed controls, altered permissions and changed business steps can still invalidate the path. It is misleading to equate DOM automation with brittle absolute XPath, or to treat all page changes as failures.

Visual interaction lets a model interpret the current screen and choose actions without a fully prepared path. That is a useful candidate for layouts whose necessary meaning is visual or for infrequent variations that would otherwise demand many scripts. It is a conditional design judgment, not evidence that a model will reliably adapt to every redesign. Interpretation moves to runtime; screenshots, model turns, execution and result checks all remain part of the work. Official docs explicitly expose mistakes and integration responsibilities.

The technologies overlap. A model can call Playwright, invoke a supported business API or combine screenshot interpretation with prepared controls. The distinction for the reader is who selects the next action and from what observation. If a model emits a new selector or new script from a screenshot at runtime, that step remains model-directed even though Playwright executes it. If it calls a fixed, previously defined “attach this file to ticket ID” function, that function can be deterministic while its caller is an AI agent. This definition prevents readers from labeling all code-based UI work deterministic or all AI-controlled browser work visual.

A normal click's success says the interaction met its conditions, not that the right business entity changed. A screenshot has the same evidentiary question: does it display the relevant record, document ID and saved state, or merely a success banner? The best verification can be mixed; a browser-only creation operation might still expose an API readback, or a UI may show an authoritative job result unavailable through the integration. Choice of action route and choice of observation route need not be identical.

Model adaptation should not be a silent response to a blocked operation. If a script fails because a locator has moved before any write, a visual path may diagnose or complete the permitted operation if its target and outcome are checkable. If the failure is a permission denial or an uncertain post-submit outcome, more interpretive flexibility does not solve the missing authority or uncertain effect. The fallback should preserve the cause of failure and the same operation identity.

## Consequential premises for independent review

1. Deterministic DOM and visual model control are mechanisms, not mutually exclusive product categories. The controlling logic and observation distinguish them.
2. Stable locators reduce one class of maintenance; current evidence does not quantify the relative maintenance cost of routes.
3. Model-directed visual control can be justified by interpretation/coverage needs, conditional on checkable effects and bounded authority. It is not a general repair mechanism for denied or ambiguous writes.
4. The business outcome check should be explicit and can use a different route from the write. No actionability check or model status is proof of the complete business job.


</details>

<details><summary>C-authority-operations.md</summary>

# Unit C: authority, human handling and operating burden

Saved 2026-11-05 04:09:05 UTC by `/root/case_en_author`. Research contribution, not an independent assessment.

## Evidence and reading scope

**S10, [GitHub App permissions](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app):** read About permissions, changes and REST endpoint access. Permissions are selected for the app; endpoint documentation specifies required permissions; user access tokens are limited by both user and app permissions, while installation tokens depend on app permissions. Permission increases require installation-owner approval. This establishes a concrete scoped integration model, not that all API tokens are narrow. Original `../originals/S10.original.txt`.

**S07, [Playwright authentication](https://playwright.dev/docs/auth):** browser state can carry impersonation-capable cookies/headers. The implication that context isolation does not reduce the signed-in user's server-side permissions is an architectural inference, not a promised security property of Playwright. Original `S07.original.txt`.

**S12, [OpenAI computer-use integration recipes, Handle user confirmation and consent](https://developers.openai.com/api/docs/guides/tools-computer-use-integration#handle-user-confirmation-and-consent):** read the full confirmation/consent section. It distinguishes action-time confirmation (including sending to third parties and financial transactions), cases where an explicit initial approval can suffice (including specified uploads/data use), and required human takeover. Its code-execution demonstration confirms every script conservatively; the guide says production should enforce action-specific rules, so the sample is not evidence for a universal per-script approval requirement. This source materially limits claims about wholly unattended visual workflows using that integration. Original `S12.original.txt` official Markdown, retrieved 2026-11-05T04:09:02.8565170Z.

**S13, [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html):** read Introduction, Remote/Indirect Prompt Injection, Input Validation, Structured Prompts, Agent-Specific Defenses, Least Privilege and Secure Implementation Pipeline. It identifies malicious instructions in issue descriptions, documents and other external material and distinguishes prompt formatting from permission enforcement at execution. Original `S13.original.txt`, retrieved 2026-11-05T04:09:03.8487917Z. This is security guidance, not an incident-frequency dataset or a proof that the recommended controls eliminate injection.

**S11, [GitHub REST best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api):** read webhooks/polling, pacing, rate-limit handling, conditional reads and repeated errors. Structured interfaces still require handling throughput limits and error meaning. A 404 can conceal a private resource from unauthorized credentials; absence is therefore not always established by that response. Original `S11.original.txt`. Keep provider-specific meanings scoped.

## Developed reasoning

An API token with broad administration rights is not intrinsically a narrower authority than a browser account restricted to one queue. Compare the actual resource and action permissions, along with the provider's automation rules. A browser that succeeds after an API permission denial may be operating under a different account; that difference is not permission to complete the denied action. A sanctioned service account or explicit operator decision can change the authorization, but changing transport alone cannot.

The execution component should bind proposed actions to the permitted record, fields and destination. A model may parse a customer's text to extract a requested update; that text cannot select an unrelated customer or provide new permission to send an attachment elsewhere. The same text returned in a JSON field retains its provenance. This inference applies OWASP's external-content analysis to both routes and avoids presenting API use as a prompt-injection remedy.

Human handling has several distinct causes. A business owner may need to approve an exceptional change; a provider may require action-time confirmation; an authentication challenge may require the account holder; a partially executed operation may require someone with access to an authoritative record. Those causes should stay visible because each affects whether unattended operation is possible and how long a job will remain unfinished. A general “human in the loop” slogan conceals the actual interruption. Conversely, no universal approval-before-every-click procedure follows from these sources.

For repeated work, a defined internal workflow can carry existing permission, with runtime enforcement of the permitted targets and changes. Any provider-specific confirmation requirement still applies; a report should not imply that a company policy waives it. The illustrative support case should stop before external customer communication and assume approved internal processing/data use. If extended to sending the document to a customer, the route decision must include the selected integration's confirmation requirements.

Operating cost has to include API integration and permission onboarding, UI locator maintenance, visual interpretation and screenshots, execution limits, completion observations, and people waiting on or resolving exceptions. None of the documents quantify a route's total cost per successful business case. GitHub's advice supplies a concrete counterexample to describing APIs as limitless or maintenance-free; the conclusion remains a local accounting exercise.

## Premises requiring independent scrutiny

1. Compare actual authority rather than treating transport as permission or security.
2. Provider confirmation rules can change a recurring workflow's achievable autonomy and labor requirements; describe their scope, without imposing one vendor's rule on all routes.
3. Free-form source content remains untrusted whether obtained by API or UI; enforce allowed actions outside model-generated instructions.
4. A cost comparison includes failed attempts and human completion/recovery work under a common result definition; no comparative ranking follows from documentation alone.


</details>

<details><summary>D-scenario-accounting-proposal.md</summary>

# Unit D design contribution: hypothetical workflow and local accounting

Created 2026-11-05 04:21:24 UTC by `/root/case_en_author`, after the S09 correction. This contribution develops scenario assumptions and an unmeasured decision model; it does not settle technical premises still under evidence/domain scrutiny. Integrate it only after those premises and their necessary corrections return. No experiment or product workflow has been executed.

## A coherent hypothetical job

The support team receives a ticket asking for a service-summary PDF in the customer's preferred language. The approved internal job is to update the document-language preference, generate the PDF, attach it to the same ticket and mark the ticket ready for a customer reply. Sending that reply is a separate action outside this illustration. This gives the job a concrete end state without implying that an attachment is already delivered to a customer.

Assume, expressly for this scenario, that the service exposes supported API operations for reading the ticket/customer, changing the allowed preference field, attaching an existing file and updating the ticket's internal state. The legacy document generator exposes creation only through its administrative interface. It has a field for a request reference and a history view that identifies completed and pending generation jobs by that reference. These capabilities are assumptions to verify in an actual application, not claims about a named product. No API key automatically supplies UI duplicate protection.

An existing job record can retain the ticket/customer IDs, the relevant ticket revision, intended language, operation reference, completed steps and returned document ID. This is state needed to resume this job; it does not require a new general workflow platform. The deployment needs one owner for the current job so two workers do not both submit its unresolved generation step. If the customer request changes before a later write, the job should be re-evaluated against the new request rather than treating the old parameters as a current instruction. The product's available version or concurrency controls determine how to enforce that condition.

Proposed sequence for later prose:

1. Read the exact ticket and customer IDs and the language request through the API. Confirm that the requested field change falls within the workflow's existing permission. Free-form ticket content supplies the requested preference, not authority to change arbitrary records or send files elsewhere.
2. Apply the preference through its supported endpoint and record the returned evidence of its result. Use that endpoint's documented replay rules if the response is lost. A response that already establishes the required saved state need not be followed by a redundant read solely to satisfy a checklist.
3. Open the document generator for that customer. For stable named controls, use a prepared DOM path to select the language/template and submit the recorded request reference. Before submission, verify the visible customer and parameters. A visual model can help interpret an unfamiliar pre-submission layout if its actions remain allowed and the exact target/result can still be checked. Its intervention does not silently authorize a changed business operation.
4. If the browser disconnects after submission, leave generation unresolved. Resume by checking the history for the same request reference. A completed matching job yields its document ID; a pending job means wait for its result. Only authoritative evidence that no job started, or an explicit safe duplicate-prevention contract, supports another submission. An empty eventually consistent list would not establish that condition. If the interface cannot settle it, a person receives the ticket ID, reference and last known state to reconcile the existing attempt.
5. Check that the generated document belongs to that customer and uses the requested language/template. Attach that exact document to the exact ticket through the supported endpoint. If the attach result is lost, reconcile the attachment using its available identity and replay conditions before attaching again. Mark the ticket ready only after the required attachment is confirmed. An error at this stage does not restart preference update or document generation.

This is principally an API-plus-DOM design because only document creation needs the UI. Requiring a visual model at every stage would introduce interpretation with no demonstrated coverage need. An entirely browser-based route remains a candidate if the workload is small, its UI paths are stable, permissions fit and the cost of maintaining an API integration outweighs the operating benefit. The report should explain this as a local trade-off, without pretending these assumptions establish which route is cheaper.

## Decision accounting without fictitious numbers

Compare routes over the same eligible job population and period. Define completion as the intended customer preference saved, the correct PDF attached once to the intended ticket and the ticket in its required internal state. A model's final message, a completed browser action and an unresolved exception do not satisfy that denominator. Separate jobs completed automatically, jobs completed with human help, jobs still unresolved and jobs found incorrectly completed. This prevents cheap execution that drops difficult work from appearing efficient.

Proposed accounting model:

`cost per verified completed job = (attributed setup/migration cost + maintenance cost + all execution/verification cost + human handling cost) / verified completed jobs`

All execution cost includes failed attempts and retries. Human handling includes required approvals, authentication interruptions, reconciliation and correcting wrong results. Include assisted completions in the denominator only with their full labor cost and disclose their share separately. Report unresolved/wrong cases alongside the ratio. If no job meets the completion definition, the ratio is undefined rather than zero. For an initial pilot, show setup cost separately so a small first batch does not obscure the later recurring burden; for the route decision, use a common expected operating period without presenting the estimate as measured fact.

A practical first pilot belongs jointly to the workflow owner, who defines acceptable finished cases and exception handling, and the engineer, who checks coverage/authority and instruments the existing job path. Use a bounded representative set with known expected results, including an interrupted submission and a recoverable restart, rather than only prepared successful demonstrations. Where a changed interface is a real maintenance concern, include it. Permission denial tests the handoff, not the ability to find a more privileged route. Set acceptable completion, intervention and turnaround levels from the team's service requirement; the public sources provide no universal target.

Migration should respond to a specific changed condition. A newly supported document endpoint can remove the UI gap, but its permissions, result semantics and migration effort still need comparison. A frequent visual path that has become predictable may justify encoding its stable steps as DOM automation. A UI that stops exposing sufficient result evidence may justify narrowing automation or asking for an API, even if clicks still work. Switching systems should preserve the identity and state of in-flight jobs, or finish them in their old path, so migration itself does not repeat an unresolved write. These are proposed design consequences to reconcile with the checked premises, not field observations.


</details>
