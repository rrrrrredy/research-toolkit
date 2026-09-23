# Evaluation Roadmap And Claim Boundaries

[English](evaluation-roadmap.md) | [简体中文](evaluation-roadmap.zh-CN.md)

Research Toolkit needs several kinds of evidence. Combining them into one score would make the project look stronger while making its claims less trustworthy.

For new report studies, use the [current evaluation standard](report-evaluation-standard.md): one five-dimension 0–4 rubric, four non-author reviewers, evidence-based finding dispositions, frozen first-submission outcomes, separately scoped report delivery, and post-evaluation product changes. Earlier frozen scales and reviewer counts remain historical, not alternative current instructions.

## Claim Ladder

| Track | Question | Current evidence | What it may claim | What it may not claim |
|---|---|---|---|---|
| A. Deterministic conformance | Did an artifact follow configured protocol and delivery rules? | Implemented: positive controls, 22 negative fixtures, source integrity checks | Known structural and traceability failures are detected for tested fixtures | The report is factually correct, insightful, or useful |
| B. Real-task efficacy | Does using the framework improve decision-useful research versus normal agent behavior? | Study design documented; no completed efficacy result published here | A bounded treatment estimate after preregistered held-out runs and independent review | Universal superiority across models, tasks, or organizations |

## Track A: Deterministic Conformance

Keep this layer fast, offline, and fail-closed. Every new mechanical rule needs both:

- a known-bad fixture that was previously accepted or is a plausible regression;
- a known-good control that proves the rule does not improve by rejecting everything.

The machine-readable result uses `result_schema_version: 2`, `conformance_status`, `conformance_score`, and `conformance_flags`. `research_quality_status` remains `not_evaluated`. A score of 100 means only that the configured mechanical checks found no issue.

High-risk flags such as false completion, malformed final review records, and configured source-instruction violations are blocking failures. `review` also exits non-zero by default.

## Development Reports And Review Diagnostics

The [2026-09-07 evidence package](../evals/diagnostics/2026-09-07/) includes actual calibration reports, retained failures, editorial repairs and three-model text diagnostics. It is not part of the held-out study. Model/provider, context exposure, retrieval access, requested and returned identity where available, incomplete responses and adjudication are disclosed separately. Different vendors diversify viewpoints; their agreement is neither factual ground truth nor human calibration.

The protocol's numeric ledger maintenance intervals, stagnation triggers and review-loop budgets are operational heuristics, not empirically optimized thresholds. No current ablation establishes their superiority. Clarification has no question quota: ask only for missing essential information, and resolve critical choices before dependent work. Preserve these defaults until observed premature stops, missed stalls, redundant searches or maintenance costs justify a scoped comparison; do not infer validity from numerical precision.

The two stagnation signals observe different units:

| Signal | Observation | Intended response |
| --- | --- | --- |
| Two stale complete unit cycles | Evidence-to-argument cycles add no useful analytical progress, even if sources were found | Change the structural angle |
| Three unproductive searches/source passes | A collection direction yields no useful evidence | Stop that collection direction |

This is an explanation of existing rules, not a new schema or extra required stage files. Self-authored non-empty gate files would not prove that a stage happened before the next one. Current receipts bind final artifacts and reviews; full intermediate-stage chronology remains only partly observable.

## Current Report And Review Plan

Complete and verify all accepted method, execution, checker, data and documentation corrections before starting new report-writing or model-review runs. Offline regressions are preparation, not an efficacy study; green CI alone does not authorize a study start.

The current development lane uses Astra inside Codex as the sole author, actually loading the pinned framework and using its research workflow. Each first-submission report receives four separate reviews; the same requirement applies to revised reports when report delivery or repair research is in scope: GPT-5.6 Sol (`gpt-5.6-sol`, `high`) in a fresh Codex context, DeepSeek, Kimi, and GLM-5.3 (requested `high`). DeepSeek, Kimi and GLM are reviewers, not substitute authors. This is a study configuration, not a Codex dependency or a four-model requirement of the framework itself.

Preserve failed reports and unresolved findings as evaluation outcomes. Move from the frozen first-submission results to the dataset and product feedback; do not require every sample to be repaired before product iteration. Repair records remain separate and do not establish a toolkit effect.

Give all four reviewers the same complete report version, task and supplied evidence, with version hashes. Do not expose another reviewer's current-round opinion before their response is locked. Record actual context, tools, evidence access, model identity when exposed, truncation and failures. Three responses constitute an incomplete panel, not a completed four-reviewer round. Author self-checks do not count as independent reviews; different models do not guarantee statistical independence.

GLM was added after some three-reviewer development runs had started. Keep those original freezes and opinions; label its same-input supplementary review as a later addition, not an originally preregistered four-person panel. The GLM lane uses a genuine supported Coding Plan client, not arbitrary HTTP use of subscription quota; see the [official integration guide](https://docs.bigmodel.cn/cn/coding-plan/tool/others). Record that client context can differ from raw API context. Returned token usage and a client's estimated price are not independently verified subscription charges or remaining quota.

Run the evaluation chain through task admission, frozen setup, outline, research, section drafting, the locked first submission, the required reviews and evidence-based adjudication. Preserve the resulting defects and failures in the dataset, use them to diagnose the toolkit, and verify the relevant product changes. Complete missing reviews that remain required under the agreed study and failure policy; record completion attempts separately without changing the original submission, failure or chronology. Existing valid reviews do not need another round merely because they identify defects.

Report revision belongs to separately scoped report delivery or repair research. For that work, a review of an old version cannot approve new text. For the evaluation itself, a confirmed defect remains a result even when the sample is never repaired; favorable votes and a high average cannot erase it. Unsupported model corrections must not be copied into either the report or a defect label.

This route does not require human reviewers. Use known-error and valid controls to check the rubric before freezing a new study, and report results explicitly as LLM-judged with an evidence-audit boundary, not human-calibrated truth. It does not enable an automatic research-quality PASS in the deterministic runner. Existing frozen experiments and their original reviewer counts remain historical records; do not rewrite them to claim this new plan was executed.

## Track B: Held-Out Real-Task Efficacy

The proposed first product-effect study uses 12 distinct, held-out, rights-cleared real research tasks sampled from the intended workload. This is a screening cohort, not a universal sample-size or statistical-power guarantee. Use two separate, excluded tasks to calibrate execution and review; freeze the main study after calibration and before its model runs.

For each task and production agent environment:

1. Run baseline and framework conditions with the same model, reasoning setting, normal tools, starting memory, context budget, timeout, and retry rule. Prevent cross-condition access to outputs or experiment-generated memory. Disable only the tested framework in the baseline; verify the treatment loads the pinned version rather than a drifting installed copy.
2. Keep the request, initial materials, target reader, and information cutoff fixed; randomize condition order within the same time block. Preserve normal web access when the real task needs it, letting each condition choose its own searches and sources. Use identical fixed sources only when the original task requires that restriction.
3. Preserve complete outputs, failures, latency, cost or token usage when exposed, and user corrections.
4. Use the fixed four-reviewer panel above, independently and blinded to condition as far as the report permits. Freeze each review before sharing opinions. Record identity/context leakage and complete a separate evidence audit of material claims and disputes. No human-review prerequisite applies to this new LLM-judged design, and no human calibration may be claimed. Missing, truncated or cross-version reviews leave the panel incomplete.
5. Score task fidelity, factual/evidence discipline, synthesis, counter-evidence, and reader usefulness separately; reader usefulness includes decision value and readable delivery. Use `not_assessed` when evidence or input is insufficient rather than treating it as zero or a clean bill of health.
6. Treat invented facts, missing primary deliverables, hidden critical limitations, and false completion as critical failures that averages cannot offset.
7. Publish every task-level pair, paired differences, descriptive uncertainty, disagreements, exclusions, and reruns. Report win, loss, tie, both-failed, and unresolved outcomes explicitly; neither both-failed nor unresolved outcomes count as framework wins. Any stopping or extension thresholds are preregistered product decision rules, not significance claims. Sequential stopping needs a corresponding statistical design before confirmatory inference.

Do not mix different models into the framework-effect estimate. Compare framework and baseline within the same production environment.

Compare first drafts with first drafts. If revision effects are also measured, give both conditions the same preregistered review and revision opportunities and report initial and revised results separately. Model-review scores alone support only a bounded LLM-judged comparison, not proof that the framework improves real-world decisions.

Twelve tasks in one production environment require 24 primary runs. If four tasks are selected in advance for one repeat of each condition, those eight additional runs measure sensitivity and are not new independent tasks. Baseline outputs do not lose semantic-quality points for lacking framework-specific registries or receipts; apply conformance checks only where the protocol is applicable, while auditing evidence and truthful delivery in both conditions.

## Data Rules

- Use synthetic packs for public deterministic checks when factual freshness is not the target.
- Quarantine internally contradictory records; never leave them active merely to preserve case counts.
- For live-web efficacy studies, freeze task inputs and time boundaries, then preserve each condition's observed sources, access times, and failures for audit. Do not turn a normally online task into a fixed-source test for evaluator convenience.
- Keep private or licensed evidence out of public bundles unless redistribution rights are explicit.
- Separate evaluator-development data, reviewer-calibration data, and final held-out tasks.

## Release And Study Requirements

Conformance schema v2 and tagged prereleases are available. The current `main` branch also contains changes listed under `Unreleased`; a prior release archive does not include those later changes.

- Freeze each real-task study before its held-out runs, and retain first outputs and review findings as evaluation evidence.
- Publish comparisons only within the scope supported by complete runs and evidence review.
