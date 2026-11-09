from pathlib import Path
import json, hashlib

base=Path(__file__).resolve().parent
root=base.parents[2]
specs=[
 ('TTC001','§§3–6; setup, difficulty and cost definitions, search/revision results; §5.3 descriptions of Appendix M examples','PaLM 2-S*; MATH 12k/500 split; v1; no software commit pinned','Difficulty-conditioned gains, PRM reward-to-go semantics, search overoptimization; difficulty inference omitted from cost'),
 ('TTC002','§§2–4, budget-forcing definitions and Figure 4 discussion; title/version header','s1-32B from Qwen2.5-32B-Instruct; Gemini Thinking teacher; AIME24/MATH500/GPQA Diamond; v2 2025-02-03','Separate post-training from within-checkpoint forcing; 50 to 57 AIME24 and saturation'),
 ('TTC003','abstract and introduction quantity claims, lines 151/163/172','v1 superseded for quantitative inventory','Contradictory v1 billion/million counts; do not propagate'),
 ('TTC003v2','title/version; §§2–3 comparison principles; §4 Table1 and §4.2 Figure5 discussion; Appendix G Table3','v2 2026-08-31; 20 configs x120 math x80 bank; public collection distinction','Inventory reconciled; shared-bank selector differences and gold-reference diagnostic'),
 ('TTC005','§§4–6; Appendix A.1–A.6, B tables6–7, C.1–C.3; D diagnostics passages','v1; Qwen3-8B; HardLCBv6 28 selected from131 February–May2025; no implementation commit pinned','Filtered mean, carry-forward, FMV definition, no hidden-test checkpoint best selection, 20000 nominal slots'),
 ('TTC006','extracted paper §§3–5 and appendices E–H; visual pages4–5 Tables1–3 and Figure3','ACL2026 Findings pp23967–23977; exact R1 checkpoint insufficiently specified','Numerical thresholds withheld because declared denominator, flip counts and figure/table values conflict'),
 ('TTC007','§§3–5; A.1–A.5; B.2–B.3; D.1','v1; six listed checkpoints; 963questions; 16trajectories and16answer probes/position','Finite-probe maximum and oracle information distinguished; cost excludes controller overhead'),
 ('TTC008','§3 propositions1–3; §4 planner/cost; §6 selected comparisons; §7 limitations; AppendixA proof setup','v1; public data releases described by paper; exact release commits unpinned','Selector-aware ceiling; conditional independence scope; proxy costs and limited-grid allocation'),
 ('TTC009','§§2–3; Table1; sampling/model settings and 40sample/10run protocol','v4 2023-03-07; PaLM540B T=.7 topk40; GSM8K and other specified benchmarks','Fixed-model plurality gains; 17.9 absolute GSM8K points'),
 ('TTC010','§§2–4; Table1 cost and Figure7 selection discussion','v2 2024-09-16; Llama3 8B/70B; DeepSeek-Coder-V2 +Moatless; SWE-bench Lite','Coverage vs selection; cost-efficiency varies by task; 10k sample bank and250agent attempts'),
 ('TTC011','§4.1–4.2, Game24 Table2 and creative writing evaluator description','v2 2023-12-03; GPT4 experiments May5–16 2023; 100harder Game24 tasks','Partial-state search mechanism; exact task scoring versus preference evaluation'),
 ('TTC012','§§2–4; Figure3 numbers and scoring; training set and controlled small-model comparison','v1 2023-05-31; GPT4-derived generator and reward models; MATH500 split; best-of1860','PRM selection benefit; training-data confounds; product-of-step probability scoring'),
 ('TTC013','§§3–7; Tables3–5; one-round correction and inference sample scaling','v1 2024-09-19; Gemini1.5Flash MATH; Gemini1.0Pro MBPP->HumanEval','Training enables repair; separate4.4point inference delta from15.6point delta improvement'),
 ('SUP-CM','§§1–2.3; Tables1–2; state machine/serial budget definitions','v1 2025-01-24; claude-3-5-sonnet-20241022 +Qwen2.5-Coder-32B-Instruct; SWE-bench Verified; repo not commit-pinned','Full loop and selection costs, coverage69.8 vs submitted57.4'),
 ('SUP-TAU','§§3–5; state/reward/pass^k definitions; Tables1–2; setup30action cap','v1 2024-06-17; 115retail+50airline; agentT0/userT1; paper versions, no current leaderboard','Repeat reliability distinct from coverage; final-state reward can miss procedure violations'),
 ('SUP-LIMITS','§§1–4 and AppendixA.2 scope passages','v1 2024-11-26; HumanEval/MBPP filters vs expanded plus evaluators','Weak-test false positives and consequence-sensitive sample limit'),
 ('SUP-SELF','§3.1–3.2 Tables2–3; original arxiv v2 after conference PDF transport failure','v2 2024-03-14; GPT3.5-0613, GPT4 accessed2023-08-29; 200question subset forGPT4','Intrinsic correction differs from oracle-stopped evaluation; reported regression'),
 ('SUP-AC','PDF pp1–5: §§1–4; main result summary; code aggregation and Beta threshold','EMNLP2023 pp12375–12396; Vicuna13B/code-davinci002/GPT3.5; reasoning40sample cap','Sample-count reductions from stability stopping; confidence is about plurality, not truth'),
 ('SUP-TREE','§§3–4, Table2, value calls/action proposal/backtracking; §5 initial sweep description','v1 2024-07-01; gpt-4o-2024-05-13 value model; WA/VWA; five-action comparison','Environment search needs replay and evaluator work; table18.9 versus prose18.6 minor mismatch avoided by citing table'),
]
ledger=[]
for sid,scope,version,observation in specs:
 folder=base/'supplemental-sources'/sid if sid.startswith('SUP-') else root/'sources'/sid
 meta=json.loads((folder/'retrieval.json').read_text(encoding='utf-8'))
 textfile=folder/'original.txt'
 ledger.append({'source_id':sid,'url':meta['url'],'title':meta.get('title'), 'reading_location':scope,'read_scope':'selected complete sections and passages named, not blanket full-paper read','version_model_evaluation':version,'observation':observation,'original_text_path':str(textfile),'original_path':str(folder/('original.pdf' if (folder/'original.pdf').exists() else 'original.html')),'text_sha256':hashlib.sha256(textfile.read_bytes()).hexdigest(),'retrieval_record':str(folder/'retrieval.json'),'reader':'/root/ttc_research'})
(base/'reading-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'Recorded {len(ledger)} source readings.')
