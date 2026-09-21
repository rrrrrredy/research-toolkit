# Gemini CLI 接入

[English](gemini-cli.md) | [简体中文](gemini-cli.zh-CN.md)

适用于能够访问本地工作目录的 Gemini CLI。

## 安装

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git .agent/research-toolkit
```

```text
读取 .agent/research-toolkit/SKILL.md 并作为研究规范。
只在当前阶段需要时读取 references。
在任务目录创建 state/、logs/、data/、drafts/、final/。
不要用来源数量判断研究完成。
```

## 执行要点

任务状态写在研究目录，不写回工具箱。收集和提炼主张后更新登记表；每阶段明确 `state/progress.json` 的 `next_action`。最终交付前完成研究检查清单。
