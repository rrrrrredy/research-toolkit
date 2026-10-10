# Gemini CLI：第一个 Lite 任务

[English](gemini-cli.md) | [简体中文](gemini-cli.zh-CN.md)

## 安装

Git 和客户端已就绪时，从项目根目录执行。目标目录已存在时，使用[更新指南](../docs/installation-versioning.zh-CN.md)。

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .gemini/skills/research-toolkit
```

从此项目启动 Gemini CLI，要求启用 `research-toolkit`，出现宿主授权提示时按提示确认。[官方技能要求](https://geminicli.com/docs/cli/using-agent-skills/)。

`core.longpaths` 只对这个 Git 副本生效，避免 Windows 深层目录的路径过长错误。

## 使用

选中技能后发送：

```text
使用 research-toolkit，选择 profile=lite。
读取 .gemini/skills/research-toolkit/SKILL.md。
读取同一工具箱里的 examples/lite/start.zh.json 和
examples/lite/sources.zh-CN.md，完成这个虚构客服工具比较。
分别交付短报告、sources/claims 记录和完整的六项 Lite checklist。
成果放在工具箱安装目录之外，披露材料虚构且未进行独立评审。
```

Agent 已就绪时，预计约 5–15 分钟产出 600–900 字简报、记录和 checklist。MCP 与评审后端均可不配置。[完整入门](../docs/quickstart-lite.zh-CN.md)。

## 无法加载时

在同一项目目录执行：

```bash
gemini skills list
```

列表应包含 `research-toolkit`；若没有，在项目会话中使用 `/skills reload`，并检查技能是否启用。也可给出已安装 `SKILL.md` 的准确路径，要求 Agent 直接读取。[其他输入方式与边界](README.zh-CN.md)。
