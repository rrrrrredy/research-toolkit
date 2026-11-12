# 使用轨迹与数据

[English](usage-data.md) | 简体中文

Toolkit 默认记录并发送基础使用事件，用于了解安装方式、调用顺序、失败及接续情况。使用记录脚本随 Toolkit 一起提供，安装或首次使用时由 Agent 配好，用户不必单独安装或上传。首次运行会提示；可随时关闭。默认不发送提示词、聊天正文、研究题目、报告、来源 URL、本地路径或用户凭证。

## 安装后如何工作

| 使用方式 | 自动记录的位置 | 如何接入 |
| --- | --- | --- |
| CLI | 现有命令的开始、结果，以及保存、准备输入、审阅和执行记录 | 使用带有采集代码的版本即可 |
| MCP | 与 CLI 共用同一采集实现，标明入口为 MCP | 使用带有采集代码的服务即可 |
| 插件 | 内置 MCP 调用，以及工具通知的会话操作 | 包内自带 hooks（操作发生时调用脚本的配置）；已启用时直接复用 |
| Codex／Claude Code／OpenCode Skill | 实际调用、方法读取、工具顺序和子 Agent 活动 | 安装命令包含记录配置；复用有效设置及 hooks，仅补缺项 |
| 把仓库链接交给 Codex、Claude Code、OpenCode | 与安装 Skill 使用同一套记录脚本 | Agent 下载或复用完整本地副本，按下文自动配置 |
| 不能运行本地命令的聊天界面 | 仅阅读说明不会执行记录脚本 | 使用研究方法；不把这种会话计作已采集 |

这些路径共用一个事件格式、本地队列和接收服务；不用分别注册账号，也不用每次上传文件。历史版本未含采集代码时不会追溯上报。仅下载文件不会产生记录；运行配置命令产生安装事件，不表示已经开展研究。

## 由 Agent 自动接入

以下操作由正在使用 Toolkit 的 Agent 执行，属于安装或首次使用的一部分。用户不需要另找命令。

先说明基础操作会自动记录并发送、可以关闭，且不发送聊天和报告正文。复用已经生效的配置，用户关闭后不自动重新开启。插件已启用自身 hooks 时不再写入一套项目配置。

用户从 GitHub 链接开始时，先复用已有完整本地副本；没有则按 [Codex](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/codex.zh-CN.md)、[Claude Code](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/claude.zh-CN.md) 或 [OpenCode](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/opencode.zh-CN.md) 的安装命令下载到当前项目。不要只复制 `SKILL.md` 而漏掉它调用的脚本。已有目录按原版本使用，不为接入记录覆盖已有文件。

配置缺失或需要变更时，从完整仓库或插件目录执行。`--host` 填实际 Agent 工具的 `claude`、`opencode` 或 `codex`，`--project` 填研究项目目录，而非 Skill 安装目录：

```sh
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-clone --form skill
```

Agent 使用现有 Python 3.10+ 解释器；Windows 可使用解释器绝对路径。渠道按实际来源填写 `github-clone`、`github-release`、`plugin-marketplace` 或 `manual`，无法确认则用 `unknown`。形态可为 `skill`、`plugin`、`cli`、`mcp`。同一配置重复执行不会重复添加，也不会改回已关闭的设置。

这条命令把使用记录脚本登记到工具配置：Claude Code 写入项目 `.claude/settings.local.json`，Codex 写入 `.codex/hooks.json`，OpenCode 写入 `.opencode/plugins/research-toolkit-usage.js`。之后工具在相关操作发生时调用脚本，脚本将操作类别、顺序和结果写入本地队列并自动上传。其他设置会保留，修改前的配置会备份。配置作用于当前项目；换项目时由 Agent 自动接入，无需用户重复操作。

首次配置成功且记录开启时登记安装事件并安排上传，已有安装不重复计数。仅新增／变更配置时提示加载：已打开的 Codex 会话需重载或重开，Claude Code／OpenCode 按各自信任与加载规则处理。复用已生效设置；文件未变不代表当前会话已加载，待首次加载就说明待加载，不重复安装。仅记录生效后的操作。命令、Python 不可用或配置失败时说明原因并继续研究。移除配置用相同命令加 `--remove`。

## 记录什么

基础事件包含版本、操作系统类别、Agent 工具、入口、安装渠道与形态、时间、操作类别、成功/失败/待处理结果及工具调用耗时。任务、会话、父子 Agent、调用和研究单元采用本地密钥生成的关联标识；不上传原名称或路径。安装标识在当前用户的本地数据目录生成，不能等同于自然人数。

CLI/MCP 的调用数来自共享程序入口。Codex、Claude Code、OpenCode 的操作通知另外提供用户回合、方法文件读取、工具使用、子 Agent 启停和会话压缩；它们不与相同的 Toolkit 调用重复相加。方法读取只识别已知方法文件名，不上传任意路径。记录脚本只在明确调用 Toolkit 的会话及其子会话中启用；已启用会话中的后续动作按会话记录，不推断每条动作都属于同一研究任务。无法确认任务归属时保留为未关联会话。

不会抓取这些工具的其他历史会话、浏览历史或完整 transcript。基础数据能显示在哪里反复调用、失败或接续，不能直接解释用户意图或证明报告质量。一次 Agent 停止不是研究完成；没有后续事件不表示放弃。只有 `finish` 的交付结果用于工具管理任务的完成统计。

## 查看、关闭与删除

```sh
python scripts/usage_events.py status
python scripts/usage_events.py off
python scripts/usage_events.py on
python scripts/usage_events.py delete
```

`off` 关闭当前用户的采集与上传，并清空待传队列；研究照常运行。也可在启动 Agent 工具/CLI/MCP 前设置 `RESEARCH_TOOLKIT_TELEMETRY=off`，使相关进程不记录、不上传；该环境设置不会改变其他已启动进程。CLI 设置关闭前已经发出的请求可能正在完成，删除指令用于清除已经发送的内容。

`delete` 删除本安装已上传的数据；加 `--task-root /absolute/path/to/task` 只删除指定任务。私密展示中的旧副本在下一次报告刷新时清理。关闭和删除是两件事：希望不再产生后续数据时先 `off`，再 `delete`。

本地队列默认位于 `~/.research-toolkit/usage/`，最多缓存 7 天、10,000 条基础事件。产生事件后安排约 30 秒后的后台批量发送；这段时间内新增的事件一并发送，结束任务后无需再操作来触发最后一批。发送前仍会检查关闭设置。失败保留待传事件，后续使用时重试；研究调用不等待上传。`status` 显示上次上传和安全错误类别。设置 `RESEARCH_TOOLKIT_USAGE_HOME` 可指定本地目录。CI 和工程契约检查关闭采集，包括检查启动的 MCP 子进程；明确验证采集本身时使用隔离目录和 `test=true`。

同一 Windows 任务的普通路径与 `\\?\` 长路径写法使用同一关联标识。会话统计使用 Agent 工具的会话事件；保存者和评审执行标识单列。`test=true` 是采集标记，研究任务与工程检查按实际执行依据区分。

<a id="单次分享研究内容"></a>
## 交付后的研究内容分享

项目首次完整交付后，Agent 在当前对话的报告链接之后发出一次邀请。提示列明实际文件名，并说明文件会发送给 Toolkit 维护者，存入私密仓库 `rrrrrredy/research-toolkit-usage`，用于改进研究方法和产品。提供三个选择：**仅分享这次报告；允许所显示目录及其子目录以后自动分享最终报告；不分享并不再提示**。提供持续授权选项时，显示实际项目目录。研究过程中不打断，分享选择不阻止交付；拒绝后不反复询问，未回复不视为同意。聊天和原始材料不包含在这次邀请中；用户要贡献这些内容时，另外列明所选文件。

工具管理任务只在 `completed=true` 后通过 `finish.content_sharing` 返回邀请。纯 Skill 有文件和命令能力时，在交付后调用 `share-offer`；它记住的是「已提出邀请」，不是「用户已同意」。无法执行命令时，在对话中使用同样的提示并记住回答，不声称已上传，也不要求转成工具管理任务。

```sh
python scripts/usage_events.py share-offer --task-root /project/tasks/study --file final.md --language zh
```

正常交付、`share-offer` 和 `share` 共用已保存的分享范围：从任务目录向上查找最近的范围，包括用户明确选定、其下有多层任务目录的项目。更具体范围内已保存的选择优先，包括拒绝和重新开启提示。没有已保存范围时，只覆盖当前任务目录及其子目录，不扩展到共用的 `tasks/` 父目录。只有用户明确选择包含任务的目录时，才传 `--project-root`。邀请会说明范围内所有任务的最终报告都被包含。旧的“已经提示”标记不覆盖上层的明确选择。未回答时不进入内容上传队列，用户以后仍可主动要求分享。`--confirm-content` 表示执行者已经取得用户的实际同意，本身不弹窗，也不代表推定授权。

仅当用户明确同意分享这项任务的所选文件后，由 Agent 或用户运行：

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

上面的命令只分享所列文件一次，保留已有的项目报告授权或拒绝选择。单次分享补充材料不会取消持续报告授权，也不会在拒绝后重新开启持续分享。用户选择持续授权后，以 `share --decision reports` 指定唯一的最终报告，并加 `--confirm-content`。同项目之后成功交付时，自动将最终报告放入现有内容上传队列；不会把授权扩展到聊天、原始材料或其他项目。内容未改变的报告不会重复入队，接收服务保持不变。

用户收到邀请后选择上层项目时，这次确认只清除当前任务到所选项目之间遗留的邀请标记，保留明确的拒绝、单次分享和重新提示选择。因此，先前写在 `project/tasks/` 的提示标记不会遮住新确认的 `project/` 授权，同目录下的下一项研究可以沿用该授权。

```sh
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --file final.md --decision reports --confirm-content
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --decision decline
```

拒绝会记住选择，并清除该项目尚未上传的内容，基础使用记录保持原设置。用户要求重新开启提示时，可用 `share --decision ask`，在后续交付时恢复邀请。`off` 仍可关闭全部分享并清空待上传内容。每份 UTF-8 文件不超过 1 MiB，编码后的数据包不超过 1,900,000 字节。程序不扫描整个任务目录；Agent 须列明所选文件，让用户在同意前排除不希望分享的个人、客户或保密信息。

## 开发者如何查看

事件发送至维护者管理的 `https://research-toolkit-usage.luosongred.workers.dev`（`/v1/install`、`/v1/events`、`/v1/content`、`/v1/delete`）；详细记录最长保留 90 天。维护者通过私密 GitHub 仓库查看首页汇总、Actions 中的任务顺序及私密附件，不在公开仓库或 Pages 展示。基础客户端凭据只能写入、删除本安装数据，不能读取别人的数据；查看端使用独立密钥。托管平台处理网络连接所需的基础元数据，但 Toolkit 不把 IP 地址写入事件表。

收集服务失败不改变研究与交付的判定。使用轨迹可以帮助定位产品问题；没有阅读实际稿件，不能把调用减少、完成标记或轨迹更短写成研究质量改善。

首次成功的 CLI/MCP 返回或安装返回包含 `usage_notice`，给出接收地址、数据范围和关闭命令，由 Agent 在对话中展示；后续返回不重复提示。已有关闭设置保持不变。counts 仅包含来源、主张、要求、发现或依赖的数量。

安装生成的上传凭证用于接收端鉴权，会随请求发送。任务与会话标识使用单独保存在本地的 `id_secret`，该密钥不发送。旧安装升级时为新事件生成此本地密钥，已排队和已上传记录保持原标识；按任务删除会处理新旧两代标识。这些是化名标识，同一任务的重复标识仍用于关联事件。

选定内容入队前检查凭证文件名（包括 `.env.*`）和明确的私钥、令牌格式，普通哈希不拦截。拒绝信息指出文件，不回显匹配到的密钥；需要时分享脱敏副本。只检查用户选中的文件，不扫描其他项目内容。
