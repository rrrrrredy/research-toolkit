# A local MCP workflow example

[English](README.md) · [简体中文](README.zh-CN.md)

This is a three-paragraph English report about an explicitly fictional shipment note. It demonstrates Full with self-review; it is not a research evaluation or an independent opinion. The report, source, registries and substantive author-context review are supplied. Lite remains the recommended first research task and skips review.

After installing `requirements-mcp.txt`, run from the repository root:

```bash
python examples/mcp/capture.py --output ../mcp-example-run
```

Use a new, short output path outside the checkout (especially on Windows). The script starts `scripts/research_mcp.py` over real stdio, calls start and guide, copies the supplied author files to the returned task directory, advances to draft with status, requests the self-review prompt, submits the supplied review with the current input version, then calls finish. It replays an existing author review; it does not call a model or generate a fresh assessment. For a new research task, the agent must write and review the actual report.

Expected files: `transcript.json` with full MCP responses, `review-request.json`, and `tasks/shipment-note/` containing the report, source/claim CSVs, `logs/review.jsonl`, review response files, and `state/final_delivery.json`. The review and receipt retain `reviewer: self` and `review_strength: degraded`; the finish response has `completed: true`.

[Published capture](captured.json) contains complete inputs and selected response fields from the 10 October 2026 local execution. Large method text, repeated prompt retrieval, local paths and detailed checks are omitted; the remaining fields are copied from server responses. Runtime IDs and timestamps may differ on a rerun.

To read the actual assignment before submitting a review, add `--pause-before-review`; inspect `review-request.json`, then resume with the same `--output` and `--resume`. The stored review only applies to the supplied unchanged report and source; the script checks input hashes and refuses changed example files. [Recording instructions](../../docs/assets/mcp-demo.md).
