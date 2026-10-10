# QwenWork: first Lite task

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

Select `research-toolkit` from `/`, then send the [Lite quickstart request](../docs/quickstart-lite.md). It supplies the question and sources: allow about 5–15 minutes for a 350–500 word report, source/claim records and six-item checklist. Keep outputs outside the skill folder. MCP and an external reviewer are unnecessary for Lite.

## If it does not load

In QwenWork, send this diagnostic request:

```text
Check whether research-toolkit appears in Extensions > Skills and is
enabled. Read its SKILL.md and examples/lite/sources.md from the
installed directory, and report the exact paths or the access error.
Do not reinstall or overwrite files.
```

If the directory is unavailable in this client, use the [file/text input route](README.md#use-without-installation). A model’s claim that it installed a skill is insufficient; confirm the entry in the skill list and readable files.
