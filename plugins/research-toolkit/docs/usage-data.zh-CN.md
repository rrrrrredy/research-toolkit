# 使用轨迹与数据

[English](usage-data.md) | 简体中文

Toolkit 的程序入口默认发送基础使用事件，用于了解安装方式、调用顺序、失败及接续情况。首次运行会提示；可随时关闭。默认不发送提示词、聊天正文、研究题目、报告、来源 URL、本地路径或密钥。

## 安装后如何工作

| 使用方式 | 自动记录的位置 | 一次性接入 |
| --- | --- | --- |
| CLI | 现有命令的开始、结果，以及保存、准备输入、审阅和执行记录 | 使用带有采集代码的版本即可 |
| MCP | 与 CLI 共用同一采集实现，标明入口为 MCP | 使用带有采集代码的服务即可 |
| 插件 | 内置 MCP 的程序事件；支持并信任 hooks 的宿主还可提供会话事件 | 安装插件并完成宿主的 hooks 信任 |
| 纯 Skill | 宿主观察器记录实际调用和工具使用顺序，不要求 Agent 额外上报 | 在使用项目中安装一次下方观察器，并按宿主提示信任 |
| 只阅读链接、粘贴文本，或无法执行观察器的聊天界面 | 没有运行组件，不能自动上报 | 仍可正常使用研究方法 |

这些路径共用一个事件格式、本地队列和接收服务；不用分别注册账号，也不用每次上传文件。历史版本未含采集代码时不会追溯上报。安装但从未运行，不计为已观察到的使用。

从已下载的完整仓库或插件目录运行一次，替换项目绝对路径。选择实际宿主 `claude`、`opencode` 或 `codex`：

```sh
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-clone --form skill
```

`python` 应是已安装的 Python 3.10+ 解释器；Windows 可使用解释器绝对路径。渠道按实际来源填写 `github-clone`、`github-release`、`plugin-marketplace` 或 `manual`，无法确认则用 `unknown`。形态可为 `skill`、`plugin`、`cli`、`mcp`。这段安装用于宿主观察，不改变研究方法或增加研究步骤。插件已经加载自己的 hooks 时，不必重复安装项目 hooks。

安装器只修改自己的 hooks/plugin 项，保留其他设置并为改动前的文件留备份。Claude Code 写入项目 `.claude/settings.local.json`，Codex 写入 `.codex/hooks.json`，OpenCode 写入 `.opencode/plugins/research-toolkit-usage.js`。宿主要求的信任与权限仍由宿主处理。移除观察器使用相同命令加 `--remove`。

## 记录什么

基础事件包含版本、操作系统类别、宿主、入口、安装渠道与形态、时间、操作类别、成功/失败/待处理结果及工具调用耗时。任务、会话、父子 Agent、调用和研究单元采用本地密钥生成的关联标识；不上传原名称或路径。安装标识在当前用户的本地数据目录生成，不能等同于自然人数。

CLI/MCP 的调用数来自共享程序入口。宿主另外观察用户回合、方法文件读取、工具使用、子 Agent 启停和会话压缩；它们不与相同的 Toolkit 调用重复相加。方法读取只识别已知方法文件名，不上传任意路径。宿主观察器只激活明确调用 Toolkit 的会话及其子会话；已激活会话中的后续动作是会话级观察，不推断每条动作都属于同一研究任务。无法确认任务归属时保留为未关联会话。

不会抓取宿主的其他历史会话、浏览历史或完整 transcript。基础数据能显示在哪里反复调用、失败或接续，不能直接解释用户意图或证明报告质量。一次 Agent 停止不是研究完成；没有后续事件不表示放弃。只有 `finish` 的交付结果用于工具管理任务的完成统计。

## 查看、关闭与删除

```sh
python scripts/usage_events.py status
python scripts/usage_events.py off
python scripts/usage_events.py on
python scripts/usage_events.py delete
```

`off` 关闭当前用户的采集与上传，并清空待传队列；研究照常运行。也可在启动宿主/CLI/MCP 前设置 `RESEARCH_TOOLKIT_TELEMETRY=off`，使相关进程不记录、不上传；该环境设置不会改变其他已启动进程。CLI 设置关闭前已经发出的请求可能正在完成，删除指令用于清除已经发送的内容。

`delete` 删除本安装已上传的数据；加 `--task-root /absolute/path/to/task` 只删除指定任务。私密展示中的旧副本在下一次报告刷新时清理。关闭和删除是两件事：希望不再产生后续数据时先 `off`，再 `delete`。

本地队列默认位于 `~/.research-toolkit/usage/`，最多缓存 7 天、10,000 条基础事件。网络传输在后台进行，失败保留待传事件，后续使用时重试；研究调用不等待上传。`status` 显示上次上传和安全错误类别。设置 `RESEARCH_TOOLKIT_USAGE_HOME` 可指定本地目录。CI 默认不发送；明确验收的流量带 `test=true` 并从实际使用统计中分开。

## 单次分享研究内容

仅当用户明确同意分享这项任务的所选文件后，由 Agent 或用户运行：

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

这次授权只覆盖所列文件；之后新增或修改的文件不会自动分享。每份 UTF-8 文件不超过 1 MiB，编码后的数据包不超过 1,900,000 字节，且必须在指定任务目录内。上传前应确认所选文件没有不希望分享的个人、客户或保密信息。程序不扫描整个任务目录，不把内容授权视为永久同意。

## 开发者如何查看

事件进入项目维护者管理的私密接收端，详细记录最长保留 90 天。维护者通过私密 GitHub 仓库查看首页汇总、Actions 中的任务顺序及私密附件，不在公开仓库或 Pages 展示。基础客户端凭据只能写入、删除本安装数据，不能读取别人的数据；查看端使用独立密钥。托管平台处理网络连接所需的基础元数据，但 Toolkit 不把 IP 地址写入事件表。

收集服务失败不改变研究与交付的判定。使用轨迹可以帮助定位产品问题；没有阅读实际稿件，不能把调用减少、完成标记或轨迹更短写成研究质量改善。
