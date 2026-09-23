# Codex Skill 安装

[English](codex.md) | [简体中文](codex.zh-CN.md)

在能够读取本地文件的 Codex 环境中使用 `research-toolkit` Skill。克隆仓库需要 Git，运行检查脚本需要 Python。保留完整仓库副本，以便读取参考资料、脚本及说明文件。

## 安装为原生 Skill

在准备开展研究的项目根目录运行：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
```

入口是 `.agents/skills/research-toolkit/SKILL.md`。如需在多个项目中使用同一份用户级安装，将目标目录替换为 `<用户主目录>/.agents/skills/research-toolkit`。目录规则见[官方技能发现说明](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

目标目录已有副本时，先按下方更新说明处理。

## 确认发现并调用

1. 在研究项目中打开 Codex。在 CLI 或 IDE 扩展中，通过 `/skills` 或 `$` 选择列表查找 `research-toolkit`。
2. 选择该 Skill，让 Codex 读取完整指令及当前任务需要的参考文件。存在多个副本时，确认实际读取路径。
3. 新安装或更新后的 Skill 未出现时，重启 Codex 再检查。

CLI 或 IDE 扩展中的调用示例：

```text
$research-toolkit
为企业 IT 采购团队比较三款企业知识检索产品。
覆盖资料接入、权限、部署方式、价格与采用风险。
交付一份包含选择建议、来源和不确定性的比较报告。
先澄清缺失需求、确认提纲，再开展研究。
```

[官方使用说明](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills)介绍了显式选择和自动匹配。发现检查确认 Skill 可用；报告质量仍需实际内容审阅。

## 直接读取文件

也可以把完整仓库放在普通本地目录：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git agent-skills/research-toolkit
```

然后向 Codex 说明：

```text
使用 agent-skills/research-toolkit 中的研究工具箱完成本次任务。
先读 SKILL.md，按需读取 references。
将研究记录、草稿和报告放在独立任务目录中。
```

这种方式通过明确路径读取文件；普通的 `agent-skills/` 文件夹不属于上方列出的原生发现目录。

## 更新原生安装

在研究项目根目录先检查已安装副本：

```bash
git -C .agents/skills/research-toolkit status --short
```

先保留本地修改。副本没有本地改动且跟踪仓库 main 分支时，可运行：

```bash
git -C .agents/skills/research-toolkit pull --ff-only
```

更新后重新确认 Skill 能被发现。用户级安装需替换为实际路径；锁定版本或有本地修改的副本，按[版本识别与更新方法](../docs/installation-versioning.zh-CN.md)处理。

## 研究文件与交付检查

在独立研究目录保存 `state/`、`logs/`、`data/`、草稿和报告。继续任务时，从任务规格、进度、已有发现和已尝试方向恢复；重要补充要求保存在 `state/requirements.jsonl`。

最终交付前，将拟发送的完成说明保存到任务目录中的 `delivery_message.md`。使用上述项目级安装时，从项目根目录运行以下命令，并替换任务目录占位符：

```bash
python .agents/skills/research-toolkit/scripts/check_delivery.py <任务目录>
```

其他安装位置使用检查脚本的实际路径。它依赖 `scripts/check_review_completion.py`，两者需一同保留；记录格式见[交付检查](../docs/delivery-verification.zh-CN.md)与[评审完成接口](../docs/review-completion.zh-CN.md)。

除文件检查外，还需完成必需的内容审阅。必需检查无法运行或未通过时，明确交付阶段成果，或处理未完成事项后再宣布最终完成。
