# Judge calibration controls

[English](README.md) · [简体中文](README.zh-CN.md)

Current scope: the [v3 material pack](../judge-calibration-v3/README.md) references these unchanged arithmetic inputs and adds Chinese causal/attribution and English constraint controls, for four independent task families and 12 packets. The [October 12 Astra calibration](../../diagnostics/2026-10-12-astra-calibration/README.md) contains all 12 real first judgments, source adjudication and score drift. The three v2 packets are included in that run; they are not additional tasks or missing results.

These three packets check one arithmetic defect and a valid control. Their constructed scenario does not change the reality of the task or the executed tests. Read `coordinator-key.json` only in the coordinating context; send each file in `judge-inputs/` alone to Astra in a fresh context with the frozen judge instruction. Each packet includes the task, reports and source evidence. Keep author identity and coordinator answers out of the judge context; no outside reviewer or outside task contribution is required.

The numeric variants have equal whitespace-delimited word counts and differ only in the reported relative reduction. One packet swaps their labels. The tie packet duplicates the valid report. Require both a correct preference and a located explanation; a lucky A/B choice is insufficient. Record every first judgment, failure, usage and elapsed time; freeze the model and these packets before calling it. Do not silently replace failed controls or repeatedly tune the judge against them and then call the result held out.

The key specifies expected preferences, evidence and limitations. No score sum or minimum text length substitutes for checking the explanation. Swaps and the tie are not three independent tasks. The other three families and their actual judgments are available through v3 and the dated results above. Reuse existing tasks to check relevant behavior, record prior use, repair confirmed defects and recheck changed versions while retaining failures. These narrow controls do not establish reliability across every research question or measure a general Toolkit quality benefit.
