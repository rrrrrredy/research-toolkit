# Use with Claude

[English](claude.md) | [简体中文](claude.zh-CN.md)

Use this when working with Claude, Claude Code, or a Claude project.

## Setup

Attach this repository, paste the repository URL, or add `SKILL.md` to Claude's project instructions. Start with:

```text
Use https://github.com/rrrrrredy/research-toolkit as the research protocol.
Read SKILL.md and apply its research methods to this task.
Clarify missing requirements and agree on an outline before collecting sources.
Create and maintain state/, logs/, and data/ for substantial work.
```

## Operating Notes

- Use Claude projects or file attachments to keep `SKILL.md` available across turns.
- Ask Claude to write state files explicitly when the task is long.
- If Claude cannot write files, ask it to maintain the same state sections in the conversation and export them when possible.
- That conversation-only fallback does not establish durable file recovery or artifact-bound delivery verification; check the [integration guide](./README.md#chat-only-use) before relying on it for a long task.
- Load `references/writing-style.md` only when entering drafting or reader cleanup.
- Load `references/quality-gates.md` before declaring completion.
