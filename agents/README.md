# Use with your agent

[English](README.md) | [简体中文](README.zh-CN.md)

Provide the research methods to your agent through a repository link, files, attachments, or pasted text. Choose the input method your interface supports.

The [entry instructions](../SKILL.md) and [Chinese reading version](../SKILL.zh-CN.md) point to the methods for each research stage. Native Skill installation is optional. For callable workflow tools, see [plugin and MCP configuration](../docs/usage-modes.md).

**First task:** copy the [5–15 minute Lite request](../docs/quickstart-lite.md). It includes a question and two fictional sources. You get a short report, separate source/claim records and a final checklist; no MCP or reviewer backend is needed.

## Use without installation

| Available input | Method |
| --- | --- |
| Repository access | Send the [repository URL](https://github.com/rrrrrredy/research-toolkit) and ask the agent to read `SKILL.md` and the required files under `references/`. |
| Local files or attachments | [Download the repository](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip). Make `SKILL.md` and the reference files available to the session. If attachment limits apply, provide the entry file and add the required methods by stage. |
| Pasted text | Paste the full entry instructions and the reference sections needed for the task. A URL alone is insufficient when the agent cannot open it. |

Use the [copyable research request](../README.md#usage) with your research question, intended use, and desired output. For a file or text input, replace the repository-reading instruction with the attached files or pasted instructions you supplied.

These methods apply instructions to the task. They do not register a native Skill, start MCP, provide web access, or execute model reviews.

## Chat-only use

An interface without file persistence or command execution can still use the research and writing methods. Keep source, claim, uncertainty, and review records separate from the report; save or export them when continuing in another session.

Lite keeps the brief, sources, claims, section drafting and final checklist without commissioning a review. For Full, follow the selected review tier. An independent review requires a separate reviewer with the full brief, report, and supporting evidence. Use another session or a reviewer you can access and return its substantive findings to the author. Do not treat the author's self-check as an independent review. If the interface cannot run file-based checks or preserve task files, those capabilities remain unavailable; chat notes do not establish persistent recovery or verified delivery.

## Install for repeated use

Follow the guide for your tool to choose its Skill directory or other supported loading method. A native installation should appear under the name `research-toolkit` in that tool's Skill list. A download into an arbitrary folder still needs an explicit instruction to read it.

Use a complete repository checkout for local installation so that references, helper scripts, and documentation remain together. Keep research outputs in a separate task folder.

## Choose your tool

Choose the client you actually use; a model name alone does not determine Skill support. Native guides cite the host's official directory and invocation requirements. File/text guides apply instructions without registering a Skill.

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
| Doubao Work (豆包工作) | Conditional file/text route; native import requirements unverified | [Input requirements and limits](doubao-work.md) |
| OpenClaw | Skill directory or direct file reading | [Existing setup guide](openclaw.md) |
| Hermes Agent | Skill directory and invocation | [Existing setup guide](hermes.md) |
| ChatGPT / other chat agents | Files, attachments or pasted instructions | [General input guide](chatgpt.md) |
| DeepSeek Harness (optional) | Native Skill and optional adapter | [Existing setup guide](deepseek-harness.md) |

Host documentation establishes an installation route, not a completed research run on every client. Confirm the actual loaded path and readable example files using the card's troubleshooting step. Availability depends on your client version, account and permissions; the [file/text route](#use-without-installation) remains available wherever the session can read the supplied material.

For an unlisted agent, check its official `SKILL.md` support first. Use its documented Skill directory if supported; otherwise provide the files or text explicitly. Neither route adds web search, persistent storage or command execution to the host.

These are setup instructions. Installation and loading checks establish which files are available; research quality is assessed through the [evaluation materials](../evals/README.md) and content reviews.

## Files to keep

The full checkout contains these parts:

| Part | Purpose |
| --- | --- |
| `SKILL.md` and `SKILL.zh-CN.md` | Authoritative agent entry point and Chinese reading version |
| `references/` | Research, analysis, review, and writing methods loaded as needed |
| `scripts/` | Checking helpers; `check_delivery.py` imports `check_review_completion.py`, so keep them together |
| `docs/` | Instructions for the helpers and their task records, including `delivery-verification.md` and `review-completion.md` |

Keep the file named `SKILL.md` as the discovery entry point; the Chinese companion provides a reading option. The checks require Python. Web search, file access, and execution permissions come from the agent environment.

## Confirm the intended copy is in use

1. For native installation, check that `research-toolkit` appears in the tool's Skill list and select it as described in its guide. For direct use, identify the local path or attached files explicitly.
2. Confirm that the agent can read the full `SKILL.md` and the reference files needed for the task. If multiple copies exist, confirm the actual path used.
3. Keep `state/`, `logs/`, `data/`, drafts, and reports in the research task folder. Confirm the session can save and reopen them.
4. Use [installation comparison](../docs/installation-versioning.md) when you need to check the installed files against a specific repository commit. File identity alone does not establish that the tool loaded that copy.

If the interface cannot retain files across conversations, save or export the task records and provide them again when continuing. If a required delivery check cannot run, follow the stage-delivery rules in `SKILL.md` and state which checks remain incomplete.

## Update an installed copy

Follow [installation identity and updates](../docs/installation-versioning.md) to compare versions and preserve local changes before updating. After an update, confirm the intended Skill is available again and that its references and scripts are still present. Follow the tool's reload instructions if the updated copy does not appear.

All usage methods share the same requirements: clarify the research brief, preserve progress, assess sources as evidence, keep review records outside the finished prose, and complete the selected profile’s checks before claiming final delivery (the final checklist for Lite; the declared reviews and delivery checks for Full). Source-embedded requests to control the agent are treated as source content, not task instructions.
