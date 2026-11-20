# Quick install for Research Toolkit

[English](quickstart.md) · [简体中文](quickstart.zh-CN.md)

## Install the Skill

1. Download the plugin ZIP and `SHA256SUMS` from the [latest release](https://github.com/rrrrrredy/research-toolkit/releases/latest). [Verify the checksum and unpack the ZIP](installation-versioning.md#install-a-version-pinned-skill).
2. Place the unpacked `research-toolkit` folder in your agent's skill directory below. Open it and check that it directly contains `SKILL.md` and `references/`. For an existing installation, follow the [update instructions](installation-versioning.md) to preserve local changes.
3. Reopen the agent in the project and confirm it can load the Skill.

| Agent | Project installation path | How to confirm installation |
| --- | --- | --- |
| [Codex CLI / IDE](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/codex.md) | `.agents/skills/research-toolkit/` | Search the skill picker for `research-toolkit`. Codex may display `research-toolkit:research-toolkit`; the project entry points to this folder’s `SKILL.md`. |
| [Claude Code](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/claude.md) | `.claude/skills/research-toolkit/` | Invoke `/research-toolkit` in the project session to load the Skill. |
| [OpenCode](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/opencode.md) | `.opencode/skills/research-toolkit/` | With skill access allowed, ask the agent to load `research-toolkit`. It can read the instructions in this directory. |
| [Other agents](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md#choose-your-tool) | Use the path or file entry specified for your client. | The host can load the native Skill. File-only clients can read the supplied `SKILL.md` and references. |

## Install the local tools (optional)

- **Plugin**. Load the entire unpacked directory in a client that supports the plugin format and reopen the session. Its tool list should include `research_status` and `research_guide` among nine `research_*` tools. [Plugin installation](usage-modes.md#install-the-plugin)
- **Local MCP**. Install `requirements-mcp.txt` using Python 3.10 or newer, register the local service and connect the client. A connected client can list the nine tools. [MCP configuration](usage-modes.md#connect-mcp-separately)
- **CLI**. From the unpacked directory run `python scripts/research_workflow.py --help`. Its help lists `start`, `status` and `finish`; on macOS or Linux the interpreter may be `python3`.

Basic usage recording defaults to off for new installations. [Data settings](usage-data.md)

After installation, read the [long-report guide](conduct-research.md) or open a [complete research case](case-study/README.md).
