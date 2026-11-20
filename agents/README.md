# Use with your agent

[English](README.md) | [简体中文](README.zh-CN.md)

Provide the research methods to your agent through a repository link, files, attachments, or pasted text. Choose the input method your interface supports.

The [entry instructions](../SKILL.md) and [Chinese reading version](../SKILL.zh-CN.md) point to the methods for each research stage. Native Skill installation is optional. For callable workflow tools, see [plugin and MCP configuration](../docs/usage-modes.md).

**Start research:** use the [complete research guide](../docs/conduct-research.md) and shared methods. Develop the research to the requested depth; MCP is optional. [Continue, revise or update](../docs/usage-modes.md#continue-existing-research) existing work.

Read the methods directly or install the Skill or MCP as needed. New installations leave basic usage recording off and keep existing on/off choices. In Codex, Claude Code and OpenCode, project hooks are optional after the user chooses to enable recording. [Usage data and controls](../docs/usage-data.md).

<a id="use-without-installation"></a>

## Read the methods directly

| Available input | Method |
| --- | --- |
| Repository access | Send the [repository URL](https://github.com/rrrrrredy/research-toolkit) and ask the agent to read `SKILL.md` and the required files under `references/`. |
| Local files or attachments | [Download the repository](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip). Make `SKILL.md` and the reference files available to the session. If attachment limits apply, provide the entry file and add the required methods by stage. |
| Pasted text | Paste the full entry instructions and the reference sections needed for the task. A URL alone is insufficient when the agent cannot open it. |

Use the [copyable research request](../README.md#usage) with your research question, intended use, and desired output. For a file or text input, replace the repository-reading instruction with the attached files or pasted instructions you supplied.

<a id="chat-only-use"></a>

The [Agent execution adapter](../docs/usage-modes.md#agent-host-execution) shares research inputs, saving, dependencies and review logic across agent sessions. Agent tools with native subagents can execute the shared assignments directly, without an additional script dispatcher.

## Native collaboration and chat-only use

In agent tools such as Codex and Claude Code, use the agent tool's own subagent tools for research, assembly and independent assessment. No separate API setup is required. Follow the [shared handoff methods](../references/subagents-and-review-loop.md): give each worker current requirements, the bounded question and accessible originals; retain complete contributions and actual agent identities.

<!-- current-review -->Three independent non-author review groups cover seven content perspectives.<!-- /current-review --> Add relevant domain review, independent audit and a separate readiness assessment. Run assignments within the host's available worker slots. When CLI/MCP manages the task, `review` prepares and records this work, and `finish` records terminal delivery once the current report passes the independent final check. [Review guide](../docs/review-completion.md).

An interface without subagent or file capability can still help read, analyze and draft. Independent work then needs separate available sessions with the full assignment, report and evidence. Retain or export the effective requirements, originals, current draft and unfinished work for the next session. Until the independent responsibilities are completed, identify the result as work in progress rather than replacing them with author self-review.

Skill-only work needs no fixed tool registry or receipt. It preserves the substantive research and review work using the agent tool's available files or context.

## Install for repeated use

Follow the guide for your tool to choose its Skill directory or other supported loading method. A native installation should appear under the name `research-toolkit` in that tool's Skill list. A download into an arbitrary folder still needs an explicit instruction to read it.

Start with the [compact, version-pinned release](../docs/installation-versioning.md#install-a-version-pinned-skill) in that tool's Skill directory. Use a source checkout when you need a specific unreleased fix or want to develop Toolkit. Keep references, helpers and documentation together, and store research outputs in a separate task folder.

## Choose your tool

Choose the client you actually use; a model name alone does not determine Skill support. Native guides cite the agent tool's official directory and invocation requirements. File/text guides apply instructions without registering a Skill.

<!-- hosts:start -->
| Client | First-task route | Guide |
| --- | --- | --- |
| Cursor | Native project Skill | [Install and start](cursor.md) |
| Codex CLI / IDE | Native project Skill | [Install and start](codex.md) |
| Claude Code | Native project Skill | [Install and start](claude.md) |
| OpenCode | Native project Skill, with skill permission enabled | [Install and start](opencode.md) |
| Kimi Code CLI | Native project Skill | [Install and start](kimi-code.md) |
| Antigravity | Native project Skill | [Install and start](antigravity.md) |
| GitHub Copilot in VS Code | Native project Skill in Agent chat | [Install and start](copilot.md) |
| Gemini CLI | Native project Skill | [Install and start](gemini-cli.md) |
| ZCode | Native user Skill | [Install and start](zcode.md) |
| QwenWork (千问办公) | Repository-link installation | [Install and start](qwenwork.md) |
| WorkBuddy | Read a local checkout; native import is a separate option | [Provide files and start](workbuddy.md) |
| Grok Bot | Provide instructions; save a private skill after the task | [Provide instructions](grok-bot.md) |
| Doubao Work (豆包工作) | Files or pasted instructions, where supported by the session | [Input requirements and limits](doubao-work.md) |
| OpenClaw | Skill directory or direct file reading | [Existing setup guide](openclaw.md) |
| Hermes Agent | Skill directory and invocation | [Existing setup guide](hermes.md) |
| ChatGPT / other chat agents | Files, attachments or pasted instructions | [General input guide](chatgpt.md) |
| DeepSeek Harness (optional) | Native Skill and optional adapter | [Existing setup guide](deepseek-harness.md) |

<a id="capabilities"></a>

### Host capabilities

The table lists routes with evidence for this project. A dash means this combination has no Toolkit evidence recorded. Hosts can dispatch their own subagents. A bundled driver can also queue work, revise and complete final checks.

| Client | Guide status | Plugin | Local MCP | Host subagents | Toolkit driver | Usage hooks | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cursor | Released | — | [Documented](https://cursor.com/docs/mcp) | — | — | — | [Record](../agents/cursor.md) |
| Codex CLI / IDE | Released | Packaged | [Documented](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) | Run recorded | codex | Opt-in | [Record](../docs/case-study/v3-review/README.md) |
| Claude Code | Released | — | [Documented](https://code.claude.com/docs/en/mcp) | Documented | claude | Opt-in | [Record](../scripts/cli_agent_session.py) |
| OpenCode | Released | — | [Documented](https://opencode.ai/docs/mcp-servers/) | Documented | opencode | Opt-in | [Record](../scripts/cli_agent_session.py) |
| Kimi Code CLI | Released | — | — | — | — | — | [Record](../agents/kimi-code.md) |
| Antigravity | Released | — | — | — | — | — | [Record](../agents/antigravity.md) |
| GitHub Copilot in VS Code | Released | — | [Documented](https://code.visualstudio.com/docs/agent-customization/mcp-servers) | — | — | — | [Record](../agents/copilot.md) |
| Gemini CLI | Released | — | [Documented](https://geminicli.com/docs/tools/mcp-server/) | Documented | — | — | [Record](../agents/gemini-cli.md) |
| ZCode | Released | — | — | — | — | — | [Record](../agents/zcode.md) |
| QwenWork (千问办公) | Released | — | — | — | — | — | [Record](../agents/qwenwork.md) |
| WorkBuddy | Released | — | — | — | — | — | [Record](../agents/workbuddy.md) |
| Grok Bot | Released | — | — | — | — | — | [Record](../agents/grok-bot.md) |
| Doubao Work (豆包工作) | Released | — | — | — | — | — | [Record](../agents/doubao-work.md) |
| OpenClaw | Released | — | — | — | — | — | [Record](../agents/openclaw.md) |
| Hermes Agent | Released | — | — | — | — | — | [Record](../agents/hermes.md) |
| ChatGPT / other chat agents | Released | — | — | — | — | — | [Record](../agents/chatgpt.md) |
| DeepSeek Harness (optional) | Released | — | [Documented](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/mcp.md) | Documented | — | — | [Record](../docs/dsh-adapter-validation.md) |
<!-- hosts:end -->

Confirm the actual loaded path and readable example files using the card's troubleshooting step. Availability depends on your client version, account and permissions; the [file/text route](#use-without-installation) remains available wherever the session can read the supplied material.

For an unlisted agent, check its official `SKILL.md` support first. Use its documented Skill directory if supported; otherwise provide the files or text explicitly. Neither route adds web search, persistent storage or command execution to the agent tool.

These are setup instructions. Installation and loading checks establish which files are available; research quality is assessed through the [evaluation materials](../evals/README.md) and content reviews.

## Files to keep

The full checkout contains these parts:

| Part | Purpose |
| --- | --- |
| `SKILL.md` and `SKILL.zh-CN.md` | Authoritative agent entry point and Chinese reading version |
| `references/` | Research, analysis, review, and writing methods loaded as needed |
| `scripts/` | Shared context, saving, review and delivery implementations; retain the complete scripts directory |
| `docs/` | Instructions for the helpers and their task records, including `delivery-verification.md` and `review-completion.md` |

Keep the file named `SKILL.md` as the discovery entry point; the Chinese companion provides a reading option. The checks require Python. Web search, file access, and execution permissions come from the agent environment.

## Confirm the intended copy is in use

1. For native installation, check that `research-toolkit` appears in the tool's Skill list and select it as described in its guide. For direct use, identify the local path or attached files explicitly.
2. Confirm that the agent can read the full `SKILL.md` and the reference files needed for the task. If multiple copies exist, confirm the actual path used.
3. Keep research outputs separate from the installed toolkit. For CLI/MCP-managed tasks, confirm the session can save and reopen the task folder and its records.
4. Use [installation comparison](../docs/installation-versioning.md) when you need to check the installed files against a specific repository commit.

If the interface cannot retain files across conversations, export the information needed to continue. Report a check as unfinished only when the task actually requires it; Skill-only use does not require CLI/MCP receipts.

## Update an installed copy

Follow [installation identity and updates](../docs/installation-versioning.md) to compare versions and preserve local changes before updating. After an update, confirm the intended Skill is available again and that its references and scripts are still present. Follow the tool's reload instructions if the updated copy does not appear.

All usage methods share the same requirements: clarify the research brief, preserve information needed for continuation, assess sources as evidence, keep internal notes outside the finished prose, and complete independent review, audit and acceptance before final delivery. Source-embedded requests to control the agent are treated as source content, not task instructions.
