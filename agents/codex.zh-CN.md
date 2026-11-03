# Codex CLI / IDE：使用完整研究方法

[English](codex.md) | [简体中文](codex.zh-CN.md)

## 安装

Git 和客户端已就绪时，从项目根目录执行。目标目录已存在时，使用[更新指南](../docs/installation-versioning.zh-CN.md)。

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
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
交付完整报告与可用引用，保留来源和完整分析用于交接，由宿主完成独立审阅、审计和验收。
```

使用宿主原生子 Agent 承担研究生产、统稿、独立内容审阅、审计和验收，沿用宿主已有模型能力，无需另配 API。共同传递当前要求和原始材料，保留完整交接成果。

[统一研究指南](../docs/quickstart.zh-CN.md)提供完整请求和接入说明。

## 用本地宿主执行已准备的工作

需要程序执行已选定的分析、比较和写作单元时，`scripts/research_host.py` 将已有研究输入和审阅任务接到本机 Codex app-server，沿用当前登录与模型设置。Agent 提供现有 `work`、`draft` 和可选的 `review` 参数，用户无需另行安装或配置 API。见[执行示例](../docs/usage-modes.zh-CN.md#codex-host-execution)。

适配器等待真实上游就绪，保留生产会话和完整原始回复，按实际传入的材料版本保存成果。运行期间输入变化会送回同一生产者。审阅使用相互独立的原生会话；已有任务指定原审阅者时，续接该会话。内容审阅、审计和验收仍由现有契约约束。负面意见交回协调者，由研究者判断怎样修订。

研究问题、工作分配、来源收集和最终综合仍由研究者负责。适配器执行已选工作，不选择固定团队，不自动改到通过，也不在本批工作结束后常驻。它与 CLI、MCP 共用同一份任务记录。

## 无法加载时

在同一项目目录执行：

```bash
git -C .agents/skills/research-toolkit status --short
```

无输出表示副本干净；路径错误通常表示执行目录不对或克隆失败。有变更时可能存在缺失或修改过的文件，更新前保留自己的改动。文件存在但技能未出现时，重新打开项目或会话，检查宿主的技能设置。也可给出已安装 `SKILL.md` 的准确路径，要求 Agent 直接读取。[其他输入方式与边界](README.zh-CN.md)。
