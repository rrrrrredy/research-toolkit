# Grok Bot: first Lite task

[English](grok-bot.md) | [简体中文](grok-bot.zh-CN.md)

Use a private Grok Bot conversation for the [Lite quickstart request](../docs/quickstart-lite.md). The request contains the repository URL, `SKILL.md` entry, complete brief and two fictional sources. If the Bot cannot open repository files, provide their text and the required references through the [general input guide](README.md#use-without-installation).

Expect a 350–500 word report, separate source/claim records and six-item checklist in about 5–15 minutes with the Bot ready. Save or export all three parts if files do not persist. There is no independent review in Lite.

## Check access before the task

Send:

```text
Read SKILL.md, examples/lite/start.en.json and examples/lite/sources.md
from the research-toolkit repository I provided. Identify the brief's
word limit and the two source titles. If any file is inaccessible,
name it and stop before making up its contents.
```

## Reuse the method

After a successful task, ask the Bot to save the research method as a private skill called `research-toolkit`, preserving the reference materials and the Lite/Full distinction. Recheck file access when reusing it.

The [official Grok Bot guide](https://docs.x.ai/grok-bot/skills-routines-and-automations) documents saved skills and the desktop `/` selector. It does not establish that a raw Git clone into another tool's skill directory registers a Grok Bot skill. If a saved skill is missing, check **Marketplace → Your plugins → Manage plugins and skills → Private skills**.
