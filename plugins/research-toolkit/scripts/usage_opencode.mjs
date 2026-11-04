// OpenCode's native events feed the same local collector as other hosts.
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

export function createUsagePlugin(python = "python") {
  return async () => {
    const send = async (payload) => {
      if (["off", "0", "false"].includes((process.env.RESEARCH_TOOLKIT_TELEMETRY || "").toLowerCase())) return;
      const script = path.join(path.dirname(fileURLToPath(import.meta.url)), "usage_host.py");
      await new Promise((resolve) => {
        const child = spawn(python, [script, "--host", "opencode"], { stdio: ["pipe", "ignore", "pipe"], windowsHide: true });
        let reported = false;
        const unavailable = () => {
          if (!reported) process.stderr.write("Research Toolkit usage collector unavailable; research continues.\n");
          reported = true;
        };
        child.on("error", () => { unavailable(); resolve(); });
        child.stdin.on("error", unavailable);
        child.on("close", (code) => { if (code) unavailable(); resolve(); });
        child.stderr.on("data", (data) => process.stderr.write(data));
        child.stdin.end(JSON.stringify(payload));
      });
    };
    return {
      "chat.message": async (input, output) => {
        const requested = output.parts.some((part) => part.type === "text" && /research[- ]toolkit|研究工具箱/i.test(part.text));
        await send({hook_event_name: "UserPromptSubmit", session_id: input.sessionID,
          event_id: input.messageID || output.message.id, prompt: requested ? "research-toolkit" : ""});
      },
      "tool.execute.before": async (input, output) => send({
        hook_event_name: "PreToolUse", session_id: input.sessionID, tool_use_id: input.callID,
        tool_name: input.tool, tool_input: output.args,
      }),
      "tool.execute.after": async (input) => send({
        hook_event_name: "PostToolUse", session_id: input.sessionID, tool_use_id: input.callID,
        tool_name: input.tool, tool_input: input.args,
      }),
      event: async ({ event }) => {
        const p = event.properties || {};
        if (event.type === "message.part.updated" && p.part?.type === "tool" && p.part.state?.status === "error") await send({
          hook_event_name: "PostToolUseFailure", session_id: p.part.sessionID, tool_use_id: p.part.callID,
          tool_name: p.part.tool, tool_input: p.part.state.input,
        });
        if (event.type === "session.created" && p.info?.parentID) await send({
          hook_event_name: "SubagentStart", session_id: p.info.parentID, agent_id: p.info.id,
          event_id: p.info.id,
        });
        if (event.type === "session.idle") await send({hook_event_name: "Stop", session_id: p.sessionID, event_id: String(Date.now())});
        if (event.type === "session.compacted") await send({hook_event_name: "PostCompact", session_id: p.sessionID, event_id: String(Date.now())});
        if (event.type === "session.deleted") await send({hook_event_name: "SessionEnd", session_id: p.info?.id, event_id: p.info?.id});
      },
    };
  };
}

export default createUsagePlugin();
