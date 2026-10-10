# Blinded pairwise pilot protocol

[English](eval-protocol.md) · [简体中文](eval-protocol.zh-CN.md)

**Status: protocol and executable harness only; no study results.** The existing public evidence remains n=2 development comparisons, unblinded for efficacy and toolkit-first in both tasks. Public records do not fully establish matched model and brief. A general Toolkit quality advantage remains unproven.

## Question and scope

For 5–10 distinct task families, does adding the pinned Toolkit's Lite instructions change the quality of a first report under the same declared model and resource ceilings? This small pilot uses fixed, publishable source texts and a single author response per condition. It evaluates **instruction-only Lite**, without MCP, retrieval, persistent agent state or internal independent review. It does not validate Full, whole-agent execution, open-web research or the historical four-reviewer study. The [current standard](report-evaluation-standard.md) supplies the five scoring dimensions; this separate pilot uses one blinded LLM judge per pair, as a diagnostic starting point rather than a general efficacy certificate.

Use tasks whose intended use genuinely permits fixed sources. Do not substitute an offline source pack for a task whose essential requirement is live search. Both conditions can self-check normally. The Toolkit condition receives the full pinned `SKILL.md`, workflow, research-standard and writing-style references; it is asked to keep planning, claims, section drafting and the Lite checklist in separate notes. Only the report is shown to the common judge. The baseline receives the same brief, sources and output envelope without Toolkit instructions. Instruction presence alone does not establish that the model followed the workflow; retain notes to inspect adherence separately from quality.

## Admit and freeze the cohort

1. Choose **5–10 different families**, fix the sample size before runs and state the target workload, selection method, language/task-type mix and exclusions. Include native English and Chinese tasks if both are part of that workload. Translations and repeated runs do not increase the family count.
2. Write a complete brief for each task: reader, use, questions, scope/cutoff, output language/length, source requirements and known boundaries. Do not supply the preferred answer. Preserve full source text, provenance and publication rights; URLs alone are insufficient.
3. Record prior exposure. Existing calibration, diagnostics and showcase tasks cannot become held out. The provided template deliberately has **no tasks**; filling it is a prospective cohort-selection decision, not generated evidence. Use `prospective_development` unless an exposure-controlled held-out claim is justified.
4. Pin author and judge model IDs/snapshot policy, Toolkit files, rubric, budgets, retry rule and analysis before any generation. `prepare` records the Git commit, actual file hashes, all briefs/sources, seed, assignments, Python version and harness hash in `coordinator/frozen.json`. `freeze-commitment.json` binds that exact snapshot. For preregistration, publish the commitment before execution while withholding the assignment key from judges. A hash cannot prove that a task was unseen.

## Configure once, run with one command

Copy [the configuration template](../evals/templates/blinded-study.json) into a dedicated directory such as `study/study.json`. Replace its endpoint/model values and explanatory placeholders, confirm source-publication rights, and add 5–10 task entries of this form. Paths are relative to the configuration file and must stay in its directory:

```json
{
  "task_id": "product-comparison-en",
  "family_id": "product-comparison-01",
  "language": "en",
  "task_type": "product_comparison",
  "brief": "briefs/product-comparison-en.md",
  "sources": ["sources/product-a.md", "sources/product-b.md"]
}
```

Use any compatible `/chat/completions` service with JSON output, request/usage metadata and the pinned returned model ID. Set `RESEARCH_EVAL_API_KEY` and `RESEARCH_EVAL_JUDGE_API_KEY` in the process environment if authentication is required; config stores **environment-variable names only**. Author and judge settings may use different endpoints or models, but the author configuration is identical across both conditions. The implementation uses the Python standard library; MCP dependencies are unnecessary.

From the repository root, with admitted inputs and credentials already configured:

```bash
python scripts/run_blinded_evals.py run --study study/study.json --seed 20261010 --output evals/runs/blinded-pilot-01
```

This command makes **paid model calls if the chosen service charges**: two author calls and, when both outputs are usable, one judge call per family. It refuses an existing output directory. It writes requests, original responses, usage/failures, masked judge packets, locked judgments and task-level results. No results are bundled with the harness.

To inspect/preregister without a model call, use `prepare` instead of `run`. Execute that exact frozen plan later with:

```bash
python scripts/run_blinded_evals.py execute --output evals/runs/blinded-pilot-01
```

The empty template fails admission rather than inventing tasks. `prepare` creates an empty results table marked pending. `execute` verifies the freeze hash and refuses a started run; partial attempts remain preserved. New supplements need a new directory and identity and cannot replace first attempts.

## Matching, randomization and masking

- **Matched author:** same model ID, brief, full sources, one fresh request, no conversation history, same maximum completion tokens, total-token ceiling and request deadline. No retrieval tools, repair feedback or retries in either arm. Log returned model identity, actual tokens and elapsed time. A different returned model, missing usage, truncation or exceeded budget is an unresolved failure, never a win for the other arm.
- **Budget boundary:** the endpoint receives the completion limit. Total usage and elapsed time are also checked after the response; these checks detect a violation, not guarantee a billing cap or remote cancellation. Toolkit inputs contain more tokens, so equal ceilings do not mean equal realized cost. Report actual usage; do not claim equal cost or guaranteed snapshot stability.
- **Run order:** a seeded, balanced list chooses which condition runs first (counts differ by at most one for an odd cohort); pairs are shuffled and each pair's two calls are adjacent. The exact order and seed are logged. A separate seeded stream randomizes A/B presentation per pair. These are prospective assignments, not a reconstruction of history.
- **Blinded judge:** a fresh request receives only the identical brief/sources, rubric and reports A/B. It never receives assignments, condition names, author notes, model metadata, seed or generation order. Only `judge-inputs/` is suitable for a human judge; keep `coordinator/` and the repository context inaccessible during rating. This implementation runs the LLM route; a human study needs separately frozen identity and collection procedures.
- **Residual clues:** reports are passed verbatim, without selectively editing style or removing defects. The judge reports recognizable condition clues after rating. Masking the assigned label does not guarantee successful blinding; investigate leaked labels and disclose clues. Using separate requests does not guarantee statistically independent errors or prevent provider-side shared effects.

## Fixed rubric, failures and interpretation

The versioned [rubric](../evals/rubrics/blinded-pairwise.v1.json) covers task fidelity; facts and evidence; explanation and synthesis; counterevidence and boundaries; reader usefulness. Each dimension receives 0–4 or `not_assessed`, with a located report excerpt, reason and source evidence. Anchors range from an absent/failed requirement (0), through substantive revision needed (2), to fully developed concrete support (4). Do not create a weighted passing score.

The primary pilot outcome is the judge's preference: A, B, tie or unresolved, decoded only after all first judgments/failures lock. These are **unadjudicated LLM preferences**, not confirmed necessary-defect counts. Report all admitted families and failures; separate execution completion from quality. Keep all raw replies, malformed outputs, disagreements and decisive reasons. Do not score missing author/judge output as zero, drop families after seeing results, rerun a valid negative judgment or substitute repaired reports. Check consequential findings against sources before interpreting a preference as evidence of an actual defect; [existing necessary-defect labels](necessary-defects.md) are unchanged.

Show per-task outcomes and dimension scores, language/task mix, model/version, actual usage and missingness. With 5–10 families this is a small pilot; avoid general superiority or precise population estimates. Any larger effect estimate, confidence-interval method, additional judge or sample extension needs a new preregistered design. Software checks only verify bookkeeping and transport behavior.

## Raw artifacts and publication

```text
coordinator/frozen.json             # config, seed, assignments, exact methods/briefs/sources
coordinator/freeze-commitment.json
coordinator/author/<pair>/<arm>/     # request, raw response, execution/usage, parsed or invalid
judge-inputs/<pair>.json            # only brief, sources, rubric, reports A/B
judgments/<pair>/                  # request, raw judgment, usage, parsed or invalid
judgments.lock.json                # locks first attempts before condition decoding
results.json / results.md           # all admitted families, including unresolved
bundle-manifest.json                # hashes of all retained files
```

`evals/runs/` remains ignored local output. After all first judgments lock, review publication rights and secrets, then commit the **whole bundle**, including assignment key, raw outputs, judgments and failures, to a new `evals/studies/<study-id>/` directory using `git add evals/studies/<study-id>`. Do not commit a summary alone or overwrite dated diagnostics. If material needs redaction, preserve its hash and disclose exactly what was withheld; narrow the public reproducibility claim accordingly. Never commit API keys. Retain the manifest and check its hashes before publication.

## Results

Pending: no author runs, blinded judgments or new effect estimates have been collected for this protocol.

| Cohort | Admitted families | With-toolkit preferred | Without-toolkit preferred | Ties | Unresolved |
| --- | --- | --- | --- | --- | --- |
