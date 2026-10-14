# Research Toolkit plugin

[English](README.md) | [简体中文](README.zh-CN.md)

One installation bundles the research Skill, detailed methods and eight local MCP tools. The agent clarifies the brief, researches and writes with its own tools, then executes the selected review and delivery checks through the shared workflow.

Use the host's supported plugin installation mechanism. The guide below covers Python 3.10+ and MCP dependencies. Bundled manifests launch `python`: the interpreter found by the host process must have the dependencies installed. If the host cannot select that environment for the plugin, connect MCP separately with the absolute virtual-environment interpreter path from the guide.

Open a new session, select Research Toolkit, and confirm the eight `research_*` tools appear. Supply a question or existing report, sources and intended use; the agent recommends Lite/Full and maintains the working records.

**[Full installation and usage guide](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.md)** · [Research instructions](SKILL.md) · [Complete standard](references/research-standard.md)

New Full tasks without a backend use explicitly degraded self-review. Configure a CLI or compatible HTTP backend for external/independent review. Lite skips review and full delivery gates while retaining its final checklist. Declared independent reviews, evaluations and audited plans never silently downgrade. The usage guide explains data destinations, account usage and configuration checks.

The portable `plugin.json` / `mcp.json` and Codex-compatible `.codex-plugin/plugin.json` / `.mcp.json` start the same implementation. MCP is local stdio, not a hosted HTTPS endpoint. The package includes no credentials. Mechanical checks do not certify research quality.

For maintainers, the package's core files are generated from the repository with `python scripts/build_plugin.py`; `--check` detects divergence. Edit the shared source first.

Generated ownership is recorded in `.generated-files.json`. Read-only `--check` compares contents and managed paths; builds delete obsolete copies only when their recorded hash still matches. Handwritten metadata and unmanaged content remain; inspect unknown ownership or modified obsolete files before proceeding.
