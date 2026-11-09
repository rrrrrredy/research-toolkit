# U1: Evidence protocol and decisive premise checks

Producer: Codex research agent `/root/ttc_research`. Date: 2026-11-09. This is original source analysis and arithmetic, not independent review and not a rerun of model experiments. Evidence cutoff: 2026-11-09. The parent researcher should send this contribution and its source locations to a different evidence/domain reviewer.

## Operational comparison protocol

The evaluated object is a complete inference system: checkpoint and post-training history; prompt and sampling settings; candidate generator; retained state; evaluator and its information access; reducer or controller; stopping rule; and resource accounting. “More compute” means changing a specified component of that system. It does not, by itself, establish a causal benefit from inference allocation when the checkpoint, teacher data, verifier, or training procedure also changes.

Use three distinct comparison levels. A **fixed-bank comparison** holds generated candidates constant and compares reducers; its result concerns answer selection conditional on that bank. A **fixed-checkpoint end-to-end comparison** permits new trajectories but freezes the generator weights and counts generation, rejected branches, selection, control, and tools. A **whole-system comparison** may change training, model size, or verifier; it can inform a purchasing/design decision but does not isolate inference allocation. A fourth useful diagnostic is an **oracle bound**, where the controller sees correctness or repeated answer probes unavailable online. Such a bound locates opportunity; it is not a deployable saving.

Keep candidate coverage, submitted-answer success, and consistency separate. Under conditionally independent samples on one task, coverage is `1-(1-p)^N`; this assumes an oracle that identifies any correct candidate if used as an answer-selection score. Self-consistency uses answer frequency; best-of-N uses a score; either can leave most coverage gains unrealized. For multi-run reliability, the probability of all k runs succeeding is a different object from finding one successful run. A shared raw token count is not a compute unit across model sizes, architectures, inference engines, or prefill/decode mixes.

Minimum accounting vector: generator input/output/reasoning tokens, discarded branches, verifier input/output and calls, controller/probe calls, tool execution and retries, any test-time gradient updates, elapsed wall time, and peak parallel resources. Prefix cache reuse belongs in the cost model only if actually available. Use measured hardware time or stated compute models for hardware comparisons; provider prices for money; dependency critical paths for latency. Do not replace any of these with a single unlabeled “cost.”

Statistical units are questions/tasks unless a claim specifically concerns conditional trajectories. A prompt bootstrap conditional on frozen samples excludes uncertainty from generating new candidates or judge calls. Selection of a maximum across many noisy prefixes requires fresh evaluation or explicit reporting as a noisy empirical maximum. Difficulty bins estimated from ground truth are oracle analysis, even when hyperparameters are cross-validated. If calibration and deployment distributions differ, re-estimate the relevant selection quantities rather than treating a historical aggregate score as a stable per-task probability.

These rules follow the explicit distinctions in TTC003v2 §§2–3 and TTC007 §§3–5; the restrictions on selector-aware scaling follow TTC008 §3. They are applied below at claim level, without discarding an entire source because one number is unusable.

## TTC003: version correction resolves the inventory question

Read versions: v1 `https://arxiv.org/html/2608.04001v1` and v2 `https://arxiv.org/html/2608.04001v2`. The recovered v2 title page dates the revision 31 August 2026 (local original.txt line 126). v1 abstract line 151 says more than 22 billion traces, while introduction/contribution lines 163/172 say more than 22 million. Those are superseded statements, not a live numerical premise for the report.

V2 explicitly reports **1,403,520 publicly released attempts**, while Table 1 counts **1,948,821 study responses**. The two totals reconcile exactly:

* Study inventory: `18,543*27*1 + 120*20*80 + 186*7*80 + 3,600*4*80 = 1,948,821`.
* Public collections: `120*20*80 + 186*4*80 + 3,600*4*80 = 1,403,520`.
* Difference: `1,948,821 - 1,403,520 = 545,301 = 500,661 + 44,640`.
* The 500,661 responses are the one-response broad evaluation; the additional `186*3*80=44,640` are three medium-effort repeats in the signal-rich mathematics study, expressly described as repeated-run diagnostics in Table 1. Public Table 3 has four configurations for that collection, while study Table 1 has seven banks.

**Decision: usable.** Cite v2 and distinguish study inventory from declared release. The paper's public-release claim is now internally reconcilable. This research did not enumerate or download all release files, so it should not claim to have audited the actual hosted dataset completeness. The earlier v1 mismatch need not dominate the report; it belongs in source/version notes if mentioned at all.

Positive contribution: v2's fixed-bank design permits reducer comparisons without conflating a better selector with a luckier generated pool. Its distinction between causal stopping and post-hoc pruning prevents counting already-generated discarded tokens as saved inference work.

## TTC005: TTSP changes the proposal distribution, and its metric has a specific meaning

Source: *Test-Time Self-Play: Scaling without a Verifier*, arXiv 2611.07367v1. Read §§4–6, Appendix A.1–A.6, B.1–B.2, C.1–C.3 and D diagnostics. Local source: `sources/TTC005/original.txt`; principal locations 220–303, 624–745, 799–904.

TTSP initializes proposer and solver LoRA adapters from Qwen3-8B and optimizes both with GRPO on a target-specific synthetic curriculum. A proposer constructs executable synthetic problems; held-out generated tests supply solver rewards; previous accepted problems and current solve rates are retained in a replay history. This creates a real mechanism for improving the target proposal distribution even without target-answer feedback. It is **test-time adaptation involving training**, not a fixed-weight inference-only method. “Without a verifier” refers to withholding a target verifier from the adaptation loop; synthetic execution remains central, and final correctness is measured with the target public-plus-private evaluator.

The benchmark universe is a 131-problem LiveCodeBench v6 slice from February–May 2025. HardLCBv6 contains 28 selected targets for which Qwen3-8B's empirical mean@512 lies strictly between 0 and 0.7; MidHard has values above 0.1 and VeryHard values at or below 0.1. The reported improvement is conditional on this selected, nonzero-coverage population. It is not a whole-LiveCodeBench success estimate. The source states that the slice postdates the model's knowledge cutoff; this is an author provenance statement, not independent proof of absence of contamination.

The eight submitted candidates are filtered with evaluator v. For a nonempty accepted set A, filtered mean@8 is `sum(correct(y), y in A)/|A|`. Thus it is acceptance-conditioned correctness, not pass@8 and not an eight-denominator average except under the accept-all v0 condition. If the strongest filter is also the final correctness evaluator, every nonempty accepted set scores 1. The remaining variation reflects whether an accepted candidate exists and, for iterative methods, the carry-forward rule. Under v0, all eight remain, so this reduces to a meaningful unfiltered candidate-quality average.

When the current checkpoint has no admitted candidate, Appendix A.5 carries forward the most recent earlier nonempty checkpoint's score; if none exists, it assigns zero. Noniterative baselines receive zero on an empty set. Identical words for the scoring convention therefore do not imply identical effective memory: an iterative method can retain a historical nonzero score while a one-shot baseline cannot. This matters especially under strong filters. Under v0 the admitted set is never empty, so this issue cannot explain v0 gains. The report can use the verifier-free candidate-quality result positively while avoiding a blanket equal-cost or equal-history superiority claim.

Appendix B explicitly states “Converged checkpoint; no best hidden-test checkpoint selection.” This resolves the old planning note that checkpoint selection might be hidden-test best-of-many. The exact convergence rule and eight-candidate handling of tied FMV maximizers are not fully specified in the inspected text; no contrary implementation should be invented. ACE's full evaluator monitoring is not revealed to its playbook outside the oracle condition, according to C.1. Artificial verifier calibration uses oracle-labelled baseline solutions and public/private tests, so it is a controlled diagnostic condition, not evidence that the same calibrated weak filter can be built without privileged target labels in deployment.

FMV terminology also needs precision. The body describes selecting the modal functional cluster. C.2 implements the **sum of pairwise agreements over individual test inputs**. These are not generally equivalent. A concrete counterexample is five candidates with output vectors `(0,0),(0,0),(1,1),(1,1),(0,1)`. The first two clusters each have size 2; the unique `(0,1)` candidate has size 1. Yet its per-input agreement score is 4, while each candidate in either larger cluster scores 3. C.2's rule selects the singleton. This is a mathematical distinction between whole-vector clustering and additive per-input consensus, not a claim that the reported software used an unobserved algorithm.

The declared 50-step schedule already entails nominally `50*(2*8 + 48*8)=20,000` proposer-plus-solver rollout slots per target: 800 proposer slots and 19,200 solver slots. It also incurs synthetic-test reconstruction/execution, evaluation, gradient computation, and replay bookkeeping. Invalid proposals and sequence lengths affect realized work. Therefore native-axis plots in rollout count, context iterations, and GRPO steps cannot establish an equal-total-compute ranking. This calculation is a lower-dimensional description of the published schedule, not a measured token, FLOP, or dollar total.

**Decision: usable** for the target-specific synthetic-curriculum mechanism, unfiltered v0 results on selected targets, training/inference distinction, and evidence of little improvement on VeryHard. **Limited use** for strong-verifier aggregate comparisons because of acceptance conditioning, history and oracle access. **Not usable** for an equal-cost advantage without complete accounting. Near-zero benefit at empirical mean@512 below about 0.1 is a result for this setup, not a universal capability threshold or proof that zero-coverage targets can never become solvable.

## TTC006: original PDF confirms numerical incompatibilities

Source: *When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling*, ACL 2026 Findings, pp.23967–23977, `https://aclanthology.org/2026.findings-acl.1199.pdf`. Read the full extracted paper and inspected original rendered pages 4 and 5, including Tables 1–3 and Figure 3. Exact images are `sources/TTC006/pages/p-04.png` and `p-05.png`. These observations are not inferred from an OCR-only transcription.

The declared AIME setup is 60 questions, deterministic decoding, one recorded answer per problem per budget, budgets 500 through 16,000 in 500-token increments. On that protocol a single accuracy must be an integer multiple of `100/60=1.6667` percentage points. Table 1 values such as 37.8%, 46.5%, and 55.8% do not fit the stated denominator, even after rounding to one decimal. There may be unreported averaging, but the paper does not specify it. Do not reverse-engineer an alternative denominator and call it the actual experiment.

The interval-average marginal utility must telescope. Table 1's R1 endpoint values imply, in percentage points per 500 tokens:

| Interval | Endpoint-derived mean MU | Printed Table 1 MU |
|---|---:|---:|
| 0.5K–2K | (37.8−28.2)/3 = 3.2 | 3.2 |
| 2K–4K | (46.5−37.8)/4 = 2.175 | 1.8 |
| 4K–6K | (50.2−46.5)/4 = 0.925 | 0.9 |
| 6K–8K | (53.8−50.2)/4 = 0.9 | 0.9 |
| 8K–12K | (55.8−53.8)/8 = 0.25 | 0.1 |
| 12K–16K | (54.9−55.8)/8 = −0.1125 | −0.3 |

Rounding cannot explain several discrepancies. They remain whether one regards the interval MU as a mean of 500-token increments or as an endpoint-derived slope, because the sums telescope on a common cohort.

Table 2 calls its counts cumulative flips in transitions from threshold t through 16K. Both positive and negative counts must then be nonincreasing as t rises; the printed negative count instead rises from 31 at 1K to 83 at 16K. At the terminal threshold, there are no subsequent transitions within the stated range. More fundamentally, on any fixed collection of binary trajectories, `positive_flips - negative_flips = correct_at_end - correct_at_start`. Repeated flips cancel. For 60 questions this difference must lie in [-60,60], whereas the 1K row gives `142-31=111`, and the 16K row gives `11-83=-72`. “One question can flip more than once” does not repair these arithmetic constraints.

For consecutive budgets on the same binary cohort, `DeltaAccuracy=(positive-negative)/n`; a local negative/positive ratio over one necessarily implies a negative local accuracy change. The paper's claim that flip ratio crosses earlier merely because it is more sensitive cannot explain a discrepancy at the same aggregation window. A suffix-cumulative ratio and a local MU can differ because their windows differ, but then the published cumulative counts still need to obey the suffix and endpoint identities.

Appendix E gives p=0.038 in prose for the 7K crossover and p=0.014 in Table 5. The 95% interval for a −0.9-point accuracy decline cannot be interpreted without resolving the observation/averaging unit. Its narrowness does not settle the denominator problem.

The cost-aware utility is explicitly `U_lambda(t)=Acc(t)-lambda*t/16000`, with accuracy in [0,1]. Using the printed Table 1 and lambda=0.5 gives utilities at 2K,4K,6K,8K,12K,16K of `0.3155,0.3400,0.3145,0.2880,0.1830,0.0490`. Among those printed points, 4K is best; 6K is not. This conclusion is deliberately limited to displayed points rather than asserting the optimum of the unavailable 32-point data.

Original Figure 3(a) also differs from Table 1: visually, the R1 curve peaks near 6–7K at approximately 52%, then declines toward about 49% at 16K. Table 1 instead peaks at 12K, 55.8%, ending at 54.9%. The image has a lambda=0.5 marker around 4K, while §5.3 says around 6K. Approximate graphical values are labelled as visual readings, not digitized numerical data. This confirms a substantive figure/table mismatch rather than an extraction ordering error.

Positive mechanism retained: successive reconsideration can replace a correct answer with a wrong one, and a cost-penalized objective can favor a point before peak accuracy. But this paper's exact 7K warning threshold, optimum budget, confidence interval, and claimed realized savings are **quantitatively withheld** until corrected data or a clarified protocol exists. Its natural-length comparison is also observational: harder questions write longer, so lower accuracy among longer traces does not establish that the extra tokens caused the error. Forced “Wait” markers need separation from spontaneous hesitation before those markers become a deployable stopping signal. Other sources can support nonmonotonic behavior without relying on this numerical record.

## TTC007: noisy prefix optima locate potential, not guaranteed savings

Source: *Constructing Pareto Frontiers of Optimal Reasoning Termination Methods for Overthinking in Reasoning Models*, arXiv 2610.13570v1. Read §§3–5, A.1–A.5, B.2–B.3, and D.1. The protocol covers six fixed checkpoints and 963 questions (90 AIME, 500 MATH, 198 GPQA-Diamond, 175 LiveCodeBench), 16 trajectories per question, hence `6*963*16=92,448` trajectories. At each retained prefix, it generates 16 answers; these are not 16 new reasoning trajectories.

STP selects the earliest measured prefix with maximal empirical answer accuracy. OR measures thinking tokens after that selected point; AD is the gap between its empirical answer rate and the full-prefix empirical answer rate. The 64.3% OR and 9.03-point AD are equal-weight model/benchmark macroaverages. They do not measure an online controller's delivered savings. On a completely flat measured curve, the earliest maximizer is zero and OR can be 100%, even though the curve provides no evidence that deleting the reasoning helps or harms.

Selection over noisy 16-probe estimates biases the selected maximum upward. For one binomial estimate with true p=0.5, the standard deviation is `sqrt(0.25/16)=0.125`, or 12.5 points; maximizing over multiple estimates adds selection optimism. This calculation illustrates measurement resolution and does not assume the estimates are mutually independent or give the magnitude of actual bias. The authors' own probe-thinning analysis is directly informative: reducing probes from 16 to 4 increases expected OR from 64.34% to 74.69% and AD from 9.03 to 11.07 points, conditional on the observed probe pool. This establishes metric sensitivity; it does not show that the 16-probe maximum is the infinite-probe truth.

The dynamic-routing, fixed-budget and dynamic-early-exit oracle action sets are nested. A richer action set cannot reduce the best attainable objective on the same frozen measurements; its frontier dominance is partly a mathematical consequence of information and action access. The reported budget caps of 71.4%, 35.0% and 14.2% for matching the 72.33% STP endpoint reference are opportunity bounds within that measurement system, not three practical systems' wall-clock costs. The original final-answer baseline is 71.78%, a distinct estimator from the 72.33% repeated-answer endpoint.

Actual method adaptation has a useful train/test question split, and Appendix A explains ThinkSwitcher, Predictive Scheduling and ThinkBrake interfaces. Nevertheless, its plotted cost excludes predictor training, feature extraction and signal computation. The question/trajectory bootstrap holds the 16-probe curves fixed, so its intervals do not cover new answer-probe uncertainty. Figure x-axes mix oracle allowed caps with actual methods' realized mean retained tokens, explicitly labelled by the authors; read them accordingly.

The abstract's 70.5B reasoning tokens and D.1's 576,688,123 stored thinking tokens describe insufficiently reconciled boundaries. The latter divided by 92,448 is about 6,238 stored thinking tokens per trajectory (microaverage), which need not equal the separately reported 8,281 macroaverage. That micro/macro difference is not itself a contradiction. The much larger 70.5B may include repeated probing/prefix processing, but this reading found no precise accounting that authorizes that interpretation. Do not use 70.5B for a cost-normalized claim.

**Decision: usable** for the STP protocol, variability along fixed trajectories, oracle action-space comparisons, and observed finite-probe sensitivity. **Limited use** for OR/AD magnitude as empirical diagnostic statistics. **Withhold** any claim of realizable 85.8% compute savings or dollar/latency gains from the oracle cap.

## TTC008: selection ceilings and allocation are useful within their assumptions

Source: *Sample, Mix, or Verify? Allocating Test-Time Compute under Imperfect Verifiers*, arXiv 2610.23255v1. Read §3 propositions, §4 planner and cost definition, selected §6 empirical comparisons, §7 limitations, and the cited Appendix A proof setup.

For one task, candidate correctness p, verifier true-positive rate tau, false-positive rate f, and `s=tau*p+f*(1-p)`, the uniform-among-accepted selector has success

`S_N = [tau*p/s] * [1-(1-s)^N]`.

This follows because any acceptance occurs with probability `1-(1-s)^N`, and each accepted candidate has correctness probability `tau*p/s`. The selector fails if none is accepted. Under the source's conditional-independence assumption, increasing N monotonically approaches the acceptance-precision ceiling. More sampling cannot remove a false-positive floor. For example, p=.2, tau=.9, f=.1 gives s=.26 and ceiling .6923; N=1,4,8,16 yields .18,.4847,.6300,.6867, while oracle coverage at N=16 is .9719. Those are illustrative mathematical values, not measured model results.

This monotonic result is selector-specific. Argmax selection depends on precision in the high-score tail and may worsen as extremes are explored. The source's separate argmax formulation must be used; do not invoke its uniform-selection theorem to dismiss reward overoptimization.

The model represents task heterogeneity and cross-generator correlation through a joint distribution of per-task success rates; it represents repeated judge dependence on a single candidate through a latent acceptance propensity. It **does not** model arbitrary dependence among candidates within a task. Duplication, shared prompts, copied plans and interaction between agents can violate the assumption even when inter-task difficulty is modelled accurately.

Re-verification improves the large-N precision ceiling exactly when its false-to-true acceptance ratio falls: `F_k/T_k < F_j/T_j`. An increased false-positive rate alone does not determine the answer, because the true-positive rate may increase more. For fixed total budget, even a better precision ratio may be outweighed by fewer candidate generations. This yields a positive engineering criterion: spend on verification when it removes incorrect acceptance more effectively than it loses correct acceptance, and compare the resulting success under the reduced candidate count.

The allocation planner includes verification in its abstract cost, an advantage over generation-only comparisons. But parameters^gamma times output tokens are declared proxies: gamma=1 approximates compute, .7 price scaling, .5 latency-like scaling, and 0 flat token pricing. Tests are assigned zero cost and judge calls one generation; additive latency ignores parallel sampling. Hence the evidence supports allocation within those cost assumptions, not measured production billing or latency.

The reported regret is relative to the paper's finite configuration grid, not an unrestricted global optimum. The 175-system SWE-bench pool is a heterogeneous coverage study without a shared verifier; it is not 175 independent repetitions of one deployed agent. Same-agent held-out selection reaches 16 rollouts. Replanning uses a simulation with measured per-task rates rather than a new long-horizon live deployment. These distinctions preserve the positive finding that coverage and verifier error statistics can rank useful allocations while limiting claims about production agents.

At one candidate, a verifier can only reject or retain it; with abstention counted as failure and no penalty for a wrong submission, filtering cannot improve accuracy. The source's SWE example falls from 32.5% to 25.1%. This supports omitting that selector under that objective. If a wrong external action is more costly than abstention, rejecting risky outputs can still improve utility; the objective must explicitly price that consequence.

## Immediate handoff decisions

1. Use TTC003v2's reconciled release and inventory; retire the v1 quantity conflict from active premises.
2. Use TTSP as test-time weight adaptation with synthetic execution, restricted to its selected target population and metric; do not write “no feedback” or “same-cost dominance.”
3. Withhold TTC006 numerical deployment thresholds and savings. Preserve mechanism discussion using independently supported sources; Figure 3/Table 1 mismatch is confirmed visually.
4. Keep TTC007's oracle/finite-probe statistics separate from online stopping efficiency. Its own thinning analysis strengthens this distinction.
5. Use TTC008's selector-aware ceiling and `F/T` criterion, with conditional-independence and proxy-resource scope stated beside the applicable claims.
6. Subsequent chapters should develop positive choices from these constraints: improving candidates, acquiring informative feedback, selecting reliably, and allocating serial/parallel work; they should not become a list of caveats.

Independent review still required: the parent should verify the TTC006 arithmetic and PDF reading; TTSP metric/history interpretation and FMV counterexample; TTC003v2 reconciliation; and TTC008 formula/selector scope. The present producer has not performed that independent review.
