# Evaluation Roadmap And Claim Boundaries

[English](evaluation-roadmap.md) | [简体中文](evaluation-roadmap.zh-CN.md)

Research Toolkit needs several kinds of evidence. Combining them into one score would make the project look stronger while making its claims less trustworthy.

For new report studies, use the [current evaluation standard](report-evaluation-standard.md): one five-dimension 0–4 rubric, four non-author reviewers, evidence-based finding dispositions, frozen first-submission outcomes, separately scoped report delivery, and post-evaluation product changes. Earlier frozen scales and reviewer counts remain historical, not alternative current instructions.

## Claim Ladder

| Track | Question | Current evidence | What it may claim | What it may not claim |
|---|---|---|---|---|
| A. Deterministic conformance | Did an artifact follow configured protocol and delivery rules? | Implemented: positive controls, 22 negative fixtures, source integrity checks | Known structural and traceability failures are detected for tested fixtures | The report is factually correct, insightful, or useful |
| B. Real-task efficacy | Does using the framework improve decision-useful research versus normal agent behavior? | Historical first reviews complete; results and failures summarized in [evaluation status](evaluation-status.md); no current general efficacy claim | A bounded treatment estimate after preregistered held-out runs and independent review | Universal superiority across models, tasks, or organizations |

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

| Historical reviewer backends (retained provenance, not a default dependency) |
| --- |
| The current development lane uses Astra inside Codex as the sole author, actually loading the pinned framework and using its research workflow. Each first-submission report receives four separate reviews; the same requirement applies to revised reports when report delivery or repair research is in scope: GPT-5.6 Sol (`gpt-5.6-sol`, `high`) in a fresh Codex context, DeepSeek, Kimi, and GLM-5.3 (requested `high`). DeepSeek, Kimi and GLM are reviewers, not substitute authors. This is a study configuration, not a Codex dependency or a four-model requirement of the framework itself. |

Preserve failed reports and unresolved findings as evaluation outcomes. Move from the frozen first-submission results to the dataset and product feedback; do not require every sample to be repaired before product iteration. Repair records remain separate and do not establish a toolkit effect.

Give all four reviewers the same complete report version, task and supplied evidence, with version hashes. Do not expose another reviewer's current-round opinion before their response is locked. Record actual context, tools, evidence access, model identity when exposed, truncation and failures. Three responses constitute an incomplete panel, not a completed four-reviewer round. Author self-checks do not count as independent reviews; different models do not guarantee statistical independence.

GLM was added after some three-reviewer development runs had started. Keep those original freezes and opinions; label its same-input supplementary review as a later addition, not an originally preregistered four-person panel. The GLM lane uses a genuine supported Coding Plan client, not arbitrary HTTP use of subscription quota; see the [official integration guide](https://docs.bigmodel.cn/cn/coding-plan/tool/others). Record that client context can differ from raw API context. Returned token usage and a client's estimated price are not independently verified subscription charges or remaining quota.

Run the evaluation chain through task admission, frozen setup, outline, research, section drafting, the locked first submission, the required reviews and evidence-based adjudication. Preserve the resulting defects and failures in the dataset, use them to diagnose the toolkit, and verify the relevant product changes. Complete missing reviews that remain required under the agreed study and failure policy; record completion attempts separately without changing the original submission, failure or chronology. Existing valid reviews do not need another round merely because they identify defects.

Report revision belongs to separately scoped report delivery or repair research. For that work, a review of an old version cannot approve new text. For the evaluation itself, a confirmed defect remains a result even when the sample is never repaired; favorable votes and a high average cannot erase it. Unsupported model corrections must not be copied into either the report or a defect label.

This route does not require human reviewers. Use known-error and valid controls to check the rubric before freezing a new study, and report results explicitly as LLM-judged with an evidence-audit boundary, not human-calibrated truth. It does not enable an automatic research-quality PASS in the deterministic runner. Existing frozen experiments and their original reviewer counts remain historical records; do not rewrite them to claim this new plan was executed.

<a id="track-b-held-out-real-task-efficacy"></a>

## Next study: freeze the design, then collect new evidence

The priority is a matched decision-quality study, not additional connector tools. The public 2-pair calibration and the 7 workflow tasks / 23 synthetic diagnostic pairs are development material. The native English showcase expands readable examples, not held-out coverage. The historical study's post-result exclusion and quota failures prevent treating its supplemental view as a clean efficacy estimate.

Use the [study template](../evals/templates/paired-study.json) for the next cohort. It is an unfilled design template: **no new held-out cohort or model results are established by this file**. The 12-family proposal is a screening option, not a required final sample size. Before any author run:

1. Select distinct, rights-cleared task families from a stated workload. Include native English and Chinese briefs across product, company, technical and policy questions where that matches the intended population; fix stratum counts in advance. Translation, renamed tasks and repeated runs remain the same family. Keep calibration families separate.
2. Complete each brief, task-specific requirements, evidence access policy and exposure record. Keep held-out briefs outside developer/author tuning contexts. Commit their hashes and timestamp before execution; release originals after reviews lock when rights permit. A hash binds a file but cannot prove that nobody saw it. If exposure cannot be excluded, label the cohort prospective development data rather than held out.
3. Pin one author model snapshot and runtime, toolkit commit and profile. Use the same brief, normal tools and total resource ceiling in both conditions. Include toolkit-internal reviews in the treatment's token/time budget; account for the common evaluation judges separately. Record actual usage and quota failures. If an important resource cannot be measured or capped comparably, disclose the limitation and narrow the budget claim.
4. Randomize balanced condition order within language/task blocks and run matched pairs close in time in fresh contexts without shared generated memory. Separately randomize the masked report order for judges. Retain the assignment privately until all opinions lock. Log recognizable condition clues; source and claim IDs alone are not a reason to award quality points.
5. Freeze the five-dimension rubric, four-reviewer configuration, evidence-based adjudication and [necessary-defect labels](necessary-defects.md). For every report, use identical judge inputs and access apart from its own evidence. Ask judges to report suspected condition clues after rating; this checks leakage, not guaranteed blinding.
6. Freeze sample size, exclusions, retry and failure policy, endpoint and interval method. Publish all admitted families, failed attempts, interventions and task-level outcomes. Later exclusions remain visible in the original denominator. New versions or quota-recovery supplements form separate views; they never replace initial results.

### Outcomes and uncertainty

The primary endpoint is the presence of an adjudicated necessary report defect per condition. Within a family, only one condition defect-free yields its win; both defective and neither defective remain separate outcomes. Missing reports or required valid reviews leave the comparison unresolved, not a win. Severity and all five rubric dimensions remain visible as secondary outcomes. Execution completion is a separate endpoint.

Choose the number of independent families from the intended precision and available budget before running. For illustration, a binary proportion near 50% has an approximately ±25 percentage-point 95% Wilson interval at 12 independent observations, versus ±15 points at 40. These are design calculations, not Toolkit results or a power guarantee. The [NIST interval formula](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) applies to a single binomial proportion, not directly to the paired treatment difference.

Report paired effects with a prespecified paired method, resampling whole task families if bootstrapping. Keep each family's two arms and reviewer observations together; four reviews are not four independent tasks. State the sampling population and language/model strata. Report all-family outcome rates and missingness; complete-case quality differences are conditional and may be biased by selective failures. A larger convenience sample does not establish generalization.

Expand public calibration for debugging and reviewer checks, then collect a separate frozen cohort for the effect estimate. Report uncertainty even when wide. Do not keep adding samples until a favorable interval appears; any extension or sequential design must be specified before observing study outcomes.

Compare first submissions with first submissions. If repair effects are separately studied, preregister equal external feedback, revision opportunities and stopping rules; report revised results separately. Baseline reports do not lose semantic-quality points for lacking Toolkit-specific registries or receipts. Do not replace a normally online task with fixed sources merely for evaluator convenience. Twelve independent families in one author environment require 24 primary runs; additional repeats measure sensitivity, not more independent families.

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
