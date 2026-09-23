# Evaluations

[English](README.md) | [简体中文](README.zh-CN.md)

This directory contains seven research cases, twenty-two negative fixtures, four positive fixtures, and report diagnostics for Research Toolkit. The cases and evaluator are runtime-neutral; no particular agent runtime is required. The offline checks examine the research brief, task files, sources and claims, review records, source-instruction boundaries, and final prose. They report those checks, not a model ranking or an overall report-quality verdict.

Evaluator result schema v2 keeps two claims separate. `conformance_status`, `conformance_score`, and `conformance_flags` describe deterministic structure, traceability, and configured failure signals. `research_quality_status` is `not_evaluated`; the runner does not claim that a mechanically conforming report is insightful, accurate, or decision-useful.

Missing required files block a pass regardless of score. Malformed requirement or conversation JSONL and invalid source or claim CSVs produce explicit failure findings; a damaged case does not prevent the remaining cases from being reported. CSV counts use logical records, and source IDs and titles must match within the same record.

Actual outputs are available in the [2026-09-07 development package](./diagnostics/2026-09-07/): four original calibration reader reports, two repairs, three-model text replies and an explicitly retained incomplete response. These are development diagnostics, not held-out efficacy results.

## Directory Layout

Existing consumers can use the [schema v2 migration guide](../docs/evaluator-v2-migration.md). The [delivery checker interface](../docs/delivery-verification.md) documents intended-message binding and the limits of optional actual-reply comparison.

New report studies follow the [current evaluation standard](../docs/report-evaluation-standard.md). It separates first-submission scoring from reader-ready delivery and product-effect testing. Complete missing original reviews; preserve valid reviews, sample defects and raw failures for Toolkit improvements. Report repair is not a prerequisite for completing an evaluation. See the [historical rubric boundary](./rubrics/) before using older scales or frozen reviewer counts; they do not belong in current five-dimension 0–4 results.

See the [source-data audit](../docs/evaluation-data-audit.md) for provenance and exclusion decisions, and [semantic diagnostic pairs](./semantic_diagnostics/) for twenty-three author-proposed bad/control pairs. The three reader-review pairs added on September 10 received an internal four-model diagnosis, with a retained pricing-scope correction. Those private reviews are not in this repository and were not part of the eight earlier public calls. These excerpts are development data, not held-out tasks or validated quality labels.

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

`report.json` uses `result_schema_version: 2`. A `pass` means mechanical conformance only. `review` and `fail` return a non-zero exit code by default; use `--allow-review` only for exploratory collection. Set both report paths when using another output directory. Record semantic reviews, reviewer disagreements and evidence limits separately from the conformance score. The dated public packages do not contain all separately maintained private evaluation studies.

## Check A Delivery Claim

For a task that uses the terminal-delivery artifacts, validate the intended user-visible message against current state and current hashes:

```bash
python scripts/check_delivery.py <task-directory>
```

The checker reads the intended message in `delivery_message.md`. To compare an independently captured reply, pass `--actual-message <reply-file>`; it does not read the chat application itself. A plainly labeled non-final stage artifact can pass without a terminal receipt.

Under the default delivery contract 3, a terminal claim requires consistent `final/complete` state, no open blockers, parseable passing global and task-required reviews bound to the current report, and a `global_final_delivery` receipt binding the required files. Declared model-review slots, substantive-validity audits, finding dispositions, independent adjudication and sampling must also be complete. Requirements closed as waived, out of scope or accepted limitations need specific recorded user decisions; declared required reading is checked against source records. Recognized disclosure contradictions fail, while ambiguous disclosure matches require review. See the [delivery checker interface](../docs/delivery-verification.md) for the exact contract and legacy mode.

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

1. Preserve original inputs, outputs, reviews, failures and costs. Complete an originally required missing review without repairing the sample or replacing an already valid review.
2. Check each finding against the task, report and evidence. Distinguish method defects, execution failures, source limitations and unsupported reviewer suggestions.
3. Make the smallest supported Toolkit change. Do not duplicate an existing rule merely because an author ignored it.
4. Match verification to the change. Changed deterministic behavior needs a failing example and a valid control; documentation changes need accurate wording, commands and links. Reuse passed checks unless a new change, failure or unresolved concern warrants another run.
5. Keep mechanical conformance separate from semantic quality. Any new product-effect study needs frozen versions, task selection, a call budget and a stopping rule before execution. Negative results do not trigger report repairs or extra rounds until scores improve.
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

Optional model reviews are recorded in the dated development packages, with separate reasons, critical-error flags and disagreements. They do not overwrite deterministic results. Current semantic evaluation uses LLM reviewers without a human-review prerequisite. Known-error and valid controls help inspect reviewer behavior; general effect claims need separate held-out testing. Disclose reviewer context and evidence limits: model agreement is not factual ground truth.

The [current report/review plan](../docs/evaluation-roadmap.md#current-report-and-review-plan) specifies one author and four model reviewers receiving the same complete input version, with each opinion locked before cross-reviewer comparison. The selected models are a study configuration, not Toolkit dependencies. Preserve earlier freezes and label later supplementary reviews separately. Complete originally missing reviews; use defects and evidence-based recommendations to improve the Toolkit. Repaired reader deliverables or repair-method experiments, when separately required, remain distinct from first-submission evaluation. This repository's dated packages do not establish a general product-effect result.

## 中文说明

这个目录是轻量评测闭环，不是模型排行榜。它检查 agent 是否呈现出框架要求的可观察符合性信号：研究范围校准、状态文件、来源和判断台账、质量门禁、来源指令隔离，以及干净的最终成稿。结果 schema v2 用 `conformance_status`、`conformance_score` 和 `conformance_flags` 表示机械符合性；`research_quality_status` 固定为 `not_evaluated`，不会把机械通过冒充为研究质量结论。

新的报告评测使用[现行评测标准](../docs/report-evaluation-standard.md#报告评测现行标准)：五维0–4分，保留首次交稿及其有效评审、原始缺陷和失败记录。原定缺失评审需要补齐；已完成评审的样稿不因低分或缺陷进入修稿返评循环。评审发现用于改进研究工具箱，稿件交付和产品效果研究分别记录。历史量表仅适用于原研究，不构成当前人工评审前提。

通用案例和检查器不依赖特定运行时。目录包含7个任务、22个反例夹具、4个正例夹具，以及23组成对语义诊断。9月10日新增三组已经过内部四模型诊断，并保留收费口径更正；私人评审原文未公开，旧八次公开调用没有评过这三组。历史目录中的“未评审”等字段描述当时冻结的输入状态，当前诊断状态以目录说明和保留修订为准。公开材料也不等于全部私人评测研究。

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
