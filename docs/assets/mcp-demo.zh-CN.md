# 录制 MCP 工作流

[English](mcp-demo.md) · [简体中文](mcp-demo.zh-CN.md)

录屏占位：**待录制**。英文演示放在 `docs/assets/mcp-workflow.en.gif`（asciinema 可用 `.cast`），中文字幕版本放在 `docs/assets/mcp-workflow.zh-CN.gif` / `.cast`。当前没有录屏，不宣称已经提供。

1. 安装 MCP 依赖，打开[示例](../../examples/mcp/README.zh-CN.md)。使用随附虚构输入、干净的终端和仓库之外的输出目录。
2. 展示 `research_start → research_guide → research_review → research_finish`，包括来源／判断文件、自评提示、第二次提交和降级标记。保留中间的 status 调用，或在字幕中说明。
3. 终端录制可执行 `asciinema rec mcp-workflow.zh-CN.cast`，再运行 `python examples/mcp/capture.py --output ../mcp-recording-run`，查看 `transcript.json`、评审记录与回执，最后退出录制。客户端 GIF 则在 MCP 客户端中录制相同的真实调用。
4. 隐去凭据、账户信息和个人文件路径，保留虚构数据与自评标记。可剪去等待，不拼接虚构的成功返回。
5. 导出较小的 GIF 或保留 `.cast`，增加可访问的说明文字，并同时把双语 README 占位链接替换成实际文件。录屏展示软件调用，不证明研究质量提升。
