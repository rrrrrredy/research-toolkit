# Independent domain review — complete English report

- Reviewer: native agent `/root/case_domain_full`, independent of report production. Domain: enterprise-agent execution, software integration and recovery from partial execution.
- Review completed: 2026-11-05T07:04:26.6098199Z.
- Artifact: `report.md`, read in full, lines 1–102. SHA-256: `15a3ee49392069f8187759eec7b889eebf9365d7424d0c08a59b3b6221a8cf91`.
- Also read: complete effective `../requirements.md`, `../requirements-clarifications.md`, `outline.md`, `source-notes.md`, the scenario/accounting contribution `analysis/D-scenario-accounting-proposal.md`, and the earlier same-role `reviews/domain-premises.md`. The earlier review was navigation/history, not a substitute for current original-source reading.
- Scope: the full report's route definitions, endpoint semantics, retry identity, UI recovery, authorization, proposed workflow, operating-cost denominator and migration conditions. No other initial reviewer output or author self-check was read. No report edits, product installation or operational experiment were performed.

## Decision

**Complete domain review; no necessary correction identified for this version.** There is no optional change requested as a condition of readiness. The report supports a conditional architecture recommendation rather than a measured ranking. This judgment does not certify production performance or any unspecified endpoint.

## Substantive checks and basis

1. **Execution routes are classified by the controller and operation, not by a library or product name.** Lines 15–22 and 32–40 distinguish supported integration APIs, prepared DOM logic, and runtime model decisions. Playwright's locator guidance supports current-DOM resolution and meaningful locator contracts; it does not promise an unchanged business process. OpenAI's original guide explicitly describes generated code and structured actions, and leaves execution to the application. A model emitting Playwright code is therefore correctly treated as model-directed even though its output uses a deterministic library. The recommendation for stable UI paths is a design inference, with no unsupported success-rate claim.

2. **Interaction and business completion are not conflated.** Lines 24–28 correctly distinguish HTTP 202 from successful synchronous operation responses, and do not require redundant polling after every write. RFC 9110 §§15.3.1–15.3.5 supports that account. Playwright's normal click conditions in the original include uniqueness, visibility, stability, event reception and enabled state; those conditions do not prove the correct document or ticket outcome. The report leaves result selection to the actual business contract. OpenAI's `computer_call` generation status is also correctly separated from execution at line 38.

3. **Retry claims use the actual documented namespace and conditions.** Lines 44–54 agree with the retained Stripe originals: v1 stores the first response after execution begins, including 500, and may prune a key after at least 24 hours; validation/concurrency failures before execution differ. V2 replay requires the same key/API/account-or-sandbox and the stated 30-day interval; successful work is skipped and failed or partial work may be re-executed. The report does not infer retry behavior from the word API, from HTTP alone, or from an API version label. It preserves the source's warning that an unresolved outcome remains possible.

4. **Recovery follows the logical operation across process and transport boundaries.** Lines 48–54 preserve keys, parameters, account and remote identifiers across restarts. The API-to-UI fallback warning is explicitly an architectural inference and allows a concrete common business key or safely repeatable state-setting operation. The v2 list consistency warning correctly prevents treating immediate absence as proof of failure. None of this asserts that arbitrary UI/API pairs share duplicate protection.

5. **The workflow supplies the conditions its recovery argument needs.** Lines 70–82 define a hypothetical internal support job with explicit API coverage, a UI-only generation step, a request reference and a history view. The history view is explicitly not called an idempotency guarantee. Single ownership of an attempt and retained request revision address duplicate workers and stale instructions at the design level. After a disconnect, pending, completed and ambiguous generation states lead to distinct actions; resubmission needs authoritative evidence or an actual replay guarantee. Attachment uncertainty is handled separately and does not regenerate the PDF. The proposed result includes the correct customer, language/template, attachment and final internal state. No named product is claimed to provide these hypothetical capabilities.

6. **Authority follows identities and concrete permissions.** Lines 58–66 accurately reflect GitHub App token permissions, Playwright's sensitive authentication state and the distinction between session isolation and application privileges. A narrowly restricted browser account can be preferable to a broad API credential; this is a valid counterexample to an absolute transport ranking. OWASP's original supports tool-parameter and permission enforcement outside the model, while the report does not promise that prompts eliminate injection. OpenAI confirmation examples at line 64 preserve the source's action-time, initial-permission and human-takeover distinctions and remain scoped to that integration. The hypothetical owner's authorization does not waive those requirements.

7. **The proposed economic comparison has a coherent denominator.** Lines 90–96 specify the same eligible workload and period, verified completed jobs, failure/retry cost, maintenance, setup/migration and human labor. Assisted completions are counted only with their labor and disclosed separately; unresolved and incorrect cases remain visible. An empty completion denominator is undefined. This avoids interpreting cheap failed attempts or uncounted staff intervention as efficiency. The model is labeled a proposal without numerical results; no vendor documentation is stretched into a total-cost estimate.

8. **Migration and the browser countercase remain conditional.** Lines 84 and 98 allow a small stable all-browser workload when the extra API integration costs more than it saves. Moving to a new endpoint or preparing a previously visual path requires comparing actual capability and maintenance, while preserving unfinished operation identity. These are reasonable design consequences, not field measurements or a claim that all hybrid systems earn their coordination cost.

## Actual original reading

These are the originals examined in this review. HTML sources were decoded locally and their relevant article/main text was read. Text/Markdown ranges below refer to the retained files; S09 uses its embedded official-page line numbers. The scope descriptions do not imply whole-page reading where only relevant sections were examined. The direct S09 regional-error responses were not used as documentation.

| Original | Actual scope read | SHA-256 |
| --- | --- | --- |
| `originals/S01.original.txt` | Lines 6915–7048: RFC 9110 successful responses, 200 through 204 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| `originals/S02.original.md` | Entire substantive page | `fd3d6f889a557f5535d7ac5e5e79c1898ac378b287c45e56a67880b5e5318ee3` |
| `originals/S03.original.md` | Entire page, including namespace table, consistency, idempotency and differences | `2117bce4ef2a6410a78669a1f723457cca55052d4cebe5724913ba735e869cac` |
| `originals/S04.original.md` | Entire page, including content/network/server errors, POST retry window and persistent keys | `9ab2e69e934255a1a5fe8fc6f86136d8ebfaa73ea7a625889adbf5711efac41e` |
| `originals/S05.original.txt` | Locating elements, role/label/text/test-ID contracts, CSS/XPath cautions, shadow-DOM and filtering sections | `643e2efba60916c4b276d9b23e7eba115212b00111fbec97f9e3fd74c63dcdf7` |
| `originals/S06.original.txt` | Entire article: actionability, force, assertions and condition definitions | `a908a515e19a8489aebc04752c39e32c07601288120297bb4d0b2ee9c0d436e1` |
| `originals/S07.original.txt` | Introduction, core concepts, shared-account recommendation and restrictions, one-account-per-worker rationale | `dac89a341e9a518fa9e74947262221f64398aacb75befa9b92c8682797b07424` |
| `originals/S08.original.txt` | Lines 1248–1275, 1622–1651, 1749–1785 and 1952–1982 | `a786fd3863e3a019514f85bfbbd9b4059e031a2186a89d99425d0fab64112e46` |
| `originals/S09.web-numbered-text.txt` | Embedded lines 267–340, 598–617 and 792–804: execution, batch failures and limitations | `0079e2bbf6f4ef69f8d7b691d7cdfdf2d265bb80d256a881ab5a7324530fe01e` |
| `originals/S10.original.txt` | Complete substantive article: permission models and endpoint access | `7538a5e922849b4c8a8a8a7425926cd8dd63fb02c9af5398d95558fd32751a89` |
| `originals/S11.original.txt` | Polling, pacing and rate-limit handling; redirect, conditional-read and error context also examined | `ca5091fab3dda8eba0f18b6f29f258c9cfbe98ef8ff98dfc4672de0575cb98a2` |
| `originals/S12.original.txt` | Lines 2703–2838: runtime enforcement, confirmation/consent levels and prompt examples | `1ab928c4185705c3033321b706fdb7678d1368ad05d24390b302b7619522a28b` |
| `originals/S13.original.txt` | Indirect injection and agent attacks; agent-specific defenses, least privilege and action-screening limits | `50874d6c26cb9d528d20feacc09325bab9fbc131c106a97fdc48a6185b3d19c4` |

The retained source retrieval records date the HTTP materials to 2026-11-05T04:05:28Z–04:09:03Z; the actual S09 page-text captures began at 2026-11-05 04:18:18 UTC. This review used those current retained originals and did not perform a new live fetch. Review time and source retrieval time are different.

Effective requirements hashes: `requirements.md` = `16b09fc2bbfdeec3d9835b4cf16d853779349f69ad41cd4d8ee6a4a8b99957a8`; `requirements-clarifications.md` = `98446bf425cbf627ac3bea86c201358600abd03efedf6d078cd1fe0ec62a58d4`. Public source-notes hash: `a8843d72f54c3587764f83f081119bd0e7a0ce15ecc6b5370ed205d91ee331bc`.
