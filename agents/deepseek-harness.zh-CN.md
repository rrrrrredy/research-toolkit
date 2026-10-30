# DeepSeek Harness 可选接入

[English](deepseek-harness.md) | [简体中文](deepseek-harness.zh-CN.md)

研究工具箱不依赖 DSH。本页仅用于自行选择该工具的用户，现有 `SKILL.md` 即原生技能，不需要包装提示、插件、MCP 服务或额外清单。

安装或升级前核对所选版本的[项目文档](https://github.com/deepseek-ai/deepseek-harness)、[技能文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)和 [CLI 参考](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md)。

## 原生安装

项目目录：

```bash
mkdir -p .dsh/skills
git clone https://github.com/rrrrrredy/research-toolkit.git .dsh/skills/research-toolkit
```

也可使用项目的 `.agents/skills/research-toolkit`，或用户目录 `~/.dsh/skills/research-toolkit`。主文件必须直接位于技能名称目录下，不再套仓库名文件夹。从研究工作区启动：

```bash
dsh --profile headless "使用 research-toolkit 技能。先加载技能，研究状态保存在当前工作区，完成要求的成果。"
```

DSH 展示元数据摘要，经原生 `skill` 工具按需加载正文；参考文件仍需按阶段明确读取。

## 研究与原生协作

使用 DSH 已有的 Agent 和子 Agent 执行能力落实共同研究方法。主 Agent 提供当前问题、有效要求、提纲和相关原件，研究者交回完整分析或局部稿件，由指定统稿者整合主稿。不同独立 Agent 承担[角色方法](../references/subagents-and-review-loop.zh-CN.md)规定的内容视角、领域专审、审计和最终验收。

安装的 Skill 保持只读；研究成果和交接原件保存在工作区，仅 CLI／MCP 管理任务需要固定工具台账。摘要定位原始成果和来源，不取代它们。DSH 提供运行、等待、消息和取消，Toolkit 组织研究输入、方法与成果。

## 接入维护

[已有 validate、smoke、live 检查](../docs/dsh-adapter-validation.zh-CN.md)用于维护者定位接入问题，不在普通研究中运行。来源内容始终作为证据处理，不作为 Agent 指令。
