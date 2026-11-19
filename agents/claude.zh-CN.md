# Claude Code：使用完整研究方法

[English](claude.md) | [简体中文](claude.zh-CN.md)

## 安装

将[固定版本的精简发布包](../docs/installation-versioning.zh-CN.md#install-a-version-pinned-skill)安装到项目内的 `.claude/skills/research-toolkit`。如果目标目录已经存在，先按[更新指南](../docs/installation-versioning.zh-CN.md#保留本地修改后更新)核对并备份。

新安装默认关闭[基础使用记录](../docs/usage-data.zh-CN.md#enable-basic-recording)。仅在用户要求记录时配置项目 hooks。

需要源码副本时，从项目根目录运行以下命令。

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .claude/skills/research-toolkit
```

从此项目启动 Claude Code，调用 `/research-toolkit`。Claude 网页聊天和 Cowork 的加载规则不同，可使用[文件或文本入口](README.zh-CN.md#直接读取使用)。[官方技能要求](https://code.claude.com/docs/en/skills)。

`core.longpaths` 只对这个 Git 副本生效，避免 Windows 深层目录的路径过长错误。

## 使用

```text
使用 research-toolkit。
读取 .claude/skills/research-toolkit/SKILL.md。
研究问题：[填写问题、读者与用途。]
范围与篇幅：[填写研究范围、信息截止日和预期深度。]
已有材料：[提供来源、文件或已有报告。]
按当前工作读取完整方法，充分展开证据、比较、机制解释和综合判断。
交付完整报告与可用引用，保留来源和完整分析用于交接，由 Claude Code 完成独立审阅、审计和验收。
```

使用 Claude Code 的原生子 Agent 承担研究生产、统稿、独立内容审阅、审计和验收，沿用 Claude Code 已有模型能力，无需另配 API。共同传递当前要求和原始材料，保留完整交接成果。

[统一研究指南](../docs/quickstart.zh-CN.md)提供完整请求和接入说明。

## Agent 执行适配器

需要脚本管理执行时，使用共同的 [Agent 执行适配器](../docs/usage-modes.zh-CN.md#agent-host-execution)，指定 `--host claude`。原生子 Agent 工具也可通过同一套 work／save／review 契约工作，均沿用 Claude Code 的登录与模型配置。

共同示例说明依赖、输入更新、原始记录和独立审阅。同一研究单元使用一处调度，不同时通过原生工具和适配器重复启动。

## 无法加载时

确认 `.claude/skills/research-toolkit/SKILL.md` 和相邻的 `references/` 目录存在。文件齐全但技能未出现时，重新打开项目或会话，检查 Claude Code 的技能设置。也可给出已安装文件的准确路径，要求 Agent 直接读取。[其他输入方式](README.zh-CN.md)。
