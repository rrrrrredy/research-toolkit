# Use with chat-based agents

[English](chatgpt.md) | [简体中文](chatgpt.zh-CN.md)

Use this guide for ChatGPT, Grok bots, WorkBuddy, or another agent that accepts files or pasted instructions. Native Skill and tool setup, where supported, are optional.

## Setup

Provide the repository URL or attach `SKILL.md`. If file attachments are limited, provide only `SKILL.md` first and add reference files on demand.

Starter prompt:

```text
Use the attached Research Toolkit SKILL.md as the protocol.
Clarify missing requirements and agree on an outline before collecting sources.
If you cannot write files, maintain task_spec, progress, source registry, claim registry, uncertainty registry, and review log as clearly separated sections.
Do not expose backstage registries in the final report unless I ask for an audit appendix.
```

## Operating Notes

- State the audience, scope, evidence needs, and intended output before research starts.
- For long tasks, request section-by-section work instead of one-shot drafting.
- When the context gets long, ask the agent to summarize state in the same field names used by the framework.
- Before final delivery, ask it to use the research completion checklist and remove execution notes from the report.
- Conversation-only state is a reduced-capability fallback, not proof of durable file recovery or artifact-bound delivery checks. Use the [integration guide](./README.md#chat-only-use) to assess this boundary before starting a long task.
