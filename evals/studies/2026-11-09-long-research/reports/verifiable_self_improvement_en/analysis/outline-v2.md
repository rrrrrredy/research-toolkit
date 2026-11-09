# Verifiable self-improvement: where the reusable gain comes from

Producer: current Codex `/root`, continuing after the recorded Astra credit exhaustion. Evidence cutoff: 2026-11-09. Task authority: `evals/cases/verifiable_self_improvement_en.json` in the current worktree. This is an outline for independent requirements and structure review, not the finished report.

## Question and argument to investigate

When does an automated improvement loop leave behind a system that performs better on the work it is meant to do? Reconstruct the actual changed object, feedback, selection and retained artifact. Explain useful bounded successes positively, then identify which comparisons establish reuse beyond the optimization examples. Do not organize around an assumed takeoff, a company ranking or a blanket dismissal of self-improvement.

The tentative synthesis is that a strong improvement loop couples a useful search space with an informative evaluator and a retained artifact that transfers. The scarce element varies by setting: correct executable objectives in program search, genuinely different unseen tasks for harness changes, and training signals that preserve good answers while correcting bad ones in learned policies. Human and external-model work enters at specific points and should remain visible.

## Proposed complete report

1. **An improvement has an object.** Distinguish target-program optimization, self-editing agent code, retained prompts/workflow and model-weight training from temporary answer refinement. A compact comparison identifies what persists and what is fixed.
2. **DGM: a search through agent lineages.** Reconstruct diagnosis, self-edit, compilation, empirical task evaluation, archive admission and parent choice. Explain why preserving a temporarily weaker ancestor can help. Separate the adaptive SWE selection subset, full Polyglot results, cross-language, cross-benchmark and cross-model transfer. Read the public outer loop to identify the parts that do not themselves evolve.
3. **AlphaEvolve: constrain correctness and search for a better algorithm.** Reconstruct seed code, editable blocks, Gemini proposals, evaluation cascade, database and selection. Explain the differing validation of Borg ranking, kernel tiling, direct IR edits, circuit changes and mathematical constructions. Include the 2026 production update as dated company reporting, using linked detailed evidence only where needed for a consequential claim.
4. **Prompts, weights and workflows change different things.** Use Promptbreeder and SCoRe as complementary mechanisms, not an exhaustive catalog. Clarify feedback labels, whether the mutator changes, retained object, teacher/base model and task splits. HarnessPro supplies a more recent concrete case of trajectory-driven candidate design and held-out selection.
5. **Which evidence demonstrates reusable progress?** A comparison matrix retains baseline, task set, score definition, optimization/search exposure, final evaluation, intervention and public artifact. Contrast DGM transfer with the controlled 2026 harness-evolution study. Explain why extra attempts can improve a task without leaving a better general harness; relate the negative result to its actual scaffold and dataset rather than generalizing it to every improvement loop.
6. **The evaluator determines the useful search direction.** Develop information exposure and data leakage separately from adaptive test overfitting, reference errors, reward exploitation and metric conflicts. Compare what reaches the candidate generator or diagnoser, what is held back, and which results use new tasks. DGM Appendix C.3 explicitly supplies the private test patch to diagnosis; retain that access fact together with the authors' inspection and transfer evidence. Contrast it with HarnessPro's training/validation/test separation and SCoRe's training-only correctness oracle. Do not infer contamination solely from high performance. Distinguish correctness by construction, randomized testing, complete verification for a defined function, held-out workload performance and field deployment. Explain selection noise and the effects of changing hardware, model or workload.
7. **Adoption decisions.** Give conditional guidance for teams optimizing a kernel/heuristic, a reusable coding agent and a learned correction policy. Explain when the objective can drive automated search, what work remains with a separate evaluator or human decision maker, and what evidence justifies retaining or reverting a candidate. Compare candidate generation and evaluation effort when disclosed; missing totals do not become guessed break-even numbers.
8. **Evidence appendix.** Exact paper revisions and code snapshots, selected claim/condition records, source locations, calculations and unresolved source discrepancies. Keep the main narrative focused on mechanisms, comparisons and decisions.

## Substantive units and actual dependencies

| Unit | Research responsibility | Principal inputs | Dependency |
|---|---|---|---|
| V1 | Definitions and evaluation distinctions; establish the comparative questions | All principal papers; actual task | Outline review |
| V2 | DGM loop, code, empirical results and transfer | VSI001 v2, VSI005, DGM_outer.py and self-improve implementation | Outline; key facts independently checked before synthesis |
| V3 | AlphaEvolve loop, objective design and engineering outcomes | VSI002, VSI006–009, linked primary result as needed | Outline; independent technical premise check |
| V4 | Promptbreeder and SCoRe mechanism contrast | Official ICML Promptbreeder paper and TTC013 SCoRe paper | Outline |
| V5 | HarnessPro and controlled harness-evolution comparison | VSI003, VSI004 and frozen implementation | Outline; reconcile score definitions before comparison |
| V6 | Cross-case evaluator/generalization analysis and adoption guidance | V1–V5 analyses, counterevidence and calculations | The substantive upstream results |
| V7 | Complete manuscript, exhibits and first self-check | V1–V6, current question and full sources | Relevant upstream independent premise findings |

These units are contributions to one argument, not a mandatory one-unit/one-section template. Main producer integrates terminology and resolves cross-case conflicts. Final delivery uses the existing seven separate content perspectives, domain specialist, independent audit and acceptance; the unit checks do not replace them.

## Material already inspected and questions still open

- VSI001: read mechanism, setup, results, limits and relevant transfer/evaluation appendices. The 20→50 SWE result uses the adaptive 200-task pool; cross-benchmark tests provide a distinct transfer result. Actual DGM outer code retains compiled candidates with `keep_all` by default and uses a fixed outer selection procedure. Need finish source-code inspection of the self-edit step and record its snapshot.
- VSI002: read evaluator interface, Borg, tiling, IR and RTL cases, and ablation design. Tiling reports 23% average kernel speedup and 1% overall Gemini training-time reduction; these are different denominators. RTL authors explicitly say downstream synthesis also found that particular bit-removal change. Need inspect any mathematical exhibit used in final text and its construction/verifier.
- VSI003: read protocol and Tables1–3, task split and discussion. 45/10/34 train/validation/test and reported 0.6-point held-out average change are one concrete outcome. Do not convert authors' general explanation into a universal law or claim a statistical equivalence test absent from the paper.
- VSI004: read train/validation/test design, generated tests, final metrics and evolved artifact behavior. ProgramBench uses mean test fraction, unlike all-tests-passed task rate on the other two benchmarks. Public repository describes frozen harnesses and evaluation runtime; do not call it a full released optimization runner without seeing that code.
- VSI007–009: retained full dated 2026 official updates/developer documentation. The 2026 impact page reports applications beyond the initial paper; main text must attribute those reports and retain task-specific denominators. The product documentation requires a functional seed and an evaluable optimization objective.
- Promptbreeder official paper and SCoRe supplementary reading remain to be completed; no detailed result claim will be inferred from titles or abstract alone.

The complete original source files are retained under the implementation `sources/` folder. Access failures, earlier paper versions and API partial outputs remain separate from completed analysis.
