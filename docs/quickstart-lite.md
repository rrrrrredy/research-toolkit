# Your first Lite task in 5–15 minutes

[English](quickstart-lite.md) · [简体中文](quickstart-lite.zh-CN.md) · [Research Toolkit](../README.md)

Try a short comparison with two supplied sources. You need an agent that can read this repository; no reviewer account, API key, plugin or MCP setup is needed. Allow about 5–15 minutes with an agent ready to use; this is a walkthrough estimate, not a model latency guarantee. The [example package](../examples/lite/README.md) contains the complete brief and source notes.

## Give your agent this request

```text
Use Research Toolkit: https://github.com/rrrrrredy/research-toolkit
Read SKILL.md and use profile=lite.

Read examples/lite/start.en.json for the complete brief and
examples/lite/sources.md for the two fictional source notes.
Choose which helpdesk plan a six-person team should trial, within
a $35 monthly subscription ceiling, with weekly CSV exports that
may be manual. Write 350–500 words in English.

The brief is complete for a trial recommendation. Establish a short
outline, read the two notes, register the important claims, and draft
the note section by section. Use only the supplied sources.
Do not invent CSV fields, measured reliability or migration costs.
Keep citations readable and put task records outside the report.

Skip research_review and the Full delivery hard gates. Finish with
all six Lite checklist items and specific evidence for each.
Disclose the fictional evidence and absence of independent review.
If local workflow tools are available, use research_start and
research_finish (or their shared CLI); otherwise return the note,
source/claim records and checklist as separate chat sections and
state that no local delivery receipt was produced.
```

The expected output is a trial recommendation with cost arithmetic and conditions, not a purchase endorsement. An agent that cannot read GitHub needs a downloaded copy of `SKILL.md`, its relevant references, the [brief](../examples/lite/start.en.json) and the [source pack](../examples/lite/sources.md).

## What you receive

| Output | What to look for |
| --- | --- |
| Short report | A recommendation, six-seat cost comparison, counter-case and concrete trial checks. |
| Source and claim records | Each important fact points to the supplied note; recommendations and unknowns are explicit. |
| Final checklist | Requirements, claims/sources, counterevidence, sections, reader edit and limitations, each with a specific location or explanation. |

Lite does not commission a reviewer. Its checklist is an author check, not independent approval. A check that fails stays open; the agent must correct the problem before marking it passed. A syntactically complete checklist does not certify research quality.

<details>
<summary>Run the local workflow from a clone or fork</summary>

Use Python 3.10+ from the repository root; the shared CLI requires only the standard library. Store the task outside the checkout. An agent does the reading and writing; these commands do not generate a report.

```bash
python scripts/research_workflow.py start --profile lite --workspace ../research-work --request examples/lite/start.en.json
```

This creates `../research-work/helpdesk-lite`. The agent copies the source notes there, fills `data/source_registry.csv` and `data/claims_registry.csv`, saves the outline and section drafts, and writes `final.md`. Stage updates use the existing `status` action; see [CLI arguments](usage-modes.md).

Call `finish` with the task and delivery message to obtain the checklist, then save `finish.json` with `task`, `message` and a `checklist` object. Its six keys are `requirements`, `claims_and_sources`, `counterevidence`, `sections`, `reader_edit` and `limitations`. Each needs `passed: true` and an `evidence` string describing the actual check and its location.

```bash
python scripts/research_workflow.py finish --workspace ../research-work --request ../research-work/helpdesk-lite/finish.json
python scripts/check_delivery.py ../research-work/helpdesk-lite
```

A completed task has `final.md` and `state/final_checklist.json`, with `status: checklist_complete`, `independent_review: false` and explicit `SKIP` logs. It has no independent review record. If the report changes, check it again and submit an updated checklist.

</details>

For your own question, replace the brief and sources. Use [Full with the appropriate review tier](../SKILL.md#choosing-a-profile) when the decision, evidence volume or review requirement exceeds this small task. This fictional exercise is onboarding material, not an additional research benchmark.
