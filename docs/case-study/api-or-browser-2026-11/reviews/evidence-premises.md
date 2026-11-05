# Independent evidence review: consequential premises

Status navigation: the initial assessment is preserved below. A later repair verification is appended at the end and resolves EN-E1; it does not replace or rewrite the original finding.

Reviewer: `/root/case_evidence_review`. Perspective: evidence. Cutoff: 5 November 2026. This is the original independent assessment. I did not consult other reviewers' assessments or edit production text.

I read the complete current Units A, B and C and `source-notes.md`, the effective root `requirements.md`, and the evidence/assignment/premise-review provisions in `research-toolkit/references/subagents-and-review-loop.md`. This assessment covers those premises, not a complete report that has not yet been submitted to this reviewer.

## Result

The substantive premises in A and C, and B's mechanism comparison, can feed assembly with their present provider, version and inference qualifications. One necessary evidence-preservation correction remains: both locally saved S09 HTTP originals contain an access-failure page, not the cited Anthropic documentation. The already saved web-tool extracts and an independent live opening support the relevant mechanism statements, so this is not a finding that those statements are false. It is a concrete mismatch between the evidence described and the files supplied, and the requirement to retain full original material is not yet satisfied for S09.

## Necessary correction EN-E1

**Location:** Unit B, S09 evidence bullet (“Original `S09.original.txt` (HTML)”), the introductory full-originals statement in Unit A, and S09 records in `originals/retrieval.jsonl`.

**Observed evidence:** `S09.original.txt` and `S09.original.md` have the HTML title `App unavailable in region | Claude by Anthropic`. Removing scripts/styles exposes the regional-unavailability landing page, footer and site navigation; it does not expose the computing-environment, agent-loop, error-handling or limitations sections. The saved `.md` is also HTML. Their recorded status 200 and matching hashes establish that those responses were saved, not that documentation retrieval succeeded. The verified SHA-256 values are `869f86820c07a85bd46de150eb221e97c2af0a9399f5d6b710dec618e5e61016` and `4511bf126724ae4780e93320f275598043fe8dce50470d57cc7f500315cd01b2` respectively.

**Impact/severity:** Required correction, medium. A future reviewer following the stated original cannot reproduce the reading; the full-original retention requirement remains incomplete. This is a source-state/provenance defect, not evidence that the product is unavailable in all regions or that the documented features do not exist.

**Repair:** Preserve both failed responses unchanged and label their content state as an access-failure page. Retain a genuinely complete readable original of the official documentation, or the complete official web-tool page if direct HTTP retrieval remains blocked, with URL, actual retrieval time, file and hash. Point Unit B and source records to that successful artifact, while identifying the already retained extracts accurately as excerpts. Do not overwrite the failed files or label HTTP 200 alone as successful original retrieval. Return this narrow repair to the same reviewer; no repeat of unchanged Stripe, Playwright or permission analysis is needed.

**Supporting text already available:** `detail-web-output-2.txt:1–66` contains the official computing-environment/agent-loop text at page lines 283–346. `detail-web-output-1.txt:1–200` contains error, implementation, migration and limitation material at page lines 601–696 and 738–836. I independently opened the [official Anthropic page](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) on 5 November and read its introductory mechanism and batch-failure sections (page lines 70–198 and 199–346). These are genuine source text, unlike the two local failed responses. They substantiate the relevant bounded premises but do not turn the saved excerpts into a complete original.

## Premises cleared for assembly and evidence checks

| Claim location | Original evidence actually checked | Assessment and condition |
| --- | --- | --- |
| A: completion semantics | RFC 9110 original lines 6915–7047, including 200, 201, 202 and 204 | Correct. The 202 limitation must not be generalized to every successful response. The unit correctly permits a synchronous response to establish the operation it actually guarantees. The multi-effect business example is author reasoning, not an RFC-defined workflow. |
| A: Stripe v1 replay | S02 official Markdown in full, especially lines 14–22; S04 lines 23–39, 54–93 | Correct. Saved first response, including 500, starts only after endpoint execution; validation/concurrent-execution failures may precede saving. Keys can be removed after at least 24 hours. The 24-hour unresolved-retry bound and reconciliation recommendation are expressly present in S04. Preserve the API v1 scope. |
| A: Stripe v2 differences | S03 official Markdown lines 1–50 and 146–174 | Correct. Same API, same account/sandbox and 30 days are explicit. Successful effects are skipped; failed/partial work may be retried with an updated response. The overview says v2 lists are eventually consistent by default, so immediate list absence does not universally prove no effect. These are namespace contracts, not all-provider claims. |
| A: durable identity and route switching | S04 lines 31–39, 56–62, 78–93 and the endpoint-scoped v1/v2 contracts | The persistent key recommendation is explicit. The UI/API route-switch conclusion is a supported inference, correctly not presented as measured duplicate frequency. Preserve the exception for a genuinely shared business identity or naturally idempotent state-setting action. |
| B: locators and actionability | S05 parsed-original blocks 95–240; S06 blocks 85–150 | The original recommends user-facing locators/explicit contracts and re-resolves the element before each action. Long structural selectors can break; this does not make every DOM script brittle. Click preconditions and assertions establish only their specified conditions. No comparative maintenance rate is established. |
| B/C: browser session and authority | S07 parsed-original blocks 85–108 | Sensitive saved cookies/headers and shared server-side state limitations are explicit. Context isolation does not itself narrow server permissions; the unit correctly labels that architectural consequence as inference. |
| B: model-directed control and execution | S08 original prose at 774–791, 1222–1291, 1620–1645, 1749–1780, 1943–1987; S09 genuine extracts/live official page as above | OpenAI's completed call status describes generated call completion, not completed environment action. Both integrations make the application execute actions and return observations. Code execution can still be model-directed. No vendor ranking or demonstrated adaptation rate follows. S09 record repair remains necessary. |
| C: scoped API authority | S10 parsed-original blocks 139–172 | GitHub user-token success depends on user and app permissions; installation access depends on app permissions. Endpoint permission documentation and approval of permission changes are explicit. The unit does not assume all API tokens are narrow. |
| C: confirmation and human handling | S12 official Markdown lines 2703–2837, full confirmation/consent section; independent official live page opening | The three confirmation categories are real. Initial specific approval can suffice for the listed uploads/data-use cases; specified actions require action-time confirmation, and specified actions require takeover. The conservative every-script demo is not a universal production rule. “Approved internal workflow” must not silently waive a documented action-specific condition. The eventual example must identify the actual action and recipient, not infer an exemption simply from the word “internal.” |
| C: untrusted source content | S13 parsed-original blocks 235–263, 314–345, 392–410, 426–448 | Indirect content, tools, permission enforcement and limits of filtering/prompt templates are explicit. The API-versus-UI application is a justified inference. The source is security guidance, not a failure-rate sample or proof of perfect resistance. |
| C: API operational burden and cost | S11 parsed-original blocks 285–337; S08 original lines 1222–1226 | GitHub documents polling, request pacing, limits, conditional reads and repeated-error handling, including private-resource 404s. These support nonzero integration obligations, not a route's measured total cost or superiority. No numerical cost calculation is supplied in the reviewed units, so none has been validated. |

## Conditions to preserve in the complete report

The route taxonomy is an analytical definition: fixed control logic and model-selected actions can coexist in one product. The hybrid recommendation is conditional on action scope and sufficiently authoritative completion evidence. The proposed support workflow remains hypothetical; unique generation identity and a trustworthy completion observation must be stated as assumptions unless supported by a selected product's actual contract.

For an exact Anthropic implementation description, use “stop the remaining actions in the batch after the first failure.” The official current text instructs that every later block is not executed; “dependent actions” should not imply that the executor may continue other remaining blocks. This is an exactness condition for assembly, not evidence of a second failed substantive premise.

The [OpenAI integration guidance](https://developers.openai.com/api/docs/guides/tools-computer-use-integration#handle-user-confirmation-and-consent) is current undated guidance as retrieved on 5 November. Its scope must stay attached to that integration. No feature launch date, universal approval-before-every-click rule, or exemption for all recurring work follows from it. The report must not convert supplier limitations or mechanism documentation into measured reliability, successful-case cost, or labor savings.

## Reading record and file integrity

I read the four analysis/note files in full. For originals, the exact sections above were read; code-heavy installation examples unrelated to these premises were not executed or claimed as tested. HTML sources were opened locally and their text extracted with the standard-library HTML parser while excluding script/style content. “Parsed-original blocks” means nonempty normalized text blocks, retaining paragraph/heading/list/table-row boundaries, not source-summary bullets. The chapter names identify the same passages independently of extraction numbering.

The complete `originals/retrieval.jsonl` was read. All 17 currently recorded original files were rehashed and match their recorded SHA-256 values; content examination separately detected the S09 access-failure pages. Hash agreement is not a content-validity verdict. Dates and versions used here are no later than 5 November 2026; undated live pages are evidence of the retrieved state, not of when each feature first existed. No products were installed or tested, as required.

The tables appended below bind this assessment to file versions and actual recorded retrieval times. This local premise review is complete, with EN-E1 open. It does not replace the future evidence review of the entire assembled report.


### Input versions and retrieval metadata

Hash verification time: 2026-11-05T04:18:46.320408+00:00.

| Input | SHA-256 |
| --- | --- |
| requirements.md | `66963099ceabceb3fd420d26167b8d8f2a2dc0e9a669539e69d6f06116bfeeb9` |
| api-or-browser-en/analysis/A-completion-retry.md | `e938c5a0ecb74efca5b16c0a22e974b59ada4b44127caa885e7222231e6e0a74` |
| api-or-browser-en/analysis/B-browser-mechanisms.md | `e9d381c8a7ae643779b5f7b440878176111a12b4b64bf70cbfdfe240df7fe9d7` |
| api-or-browser-en/analysis/C-authority-operations.md | `a69bb061148dbad7d859307fc3c8f3f2d853abcd77de33eb53754f60d5c12bdf` |
| api-or-browser-en/source-notes.md | `000238562c091ab64a148f0d3356d7392fbfa6324051d8c0f2dec519b11c2e10` |

| Actual source file (scope above) | Recorded retrieval UTC | SHA-256 |
| --- | --- | --- |
| S01.original.txt | 2026-11-05T04:05:28.9255909Z | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| S02.original.md | 2026-11-05T04:06:17.2024788Z | `fd3d6f889a557f5535d7ac5e5e79c1898ac378b287c45e56a67880b5e5318ee3` |
| S03.original.md | 2026-11-05T04:06:18.1714487Z | `2117bce4ef2a6410a78669a1f723457cca55052d4cebe5724913ba735e869cac` |
| S04.original.md | 2026-11-05T04:06:18.9497863Z | `9ab2e69e934255a1a5fe8fc6f86136d8ebfaa73ea7a625889adbf5711efac41e` |
| S05.original.txt | 2026-11-05T04:05:36.0987899Z | `643e2efba60916c4b276d9b23e7eba115212b00111fbec97f9e3fd74c63dcdf7` |
| S06.original.txt | 2026-11-05T04:05:37.7063014Z | `a908a515e19a8489aebc04752c39e32c07601288120297bb4d0b2ee9c0d436e1` |
| S07.original.txt | 2026-11-05T04:05:38.1102269Z | `dac89a341e9a518fa9e74947262221f64398aacb75befa9b92c8682797b07424` |
| S08.original.txt | 2026-11-05T04:05:38.5621223Z | `a786fd3863e3a019514f85bfbbd9b4059e031a2186a89d99425d0fab64112e46` |
| S09.original.txt | 2026-11-05T04:05:40.2701303Z | `869f86820c07a85bd46de150eb221e97c2af0a9399f5d6b710dec618e5e61016` |
| S09.original.md | 2026-11-05T04:06:19.7255864Z | `4511bf126724ae4780e93320f275598043fe8dce50470d57cc7f500315cd01b2` |
| S10.original.txt | 2026-11-05T04:05:44.6441884Z | `7538a5e922849b4c8a8a8a7425926cd8dd63fb02c9af5398d95558fd32751a89` |
| S11.original.txt | 2026-11-05T04:05:45.0614585Z | `ca5091fab3dda8eba0f18b6f29f258c9cfbe98ef8ff98dfc4672de0575cb98a2` |
| S12.original.txt | 2026-11-05T04:09:02.8565170Z | `1ab928c4185705c3033321b706fdb7678d1368ad05d24390b302b7619522a28b` |
| S13.original.txt | 2026-11-05T04:09:03.8487917Z | `50874d6c26cb9d528d20feacc09325bab9fbc131c106a97fdc48a6185b3d19c4` |
| detail-web-output-1.txt | Retrieved 2026-11-05 according to saved tool output; exact timestamp not present in file | `7aa81b50d2524af8b47ee71ca859484d218a761f75b090f2c1719ff53e32b1d1` |
| detail-web-output-2.txt | Retrieved 2026-11-05 according to saved tool output; exact timestamp not present in file | `80542d00bbca75d6b7f48bf17cc95454734a4726c7bad91e58be197e130df0f5` |

## Repair verification: EN-E1 resolved

The author returned a narrow source-capture repair in the same review context. I read the revised Unit B in full, checked the changed Unit A opening and S09 source-notes entry, read S09.web-capture-metadata.json and the appended retrieval correction, and inspected the actual six new web-tool capture files and their numbered extraction. The old assessment above remains the original record.

All six captures carry the official documentation title/URL. I independently combined their actual numbered lines: the union covers every line 0–1073, with no missing line and no conflicting overlapping text. S09.web-numbered-text.txt exactly matches that union. I read the saved affected passages at 267–282, 598–617 and 792–801, alongside the already-read environment/loop and live official source. The batch rule now preserves all remaining calls, without extending it to unrelated work. A and B no longer describe the regional-unavailability responses as successful documentation retrievals; source-notes identifies the successful text route correctly.

Both original failed responses retain their previously verified hashes. The successful source is explicitly identified as web-tool text rather than HTTP HTML. The six captures record retrieval start at 2026-11-05 04:18:18 UTC; retrieval.jsonl records the correction at 04:19:41.2167977Z. This meets the original-text retention requirement for this source. **EN-E1 is resolved.** The existing A–C premises may be used with the qualifications above. Whole-report evidence review remains outstanding.

Verification recorded: 2026-11-05T04:22:45.043728+00:00.

| Reviewed repair artifact | SHA-256 |
| --- | --- |
| analysis/A-completion-retry.md | `a3d7aa3db6598f3094d8dd4f4043bcdf0b82726e9f8b50db7273405f01782f3b` |
| analysis/B-browser-mechanisms.md | `048b4b5dd103eaaea16cc74336abd26ec187c19b8fcc65dfae013823689f9f93` |
| source-notes.md | `a8843d72f54c3587764f83f081119bd0e7a0ce15ecc6b5370ed205d91ee331bc` |
| originals/S09.web-capture-metadata.json | `c4439b75b87ee7d0f0fd0ed0de42190945ede55913f984c7457d8d0bbff7b739` |
| originals/retrieval.jsonl | `55b2ff1885205d7d7d673222c1693a2f52adee2566b75c52d6fccf44b49380d1` |
| originals/S09.web-numbered-text.txt | `0079e2bbf6f4ef69f8d7b691d7cdfdf2d265bb80d256a881ab5a7324530fe01e` |
| originals/S09.web-original-180.txt | `2d4dfcc7fea0bff69db0fc0f68916757f880a2b48c957e3a525e651eb0ed9e40` |
| originals/S09.web-original-330.txt | `84bc3c60074df783804d10b258a858ca42ff4ca522a5473386e23d75f6dbfce9` |
| originals/S09.web-original-480.txt | `25d7f9a59e2cae0bd10e49e5662615a78bf67b9b5249fdb67068a3e796935d1c` |
| originals/S09.web-original-630.txt | `b06a57ad4703c8681d5cf90f00d47a7c775ea6d0242696abf2b1a69851baabd1` |
| originals/S09.web-original-780.txt | `89de9cb63ee7cd776e8db09efdc685e015455c3989114edd5e1af25cc396ce65` |
| originals/S09.web-original-930.txt | `3f4e7f42944ad0dea52c05da190f7b80c4bcc6c432dc62639da051dc9eb80ab9` |
| originals/S09.original.txt | `869f86820c07a85bd46de150eb221e97c2af0a9399f5d6b710dec618e5e61016` |
| originals/S09.original.md | `4511bf126724ae4780e93320f275598043fe8dce50470d57cc7f500315cd01b2` |

### Effective requirement clarification

At 2026-11-05T04:23:39.781345+00:00, I read the clarified root requirements (SHA-256 `16b09fc2bbfdeec3d9835b4cf16d853779349f69ad41cd4d8ee6a4a8b99957a8`): retain the original text actually acquired and used, identify excerpt coverage accurately, and obtain additional context only when it could affect the conclusion. This does not reinstate EN-E1. Its concrete content-state defect was that a failed HTTP response was labeled as a documentation original; that label has been corrected, failed responses preserved, and relevant genuine source text retained and checked. The full-page capture is available, but unrelated page or attachment acquisition is not an additional acceptance condition.
