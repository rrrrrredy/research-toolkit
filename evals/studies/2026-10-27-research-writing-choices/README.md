# Research choices: two prose comparisons

[English](README.md) | [简体中文](README.zh-CN.md)

**The added examples accompanied local improvements and omissions, not consistently better reports or observed reductions in substantive rework.** The archive-digitization draft derived a useful license-price threshold, but left another savings threshold's feasibility unexplained and omitted a trial-labor budget condition. The cold-chain draft explained why thermal-test headroom is not a guaranteed rescue window; both drafts still need to distinguish availability this season from delivery next week. The passage-level findings and first blinded reviews are retained below; there is no aggregate score.

Retain the three examples as optional reading within the existing writing method. Actual prose supplied useful cost reasoning and mechanism explanation, but adding the examples together did not prevent omissions. Both versions already rejected irrelevant marketing claims. These two pairs cannot establish an effect for each individual example, and do not justify more rules or sampling.

## Change and provenance

Baseline: `8e3db9db49aeda63bc9c3b1790da7702f8b66649`, v1.4.8. The product change adds three question/material–original gap–rewritten passage–reason examples to both `references/writing-style.*` files and their plugin copies. The research entry, tools, fields, completion requirements and review configuration are unchanged.

1. Predictive maintenance: retain the downtime observation and develop the connections among attribution, economic value and multiyear prepayment.
2. Scope-3 RFQs: remove repeated writing advice and use the passage to establish whether the material fits the buyer's question.
3. Maple storage: use an explicitly constructed follow-up requirement to revise affected judgments while retaining valid analysis.

The first two are teaching adaptations of archived original and revised reports; the third's changed requirements were constructed for this example. The original cases use synthetic material, not real-company facts. Original reports and historical records remain unchanged. Different wording and structures can be valid; a desired conclusion remains subject to the question and evidence. The [reference-reading record](reference-reading.md), in Chinese, identifies the post, seven inspected images and existing method coverage. No third-party full article or image is redistributed here.

## Execution

- Two new constructed tasks: archive-digitization procurement/work allocation and a food cooperative's cold-chain decision revision. Neither appears in the teaching examples, and no target final answer was provided. The cold-chain input includes an old brief to revise, not an answer under the new requirements.
- Fixed `gpt-6-astra`, `high` reasoning and `default` service tier, with identical task material and other methods. Codex CLI exposes no generation seed or temperature setting used here; all calls used the same service defaults. This is not a claim of token-identical reproducibility.
- One generation per method per task: **4 author calls**. Order was before→after for archives and after→before for cold chain. Fresh contexts received fixed common methods and the relevant writing-method version directly. There were no web/tool calls, follow-ups, author repairs or reruns. No separate self-check was requested or fabricated.
- Each pair received **one blinded review in a fresh context**, using the same model: **2 review calls**. Review inputs contained task/materials, numbered prose and passage-comparison instructions, without methods, version names, timing or an expected winner. This did not add a review layer to the product.
- A/B labels were shuffled with a fixed seed before execution; both happened to map A=after, B=before. The [mapping](coordinator-map.json) was not supplied to reviewers. The maintainer subsequently checked review claims against the inputs; that subsequent analysis was not blind.
- Totals: **2 tasks, 4 first outputs, 2 first reviews, 6 CLI model calls**. All returned a single report/review and exited 0. CLI events show no tool calls or generation retries. Backend retry telemetry was unavailable, so six is not a measured count of independent HTTP requests.

These calls generated or revised research prose, rather than selecting candidate paragraphs. They compare the entire three-example addition, not individual examples, natural method-loading behavior or Toolkit's general benefit.

## Passage-level observations

Numbers refer to the anonymous inputs: [archive A](reviews/archive-digitization/A.md), [archive B](reviews/archive-digitization/B.md), [cold-chain A](reviews/cold-chain-revision/A.md), [cold-chain B](reviews/cold-chain-revision/B.md). A is after; B is before. Original outputs and reviews are Chinese; this summary does not translate or replace them.

| Task and passages | Observed difference | Assessment and remaining work |
| --- | --- | --- |
| Archive A08 / B07 | B requires savings to cover the license; A derives about 106.7 hours saved on printed forms and a license price near RMB 10,700 for cost parity. | Useful negotiation reasoning; it does not change the recommendation against buying now. |
| Archive A08 | A also requires 400 hours saved to cover a RMB 40,000 license, without explaining that all manual work on printed forms takes only about 213.3 hours. | Arithmetic is correct, but that threshold is unreachable within the current printed-forms-only scope. State the scope rather than implying that further print speed improvements alone could reach it. |
| Archive A08 / B07 | B explicitly budgets trial labor and asks for comparable originals and category-specific error records; A specifies no extra license charge and records all labor. | A omits an execution condition. Restore the labor-budget constraint and comparable inputs. A05 also states operator proficiency and representativeness limits less explicitly than B04. |
| Archive A07 / B02, B06 | A starts planning at 640 hours and updates from the first batch. B first denies a reliable range, then recommends planning at 613–640 hours. | A offers clearer implementation. B should resolve its range ambiguity; actual staffing must still be secured for both. |
| Archive A02, A04–A06 / B02–B05 | Both recover 14 omitted labor hours, compare complete category-based costs, separate character accuracy from pages with key-field errors, and reject causal inference from confounded batches. | No incremental core decision or calculation benefit. A table is not inherently better than paragraphs. |
| Cold-chain A02, A04 / B01, B02 | A explicitly preserves the old decision's validity and says the price cut did not improve performance. B already connects new orders/prices to the original same-configuration test. | More explicit explanation, not a new ability absent from B. |
| Cold-chain A05–A06 / B05–B06 | A explains that one extra test hour is not a rescue window: waiting and transfer consume thermal headroom; it retains temperature control during transfer. | Specific mechanism improvement. B made no false guarantee, but explained less. |
| Cold-chain A06 / B06 | B asks for a route-specific backup arrival limit and breach terms; A more generally asks to clarify dispatch and responsibility. | Restore the specific gap corresponding to the new promotional claim in A. |
| Cold-chain A01, A06 / B01, B06 | Materials establish availability this season, not arrival before next week's start. A's opening broadly says requirements are met; B also leaves this distinction implicit there. | Both should separate selection from the exact delivery date still to confirm. This does not overturn valid price/capacity/thermal comparisons. |
| Cold-chain B02; marketing material in both tasks | B's warning against unlimited order growth is irrelevant to the current 76 boxes; A omits it. Both exclude awards, language counts and other irrelevant selling points. | Small deletion difference; no additional benefit in rejecting marketing. Neither transfers teaching-example names, numbers or conclusions into the new tasks. |

First reviews: [archive](reviews/archive-digitization/output.md), [cold chain](reviews/cold-chain-revision/output.md). Maintainer source checks support the observations above, including the 400-hour scope and exact delivery-date issues. These are substantive edits still needed, not completed human revisions. Human rework time was not measured; edit counts are not a score. All four first drafts remain unchanged, rather than being repaired and presented as generation results.

## Actual elapsed time

| Task | Before | With examples | First blinded review |
| --- | ---: | ---: | ---: |
| Archive digitization | 84.938 s | 84.109 s | 170.594 s |
| Cold-chain revision | 59.781 s | 62.907 s | 137.672 s |

Author processes total **291.735 s**; reviews total **308.266 s**; all six total **600.001 s**. Monotonic process wall time includes CLI startup and network/model latency, excluding preparation and maintainer reading. Reported input usage increases by 1,893 tokens per author call with the examples. No bill or speedup is inferred.

The first archive baseline logged a model-catalog refresh timeout but completed generation. Calls retain PowerShell shell-snapshot and unstable-feature warnings. Warnings were not deleted or counted as extra generations. Service variability prevents attributing differences of a few seconds to the methods.

Configuration, UTC start/end times, usage and event types are in [execution-summary.json](execution-summary.json) and each run's `command.json`, `execution.json`, `events.jsonl`, `event-times.jsonl` and `stderr.txt`.

## Evidence and reproduction

- [Frozen plan](plan.json), [common method](methods/common.md), [before Chinese method](methods/before/writing-style.zh-CN.md), [after Chinese method](methods/after/writing-style.zh-CN.md), and English snapshots. Author prompts used Chinese; English was checked for synchronization only.
- [Archive task](tasks/archive-digitization/input.md) and [before](runs/archive-digitization/before/output.md)/[after](runs/archive-digitization/after/output.md) outputs.
- [Cold-chain task](tasks/cold-chain-revision/input.md) and [before](runs/cold-chain-revision/before/output.md)/[after](runs/cold-chain-revision/after/output.md) outputs.
- Each `request.txt` is the complete actual input; `command.json` preserves exact arguments. Reproduction can reuse the request, model and settings after replacing local CLI/work/output paths. Stochastic output need not be identical. No reproduction was run this round.
- [raw-manifest.json](raw-manifest.json) records SHA-256 for 63 frozen methods, tasks, inputs, raw outputs, logs and other evidence files. It excludes these explanatory READMEs and subsequent verification records.

Work stops here: no old-case reruns, repeated sampling, label-swapped reviews, product-code changes or release.
