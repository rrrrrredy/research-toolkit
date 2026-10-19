# Four report revisions and result corrections

[English](README.md) | [简体中文](README.zh-CN.md)

On October 19, 2026, four reports were revised using their existing briefs and four-source synthetic packs. The originals contain repeated passages, sometimes with off-topic templates. Their author's qualified/pass descriptions and `reader_edit: passed=true` conflict with the prose and must no longer be cited as quality passes. Original reports, self-checks, sources, batch summaries and mechanical outcomes remain in the [original run archive](../../studies/2026-10-19-external-batches/README.md).

## Revised reports and changes

| Report | Original → revised length | Changes and passages checked |
| --- | --- | --- |
| [Predictive-maintenance subscriptions](reports/iIoT-predictive-maintenance-arr-zh-20261016.md) (Chinese) | 3081 → 3453 non-whitespace characters | Removed repeated and unrelated guide-fund language. Sections 1 and 3 use S1/S2 to distinguish prepayment from renewals, proposed terms from agreed protection, and calculations from quoted totals. Section 4 uses S3 to separate downtime, load and alarm denominators. Sections 5–6 retain the noncritical-workshop counterexample and procurement choices. |
| [Guide-fund investment and exits](reports/guide-fund-hardtech-return-ratio-zh-20261016.md) (Chinese) | 3056 → 3629 non-whitespace characters | Removed repeated conclusions. Sections 1 and 4 use S1: 118% versus 81% is a 37-percentage-point difference; nine exited or proposed-exit investments are not nine cash realizations. Section 2 keeps S3's consultation proposals distinct from current rules. Sections 5–6 retain S4/S2's local activity and policy/financial tradeoff. |
| [Scope-3 factors in RFQs](reports/scope3-factor-rfq-evidence-en-20261016.md) | 1501 → 1787 whitespace words | Removed recurring instructions about a passing memo. Sections 1 and 3 use S1/S2 to distinguish screening, specific estimates and assurance, with the three-year and top-20% proposals labelled as internal drafts. Sections 2 and 4 match S3/S2 failures to remedies and reproducible calculations. Section 6 preserves S4's screening counterpoint and labels the 2027 outlook as a forecast. |
| [LLM credit-memo drafting](reports/regional-bank-llm-credit-memo-controls-en-20261016.md) | 1521 → 1788 whitespace words | Removed shared filler. Section 2 keeps S3's 9/120=7.5% and 6/120=5% at the recorded section level. Sections 3–5 use S2 to distinguish unsupported numbers, softened risk, stale covenants and human repair; eight weeks do not document the required sixty days, and no missing threshold is invented. Sections 6–7 apply S4's scope distinction to actual workflow effects. |

The revision author read all four current reports against their S1–S4 sources. The table records concrete passages, calculations and limitations checked rather than generic assurances. Each report retains counterevidence and decision-relevant missing information, with links to original sources. Repeated self-check instructions have been removed from the report bodies.

Counts cover the whole Markdown file, including headings, tables and citations. The briefs require at least 3000 non-whitespace characters for Chinese and 1500 whitespace words for English, with suggested bands of 3000–5000 and 1500–2500. These are report repairs: no research runs were repeated, no new `finish.json` receipts were produced and no evaluation runs were added. They are not a Toolkit core-capability upgrade.

## Provenance

The original predictive-maintenance report repeats an unrelated province/guide-fund passage at lines 39 and 51. The Scope-3 report repeats the paragraph beginning “For decision-makers, a passing long-form memo” at lines 37, 49, 61, 73, 85 and 97; the credit-memo report also reuses it. Yet the corresponding `finish.json` contains the generic reader-edit evidence “Readable source titles; no workflow narration or internal paths in body.”

The [October 16 brief](../../studies/2026-10-19-external-batches/batches/2026-10-16-confirmed/DAILY_BRIEF.md) separates research execution from the ingest agent. [PR #80](https://github.com/rrrrrredy/research-toolkit/pull/80) is an ingest PR with Cursor agent provenance. The defects are present in its archived originals, not established as ingest-time changes. Shared wording suggests a reused template or length-padding process, but the archive lacks the generation script, full writing commands and model-call receipts needed to establish the exact cause or attribute it to a Grok call. October 17's six outer Grok notes do not cover these four October 16 reports.

The [copyable Grok investigation prompt](grok-self-audit.zh-CN.md) (Chinese) asks the bot to inspect its own execution records without assuming a cause or reconstructing missing logs.

## Actual Toolkit changes

The existing six-item checklist, fields and validation predicates stay unchanged. `profile_policy.py` instructions and diagnostics now ask for concrete report/source locations and findings, with unresolved items remaining false. They replace the bare instruction to supply `passed=true`; changing the flag is not a repair. The reader-edit item and bilingual Lite guide explicitly cover reading the complete report for repeated and off-topic passages. No checker, reviewer or call step was added.

Bilingual READMEs, plugin descriptions and homepages now describe the nine MCP tools actually registered; resources and prompts are not tools. Packaged guidance is synchronized. This removes a misleading completion cue; this round does not measure a reduction in false self-reported passes or claim automatic detection of all prose defects.

## Verification

Each check below was run once and succeeded:

- `python -m py_compile scripts/profile_policy.py plugins/research-toolkit/scripts/profile_policy.py`: affected code compiles.
- `python scripts/build_plugin.py`, then `python scripts/build_plugin.py --check`: generated and verified 46 shared plugin files.
- `python scripts/build_site.py`, then `python scripts/build_site.py --check`: generated and verified bilingual site files.
- `python evals/studies/2026-10-19-external-batches/verify.py`: existing archive verification passed. Only the two README hashes were updated; original-file hashes, twelve runs and freeze commits remain unchanged.

No research task, additional review or full test suite was run. The effect of the wording change on subsequent agent self-check behavior has not been measured in this round.
