# Old and new tasks: drafting, measurement and Astra acceptance

[English](README.md) · [简体中文](README.zh-CN.md)

Executed on 2026-10-13 with four independent real test tasks: the original Maple storage and Brook rinsing questions, plus new repository-grounded questions on explicit independent-review profile selection and delivery recovery after editing a reviewed report. Original scenario materials keep their provenance. Development use does not invalidate a task or an executed test.

Four API models drafted; programs measured exact length; out-of-range drafts received one targeted revision with the actual count. Astra reviewed complete sources and anonymous reports in separate contexts. Private author notes, model identities and label mappings were withheld. Each task's four reports shared one request, with a separate verdict for each. This tests fixed-source drafting and operational advice; the API calls did not execute MCP or Full state transitions.

## Results

| Author | Initial length pass | Length pass after one targeted revision | First Astra pass | Later maintainer repairs |
| --- | --- | --- | --- | --- |
| deepseek | 2/4 | 4/4 | 1/4 | 3 |
| kimi | 0/4 | 3/4 | 2/4 | 2 |
| glm | 4/4 | 4/4 | 2/4 | 2 |
| longcat | 1/4 | 2/4 | 1/4 | 3 |

Of 16 initial drafts, 7 met length. Nine targeted revisions produced 8 parseable replies and one invalid JSON reply; the failure and original draft were retained. Thirteen reports then met length. First Astra review passed 6 and requested revision for 10. The maintainer corrected those 10: eight new editorial versions passed two Astra requests, and two reused previously accepted same-task repairs after checking identical report, brief and source texts. All 16 final delivery versions meet length and have corresponding passing Astra reviews. **Ten include maintainer edits; this is not a 16/16 provider-first-draft success rate.**

There were 31 new requests: 16 initial authors, 9 measured-feedback revisions, 4 initial Astra batches and 2 editorial-repair review batches. No unchanged retries; the predeclared ceiling was 40. The two reused passes come from the [earlier repair evidence](../../repairs/2026-10-13-astra/README.md) and are not new calls here.

## Findings and repairs

- DeepSeek's storage report reversed budget comparisons and invented a capacity requirement. The recommendation was corrected against the actual quoted numbers and requirements.
- LongCat's rinsing report turned unrecorded soil composition into an observed change and remained too long. The repair restores the unknown status and meets the original length rule.
- New-task reports omitted actual acceptance steps or wrongly exempted unchanged required review scopes from current-artifact review. Repairs complete the required revision and delivery steps.
- One LongCat revision contained an invalid JSON escape. The original response remains a format failure; parsing was not relaxed.
- The initial driver removed source path metadata from judges while authors received it, causing one false provenance finding in the profile task. `repair-plan.json` records this input mismatch. Changed-report reviews receive the same full sources as authors, including provenance. Original judgments remain; other confirmed findings were repaired normally. Identity masking must not remove necessary evidence.

This supports concrete repair and role allocation, not a with/without Toolkit effect estimate. The October 12 four-author/Astra-judge allocation was already correct. The earlier October 13 eight-call diagnostic lacked Astra content acceptance; this recheck adds actual old/new-task acceptance without invalidating or overwriting previous results.

## Files and verification

`plan.json` and `commitment.json` retain the pre-call plan. `authors/` stores original/revised requests, replies, parsing and measurements; `judges/` keeps first reviews; `repairs/` and `repair-judges/` contain editorial versions and rechecks. `summary.json` maps every final version to its text hash and review. Drivers are execution snapshots, including the original metadata-masking mistake; the separate repair driver corrects it. `manifest.json` hashes every public file; only local account names in CLI diagnostics are redacted.

From the repository root, run `python evals/diagnostics/2026-10-13-targeted-recheck/verify.py` for offline file, request-count, length, report/review and summary checks. It makes no model calls.
