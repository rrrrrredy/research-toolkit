# 研究工具箱插件

[English](README.md) | [简体中文](README.zh-CN.md)

一次安装，包含研究 Skill、完整方法和五个本地 MCP 工具。Agent 先澄清研究需求，用已有工具检索、分析、写作，再通过共用流程执行独立评审和交付检查。

以 Codex 为例，安装 Python 3.10 及以上版本、Git 和 Codex CLI 后运行：

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

重开会话，选择 Research Toolkit，确认五个 `research_*` 工具可用。直接说明研究题目、读者和成果要求；缺失的关键条件由 Agent 追问。

**[完整安装与使用说明](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md)** · [研究入口](SKILL.zh-CN.md) · [完整规范](references/research-standard.zh-CN.md)

默认评审使用已登录的 Codex CLI 账户，发送完整任务、正文与证据，分别启动评审和审查者，消耗对应额度。使用说明包含其他可信评审命令、失败恢复和评测模式。

通用 `plugin.json` / `mcp.json` 与 Codex 兼容清单 `.codex-plugin/plugin.json` / `.mcp.json` 启动相同实现。MCP 通过本地 stdio 接入，不是托管的 HTTPS 服务。包内没有凭据，机械检查也不证明研究质量。

维护时先修改仓库共用源码，再运行 `python scripts/build_plugin.py` 更新包内副本；`--check` 可核对一致性。
