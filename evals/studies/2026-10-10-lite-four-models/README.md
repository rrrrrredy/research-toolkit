# Four-model fixed-source Lite pilot — 2026-10-10

[English](README.md) · [简体中文](README.zh-CN.md)

This prospective development pilot ran **five task families under four author models**: three original English briefs and two original Chinese briefs. Each same-model pair used the same brief, source text and resource ceilings, with randomized generation order and A/B presentation. It tests one-response, instruction-only Lite, without retrieval, MCP, persistent state or Full review gates. The findings do not establish a general Toolkit quality advantage.

## Judgment coverage

**All 20 model–task pairs now have complete reports and recorded judgments.** Twenty additional author requests and ten judgments completed the ten previously unjudged pairs; the other ten retain their existing judgments. All original 40 author attempts and failures remain intact. This table describes coverage, not a pooled primary effect estimate across three analysis stages; there are still only five task families.

| Author | Judged pairs | Original primary | Fence-only supplement | Regeneration supplement |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 5 / 5 | 2 | 0 | 3 |
| Kimi | 5 / 5 | 0 | 5 | 0 |
| GLM | 5 / 5 | 0 | 3 | 2 |
| LongCat | 5 / 5 | 0 | 0 | 5 |

Preferences vary across models and tasks; complete judgment coverage is not a general Toolkit advantage. [completion-summary.json](completion-summary.json) identifies every pair's provenance, and [coverage-scores.csv](coverage-scores.csv) contains dimension scores for all 20 pairs.

## Primary results

All 40 first author requests are retained. Failures and malformed output remain unresolved, not zero-quality scores or wins for the other arm. Preference counts below come from the first unadjudicated LLM judgments; the same five families are repeated across model strata, so this is **n=5 families**, not 20 independent tasks.

| Author | Toolkit preferred | Baseline preferred | Ties | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 0 | 1 | 1 | 3 |
| Kimi | 0 | 0 | 0 | 5 |
| GLM | 0 | 0 | 0 | 5 |
| LongCat | 0 | 0 | 0 | 5 |

Author execution details: DeepSeek: 3 truncated responses, 1 strict-JSON parse failure; Kimi: 10 strict-JSON parse failures; GLM: 9 strict-JSON parse failures; LongCat: 6 timeouts/deadline failures, 2 strict-JSON parse failures. See the raw execution/invalid records; completed HTTP requests can still fail parsing.

## Separate format supplement

After observing author parsing failures, an [explicit post-hoc policy](format-supplement-policy.json) allowed removal of exactly one enclosing Markdown code fence around an otherwise valid JSON response. Both author executions must have completed; at least one needs that transformation; the pair must not already have a primary judgment. It does not repair JSON syntax, alter report text, regenerate authors or retry judgments. The policy applies equally to all four models. Primary results above remain unchanged.

| Author | Eligible pairs | Toolkit preferred | Baseline preferred | Ties | Unresolved eligible pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek | 0 | 0 | 0 | 0 | 0 |
| Kimi | 5 | 3 | 1 | 1 | 0 |
| GLM | 3 | 1 | 2 | 0 | 0 |
| LongCat | 0 | 0 | 0 | 0 | 0 |

The supplement admitted 8 previously unjudged pairs and made no new author calls. These are supplemental diagnostics on the same families, not additional tasks or a replacement primary result. [Derivations and original response hashes](format-supplement/) connect every eligible report to its first response. The policy was recorded after format failures and before inspecting any judgment preferences; it was not part of the original frozen analysis.

## Separate regeneration supplement

The [completion plan](completion-supplement/plan.json) was frozen locally before new calls. It selects only the three DeepSeek, two GLM and five LongCat pairs still lacking a valid judgment. Both arms were regenerated for each selected pair; no new report was paired with an old report, and no valid existing judgment was rerun. There were no preference-based retries, and original failures were not relabeled successful.

| Cause | Original evidence | Matched change in both arms |
| --- | --- | --- |
| DeepSeek reasoning exhausted the completion budget | Three `finish_reason=length` responses reached 12,288 completion tokens | Enlarge the ceiling and use documented `reasoning_effort=low` ([API reference](https://api-docs.deepseek.com/guides/thinking_mode/)) |
| Markdown escaped incorrectly inside JSON | Unescaped quotations in GLM battery reports and control characters in its banking report; removing fences alone cannot fix these | Separate raw Markdown and working notes with one delimiter line, preserving report text without JSON repair |
| LongCat client deadlines | Six reads failed at about 240 seconds without a complete response or usage | Keep thinking enabled and enlarge the token ceiling and deadline ([API reference](https://longcat.ai/platform/docs/zh/api/chat)) |

All regenerated arms use the Markdown/notes delimiter, 32,768 completion tokens, 131,072 total tokens and a 1,200-second deadline. DeepSeek and GLM use low reasoning effort; LongCat explicitly enables thinking. Kimi was not regenerated. Model, brief, sources, pinned Toolkit text and rubric remain the same; seed `2026101002` independently randomizes run order and A/B presentation. [completion-usage.csv](completion-usage.csv) records actual usage. Judge settings remain unchanged; author outputs lock before judging, and judgments lock before labels are decoded.

For example, the [regenerated LongCat Toolkit banking report](completion-supplement/longcat/authors/pair-01/with_toolkit/execution.json) used 30,563 completion tokens and 572.453 seconds, exceeding both original per-call ceilings. Successful completion here does not demonstrate completion under the original budget.

| Author | Regenerated pairs | Toolkit preferred | Baseline preferred | Ties | Unresolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek | 3 | 0 | 3 | 0 | 0 |
| GLM | 2 | 1 | 0 | 1 | 0 |
| LongCat | 5 | 2 | 3 | 0 | 0 |

These are post-hoc results under changed formatting, resource ceilings and some reasoning settings. They do not replace the primary analysis or constitute held-out validation or new independent samples. Factual, length and reasoning defects did not trigger report rewrites, and judgment preferences did not trigger rejudging.

| Author / task | Toolkit report | Baseline report | Judgment preference and reasons |
| --- | --- | --- | --- |
| DeepSeek / `ai-risk-adoption-zh` | [Markdown](completion-supplement/deepseek/authors/pair-04/with_toolkit/report.md) | [Markdown](completion-supplement/deepseek/authors/pair-04/without_toolkit/report.md) | [without_toolkit](completion-supplement/deepseek/judgments/pair-04/parsed.json) |
| DeepSeek / `battery-market-en` | [Markdown](completion-supplement/deepseek/authors/pair-05/with_toolkit/report.md) | [Markdown](completion-supplement/deepseek/authors/pair-05/without_toolkit/report.md) | [without_toolkit](completion-supplement/deepseek/judgments/pair-05/parsed.json) |
| DeepSeek / `memory-roadmap-en` | [Markdown](completion-supplement/deepseek/authors/pair-01/with_toolkit/report.md) | [Markdown](completion-supplement/deepseek/authors/pair-01/without_toolkit/report.md) | [without_toolkit](completion-supplement/deepseek/judgments/pair-01/parsed.json) |
| GLM / `banking-chatbots-en` | [Markdown](completion-supplement/glm/authors/pair-05/with_toolkit/report.md) | [Markdown](completion-supplement/glm/authors/pair-05/without_toolkit/report.md) | [with_toolkit](completion-supplement/glm/judgments/pair-05/parsed.json) |
| GLM / `battery-market-en` | [Markdown](completion-supplement/glm/authors/pair-04/with_toolkit/report.md) | [Markdown](completion-supplement/glm/authors/pair-04/without_toolkit/report.md) | [tie](completion-supplement/glm/judgments/pair-04/parsed.json) |
| LongCat / `ai-risk-adoption-zh` | [Markdown](completion-supplement/longcat/authors/pair-04/with_toolkit/report.md) | [Markdown](completion-supplement/longcat/authors/pair-04/without_toolkit/report.md) | [with_toolkit](completion-supplement/longcat/judgments/pair-04/parsed.json) |
| LongCat / `banking-chatbots-en` | [Markdown](completion-supplement/longcat/authors/pair-01/with_toolkit/report.md) | [Markdown](completion-supplement/longcat/authors/pair-01/without_toolkit/report.md) | [without_toolkit](completion-supplement/longcat/judgments/pair-01/parsed.json) |
| LongCat / `battery-market-en` | [Markdown](completion-supplement/longcat/authors/pair-02/with_toolkit/report.md) | [Markdown](completion-supplement/longcat/authors/pair-02/without_toolkit/report.md) | [without_toolkit](completion-supplement/longcat/judgments/pair-02/parsed.json) |
| LongCat / `memory-roadmap-en` | [Markdown](completion-supplement/longcat/authors/pair-05/with_toolkit/report.md) | [Markdown](completion-supplement/longcat/authors/pair-05/without_toolkit/report.md) | [without_toolkit](completion-supplement/longcat/judgments/pair-05/parsed.json) |
| LongCat / `productivity-outlook-zh` | [Markdown](completion-supplement/longcat/authors/pair-03/with_toolkit/report.md) | [Markdown](completion-supplement/longcat/authors/pair-03/without_toolkit/report.md) | [with_toolkit](completion-supplement/longcat/judgments/pair-03/parsed.json) |

## Reading the judgments

The retained banking-chatbot judgment preferred the DeepSeek baseline for a more explicit bounded pilot and stopping criteria, while crediting the Toolkit report with stronger security-mechanism coverage. A simple whitespace count is 913 versus 785 words, including headings, for a 600–800-word brief. In the GLM productivity supplement, the preferred Toolkit report still misstates the manufacturing historical baseline as 1947; the supplied BLS narrative says 1987. The Kimi battery-market supplement preferred the Toolkit report for connecting the opportunity to uncontracted procurement and supplier specifications, while explicitly criticizing unsupported inferences in both reports. These inspected examples illustrate tradeoffs and fallibility, not an independent adjudication of every rating. Original judgments were not replaced.

The [regenerated LongCat banking judgment](completion-supplement/longcat/judgments/pair-01/parsed.json) identifies a defect in both reports: they describe a late fee as incurred, while [the supplied complaint](inputs/sources/chatbots.md) says it is expected. Checking the reports against the source confirms that distinction. A preference between reports does not certify the preferred report as factually correct.

## Tasks and sources

| Task | Language / requested length | Admitted source unit |
| --- | --- | --- |
| [Battery-market discovery](inputs/briefs/battery-market-en.md) | English, 600–800 words | [EIA article body](inputs/sources/battery.md); installed and planned power capacity, not supplier revenue |
| [Banking chatbot pilot](inputs/briefs/banking-chatbots-en.md) | English, 600–800 words | [CFPB narrative and endnotes](inputs/sources/chatbots.md); complaint examples, not incidence rates |
| [Memory-safety roadmap](inputs/briefs/memory-roadmap-en.md) | English, 600–800 words | [CISA resource introduction](inputs/sources/memory-roadmap.md) and [announcement](inputs/sources/memory-oss.md); linked reports were not supplied |
| [Productivity and software sales](inputs/briefs/productivity-outlook-zh.md) | Chinese, 1,000–1,400 characters | [BLS release narrative](inputs/sources/productivity.md) before Table A1; tables and technical notes were not supplied |
| [AI risk management for a small firm](inputs/briefs/ai-risk-adoption-zh.md) | Chinese, 1,000–1,400 characters | [NIST FAQ](inputs/sources/ai-faq.md) and [AI RMF Core](inputs/sources/ai-core.md) |

The organizational decisions are hypothetical; source texts are actual US federal publications. The [source manifest](inputs/source-manifest.json) records URLs, text-unit boundaries and hashes. Public text was retrieved on October 10, 2026; brief-specific historical decision dates are explicit. This is purposive development selection, not held-out, representative or unseen-training data. BLS/CFPB text was captured through browser text when direct downloads were unavailable; source link labels were retained, while extraction-tool markers were removed. Linked third-party works were not separately retrieved. Supplied text units are not claims to have captured every linked document, table or image.

## Models, budgets and masking

| Author model (returned on captured responses) | API route | Order / presentation seed |
| --- | --- | --- |
| `deepseek-flash` | `api.deepseek.com` | 20261010 |
| `kimi-k2.6` | `api.moonshot.cn/v1` | 20261011 |
| `glm-5.3` | `open.bigmodel.cn/api/paas/v4` | 20261012 |
| `LongCat-2.5-Preview` | `api.longcat.chat/openai/v1` | 20261013 |

GLM Coding Plan was attempted first through its native CLI route and returned an expired-subscription error; all report generation then used the ordinary API. These are provider aliases, not immutable weight snapshots. Every original author arm had a 12,288 completion-token ceiling, a 98,304 total-token ceiling and a 240-second request deadline. Reasoning tokens count toward provider completion usage. GLM used `reasoning_effort=low` in both arms; other provider reasoning defaults were unchanged. Total usage and elapsed time were checked after responses; a timeout does not prove remote cancellation or absence of billing.

The Toolkit arm received the complete pinned Skill, workflow, research-standard and writing-style texts. Both original arms received identical briefs, sources and the report/notes JSON envelope; only report strings were judged. Longer Toolkit inputs mean equal ceilings do not imply equal realized cost. [Usage records](usage.csv) retain per-call tokens, duration and missing usage; no dollar-cost estimate is inferred.

| Author | Calls / complete responses | Known input tokens | Known completion tokens | Calls missing usage |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 10 / 7 | 111,599 | 91,073 | 0 |
| Kimi | 10 / 10 | 110,228 | 56,036 | 0 |
| GLM | 10 / 10 | 110,698 | 18,909 | 0 |
| LongCat | 10 / 4 | 47,244 | 24,266 | 6 |

The common judge requested `gpt-6-astra` at low effort through native CLI version `0.162.0-alpha.17.2`, using a fresh ephemeral, read-only context for each pair and the user's configured CLI entitlement. The returned model identity is not independently attested. Judge packets contain only the brief, sources, fixed five-dimension 0–4 rubric, and randomized reports A/B; assignments and author notes are withheld. Raw events record tool use; a call using tools fails isolation checks. User configuration and project documentation were disabled, but host base context or skill metadata may remain. The judge's 8,192 output-token ceiling was checked after completion, not enforced as a hard CLI generation limit.

Reports were transmitted verbatim, including possible condition clues. For example, the DeepSeek and GLM productivity judgments noted statements about the absence of independent review as possible workflow clues. Assigned-label masking is therefore narrower than guaranteed successful blinding. This single-judge, small-sample pilot has no human calibration or independent adjudication. Dimension ratings and located reasons are available in [scores.csv](scores.csv) and the linked raw judgments, not treated as confirmed necessary-defect labels.

The [plan](study-plan.json), source packet, Toolkit text, rubric and assignments were frozen locally before author generation. This was **not publicly timestamped preregistration**. The exact harness is retained as [harness-snapshot.py](harness-snapshot.py), with per-stratum commitments under `runs/*/coordinator/`. Existing historical studies, labels and failure records are unchanged.

## Inspect and reproduce

From the repository root, verify all retained hashes and matched inputs without model calls:

```bash
python evals/studies/2026-10-10-lite-four-models/verify_bundle.py
python evals/studies/2026-10-10-lite-four-models/summarize.py
python evals/studies/2026-10-10-lite-four-models/summarize_completion.py
```

The second command covers only the primary and fence-only stages and derives [summary.json](summary.json), [scores.csv](scores.csv) and [usage.csv](usage.csv) from the original files. The third audits the completion plan, unchanged originals, matched inputs/settings and verbatim judge reports, then derives coverage and supplemental usage; add `--verify-only` for read-only auditing. Offline verification checks retention and matching, not report quality.

To repeat generation, set `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `GLM_API_KEY` and `LONGCAT_API_KEY` in your process environment, install/authenticate the native judge CLI, and put it on PATH or set `CODEX_BIN`. Keep the pinned Toolkit methods and harness revision. Then run:

```bash
python evals/studies/2026-10-10-lite-four-models/reproduce.py --output evals/runs/lite-four-models-repeat
```

This makes **40 author API calls and up to 20 judge calls**, billed to your provider accounts and CLI entitlement. It uses the original ordinary API routes, not a new Coding Plan availability probe. Output must be a new directory. Add `--prepare-only` for zero model calls; add `--include-format-supplement` to apply the separately labeled policy after primary attempts lock. The supplement never increases the combined judge ceiling beyond 20 and never adds author calls. Nonzero exit for unresolved primary pairs preserves their records; it is not an instruction to rerun them. Model aliases, availability and responses can change; identical generations are not promised.

To repeat the declared completion supplement (20 author requests and 10 judgments, not a new full study), keep the process credentials above and choose a new output directory inside the study:

```bash
python evals/studies/2026-10-10-lite-four-models/run_completion_supplement.py --output evals/studies/2026-10-10-lite-four-models/completion-repeat
```

This preserves the original failures and refuses an existing output directory. Add `--prepare-only` to inspect the plan without calls. A repeat does not replace these retained results. Ordinary API and native judge CLI calls still consume the respective accounts' quotas.

| Artifact | Contents |
| --- | --- |
| `inputs/` | Briefs, exact supplied source texts, provenance, four model configurations and judge schema |
| `runs/<model>/` | Frozen assignment key and methods, all first author requests/replies/failures, primary judge packets/replies, usage, outcomes and hash manifests |
| `completion-supplement/` | Separate frozen plan, 20 new author requests/raw responses/readable Markdown reports, 10 judgments, locked results and hashes |
| `format-supplement/<model>/` | Eligibility outcomes, byte-preserving derivations, separately locked judge replies and supplemental results |
| `run_live_study.py`, `run_format_supplement.py` | Execution adapters retained without post-run changes; invoke through `reproduce.py` |
| `host.json` | OS, Python/CLI version and model-identity boundary |

Original response payloads and failures are published in full. Machine-specific native CLI stderr is retained privately; it is excluded from these evidence manifests and used for no quality finding. No credentials or local account paths are included. Byte-preserving Git attributes keep frozen evidence hashes stable across checkouts.
