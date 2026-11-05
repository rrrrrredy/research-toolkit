# Independent whole-report evidence review

Reviewer: `/root/case_evidence_full`. Perspective: evidence and data. This independent context succeeds the unavailable `/root/case_evidence_review` premise-review context. Review date: 5 November 2026.

## Result and independence

The evidence review of the complete English report is complete. **No necessary correction and no optional evidence correction were found in the reviewed version.** The report's facts remain within the cited contracts, while its route preference, hypothetical workflow and accounting proposal are identified as judgments or assumptions. This is a content-perspective result, not independent audit or final acceptance.

I read the complete 102-line `report.md`, the complete current `source-notes.md` and `outline.md`, the effective root requirements and clarification, the review/assignment responsibilities in `research-toolkit/references/subagents-and-review-loop.md`, and my predecessor's complete `reviews/evidence-premises.md`, including its repair verification. I then read the actual retained primary-source passages listed below. I did not consult other perspectives' initial reviews, author self-checks or author ratings, and I did not edit the report or its sources. No product was installed or run.

The report hash was observed at 2026-11-05T14:54:44.8579035+08:00 and rechecked at 2026-11-05T14:56:43.0070985+08:00 without a change. Final metadata below records the completion time. Source retrieval times are the actual saved retrieval metadata, not this reviewer claiming to have fetched every page again.

## Substantive checks and disposition

| Report location | Actual primary evidence and reasoning checked | Finding and consequence |
| --- | --- | --- |
| Lines 5–22, route definitions and selection table | Playwright S05 locating-element passages; OpenAI S08 driver and direct-API sections; Anthropic S09 environment/loop text | No defect. Fixed control logic and model-selected actions are distinguished by who chooses actions, not by the mere presence of Playwright. The table's fit conditions are analytical recommendations, not measured product capabilities or a vendor ranking. |
| Lines 24–28, response and completion evidence | RFC 9110 S01 lines 6910–7050; S06 click checks and assertions | No defect. The report preserves the specific noncommittal meaning of 202 and the possibility that another successful response establishes its specified effect. It does not require redundant readback after every synchronous write. Playwright actionability is accurately stated as a precondition for interaction, with the desired business assertion left to the implementer. |
| Lines 32–40, DOM and model behavior | S05 normalized blocks 85–250, especially 100–110 and 223–237; S08 lines 774–791, 1236–1291, 1620–1645 and 1749–1780; S09 numbered lines 283–346 and 792–801 | No defect. User-facing locator contracts, re-resolution and structural-selector vulnerability are all explicit in S05. The report avoids the false premise that DOM means coordinate replay. S08 explicitly puts environment execution and permissions in the application, and says `completed` is completed call generation. S09 supports possible coordinate/tool-selection mistakes and latency limitations. These limitations are not turned into a measured comparative reliability ranking. |
| Lines 44–46, Stripe namespace differences | Full S02 Markdown, especially 14–22; S03 Markdown lines 146–174 | No defect. V1 first-result caching includes 500 after execution starts; the report preserves possible pruning after at least 24 hours, parameter matching and pre-execution exceptions. V2 replay is qualified by same API, same account/sandbox and 30 days, and distinguishes successful work from failed/partial work. Neither is generalized to all endpoints or providers. |
| Lines 48–54, restarts, route changes and delayed visibility | Full S04 Markdown, especially 31–39, 54–62 and 76–93; S03 line 27 | No defect. The original explicitly requires persistent keys across separate calls/restarts, limits unresolved v1 retries to the first 24 hours and calls for reconciliation afterward. The API-to-UI duplicate-protection warning is labeled architectural inference and retains an exception for an enforced shared key or safely repeatable state-setting operation. V2 list consistency is stated as eventual by default, so list absence is correctly not equated with confirmed absence. |
| Lines 58–60, actual authority | S10 normalized blocks 139–172; S07 blocks 85–108 | No defect. User access depends on both user and app permissions; installation-token access depends on app permissions. Endpoint permission requirements are explicit. S07 establishes authenticated state and impersonation risk. The report's distinction between context isolation and server-side permission is a sound architectural inference; it does not claim that all APIs are least-privilege or all browsers are broadly privileged. |
| Lines 62–66, untrusted text and human handling | S13 normalized blocks 254–263, 314–355 and 392–438; S12 lines 2703–2837 | No defect. OWASP identifies external issue/email/page content, tool-parameter manipulation and enforcement outside the model. The JSON-versus-rendered-text application is reasoned synthesis, not a claimed experimental result. OpenAI's action-time, pre-approval and takeover categories are accurately separated and scoped to that integration. The report does not universalize the every-script demonstration or waive action-specific confirmation for all internal work. |
| Lines 70–84, entire hybrid example | Read the full scenario against the above completion, persistence and consent contracts | No defect. The example expressly assumes API coverage, company-operated UI, reference and history capabilities; no named product is asserted to supply them. A history reference is explicitly insufficient by itself for idempotency. The narrative retains partial completion, a single attempt owner, document identity, request revision, unknown generation state, separate attachment recovery, and an investigation path when state cannot be established. It preserves integration-specific confirmation rather than inferring authorization from “internal.” |
| Lines 88–98, obligations, denominator and pilot | S11 normalized blocks 285–338; S08 lines 1222–1226; complete cost/pilot text | No defect. GitHub supports the webhook, pacing and rate-limit obligations, but no magnitude is attributed to the source. The proposed numerator includes failed work and human handling; the denominator is verified jobs, assisted work is separately visible, unresolved/incorrect work is not silently discarded, and the zero-denominator case is expressly undefined. There are no empirical figures or arithmetic results to validate. The same-workload/period and separate initial/recurring effort conditions prevent the formula from masquerading as a measured ranking. |
| Lines 98–102, migration, practical default and evidence limits | Complete ending and source notes, checked against scoped originals above | No defect. Migration retains unfinished-job identity, route preference remains conditional, and the report explicitly discloses the hypothetical scenario and absence of product trial, deployment or comparative measurement. The current retrieval date is not misrepresented as feature launch date. |

## S09: previous necessary finding remains resolved

I read the original EN-E1 finding and its appended repair verification. I independently inspected the titles of both preserved HTTP responses; they remain region-unavailability pages and retain the recorded hashes. The current source notes explicitly identify this content state and use the readable official-page capture instead. I read the saved numbered text and relevant raw web-tool captures, rather than treating status 200 or access metadata as evidence of documentation contents.

The actual captures contain the application-execution/observation text and the coordinate, tool-selection and latency limitations used in report line 36. The source-notes batch statement also matches S09 lines 267–282 and 598–617: execution stops before all later calls in the failed batch. There is no new EN-E1 finding. The clarification requires accurate preservation of acquired/used text and consequential context; it does not require unrelated full-page acquisition. The earlier full-capture verification is retained as prior work and was not repeated unnecessarily.

## Actual reading coverage and limits

For Markdown/text originals, line numbers below refer to the retained files. For HTML originals, “normalized blocks” refers to nonempty text after script/style removal, block-tag line separation, HTML entity decoding and whitespace normalization. This was performed in memory with PowerShell/.NET; no original was rewritten. The extraction numbering agrees with the section landmarks listed below. A first attempt to use `python` was unavailable; the actual completed extraction used PowerShell/.NET.

| Retained original | Actual reading in this context |
| --- | --- |
| S01.original.txt | Lines 6910–7050, successful 2xx and 200/201/202/203/204 context. |
| S02.original.md | Entire file, lines 1–22. |
| S03.original.md | Entire file, lines 1–212, including namespace/version context and idempotency. |
| S04.original.md | Entire file, lines 1–119. |
| S05.original.txt | Normalized blocks 85–250: introduction, recommended locator kinds, locating elements, roles/labels/text/test IDs, CSS/XPath and opening Shadow DOM context. |
| S06.original.txt | Normalized blocks 75–170: introduction, complete checks table, forcing, assertions and definitions. |
| S07.original.txt | Normalized blocks 75–130: authentication/isolation, sensitive state and shared-account conditions; opening setup example. |
| S08.original.txt | Lines 760–810, 1200–1305, 1610–1650, 1740–1790 and 1930–1990. These cover the cited prose and immediate code/section context, not every installation example. |
| S09.web-numbered-text.txt | Header; source-numbered lines 260–349, 590–629 and 780–809. |
| S09.web-original-180.txt | Official title/URL; source-numbered lines 267–270, 281–301 and 307–309. |
| S09.web-original-330.txt | Official title/URL; same early passages plus 598–617. |
| S09.web-original-780.txt | Official title/URL; 598–617 and 792–801. |
| S09.original.txt and S09.original.md | Actual HTML title/content-state inspection and hash verification; not treated as documentation text. |
| S10.original.txt | Normalized blocks 135–175, permission model and REST/GraphQL/Git context. |
| S11.original.txt | Normalized blocks 285–338, operating obligations and repeated-error context. |
| S12.original.txt | Lines 2680–2850, adapter context and the complete confirmation/consent section through its end and migration opening. |
| S13.original.txt | Normalized blocks 230–275, 310–355 and 390–460, including indirect injection, limitations of prompt filtering, tool-boundary enforcement, and smoke-test scope. |

I read the complete retrieval ledger and S09 capture metadata. All 17 ledger entries with an `original_file` were independently rehashed and match their recorded SHA-256; this integrity check is separate from substantive reading coverage. The larger Stripe HTML duplicates were hashed, not read as additional evidence. I did not repeat the old six-capture full-page union check or claim it as new reading. Every external citation in the report maps to one of the original passages above; the relative source-notes link resolves to the file read here.

The evidence supports the bounded guidance actually written. It does not establish runtime performance, savings, deployment success, universal prompt-injection resistance, or a named application implementing the hypothetical workflow. The report does not make those claims. No further evidence-perspective work is required for this unchanged report version.

## Input versions and recorded retrieval times

Review completed: 2026-11-05T14:58:52.3496652+08:00

| Input | SHA-256 |
| --- | --- |
| requirements.md | `16b09fc2bbfdeec3d9835b4cf16d853779349f69ad41cd4d8ee6a4a8b99957a8` |
| requirements-clarifications.md | `98446bf425cbf627ac3bea86c201358600abd03efedf6d078cd1fe0ec62a58d4` |
| api-or-browser-en/report.md | `15a3ee49392069f8187759eec7b889eebf9365d7424d0c08a59b3b6221a8cf91` |
| api-or-browser-en/source-notes.md | `a8843d72f54c3587764f83f081119bd0e7a0ce15ecc6b5370ed205d91ee331bc` |
| api-or-browser-en/outline.md | `4fd09307b3d132f0d098403e778fea6c4c849fdcf37c22077b5978698f5d93d5` |
| api-or-browser-en/reviews/evidence-premises.md | `31e9356f26d8c26dc03aa53afb1c104e697284cbc114d435034d8ab24d573f4d` |
| research-toolkit/references/subagents-and-review-loop.md | `0271b6aef839209f0d635808365e008e741008c97fa34d66bb20e812df5a3021` |

| Actual source or provenance file | Recorded retrieval UTC | Current SHA-256 |
| --- | --- | --- |
| S01.original.txt | 11/05/2026 04:05:28 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| S02.original.md | 11/05/2026 04:06:17 | `fd3d6f889a557f5535d7ac5e5e79c1898ac378b287c45e56a67880b5e5318ee3` |
| S03.original.md | 11/05/2026 04:06:18 | `2117bce4ef2a6410a78669a1f723457cca55052d4cebe5724913ba735e869cac` |
| S04.original.md | 11/05/2026 04:06:18 | `9ab2e69e934255a1a5fe8fc6f86136d8ebfaa73ea7a625889adbf5711efac41e` |
| S05.original.txt | 11/05/2026 04:05:36 | `643e2efba60916c4b276d9b23e7eba115212b00111fbec97f9e3fd74c63dcdf7` |
| S06.original.txt | 11/05/2026 04:05:37 | `a908a515e19a8489aebc04752c39e32c07601288120297bb4d0b2ee9c0d436e1` |
| S07.original.txt | 11/05/2026 04:05:38 | `dac89a341e9a518fa9e74947262221f64398aacb75befa9b92c8682797b07424` |
| S08.original.txt | 11/05/2026 04:05:38 | `a786fd3863e3a019514f85bfbbd9b4059e031a2186a89d99425d0fab64112e46` |
| S09.original.txt | 11/05/2026 04:05:40 | `869f86820c07a85bd46de150eb221e97c2af0a9399f5d6b710dec618e5e61016` |
| S09.original.md | 11/05/2026 04:06:19 | `4511bf126724ae4780e93320f275598043fe8dce50470d57cc7f500315cd01b2` |
| S09.web-numbered-text.txt | 2026-11-05 04:18:18 UTC (capture start) | `0079e2bbf6f4ef69f8d7b691d7cdfdf2d265bb80d256a881ab5a7324530fe01e` |
| S09.web-original-180.txt | 2026-11-05 04:18:18 UTC (capture start) | `2d4dfcc7fea0bff69db0fc0f68916757f880a2b48c957e3a525e651eb0ed9e40` |
| S09.web-original-330.txt | 2026-11-05 04:18:18 UTC (capture start) | `84bc3c60074df783804d10b258a858ca42ff4ca522a5473386e23d75f6dbfce9` |
| S09.web-original-780.txt | 2026-11-05 04:18:18 UTC (capture start) | `89de9cb63ee7cd776e8db09efdc685e015455c3989114edd5e1af25cc396ce65` |
| S09.web-capture-metadata.json | 2026-11-05 04:18:18 UTC (capture start) | `c4439b75b87ee7d0f0fd0ed0de42190945ede55913f984c7457d8d0bbff7b739` |
| S10.original.txt | 11/05/2026 04:05:44 | `7538a5e922849b4c8a8a8a7425926cd8dd63fb02c9af5398d95558fd32751a89` |
| S11.original.txt | 11/05/2026 04:05:45 | `ca5091fab3dda8eba0f18b6f29f258c9cfbe98ef8ff98dfc4672de0575cb98a2` |
| S12.original.txt | 11/05/2026 04:09:02 | `1ab928c4185705c3033321b706fdb7678d1368ad05d24390b302b7619522a28b` |
| S13.original.txt | 11/05/2026 04:09:03 | `50874d6c26cb9d528d20feacc09325bab9fbc131c106a97fdc48a6185b3d19c4` |
| retrieval.jsonl | Ledger corrections through 2026-11-05T04:19:41.2167977Z | `55b2ff1885205d7d7d673222c1693a2f52adee2566b75c52d6fccf44b49380d1` |
