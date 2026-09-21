# OpenClaw 接入

[English](openclaw.md) | [简体中文](openclaw.zh-CN.md)

适用于可从工作区或用户目录读取本地技能的 OpenClaw。依据官方[技能说明](https://docs.openclaw.ai/tools/skills)与[技能配置](https://docs.openclaw.ai/tools/skills-config)。

## 安装

每个技能目录含带 YAML 元数据的 `SKILL.md`，可见技能名称来自其 `name` 字段。默认状态目录下，按以下优先级发现：

```text
<workspace>/skills/research-toolkit
<workspace>/.agents/skills/research-toolkit
~/.agents/skills/research-toolkit
~/.openclaw/skills/research-toolkit
```

设置 `OPENCLAW_STATE_DIR` 时，托管技能位于 `<state-dir>/skills/`，不会加载家目录的 `~/.agents/skills/` 兼容目录。按当前配置选择路径。

工作区安装：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git ./skills/research-toolkit
```

默认托管目录安装：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git ~/.openclaw/skills/research-toolkit
```

向 agent 说明：

```text
使用 research-toolkit 技能完成研究。
先读 SKILL.md，按阶段需要读取 references。
state/、logs/、data/ 放在研究项目目录，不写入技能目录。
```

## 执行要点

普通研究期间技能只读。任务状态、草稿和成稿均写入研究目录。工具箱不需要 `skills.entries.<key>.env` 或 `apiKey`；它是指令包，不是依赖秘密的工具。

启用技能允许列表时，允许元数据名称 `research-toolkit`。技能或配置更新后可能需要新会话刷新快照。没有技能加载器时，粘贴或上传主文件，按需手动读取参考文件。长任务每阶段更新 `state/progress.json`，供后续会话恢复。
