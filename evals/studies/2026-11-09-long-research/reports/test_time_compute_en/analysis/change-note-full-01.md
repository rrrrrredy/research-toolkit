# Full-report author revision 01

Author: Codex /root/ttc_research; original substantive author, not an independent reviewer.
Recorded: 2026-11-09T14:54:58.082790+00:00.

Input: `C:\Users\luosong03\Documents\ChatGPT\Others\work\toolkit-long-research-20261109\evals\runs\2026-11-09-long-research\tasks\test_time_compute_en\reports\current.md`
Input SHA-256: `e1b4fa3580310c7761668eb042def1b4e7bc72a51a2d7e8f614385cca6bcbb78`
Output: `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\test_time_compute_en\codex-production\draft-revision-full-01.md`
Output SHA-256: `bf7a5db85e34a783b79040afd9eded0594ce7da69ee970f5b82f3c51f9f74cea`

## Finding disposition

- RU-TTCEN-01: Defined Overthinking Ratio (thinking-token fraction after the earliest observed maximum-accuracy prefix) and Accuracy Degradation (maximum minus full-thinking endpoint accuracy) before the first numerical table use. Percent and percentage-point units are explicit; finite-probe and oracle limits remain.
- RU-TTCEN-02: Return the executed increment to the existing completion check; update budget/time accounting before feasibility; return a reduced plan to accounting and feasibility; route an infeasible unrevisable plan to defer/abstain. Marginal value remains inside the hard constraints.
- natural_expression-01: Replaced internal planning-history wording with the 19,200 solver plus 800 proposer decomposition; removed the sentence about this writing request and a governance framework while retaining concrete pilot measurements.

## Review and original-source reading

- Read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\test_time_compute_en\native-full-reviews\reader_usefulness\response.json`; SHA-256 `31da238a944b8b152c60b4082b1a6728db178d4a0b986cb2fb8f7df2d79e9117`. Relevant findings: RU-TTCEN-01, RU-TTCEN-02, natural_expression-01.
- Read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\test_time_compute_en\native-full-reviews\natural_expression\response.json`; SHA-256 `9b1a6821e0b1a18b8628a9ff31ae94543648645f89c7f5b0a01e23af33e6a4d9`. Relevant findings: RU-TTCEN-01, RU-TTCEN-02, natural_expression-01.
- Actually read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\sources\TTC007\original.txt`: Abstract/introduction lines 69, 95-102; section 3.1 lines 139-155; full-thinking reference distinction lines 816-825; probe-thinning qualifications lines 1045-1058. SHA-256 `708e50f5dfbe69b53de523d40da5abdbd33bd54eb7f22a80a50e61e11d0eab1d`.

## Scope and preservation

The input current manuscript, first manuscript, prior author checks, upstream originals and calculation artifacts were not edited. No research/model experiment, model API call, calculation rerun, managed-state update or review import was performed. The diff below is the complete textual change. Author completion does not claim independent reviewer acceptance.

## Complete diff

````diff
--- reports/current.md (read-only input)
+++ draft-revision-full-01.md
@@ -130,6 +130,8 @@
 
 ## 8. Scaling comparison: what is supported and what remains a different experiment
 
+For OTBench, **Overthinking Ratio (OR)** is the fraction of a trajectory's thinking tokens generated after its earliest measured prefix attaining the highest observed answer-probe accuracy, reported as a percentage. **Accuracy Degradation (AD)** is that maximum observed accuracy minus the accuracy at the full-thinking endpoint, reported in percentage points. These are diagnostics of the finite prefix/probe measurements, not a proportion of failed tasks or realized online cost savings; the oracle and finite-probe limits remain material. [TTC007, §3.1](https://arxiv.org/html/2610.13570v1).
+
 | Study and frozen version | Comparison and statistical target | Reported scaling result | Useful conclusion and boundary |
 |---|---|---|---|
 | Self-Consistency, TTC009 v4 | Same checkpoint and prompts; 40 sampled paths vs greedy; ten runs | PaLM-540B GSM8K 56.5→74.4% | Voting can turn diversity into answer accuracy; no external checker, 40-generation cost |
@@ -141,7 +143,7 @@
 | SCoRe, TTC013 v1 | Trained model, one correction round; MATH 500-question split | 60→64.4%; base correction 52.6→41.4% | Repair behavior can be learned; 15.6-point headline is a change in deltas |
 | Adaptive-Consistency, SUP-AC EMNLP2023 | Fixed-weight stopping vs fixed sample budgets | 3.3x fewer samples average, <0.1-point average loss | Stop stable consensus; sample reduction is not a measured system latency reduction |
 | TTSP, TTC005 v1 | Target-specific GRPO adaptation on selected HardLCBv6 | Gains under weak target verification; near-zero on very low coverage subset | Change proposals through synthetic execution; cannot equate GRPO steps and sampling cost |
-| OTBench, TTC007 v1 | Frozen prefix/probe curves; nested oracle action sets | Mean OR64.3%, AD9.03 points; large oracle stopping headroom | Diagnostic upper bounds with finite-probe selection, not realized online savings |
+| OTBench, TTC007 v1 | Frozen prefix/probe curves; nested oracle action sets | Mean OR 64.3%, AD 9.03 percentage points; large oracle stopping headroom | Diagnostic upper bounds with finite-probe selection, not realized online savings |
 | CodeMonkeys, SUP-CM v1 | Full coding system with retained selection stage | 69.8% coverage, 57.4% submitted success | End-to-end improvement requires feedback and selection; historic cost ledger supports partial normalization |
 | Web tree search, SUP-TREE v1 | Fixed agent plus value-guided environment search | WA15.0→19.2% with five committed actions | Environment replay and value calls are essential parts of the method |
 | τ-bench, SUP-TAU v1 | Repeated task trials with user stochasticity | GPT-4o mean48.2%; retail pass^8<25% | Reliability cannot be inferred from best-run coverage |
@@ -190,7 +192,7 @@
 
 This normalization is useful because the selector's cost is included in the reported LLM total. It does not authorize comparison with a current product price or a different benchmark split. It also does not make a one-off benchmark expenditure equal to a production service's marginal cost. Deployment can reuse some fixed work, but may add queuing, cold starts, access control, logging and external API charges. Only components actually required by the task should enter the chosen ledger; the point is complete accounting of the system being compared, not speculative overhead inflation.
 
-TTC005's declared TTSP schedule provides a different kind of normalization. Fifty target-specific GRPO steps, with 16 proposer rollouts and 48×8 solver rollouts per step, imply **20,000 nominal rollout slots per target**. That quantity counts both proposer and solver generations. It does not include test construction, executions, target evaluations, sequence length variation or backward passes. It is therefore useful for checking the scale of the schedule but cannot be divided by another method's sample count to claim an efficiency ratio. The earlier planning estimate of 19,200 corresponds to solver slots only; the complete nominal sum adds 800 proposer slots. [TTSP, Appendix B](https://arxiv.org/html/2611.07367v1).
+TTC005's declared TTSP schedule provides a different kind of normalization. Fifty target-specific GRPO steps, with 16 proposer rollouts and 48×8 solver rollouts per step, imply **20,000 nominal rollout slots per target**. That quantity counts both proposer and solver generations. It does not include test construction, executions, target evaluations, sequence length variation or backward passes. It is therefore useful for checking the scale of the schedule but cannot be divided by another method's sample count to claim an efficiency ratio. The complete nominal sum is 19,200 solver slots plus 800 proposer slots. [TTSP, Appendix B](https://arxiv.org/html/2611.07367v1).
 
 Similarly, SCoRe's equal-solution-budget comparison can inform how to allocate attempts within its trained policy, but it does not normalize growing revision context into FLOPs. TTC001's fourfold result is a generation-equivalent comparison with difficulty-estimation overhead omitted. TTC007's retained-token frontiers exclude predictor/feature overhead and use labelled probe curves. These findings remain valuable at their declared level; forcing them into a common dollar leaderboard would discard the information needed to interpret them.
 
@@ -250,8 +252,8 @@
 
 ```mermaid
 flowchart TD
-    A[Define delivered success, wrong-action cost, deadline and budget] --> B{Does the simple path meet the requirement?}
-    B -->|Yes| Z[Use the simple path and stop]
+    A[Define delivered success, wrong-action cost, deadline and budget; assess the simple path] --> B{Does the current result meet the requirement?}
+    B -->|Yes| Z[Return the validated result and stop]
     B -->|No| C{What limits delivered success?}
     C -->|Missing external information| D{Reliable tool or user feedback available?}
     D -->|Yes| E[Acquire the information and retain the result]
@@ -273,13 +275,15 @@
     M --> Q
     O --> Q
     P --> Q
-    Q --> R{Fits deadline and parallel resource limit?}
+    Q --> Q1[Update remaining budget, elapsed time and resource use]
+    Q1 --> R{Fits remaining budget, deadline and parallel resource limit?}
     R -->|No| S[Reduce depth or width, route stronger, or simplify]
     R -->|Yes| T{Expected marginal value exceeds total marginal cost and error risk?}
-    S --> T
-    T -->|Yes| U[Allocate the next bounded increment]
+    S -->|Revised plan| Q
+    S -->|No feasible plan| V
+    T -->|Yes| U[Execute the next bounded increment and update the current result]
     T -->|No| V[Return current validated result, defer or abstain]
-    U --> T
+    U --> B
 ```
 
 “Meets the requirement” is more useful than “the model feels confident.” For an executable coding task it may mean passing relevant tests without breaking required behavior. For a final-state task it may mean achieving the intended database state while respecting the required action procedure. For an open-ended research answer it may mean that the claims needed for the user's decision have adequate source support. Extra computation should address a remaining gap rather than merely prolong the transcript.
@@ -288,7 +292,7 @@
 
 ## 15. Estimating the quantities that drive the policy
 
-A representative pilot should separate three observations: how often a useful candidate is generated; how often the deployed selector accepts or prefers a correct versus incorrect candidate; and how much total work the complete procedure requires. The final evaluator should have information not used to overfit the selector where possible, such as held-out tests or a blinded expert rubric. Record failed and discarded work. For agents, record tool errors and whether replay actually restores the relevant state. The request is to measure the real use path, not to add a broad governance framework.
+A representative pilot should separate three observations: how often a useful candidate is generated; how often the deployed selector accepts or prefers a correct versus incorrect candidate; and how much total work the complete procedure requires. The final evaluator should have information not used to overfit the selector where possible, such as held-out tests or a blinded expert rubric. Record failed and discarded work. For agents, record tool errors and whether replay actually restores the relevant state.
 
 Task-specific estimates matter. A mean success rate from easy and hard tasks does not predict the benefit of another sample on a particular unresolved case. Failure after several attempts is itself evidence that the case is harder or that the generator and verifier share a blind spot. An allocation policy can use that information, but its update rule should be calibrated against representative held-out tasks rather than fitted to the same final outcomes it is credited with predicting.
 
````
