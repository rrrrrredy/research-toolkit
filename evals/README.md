# Evaluations

[English](README.md) | [简体中文](README.zh-CN.md)

[October 19 public-library self-check comparison](studies/2026-10-19-library-self-check/README.md): one research question, two Lite runs on v1.3.1 and v1.3.2 with the same model, materials and draft. Both corrected two explicitly injected defects before their first passing checklist. Neither falsely passed; this case showed no incremental v1.3.2 benefit. First drafts, first checks, final reports and actual costs are retained.

[October 14 complete native-Agent comparison](studies/2026-10-14-native-agent/README.md): one existing real long task, tied first/final blind assessments, higher Full resource use, and a Windows encoding failure turned into a targeted fix.

[October 16 external batches](studies/2026-10-16-external-batches/README.md): 12 Song-authorized runs from confirmed batches 2026-10-14 (Toolkit `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`, v1.0.0, Lite) and 2026-10-15-v1 (Toolkit `f31345c5a994a8f1574d946388ee58fe1177ede2`, v1.1.0, Lite×4 and Full×2). Two Full records repeat a Day-1 research question, so the set is 12 runs and 10 questions. Synthetic sources are disclosed. The Full reviews are same-session degraded reviews.

[October 19 external batches](studies/2026-10-19-external-batches/README.md): 12 Song-authorized Lite runs from confirmed batches 2026-10-16-v1 (Toolkit `f31345c5a994a8f1574d946388ee58fe1177ede2`, v1.1.0) and 2026-10-17-v2 (Toolkit `fedf7cde832139c86cad585883cb5ec2f666427f`, v1.3.0). The 12 question texts in that folder are distinct. Two retests repeat a question already ingested on October 16. Synthetic sources are disclosed. Lite runs record author self-check. The six 2026-10-17-v2 outer Grok notes are not Toolkit independent reviews.

[October 21 external batches](studies/2026-10-21-external-batches/README.md): 12 Song-authorized Lite runs from confirmed batches 2026-10-18-v1 (Toolkit `fedf7cde832139c86cad585883cb5ec2f666427f`, v1.3.0) and 2026-10-19-v1 (Toolkit `e245b90a324933f53fddf0deea039a7715708005`, v1.3.1). The 12 question texts in that folder are distinct. Four retests repeat a question already ingested. Synthetic sources are disclosed. Lite runs record author self-check. All 12 outer Grok notes are not Toolkit independent reviews. [Two report/source errors and missed reviews are corrected separately](repairs/2026-10-21-source-polarity/README.md); original passes are historical.

Existing and future user tasks, development tasks, reference tests and cases are real independent tasks; tests actually executed are real tests. Model execution and evaluation also provide a user perspective: judge usefulness from actual context use, extra reading, time, rework and research results. Human participation is not a prerequisite; describe the observed benefit and its task scope. Task identity follows the research question, so repeated runs of one task remain repeated runs. Source materials retain their stated provenance, including supplied or constructed data. Astra in a separate context can review independently; no outside person, different model vendor or additional external material is required. Changes to task assignment, reviewer inputs or acceptance criteria require targeted revalidation.

Research Toolkit helps execute research; the research evaluation dataset uses tasks, material and criteria to identify weaknesses in outputs. This directory also contains Toolkit software checks. Passing those checks is not a research-quality score.

| What you need | Entry point |
|---|---|
| October 12 baseline versus v1.0.0: complete reports | [10-task comparison and targeted repairs](studies/2026-10-13-before-after/README.md): no stable overall gain; original mean 100 → 99.5, 20 reports, 20 blind reviews, two separately accepted revisions |
| External batches, 2026-10-14 and 2026-10-15-v1 | [12 Song-authorized runs](studies/2026-10-16-external-batches/README.md) on Toolkit `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3` (v1.0.0, Lite) and `f31345c5a994a8f1574d946388ee58fe1177ede2` (v1.1.0, Lite×4 and Full×2). Two Full records repeat a Day-1 question, so the set is 12 runs and 10 questions. Synthetic sources are disclosed. The Full reviews are same-session degraded reviews. |
| External batches, 2026-10-16-v1 and 2026-10-17-v2 | [12 Song-authorized Lite runs](studies/2026-10-19-external-batches/README.md) on Toolkit `f31345c5a994a8f1574d946388ee58fe1177ede2` (v1.1.0) and `fedf7cde832139c86cad585883cb5ec2f666427f` (v1.3.0). The 12 question texts in that folder are distinct. Two retests repeat a question already ingested on October 16. Synthetic sources are disclosed. The six outer Grok notes are not Toolkit independent reviews. |
| External batches, 2026-10-18-v1 and 2026-10-19-v1 | [12 Song-authorized Lite runs](studies/2026-10-21-external-batches/README.md) on Toolkit `fedf7cde832139c86cad585883cb5ec2f666427f` (v1.3.0) and `e245b90a324933f53fddf0deea039a7715708005` (v1.3.1). The 12 question texts in that folder are distinct. Four retests repeat a question already ingested. Synthetic sources are disclosed. The 12 outer Grok notes are not Toolkit independent reviews.  [Two report/source errors and missed reviews are corrected separately](repairs/2026-10-21-source-polarity/README.md); original passes are historical. |
| Report-defect examples and comparison excerpts | [Semantic diagnostics](semantic_diagnostics/README.md) |
| Research-quality criteria and result interpretation | [Five-dimension standard](../docs/report-evaluation-standard.md), [existing results and public scope](../docs/evaluation-status.md) |
| Toolkit software behavior checks | The cases, fixtures and commands below |

Changes to Toolkit defaults do not rewrite existing samples, first reviews or labels, and do not automatically start new model evaluations.

## Case and dataset inventory

[Full collection-to-method coverage](../docs/correction-audit-2026-10-13.md)

The dedicated Toolkit task set is [`cases/`](cases/). It is separate from the later four-model task sets. This inventory covers the current tasks, controls, examples and dated results; categories overlap where the same material is reused, so their counts must not be added as if each were a new independent task.

| Material | Size | Use and current status |
|---|---|---|
| [Toolkit research cases](cases/) | 7 tasks | [Original seven-report rerun](diagnostics/2026-10-13-dedicated-seven/README.md): 15 calls retained; six supplied-source reports accepted. The pipeline task now has a [complete named-company report with R01–R13 passing Astra review](repairs/2026-10-13-pipeline-complete/README.md). |
| [External batches, 2026-10-14 and 2026-10-15-v1](studies/2026-10-16-external-batches/README.md) | 12 runs, 10 questions | Song-authorized external tasks on frozen Toolkit 1.0.0 (`45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`, Lite) and 1.1.0 (`f31345c5a994a8f1574d946388ee58fe1177ede2`, Lite×4 and Full×2). Synthetic sources are disclosed. The two Full reviews are same-session degraded reviews. |
| [External batches, 2026-10-16-v1 and 2026-10-17-v2](studies/2026-10-19-external-batches/README.md) | 12 Lite runs, 12 question texts | Song-authorized external tasks on frozen Toolkit 1.1.0 (`f31345c5a994a8f1574d946388ee58fe1177ede2`) and 1.3.0 (`fedf7cde832139c86cad585883cb5ec2f666427f`). Two retests repeat a question already ingested on October 16. Synthetic sources are disclosed. The six outer Grok notes are not Toolkit independent reviews. |
| [External batches, 2026-10-18-v1 and 2026-10-19-v1](studies/2026-10-21-external-batches/README.md) | 12 Lite runs, 12 question texts | Song-authorized external tasks on frozen Toolkit 1.3.0 (`fedf7cde832139c86cad585883cb5ec2f666427f`) and 1.3.1 (`e245b90a324933f53fddf0deea039a7715708005`). Four retests repeat a question already ingested. Synthetic sources are disclosed. The 12 outer Grok notes are not Toolkit independent reviews.  [Two report/source errors and missed reviews are corrected separately](repairs/2026-10-21-source-polarity/README.md); original passes are historical. |
| [Negative fixtures](regression_fixtures/manifest.json) / [positive fixtures](conformance_fixtures/manifest.json) | 22 / 4 | Real software checks on expected failures and valid controls; not 26 additional research questions. |
| [Semantic diagnostics](semantic_diagnostics/README.md) | 23 paired examples | Current catalog applies documented corrections; original inputs and judgments remain available. |
| [Four-model tasks](tasksets/development-v2-synthetic/README.md) | 5 task families | [October 12 run](studies/2026-10-12-lite-four-models/README.md): 72 requests, 16 valid pairs, four missing pairs and six swap preference changes retained. |
| [Judge calibration v3](tasksets/judge-calibration-v3/README.md) | 4 families, 12 packets | [12 actual Astra judgments](diagnostics/2026-10-12-astra-calibration/README.md); v2 arithmetic inputs are already included. |
| [Old/new-task repair recheck](diagnostics/2026-10-13-targeted-recheck/README.md) | 4 tasks: 2 existing, 2 new | 31 requests; 16 final versions accepted, including ten maintainer corrections; originals retained. |
| [Writing examples](taste_anchors/README.md) | 4 groups | Reusable examples for concrete criteria; prior exposure and fictional or undated source facts remain explicit. |
| [Source packs](source_packs/) | 3 packs | Supplied evidence for tasks; source facts and provenance are preserved. |
| [Public research cases](../docs/case-study/README.md) | 2 cases | Chinese office-agent research and original English API/browser research, with drafts, reviews and revisions. Translations are not additional tasks. |
| [Templates](templates/) and [Lite example](../examples/lite/) | Workflow aids | Reusable configuration and onboarding examples. |

The seven dedicated cases are:

| Original task file | Research question |
|---|---|
| [ai_agent_market_landscape_zh.json](cases/ai_agent_market_landscape_zh.json) | AI Agent market landscape |
| [ai_video_generation_investment_memo_zh.json](cases/ai_video_generation_investment_memo_zh.json) | AI video-generation investment memo |
| [reasoning_model_competition_zh.json](cases/reasoning_model_competition_zh.json) | Reasoning-model competition |
| [model_price_war_competitive_analysis_zh.json](cases/model_price_war_competitive_analysis_zh.json) | Model price-war competitive analysis |
| [monthly_observation_synthesis_zh.json](cases/monthly_observation_synthesis_zh.json) | Monthly AI observation synthesis |
| [source_instruction_boundary_zh.json](cases/source_instruction_boundary_zh.json) | Research with source-embedded instruction attempts |
| [model_company_pipeline_long_horizon_zh.json](cases/model_company_pipeline_long_horizon_zh.json) | Eight-company model pipeline with 13 turns of requirements |

These seven original questions are in Chinese; this English index is a guide, not seven translated or additional tasks. `scripts/run_evals.py` now puts the current division of work into every new prompt: programs measure length, Astra reviews content in a separate context with the complete task/report/sources and necessary provenance, and the author repairs confirmed defects in a separately saved version. Author and reviewer may use the same model. No outside reviewer, outside contribution or fixed panel is required. One completed current-report review is sufficient; the long-horizon case no longer imposes a three-row minimum. Missing or negative reviews still fail the applicable completion checks.

PR #38 checked all seven generated prompts and the one-review rule offline. The subsequent [seven-report rerun](diagnostics/2026-10-13-dedicated-seven/README.md) now contains seven complete generated texts, seven first Astra reviews and one changed-report review. Six first drafts passed; the pipeline report was shortened from 6,020 to 5,987 characters and accepted as a stage report, with R04/R05 open at that point. The subsequent [complete named-company report](repairs/2026-10-13-pipeline-complete/README.md) is 5,244 characters and passes all 13 requirements after actual research, revision and fresh-context Astra review. That completion is the current task status. All 13 historical requirements were supplied together; this does not claim live 13-turn agent execution. The earlier 31-request recheck used four other tasks. Preserve original folders and results, and record repairs as new versions.

This directory contains seven research cases, twenty-two negative fixtures, four positive fixtures, and report diagnostics for Research Toolkit. The cases and evaluator are runtime-neutral; no particular agent runtime is required. The offline checks examine the research brief, task files, sources and claims, review records, source-instruction boundaries, and final prose. They report those checks, not a model ranking or an overall report-quality verdict.

Evaluator result schema v2 keeps two claims separate. `conformance_status`, `conformance_score`, and `conformance_flags` describe deterministic structure, traceability, and configured failure signals. `research_quality_status` is `not_evaluated`; the runner does not claim that a mechanically conforming report is insightful, accurate, or decision-useful.

Missing required files block a pass regardless of score. Malformed requirement or conversation JSONL and invalid source or claim CSVs produce explicit failure findings; a damaged case does not prevent the remaining cases from being reported. CSV counts use logical records, and source IDs and titles must match within the same record.

Actual outputs are available in the [2026-09-07 development package](./diagnostics/2026-09-07/): four original calibration reader reports, two repairs, three-model text replies and an explicitly retained incomplete response. These are real executed tests on distinct tasks, with their original reports and results retained.

See [evaluation status and version boundaries](../docs/evaluation-status.md) for completed historical first-review counts and their interpretation. The public files below are a subset of the retained evaluation material.


New [protocol v2](../docs/eval-protocol-v2.md) includes [five independent test tasks](tasksets/development-v2-synthetic/README.md) and [separate judge controls](tasksets/judge-calibration-v3/README.md). The [dated Astra calibration](diagnostics/2026-10-12-astra-calibration/README.md) adds 12 first judgments and source adjudication; the [four-model development run](studies/2026-10-12-lite-four-models/README.md) is complete, retaining four missing pairs and six swap preference changes. These input packs are separate from the seven workflow cases above.

The [October 13 feedback probes](diagnostics/2026-10-13-feedback-probes/README.md) retain eight new first attempts after prompt/method corrections: all parse, but only three meet length and semantic errors remain. Five real length failures and two post-result editorial controls exercise the existing delivery gate; no quality-benefit claim.

[October 13 old/new-task acceptance](diagnostics/2026-10-13-targeted-recheck/README.md) is complete: four independent tasks, 31 new requests, six reports accepted at first Astra review and ten maintainer corrections. All 16 final versions meet length and have corresponding passing Astra reviews; ten contain maintainer edits. Original reports and failures remain unchanged.

## Optional comparisons and defect labels / 可选比较与缺陷标签

For an optional with/without Toolkit comparison, use the [paired-study template](templates/paired-study.json) and [comparison guidance](../docs/evaluation-roadmap.md#next-study-freeze-the-design-then-collect-new-evidence). Routine repairs do not require this comparison. The template is not a frozen cohort or a run result. [Necessary-defect labels](../docs/necessary-defects.md) provide stable categories; the [23-case overlay](semantic_diagnostics/defect-tags.v1.json) preserves the existing diagnostic-only boundary. The Lite quickstart is onboarding, not another eval case.

需要比较使用／不使用工具箱时，可用[配对模板](templates/paired-study.json)和[比较说明](../docs/evaluation-roadmap.zh-CN.md#下一项研究先冻结设计再产生新证据)，不作为正常修复的前提；模板不代表已冻结样本或运行结果。[必要缺陷标签](../docs/necessary-defects.zh-CN.md)提供稳定类别，[23 例覆盖层](semantic_diagnostics/defect-tags.v1.json)保持开发诊断边界。Lite 入门不计为新增评测案例。

For an executable prospective 5–10-family pilot, see the [blinded pairwise protocol](../docs/eval-protocol.md). The script freezes and logs seed/order, masks A/B judge inputs, and retains first outputs, judgments and failures. The [2026-10-10 four-model pilot](studies/2026-10-10-lite-four-models/README.md) covers all 20 model–task judgments across five shared families, retaining all first attempts and failures and separately labeling format diagnostics and regenerated completion pairs; it does not establish general efficacy. To reproduce only the existing public two-pair archive inventory, run `python scripts/reproduce_calibration.py`; expected outputs are `evals/runs/calibration-reproduction/inventory.json` and `inventory.md`, with zero model calls.

## Contribute a failure case

1. [Submit a failure case](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml) with the question, expected result, sources, observed problem and profile/reviewer tier; paste a report excerpt if useful.
2. A maintainer reproduces and reviews it against the originals, distinguishing a tool defect, execution error and evidence gap; any missing details are requested in the issue.
3. An accepted minimal case enters the appropriate regression-fixture or semantic-diagnostic directory, linking the issue and retaining the original failure and its scope.

Admission requires a reproducible problem and original material that can lawfully be published; contributors do not need to write code or build a fixture.

## Directory Layout

Existing consumers can use the [schema v2 migration guide](../docs/evaluator-v2-migration.md). The [delivery checker interface](../docs/delivery-verification.md) documents intended-message binding and the limits of optional actual-reply comparison.

New report studies follow the [current evaluation standard](../docs/report-evaluation-standard.md). It separates first-submission scoring from reader-ready delivery and product-effect testing. Complete missing original reviews; preserve valid reviews, sample defects and raw failures for Toolkit improvements. Report repair is not a prerequisite for completing an evaluation. See the [historical rubric boundary](./rubrics/) before using older scales or frozen reviewer counts; they do not belong in current five-dimension 0–4 results.

See the [source-data audit](../docs/evaluation-data-audit.md) for provenance and exclusion decisions, and [semantic diagnostic pairs](./semantic_diagnostics/) for twenty-three author-proposed bad/control pairs. The three reader-review pairs added on September 10 received an internal four-model diagnosis, with a retained pricing-scope correction. Those reviews were not part of the eight earlier public calls; historical records are indexed separately from the current semantic catalog. These excerpts are development data, not held-out tasks or validated quality labels.

The [two-reviewer semantic results](./semantic_diagnostics/reviews/2026-09-08/) retain a shared missed defect, severity disagreements, a context/order-sensitive judgment and separately reviewed case revisions. Use the current catalog loader; original catalogs remain frozen historical inputs. Agreement with the author's labels is not accuracy.

```text
evals/
  cases/                         # one JSON task per eval case
  conversation_packs/            # sanitized multi-turn requirement sequences
  diagnostics/                   # dated actual outputs and non-scoring model reviews
  conformance_fixtures/          # known-good artifacts that must pass
  regression_fixtures/           # known-bad outputs that the runner must flag
  rubrics/                       # retained earlier study rubrics; current standard linked above
  semantic_diagnostics/          # non-scoring, synthetic editorial diagnostic pairs
  source_policy.json             # workflow-only use and audited exact claim exclusions
  source_packs/
    ai_knowledge_sanitized/      # sanitized seed sources generated from local knowledge repos
    prompt_injection_synthetic/  # synthetic source-instruction boundary case
    model_company_pipeline_synthetic/ # fictional eight-company pipeline evidence
  runs/                          # local eval outputs, ignored by git
```

## Rebuild The Sanitized Source Pack

The committed cases can be used directly. Optional regeneration requires local copies of `aiknowledge-cli` and `ai-knowledge-graph`. Generate into a separate directory so existing study inputs are preserved:

```bash
python scripts/build_sanitized_eval_set.py \
  --aiknowledge-cli /path/to/aiknowledge-cli \
  --knowledge-graph /path/to/ai-knowledge-graph \
  --out /path/to/new-eval-seed
```

On Windows PowerShell:

```powershell
python scripts/build_sanitized_eval_set.py `
  --aiknowledge-cli D:\path\to\aiknowledge-cli `
  --knowledge-graph D:\path\to\ai-knowledge-graph `
  --out D:\path\to\new-eval-seed
```

The builder applies configured substitutions for internal URL patterns, document IDs, email addresses, Chinese mobile numbers, and knowledge-system labels. These substitutions are not a comprehensive privacy or publication-rights review. It quarantines records whose summaries say that usable content is unavailable while their key points still assert facts. The generated pack is still a workflow eval seed, not a public factual authority.

The builder also applies the reviewed exclusions in source_policy.json, preserving the original excluded wording and reasons there. The integrity checker rejects recurrence of those exact claims. It checks the declared workflow purpose; `--purpose factual` must fail for the current packs. Missing source dates, unavailable original provenance and unverified reuse rights remain explicit, not inferred from a pack generation timestamp.

Validate active/quarantined separation and case references after rebuilding:

```bash
python scripts/check_eval_source_integrity.py --evals-dir /path/to/new-eval-seed
```

## Run An Eval

Create run folders and prompts in a new run directory. Skeleton creation rewrites `prompt.md`; use a distinct directory for a new input version:

```bash
python scripts/run_evals.py --create-skeletons --allow-missing-output --runs-dir evals/runs
```

For each case, give `evals/runs/<case_id>/prompt.md` to the agent under test. The agent should fill:

```text
state/task_spec.md
state/progress.json
state/requirements.jsonl         # when required by the case
data/source_registry.csv
data/claims_registry.csv
logs/review.jsonl
final.md
conversation/assistant_messages.jsonl # for multi-turn completion timing cases
delivery_message.md              # intended user-visible status
state/final_delivery.json        # only for terminal delivery cases
```

Then check mechanical conformance:

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md --json-report evals/runs/report.json
```

The runner writes:

```text
evals/runs/report.md
evals/runs/report.json
```

`report.json` uses `result_schema_version: 2`. A `pass` means mechanical conformance only. `review` and `fail` return a non-zero exit code by default; use `--allow-review` only for exploratory collection. Set both report paths when using another output directory. Record semantic reviews, reviewer disagreements and evidence limits separately from the conformance score. Separately maintained historical evaluation studies are available through the [public management repository](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.md).

## Check A Delivery Claim

For a task that uses the terminal-delivery artifacts, validate the intended user-visible message against current state and current hashes:

```bash
python scripts/check_delivery.py <task-directory>
```

The checker reads the intended message in `delivery_message.md`. To compare an independently captured reply, pass `--actual-message <reply-file>`; it does not read the chat application itself. A plainly labeled non-final stage artifact can pass without a terminal receipt.

Under the default delivery contract 3, a terminal claim requires consistent `final/complete` state, no open blockers, parseable passing global and task-required reviews bound to the current report, and a `global_final_delivery` receipt binding the required files. Declared content reviews must be complete. Additional validity audits, dispositions, independent adjudication and formal sampling apply to declared audited plans and historical audited fixtures. Requirements closed as waived, out of scope or accepted limitations need specific recorded user decisions; declared required reading is checked against source records. Recognized disclosure contradictions fail, while ambiguous disclosure matches require review. See the [delivery checker interface](../docs/delivery-verification.md) for the exact contract and legacy mode.

This checks record consistency. It does not authenticate user consent, actual reading, semantic correctness or report quality.

## Run Regression Fixtures

Regression fixtures are intentionally bad outputs. They are not new research tasks; they verify that the deterministic runner catches recurring failures such as process leakage, depth collapse, evidence drift, source-instruction leakage, visible completion against non-final state, stale or local-only receipts, lost or unresolved late corrections, premature completion, hidden limitations, forbidden appendices, noncanonical state, case-specific process sprawl, sentence-level keyword stuffing, malformed review logs, and a late global failure superseding an earlier PASS.

```bash
python scripts/check_regression_fixtures.py
```

These historical regression fixtures explicitly use delivery contract 1 to preserve their original comparisons; they do not establish acceptance under the current delivery contract. Current-contract behavior is covered by the delivery and evaluator contract checks listed below.

The fixture check passes only when each bad sample is scored as `review` or `fail` and the expected conformance or coverage flags are present.

## Run Known-Good Conformance Fixtures

Known-good fixtures guard against an evaluator that catches bad patterns by flagging everything. The positive controls combine prepared state artifacts with illustrative report anchors. A positive fixture is a mechanical control, not a validated research-quality label. They include a general report, a source-boundary case, a terminal long-horizon delivery, and the same long-horizon artifact honestly delivered as a non-final stage.

```bash
python scripts/check_conformance_fixtures.py
```

These historical positive fixtures also use delivery contract 1. Their passing results do not claim current-contract completion or validate the example's research quality.

The check passes only when each known-good run reaches `pass`, meets its minimum score, avoids the listed conformance and coverage flags, and preserves or excludes fixture-specific terms where required.

## Continuous Checks

GitHub Actions runs the full offline suite listed in the [contribution guide](../CONTRIBUTING.md#verification) on pushes and pull requests. None of these checks calls a model. The suite includes the current review-completion contract checks.

## How To Iterate

1. Preserve original inputs, outputs, reviews, failures and costs. Complete any originally required missing review on its original version. For authorized improvements, repair defective reports in separate versions and recheck those versions; keep the initial result.
2. Check each finding against the task, report and evidence. Distinguish method defects, execution failures, source limitations and unsupported reviewer suggestions.
3. Make the smallest supported Toolkit change. Do not duplicate an existing rule merely because an author ignored it.
4. Match verification to the change. Changed deterministic behavior needs a failing example and a valid control; documentation changes need accurate wording, commands and links. Reuse passed checks unless a new change, failure or unresolved concern warrants another run.
5. Use programs for mechanical checks and Astra for content review. Confirmed defects lead to actual repairs and checks of changed versions, without repeating unchanged attempts for a better score. A with/without comparison is optional and is planned separately when that question matters.
6. Retain useful reference examples and reasoned no-change decisions. They explain review criteria without imposing a universal writing template.

## What The Automated Runner Checks

- required artifacts exist
- `progress.json.stage` uses a canonical protocol stage, and `stage: final` appears if and only if `status: complete`
- expected sections appear
- must-cover entities appear
- backstage sources are traceable in `data/source_registry.csv`
- when a case requires reader references, they use reader-facing source titles rather than internal source ids
- case-specific forbidden headings, such as a rejected glossary or reference appendix, remain absent
- material follow-up requirement ids are present and resolved before terminal delivery
- completion is not claimed before the last configured material requirement turn
- the user-visible delivery message agrees with canonical progress state and open blockers
- the latest full-report or global-final review supersedes earlier reviews, is parseable, passes, and has no open issues
- a terminal receipt covers the global delivery and matches current cross-platform SHA-256 hashes for the final report, progress, review log, delivery message, and required backstage inputs (text newlines are normalized to LF)
- accepted-limitations records are checked for configured disclosure contradictions; ambiguous matches require separate review
- case-specific progress-size and control-file budgets detect process sprawl without imposing a global file-count rule
- uncertainty, risk, limitation, or counter-evidence is present
- claim/evidence/judgment language is present
- banned process phrases do not leak into `final.md`
- internal source ids do not leak into `final.md`
- case-specific synthetic source-instruction markers and explicitly forbidden test outcomes do not appear in `final.md`
- obvious eval/process language does not leak into `final.md`
- repeated template-like lines, sentence-level keyword stuffing, and high bullet-line ratios are flagged for review
- repeated source-listing templates are flagged because they show traceability without synthesis
- output is not obviously too short
- claim registries and review logs are not empty shells
- overconfident absolute claims are flagged when they lack uncertainty language
- progress or user-visible completion signals are flagged when unresolved issues or evaluator flags remain

These checks are intentionally mechanical. They catch regressions; they do not replace editorial judgment.

The synthetic source-boundary fixtures check configured strings: a canary and listed malicious outcomes are absent, and specified vendor figures and limitation terms are present. These checks do not establish semantic rejection of an instruction. They do not prove general prompt-injection resistance or detect every tool call, state mutation, secret disclosure, or semantic paraphrase.

## LLM Judge Status

This repo does not enable an LLM judge by default. The first line of defense is deterministic:

- artifact presence
- source registry coverage
- reader-facing references
- process-language leakage
- internal source-id leakage
- bullet density
- repeated source-listing templates
- output length
- late-requirement closure
- completion-claim timing
- global review scope
- current artifact hashes
- honest non-final delivery

Optional model reviews are recorded in the dated development packages, with separate reasons, critical-error flags and disagreements. They do not overwrite deterministic results. Current semantic evaluation uses LLM reviewers without a human-review prerequisite. Known-error and valid controls help inspect reviewer behavior; any optional comparison should state the tasks and conditions actually tested. Disclose reviewer context and evidence limits: model agreement is not factual ground truth.

The [current report/review plan](../docs/evaluation-roadmap.md#current-report-and-review-plan) uses Astra in a review context separate from the author; the same model may perform both roles. Programs measure exact length, and the author repairs confirmed problems. Give author and reviewer the same complete sources and necessary provenance, hiding author identity, private notes and condition mappings. No outside people or fixed panel are required. Historical reviewer counts remain historical records; preserve initial results and record repaired versions separately.

## 中文说明

这个目录是轻量评测闭环，不是模型排行榜。它检查 agent 是否呈现出框架要求的可观察符合性信号：研究范围校准、状态文件、来源和判断台账、质量门禁、来源指令隔离，以及干净的最终成稿。结果 schema v2 用 `conformance_status`、`conformance_score` 和 `conformance_flags` 表示机械符合性；`research_quality_status` 固定为 `not_evaluated`，不会把机械通过冒充为研究质量结论。

新的报告评测使用[现行评测标准](../docs/report-evaluation-standard.md#报告评测现行标准)：五维0–4分，保留首次交稿及其有效评审、原始缺陷和失败记录。原定缺失评审按原版本补齐；已授权改进中的真实缺陷直接修正，修订稿另存并复查，原结果保留。不对未改稿件重复评分；可选的使用效果比较另行记录。历史量表仅适用于原研究，不构成当前人工评审前提。

通用案例和检查器不依赖特定运行时。目录包含7个任务、22个反例夹具、4个正例夹具，以及23组成对语义诊断。9月10日新增三组已经过内部四模型诊断，并保留收费口径更正；相关历史评审与材料的当前公开入口见[数据管理仓库](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.zh-CN.md)；旧八次调用没有评过这三组。历史目录中的“未评审”等字段描述当时冻结的输入状态，当前诊断状态以目录说明和保留修订为准。历史材料的文件路径、数量和实际用途见公开集合索引。

使用方法：

1. 直接使用仓库已有案例。只有需要更新种子材料时才运行生成器，并写入新的输出目录。
2. 运行 `python scripts/run_evals.py --create-skeletons --allow-missing-output --runs-dir evals/runs`，在新的运行目录生成 prompt 和必要文件。
3. 把 `prompt.md` 交给待测 agent，保存实际输出与失败；运行 evaluator 生成机械符合性结果。
4. 阅读真实报告和来源，对照 LLM 评审核实问题，形成可复用的工具箱改进建议。
5. 修改工具箱后只做与改动有关的检查。上方 CI 清单列出仓库现有自动检查；它不调用模型，也不要求安装任何可选运行时。
6. 发布改动需完成 GitHub 推送、对应 CI 和适用的 Pages 部署，并核对实际公开内容。脚本通过不代表报告质量或项目整体已经验收。

语义评测由 LLM 承担，不要求人工评测或人工校准。模型判断、分歧、来源核实与机械检查分开记录；模型一致不等于事实正确。两模型八次公开调用保留共同漏检、严重性分歧、顺序和上下文敏感，以及两项修订的独立复审。修订不增加独立题目数，也不覆盖旧结果。

来源边界夹具核对配置中的 canary、禁用结论、供应商数字及限制词是否出现；它们不证明语义层面的指令拒绝，更不证明通用提示注入防御。长周期案例使用13轮需求和8家虚构公司材料，机械检查实体、关键词、纠错记录与完成状态；是否真正解释清楚公司差异仍须通过内容和证据审阅判断。

`python scripts/check_delivery.py <任务目录>` 默认核对保存的 `delivery_message.md` 与状态、评审、需求和文件哈希；提供 `--actual-message <回复文件>` 才会额外比对捕获的真实回复。它不直接读取聊天，也不证明文件中的用户授权、阅读记录或评审结论真实有效。
