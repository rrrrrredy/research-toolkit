from pathlib import Path
import sys, json
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root))
import fetch_sources
fetch_sources.ROOT=Path(__file__).with_name('supplemental-sources')
items=[
 {'id':'SUP-CM','url':'https://arxiv.org/html/2501.14723v1','title':'CodeMonkeys: Scaling Test-Time Compute for Software Engineering'},
 {'id':'SUP-TAU','url':'https://arxiv.org/html/2406.12045v1','title':'tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains'},
 {'id':'SUP-LIMITS','url':'https://arxiv.org/html/2411.17501v1','title':'Inference Scaling FLaws: The Limits of LLM Resampling with Imperfect Verifiers'},
 {'id':'SUP-SELF','url':'https://arxiv.org/html/2310.01798v2','title':'Large Language Models Cannot Self-Correct Reasoning Yet'},
 {'id':'SUP-AC','url':'https://aclanthology.org/2023.emnlp-main.761.pdf','title':"Lets Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs"},
 {'id':'SUP-TREE','url':'https://arxiv.org/html/2407.01476v1','title':'Tree Search for Language Model Agents'},
]
with ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(fetch_sources.fetch,items):
  print(json.dumps(result),flush=True)
