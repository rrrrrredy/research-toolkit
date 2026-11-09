# Verifiable Self-Improvement: What Changes, Why It Helps, and What Survives the Search

Evidence through 9 November 2026. A research report for engineering and research leaders deciding where automated improvement can produce a reusable capability.

## The useful question is what the next task inherits

Automated improvement is already producing useful artifacts: a coding agent with better tools, a faster numerical kernel, a more effective task prompt, and a model that corrects its own mistakes more selectively. These advances have different causes and different deployment requirements. Treating them as one capability called “recursive self-improvement” obscures the engineering decisions that make them work.

The clearest dividing line is what remains after an optimization run ends. A better answer helps the current user. A better program, prompt or learned policy can help later users. The second outcome is valuable when the retained change improves the work it will actually encounter, with its required properties intact. Repeatedly obtaining a higher score on the examples used to choose the change is useful search feedback; the deployment decision concerns the future work that inherits the artifact.

Three findings organize this report. First, **the editable interface and evaluator form the central product design**. AlphaEvolve can search aggressively because many target programs have an executable objective and a controlled place to insert a change. Second, **reuse has to be measured on the relevant axis of change**. DGM's cross-benchmark results support transfer of some agent-code improvements; a controlled harness-evolution study finds little transfer under another protocol. Third, **correction needs a selective objective**. SCoRe improves the ability to repair wrong answers while preserving correct ones; a generic request to reconsider can worsen the result.

The practical opportunity is therefore broad but structured. Teams with a recurring, checkable task can expose a useful part of the system to automated search, retain the candidate's exact dependencies, and deploy the change that performs well on the work they expect next. Teams whose outcomes depend on unresolved judgments first need a more informative evaluation target. A larger improvement loop cannot supply a missing definition of success.

## Name the retained object before comparing systems

| System | What changes and persists | Candidate generator | Feedback and selection | What remains externally supplied |
|---|---|---|---|---|
| DGM | Coding-agent source patches and an archive of agent variants | An archived agent modifies its own code after a separate model diagnoses a failure | Empirical coding-task outcomes; fixed archive and parent-selection procedure | Foundation models, diagnostic model, task tests, initial agent and outer search code |
| AlphaEvolve | A target algorithm or program implementation | Gemini-based code proposals using a seed and program database | Executable evaluators, staged rejection and performance measurement | Objective, editable interface, workload, correctness checks and deployment integration |
| Promptbreeder | Task prompts, mutation prompts and selected worked examples | A frozen language model generates task and mutator variations | Training-example accuracy and population selection | Base model, examples and labels, genetic procedure and final test |
| SCoRe | Model weights implementing a two-attempt correction policy | On-policy responses during reinforcement learning | Training-time correctness rewards and a staged correction objective | Training oracle, task construction, initial checkpoint and learning algorithm |
| HarnessPro | Instructions, tool/runtime settings and selected harness packages | A development team diagnoses trajectories and proposes changes | Frozen generated tests, validation selection and final official grading | Models, development roles, task partitions, base runtime and final grader |

This is a classification of mechanisms, not a ranking. DGM edits parts of the agent that will perform later improvements; AlphaEvolve normally edits a target program used by another application. Promptbreeder can change the prompt that generates future prompts; SCoRe changes a policy through training. A temporary second attempt is a use of that policy, not another update to its weights. These distinctions identify what can compound and what must be supplied anew.

They also define the baseline. A proposed kernel should be compared with the implementation and compiler actually deployed. An agent-code change should be compared under the same downstream model and task conditions. A correction policy should be compared with the same model's first and second attempts. A search procedure should face a meaningful alternative use of the same search opportunity. The strongest claim in each comparison is the one that matches its changed object.

## How a retained improvement is produced

The common structure can be written as:

**Define the target and admissible changes → propose a candidate → execute a relevant evaluator → select or archive → evaluate the retained artifact on its intended future work → deploy, keep for further search, or revert.**

The steps have different meanings across the systems. Archiving a DGM descendant preserves a possible stepping stone; deploying it chooses what users will receive. AlphaEvolve's evaluator may protect feasibility outside the editable block. Promptbreeder's fitness labels tell the search which answers count as correct. SCoRe's training reward teaches when a second answer should differ. These are substantive decisions, not interchangeable boxes in a generic workflow.

The following comparisons reconstruct those decisions and show where the published results support useful reuse.
