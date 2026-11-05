# Independent full-report review: process language

- Perspective: `process_language`
- Execution context: `/root/case_process_full`; separate from production of either report. No other initial review or author self-check was read.
- Recorded at: 2026-11-05 07:17:09 UTC
- Verdict: pass for this perspective. Required corrections: 0. Optional edits: 0.
- Applicable requirement: keep production logs out of public prose while retaining methods, source attribution, uncertainty and operational detail needed to answer the reader's question.

## Actual reading and version

I read the complete current `requirements.md`, `requirements-clarifications.md`, the role instructions in `references/subagents-and-review-loop.md`, and the public case's `brief.md`. I did not read other reviews, author self-checks or revision responses.

I read `report.md` in full, lines 1–102: the opening, all six sections, route table, support scenario, cost formula and final source note. I then read the complete website `report.html`, lines 1–167, including navigation, contents, table cells, article text and link labels. This was a Markdown and HTML text review, not a browser-layout test. No linked external original was reopened; the present assignment assesses whether the language belongs in reader-facing prose, rather than independently checking the underlying technical claims.

| Read or checked artifact | SHA-256 |
| --- | --- |
| Task `api-or-browser-en/report.md` | `15A3EE49392069F8187759EEC7B889EEBF9365D7424D0C08A59B3B6221A8CF91` |
| Website `docs/case-study/api-or-browser-2026-11/report.md` | `15A3EE49392069F8187759EEC7B889EEBF9365D7424D0C08A59B3B6221A8CF91` |
| Website `docs/case-study/api-or-browser-2026-11/report.html` | `D3A4E2E0CE6F4E552C11269EE9B4D1FAD1C5BB537F591503A7984EF045399DDA` |

The website Markdown matches the fully read task report by hash. HTML anchors below correspond to the Markdown line numbers.

## Located observations

| Location | Observed language and classification | Reader impact | Disposition and severity |
| --- | --- | --- | --- |
| Lines 3–9 and 102; HTML `#L3`, `#L9`, `#L102` | The date, documentation basis, distinction between design judgment and measured ranking, hypothetical-scenario label and absence of a deployment or comparative trial define the evidence boundary. They do not describe tools used to write the article, delegation, review progress or failed research attempts. | Prevents the recommendation and scenario from being mistaken for a measured production comparison. | Retain. No defect or required edit. |
| Lines 24–40; HTML `#L24` through `#L40` | HTTP status, Playwright action checks, a computer call's `completed` status and application-side execution describe the mechanisms being compared. The quoted instruction “attach this document to this ticket” is a functional example, not an excerpt from this research session's assistant dialogue. | Makes the difference between an interaction, a generated tool call and a finished business operation explicit. | Retain. No process-language leak. |
| Lines 44–54; HTML `#L44` through `#L54` | Same-key retries, process restarts, saved identifiers, unresolved state and the model's conversation concern an enterprise agent's recovery design. “This is an architectural inference” at line 52 labels the status of a consequential conclusion; it is not an author response to review. | Preserves the contract assumptions that determine whether a resumed write is safe and distinguishes documented behavior from inference. | Retain. No defect. |
| Lines 58–66; HTML `#L58` through `#L66` | Permissions, external content, confirmation and human handling are properties of the proposed integration and cited provider requirements. They do not import this author's own approval workflow or internal research constraints into the reader's system. | Explains why route selection depends on actual authority and the specific interruption. | Retain. No defect. |
| Lines 70–84; HTML `#L70` through `#L84` | Ticket/customer IDs, job records, a request revision, one worker owning an attempt and handoff to a support operator all belong to the explicitly hypothetical support workflow. No actual internal research ID, local path or production-agent identity appears. | The detail is necessary to follow partial completion across an interrupted document-generation step. Removing it would obscure the example's recovery logic. | Retain. No defect. |
| Lines 88–100; HTML `#L88` through `#L100` | Cost accounting, a bounded pilot, expected results and migration conditions are reader recommendations answering the route-choice question. The text calls the formula a proposal and does not claim the present research executed such a pilot. | Supports a local decision without inventing measured savings or a universal ranking. | Retain. No defect. |
| HTML line 2 and the final source link | “This research archive” and “Historical case” are public navigation. `L11` and similar attributes are section/paragraph anchors, not visible review IDs. `source-notes.md` is a portable public reference. The full article contains no production log, local absolute path, session identity, reviewer status or conversational progress update. | Readers can navigate the article and its evidence notes without being exposed to the research team's execution history. | No edit needed. No defect. |

Required corrections: none. Optional changes: none identified for this perspective. This verdict concerns process-language removal in the bound report versions; it does not stand in for other review perspectives or establish a general benefit from the Toolkit.

