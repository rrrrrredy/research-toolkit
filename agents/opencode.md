# OpenCode: use the complete research methods

[English](opencode.md) | [简体中文](opencode.zh-CN.md)

<!-- hosts:start -->
**Entry**　Native project Skill, with skill permission enabled.  Bundled dispatch driver: `opencode`.  [Host capabilities](README.md#capabilities)
<!-- hosts:end -->

## Install

Install the [compact, version-pinned release](../docs/installation-versioning.md#install-a-version-pinned-skill) in `.opencode/skills/research-toolkit` under the project root. If the destination exists, follow the [update guide](../docs/installation-versioning.md#update-without-losing-local-work).

New installations leave [basic usage recording](../docs/usage-data.md#enable-basic-recording) off. Configure project hooks only if the user requests recording.

For a source checkout, run the following command from the project root.

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .opencode/skills/research-toolkit
```

Start OpenCode in this project and ask it to load the `research-toolkit` skill. Skill discovery must be enabled and its permission must not be `deny`. This directory works with the documented [V2 skill layout](https://opencode.ai/v2/docs/skills) too. [Official skill requirements](https://opencode.ai/docs/skills).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

```text
Use research-toolkit.
Read .opencode/skills/research-toolkit/SKILL.md.
Research question: [Question, audience and intended use.]
Scope and length: [Coverage, information cutoff and expected depth.]
Existing material: [Sources, files or an existing report.]
Load the complete methods as needed and develop the evidence, comparisons,
mechanisms and synthesis. Deliver the complete report with usable citations;
preserve sources and full analysis for handoff; organize independent review, audit and acceptance through OpenCode.
```

The [shared research guide](../docs/conduct-research.md) provides a complete request and setup details.

## Agent execution adapter

For script-managed work, use the shared [Agent execution adapter](../docs/usage-modes.md#agent-host-execution) with `--host opencode`. Native subagent tools also use the same work/save/review contracts. Both paths use OpenCode's login and model configuration.

The shared example describes dependencies, input updates, original records and independent review. Use one dispatcher for a work unit; do not launch it through native tools and the adapter at the same time.

## If it does not load

Check that `.opencode/skills/research-toolkit/SKILL.md` and its neighboring `references/` directory exist. Reopen the project or session and check OpenCode's Skill settings if the files exist but the Skill is absent. You can also ask the agent to read the installed file by its exact path. [Other input methods](README.md).
