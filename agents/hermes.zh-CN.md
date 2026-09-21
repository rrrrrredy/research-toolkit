# Hermes Agent 接入

[English](hermes.md) | [简体中文](hermes.zh-CN.md)

适用于 Hermes CLI、TUI、桌面应用或消息网关。依据官方[技能说明](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)、[技能目录](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)与[迁移说明](https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw)。

## 安装与发现

技能是按需加载的知识文档。默认配置放在 `~/.hermes/skills/`，自定义配置使用自身 `HERMES_HOME/skills/`。

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git ~/.hermes/skills/research-toolkit
hermes
/skills
```

按安装名称调用，或说明：

```text
本次研究使用 research-toolkit 技能。
先读 SKILL.md，按阶段需要读取 references。
研究状态保存在项目工作区。
```

## 从 OpenClaw 迁移

```bash
hermes claw migrate --dry-run
hermes claw migrate
```

先预览再迁移，随后检查实际导入路径及 `SKILL.md`、`references/` 是否齐全。嵌套导入路径可直接使用，也可重新克隆到默认技能目录。

## 执行要点

保持为指令包，不改成插件或核心工具。用 `/skills` 查看并按名称调用。模型和工具按 `hermes model`、`hermes tools` 配置，工具箱不依赖特定供应商。

状态、日志、数据、草稿和报告放在研究工作区。消息网关的长任务每阶段持久保存 `state/progress.json`，以便继续对话。
