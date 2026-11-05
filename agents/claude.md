# Claude Code: use the complete research methods

[English](claude.md) | [简体中文](claude.zh-CN.md)

## Install

With Git and the client ready, run from your project root. If the destination already exists, use the [update guide](../docs/installation-versioning.md).

The agent runs the complete installation below with an available Python 3.10+ interpreter. Usage recording is included by default; users do not install a second component. It sends basic operation events, excludes conversations and reports, and can be disabled. On first use of an existing Skill installation, complete the [recording setup](../docs/usage-data.md#automatic-setup-by-the-agent).

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .claude/skills/research-toolkit
python .claude/skills/research-toolkit/scripts/install_usage.py --host claude --project . --channel github-clone --form skill
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

Run this from the same project directory:

```bash
git -C .claude/skills/research-toolkit status --short
```

No output means the checkout is clean; a path error means the command is running from the wrong directory or the clone failed. Changes may indicate missing or edited files—preserve your edits before updating. If files exist but the skill is absent, reopen the project/session and check Claude Code’s skill settings. You can also ask the agent to read the installed `SKILL.md` by its exact path. [All input methods and limits](README.md).
