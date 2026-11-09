# Research brief

## question

Write a research report on how model-selection teams should interpret and combine benchmark evidence rather than select a model from a single leaderboard. Use HELM, its official papers, documentation, and implementation as an entry point. Compare it with a manageable set of complementary evaluation frameworks and benchmarks covering static knowledge or reasoning tests, executable coding tasks, tool-using or agent tasks, and human or model-judged preferences. Focus on versions and results publicly available from 2022 through 2026-11-09, with earlier context where necessary. The evidence cutoff is 2026-11-09; distinguish a historical version from a subsequently revised dataset or leaderboard.

Explain the difference between a benchmark dataset, an evaluation framework, an execution harness, and a leaderboard. For the selected examples, examine task construction, sampling, language and domain coverage, target capabilities, scoring rules, aggregation, and the unit of evaluation. Discuss which dimensions of quality, robustness, calibration, efficiency, or safety are actually measured and which are merely suggested by a benchmark's name or reputation. A small benchmark result must not be treated as a direct estimate of all user workloads.

Reconstruct the conditions needed to interpret representative reported results: model identity and release, prompt and few-shot format, decoding and reasoning settings, tool access, context limits, harness version, judge configuration, and available cost or latency information. Explain how these choices can change rankings or make comparisons invalid. Examine contamination and memorization, public-test adaptation, hidden-test access, benchmark refreshes, evaluator bias, and uncertainty from finite samples. Separate evidence of contamination from suspicion, and do not invent significance estimates when the underlying observations are unavailable.

Assess reproducibility from the artifacts that are actually public. Identify whether a result has accessible data, executable evaluation code, stable dependencies, inspectable scoring, and a usable model or API version. Distinguish the ability to reconstruct a procedure from an independently reproduced score. Explain the consequences of private tests, mutable APIs, unavailable judge models, and changing web or software environments. Published independent replications may be analyzed, but this task does not require claiming or conducting a new benchmark run.

Connect the comparison to two contrasting deployment decisions: selecting a model for a grounded customer-support assistant and selecting a model for a repository-level coding agent. Explain which benchmark evidence transfers plausibly to each workload, what it misses, and what task-specific evidence would change the selection. Discuss successful-task cost, failure severity, operational constraints, and distribution shift rather than treating the highest aggregate score as the universal best choice. Where studies relate benchmark scores to user outcomes, distinguish observed association from a demonstrated causal relationship.

Deliver a complete report with an evaluation coverage matrix, a versioned reproducibility comparison, worked interpretations of representative score comparisons, and conditional model-selection recommendations for the two workloads. Organize the report freely and cite primary evaluation definitions and the exact result versions used. The key checks are whether unlike evaluation objects remain distinguishable, whether score claims retain their execution conditions and uncertainty, and whether the recommendations acknowledge meaningful rank reversals or contradictory evidence. There is no required preferred benchmark or model, and a finding that the available evidence cannot resolve a selection is acceptable when the missing decision-relevant evidence is specified.

## audience

Model-selection, evaluation, and deployment teams deciding which benchmark evidence to trust

## scope

Follow the task geography, comparison scope and evidence cutoff of 2026-11-09. Each other-language version uses its frozen sources without seeing the first-language report.

## output

Complete long-form research report final.md with the task-specific comparisons, explanations, tables and locatable citations. Preserve the first draft and actual independent results.

## depth

A comparative research report that reconstructs evaluation conditions, explains what benchmark results measure, and connects their limitations to concrete model-selection decisions.

## evidence_standard

Use original public sources with actual dates, reading evidence and retained originals. Conduct seven separate independent content perspectives, relevant domain review, independent audit and final acceptance. Live primary research
