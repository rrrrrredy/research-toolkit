# 使用轨迹与数据

[English](usage-data.md) | 简体中文

新安装默认关闭基础使用记录。用户主动开启后，Toolkit 才发送操作元数据，帮助维护者了解安装方式、失败及接续情况。这些事件不包含提示词、聊天正文、研究题目、报告、来源 URL、本地路径或用户凭证。已有开启或关闭设置继续生效。研究报告分享单独授权。

**版本说明**　此命令随 v3.0.0 之后的[仓库源码](https://github.com/rrrrrredy/research-toolkit)提供。要先看当前设置和将涉及的文件，可运行 `python scripts/research_workflow.py setup --host codex --project .`。它列出记录开关、配置路径和将安装的钩子。新安装返回 `planned_action: none`，预览过程不写文件。使用 `setup --host codex --no-telemetry` 会跳过本次配置。已明确开启记录时，`setup --host codex --apply` 可写入预览所列的钩子。

## 安装后如何工作

| 使用方式 | 同意后记录的操作 | 如何接入 |
| --- | --- | --- |
| CLI | 现有命令的开始、结果，以及保存、准备输入、审阅和执行记录 | 使用带有采集代码的版本即可 |
| MCP | 与 CLI 共用同一采集实现，标明入口为 MCP | 使用带有采集代码的服务即可 |
| 插件 | 内置 MCP 调用，以及工具通知的会话操作 | 包内自带 hooks（操作发生时调用脚本的配置）；已启用时直接复用 |
| Codex／Claude Code／OpenCode Skill | 实际调用、方法读取、工具顺序和子 Agent 活动 | 按下文可选设置为当前项目接入记录 |
| 把仓库链接交给 Codex、Claude Code、OpenCode | 与安装 Skill 使用同一套记录脚本 | 直接读取方法或使用完整本地副本。仅在用户同意后配置记录 |
| 不能运行本地命令的聊天界面 | 仅阅读说明不会执行记录脚本 | 使用研究方法；不把这种会话计作已采集 |

这些路径共用一个事件格式、本地队列和接收服务。下载文件不会产生记录。开启记录后配置接入，可先于研究操作生成一条安装事件。

<a id="由-agent-自动接入"></a>
<a id="enable-basic-recording"></a>

## 开启基础使用记录

新安装默认关闭基础记录。升级沿用已保存的设置。旧版的默认开启和手动开启都保存为 `on`。可以用 `status` 查看当前设置，用 `off` 关闭。

用户明确要求开启时，从完整的 [Skill 安装目录](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/installation-versioning.zh-CN.md#install-a-version-pinned-skill)或插件目录运行第一条命令，为当前本地用户开启跨项目的基础事件。CLI 和 MCP 只需这一步。用户还希望记录当前项目的 Agent 会话操作时，再按实际工具运行第二条命令。插件自带的 hooks 已生效时直接复用。

```sh
python scripts/usage_events.py on
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-release --form skill
```

使用 Python 3.10+ 解释器。`--host` 填 `codex`、`claude` 或 `opencode`，`--project` 填研究项目目录。渠道按实际来源填写 `github-clone`、`github-release`、`plugin-marketplace` 或 `manual`，无法确认时用 `unknown`。形态可为 `skill`、`plugin`、`cli` 或 `mcp`。

安装脚本仅在记录开启时配置当前项目的 hooks。Claude Code 写入 `.claude/settings.local.json`，Codex 写入 `.codex/hooks.json`，OpenCode 写入 `.opencode/plugins/research-toolkit-usage.js`。保留其他设置，备份有变化的配置并复用已匹配的配置。记录关闭时，包内自带的 hook 在读取输入前退出。给安装命令加 `--remove` 可移除 Toolkit 写入的项目 hooks。

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

`off` 关闭当前本地用户的基础使用记录，清空待传基础事件。若要让某个 Agent 工具、CLI 或 MCP 进程同时停用基础事件和内容上传，在启动前设置 `RESEARCH_TOOLKIT_TELEMETRY=off`。设置只影响收到该变量的进程，已发出的请求仍可能完成。新安装保持默认设置时，接入、正常操作和状态查询均不创建本地采集库。

`delete` 删除本安装已上传的数据，加 `--task-root /absolute/path/to/task` 只删除指定任务。私密展示中的旧副本在下一次报告刷新时清理。要停止后续上传，分别关闭基础记录并撤回已开启的报告分享授权。

本地队列默认位于 `~/.research-toolkit/usage/`，最多缓存 7 天、10,000 条基础事件。产生事件后安排约 30 秒后的后台批量发送；这段时间内新增的事件一并发送，结束任务后无需再操作来触发最后一批。发送前仍会检查关闭设置。失败保留待传事件，后续使用时重试；研究调用不等待上传。`status` 显示上次上传和安全错误类别。设置 `RESEARCH_TOOLKIT_USAGE_HOME` 可指定本地目录。CI 和工程契约检查关闭采集，包括检查启动的 MCP 子进程；明确验证采集本身时使用隔离目录和 `test=true`。

同一 Windows 任务的普通路径与 `\\?\` 长路径写法使用同一关联标识。会话统计使用 Agent 工具的会话事件；保存者和评审执行标识单列。`test=true` 是采集标记，研究任务与工程检查按实际执行依据区分。

<a id="单次分享研究内容"></a>
## 交付后的研究内容分享

单次分享和项目持续授权都需要明确同意，基础记录关闭时也能使用。用户希望看到邀请，或已有设置要求提示时，在交付报告链接后列明实际文件名和接收方。接收方为 Toolkit 维护者的私密仓库 `rrrrrredy/research-toolkit-usage`。用户可以仅分享本次报告，允许所显示目录及其子目录未来自动分享最终报告，或拒绝分享。未回复时报告保留在本地。用户希望另外贡献聊天或原始资料时，单独列明所选文件。

工具管理任务在 `completed=true` 后可以通过 `finish.content_sharing` 返回邀请。纯 Skill 可在交付后调用 `share-offer` 查看适用的分享设置。新安装默认关闭基础记录时，不自动发出分享邀请。旧版已保存的 `off` 继续暂停原有自动分享授权。用户仍可明确授权新的单次分享，或对选定目录重新确认持续分享。

```sh
python scripts/usage_events.py share-offer --task-root /project/tasks/study --file final.md --language zh
```

正常交付、`share-offer` 和 `share` 共用已保存的分享范围：从任务目录向上查找最近的范围，包括用户明确选定、其下有多层任务目录的项目。更具体范围内已保存的选择优先，包括拒绝和重新开启提示。没有已保存范围时，只覆盖当前任务目录及其子目录，不扩展到共用的 `tasks/` 父目录。只有用户明确选择包含任务的目录时，才传 `--project-root`。邀请会说明范围内所有任务的最终报告都被包含。旧的“已经提示”标记不覆盖上层的明确选择。未回答时不进入内容上传队列，用户以后仍可主动要求分享。`--confirm-content` 表示执行者已经取得用户的实际同意，本身不弹窗，也不代表推定授权。

旧持续授权没有记录用户是否确认过明确显示的目录范围。下一次交付或 `share-offer` 使用这种授权时，沿用现有邀请显示实际目录；用户同意前不将新报告入队。未回答时只提示一次，单次分享不确认今后的自动分享。选择 `reports` 后保存范围确认，后续交付沿用该授权。用户可以选择更窄的目录或拒绝；已有明确拒绝继续有效。

仅当用户明确同意分享这项任务的所选文件后，由 Agent 或用户运行：

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

上面的命令只分享所列文件一次，保留已有的项目报告授权或拒绝选择。单次分享补充材料不会取消持续报告授权，也不会在拒绝后重新开启持续分享。用户选择持续授权后，以 `share --decision reports` 指定唯一的最终报告，并加 `--confirm-content`。同项目之后成功交付时，自动将最终报告放入现有内容上传队列；不会把授权扩展到聊天、原始材料或其他项目。内容未改变的报告不会重复入队，接收服务保持不变。

用户收到邀请后选择上层项目时，这次确认只清除当前任务到所选项目之间遗留的邀请标记，保留明确的拒绝、单次分享和重新提示选择。因此，先前写在 `project/tasks/` 的提示标记不会遮住新确认的 `project/` 授权，同目录下的下一项研究可以沿用该授权。

显示邀请只记录已提示，不会覆盖用户明确选择的 `ask`、拒绝或持续报告授权。子目录设为 `ask` 后，即使已经显示邀请，也继续阻止继承上层目录的自动分享授权；未回复不入队。用户明确选择 `share --decision ask` 时，会重置提示记录，允许再次显示邀请。单次分享也保留这一选择。

```sh
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --file final.md --decision reports --confirm-content
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --decision decline
```

拒绝会记住选择，并清除该项目尚未上传的内容。用户要求重新开启提示时，可用 `share --decision ask` 在后续交付中恢复邀请。两种选择均保留基础使用记录的原设置。每份 UTF-8 文件不超过 1 MiB，编码后的数据包不超过 1,900,000 字节。Agent 须在取得同意前列明所选文件。

撤回上级持续授权所覆盖的某个目录时，无论选择拒绝还是恢复提示，都会清除该目录下依该授权入队的待传内容。兄弟目录仍可使用上级授权。对于旧版从上级授权入队、缺少本地路径且无法确认位于撤回范围外的待传内容，一并移除。

## 开发者如何查看

事件发送至维护者管理的 `https://research-toolkit-usage.luosongred.workers.dev`（`/v1/install`、`/v1/events`、`/v1/content`、`/v1/delete`）；详细记录最长保留 90 天。维护者通过私密 GitHub 仓库查看首页汇总、Actions 中的任务顺序及私密附件，不在公开仓库或 Pages 展示。基础客户端凭据只能写入、删除本安装数据，不能读取别人的数据；查看端使用独立密钥。托管平台处理网络连接所需的基础元数据，但 Toolkit 不把 IP 地址写入事件表。

收集服务失败不改变研究与交付的判定。使用轨迹可以帮助定位产品问题；没有阅读实际稿件，不能把调用减少、完成标记或轨迹更短写成研究质量改善。

首次成功的 CLI/MCP 返回或安装返回包含 `usage_notice`，给出接收地址、数据范围和关闭命令。CLI 请求将 `language` 传给该提示：`zh`／`zh-CN` 使用中文，`en` 使用英文。Agent 在对话中展示，后续返回不重复提示。已有关闭设置保持不变。counts 仅包含来源、主张、要求、发现或依赖的数量。

安装生成的上传凭证用于接收端鉴权，会随请求发送。任务与会话标识使用单独保存在本地的 `id_secret`，该密钥不发送。旧安装升级时为新事件生成此本地密钥，已排队和已上传记录保持原标识；按任务删除会处理新旧两代标识。这些是化名标识，同一任务的重复标识仍用于关联事件。

选定内容入队前检查凭据文件名，包括 `.env.*`、`credentials.json`、`client_secret*.json`、`secrets.yaml`、`.npmrc` 和 `.netrc`；检查私钥、可识别的 OpenAI/Anthropic、GitHub、AWS、Slack 和 Google 令牌格式、JWT，以及授权／密码字段中填写的值和数据库连接中的密码。普通哈希、协议说明及 `<password>`、`${DB_PASSWORD}`、`YOUR_TOKEN` 等明确占位符可继续用于报告。拒绝信息指出文件，不回显匹配到的密钥，本批选中文件均不入队；需要时分享脱敏副本。只检查用户选中的文件，不扫描其他项目内容。
