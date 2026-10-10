# WorkBuddy：第一个 Lite 任务

[English](workbuddy.md) | [简体中文](workbuddy.zh-CN.md)

使用能访问本地目录的 WorkBuddy。[官方产品说明](https://cloud.tencent.com/product/workbuddy)包含本地文件读取能力；以下方式无需原生 Skill 安装。

## 提供文件

在工作目录执行：

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git research-toolkit
```

在 WorkBuddy 中打开该工作目录，发送：

```text
读取 research-toolkit/SKILL.md，选择 profile=lite。
读取 research-toolkit/examples/lite/start.zh.json 和
research-toolkit/examples/lite/sources.zh-CN.md，完成这个虚构客服
工具比较。分别交付短报告、sources/claims 记录及完整的六项
Lite checklist。成果保存在独立任务目录。
披露材料虚构且没有独立评审。
```

预计约 5–15 分钟产出 600–900 字简报及记录。[完整入门](../docs/quickstart-lite.zh-CN.md)。

## 无法读取时

在工作目录执行：

```bash
git -C research-toolkit status --short
```

路径错误表示目录不存在或克隆失败；无输出表示副本干净。确认 WorkBuddy 获准访问的是同一个工作目录。

重复使用时，也可通过“技能 → 添加技能 → 上传技能”导入并启用。按[官方导入说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)和客户端实际接受的格式操作。本指南不假定工具箱已上架技能市场，也不把 GitHub ZIP 视为已经验证可导入的技能包。
