# Gemini CLI: use the complete research methods

[English](gemini-cli.md) | [简体中文](gemini-cli.zh-CN.md)

## Install

With Git and the client ready, run from your project root. If the destination already exists, use the [update guide](../docs/installation-versioning.md).

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .gemini/skills/research-toolkit
```

Start Gemini CLI in this project and ask it to activate `research-toolkit`. Review the host’s activation consent when prompted. [Official skill requirements](https://geminicli.com/docs/cli/using-agent-skills/).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

```text
Use research-toolkit.
Read .gemini/skills/research-toolkit/SKILL.md.
Research question: [Question, audience and intended use.]
Scope and length: [Coverage, information cutoff and expected depth.]
Existing material: [Sources, files or an existing report.]
Load the complete methods as needed and develop the evidence, comparisons,
mechanisms and synthesis. Deliver the complete report with usable citations;
maintain the working records yourself.
```

The [shared research guide](../docs/quickstart.md) provides a complete request and setup details.

## If it does not load

Run this from the same project directory:

```bash
gemini skills list
```

The list should include `research-toolkit`. If absent, use `/skills reload` in the project session and check that the skill is enabled. You can also ask the agent to read the installed `SKILL.md` by its exact path. [All input methods and limits](README.md).
