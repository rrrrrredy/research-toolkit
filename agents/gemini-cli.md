# Gemini CLI: first Lite task

[English](gemini-cli.md) | [简体中文](gemini-cli.zh-CN.md)

## Install

With Git and the client ready, run from your project root. If the destination already exists, use the [update guide](../docs/installation-versioning.md).

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .gemini/skills/research-toolkit
```

Start Gemini CLI in this project and ask it to activate `research-toolkit`. Review the host’s activation consent when prompted. [Official skill requirements](https://geminicli.com/docs/cli/using-agent-skills/).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

Send this request after selecting the skill:

```text
Use research-toolkit with profile=lite.
Read .gemini/skills/research-toolkit/SKILL.md.
Within that same toolkit, read examples/lite/start.en.json and
examples/lite/sources.md.
Complete that fictional helpdesk comparison. Return the short report,
separate sources/claims records and all six Lite checklist items.
Keep outputs outside the installed toolkit. Disclose the fictional
evidence and absence of independent review.
```

Expect a 350–500 word report plus records and checklist in about 5–15 minutes with your agent ready. MCP and a reviewer backend are optional. [Full walkthrough](../docs/quickstart-lite.md).

## If it does not load

Run this from the same project directory:

```bash
gemini skills list
```

The list should include `research-toolkit`. If absent, use `/skills reload` in the project session and check that the skill is enabled. You can also ask the agent to read the installed `SKILL.md` by its exact path. [All input methods and limits](README.md).
