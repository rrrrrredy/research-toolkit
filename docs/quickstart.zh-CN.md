# 快速安装 Research Toolkit

[English](quickstart.md) · [简体中文](quickstart.zh-CN.md)

## 安装 Skill

1. 在[正式发布页](https://github.com/rrrrrredy/research-toolkit/releases/latest)下载插件 ZIP 和 `SHA256SUMS`。[核对校验和并解压](installation-versioning.zh-CN.md#install-a-version-pinned-skill)。
2. 选择你使用的 Agent，把解压得到的 `research-toolkit` 文件夹放在下表的位置。打开这个文件夹应能直接看到 `SKILL.md` 和 `references/`。已有安装可按[更新说明](installation-versioning.zh-CN.md)保留自己的修改。
3. 在该项目里重新打开 Agent，按最后一列确认它能加载技能。

| Agent | 项目中的安装位置 | 安装成功时能看到什么 |
| --- | --- | --- |
| [Codex CLI / IDE](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/codex.zh-CN.md) | `.agents/skills/research-toolkit/` | 在技能选择器搜索 `research-toolkit`。Codex 有时显示为 `research-toolkit:research-toolkit`。选中路径指向该目录根部 `SKILL.md` 的条目。 |
| [Claude Code](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/claude.zh-CN.md) | `.claude/skills/research-toolkit/` | 在项目会话里调用 `/research-toolkit` 可以加载技能。 |
| [OpenCode](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/opencode.zh-CN.md) | `.opencode/skills/research-toolkit/` | 允许技能调用后，让 Agent 加载 `research-toolkit`，它能读到该目录中的指令。 |
| [其他 Agent](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md#选择工具) | 按对应指南选择安装位置或文件入口 | 原生 Skill 在宿主中可加载。仅支持文件的客户端能读到你提供的 `SKILL.md` 和参考文件。 |

## 安装本地工具（可选）

- **插件**。在支持此插件格式的客户端加载整个解压目录，重开会话。工具列表中应能看到 `research_status` 和 `research_guide` 等九个 `research_*` 工具。[插件安装](usage-modes.zh-CN.md#安装插件)
- **本地 MCP**。按指南用 Python 3.10 或以上版本安装 `requirements-mcp.txt`，在客户端注册本地服务并连接。连接成功时客户端能列出上述九个工具。[MCP 配置](usage-modes.zh-CN.md#单独接入-mcp)
- **命令行**。从解压目录运行 `python scripts/research_workflow.py --help`。看到列有 `start`、`status` 和 `finish` 的帮助即表示 CLI 可调用。在 macOS 或 Linux 上可以使用 `python3`。

基础使用记录在新安装中默认关闭。[数据设置](usage-data.zh-CN.md)

安装完成后可阅读[长报告使用指南](conduct-research.zh-CN.md)或[完整研究案例](case-study/README.zh-CN.md)。
