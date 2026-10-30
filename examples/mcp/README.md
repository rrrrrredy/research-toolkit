# Local MCP call example

[English](README.md) · [简体中文](README.zh-CN.md)

The fictional shipment note demonstrates interface calls, not a complete research task or quality study. The current capture prepares independent host assignments; it does not replay the supplied historical author self-review. See the [quickstart](../../docs/quickstart.md) for complete research.

After installing `requirements-mcp.txt`, run from the repository root:

```bash
python examples/mcp/capture.py --output ../mcp-example-run
```

The script uses real MCP stdio to create the task, load methods and register the supplied materials. It saves references to complete independent assignments in `review-request.json`. The host dispatches native agents to read the assignments and originals and perform the actual reviews. Missing required results leave the task incomplete.

Submit a completed assignment using a JSON file containing `slot_id`, the actual `host_task`, and original `response_path` and `execution_path`:

```bash
python examples/mcp/capture.py --output ../mcp-example-run --resume --host-result actual-result.json
```

The original response quotes its `input_version` and `assignment_version`. The execution capture retains the actual host identity, completed status and assignment version. See the [independent review interface](../../docs/review-completion.md). Actual content reviews, independent audit and separate final acceptance precede `finish`; only the current completed contract permits delivery. `transcript.json` preserves every actual MCP request and return.

The [October 10, 2026 capture](captured.json), `self-review.json` and its binding preserve the historical implementation and results. The current script does not submit them as independent opinions or apply their old receipt to new work.
