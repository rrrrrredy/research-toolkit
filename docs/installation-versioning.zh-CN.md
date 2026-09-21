# 安装版本识别与更新

[English](installation-versioning.md) | [简体中文](installation-versioning.zh-CN.md)

当前仓库和 Skill 名称为 `research-toolkit`。GitHub 的旧仓库链接重定向到同一项目；当前页面为[研究工具箱](https://rrrrrredy.github.io/research-toolkit/)。

锁定旧提交的安装仍使用该提交的内容和 Skill 名称。需要更名后的版本时，选择新提交，放入 `research-toolkit` 技能目录，再核对实际文件。同一任务只启用预期版本。历史实验保留原名称和哈希。

仓库和规范 SKILL 只维护一套。发布版、安装副本、本地改版和实验所用版本可以不同，但必须分别识别。

## 比较实际内容

从已包含目标发布提交的可信克隆运行：

~~~bash
python scripts/check_installation.py /path/to/installed/research-toolkit --reference <full-commit-sha>
~~~

命令只读，对照 Git 对象中的内容，比较 SKILL.md、全部参考 Markdown、交付和评审完成检查器及其记录说明，仅规范文本换行。不把安装目录的 Git HEAD、README 版本或 INSTALLATION.json 当作内容相同的证明；不拉取、不安装、不写清单、不覆盖文件。

交付检查器依赖 `scripts/check_review_completion.py`，部分复制时须同时保留两个脚本。记录说明为 `docs/review-completion.md` 和 `docs/delivery-verification.md`；中文对照按相邻语言入口读取。历史版本只比较当时提交实际存在的文件。

退出码 0 表示选定内容一致；1 表示有修改、缺失或无法读取；2 表示参考版本无法读取。存在差异本身不证明本地改版有故障，应先阅读差异再决定保留什么。命令不检查未纳入范围的其他文件，也不证明运行环境实际加载的是哪一份。

实验记录解析后的完整提交号。有意修改的副本应记录自身内容哈希和名称，不能称为未经修改的发布版。精简本地 Skill 不能证明完整公开 Skill 导致某个问题，反之亦然；新模型运行应记录实际加载文件。

## 保留本地修改后更新

1. 选定版本并解析完整提交，单独核实发布状态。
2. 对比安装内容，在改动前备份当前安装的实际内容。
3. 未明确选择替换前保留本地修改。不要对有修改的工作区强制重置或覆盖整个目录；对照独立导出的干净版本，只应用约定文件。
4. 重新比较，并运行相关检查。按工具说明重启或重新加载，再核实预期 Skill 实际被加载。
5. 旧副本及其实验结果单独保存。更新安装不能改变历史报告实际使用的版本。

只安装新版检查器不会把旧版或精简 Skill 变成完整新版；规范未更新而检查器已更新，也是混合安装，须有意识别与记录。清单可以说明版本，但其声明仍须由实际文件支持。

## 分发范围

中英文入口放在同一仓库，`SKILL.md` 为唯一规范原件，环境接入说明位于 `agents/`。环境需要时，可以把同一 Skill 打包成插件、扩展或其他受支持格式；打包是可选分发方式，不能成为另一套研究规则。框架不由某一家 Agent 产品定义。

不要只因语言或安装器不同另建第二个维护中的 Skill 仓库。复用版本化来源，记录打包提交。安装或能力声明，与已观察的接入表现和研究质量分开表述。

## 维护网页与阅读入口

`docs/framework.html` 的 Full SKILL 区块是 `SKILL.md` 的副本。CI 在规范换行后检查全文一致性。规范修改后运行：

~~~bash
python scripts/check_docs_sync.py --write
python scripts/check_docs_sync.py
~~~

README 说明读者如何在线阅读、加载 Skill 或按环境安装；仓库拆分、同步命令、CI 和打包政策放在维护文档。对应中英文内容一同维护，两种语言的章节编号不必相同。

评测资料用途见[数据审计](evaluation-data-audit.zh-CN.md)，语义审查材料见[诊断对照](../evals/semantic_diagnostics/README.zh-CN.md)。安装内容相同不证明报告质量或运行时实际加载。
