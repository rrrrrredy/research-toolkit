# OpenCode：使用完整研究方法

[English](opencode.md) | [简体中文](opencode.zh-CN.md)

## 安装

Git 和客户端已就绪时，从项目根目录执行。目标目录已存在时，使用[更新指南](../docs/installation-versioning.zh-CN.md)。

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git .opencode/skills/research-toolkit
```

从此项目启动 OpenCode，要求加载 `research-toolkit` 技能。技能发现需开启，权限不能为 `deny`；此目录也符合官方 [V2 技能布局](https://opencode.ai/v2/docs/skills)。[官方技能要求](https://opencode.ai/docs/skills)。

`core.longpaths` 只对这个 Git 副本生效，避免 Windows 深层目录的路径过长错误。

## 使用

```text
使用 research-toolkit。
读取 .opencode/skills/research-toolkit/SKILL.md。
研究问题：[填写问题、读者与用途。]
范围与篇幅：[填写研究范围、信息截止日和预期深度。]
已有材料：[提供来源、文件或已有报告。]
按当前工作读取完整方法，充分展开证据、比较、机制解释和综合判断。
交付完整报告与可用引用，由你维护工作记录。
```

[统一研究指南](../docs/quickstart.zh-CN.md)提供完整请求和接入说明。

## 无法加载时

在同一项目目录执行：

```bash
git -C .opencode/skills/research-toolkit status --short
```

无输出表示副本干净；路径错误通常表示执行目录不对或克隆失败。有变更时可能存在缺失或修改过的文件，更新前保留自己的改动。文件存在但技能未出现时，重新打开项目或会话，检查宿主的技能设置。也可给出已安装 `SKILL.md` 的准确路径，要求 Agent 直接读取。[其他输入方式与边界](README.zh-CN.md)。
