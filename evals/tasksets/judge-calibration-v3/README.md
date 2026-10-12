# Bilingual judge calibration controls

[English](README.md) · [简体中文](README.zh-CN.md)

Four fictional development families supply 12 judge packets: one valid/defective pair, its exact A/B reversal and an identical-valid tie per family. The [dated Astra calibration](../../diagnostics/2026-10-12-astra-calibration/README.md) now retains all 12 first judgments, source adjudication and score drift; the input controls remain unchanged. These public, implementation-authored controls are separate from the five development tasks and from any future held-out study. Version 3 names this material pack; it does not change protocol v2 or study schema 2.

| Family | Known defect | Length of each variant | Primary valid label |
| --- | --- | --- | --- |
| `cal-relative-rate-en` | Confuses percentage-point and relative reductions | 48 whitespace-delimited words | A |
| `cal-causal-zh` | Claims an identified lighting effect despite confounded greenhouse observations | 148 nonwhitespace characters | B |
| `cal-attribution-zh` | Turns a supplier's claim into independently verified evidence | 134 nonwhitespace characters | A |
| `cal-constraints-en` | Selects an option that violates the mandatory first-year budget | 65 whitespace-delimited words | B |

The arithmetic family references the three unchanged [v2 packets](../judge-calibration-v2/README.md). Nine new packets add causal, attribution and decision-constraint checks. Each defective report changes one decisive phrase in its valid partner. Chinese counts include punctuation, digits and citation markers and count Unicode code points except whitespace; they are not token counts. English uses Python whitespace splitting, including citation markers. Equal counts reduce one presentation difference but do not eliminate stylistic, position or model biases. No report length threshold or dimension sum certifies correctness.

## Coordinator-only material

`coordinator-manifest.json` records each packet path/hash, expected preference, located report/source excerpts, rationale, counts and exposure. Paths are relative to `evals/tasksets/`, so the three v2 originals need not be copied. Hashes use parsed JSON serialized with sorted keys, compact separators, `ensure_ascii=false`, UTF-8, then SHA-256. Formatting and checkout line endings do not change this identity; report strings and other JSON values do. This is not a raw-file-byte hash or an external commitment against someone changing both packet and manifest.

The coordinator checks expectations against the supplied sources. They remain authored hypotheses subject to evidence review. Only an individual referenced packet, together with a separately frozen judge system instruction, goes to a fresh judge context. Keep this README, the manifest, filenames/family IDs, other packets, the repository and the design conversation inaccessible to that context. Packets contain only `brief`, `sources`, `rubric` and `reports`; structural checks reject additional metadata fields but cannot prove prose contains no clues. The checker does not launch a judge or enforce context isolation.

## Before live collection

Freeze the manifest, all referenced packets, judge system instruction (the pilot's `JUDGE_SYSTEM`), requested/accepted model IDs, limits, response protocol and collection order before calls. Freeze the ordering/seed separately; never present all three variants in one context. Retain every first judgment, raw reply, parse/identity failure, usage and elapsed time. Do not retry failed controls or choose a favorable orientation. The five-call connectivity phase in the [improvement plan](../../../docs/improvement-plan.md) is separate: **this pack requires 12 additional judge requests per model**, no author generation, under its own frozen call budget. The separate [native judge guide](../../../docs/native-judge.md) supplies the adapter and dated settings; this packet directory contains inputs only.

Check the preference **and** its located explanation against the sources. Require identification of the known defect in both orientations and no invented substantive difference between identical valid reports. Record unresolved judgments, misses, false alarms and source-based adjudication separately. Neither a lucky A/B choice nor model agreement is sufficient. Passing these narrow controls does not validate all five rubric dimensions, establish general judge reliability or show Toolkit efficacy. Four families are not 12 independent observations; reuse, translations and repeated models do not add families. If these public controls inform tuning, later checks of generalization need new independently designed material and explicit exposure records. Human review is not an added prerequisite.

## Offline checks

```bash
python scripts/check_judge_calibration.py --self-test
```

Run from the repository root. The read-only checker verifies hashes, shared inputs, exact reversals, ties, language-specific counts and excerpt locations. Its corruption controls run on temporary copies. It makes zero model calls and reports judge reliability as `not_evaluated`; it cannot establish semantic validity, independent task design or successful blinding.
