# Located process-language revision

Based on the independent process_language findings. Preserve source versions, cited locations, assumptions, calculations and substantive evidence limits; keep access/reading operations in the original execution records.

Previous SHA256: 6738773ca0c6fd185906c967db5f26d77c20acf0e2f55892757ae11855383905

Revised SHA256: c339d6244bdf03eb4d0935e4428c2106b59f7dd556774a083165b29bf6f3fc19

```diff
--- current-before.md
+++ draft-revision-full-02.md
@@ -93,7 +93,7 @@
 
 The replacement rule is explicit: sample two individuals, select the fitter one, mutate it, and overwrite the loser with the mutated copy. Each individual retains its task-prompt set and mutation prompt, plus correct worked examples in the few-shot setting. Thus the winner supplies the parent of the next retained candidate, while mutation can alter the instruction that will generate later variants. A mutation is not automatically an improvement; tournament competition and subsequent fitness evaluation shape the population over repeated steps. [Official ICML paper, §3](https://proceedings.mlr.press/v235/fernando24a.html).
 
-The useful mechanism is adaptation to a recurring domain. A prompt found for one problem is a one-off artifact; a prompt that improves performance on unseen problems from that domain is reusable. Promptbreeder's official Table 1 reports PaLM 2-L zero-shot GSM8K accuracy of 83.9%, versus 66.5% for its CoT baseline and 65.5% for a 2,000-prompt combinatorial-initialization baseline. The held-out evaluation and baseline identity are essential to interpreting that comparison. The official paper and Table 1 were read, including the footnote assigning half-splits to four datasets without supplied training/test partitions.
+The useful mechanism is adaptation to a recurring domain. A prompt found for one problem is a one-off artifact; a prompt that improves performance on unseen problems from that domain is reusable. Promptbreeder's official Table 1 reports PaLM 2-L zero-shot GSM8K accuracy of 83.9%, versus 66.5% for its CoT baseline and 65.5% for a 2,000-prompt combinatorial-initialization baseline. The held-out evaluation and baseline identity are essential to interpreting that comparison. The Table 1 footnote assigns half-splits to four datasets without supplied training/test partitions.
 
 The mutation-prompt mechanism does not make human problem formulation irrelevant. A mutator can propose novel instructions only within the objective and examples available to the search. If the task description is wrong, the system can spend substantial effort becoming better at the wrong framing. If the labels reward an incomplete answer, fluent prompt variants may optimize that omission. The remedy is to improve the specification or evidence about the intended task, rather than make the evolutionary loop more elaborate.
 
@@ -249,7 +249,7 @@
 | [AlphaEvolve technical report](https://arxiv.org/html/2506.13131v1) | arXiv2506.13131v1,2025 | Evaluator interface and evolutionary search; §3.3 engineering applications; §4 ablations |
 | [AlphaEvolve impact update](https://deepmind.google/blog/alphaevolve-impact/) | Official company update, 7 May 2026 | Deployment examples; different application denominators retained |
 | [AlphaEvolve product overview](https://cloud.google.com/vertex-ai/generative-ai/docs/alphaevolve/overview) | Retrieved 9 November 2026; page updated 28 October 2026 | Functional seed and evaluable objective requirements |
-| [Promptbreeder official ICML paper](https://proceedings.mlr.press/v235/fernando24a.html) | PMLR 235, 2024; official 64-page PDF | Main §§3–5; Table 1; Appendix B Figure 4; Appendix K.2. Table 1 and Figure 4 were also inspected as rendered pages |
+| [Promptbreeder official ICML paper](https://proceedings.mlr.press/v235/fernando24a.html) | PMLR 235, 2024; official 64-page PDF | Main §§3–5; Table 1; Appendix B Figure 4; Appendix K.2. Table 1 and Figure 4 provide the reported comparison and ablation results |
 | [SCoRe](https://arxiv.org/html/2409.12917v1) | arXiv2409.12917v1,2024 | §§3–7; Tables3–5; task and checkpoint-specific correction results |
 | [HarnessPro](https://arxiv.org/html/2610.26770v2) | arXiv2610.26770v2,2026 | §§4–5; generated-test experiment; data partitions; Tables2–3; released-artifact descriptions in the appendix |
 | [HarnessPro release](https://github.com/pzs19/HarnessPro) | Retrieved 9 November 2026; README blob `095fa2738741688c7380075a9d83cc6f5cb503e0` | Distribution contains selected artifacts, splits and evaluation runtime |
```
