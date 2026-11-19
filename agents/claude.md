# Claude Code: use the complete research methods

[English](claude.md) | [简体中文](claude.zh-CN.md)

## Install

Install the [compact, version-pinned release](../docs/installation-versioning.md#install-a-version-pinned-skill) in `.claude/skills/research-toolkit` under the project root. If the destination exists, follow the [update guide](../docs/installation-versioning.md#update-without-losing-local-work).

New installations leave [basic usage recording](../docs/usage-data.md#enable-basic-recording) off. Configure project hooks only if the user requests recording.

For a source checkout, run the following command from the project root.

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .claude/skills/research-toolkit
```

Start Claude Code in this project and invoke `/research-toolkit`. Claude web chat and Cowork have different loading rules; use the [file/text route](README.md#use-without-installation) there. [Official skill requirements](https://code.claude.com/docs/en/skills).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

```text
Use research-toolkit.
Read .claude/skills/research-toolkit/SKILL.md.
Research question: [Question, audience and intended use.]
Scope and length: [Coverage, information cutoff and expected depth.]
Existing material: [Sources, files or an existing report.]
Load the complete methods as needed and develop the evidence, comparisons,
mechanisms and synthesis. Deliver the complete report with usable citations;
preserve sources and full analysis for handoff; organize independent review, audit and acceptance through Claude Code.
```

Use Claude Code’s native subagents for production, assembly, independent content review, audit and acceptance. They use Claude Code’s existing model access, without separate API configuration. Share current requirements and original materials, and retain full handoffs.

The [shared research guide](../docs/quickstart.md) provides a complete request and setup details.

## Agent execution adapter

For script-managed work, use the shared [Agent execution adapter](../docs/usage-modes.md#agent-host-execution) with `--host claude`. Native subagent tools also use the same work/save/review contracts. Both paths use Claude Code's login and model configuration.

The shared example describes dependencies, input updates, original records and independent review. Use one dispatcher for a work unit; do not launch it through native tools and the adapter at the same time.

## If it does not load

Check that `.claude/skills/research-toolkit/SKILL.md` and its neighboring `references/` directory exist. Reopen the project or session and check Claude Code's Skill settings if the files exist but the Skill is absent. You can also ask the agent to read the installed file by its exact path. [Other input methods](README.md).
