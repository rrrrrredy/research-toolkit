# 研究工具箱插件

[English](README.md) | [简体中文](README.zh-CN.md)

一次安装，包含研究 Skill、完整方法和九个本地 MCP 工具。Agent 明确研究需求，用已有能力检索、分析与写作；需要任务管理时，包内 MCP 调用与 CLI 相同的本地能力。

使用宿主支持的插件安装方式；Python 3.10+ 与 MCP 依赖安装方法见下方指南。内置清单用 `python` 启动服务：宿主进程找到的解释器必须是已安装依赖的环境。若无法给插件指定该环境，按使用指南用虚拟环境解释器的绝对路径单独接入 MCP，避免安装到系统 Python 后仍用错解释器。

重开会话，选择 Research Toolkit，确认九个 `research_*` 工具可用。提供研究问题或已有报告、来源与用途，Agent 使用完整研究方法。安装插件提供了可调用工具，不要求每份报告都创建工具管理的任务。

**[完整安装与使用说明](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md)** · [研究入口](SKILL.zh-CN.md) · [完整规范](references/research-standard.zh-CN.md)

新建工具管理任务通过宿主的独立 Agent 完成审阅、审计与验收。原生委派不要求另配 API；自配 CLI／HTTP 后端仍是可选方式。

基础操作事件默认发送，首次运行提示并提供关闭方式，不含提示词、报告和路径。插件附带宿主 hooks，在宿主支持并信任后观察会话顺序。见[使用数据与控制](docs/usage-data.zh-CN.md)。

通用 `plugin.json` / `mcp.json` 与 Codex 兼容清单 `.codex-plugin/plugin.json` / `.mcp.json` 启动相同实现。MCP 通过本地 stdio 接入，不是托管的 HTTPS 服务。包内没有凭据，机械检查也不证明研究质量。

维护时先修改仓库共用源码，再运行 `python scripts/build_plugin.py` 更新包内副本；`--check` 可核对一致性。

生成归属保存在 `.generated-files.json`。`--check` 只读地检查内容与受管路径集合；构建仅删除仍与归属哈希匹配的过期副本。手写元数据与非受管内容保留，归属不明或已修改的过期副本须先核对。
