# Claude 接入

[English](claude.md) | [简体中文](claude.zh-CN.md)

适用于 Claude、Claude Code 或 Claude 项目。

## 使用方式

附上仓库、粘贴仓库链接，或将 `SKILL.md` 加入项目指令：

```text
使用 https://github.com/rrrrrredy/research-toolkit 作为研究规范。
先读 SKILL.md。关键需求缺失时，在收集资料前集中澄清。
实质性任务创建并维护 state/、logs/、data/。
```

## 执行要点

通过项目或附件让主指令持续可用，长任务明确要求保存状态文件。不能写文件时在对话里分区记录并尽可能导出；这不能证明持久恢复或文件绑定的交付检查，见[纯聊天使用边界](README.zh-CN.md#只能在聊天中使用时)。

先明确范围、读者、深度、证据标准和提纲，再收集、分析、分节写作。写作或读者润色时读[写作风格](../references/writing-style.zh-CN.md)，宣布完成前读[质量关卡](../references/quality-gates.zh-CN.md)。
