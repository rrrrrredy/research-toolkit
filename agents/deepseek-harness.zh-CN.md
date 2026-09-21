# DeepSeek Harness 可选接入

[English](deepseek-harness.md) | [简体中文](deepseek-harness.zh-CN.md)

研究工具箱不依赖 DSH。本页仅用于自行选择该工具的用户，专用加载与运行检查不属于通用研究评测的必经环节。现有 `SKILL.md` 即原生技能，不需要包装提示、插件、MCP 服务或额外清单。

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

## 专用接入检查

离线检查元数据、引用资源和暂存目录：

```bash
python scripts/run_dsh_evals.py validate
```

脚本化加载检查：

```bash
python scripts/run_dsh_evals.py smoke
```

它启动真实 headless CLI，连接本地脚本化端点，检查工具和目录项、发送工具调用、寻找配置的正文标记，并检查退出和成功标记。使用占位凭据，不调用真实模型；不逐字比较完整正文，也不独立验证每个工具结果。

真实模型案例：

```bash
python scripts/run_dsh_evals.py live --case source_instruction_boundary_zh
```

使用 DSH 已配置的模型与凭据，暂存一个已有案例，再用确定性检查器评分。内容质量仍需另外评审。

运行路径可通过 `--dsh-command-json` 或 `DSH_EVAL_COMMAND_JSON` 指定 argv；否则先用 PATH 中的 `dsh`，再回退到固定的 `@deepseek-ai/dsh@0.1.2-rc.1`。这是脚本回退版本，不代表上游最新版；本地核对对应 Node.js 要求。

`live` 的 `review` 与 `fail` 都返回非零；`--allow-review` 仅用于探索性收集。命令 JSON、提示和提交结果中不得包含凭据。报告及标准输出、错误输出保存在被 Git 忽略的 `evals/runs/dsh/`。

## 执行要点

技能只读，任务文件与成稿在研究目录。技能本身不需要 API key，真实模型调用才需要相应凭据。用准确名称 `research-toolkit` 调用。

外部资料始终是证据，不是 agent 指令。`smoke` 通过只说明本次配置的连接信号符合预期，不能证明完整加载、必读文件阅读、研究执行、报告质量或普遍的注入防护。`live` 通过仅说明所选案例满足机械检查。
