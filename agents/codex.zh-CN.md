# Codex CLI / IDE：使用完整研究方法

[English](codex.md) | [简体中文](codex.zh-CN.md)

## 安装

Git 和客户端已就绪时，从项目根目录执行。目标目录已存在时，使用[更新指南](../docs/installation-versioning.zh-CN.md)。

新安装由 Agent 用现有 Python 3.10+ 执行以下命令。已有副本按[接入说明](../docs/usage-data.zh-CN.md#由-agent-自动接入)仅补缺失或变更配置，复用有效设置及插件 hooks，保留 off。基础事件默认发送，可关闭，不含题目、提示词、聊天、报告或路径；配置失败时仍直接使用方法研究。

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
python .agents/skills/research-toolkit/scripts/install_usage.py --host codex --project . --channel github-clone --form skill
```

输入 `/skills` 或 `$`，选择 `research-toolkit`，确认路径以 `.agents/skills/research-toolkit/SKILL.md` 结尾。[官方技能要求](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

`core.longpaths` 只对这个 Git 副本生效，避免 Windows 深层目录的路径过长错误。

## 使用

```text
使用 research-toolkit。
读取 .agents/skills/research-toolkit/SKILL.md。
研究问题：[填写问题、读者与用途。]
范围与篇幅：[填写研究范围、信息截止日和预期深度。]
已有材料：[提供来源、文件或已有报告。]
按当前工作读取完整方法，充分展开证据、比较、机制解释和综合判断。
交付完整报告与可用引用，保留来源和完整分析用于交接，由 Codex 完成独立审阅、审计和验收。
```

使用 Codex 的原生子 Agent 承担研究生产、统稿、独立内容审阅、审计和验收，沿用 Codex 已有模型能力，无需另配 API。共同传递当前要求和原始材料，保留完整交接成果。

[统一研究指南](../docs/quickstart.zh-CN.md)提供完整请求和接入说明。

## Agent 执行适配器

需要脚本管理执行时，使用共同的 [Agent 执行适配器](../docs/usage-modes.zh-CN.md#agent-host-execution)，指定 `--host codex`。原生子 Agent 工具也可通过同一套 work／save／review 契约工作，均沿用 Codex 的登录与模型配置。

共同示例说明依赖、输入更新、原始记录和独立审阅。同一研究单元使用一处调度，不同时通过原生工具和适配器重复启动。

## 无法加载时

在同一项目目录执行：

```bash
git -C .agents/skills/research-toolkit status --short
```

无输出表示副本干净；路径错误通常表示执行目录不对或克隆失败。有变更时可能存在缺失或修改过的文件，更新前保留自己的改动。文件存在但技能未出现时，重新打开项目或会话，检查 Codex 的技能设置。也可给出已安装 `SKILL.md` 的准确路径，要求 Agent 直接读取。[其他输入方式与边界](README.zh-CN.md)。
