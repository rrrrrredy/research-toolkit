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
