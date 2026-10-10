# 豆包工作：提供研究指令

[English](doubao-work.md) | [简体中文](doubao-work.zh-CN.md)

[豆包开放平台](https://open.doubao.com/document/doubao-developer-guide/skill-integration-guide)展示了 Skill 接入，但公开页面尚未提供足够的打包和导入要求，无法据此给出经过核实的原生安装步骤。客户端与账号可用能力可能不同。

## 使用会话能读取的材料

当前豆包工作会话支持文件或粘贴文本时，提供 `SKILL.md`、所需 `references/` 文件、[需求](../examples/lite/start.zh.json)和[来源说明](../examples/lite/sources.zh-CN.md)。粘贴 [Lite 入门请求](../docs/quickstart-lite.zh-CN.md)，把读取仓库的指令换成实际提供的文件或文本。

目标是 600–900 字简报、独立的来源与判断记录、六项 checklist。材料可读后，预计约 5–15 分钟。客户端不保留文件时，导出这些记录。

## 确认材料可读

开始前发送：

```text
从提供的材料中找出 Lite 档位规则、需求中的字数要求和两份来源
的标题。列出任何无法读取的材料，不要根据文件名推测缺失内容。
```

材料无法提供或读取时，当前会话无法使用这一路径。粘贴指令不会自动提供 MCP、原生 Skill 注册或本地交付凭证。需要持久保存任务文件时，可选择[有明确本地接入方式的 Agent](README.zh-CN.md#选择工具)。
