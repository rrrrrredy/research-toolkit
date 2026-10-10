# Record the MCP workflow

[English](mcp-demo.md) · [简体中文](mcp-demo.zh-CN.md)

Recording slot: **pending**. Place an English demo at `docs/assets/mcp-workflow.en.gif` (or `.cast` for asciinema), and a Chinese-captioned version at `docs/assets/mcp-workflow.zh-CN.gif` / `.cast`. No recording is included or claimed yet.

1. Install the MCP dependency and open the [example](../../examples/mcp/README.md). Use the supplied fictional inputs, a clean terminal and an output directory outside the repository.
2. Show `research_start → research_guide → research_review → research_finish`, including source/claim files, the self-review prompt, its second submission and the degraded marker. Keep the intervening status call visible or explain it in captions.
3. For a terminal recording, run `asciinema rec mcp-workflow.en.cast`, execute `python examples/mcp/capture.py --output ../mcp-recording-run`, inspect `transcript.json` and the review/receipt, then exit the recording. For a client GIF, record the same real tool calls in your MCP client.
4. Remove credentials, account details and personal filesystem paths from the recording. Preserve the fictional-data and self-review labels. Trim idle time without splicing in invented successful responses.
5. Export a small GIF or retain the `.cast`; add an accessible caption and replace the README recording-slot link with the actual file link in both languages. The recording demonstrates software calls, not improved research quality.
