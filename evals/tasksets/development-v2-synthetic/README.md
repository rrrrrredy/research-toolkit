# Five independent test tasks

[English](README.md) · [简体中文](README.zh-CN.md)

These five tasks were created on 2026-10-12 and used in the [actual four-model test](../../studies/2026-10-12-lite-four-models/README.md). They are independent tasks defined by distinct research questions; development use or prior access does not invalidate them. Source text is retained as supplied in each task.

| Task | Language | Necessary judgment |
| --- | --- | --- |
| `wash-water-en` | English | Reconcile litres/cubic metres, totals/intensity and rollout limits |
| `archive-scan-zh` | Chinese | Reconcile different populations and jointly enforce accuracy/throughput |
| `library-reminders-en` | English | Separate group differences, changes and causal identification |
| `backup-budget-zh` | Chinese | Enforce first-year hard constraints and future capacity conditions |
| `ferry-timeline-en` | English | Distinguish superseded targets, conditional plans and current status |

Each folder supplies a reader brief, two complete supplied sources and a coordinator-only design record with provenance, rationale, expected judgments, exclusions and exposure. The five families are different from the October 10 battery, AI risk, banking, memory and productivity tasks; they still share broad research skills. This purposive set is not a representative population sample. Three English and two Chinese tasks are native scenarios, not translations counted twice.

`study.json` contains inspectable placeholders and enables position swaps: at most 10 author requests and 10 judge requests per author model. Preparing it freezes an offline inspection plan; verify and replace provider settings before freezing any real execution plan. No credentials belong here. This input directory stores no outputs; the linked dated test retains the actual responses and results. The separate [judge controls](../judge-calibration-v3/README.md) do not count as a sixth development family.

Reuse these independent tasks for diagnosis and regression checks. Add new tasks when they cover a different question or a specific gap. Record prior use accurately; neither outside authorship nor a new held-out set is a prerequisite for repairs.
