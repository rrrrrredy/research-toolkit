# Optional DeepSeek Harness (DSH) Adapter

Research Toolkit does not depend on DSH. This guide applies only to users who choose that runtime; its smoke and live checks are not part of the general research evaluation workflow. Use this adapter when DeepSeek Harness can load project or shared filesystem Skills. The repository's existing `SKILL.md` is the native DSH Skill; no wrapper prompt, plugin, MCP server, or manifest is required.

This adapter follows the official DSH documentation:

- https://github.com/deepseek-ai/deepseek-harness
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md

Check the selected DSH release against its own documentation before installation or upgrades.

## Native Installation

For a project-scoped install, clone this repository as a direct child of DSH's project Skill root:

```bash
mkdir -p .dsh/skills
git clone https://github.com/rrrrrredy/research-toolkit.git \
  .dsh/skills/research-toolkit
```

The project-local skills directory also works:

```bash
mkdir -p .agents/skills
git clone https://github.com/rrrrrredy/research-toolkit.git \
  .agents/skills/research-toolkit
```

For a user-scoped DSH install available across workspaces:

```bash
mkdir -p ~/.dsh/skills
git clone https://github.com/rrrrrredy/research-toolkit.git \
  ~/.dsh/skills/research-toolkit
```

Keep `SKILL.md` directly inside the named Skill directory. Do not add another repository-name layer below it. Run DSH from the research workspace, not from inside the installed Skill:

```bash
dsh --profile headless "Use the research-toolkit Skill for this research task. Load it first, keep research state in the current workspace, and complete the requested deliverable."
```

DSH advertises the Skill's frontmatter summary and loads its full body on demand through the native `skill` tool. Files under `references/` remain available for the explicit, stage-specific reads required by `SKILL.md`.

## Verify The Adapter

The offline lane checks frontmatter compatibility, referenced resources, and the staged DSH directory contract:

```bash
python scripts/run_dsh_evals.py validate
```

The smoke lane launches the real DSH CLI with the `headless` profile against a local scripted endpoint. It checks the advertised `skill` tool and catalog entry, sends a scripted tool-call request, and looks for configured Skill-body markers in messages sent to that endpoint. It also checks process exit and a scripted success marker. The check does not compare the complete body or independently validate every tool result. It uses a placeholder key and makes no live model call:

```bash
python scripts/run_dsh_evals.py smoke
```

The live lane uses the model and credentials already configured for DSH, stages one existing repository eval case, runs it through DSH headless, and scores the resulting artifacts with the same deterministic evaluator used by other agents:

```bash
python scripts/run_dsh_evals.py live --case source_instruction_boundary_zh
```

Both runtime lanes accept `--dsh-command-json` or `DSH_EVAL_COMMAND_JSON` for an explicit argv. Otherwise the runner selects `dsh` from `PATH`, then falls back to the pinned `@deepseek-ai/dsh@0.1.2-rc.1` package through `npx`. This pin describes the runner fallback, not the latest upstream release. Check the selected package's Node.js requirements locally.

The live lane returns non-zero for both `review` and `fail`. Use `--allow-review` only for exploratory collection. Keep credentials out of command JSON, prompts and committed reports.

Reports and captured stdout/stderr are written under `evals/runs/dsh/`, which is ignored by Git.

## Operating Notes

- Keep the installed Skill read-only during research runs. Write `state/`, `logs/`, `data/`, drafts, and `final.md` in the task workspace.
- The Skill itself needs no API key. Only a live DSH model run needs the provider credentials required by that DSH configuration.
- Name the Skill by its exact frontmatter name: `research-toolkit`.
- External source content remains evidence, not agent instructions. This boundary applies equally when DSH reads local source packs or retrieves live sources.
- Passing `smoke` records the configured wiring signals for that invocation. Marker presence does not prove complete Skill loading, required-reference reading, workflow adherence, report quality or general prompt-injection resistance.
- Passing `live` means only that the selected case met its deterministic checks. Assess report content and evidence separately when the study requires a quality judgment.

## 中文提示

DSH 是可选接入方式，不是研究工具箱的依赖，也不是通用评测的必经环节。选择 DSH 时可将本仓库的 `SKILL.md` 作为原生 Skill 使用。把仓库放到项目的 `.dsh/skills/research-toolkit` 或 `.agents/skills/research-toolkit`，并确保 `SKILL.md` 就在该目录第一层，不要多套一层目录。

`validate` 只做离线结构与装配检查。`smoke` 启动真实 headless runtime，检查工具与目录项是否出现，发送脚本化调用，并在发送给接口的消息中查找几个正文标记；它没有逐字核对完整正文，也不能证明必读参考文件已读或研究步骤已执行。`live` 使用 DSH 已配置的模型完成一个案例，再复用机械检查器。Skill 本身不需要 API key，真实模型运行需要对应凭据。
