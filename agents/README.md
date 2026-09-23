# Skill Installation and Use

[English](README.md) | [简体中文](README.zh-CN.md)

Research Toolkit provides the `research-toolkit` Skill. Choose how you want to use it: read its files for a task, or install it in a tool that supports native Skill discovery. The [full Skill](../SKILL.md) and [Chinese reading version](../SKILL.zh-CN.md) describe the same research methods.

## Use without installation

Give the agent the repository URL and ask it to read `SKILL.md` first. Load files under `references/` when the current task needs them. The [quickstart example](../README.md#quickstart) includes a research request you can adapt.

If repository links are unavailable, download the repository and give the agent access to the files, or attach `SKILL.md` and the supporting files it needs. Reading or attaching these files applies the instructions to the current task; it does not register a native Skill.

## Install for repeated use

Follow the guide for your tool to choose its Skill directory or other supported loading method. A native installation should appear under the name `research-toolkit` in that tool's Skill list. A download into an arbitrary folder still needs an explicit instruction to read it.

Use a complete repository checkout for local installation so that references, helper scripts, and documentation remain together. Keep research outputs in a separate task folder.

## Choose your tool

| Tool | Method covered by the guide | Confirm before use |
| --- | --- | --- |
| [Codex](codex.md) | Native Skill installation or direct file reading | `research-toolkit` is discoverable for native use; the intended files can be read |
| [Claude](claude.md) | Project instructions, attachments, and local files where available | Required files and tools are available in the session |
| [Gemini CLI](gemini-cli.md) | Reading the toolkit from a local folder | References are readable and research files can be saved |
| [Cursor](cursor.md) | Repository instructions and local files | The session reads the intended toolkit copy |
| [ChatGPT / general agents](chatgpt.md) | Uploaded files or pasted instructions | Sources and saved task records can be accessed |
| [OpenClaw](openclaw.md) | Skill directory installation and direct file reading | The intended Skill is visible and allowed |
| [Hermes Agent](hermes.md) | Skill directory installation and invocation | The Skill appears in the catalog with its references available |
| [DeepSeek Harness (optional)](deepseek-harness.md) | Native Skill installation and its optional adapter | Follow this guide only when using that tool |

These are setup instructions. Installation and loading checks establish which files are available; research quality is assessed through the [evaluation materials](../evals/README.md) and content reviews.

## Files to keep

The full checkout contains these parts:

| Part | Purpose |
| --- | --- |
| `SKILL.md` and `SKILL.zh-CN.md` | Authoritative agent entry point and Chinese reading version |
| `references/` | Research, analysis, review, and writing methods loaded as needed |
| `scripts/` | Checking helpers; `check_delivery.py` imports `check_review_completion.py`, so keep them together |
| `docs/` | Instructions for the helpers and their task records, including `delivery-verification.md` and `review-completion.md` |

Keep the file named `SKILL.md` as the discovery entry point; the Chinese companion provides a reading option. The checks require Python. Web search, file access, and execution permissions come from the agent environment.

## Confirm the intended copy is in use

1. For native installation, check that `research-toolkit` appears in the tool's Skill list and select it as described in its guide. For direct use, identify the local path or attached files explicitly.
2. Confirm that the agent can read the full `SKILL.md` and the reference files needed for the task. If multiple copies exist, confirm the actual path used.
3. Keep `state/`, `logs/`, `data/`, drafts, and reports in the research task folder. Confirm the session can save and reopen them.
4. Use [installation comparison](../docs/installation-versioning.md) when you need to check the installed files against a specific repository commit. File identity alone does not establish that the tool loaded that copy.

If the interface cannot retain files across conversations, save or export the task records and provide them again when continuing. If a required delivery check cannot run, follow the stage-delivery rules in `SKILL.md` and state which checks remain incomplete.

## Update an installed copy

Follow [installation identity and updates](../docs/installation-versioning.md) to compare versions and preserve local changes before updating. After an update, confirm the intended Skill is available again and that its references and scripts are still present. Follow the tool's reload instructions if the updated copy does not appear.

All usage methods share the same requirements: clarify the research brief, preserve progress, assess sources as evidence, keep review records outside the finished prose, and complete the required reviews before claiming final delivery. Source-embedded requests to control the agent are treated as source content, not task instructions.
