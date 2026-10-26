# WorkBuddy: use the complete research methods

[English](workbuddy.md) | [简体中文](workbuddy.zh-CN.md)

Use WorkBuddy with access to a local folder. Its [official product page](https://cloud.tencent.com/product/workbuddy) describes local file reading; no native Skill installation is needed for this route.

## Make the files available

In the working folder, run:

```bash
git clone --depth 1 -c core.longpaths=true https://github.com/rrrrrredy/research-toolkit.git research-toolkit
```

Open that working folder in WorkBuddy and send:

```text
Read the supplied research-toolkit/SKILL.md and load complete methods as needed.
Research question: [Question, audience and purpose.]
Scope and depth: [Coverage, information cutoff and length requirements.]
Existing material: [Sources or an existing report.]
Develop evidence, comparisons, explanations and synthesis. Deliver the complete
report with usable citations. Identify inaccessible required material without
inventing its contents.
```

Allow about 5–15 minutes; expect 350–500 words plus records. [Complete walkthrough](../docs/quickstart.md).

## If it cannot read the files

Run from the working folder:

```bash
git -C research-toolkit status --short
```

A path error means the folder or clone is missing; no output means a clean checkout. Confirm WorkBuddy has access to this same folder.

For repeated use, WorkBuddy also provides **Skills → Add Skill → Upload Skill** and an enable switch. Follow its [official import instructions](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) and the formats accepted by your client. This guide does not assume the toolkit has a marketplace listing or that a GitHub ZIP is an accepted skill package.
