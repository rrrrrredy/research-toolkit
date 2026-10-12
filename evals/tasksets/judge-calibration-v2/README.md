# Judge calibration controls

[English](README.md) · [简体中文](README.zh-CN.md)

2026-10-12 update: the [v3 material pack](../judge-calibration-v3/README.md) references these unchanged arithmetic inputs and adds Chinese causal/attribution and English constraint controls, for four families and 12 packets. The description below records the original v2 scope; its pending-design statement is superseded by that pack, which still has no live calibration results.

Three synthetic packets check one arithmetic defect and a valid control. They are separate from development tasks and have no real judge results yet. Read `coordinator-key.json` only in the coordinating context; send each file in `judge-inputs/` alone to a fresh judge with the frozen judge instruction. Do not give the judge this directory, the repository, this README or the key.

The numeric variants have equal whitespace-delimited word counts and differ only in the reported relative reduction. One packet swaps their labels. The tie packet duplicates the valid report. Require both a correct preference and a located explanation; a lucky A/B choice is insufficient. Record every first judgment, failure, usage and elapsed time; freeze the model and these packets before calling it. Do not silently replace failed controls or repeatedly tune the judge against them and then call the result held out.

The key specifies expected preferences, evidence and limitations. No score sum or minimum text length substitutes for checking the explanation. Swaps and the tie are not three independent tasks. One English arithmetic example does not calibrate all five dimensions: independent Chinese, causal, source-attribution and decision-constraint controls remain pending. These materials make calibration reviewable; they do not establish judge reliability or Toolkit efficacy.
