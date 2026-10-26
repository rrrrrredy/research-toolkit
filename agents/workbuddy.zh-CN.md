# WorkBuddy：使用完整研究方法

[English](workbuddy.md) | [简体中文](workbuddy.zh-CN.md)

使用能访问本地目录的 WorkBuddy。[官方产品说明](https://cloud.tencent.com/product/workbuddy)包含本地文件读取能力；以下方式无需原生 Skill 安装。

## 提供文件

在工作目录执行：

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git research-toolkit
```

在 WorkBuddy 中打开该工作目录，发送：

```text
读取提供的 research-toolkit/SKILL.md，按当前工作加载完整方法。
研究问题：[填写问题、读者与用途。]
范围与深度：[填写覆盖范围、信息截止日及篇幅要求。]
已有材料：[提供来源或已有报告。]
充分展开证据、比较、解释与综合判断，交付完整报告和可用引用。
无法读取必需材料时说明具体缺口，不编造内容。
```

提供研究问题、读者、范围与已有材料；按所需深度交付完整报告和可用引用。工作记录单独保存。

## 无法读取时

在工作目录执行：

```bash
git -C research-toolkit status --short
```

路径错误表示目录不存在或克隆失败；无输出表示副本干净。确认 WorkBuddy 获准访问的是同一个工作目录。

重复使用时，也可通过“技能 → 添加技能 → 上传技能”导入并启用。按[官方导入说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)和客户端实际接受的格式操作。本指南不假定工具箱已上架技能市场，也不把 GitHub ZIP 视为已经验证可导入的技能包。
