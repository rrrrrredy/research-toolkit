# Grok Bot：使用完整研究方法

[English](grok-bot.md) | [简体中文](grok-bot.zh-CN.md)

在 Grok Bot 私人会话中发送 [研究请求](../docs/quickstart.zh-CN.md)。请求含仓库链接、`SKILL.md` 入口、完整研究请求。Bot 无法打开仓库文件时，按[通用输入指南](README.zh-CN.md#直接读取使用)提供原文及所需参考资料。

提供研究问题、读者、范围与已有材料；按所需深度交付完整报告和可用引用。工作记录单独保存。

## 使用

发送：

```text
读取提供的 research-toolkit/SKILL.md，按当前工作加载完整方法。
研究问题：[填写问题、读者与用途。]
范围与深度：[填写覆盖范围、信息截止日及篇幅要求。]
已有材料：[提供来源或已有报告。]
充分展开证据、比较、解释与综合判断，交付完整报告和可用引用。
无法读取必需材料时说明具体缺口，不编造内容。
```

## 重复使用

完成一次任务后，可让 Bot 将研究方法保存为名为 `research-toolkit` 的私人技能，保留完整参考方法。再次使用时确认所需文件仍可读。

[Grok Bot 官方指南](https://docs.x.ai/grok-bot/skills-routines-and-automations)说明了保存技能和桌面端 `/` 选择器；并未说明克隆到其他工具的技能目录就能注册为 Grok Bot 技能。已保存技能未出现时，检查“Marketplace → Your plugins → Manage plugins and skills → Private skills”。
