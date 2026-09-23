# Codex Skill Installation

[English](codex.md) | [简体中文](codex.zh-CN.md)

For an installation that bundles the Skill with executable review and delivery tools, use the [plugin or standalone MCP guide](../docs/usage-modes.md). This page covers Skill-only installation.

Use the `research-toolkit` Skill in a Codex environment that can read local files. Git is needed to clone the repository; Python is needed for the checking scripts. Keep the complete checkout so that references, scripts, and documentation remain available.

## Install as a native Skill

From the root of the project where you will do the research, run:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git .agents/skills/research-toolkit
```

The entry point is `.agents/skills/research-toolkit/SKILL.md`. For a user-level installation shared across projects, use `<user-home>/.agents/skills/research-toolkit` as the destination. These locations follow the [official Skill discovery documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

If the destination already contains a copy, follow the update instructions below before changing it.

## Verify and invoke

1. Open Codex in the research project. In the CLI or IDE extension, use `/skills` or the `$` selector to find `research-toolkit`.
2. Select it and ask Codex to read the full instructions and the references needed for the task. If multiple copies exist, confirm the actual path used.
3. If the new or updated Skill is absent, restart Codex and check again.

Example invocation in the CLI or IDE extension:

```text
$research-toolkit
Compare three enterprise knowledge-search products for an IT procurement team.
Cover source coverage, permissions, deployment, pricing, and adoption risks.
Deliver a comparison report with a recommendation, sources, and uncertainties.
Clarify missing requirements and agree on an outline before research.
```

The [official usage guide](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills) explains explicit selection and automatic matching. Discovery confirms that the Skill is available; report quality still requires content review.

## Use files without native installation

You can keep a complete checkout in an ordinary local folder:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git agent-skills/research-toolkit
```

Then tell Codex:

```text
Use the Research Toolkit in agent-skills/research-toolkit for this task.
Read SKILL.md first and load references as needed.
Keep research records, drafts, and reports in a separate task folder.
```

This explicitly loads the files. The ordinary `agent-skills/` folder is not one of the native discovery locations above.

## Update a native installation

Inspect the installed checkout from the research project root:

```bash
git -C .agents/skills/research-toolkit status --short
```

Preserve local changes before updating. For a clean checkout following the repository's main branch:

```bash
git -C .agents/skills/research-toolkit pull --ff-only
```

Then repeat the discovery check. For a user-level installation, substitute its actual path. For pinned versions or modified copies, follow [installation identity and updates](../docs/installation-versioning.md).

## Research files and delivery checks

Keep `state/`, `logs/`, `data/`, drafts, and reports in a separate research task folder. Resume from the task specification, progress, findings, and previously explored directions. Preserve material follow-up requirements in `state/requirements.jsonl`.

Before final delivery, save the intended completion message to `delivery_message.md` in that task folder. For the project-local installation above, run this from the project root and replace the task-directory placeholder:

```bash
python .agents/skills/research-toolkit/scripts/check_delivery.py <task-directory>
```

For another installation location, use the checker's actual path. It imports `scripts/check_review_completion.py`; keep both. See [delivery verification](../docs/delivery-verification.md) and [review completion](../docs/review-completion.md) for record formats.

Complete required content reviews as well as file checks. If a required check cannot run or does not pass, deliver a clearly labeled stage artifact or resolve the outstanding work before claiming final completion.
