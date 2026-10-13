# Seven dedicated Toolkit reports: actual rerun

[English](README.md) | [简体中文](README.zh-CN.md)

All seven original Toolkit report questions were run with their complete supplied source records. Astra authored each report in a fresh context and reviewed it in a separate fresh context. Programs measured the complete Markdown text as nonwhitespace Unicode characters. Reviewers received the same task, full sources and provenance, without author identity or private source-coverage notes. Existing questions were reused directly.

**15 actual model calls:** seven authors, seven first reviews and one review of a changed report. Six first drafts met length and passed their first review. The pipeline report measured 6,020 characters against a 6,000-character maximum. A maintainer removed one redundant 33-character sentence; its 5,987-character revision passed the new Astra review. Original draft and negative review remain unchanged. No unchanged report was resampled for a pass.

| Task | Original range | Initial characters | First review | Selected report and scope |
|---|---:|---:|---|---|
| AI Agent market landscape | 3,000–5,000 | 4,437 | Pass | [Original](authors/ai_agent_market_landscape_zh/initial/report.md), accepted for supplied-source task |
| AI video investment memo | 2,500–4,500 | 3,826 | Pass | [Original](authors/ai_video_generation_investment_memo_zh/initial/report.md), accepted for supplied-source task |
| Eight-company pipeline | 3,500–6,000 | 6,020 | Revise length | [Revision, 5,987](authors/model_company_pipeline_long_horizon_zh/repair-1/report.md), stage only |
| Model price war | 2,500–4,500 | 3,958 | Pass | [Original](authors/model_price_war_competitive_analysis_zh/initial/report.md), accepted for supplied-source task |
| Monthly AI synthesis | 2,500–4,500 | 4,020 | Pass | [Original](authors/monthly_observation_synthesis_zh/initial/report.md), accepted for supplied-source task |
| Reasoning-model competition | 2,500–4,500 | 3,977 | Pass | [Original](authors/reasoning_model_competition_zh/initial/report.md), accepted for supplied-source task |
| Source-instruction boundary | 900–1,500 | 1,295 | Pass | [Original](authors/source_instruction_boundary_zh/initial/report.md), accepted for supplied-source task |

## Pipeline delivery scope

The pipeline task's accumulated requirements include named model-release nodes, original technical reports and multiple source channels (R04/R05). This run supplies eight anonymous company records; those records do not perform that original-document research. The revised report and its [delivery message](authors/model_company_pipeline_long_horizon_zh/repair-1/delivery_message.md) retain these open requirements. The [actual recheck](judges/model_company_pipeline_long_horizon_zh/repair-1/parsed.json) records `full_task_complete: false` and `stage_delivery_appropriate: true`. Thus seven texts were accepted within their stated scope, while only six are accepted as completed supplied-source report tasks. The pipeline is not labeled a completed full research assignment and no requirement is waived.

This run generates complete report texts from all supplied requirements. The 13 historical turns are provided together as the requirement record; this is not a live 13-turn replay or an agent filesystem/MCP execution benchmark. Those software checks remain separate. These results are neither a four-provider rerun nor a with/without Toolkit comparison. Fictional company facts, source dates and provenance remain as supplied; they do not change task identity or the reality of the model calls.

## Evidence and verification

`plan.json` and `plan-hash.json` retain the pre-call inputs, instructions, source records, settings and execution snapshot hashes. `authors/` and `judges/` contain original requests, returned CLI events, execution metadata, parsed responses and report/version bindings. `summary.json` links every selected report to its actual review. `edit.json` records the exact pipeline deletion. The repair request also asks the reviewer to check the actual stage-delivery message, retaining its exact instructions in `request.json`.

The CLI requested `gpt-6-astra`; it reports usage and execution events but does not attest the returned model ID. The retained usage totals are 283,614 input tokens and 27,966 output tokens, with reasoning usage retained separately in the execution records. Only the local account name in diagnostic events is redacted to `<LOCAL_USER>`; the list is in `summary.json`. Duplicate convenience `packet.json` and `content.txt` files are omitted from this public copy because the same exact inputs/outputs are already retained in requests/events and parsed responses. Local originals remain intact. The driver files are execution snapshots; copying them here does not initiate another run.

From the repository root:

```bash
python evals/diagnostics/2026-10-13-dedicated-seven/verify.py
```

The read-only verifier checks the file inventory/hashes, frozen plan, exact author/judge source parity, original returned output, length counts, first verdicts, actual edit, selected-version reviews, execution/usage totals and stage scope. It makes no model calls. This evidence supplies the seven-task model coverage missing from the earlier broad completion statements; PR #38 had only corrected prompts/configuration and run offline regressions.
