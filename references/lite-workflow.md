# Historical checklist-task compatibility

Only for resuming saved `profile=lite` tasks, not a separate research entry. Use the [complete shared methods](../SKILL.md) for research, analysis and writing. Preserve the saved completion requirements; do not relabel author checks as independent review.

## final — Complete the author checklist

Read the complete current report against the brief and material follow-ups before filling the checklist. Record the passages/sources checked and actual findings or corrections; copying a criterion such as "edited for the reader" is not evidence. Keep failed or unchecked items false until the work is done. A checklist error asks you to complete the work, not merely change `passed` to `true`. Each of the six items refers to this report:

| Key | What to check |
| --- | --- |
| `requirements` | Required questions, follow-ups, format and length are satisfied; record the actual length and counting convention. |
| `claims_and_sources` | Important claims and citations match the sources actually read. |
| `counterevidence` | Counter-evidence and uncertainty are addressed at the affected conclusions. |
| `sections` | Each necessary section explains its own point and covers the brief without repeated filler. |
| `reader_edit` | Check the full current report and reject duplicated filler or repeated boilerplate paragraphs, and cross-task or off-topic template text used to pad length. The report is useful to the named reader and excludes production records; identify the passages checked and any corrections. |
| `limitations` | Material evidence limits and the absence of independent review are disclosed. |

With tools, call `research_finish` with the task, artifact and intended delivery message to get the checklist template. Submit every item's `passed` and `evidence` after checking; only actual passes use `passed: true`. The tool saves `state/final_checklist.json`. New receipts bind the report, delivery message, task specification, source/claim registries, requirement ledger (including its absence), and declared local files for sources marked read. An item may also declare `evidence_files: ["checks/length.md"]` for a retained check note; these task-relative, nonempty files are bound too. Workflow output files cannot serve as those check notes. Address any returned error before claiming completion; recheck and resubmit after any bound input changes. A remote URL or page locator remains a recorded reference, not a downloaded or monitored source. Older receipts retain their original report/message-only checks.

For an agreed whole-file word/character range, record a `length_constraint` in the existing requirement ledger before drafting: `unit` is `whitespace_words` or `nonwhitespace_characters`, `scope` is `whole_artifact`, and `min` and/or `max` are inclusive integers. Keep the actual agreement in the row's `summary`, plus its ID, status and evidence. Finish returns/recomputes `length_checks`, including Markdown and references. Do not translate body-only/page limits into this scope or invent a minimum; those need the appropriate manual measurement. An explicit range check does not establish research depth. See [the counting contract](../docs/delivery-verification.md#explicit-length-requirements).

Without tools, deliver the report, separate source/claim records and checklist, and state that no local receipt was generated. In either path the checklist records the author's checks; it is not independent review or automatic proof that the report is correct.
