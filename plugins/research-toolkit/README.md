# Research Toolkit plugin

[English](README.md) | [简体中文](README.zh-CN.md)

One installation bundles the research Skill, detailed methods and six local MCP tools. The agent clarifies the brief, researches and writes with its own tools, then executes the selected review and delivery checks through the shared workflow.

For Codex, with Python 3.10+, Git and Codex CLI installed:

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

Open a new session, select Research Toolkit, and confirm the six `research_*` tools are available. Describe the topic, intended reader and desired output; the agent asks about missing critical requirements.

**[Full installation and usage guide](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.md)** · [Research instructions](SKILL.md) · [Complete standard](references/research-standard.md)

New Full tasks without a backend use explicitly degraded self-review. Configure a CLI or compatible HTTP backend for external/independent review. Lite skips review and full delivery gates while retaining its final checklist. Declared independent reviews, evaluations and audited plans never silently downgrade. The usage guide explains data destinations, account usage and configuration checks.

The portable `plugin.json` / `mcp.json` and Codex-compatible `.codex-plugin/plugin.json` / `.mcp.json` start the same implementation. MCP is local stdio, not a hosted HTTPS endpoint. The package includes no credentials. Mechanical checks do not certify research quality.

For maintainers, the package's core files are generated from the repository with `python scripts/build_plugin.py`; `--check` detects divergence. Edit the shared source first.
