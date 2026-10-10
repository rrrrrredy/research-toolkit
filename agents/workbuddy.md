# WorkBuddy: first Lite task

[English](workbuddy.md) | [简体中文](workbuddy.zh-CN.md)

Use WorkBuddy with access to a local folder. Its [official product page](https://cloud.tencent.com/product/workbuddy) describes local file reading; no native Skill installation is needed for this route.

## Make the files available

In the working folder, run:

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git research-toolkit
```

Open that working folder in WorkBuddy and send:

```text
Read research-toolkit/SKILL.md and use profile=lite.
Read research-toolkit/examples/lite/start.en.json and
research-toolkit/examples/lite/sources.md. Complete that fictional
helpdesk comparison with a short report, separate sources/claims
records and all six Lite checklist items. Save outputs in a separate
task folder. Disclose the fictional evidence and no independent review.
```

Allow about 5–15 minutes; expect 350–500 words plus records. [Complete walkthrough](../docs/quickstart-lite.md).

## If it cannot read the files

Run from the working folder:

```bash
git -C research-toolkit status --short
```

A path error means the folder or clone is missing; no output means a clean checkout. Confirm WorkBuddy has access to this same folder.

For repeated use, WorkBuddy also provides **Skills → Add Skill → Upload Skill** and an enable switch. Follow its [official import instructions](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) and the formats accepted by your client. This guide does not assume the toolkit has a marketplace listing or that a GitHub ZIP is an accepted skill package.
