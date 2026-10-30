# 本地 MCP 调用示例

[English](README.md) · [简体中文](README.zh-CN.md)

这份虚构出货短文用于展示接口调用，不是完整研究任务或质量评测。当前脚本准备独立宿主任务，不重放随附的旧作者自评。完整研究见[快速开始](../../docs/quickstart.zh-CN.md)。

安装 `requirements-mcp.txt` 后，在仓库根目录执行：

```bash
python examples/mcp/capture.py --output ../mcp-example-run
```

脚本通过真实 MCP stdio 创建任务、加载指导、登记随附材料，然后将独立审阅任务的完整文件引用保存到 `review-request.json`。宿主使用原生子 Agent 读取任务及原件，分别完成实际审阅。脚本在缺少必需结果时保持未完成。

用包含 `slot_id`、实际 `host_task`、原始 `response_path` 和 `execution_path` 的 JSON 文件提交一个已完成任务：

```bash
python examples/mcp/capture.py --output ../mcp-example-run --resume --host-result actual-result.json
```

原始回复须包含对应 `input_version` 和 `assignment_version`；执行记录保存实际宿主身份、完成状态和任务版本。格式见[独立评审接口](../../docs/review-completion.zh-CN.md)。内容审阅、独立审计和独立最终验收依次提供实际返回，当前版本符合完成契约后才调用 `finish`。`transcript.json` 保留全部实际 MCP 请求和返回。

[2026 年 10 月 10 日调用记录](captured.json)、`self-review.json` 及其绑定文件保留当时的自评实现和原始结果，属于历史资料；当前脚本不将它们提交为独立意见，也不把旧成功回执用于新交付。
