from pathlib import Path
import json,re
base=Path(__file__).resolve().parent
intro=(base/'manuscript-introduction.md').read_text(encoding='utf-8')
mechanisms=(base/'U2-U6-mechanisms-and-evidence.md').read_text(encoding='utf-8')
mechanisms=mechanisms[mechanisms.index('## 1.'):]
budget=(base/'U7-U8-budget-and-design.md').read_text(encoding='utf-8')
budget=budget[budget.index('## 1.'):]
budget=re.sub(r'^## (\d+)\.',lambda m:f'## {int(m.group(1))+9}.',budget,flags=re.M)
# Authoring integration: remove work-unit references from reader-facing prose.
mechanisms=mechanisms.replace('The U1 contribution documents the finite-probe maximum selection and excluded overhead; the final report should use that result to motivate calibrated online control rather than advertise the oracle cap as a realized saving.','Appendix A documents finite-probe selection and excluded overhead; these findings motivate calibrated online control rather than a claim that an oracle budget cap is a realized saving.')
mechanisms=mechanisms.replace('The U1 metric and cost analysis should accompany any numerical statement.','Appendix A states the metric and selection conditions for numerical interpretation.')
mechanisms=mechanisms.replace("because the U1 checks found unreconciled protocol and arithmetic conflicts", "because source checks found unreconciled protocol and arithmetic conflicts (Appendix A)")
mechanisms=mechanisms.replace('elaborated with calculation in U7–U8','elaborated with the calculation and decision tree below')
budget=budget.replace("and re-derived in U1", "and derived from the acceptance event")
budget=budget.replace('The table below was computed by the attached script.', 'The table below was computed directly from these inputs; the accompanying calculation record retains the arithmetic.')
appendix=(base/'manuscript-evidence-appendix.md').read_text(encoding='utf-8')
ledger=json.loads((base/'reading-ledger.json').read_text(encoding='utf-8'))
display={
 'TTC001':('Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters','v1; PaLM 2-S*; MATH 12,000/500 train/evaluation split; implementation commit not pinned'),
 'TTC002':('s1: Simple Test-Time Scaling','v2, 3 February 2025; s1-32B distilled from Gemini Thinking into Qwen2.5-32B-Instruct; AIME24, MATH500, GPQA Diamond'),
 'TTC003v2':('Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility','v2, 31 August 2026; repeated-math bank: 20 configurations × 120 questions × 80 responses; separate public-release inventory'),
 'TTC005':('Test-Time Self-Play: Scaling without a Verifier','v1; Qwen3-8B; 28 HardLCBv6 targets selected from 131 February–May 2025 problems; implementation commit not pinned'),
 'TTC006':('When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling','ACL 2026 Findings, pp. 23967–23977; exact R1 checkpoint insufficiently specified; numerical thresholds withheld'),
 'TTC007':('Constructing Pareto Frontiers of Optimal Reasoning Termination Methods for Overthinking in Reasoning Models','v1; six named checkpoints; 963 questions, 16 trajectories per question, 16 answer probes per retained position'),
 'TTC008':('Sample, Mix, or Verify? Allocating Test-Time Compute under Imperfect Verifiers','v1; paper-described public sample releases; exact data/code commits unpinned; selector and cost assumptions retained'),
 'TTC009':('Self-Consistency Improves Chain of Thought Reasoning in Language Models','v4, 7 March 2023; PaLM-540B temperature 0.7, top-k 40; 40 samples per run, ten runs'),
 'TTC010':('Large Language Monkeys: Scaling Inference Compute with Repeated Sampling','v2, 16 September 2024; Llama-3 8B/70B; DeepSeek-Coder-V2 with Moatless Tools on SWE-bench Lite'),
 'TTC011':('Tree of Thoughts: Deliberate Problem Solving with Large Language Models','v2, 3 December 2023; GPT-4 experiments 5–16 May 2023; 100 selected Game-of-24 tasks'),
 'TTC012':('Let’s Verify Step by Step','v1, 31 May 2023; GPT-4-derived generator and reward models; 500-question MATH evaluation; 1,860 candidates'),
 'TTC013':('Training Language Models to Self-Correct via Reinforcement Learning','v1, 19 September 2024; Gemini 1.5 Flash for MATH; Gemini 1.0 Pro trained on MBPP and evaluated on HumanEval'),
 'SUP-CM':('CodeMonkeys: Scaling Test-Time Compute for Software Engineering','v1, 24 January 2025; claude-3-5-sonnet-20241022 and Qwen2.5-Coder-32B-Instruct; SWE-bench Verified'),
 'SUP-TAU':('τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains','v1, 17 June 2024; 115 retail and 50 airline tasks; agent temperature 0, user temperature 1; historical models'),
 'SUP-LIMITS':('Inference Scaling FLaws: The Limits of LLM Resampling with Imperfect Verifiers','v1, 26 November 2024; HumanEval/MBPP filters versus expanded “+” evaluators'),
 'SUP-SELF':('Large Language Models Cannot Self-Correct Reasoning Yet','v2, 14 March 2024; GPT-3.5-0613 and GPT-4 accessed 29 August 2023; 200-question samples for GPT-4'),
 'SUP-AC':('Let’s Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs','EMNLP 2023, pp. 12375–12396; Vicuna-13B, code-davinci-002, GPT-3.5; 40-sample reasoning cap'),
 'SUP-TREE':('Tree Search for Language Model Agents','v1, 1 July 2024; gpt-4o-2024-05-13 value model; WebArena/VisualWebArena; matched five-action comparisons')
}
biblio='## Appendix B. Inspected source and evaluation versions\n\nThe source list identifies the versions used, rather than implying that older model results describe present-day products. Software commits were not independently pinned when the source did not specify them; no code implementation is claimed to have been reproduced.\n\n| ID and original | Version, model and evaluation boundary |\n|---|---|\n'
for s in ledger:
 if s['source_id']=='TTC003':continue
 title,version=display[s['source_id']]
 biblio+=f"| [{s['source_id']}: {title}]({s['url']}) | {version} |\n"
text='\n\n'.join([intro.strip(),mechanisms.strip(),budget.strip(),appendix.strip(),biblio.strip()])+'\n'
(base/'draft-final.md').write_text(text,encoding='utf-8')
print(json.dumps({'path':str(base/'draft-final.md'),'words':len(text.split()),'characters':len(text),'status':'author manuscript ready for independent full-report review'},ensure_ascii=False))
