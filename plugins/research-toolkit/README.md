# Research Toolkit plugin

[English](README.md) | [简体中文](README.zh-CN.md)

One installation bundles the research Skill, detailed methods and nine local MCP tools. The agent clarifies the brief, researches and writes with its own capabilities. When task management is needed, the bundled MCP exposes the same local operations as the CLI.

Install the complete unpacked [version-pinned release package](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/installation-versioning.md#install-a-version-pinned-skill) using the host's plugin mechanism. Bundled manifests launch `python`, so install the MCP dependencies in the Python 3.10+ interpreter the host finds. If the host cannot select that interpreter, connect MCP separately using the absolute virtual-environment interpreter path.

Open a new session, select Research Toolkit, and confirm the nine `research_*` tools appear. Supply a question or existing report, sources and intended use; the agent uses the complete research methods. Installing the plugin makes tools available; it does not require creating a managed task for every report.

**[Full installation and usage guide](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.md)** · [Research instructions](SKILL.md) · [Complete standard](references/research-standard.md)

New tool-managed tasks use independent host agents for grouped review, audit and readiness assessment. Follow the host's available slots. The user explicitly accepts the current report before `finish` records completion. Native delegation uses the host's existing access.

Basic usage recording is off on new installations. The package's host hooks record operations only when recording is enabled. Sharing a report requires separate consent. [Usage data and controls](docs/usage-data.md).

The portable `plugin.json` / `mcp.json` and Codex-compatible `.codex-plugin/plugin.json` / `.mcp.json` start the same implementation. MCP is local stdio, not a hosted HTTPS endpoint. The package includes no credentials. Mechanical checks do not certify research quality.

For maintainers, the package's core files are generated from the repository with `python scripts/build_plugin.py`; `--check` detects divergence. Edit the shared source first.

Generated ownership is recorded in `.generated-files.json`. Read-only `--check` compares contents and managed paths; builds delete obsolete copies only when their recorded hash still matches. Handwritten metadata and unmanaged content remain; inspect unknown ownership or modified obsolete files before proceeding.
