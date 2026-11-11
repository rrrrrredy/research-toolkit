# Local MCP call example

[English](README.md) · [简体中文](README.zh-CN.md)

The fictional shipment note demonstrates interface calls, not a complete research task or quality study. The current capture prepares independent agent tool assignments; it does not replay the supplied historical author self-review. See the [quickstart](../../docs/quickstart.md) for complete research.

After installing `requirements-mcp.txt`, run from the repository root:

```bash
python examples/mcp/capture.py --output ../mcp-example-run --host-task "ACTUAL_AGENT_TASK_OR_SESSION_ID"
```

Replace `ACTUAL_AGENT_TASK_OR_SESSION_ID` with the real ID of the agent running this command. The script imports the existing example manuscript and registers it with `main=true`, that agent identity, sources and claims through real MCP stdio, after creating the task and loading methods. It saves references to complete independent assignments in `review-request.json`. The agent tool dispatches native agents to read the assignments and originals and perform the actual reviews. The first command stops with independent review assignments ready, before report acceptance. Usage uploads are disabled for this example.

Submit a completed assignment using a JSON file containing `slot_id`, the actual `host_task`, and original `response_path` and `execution_path`:

```bash
python examples/mcp/capture.py --output ../mcp-example-run --resume --host-result actual-result.json
```

The original response quotes its `input_version` and `assignment_version`. The execution capture retains the actual agent identity, completed status and assignment version. See the [independent review interface](../../docs/review-completion.md). Actual content reviews, independent audit and separate final acceptance precede `finish`; only the current completed contract permits delivery. `transcript.json` preserves every actual MCP request and return.

The [October 10, 2026 capture](history/captured.json), `history/self-review.json` and its binding preserve the historical implementation and results. The current script does not submit them as independent opinions or apply their old receipt to new work.

The frozen inputs and original hashes are preserved together in [history/](history/), including `start.json` before its legacy parameter was removed. Current execution does not validate new inputs against the historical self-review binding.
