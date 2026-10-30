# Optional DeepSeek Harness (DSH) Adapter

[English](deepseek-harness.md) | [简体中文](deepseek-harness.zh-CN.md)

Research Toolkit does not depend on DSH. This guide applies only to users who choose that runtime; Use this adapter when DeepSeek Harness can load project or shared filesystem Skills. The repository's existing `SKILL.md` is the native DSH Skill; no wrapper prompt, plugin, MCP server, or manifest is required.

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

## Research and native collaboration

Use DSH's existing agent and subagent execution to carry the shared research method. The lead provides the current question, effective requirements, outline and relevant original files. Research workers return full analysis or local drafts; one designated agent integrates the main report. Separate independent agents carry the content-review perspectives, domain review, audit and final acceptance described in the [role methods](../references/subagents-and-review-loop.md).

Keep the installed Skill read-only. Research artifacts and retained handoffs belong in the research workspace; fixed tool registries apply only when using CLI/MCP management. Summaries locate original results and sources rather than replacing them. DSH supplies execution, waiting, messaging and cancellation; Toolkit organizes the research inputs, methods and outputs.

## Adapter maintenance

[Existing validate, smoke and live checks](../docs/dsh-adapter-validation.md) are for maintainers diagnosing the adapter. They do not run during ordinary research. Source content remains evidence rather than instructions.
