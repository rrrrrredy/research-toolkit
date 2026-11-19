# Codex CLI / IDE: use the complete research methods

[English](codex.md) | [简体中文](codex.zh-CN.md)

## Install

Install the [compact, version-pinned release](../docs/installation-versioning.md#install-a-version-pinned-skill) in `.agents/skills/research-toolkit` under the project root. If the destination exists, follow the [update guide](../docs/installation-versioning.md#update-without-losing-local-work).

New installations leave [basic usage recording](../docs/usage-data.md#enable-basic-recording) off. Configure project hooks only if the user requests recording.

For a source checkout, run the following command from the project root.

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
```

Run `/skills` or type `$` and select `research-toolkit`; confirm the path ends in `.agents/skills/research-toolkit/SKILL.md`. [Official skill requirements](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

```text
Use research-toolkit.
Read .agents/skills/research-toolkit/SKILL.md.
Research question: [Question, audience and intended use.]
Scope and length: [Coverage, information cutoff and expected depth.]
Existing material: [Sources, files or an existing report.]
Load the complete methods as needed and develop the evidence, comparisons,
mechanisms and synthesis. Deliver the complete report with usable citations;
preserve sources and full analysis for handoff; organize independent review, audit and acceptance through Codex.
```

Use Codex’s native subagents for production, assembly, independent content review, audit and acceptance. They use Codex’s existing model access, without separate API configuration. Share current requirements and original materials, and retain full handoffs.

The [shared research guide](../docs/quickstart.md) provides a complete request and setup details.

## Agent execution adapter

For script-managed work, use the shared [Agent execution adapter](../docs/usage-modes.md#agent-host-execution) with `--host codex`. Native subagent tools also use the same work/save/review contracts. Both paths use Codex's login and model configuration.

The shared example describes dependencies, input updates, original records and independent review. Use one dispatcher for a work unit; do not launch it through native tools and the adapter at the same time.

## If it does not load

Check that `.agents/skills/research-toolkit/SKILL.md` and its neighboring `references/` directory exist. Reopen the project or session and check Codex's Skill settings if the files exist but the Skill is absent. You can also ask the agent to read the installed file by its exact path. [Other input methods](README.md).
