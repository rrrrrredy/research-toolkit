# DSH adapter maintenance checks

[English](dsh-adapter-validation.md) | [简体中文](dsh-adapter-validation.zh-CN.md)

These are existing adapter-maintenance commands, moved from the host installation card. They are not required steps for a research task. [Installation and native collaboration](../agents/deepseek-harness.md).

## Verify The Adapter

The offline lane checks frontmatter compatibility, referenced resources, and the staged DSH directory contract:

```bash
python scripts/run_dsh_evals.py validate
```

The smoke lane launches the real DSH CLI with the `headless` profile against a local scripted endpoint. It checks the advertised `skill` tool and catalog entry, sends a scripted tool-call request, and looks for configured Skill-body markers in messages sent to that endpoint. It also checks process exit and a scripted success marker. The check does not compare the complete body or independently validate every tool result. It uses a placeholder key and makes no live model call:

```bash
python scripts/run_dsh_evals.py smoke
```

The smoke child receives only allowlisted runtime discovery, home/cache, locale and temporary-directory variables, plus the local endpoint and placeholder key. Service secrets and runtime injection settings such as `NODE_OPTIONS` are not inherited. This limits environment forwarding; it does not sandbox the selected executable or prevent access to files. The live lane retains its separately configured model credentials.

The live lane uses the model and credentials already configured for DSH, stages one existing repository eval case, runs it through DSH headless, and scores the resulting artifacts with the same deterministic evaluator used by other agents:

```bash
python scripts/run_dsh_evals.py live --case source_instruction_boundary_zh
```

Both runtime lanes accept `--dsh-command-json` or `DSH_EVAL_COMMAND_JSON` for an explicit argv. Otherwise the runner selects `dsh` from `PATH`, then falls back to the pinned `@deepseek-ai/dsh@0.1.2-rc.1` package through `npx`. This pin describes the runner fallback, not the latest upstream release. Check the selected package's Node.js requirements locally.

The live lane returns non-zero for both `review` and `fail`. Use `--allow-review` only for exploratory collection. Keep credentials out of command JSON, prompts and committed reports.

Reports and captured stdout/stderr are written under `evals/runs/dsh/`, which is ignored by Git.
