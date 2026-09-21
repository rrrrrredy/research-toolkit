# Codex 接入

[English](codex.md) | [简体中文](codex.zh-CN.md)

适用于可读取或克隆本地仓库的 Codex 会话。

## 安装

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git agent-skills/research-toolkit
```

向 Codex 说明：

```text
使用 agent-skills/research-toolkit 中的研究工具箱。
先读 SKILL.md，按需读取 references。
本次研究先创建任务状态文件，再扩大资料收集。
```

## 执行要点

用文件保存 `state/`、`logs/`、`data/`、草稿和评审记录，正文与后台表分开。中断后从任务规格、进度、近期发现和已尝试方向恢复。交付对象是研究报告，不能让编码习惯取代研究关卡。

重要补充要求写入 `state/requirements.jsonl`。最终交付前，将拟交付说明保存为 `delivery_message.md`，从包含 `agent-skills/` 的目录运行：

```bash
python agent-skills/research-toolkit/scripts/check_delivery.py <task-directory>
```

也可以使用检查脚本的绝对安装路径。未通过时，明确交付实际阶段成果或修复对应问题，不宣称最终完成。
