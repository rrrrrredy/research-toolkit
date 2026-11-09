## Evidence appendix

### Primary versions and locations

| Source | Version used | Relevant original locations |
|---|---|---|
| [Darwin Gödel Machine](https://arxiv.org/html/2505.22954v2) | arXiv2505.22954v2,2025 | §§3–4; Appendix A transfer experiments; Appendix C.3 diagnosis; computational-cost discussion |
| [DGM outer implementation](https://github.com/jennyzzt/dgm/blob/main/DGM_outer.py) | Retrieved9November2026, Git blob`2c87f4bdc303d0ab3c4ad2333b03ecf0a74392be` | Parent selection, archive admission and CLI defaults |
| [DGM self-improvement implementation](https://github.com/jennyzzt/dgm/blob/main/self_improve_step.py) | Retrieved9November2026, Git blob`c8e41b5050f169959882dec1afca2ff94d69303e` | Diagnostic model, patch application, candidate editing and evaluation |
| [AlphaEvolve technical report](https://arxiv.org/html/2506.13131v1) | arXiv2506.13131v1,2025 | Evaluator interface and evolutionary search; §3.3 engineering applications; §4 ablations |
| [AlphaEvolve impact update](https://deepmind.google/blog/alphaevolve-impact/) | Official company update,7May2026 | Deployment examples; different application denominators retained |
| [AlphaEvolve product overview](https://cloud.google.com/vertex-ai/generative-ai/docs/alphaevolve/overview) | Retrieved9November2026; page updated28October2026 | Functional seed and evaluable objective requirements |
| [Promptbreeder official ICML paper](https://proceedings.mlr.press/v235/fernando24a.html) | PMLR235,2024; official64-page PDF | Main §§3–5; Table1; Appendix B Figure4; Appendix K.2. Table1 and Figure4 were also inspected as rendered pages |
| [SCoRe](https://arxiv.org/html/2409.12917v1) | arXiv2409.12917v1,2024 | §§3–7; Tables3–5; task and checkpoint-specific correction results |
| [HarnessPro](https://arxiv.org/html/2610.26770v2) | arXiv2610.26770v2,2026 | §§4–5; generated-test experiment; data partitions; Tables2–3; released-artifact descriptions in the appendix |
| [HarnessPro release](https://github.com/pzs19/HarnessPro) | Retrieved9November2026; README blob`095fa2738741688c7380075a9d83cc6f5cb503e0` | Distribution contains selected artifacts, splits and evaluation runtime |
| [Terminal-medium runtime hook](https://github.com/pzs19/HarnessPro/blob/main/harnesses/terminal-bench-2/medium/runtime/hook.py) | Source blob`7602e6fed53e31f3886ece6b7db15defd88a6dfe`; first100lines inspected | Session/tool-call handling and executable denial after configured finalization threshold; no claim to have executed the package |
| [Rethinking automatic harness evolution](https://arxiv.org/html/2607.12227v1) | arXiv2607.12227v1,2026 | §§3–5; Tables1–3; five-attempt comparison and45/10/34 transfer split |

Original snapshots, retrieval metadata and the report's source-location record accompany the research archive. The reported experiments are the authors' experiments. This report reconstructs them from those originals and inspects the specified implementation; it does not run a new self-modifying system.

### Measurement details that change interpretation

- **DGM run units:** The paper's80generated-agent iterations and the public code's80outer generations with two candidate attempts are retained as separate descriptions. The reported empirical scores follow the paper's protocol.
- **DGM model contributions:** A separate o1diagnostic model contributes proposed improvements; the agent's frozen foundation model and fixed outer selection remain external to the changed code.
- **AlphaEvolve performance:** Local kernel speedup and overall training-time reduction are reported separately. The RTL example explicitly acknowledges an existing downstream synthesis optimization.
- **Promptbreeder ablation:** Population mean fitness over200evaluations is not the final held-out score. The GSM8K comparison uses the same PaLM2-L block of Table1, avoiding cross-model mixing.
- **SCoRe correction:**15.6points is the change in the MATH correction delta; the trained policy's second attempt adds4.4points. The MATH and coding experiments use different named Gemini checkpoints.
- **HarnessPro metric and expense:** ProgramBench averages test fractions, unlike binary task success on the other two benchmarks. Mean final-task execution cost is distinct from developing and selecting the package.
- **Rethinking selected versus available answers:** Pass@1 for the delivered choice and pass@5 for availability in a candidate set remain distinct. The printed table averages and one-decimal model values are retained rather than reconstructed into false precision. The observed held-out+0.6points is not a statistical-equivalence result.

These details are concentrated here so that the main argument can focus on mechanisms and decisions. They should travel with the corresponding claims when the comparison is reused.

### Calculations and remaining information gaps

The accompanying `calculations.py` reproduces percentage-point changes, the33.945%mean-execution-cost reduction from$1.09to$0.72, and the explicitly hypothetical Amdahl illustrations. It performs arithmetic on source values and stated assumptions; it is not a rerun of any model experiment.

An all-in optimization bill is unavailable on a common basis across these systems. Consequently the report compares what expenditure is actually disclosed and gives a symbolic amortization relation instead of an invented financial ranking. The inspected HarnessPro public release is sufficient to examine the selected behavior but not to rerun its complete optimization process. Google's newer deployment examples are attributed official reports, with the original technical report supplying the more detailed mechanism comparison. These gaps leave the specific documented gains intact and identify what a team would need for its own adoption decision.
