# Research brief

## question

Investigate when an automated feedback loop produces a verifiable improvement in a model or software system, and what evidence is needed before calling the result self-improvement. Use DGM and AlphaEvolve as entry points for comparing different mechanisms, not as proof that they belong to one category or achieve unrestricted recursive improvement. Focus on public work from 2023 through the evidence cutoff of 2026-11-09, with earlier foundations where useful. Identify the versions of papers, code, tasks, and reported results used, and exclude information first made public after the cutoff.

Define the object being changed: model weights, source code, prompts, tool policies, or a larger workflow. Distinguish an external optimizer improving a target program from an agent modifying components of its own operating system, and distinguish temporary inference-time adaptation from a retained system change. Select complementary examples where they clarify these boundaries, rather than constructing an exhaustive list of systems advertised as self-improving.

Reconstruct each principal improvement loop in enough detail to identify the candidate generator, editable state, evaluator, selection rule, retained history, and deployment or rollback decision. Explain where human-designed objectives, test suites, search spaces, constraints, manual repairs, or candidate filtering enter the loop. Compare the cost and role of generating candidates with the cost of evaluating them. Separate gains attributable to additional search or stronger external models from evidence that the modified system itself has become better.

Examine evaluator validity and failure modes. Address adaptive overfitting to reused tests, multiple candidate selection, data leakage, reward exploitation, incorrect reference answers, and changes that improve one metric while breaking another required property. For program optimization, investigate functional equivalence, correctness coverage, and hardware or workload dependence. For agents or learned systems, distinguish optimization tasks from genuinely held-out tasks, environments, or task families. Explain whether an apparent gain persists outside the evaluator used to select the candidate, and whether the public evidence can support that conclusion at all.

Build an evidence comparison that retains baseline identity, modification type, optimization budget when disclosed, evaluation conditions, human intervention, and the scope of measured generalization. Analyze representative improvement claims and negative or limiting evidence in depth. Missing compute or intervention information should narrow a comparison rather than be replaced with guessed values. Public documentation and existing replications can support the report; running a new self-modifying system is not required, and an implementation description must not be presented as an independent reproduction.

Deliver a complete report with reconstructed loop diagrams or equivalent tables, a comparative evidence matrix, and conditional adoption guidance. Explain which objectives are sufficiently checkable for bounded automated improvement, when a separate evaluator or protected holdout is essential, and when preserving the original system or requiring human review is the better choice. These are design conclusions for the reader, not a requirement to introduce a new evaluation process for this research task.

The key checks are whether the claimed improvement has a defined target and baseline, whether selection feedback is separated from independent evidence of generalization, and whether human and external-model contributions remain visible. A system may demonstrate useful program optimization without demonstrating general self-improvement. Equally, limited or negative evidence should not erase well-supported gains within a narrow domain. Allow the conclusions to follow the evidence rather than a predetermined claim about recursive progress.

## audience

Research and engineering leaders evaluating automated improvement systems and their deployment boundaries

## scope

Follow the task geography, comparison scope and evidence cutoff of 2026-11-09. Each other-language version uses its frozen sources without seeing the first-language report.

## output

Complete long-form research report final.md with the task-specific comparisons, explanations, tables and locatable citations. Preserve the first draft and actual independent results.

## depth

A mechanism-level research report that reconstructs improvement loops, examines evaluator validity and generalization, and separates measured gains from broader autonomy claims.

## evidence_standard

Use original public sources with actual dates, reading evidence and retained originals. Conduct seven separate independent content perspectives, relevant domain review, independent audit and final acceptance. Live primary research
