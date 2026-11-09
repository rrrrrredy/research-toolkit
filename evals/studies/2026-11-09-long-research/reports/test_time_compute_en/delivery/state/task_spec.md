# Research brief

## question

Investigate how additional computation at inference time changes the capabilities, reliability, and economics of reasoning models and agents. The reader needs to decide which strategies to use, how to allocate a finite budget, and when extra computation is unlikely to help. Focus on work published from 2022 through the evidence cutoff of 2026-11-09, using earlier work where needed to explain foundations. Use only evidence publicly available by the cutoff and identify the relevant paper, model, implementation, and evaluation versions. Do not turn later knowledge into evidence available at the cutoff.

Develop a mechanism-based comparison of independent sampling, self-consistency, best-of-N selection, sequential revision, search over intermediate states, outcome and process verification, adaptive budget allocation, and agent loops involving tools or environmental feedback. Explain what generates candidates, what selects or rejects them, what state is retained, and what information the evaluator can access. Distinguish inference-time allocation from training changes that enable it. Separate results for a fixed base model from comparisons in which model size, post-training, data, or the verifier also changes.

Examine evidence from mathematical reasoning, executable coding tasks, and multi-step tool-using tasks. Select informative studies rather than attempting an exhaustive paper catalogue. Compare scaling behavior, marginal gains, saturation, regressions, and variation with task difficulty. Explain how correlated errors, weak or miscalibrated verifiers, reward exploitation, unreliable tools, compounding action errors, or unavailable feedback can change the apparent benefit of additional search. Assess whether results on tasks with cheap, reliable checking transfer to tasks with ambiguous outcomes or delayed feedback.

Build a budget-aware comparison framework. Account for candidate generation, discarded branches, verifier calls, hidden or explicit reasoning tokens when disclosed, tool execution, and retries. Distinguish total compute or monetary cost from serial latency, parallel resource demand, and end-to-end wall-clock time. Token counts alone are not a common compute unit across different models. Where published studies permit a defensible normalization, show it with units and assumptions; otherwise retain separate comparisons and explain the missing information. Include a worked allocation example using reported values or clearly labeled hypothetical inputs, without presenting an illustrative calculation as a new experiment.

Deliver a complete research report with a method-and-evidence matrix, a comparison of reported scaling behavior, and a design decision tree covering task verifiability, error consequences, latency constraints, tool availability, and budget. Explain how a designer should choose among a stronger base model, more samples, deeper search, better verification, or a simpler execution path. Distinguish empirical findings from proposed policies, and include cases in which no additional inference-time computation is the defensible choice. Tables and diagrams may be integrated into any coherent report structure; a literature list or brief recommendation sheet is not sufficient.

The central checks are whether budget comparisons include the computation used to select answers, whether training and inference effects remain distinguishable, and whether the proposed design choices follow from task-specific evidence. Report benchmark contamination, test-selection effects, evaluator leakage, and missing uncertainty estimates when they materially affect a claim. Publicly reported results need not be rerun, but they must not be described as independently reproduced unless they actually were. No particular scaling law or conclusion about the superiority of test-time compute is assumed.

## audience

Model researchers, inference engineers, and agent-system designers making compute-allocation decisions

## scope

Follow the task geography, comparison scope and evidence cutoff of 2026-11-09. Each other-language version uses its frozen sources without seeing the first-language report.

## output

Complete long-form research report final.md with the task-specific comparisons, explanations, tables and locatable citations. Preserve the first draft and actual independent results.

## depth

A full technical research report connecting mechanisms, budget-aware empirical comparisons, scaling limits, and implementable design choices across reasoning and agent workloads.

## evidence_standard

Use original public sources with actual dates, reading evidence and retained originals. Conduct seven separate independent content perspectives, relevant domain review, independent audit and final acceptance. Live primary research
