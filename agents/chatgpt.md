# Use with chat-based agents

[English](chatgpt.md) | [简体中文](chatgpt.zh-CN.md)

Use this guide with an agent that accepts files or pasted instructions. Native Skill and tool setup, where supported, are optional.

## Setup

Provide the repository URL or attach `SKILL.md`. If file attachments are limited, provide only `SKILL.md` first and add reference files on demand.

Starter prompt:

```text
Use the attached Research Toolkit SKILL.md and the methods relevant to this task.
Research question or revision request: [Include the audience and intended use.]
Requirements and material: [Include scope, format, sources and any existing report.]
Use the conversation and material to proceed; ask only about consequential choices you cannot resolve.
Deliver the requested research with substantive analysis and usable citations; add a short change note for revisions.
```

## Operating Notes

The agent is responsible for organizing the research, reading relevant methods, retaining full material, coordinating continuation, and completing independent review, audit and acceptance. It should carry the user's requirements into the actual report and keep execution notes outside it; the user does not need to prompt each step.

When the interface cannot save files, the agent keeps the useful working notes separate from the report and prepares a continuation summary when needed. The user may need to save or reattach that material if the host cannot carry it between conversations. For those host limitations, see [chat-only use](README.md#chat-only-use).
