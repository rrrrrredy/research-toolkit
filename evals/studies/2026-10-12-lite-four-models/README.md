# Four-model Lite development diagnostic — 12 October 2026

[English](README.md) | [简体中文](README.zh-CN.md)

This run does **not establish a Toolkit quality benefit**. It completed 72 first requests (40 authors, 32 judges) within a frozen ceiling of 80. Four LongCat format failures left four of 20 model-task pairs unresolved. Among 16 judged pairs, six changed preference after swapping A/B; 21 dimension scores changed. All first results remain unchanged.

| Author | With Toolkit preferred | Without preferred | Tie | Unresolved | Swap agrees / judged |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek `deepseek-flash` | 2 | 3 | 0 | 0 | 3 / 5 |
| Kimi `kimi-k2.6` | 1 | 3 | 1 | 0 | 4 / 5 |
| GLM `glm-5.3` | 1 | 1 | 3 | 0 | 3 / 5 |
| LongCat `LongCat-2.0` | 1 | 0 | 0 | 4 | 0 / 1 |

These are the **first primary judge preferences**, not source-validated winners, a model ranking or an effect estimate. A relative preference can select a report that still contains major defects. Missing pairs stay in each model's five-pair denominator; swapped judgments are sensitivity checks, not extra samples.

## Design and execution

[Plan](batch-plan.json), [commitment](batch-commitment.json), per-provider `coordinator/frozen.json` and archived `code/*.py.b64` preserve the pre-call inputs. Toolkit base: `422b437169e609b94c16087c65fdd68a83ad0ca4`. Five public, implementation-authored synthetic task families cover units, conflicting measurements, causal identification, constrained choice and temporal synthesis; three are English and two Chinese. Four providers do not turn five families into twenty independent tasks. Inputs were already development-exposed, not held out.

Authors received fixed sources, with/without Toolkit instructions, using the same model, output format, thinking setting and token/time limits within each pair. Toolkit adds instruction tokens: this is not a token-matched comparison. No retrieval, persistent task files, MCP execution or Full workflow was tested. GLM used enabled thinking/low effort; other authors disabled thinking. Each stratum completed ten authors before judging; incomplete pairs skipped both judgments. Four strata could overlap. No retries or outcome-dependent additions occurred.

The single judge requested `gpt-6-astra` in fresh Codex contexts, after the separate [calibration](../../diagnostics/2026-10-12-astra-calibration/README.md). Native events do not attest the returned model identity. They retain usage and execution evidence. Limits of 4,096 output / 30,000 total tokens are checked after return, not hard generation or billing caps. See [native transport](../../../docs/native-judge.md).

## What the evidence supports

- Format: 36/40 author replies parsed. LongCat changed the exact notes marker three times and omitted it once. Its two Toolkit and two baseline failures span four pairs. They were not repaired, quality-scored or replaced.
- Length: 6/18 valid Toolkit reports and 8/18 valid baseline reports meet the brief's range. Count the complete reader report, including headings, Markdown and citations: whitespace words for English; non-whitespace Unicode characters for Chinese. All 15 format-valid Chinese reports exceed 500 characters. Failed-format reports have no extracted-report length result.
- Source checks: examples include recommending a 26-unit option against a 24-unit budget, treating next-year forecasts as current requirements, changing an accuracy threshold to require uncorrected output, and turning unknown soil mix into a known change. [Adjudication](source-adjudication.json) records concrete findings for all 36 valid reports. The implementation assistant authored the tasks and knew conditions: this is **not independent human validation** or exhaustive certification of every dimension.
- Judge limits: the swapped Kimi water judgment incorrectly calls the 177-word baseline within the 180–260 range. Other stated counts use varying scopes. Mechanical counts in [analysis](analysis.json) supersede those length assertions, without changing any original score or preference.
- Masking: packets contained only brief, sources, rubric and verbatim A/B reports; notes, assignments, task designs and logs were excluded. Three DeepSeek Toolkit reports nevertheless disclosed independent-review status. Literal detections and all judge `condition_clues` remain available. Formatting may provide additional clues; successful metadata separation does not prove successful blinding.

Author usage totals 312,893 provider-reported tokens. Native judge events report 372,564 input and 71,224 output tokens; cached/reasoning fields are subcategories, not extra totals. [Analysis](analysis.json) retains provider-level usage and sums of local request elapsed time. Concurrent sums are not wall-clock duration; no monetary cost is inferred from incompatible provider fields or unknown rates.

## Preservation and reproduction

All successes, failures, raw responses/events, parse rules, reports/notes, judge packets, first-judgment locks and results are public. Account-name occurrences in native warning events are replaced with `<LOCAL_USER>` only. Code is base64 of exact execution bytes to preserve CRLF. [Public manifest](public-manifest.json) records original/public hashes and every transformation. Other bytes remain unchanged; input READMEs and pending-adjudication labels are historical snapshots, not current status pages. Hashes check correspondence, not trusted timestamps or semantic truth.

Run `python scripts/check_development_evidence.py --self-test` from the repository. It is read-only, makes no model calls and includes seven mutation/retention controls. `python scripts/summarize_development_pilot.py --root evals/studies/2026-10-12-lite-four-models` reconstructs the complete analysis without rewriting artifacts.

The separately frozen [LongCat JSON probes](../../diagnostics/2026-10-12-longcat-format/README.md) passed format in 3/4 replies. They do not fill missing pairs or establish a stable replacement format. Follow-up work targets prompt/schema alignment, short-report space allocation and constraint-to-recommendation consistency; any validation uses new frozen samples and preserves this run.
