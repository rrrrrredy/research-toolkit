# 本地 MCP 调用示例

[English](README.md) · [简体中文](README.zh-CN.md)

这份虚构出货短文用于展示接口调用，不是完整研究任务或质量评测。当前脚本准备独立 Agent 工具任务，不重放随附的旧作者自评。完整研究见[快速开始](../../docs/quickstart.zh-CN.md)。

安装 `requirements-mcp.txt` 后，在仓库根目录执行：

```bash
python examples/mcp/capture.py --output ../mcp-example-run --host-task "ACTUAL_AGENT_TASK_OR_SESSION_ID"
```

将 `ACTUAL_AGENT_TASK_OR_SESSION_ID` 替换为当前执行 Agent 的真实任务或会话 ID。脚本导入现有示例稿，使用该身份登记 `main=true` 主稿及来源、主张。它通过真实 MCP stdio 创建任务、加载指导和保存材料，然后将独立审阅任务的完整文件引用保存到 `review-request.json`。Agent 工具使用原生子 Agent 读取任务及原件，分别完成实际审阅。首次命令运行到独立审阅任务准备就绪，尚不代表报告已验收；本示例关闭使用记录上传。

用包含 `slot_id`、实际 `host_task`、原始 `response_path` 和 `execution_path` 的 JSON 文件提交一个已完成任务：

```bash
python examples/mcp/capture.py --output ../mcp-example-run --resume --host-result actual-result.json
```

原始回复须包含对应 `input_version` 和 `assignment_version`；执行记录保存实际 Agent 执行身份、完成状态和任务版本。格式见[独立评审接口](../../docs/review-completion.zh-CN.md)。内容审阅、独立审计和独立最终验收依次提供实际返回，当前版本符合完成契约后才调用 `finish`。`transcript.json` 保留全部实际 MCP 请求和返回。

[2026 年 10 月 10 日调用记录](history/captured.json)、`history/self-review.json` 及其绑定文件保留当时的自评实现和原始结果，属于历史资料；当前脚本不将它们提交为独立意见，也不把旧成功回执用于新交付。

旧输入和原始哈希一起保存在 [history/](history/)，包括移除旧参数前的 `start.json`。当前执行不使用历史自评绑定校验新版输入。
