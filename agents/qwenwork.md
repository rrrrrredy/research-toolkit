# QwenWork: use the complete research methods

[English](qwenwork.md) | [简体中文](qwenwork.zh-CN.md)

This card covers QwenWork (千问办公), not the general Qwen chat application.

## Install in one request

Send this to QwenWork:

```text
Install https://github.com/rrrrrredy/research-toolkit in
~/.qwenworkcn/skills/research-toolkit. Keep the complete repository,
including SKILL.md, references, scripts and examples.
On Windows, enable core.longpaths for this clone, not globally.
If that directory already exists, inspect it before changing anything.
```

QwenWork documents repository-link installation, the above user-level directory, and a `/` skill selector. [Official instructions](https://help.aliyun.com/zh/qwenwork/skills).

## Try it

```text
Use research-toolkit.
Read the installed research-toolkit/SKILL.md.
Research question: [Question, audience and intended use.]
Scope and length: [Coverage, information cutoff and expected depth.]
Existing material: [Sources, files or an existing report.]
Load the complete methods as needed and develop the evidence, comparisons,
mechanisms and synthesis. Deliver the complete report with usable citations;
preserve sources and full analysis for handoff; organize independent review, audit and acceptance through the host.
```

The [shared research guide](../docs/quickstart.md) provides a complete request and setup details.

## If it does not load

In QwenWork, send this diagnostic request:

```text
Read the supplied research-toolkit/SKILL.md and load complete methods as needed.
Research question: [Question, audience and purpose.]
Scope and depth: [Coverage, information cutoff and length requirements.]
Existing material: [Sources or an existing report.]
Develop evidence, comparisons, explanations and synthesis. Deliver the complete
report with usable citations. Identify inaccessible required material without
inventing its contents.
```

If the directory is unavailable in this client, use the [file/text input route](README.md#use-without-installation). A model’s claim that it installed a skill is insufficient; confirm the entry in the skill list and readable files.
