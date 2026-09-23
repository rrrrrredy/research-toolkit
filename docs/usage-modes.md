# Skill, plugin and MCP

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

**Use the plugin when your agent supports it. It bundles the Skill and MCP tools; you do not need three installations.** The Skill remains available for instruction-only use, and the same MCP server can be connected separately.

| Form | What it supplies | Choose it when |
| --- | --- | --- |
| Skill | Concise entry instructions and detailed methods loaded by research stage | Your tool loads Skills or files, or you only want the research methods |
| Plugin | An installable bundle containing the Skill, references and local MCP server | Your agent supports the plugin format and local tools |
| MCP | Five callable tools for task setup, stage guidance, effective reviews and delivery checks | Your agent supports local MCP but you are not installing the plugin |

All three use the same research standard. The plugin packages the shared scripts; MCP calls those scripts. Installing a second copy does not add another research method. Keep one intended Skill copy active.

## Install the plugin

The [plugin directory](../plugins/research-toolkit/) contains the portable manifest and Codex compatibility manifest. This is a repository-distributed local plugin, not a hosted service or a claim of listing in a public plugin directory.

For Codex, install Python 3.10 or later, Git and a current Codex CLI, then run:

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

The plugin launches MCP with `python`; that Python environment must contain the dependency. Restart/open a new agent session, select Research Toolkit, and confirm that the `research_start`, `research_status`, `research_guide`, `research_review` and `research_finish` tools are available. If MCP cannot start, check the Python executable and dependency in that environment.

Then make an ordinary research request:

> Use Research Toolkit to compare three enterprise knowledge-search products for our IT procurement team. Cover permissions, deployment, price and adoption risks. Deliver a Chinese comparison report with a recommendation and sources. Clarify missing requirements and agree on the outline before collecting evidence.

The agent assembles the brief from the conversation and asks only about missing critical requirements. Users should not have to maintain workflow files or inspect review logs themselves.

The portable manifest follows the [Agent Plugins specification](https://developers.openai.com/plugins/build/plugins). Other hosts must support that format and local stdio MCP; support for arbitrary plugin formats is not implied. The standalone MCP route below avoids maintaining a separate implementation for each host.

## Connect MCP separately

Skip this section if you installed the plugin and its tools are available.

Clone the repository, install its dependency in the Python environment your client will use, and connect the server:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git
cd research-toolkit
python -m pip install -r requirements-mcp.txt
```

A client using an `mcpServers` configuration can use the following example. Replace both executable/script paths and the research workspace with your actual paths; adapt the enclosing configuration to your client.

```json
{
  "mcpServers": {
    "research-toolkit": {
      "command": "/absolute/path/to/python",
      "args": ["/absolute/path/to/research-toolkit/scripts/research_mcp.py"],
      "env": {
        "RESEARCH_TOOLKIT_WORKSPACE": "/absolute/path/to/research-tasks"
      }
    }
  }
}
```

On Windows, forward-slash paths such as `D:/tools/python/python.exe` are valid JSON path strings. Research files are saved under the configured workspace. Without this setting, the server uses the plugin's data directory if available, otherwise `~/.research-toolkit/tasks`. Do not save research inside the installed package.

The server also exposes the `research` prompt and `research-toolkit://instructions` resource. Ask the agent to read the instructions before using the tools. Local stdio requires a client that can start a local process; a web-only client expecting a remote HTTPS server cannot connect directly.

## What happens during a task

| Tool | Action and completion boundary |
| --- | --- |
| `research_start` | Creates task records; returns missing question, audience, scope, output, depth and evidence requirements |
| `research_status` | Returns saved progress and current methods; changing to analysis/drafting requires prerequisite source/claim records |
| `research_guide` | Loads the applicable methods without starting a task; supports English and Chinese |
| `research_review` | Freezes full inputs, executes configured reviewers and a fresh auditor, preserves replies/failures, adjudicates findings and samples content |
| `research_finish` | Checks the reviewed artifact, current evidence, unresolved requirements and delivery text; writes completion state and a receipt only when checks pass |

The author agent still searches, reads, analyzes and writes, using its existing tools. It must save required source texts and source/claim records in the task directory. Stage guidance reduces repeated context loading; it does not establish that a model has obeyed every instruction.

Reviews require the full task, report and source files, not just URLs. The local input limit is 16 MiB; oversized input is rejected rather than silently truncated. This limit is not a promise that the configured model accepts a context of that size.

### Review accounts and recovery

The default executor uses an installed, signed-in **Codex CLI** with its configured model: one fresh reviewer context, followed by a separate auditor context. The auditor checks validity, consequential findings, sampled passed content and the whole report in the same assignment. No fixed four-provider panel is required.

**Review calls send the supplied task, report and evidence to the configured model service and consume its account usage.** The package includes no credentials or free model access. Use an account authorized for the material. Host-agent access to a model does not automatically supply the review subprocess with credentials.

Each reviewer must produce a substantive, version-bound reply with observable execution evidence. The auditor must also return a complete result. Invalid or interrupted work remains incomplete. The tool makes at most two reviewer attempts per slot per invocation; it retains failures and returns remaining work. Restore the underlying dependency, access, limit or response problem, then call the same assignment again. Completed reviews are reused; a failed auditor resumes without repeating the completed reviewer.

A valid negative review is complete. `reviews_complete` records review validity; `completion_check` separately reports whether the artifact is ready for its declared purpose. With `purpose: "evaluation"`, keep reports and defects unchanged; `evaluation_complete` is the endpoint. A changed reader-ready report is a separate, explicitly authorized `report_delivery` revision. The tools never rewrite reports to improve evaluation results.

A client must allow enough tool-call time for its configured reviews. Avoid concurrent clients or CLI writers for the same task. The MCP process rejects a second simultaneous modifying operation for a task; this is not a distributed scheduler.

### Configure another reviewer

The default needs no configuration file. To select models or multiple required reviewers, point `RESEARCH_TOOLKIT_REVIEW_CONFIG` to a trusted local JSON file when starting the server:

```json
{
  "reviewers": [
    {"id": "primary", "model": "codex-configured", "format": "codex-jsonl"}
  ],
  "auditor": {"id": "audit", "model": "codex-configured", "format": "codex-jsonl"}
}
```

Replace `codex-configured` with an available model identifier if needed. Every declared reviewer gets a separate context and a subsequent audit; use additional reviewers only when the task calls for them. Each executor has an optional `timeout_seconds` from 1 to 1800 (default 600).

For another provider, configure a trusted `command` argument list and `format: "json"`. The command receives one assignment JSON on stdin. It must actually call the chosen model, retain its original reply, and return this envelope on stdout:

```json
{"execution_id": "actual-provider-request-or-session-id", "content": "original model response text"}
```

Use a fresh execution context for every assignment. Read credentials from the provider's normal secure configuration; do not put secrets in the repository, task, command arguments or response. Commands are accepted only from trusted startup configuration, never model-generated MCP arguments. An adapter's own assertion is not independent proof of provider behavior; retain its original execution evidence.

## Skill only and CLI fallback

For Skill-only use, follow the [installation guide](../agents/README.md). The agent carries out the methods with its own capabilities; installing instructions alone does not start MCP or automatically run reviews.

The plugin also includes a dependency-free workflow CLI. It uses the same implementation; only starting MCP requires the SDK:

```bash
python scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

A brief request is `{"task":"comparison","language":"en","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`. Review arguments include `task`, task-relative `evidence_paths`, optional `artifact` (default `final.md`) and `purpose`. The `status`, `guide` and `finish` actions mirror MCP arguments. JSON may also be supplied through stdin.

## Verification and limits

The repository checks the shared workflow, package/source consistency and a real MCP stdio connection with **synthetic** reviewer subprocesses. Those tests do not call paid models or establish report quality. The implementation launches real configured model executors in normal use; a successful installation or test is not evidence that a particular research report has been reviewed.

The tools enforce their own completion conditions. They cannot prevent an agent from ignoring tools or editing files outside them, and they cannot mechanically certify factual truth. Independent content review and retained evidence remain part of acceptance.
