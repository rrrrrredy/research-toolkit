# Complete-report comparison: no stable overall quality gain observed

[English](README.md) · [简体中文](README.zh-CN.md)

The user selected the actual October 12 baseline, `422b437169e609b94c16087c65fdd68a83ad0ca4`, against v1.0.0 at `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`. Both method snapshots generated new complete reports with the same evidence and resources. Historical short outputs were not paired with newly expanded reports.

The initial study ran October 13; repair and rechecking finished October 14. Seven existing real independent tasks and three new tasks produced **10 pairs, 20 complete reports and 20 fresh-context Astra blind reviews**. Astra also authored the reports: analysis followed by two or three separately executed writing units. All 62 author-stage calls and 20 initial review calls completed.

## Initial results

| Metric | October 12 baseline | v1.0.0 |
|---|---:|---:|
| Primary mean score /100 | 100 | 99.5 |
| Seven original-task mean | 100 | 99.29 |
| Three new-task mean | 100 | 100 |
| Primary preference | 2 tasks | 4 tasks |
| Swapped-order preference | 3 tasks | 3 tasks |
| Astra primary pass verdict | 10/10 | 10/10 |
| Original length requirement met | 10/10 | 10/10 |

Both orientations have four ties. Mean paired change is **−0.5 points**, median zero. Preference agrees across orientations for seven tasks and changes for three: two stable current-version wins, two stable baseline wins, three stable ties and three order-sensitive pairs. The primary 4–2 preference count does not establish an overall gain or a percentage improvement in research quality.

The existing five-dimension 0–4 rubric is equally weighted and scaled to 100. Ratings show a strong ceiling effect and are not factual-accuracy percentages. **The maintainer subsequently identified a citation defect in one current-version report that both initial orientations missed.** Original pass verdicts and scores remain unchanged.

## Full paired reports and original judgments

Score links open complete reports. Each row is one task; an order swap is not an additional task.

| Task | Before | After | Primary / swap preference | Reviews |
|---|---:|---:|---|---|
| `ai_agent_market_landscape_zh` | [100](authors/ai_agent_market_landscape_zh/before/report.md) | [100](authors/ai_agent_market_landscape_zh/after/report.md) | after / before | [Primary](reviews/ai_agent_market_landscape_zh/primary/parsed.json) · [Swap](reviews/ai_agent_market_landscape_zh/swap/parsed.json) |
| `ai_video_generation_investment_memo_zh` | [100](authors/ai_video_generation_investment_memo_zh/before/report.md) | [100](authors/ai_video_generation_investment_memo_zh/after/report.md) | after / after | [Primary](reviews/ai_video_generation_investment_memo_zh/primary/parsed.json) · [Swap](reviews/ai_video_generation_investment_memo_zh/swap/parsed.json) |
| `model_company_pipeline_long_horizon_zh` | [100](authors/model_company_pipeline_long_horizon_zh/before/report.md) | [100](authors/model_company_pipeline_long_horizon_zh/after/report.md) | tie / after | [Primary](reviews/model_company_pipeline_long_horizon_zh/primary/parsed.json) · [Swap](reviews/model_company_pipeline_long_horizon_zh/swap/parsed.json) |
| `model_price_war_competitive_analysis_zh` | [100](authors/model_price_war_competitive_analysis_zh/before/report.md) | [100](authors/model_price_war_competitive_analysis_zh/after/report.md) | after / tie | [Primary](reviews/model_price_war_competitive_analysis_zh/primary/parsed.json) · [Swap](reviews/model_price_war_competitive_analysis_zh/swap/parsed.json) |
| `monthly_observation_synthesis_zh` | [100](authors/monthly_observation_synthesis_zh/before/report.md) | [100](authors/monthly_observation_synthesis_zh/after/report.md) | tie / tie | [Primary](reviews/monthly_observation_synthesis_zh/primary/parsed.json) · [Swap](reviews/monthly_observation_synthesis_zh/swap/parsed.json) |
| `reasoning_model_competition_zh` | [100](authors/reasoning_model_competition_zh/before/report.md) | [95](authors/reasoning_model_competition_zh/after/report.md) | before / before | [Primary](reviews/reasoning_model_competition_zh/primary/parsed.json) · [Swap](reviews/reasoning_model_competition_zh/swap/parsed.json) |
| `source_instruction_boundary_zh` | [100](authors/source_instruction_boundary_zh/before/report.md) | [100](authors/source_instruction_boundary_zh/after/report.md) | tie / tie | [Primary](reviews/source_instruction_boundary_zh/primary/parsed.json) · [Swap](reviews/source_instruction_boundary_zh/swap/parsed.json) |
| `rag_long_context_decision_zh` | [100](authors/rag_long_context_decision_zh/before/report.md) | [100](authors/rag_long_context_decision_zh/after/report.md) | after / after | [Primary](reviews/rag_long_context_decision_zh/primary/parsed.json) · [Swap](reviews/rag_long_context_decision_zh/swap/parsed.json) |
| `test_time_compute_decision_zh` | [100](authors/test_time_compute_decision_zh/before/report.md) | [100](authors/test_time_compute_decision_zh/after/report.md) | tie / tie | [Primary](reviews/test_time_compute_decision_zh/primary/parsed.json) · [Swap](reviews/test_time_compute_decision_zh/swap/parsed.json) |
| `coding_benchmark_decision_zh` | [100](authors/coding_benchmark_decision_zh/before/report.md) | [100](authors/coding_benchmark_decision_zh/after/report.md) | before / before | [Primary](reviews/coding_benchmark_decision_zh/primary/parsed.json) · [Swap](reviews/coding_benchmark_decision_zh/swap/parsed.json) |

The stable current-version wins are the AI-video investment and RAG decisions. The stable baseline wins are reasoning-model competition and coding-benchmark interpretation. In the former, the current report underused available OpenAI evidence about information acquisition, web understanding and citation checking. In the latter, the baseline offered a more concrete pilot starting scope, sequence and adjustment conditions. The linked reports and judgments expose the differences.

## Findings, changes and targeted rechecks

The current coding report contained six private browser citation tokens that do not locate sources in standalone Markdown: one underlying publication defect, at six locations, labeled ND03/ND07. Both first reviews missed it. A later anonymous comparison explicitly applying the destination-format requirement confirmed it. No first result was discarded or overwritten.

English and Chinese workflow, writing and review guidance, plus their packaged plugin copies, now clarify the use of distinguishing evidence in requested comparisons, actionable starting assumptions in requested plans, and source-title/URL citations that work in exported artifacts. No outside reviewer, extra source requirement, fixed panel or runtime interface was added.

Two current reports were revised. Fresh-context Astra preferred each revision in an anonymous original-versus-revised comparison. The reasoning revision passed. The coding revision still needed existing repository-stratified benchmark results; these were checked against Scale's original article, added with historical and later-audit qualifications, and the changed complete report passed a further fresh-context Astra review. The overlength 4,557-character reasoning repair and the negative coding recheck remain preserved. Unchanged valid reports were not repeatedly reviewed for a favorable outcome.

- [reasoning_model_competition_zh: selected revision](repairs/reasoning_model_competition_zh/report-final.md), 4494 nonwhitespace characters; [current-version Astra review](repairs/reasoning_model_competition_zh/review/parsed.json) passes.
- [coding_benchmark_decision_zh: selected revision](repairs/coding_benchmark_decision_zh/report-final-v2.md), 3758 nonwhitespace characters; [current-version Astra review](repairs/coding_benchmark_decision_zh/review-2/parsed.json) passes.

Repair used two author calls, two anonymous comparisons and one changed-report check: five additional calls, **87 actual model calls in total**. Later judgments also changed scores and defect classifications for the same original texts; those judgments remain intact and are not used to re-estimate the initial effect. These feedback-assisted revisions do not replace the initial −0.5-point estimate. [Finding dispositions](source-adjudication.json) · [Method changes](method-change.json) · [Repair results and preserved attempts](repair-summary.json).

## Design and evidence scope

The intervention consists of six method files at two real commits. Author model, source material, stage structure and output limits are shared. Reviewers receive the task, identical source texts, complete anonymous reports and program counts; they do not receive author notes, methods, condition maps or other judgments. Each orientation uses a fresh context; conditions were decoded after all initial judgments completed. The later destination-format clarification applies only to explicitly recorded repair checks, not to rewritten initial scores.

The seven original tasks retain their identities and source provenance. The pipeline task uses the completed named-company continuation, with identical original papers/technical documents and multiple source channels in both conditions; anonymous A–H companies are not decoded into real companies. New tasks concern RAG versus long context, inference-compute allocation and coding-agent benchmarks. Full third-party source texts and exact requests remain local; public records retain original URLs, excerpt spans, provenance and hashes. Repository-authored source records are included in full.

This measures **complete-report quality with Astra under shared evidence and staged execution**. Common source acquisition, stage scheduling and counting cannot be credited to either version. Live retrieval strategy, MCP state transitions, Lite and the earlier four author models were not compared here. No outside people or additional tasks are required to report these results.

## Inspect and verify

[Frozen protocol and tasks](protocol.json), [rubric alignment before the first judgment](review-standard-amendment.json), [initial statistics](initial-summary.json), [calls and input bindings](calls.json), [review bindings](review-bindings.json), [execution snapshots](code/). Original CLI returns, complete reports, reviews and failed revisions are retained. Astra is the model requested in the actual calls; CLI events retain usage but do not independently attest a returned model identity. Initial usage is 3,321,918 input and 143,962 output tokens; cached input is a subset, not another total.

Run `python evals/studies/2026-10-13-before-after/verify.py` to check bytes, original-response extraction, report/review bindings and descriptive arithmetic with zero model calls. It does not judge research quality.
