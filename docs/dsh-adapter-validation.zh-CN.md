# DSH 接入维护检查

[English](dsh-adapter-validation.md) | [简体中文](dsh-adapter-validation.zh-CN.md)

本页从宿主安装卡片移入已有接入维护命令，不是研究任务的必经步骤。[安装与原生协作](../agents/deepseek-harness.zh-CN.md)。

## 专用接入检查

离线检查元数据、引用资源和暂存目录：

```bash
python scripts/run_dsh_evals.py validate
```

脚本化加载检查：

```bash
python scripts/run_dsh_evals.py smoke
```

smoke 子进程只继承白名单中的运行路径、用户与缓存目录、语言和临时目录变量，以及本地端点和占位凭据，不继承服务密钥或 `NODE_OPTIONS` 等运行时注入设置。这只限制环境变量传递，不为所选可执行程序提供文件访问隔离；live 路径仍使用单独配置的模型凭据。

它启动真实 headless CLI，连接本地脚本化端点，检查工具和目录项、发送工具调用、寻找配置的正文标记，并检查退出和成功标记。使用占位凭据，不调用真实模型；不逐字比较完整正文，也不独立验证每个工具结果。

真实模型案例：

```bash
python scripts/run_dsh_evals.py live --case source_instruction_boundary_zh
```

使用 DSH 已配置的模型与凭据，暂存一个已有案例，再用确定性检查器评分。内容质量仍需另外评审。

运行路径可通过 `--dsh-command-json` 或 `DSH_EVAL_COMMAND_JSON` 指定 argv；否则先用 PATH 中的 `dsh`，再回退到固定的 `@deepseek-ai/dsh@0.1.2-rc.1`。这是脚本回退版本，不代表上游最新版；本地核对对应 Node.js 要求。

`live` 的 `review` 与 `fail` 都返回非零；`--allow-review` 仅用于探索性收集。命令 JSON、提示和提交结果中不得包含凭据。报告及标准输出、错误输出保存在被 Git 忽略的 `evals/runs/dsh/`。
