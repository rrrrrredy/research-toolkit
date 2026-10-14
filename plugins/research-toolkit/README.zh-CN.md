# 研究工具箱插件

[English](README.md) | [简体中文](README.zh-CN.md)

一次安装，包含研究 Skill、完整方法和八个本地 MCP 工具。Agent 先澄清研究需求，用已有工具检索、分析、写作，再通过共用流程执行选定档位的评审和交付检查。

使用宿主支持的插件安装方式；Python 3.10+ 与 MCP 依赖安装方法见下方指南。内置清单用 `python` 启动服务：宿主进程找到的解释器必须是已安装依赖的环境。若无法给插件指定该环境，按使用指南用虚拟环境解释器的绝对路径单独接入 MCP，避免安装到系统 Python 后仍用错解释器。

重开会话，选择 Research Toolkit，确认八个 `research_*` 工具可用。提供研究问题或已有报告、来源与用途，Agent 推荐 Lite／Full 并维护工作记录。

**[完整安装与使用说明](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md)** · [研究入口](SKILL.zh-CN.md) · [完整规范](references/research-standard.zh-CN.md)

新建 Full 任务未配置后端时，使用明确标注强度降级的 self 评审；external／independent 可配置 CLI 或兼容 HTTP 后端。Lite 跳过评审和完整交付门槛，保留最终 checklist。已声明的独立评审、评测与审计计划不静默降级。材料去向、额度及配置自查见完整使用说明。

通用 `plugin.json` / `mcp.json` 与 Codex 兼容清单 `.codex-plugin/plugin.json` / `.mcp.json` 启动相同实现。MCP 通过本地 stdio 接入，不是托管的 HTTPS 服务。包内没有凭据，机械检查也不证明研究质量。

维护时先修改仓库共用源码，再运行 `python scripts/build_plugin.py` 更新包内副本；`--check` 可核对一致性。

生成归属保存在 `.generated-files.json`。`--check` 只读地检查内容与受管路径集合；构建仅删除仍与归属哈希匹配的过期副本。手写元数据与非受管内容保留，归属不明或已修改的过期副本须先核对。
