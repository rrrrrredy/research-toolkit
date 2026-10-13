# Four-task wording recheck

[English](README.md) · [简体中文](README.zh-CN.md)

On October 13, one fresh-context `gpt-6-astra` reviewer assessed four existing real independent tasks after their evidence prefixes were corrected to distinguish task identity from constructed source material. It received only [judge-input.json](judge-input.json), containing evidence and balanced A/B candidates, without source labels, explanations, the [coordinator mapping](coordinator-map.json) or author history. This was one actual subagent review of four tasks and eight candidates; tasks and repeats are not added to the catalog count.

The [complete review](review.json), [response](response.md) and [input/context hash](context.json) are retained. Results: case-1 A flawed/B acceptable; case-2 A acceptable/B flawed; case-3 A flawed/B acceptable; case-4 A acceptable/B flawed. All eight judgments match the retained diagnostic labels. The reviewer judged each candidate independently and did not receive a requirement that exactly one candidate pass.

The changes affect task wording only: facts, calculations, bad/control excerpts and original labels remain unchanged. This confirms the recorded judgments on these four revised inputs, not all 23 current pairs or general Toolkit effectiveness. Historical inputs and reviews remain untouched. Current cases are assembled through the [dated overlay](../../semantic_diagnostics/wording-revisions-2026-10-13.json); no outside person, vendor or new task contribution is required.

Record verification: `python evals/repairs/2026-10-13-pipeline-complete/verify.py`.
