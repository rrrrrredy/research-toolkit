# Codex CLI / IDE: first Lite task

[English](codex.md) | [简体中文](codex.zh-CN.md)

## Install

With Git and the client ready, run from your project root. If the destination already exists, use the [update guide](../docs/installation-versioning.md).

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
```

Run `/skills` or type `$` and select `research-toolkit`; confirm the path ends in `.agents/skills/research-toolkit/SKILL.md`. [Official skill requirements](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

`core.longpaths` applies to this Git checkout and prevents long-path checkout failures on Windows.

## Try it

Send this request after selecting the skill:

```text
Use research-toolkit with profile=lite.
Read .agents/skills/research-toolkit/SKILL.md.
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
git -C .agents/skills/research-toolkit status --short
```

No output means the checkout is clean; a path error means the command is running from the wrong directory or the clone failed. Changes may indicate missing or edited files—preserve your edits before updating. If files exist but the skill is absent, reopen the project/session and check the host’s skill settings. You can also ask the agent to read the installed `SKILL.md` by its exact path. [All input methods and limits](README.md).
