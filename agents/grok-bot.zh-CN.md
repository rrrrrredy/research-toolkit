# Grok Bot：第一个 Lite 任务

[English](grok-bot.md) | [简体中文](grok-bot.zh-CN.md)

在 Grok Bot 私人会话中发送 [Lite 入门请求](../docs/quickstart-lite.zh-CN.md)。请求含仓库链接、`SKILL.md` 入口、完整需求和两份虚构来源。Bot 无法打开仓库文件时，按[通用输入指南](README.zh-CN.md#直接读取使用)提供原文及所需参考资料。

Bot 已就绪时，预计约 5–15 分钟产出 600–900 字简报、独立的来源与判断记录、六项 checklist。文件不能持久保存时，保存或导出这三部分。Lite 没有独立评审。

## 开始前确认文件可读

发送：

```text
读取我提供的 research-toolkit 仓库中的 SKILL.md、
examples/lite/start.zh.json 和 examples/lite/sources.zh-CN.md。
列出需求中的字数要求和两份来源的标题。
任何文件无法访问时，指出文件名，不编造内容。
```

## 重复使用

完成一次任务后，可让 Bot 将研究方法保存为名为 `research-toolkit` 的私人技能，保留参考材料及 Lite/Full 的区别。再次使用时确认所需文件仍可读。

[Grok Bot 官方指南](https://docs.x.ai/grok-bot/skills-routines-and-automations)说明了保存技能和桌面端 `/` 选择器；并未说明克隆到其他工具的技能目录就能注册为 Grok Bot 技能。已保存技能未出现时，检查“Marketplace → Your plugins → Manage plugins and skills → Private skills”。
