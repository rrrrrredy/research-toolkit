# 千问办公：使用完整研究方法

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

```text
使用 research-toolkit。
读取已安装的 research-toolkit/SKILL.md。
研究问题：[填写问题、读者与用途。]
范围与篇幅：[填写研究范围、信息截止日和预期深度。]
已有材料：[提供来源、文件或已有报告。]
按当前工作读取完整方法，充分展开证据、比较、机制解释和综合判断。
交付完整报告与可用引用，由你维护工作记录。
```

[统一研究指南](../docs/quickstart.zh-CN.md)提供完整请求和接入说明。

## 无法加载时

在千问办公中发送这条排查请求：

```text
读取提供的 research-toolkit/SKILL.md，按当前工作加载完整方法。
研究问题：[填写问题、读者与用途。]
范围与深度：[填写覆盖范围、信息截止日及篇幅要求。]
已有材料：[提供来源或已有报告。]
充分展开证据、比较、解释与综合判断，交付完整报告和可用引用。
无法读取必需材料时说明具体缺口，不编造内容。
```

当前客户端无法访问目录时，使用[文件或文本入口](README.zh-CN.md#直接读取使用)。模型声称安装成功还不够，应确认技能列表中存在入口，且实际文件可读。
