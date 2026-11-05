# Domain review of the initial premises

Reviewer: `/root/case_domain_review`. Domain: enterprise agent execution architecture, browser automation, operation recovery and authorization. Review date: 5 November 2026. This is an independent local premise review of Units A–C, not a review of an assembled report or final acceptance. No other reviewer opinions were read, and no author files were edited.

The effective requirements and `research-toolkit/references/subagents-and-review-loop.md` were read. The examination used the full three analysis contributions, the original passages listed below, and live official OpenAI and Anthropic documentation. No application, model or vendor benchmark was run. The sources can establish contracts and stated limitations; they cannot establish comparative success rates or total operating cost.

## Result and required corrections

The central architectural premises are sound and can support assembly, subject to the two narrow corrections below. No reason was found to require universal redundant polling, universal approval before every click, or one vendor's confirmation policy for every route.

**EN-D1 — Describe Anthropic's complete remaining-batch halt rule accurately. Required, medium severity for integration guidance.** Location: Unit B, S09 evidence bullet, “stop dependent batched actions after a failure.” The current [Anthropic computer-use documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#handle-errors) says to answer the remaining blocks with the halt text instead of running them. The saved true page excerpt is `originals/detail-web-output-2.txt:207–226`, especially line 209, corresponding to official page lines 598–617. The reference executor also maintains a failure flag for later blocks. The source does not delegate a dependency analysis that permits supposedly independent later actions to run. Replace the phrase with “stop the remaining actions in that batch and return the specified halted/error results.” This preserves the intended failure-management argument while avoiding a weaker protocol than the source documents. It does not establish a universal rule for all tools or independently submitted work.

**EN-D2 — Correct the identity of the retained Anthropic originals. Required, medium severity for reproducible source access; not a finding that the technical premise is false.** Location: Unit B's description of `S09.original.txt` and the original-source record. Reading both the saved HTML and the `.md` response shows an “App unavailable in region” page, not the computer-use guide. HTTP status 200 therefore does not establish that the guide was retained in those files. The existing `detail-web-output-1.txt` and `detail-web-output-2.txt` contain the relevant real official passages. This reviewer also opened the official guide live and checked the client execution loop, batch handling, security considerations and limitations. Preserve the failed response, label it correctly, and point the claim to the actual retained page excerpts or a newly acquired complete guide. Do not overwrite the failed response or imply that a partial web result is a complete HTTP original. The excerpt evidence is sufficient for the examined local claims; completeness of any new archive can be checked with the later handoff.

## Premises supported by the examined originals

1. **Completion follows the operation contract.** RFC 9110 distinguishes 202 from 200/201/204. A synchronous result may establish the operation's required effect. Unit A correctly avoids converting every success response into a mere acknowledgment or demanding a second read after every write. A multi-step business workflow still needs evidence for the other required effects. The hypothetical support example must state the finished object and business state, rather than count successful calls.

2. **Idempotency is a scoped replay contract.** Stripe v1 stores the first result after execution begins, including failures; its retention, parameter comparison and pre-execution exclusions matter. Stripe v2 describes a different replay behavior and a 30-day, same-API/account-or-sandbox scope. Both the namespace and the provider must remain attached to these examples. Unit A's warning about eventual list consistency and unknown outcomes is supported. A retry counter or a freshly generated key cannot substitute for preserving the earlier logical operation and known remote identifiers.

3. **Changing route does not transfer duplicate protection.** An unresolved API write followed by a UI submit is a new attempted effect unless a concrete shared business key or idempotent state-setting mechanism makes it safe. This is an architectural inference from the scoped contracts, not a measured claim that every UI/API pair duplicates work. Unit A explicitly allows those concrete exceptions and does not assert that reconciliation can always recover a definitive answer. The proposed human handling path is a recommendation for unresolved state, not a vendor promise.

4. **Observation, controller and execution mechanism are distinct.** Playwright resolves locators against current DOM state and recommends meaningful user-facing or explicit locator contracts. DOM automation is therefore not inherently absolute-XPath replay. Conversely, a model choosing selectors or emitting code at runtime remains model-directed. A fixed function can execute deterministically inside a model-directed workflow. OpenAI's current code-execution and structured-action paths support this distinction. No comparative reliability ranking follows from these mechanisms alone.

5. **Actionability and generation status are not business completion.** Playwright's click checks concern the target interaction. The OpenAI computer-call `completed` status concerns generation of that call, which the application still executes. Result checks should verify the intended record, state and artifact. A different read route may supply that evidence; the analysis does not require the write and observation routes to match.

6. **Actual authority is not implied by API or browser transport.** GitHub App user tokens combine user and app permissions, and permission changes require installation-owner acceptance. Playwright context isolation does not narrow an authenticated user's application permissions. The analysis correctly treats broad API tokens and restricted browser identities as possible counterexamples to a blanket “API is safer” claim. Third-party content remains data when carried in a JSON field or visible page, and cannot grant new authority. The OWASP guidance supports runtime permission and parameter enforcement without proving complete prompt-injection prevention.

7. **Current vendor confirmation semantics need their actual scope.** The [OpenAI integration guidance](https://developers.openai.com/api/docs/guides/tools-computer-use-integration#handle-user-confirmation-and-consent) separates action-time confirmation, certain explicit initial approvals, and human takeover. The every-script approval example is expressly conservative, not a universal requirement. Unit C preserves those distinctions and does not let company policy waive the chosen integration's requirements. Anthropic's current security guidance describes human confirmation for meaningful consequences and affirmative consent, plus end-user consent before enabling the feature; it does not supply the same enumerated rule set as OpenAI. Neither source supports silently carrying one provider's exact policy into every route.

8. **Operational burdens cannot be ranked from these documents.** Rate limits, credentials, UI maintenance, observations, model execution and human interruption can all affect cost. The sources establish that these terms exist, not how large they are for the proposed workflow. Unit C appropriately leaves comparative totals to a common business-result measurement.

## Conditions to preserve in assembly

- The support workflow remains hypothetical. A useful case needs explicit completion and ambiguity handling, including the stated unique generation reference/authoritative terminal status assumption or a human handling branch.
- Preserve the distinction between a blocked write, a permission denial and a locator failure before any write. Visual interpretation can help some interface problems without curing missing authority or unknown side effects.
- Keep provider-specific replay and consent rules provider-specific. An internal processing example with explicit approval does not automatically authorize later external communication or changed sharing.
- Do not derive product launch dates, adaptation success, maintenance savings or unattended operation guarantees from undated mechanism documentation.

## Actual reading and version record

The following manifest records the materials actually examined, their retrieved timestamps where recorded, and SHA-256 computed on the retained bytes. HTML was locally parsed for the relevant original sections; Markdown/text originals were read directly. A manifest entry is not a claim of whole-document reading: the scope column states the actual examined range. For the two Anthropic HTTP responses, the scope is failure-page identification only. Web excerpt files are identified as excerpts.


| Retained file | Actual reading scope | Recorded retrieval UTC | SHA-256 |
| --- | --- | --- | --- |
| `S01.original.txt` | RFC sections 15.3.1-15.3.5; lines 6915-7048 | 2026-11-05T04:05:28.9255909Z | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| `S02.original.md` | Whole substantive page | 2026-11-05T04:06:17.2024788Z | `fd3d6f889a557f5535d7ac5e5e79c1898ac378b287c45e56a67880b5e5318ee3` |
| `S03.original.md` | Namespace comparison, list consistency, Idempotency and Idempotency differences; remainder read without adopting it as a premise | 2026-11-05T04:06:18.1714487Z | `2117bce4ef2a6410a78669a1f723457cca55052d4cebe5724913ba735e869cac` |
| `S04.original.md` | Content, network and server errors; idempotency, POST requests and persistent keys | 2026-11-05T04:06:18.9497863Z | `9ab2e69e934255a1a5fe8fc6f86136d8ebfaa73ea7a625889adbf5711efac41e` |
| `S05.original.txt` | Locating elements, role/label/test-ID locators, CSS/XPath cautions and filtering | 2026-11-05T04:05:36.0987899Z | `643e2efba60916c4b276d9b23e7eba115212b00111fbec97f9e3fd74c63dcdf7` |
| `S06.original.txt` | Introduction, action checks, forcing, assertions and visibility/stability/events | 2026-11-05T04:05:37.7063014Z | `a908a515e19a8489aebc04752c39e32c07601288120297bb4d0b2ee9c0d436e1` |
| `S07.original.txt` | Introduction, Core concepts and shared-account limitations | 2026-11-05T04:05:38.1102269Z | `dac89a341e9a518fa9e74947262221f64398aacb75befa9b92c8682797b07424` |
| `S08.original.txt` | 1248-1275, 1622-1651, 1749-1785, 1952-1982 | 2026-11-05T04:05:38.5621223Z | `a786fd3863e3a019514f85bfbbd9b4059e031a2186a89d99425d0fab64112e46` |
| `S09.original.txt` | Regional-unavailability page identification; NOT the guide | 2026-11-05T04:05:40.2701303Z | `869f86820c07a85bd46de150eb221e97c2af0a9399f5d6b710dec618e5e61016` |
| `S09.original.md` | Regional-unavailability response identification; NOT Markdown documentation | 2026-11-05T04:06:19.7255864Z | `4511bf126724ae4780e93320f275598043fe8dce50470d57cc7f500315cd01b2` |
| `S10.original.txt` | App permissions, token intersection, permission changes and REST access | 2026-11-05T04:05:44.6441884Z | `7538a5e922849b4c8a8a8a7425926cd8dd63fb02c9af5398d95558fd32751a89` |
| `S11.original.txt` | Polling, rate limits, mutation pacing, conditional requests and 404 interpretation | 2026-11-05T04:05:45.0614585Z | `ca5091fab3dda8eba0f18b6f29f258c9cfbe98ef8ff98dfc4672de0575cb98a2` |
| `S12.original.txt` | 2703-2838; confirmation/consent levels and prompt examples | 2026-11-05T04:09:02.8565170Z | `1ab928c4185705c3033321b706fdb7678d1368ad05d24390b302b7619522a28b` |
| `S13.original.txt` | Indirect injection, Agent-Specific Defenses, Least Privilege and separate action enforcement | 2026-11-05T04:09:03.8487917Z | `50874d6c26cb9d528d20feacc09325bab9fbc131c106a97fdc48a6185b3d19c4` |
| `detail-web-output-1.txt` | Local lines 150-165; real Anthropic limitations excerpt | Web excerpt; exact UTC absent from HTTP log | `7aa81b50d2524af8b47ee71ca859484d218a761f75b090f2c1719ff53e32b1d1` |
| `detail-web-output-2.txt` | Local lines 1-42 and 200-226; environment, loop and failure handling excerpts | Web excerpt; exact UTC absent from HTTP log | `80542d00bbca75d6b7f48bf17cc95454734a4726c7bad91e58be197e130df0f5` |

### Reviewed input versions

- `history/A-completion-retry.before-S09-correction.md`: `e938c5a0ecb74efca5b16c0a22e974b59ada4b44127caa885e7222231e6e0a74`
- `history/B-browser-mechanisms.before-S09-correction.md`: `e9d381c8a7ae643779b5f7b440878176111a12b4b64bf70cbfdfe240df7fe9d7`
- `analysis/C-authority-operations.md`: `a69bb061148dbad7d859307fc3c8f3f2d853abcd77de33eb53754f60d5c12bdf`

Effective requirements SHA-256: `16b09fc2bbfdeec3d9835b4cf16d853779349f69ad41cd4d8ee6a4a8b99957a8`.

## Targeted correction recheck

Rechecked on 2026-11-05T04:23:11.895589+00:00. Read the current Unit B in full and checked original numbered lines 267-282 and 598-617 in the newly retained Anthropic text, against the same official page independently opened during this review. **EN-D1 is resolved**: the current text explicitly stops every remaining call in the failed computer-use batch without extending the rule to unrelated work.

**EN-D2 is resolved for this premise handoff**: Unit B now correctly labels both earlier HTTP responses as regional-unavailability pages, retains them, and identifies the actual web captures. The captured-text union contains numbered lines 0-1073. This confirms the readable text archive, not preservation of images or an exact HTTP page. The relevant guide sections were read; the whole page was not substantively re-read. The original findings remain intact above.

### Reviewed input versions

- `analysis/A-completion-retry.md`: `a3d7aa3db6598f3094d8dd4f4043bcdf0b82726e9f8b50db7273405f01782f3b`
- `analysis/B-browser-mechanisms.md`: `048b4b5dd103eaaea16cc74336abd26ec187c19b8fcc65dfae013823689f9f93`
- `originals/S09.web-capture-metadata.json`: `c4439b75b87ee7d0f0fd0ed0de42190945ede55913f984c7457d8d0bbff7b739`
- `originals/S09.web-numbered-text.txt`: `0079e2bbf6f4ef69f8d7b691d7cdfdf2d265bb80d256a881ab5a7324530fe01e`

The new captures report retrieval start `2026-11-05 04:18:18 UTC`; URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool .
- `S09.web-original-180.txt`: `2d4dfcc7fea0bff69db0fc0f68916757f880a2b48c957e3a525e651eb0ed9e40` (capture integrity recorded; numbered text supplied scoped reading).
- `S09.web-original-330.txt`: `84bc3c60074df783804d10b258a858ca42ff4ca522a5473386e23d75f6dbfce9` (capture integrity recorded; numbered text supplied scoped reading).
- `S09.web-original-480.txt`: `25d7f9a59e2cae0bd10e49e5662615a78bf67b9b5249fdb67068a3e796935d1c` (capture integrity recorded; numbered text supplied scoped reading).
- `S09.web-original-630.txt`: `b06a57ad4703c8681d5cf90f00d47a7c775ea6d0242696abf2b1a69851baabd1` (capture integrity recorded; numbered text supplied scoped reading).
- `S09.web-original-780.txt`: `89de9cb63ee7cd776e8db09efdc685e015455c3989114edd5e1af25cc396ce65` (capture integrity recorded; numbered text supplied scoped reading).
- `S09.web-original-930.txt`: `3f4e7f42944ad0dea52c05da190f7b80c4bcc6c432dc62639da051dc9eb80ab9` (capture integrity recorded; numbered text supplied scoped reading).
