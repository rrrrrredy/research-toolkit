# 本地 MCP 工作流示例

[English](README.md) · [简体中文](README.zh-CN.md)

示例是一份关于虚构出货记录的三段英文短文，用于展示 Full 自评流程，不是研究评测或独立意见。报告、来源、登记表和有具体依据的作者自评均已提供。首次研究任务仍建议 Lite；Lite 跳过评审。

安装 `requirements-mcp.txt` 后，在仓库根目录执行：

```bash
python examples/mcp/capture.py --output ../mcp-example-run
```

使用仓库之外新的短路径，Windows 尤其需要注意。脚本通过真实 stdio 启动 `scripts/research_mcp.py`，调用 start 与 guide，将随附作者文件写入返回的任务目录，用 status 推进至起草阶段，获取自评提示，带当前输入版本提交随附自评，最后调用 finish。它重放已有作者评审，不调用模型或产生新评估；新研究任务必须由 Agent 起草并评审实际报告。

预期文件：包含完整 MCP 返回的 `transcript.json`、`review-request.json`，以及 `tasks/shipment-note/` 下的报告、来源／判断 CSV、`logs/review.jsonl`、评审回复和 `state/final_delivery.json`。评审及回执保留 `reviewer: self` 与 `review_strength: degraded`；finish 返回 `completed: true`。

[公开调用记录](captured.json)保留 2026 年 10 月 10 日本地执行的完整输入和选定返回字段，省略较长的方法正文、重复的提示读取、本机路径与详细检查。其余字段直接来自服务返回；重跑时运行 ID 和时间戳可能变化。

需要在提交前阅读实际评审任务时，加 `--pause-before-review`，阅读 `review-request.json` 后用同一 `--output` 和 `--resume` 继续。随附评审仅适用于未变更的示例报告与来源；脚本核对输入哈希，拒绝对改过的示例文件重放该评审。[录屏说明](../../docs/assets/mcp-demo.zh-CN.md)。
