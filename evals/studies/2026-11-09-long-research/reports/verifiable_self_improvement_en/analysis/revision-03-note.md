# Located English spacing correction

Natural-expression finding natural_expression-01: restore spaces in five English/numeric expressions. All numbers, source links, causal explanations and conclusions are unchanged. No research or calculation was rerun.

```diff
--- draft-v5.md
+++ draft-v6.md
@@ -199,7 +199,7 @@
 
 An evaluation set used repeatedly to choose candidates becomes part of the optimization process even if the model never sees its raw answers. Selection leaks information through which candidate survives. A large search can exploit a small systematic quirk or a lucky collection of examples. This is the practical meaning of adaptive overfitting: the best candidate on the reused set can be the one most fitted to that set's accidents.
 
-DGM's adaptive coding pool and transfer results illustrate how to keep the questions separate. The optimization curve tells an engineer whether search is finding variants favored by its feedback. The cross-benchmark evaluation asks whether the selected agent retains useful behavior on another distribution. HarnessPro's validation set selects candidates and its held-out tasks evaluate the selected artifacts. Rethinking's45/10/34 split directly shows how apparent search progress can become only a small change on new tasks. These are different evidentiary roles, rather than stronger and weaker names for the same score.
+DGM's adaptive coding pool and transfer results illustrate how to keep the questions separate. The optimization curve tells an engineer whether search is finding variants favored by its feedback. The cross-benchmark evaluation asks whether the selected agent retains useful behavior on another distribution. HarnessPro's validation set selects candidates and its held-out tasks evaluate the selected artifacts. Rethinking's 45/10/34 split directly shows how apparent search progress can become only a small change on new tasks. These are different evidentiary roles, rather than stronger and weaker names for the same score.
 
 The needed holdout should match the decision. A team changing an inference model needs evidence on that model; a team expanding to new repositories needs new repositories; a team entering a new task family needs that family. Merely reshuffling familiar prompts may test response variability while leaving the important distribution shift untouched. Conversely, an exact algorithm improvement need not outperform on unrelated natural-language tasks to be valuable. The future workload defines the relevant transfer claim.
 
@@ -261,12 +261,12 @@
 ### Measurement details that change interpretation
 
 - **DGM run units:** The paper's 80 generated-agent iterations and the public code's 80 outer generations with two candidate attempts are retained as separate descriptions. The reported empirical scores follow the paper's protocol.
-- **DGM model contributions:** A separate o1diagnostic model contributes proposed improvements; the agent's frozen foundation model and fixed outer selection remain external to the changed code.
+- **DGM model contributions:** A separate o1 diagnostic model contributes proposed improvements; the agent's frozen foundation model and fixed outer selection remain external to the changed code.
 - **AlphaEvolve performance:** Local kernel speedup and overall training-time reduction are reported separately. The RTL example explicitly acknowledges an existing downstream synthesis optimization.
 - **Promptbreeder ablation:** Population mean fitness over 200 evaluations is not the final held-out score. The GSM8K comparison uses the same PaLM 2-L block of Table 1, avoiding cross-model mixing.
-- **SCoRe correction:**15.6points is the change in the MATH correction delta; the trained policy's second attempt adds4.4points. The MATH and coding experiments use different named Gemini checkpoints.
+- **SCoRe correction:** 15.6 points is the change in the MATH correction delta; the trained policy's second attempt adds 4.4 points. The MATH and coding experiments use different named Gemini checkpoints.
 - **HarnessPro metric and expense:** ProgramBench averages test fractions, unlike binary task success on the other two benchmarks. Mean final-task execution cost is distinct from developing and selecting the package.
-- **Rethinking selected versus available answers:** Pass@1 for the delivered choice and pass@5 for availability in a candidate set remain distinct. The printed table averages and one-decimal model values are retained rather than reconstructed into false precision. The observed held-out+0.6points is not a statistical-equivalence result.
+- **Rethinking selected versus available answers:** Pass@1 for the delivered choice and pass@5 for availability in a candidate set remain distinct. The printed table averages and one-decimal model values are retained rather than reconstructed into false precision. The observed held-out +0.6 points is not a statistical-equivalence result.
 
 These details are concentrated here so that the main argument can focus on mechanisms and decisions. They should travel with the corresponding claims when the comparison is reused.
 
```
