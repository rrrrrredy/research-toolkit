# Kimi Code CLI: use the complete research methods

[English](kimi-code.md) | [简体中文](kimi-code.zh-CN.md)

## Install

With Git and the client ready, run from your project root. If the destination already exists, use the [update guide](../docs/installation-versioning.md).

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
```

Start a new Kimi Code session from the project Git root and invoke `/skill:research-toolkit`. [Official skill requirements](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html).

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
preserve sources and full analysis for handoff; organize independent review, audit and acceptance through the host.
```

The [shared research guide](../docs/quickstart.md) provides a complete request and setup details.

## If it does not load

Run this from the same project directory:

```bash
git -C .agents/skills/research-toolkit status --short
```

No output means the checkout is clean; a path error means the command is running from the wrong directory or the clone failed. Changes may indicate missing or edited files—preserve your edits before updating. If files exist but the skill is absent, reopen the project/session and check the host’s skill settings. You can also ask the agent to read the installed `SKILL.md` by its exact path. [All input methods and limits](README.md).
