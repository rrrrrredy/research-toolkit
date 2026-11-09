"""Illustrative arithmetic only. No model experiment, benchmark run, or live prices.

For one homogeneous task class, candidate pairs (correct, accepted) are i.i.d.
A selector returns a uniformly chosen accepted candidate; if none passes, abstain.
The success formula follows TTC008 section 3, with all numerical inputs assumed.
Eight independent pipeline slots, waves, no inter-wave overlap, no queueing.
"""
import json, math
from pathlib import Path

BUDGET = 0.10
SLOTS = 8
TOOL_COST = 0.0004 * 1.10  # 10% get exactly one retry; per executed candidate
TOOL_SECONDS = 2.0 * 1.10
GEN_COST = (800 * 0.5 + 1200 * 2.0) / 1e6
VERIFY_COST = (2000 * 1.0 + 200 * 3.0) / 1e6
GEN_SECONDS = 1.5 + 1200 / 60
VERIFY_SECONDS = 1 + 200 / 80

def outcomes(n, p, tpr, fpr):
    accepted = p*tpr + (1-p)*fpr
    some = 1-(1-accepted)**n
    good = p*tpr/accepted*some if accepted else 0.0
    wrong = (1-p)*fpr/accepted*some if accepted else 0.0
    return dict(coverage=1-(1-p)**n, success=good, wrong_submission=wrong,
                abstain=1-some, precision_ceiling=p*tpr/accepted if accepted else 0,
                utility_wrong_cost_4=good-4*wrong)

configs = [
    dict(name='cheap_generator_weak_verifier', p=.25, tpr=.95, fpr=.10,
         generation_cost=GEN_COST, verification_cost=VERIFY_COST,
         tool_cost=TOOL_COST, pipeline_seconds=GEN_SECONDS+TOOL_SECONDS+VERIFY_SECONDS,
         generation_tokens=1200, input_tokens=800, verifier_input_tokens=2000,
         verifier_output_tokens=200, tool_calls=1.1),
    dict(name='cheap_generator_stronger_verifier', p=.25, tpr=.95, fpr=.01,
         generation_cost=GEN_COST, verification_cost=2*VERIFY_COST,
         tool_cost=TOOL_COST, pipeline_seconds=GEN_SECONDS+TOOL_SECONDS+2*VERIFY_SECONDS,
         generation_tokens=1200, input_tokens=800, verifier_input_tokens=2000,
         verifier_output_tokens=200, tool_calls=1.1),
    dict(name='stronger_generator_weak_verifier', p=.55, tpr=.95, fpr=.10,
         generation_cost=4*GEN_COST, verification_cost=VERIFY_COST,
         tool_cost=TOOL_COST, pipeline_seconds=1.5+1200/40+TOOL_SECONDS+VERIFY_SECONDS,
         generation_tokens=1200, input_tokens=800, verifier_input_tokens=2000,
         verifier_output_tokens=200, tool_calls=1.1),
    dict(name='two_turn_revision_weak_verifier', p=.40, tpr=.95, fpr=.10,
         generation_cost=GEN_COST+(2000*.5+1200*2)/1e6,
         verification_cost=VERIFY_COST, tool_cost=2*TOOL_COST,
         pipeline_seconds=GEN_SECONDS+TOOL_SECONDS+(2.7+1200/60)+TOOL_SECONDS+VERIFY_SECONDS,
         generation_tokens=2400, input_tokens=2800, verifier_input_tokens=2000,
         verifier_output_tokens=200, tool_calls=2.2),
]
rows=[]
for cfg in configs:
    cost=cfg['generation_cost']+cfg['verification_cost']+cfg['tool_cost']
    n=math.floor((BUDGET+1e-12)/cost)
    row={**cfg,'n':n,'per_candidate_cost_usd':cost,'total_cost_usd':n*cost,
         'generation_cost_usd':n*cfg['generation_cost'],
         'verification_cost_usd':n*cfg['verification_cost'],
         'tool_cost_usd':n*cfg['tool_cost'],
         'total_generation_tokens':n*cfg['generation_tokens'],
         'total_generator_input_tokens':n*cfg['input_tokens'],
         'total_verifier_input_tokens':n*cfg['verifier_input_tokens'],
         'total_verifier_output_tokens':n*cfg['verifier_output_tokens'],
         'expected_tool_calls':n*cfg['tool_calls'],
         'worst_nonselected_complete_candidate_tokens':(n-1)*1200,
         'wall_seconds_8_slots':math.ceil(n/SLOTS)*cfg['pipeline_seconds'],
         **outcomes(n,cfg['p'],cfg['tpr'],cfg['fpr'])}
    rows.append(row)
result={'kind':'assumption_based_illustrative_calculation','currency':'hypothetical_USD',
        'budget':BUDGET,'slots':SLOTS,'rows':rows,
        'weak_verifier_width_sweep':[dict(n=n,**outcomes(n,.25,.95,.1)) for n in [1,4,8,16,32,64]],
        'correlation_extremes_n17':{'iid_coverage':1-.75**17,'identical_candidates_coverage':.25},
        'independent_action_success':{'q=.98,h=20':.98**20,'q=.995,h=20':.995**20},
        'limitations':['No live prices or measured throughput; no accuracy estimates from model runs.',
        'Tool retries change cost only in this example; p already refers to final candidate correctness.',
        'All candidates and verifier errors are conditionally independent across candidates.',
        'Revision p=.40 is an assumption about a capable revision system, not a property of prompting.',
        'Wall time is a waves model with average retry service time, not a tail-latency bound.',
        'Uniform accepted selection is not argmax scoring; formulas do not transfer unchanged.']}
target=Path(__file__).with_name('budget_output.json')
target.write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
for r in rows:
    print(f"{r['name']}: n={r['n']}, cost=${r['total_cost_usd']:.5f}, gen=${r['generation_cost_usd']:.5f}, verify=${r['verification_cost_usd']:.5f}, tool=${r['tool_cost_usd']:.5f}, coverage={r['coverage']:.6f}, success={r['success']:.6f}, false={r['wrong_submission']:.6f}, abstain={r['abstain']:.6f}, wall={r['wall_seconds_8_slots']:.1f}s, U4={r['utility_wrong_cost_4']:.6f}")
print(json.dumps(result['weak_verifier_width_sweep'],ensure_ascii=False))
print(json.dumps(result['correlation_extremes_n17'],ensure_ascii=False))
print(json.dumps(result['independent_action_success'],ensure_ascii=False))
