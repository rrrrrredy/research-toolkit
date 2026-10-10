# 千问办公：第一个 Lite 任务

[English](qwenwork.md) | [简体中文](qwenwork.zh-CN.md)

本卡适用于 QwenWork（千问办公），不等同于通用千问聊天应用。

## 一句话安装

在千问办公中发送：

```text
将 https://github.com/rrrrrredy/research-toolkit 安装到
~/.qwenworkcn/skills/research-toolkit，保留完整仓库，
包括 SKILL.md、references、scripts 和 examples。
Windows 克隆时仅为此副本启用 core.longpaths，不改全局设置。
目录已存在时先检查，不直接覆盖。
```

千问办公官方说明支持通过仓库链接安装、使用上述用户级目录，并通过 `/` 选择技能。[官方说明](https://help.aliyun.com/zh/qwenwork/skills)。

## 使用

从 `/` 中选择 `research-toolkit`，发送 [Lite 入门请求](../docs/quickstart-lite.zh-CN.md)。题目和来源已备好，预计约 5–15 分钟产出 600–900 字简报、来源与判断记录、六项 checklist。成果放在技能目录之外。Lite 无需 MCP 或外部评审。

## 无法加载时

在千问办公中发送这条排查请求：

```text
检查“扩展 → 技能”里是否有 research-toolkit，是否启用。
从安装目录读取它的 SKILL.md 和 examples/lite/sources.zh-CN.md，
报告准确路径或访问错误。不要重新安装或覆盖文件。
```

当前客户端无法访问目录时，使用[文件或文本入口](README.zh-CN.md#直接读取使用)。模型声称安装成功还不够，应确认技能列表中存在入口，且实际文件可读。
