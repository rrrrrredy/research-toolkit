"""Deterministic arithmetic for labelled hypothetical allocation, not an experiment."""
from pathlib import Path
import json, math

generators={'small':{'cost':1.0,'seconds':30,'p':.2},'strong':{'cost':4.0,'seconds':45,'p':.5}}
verifiers={'weak':{'cost':.25,'seconds':5,'tpr':.9,'fpr':.1},'better':{'cost':1.0,'seconds':10,'tpr':.9,'fpr':.02}}
rows=[]
for budget in [8,16,32]:
 for gn,g in generators.items():
  for vn,v in verifiers.items():
   n=math.floor(budget/(g['cost']+v['cost']))
   a=g['p']*v['tpr']
   s=a+(1-g['p'])*v['fpr']
   rows.append({'budget_credits':budget,'generator':gn,'verifier':vn,'candidates':n,
    'generation_credits':n*g['cost'],'verification_credits':n*v['cost'],
    'unused_credits':budget-n*(g['cost']+v['cost']),
    'probability_correct_submission':a/s*(1-(1-s)**n),
    'probability_wrong_submission':(s-a)/s*(1-(1-s)**n),
    'probability_abstain':(1-s)**n,
    'unlimited_parallel_seconds':g['seconds']+v['seconds'],
    'four_worker_wave_seconds':math.ceil(n/4)*(g['seconds']+v['seconds']),
    'single_worker_seconds':n*(g['seconds']+v['seconds'])})
deadline_rows=[]
for budget in [8,16,32]:
 for gn,g in generators.items():
  for vn,v in verifiers.items():
   n=min(math.floor(budget/(g['cost']+v['cost'])),4*math.floor(100/(g['seconds']+v['seconds'])))
   a=g['p']*v['tpr']; s=a+(1-g['p'])*v['fpr']
   success=a/s*(1-(1-s)**n); wrong=(s-a)/s*(1-(1-s)**n)
   deadline_rows.append({'budget_credits':budget,'generator':gn,'verifier':vn,'candidates':n,'spent_credits':n*(g['cost']+v['cost']),
    'probability_correct_submission':success,'probability_wrong_submission':wrong,
    'utility_correct_1_wrong_minus_4':success-4*wrong,
    'four_worker_wave_seconds':math.ceil(n/4)*(g['seconds']+v['seconds'])})
results={'producer':'/root/ttc_research','kind':'hypothetical arithmetic; no new model experiments',
 'assumptions':{'selector':'uniform among accepted; no accepted candidate means abstain and no correctness credit',
  'candidate_dependence':'conditionally independent given this single task',
  'rates':'known hypothetical p/TPR/FPR; not pilot estimates or published measured rates',
  'currency':'abstract cost credits, not FLOPs, tokens or current provider prices',
  'time':'deterministic generated durations; each worker processes generation then verification; equal waves, no early stop, setup or queueing',
  'workers':4,'deadline_seconds':100},
 'generators':generators,'verifiers':verifiers,'rows':rows,'deadline_feasible_rows':deadline_rows,
 'reported_code_monkeys_arithmetic':{'total_llm_cost_usd':2291.90,'issues':500,'mean_cost_per_issue':2291.90/500,
  'selection_usd':131.95,'selection_fraction':131.95/2291.90,'selection_per_issue':131.95/500,
  'coverage_selection_gap_percentage_points':69.8-57.4,
  'fraction_of_random_to_oracle_gap_recovered':(57.4-45.8)/(69.8-45.8),
  'scope':'published historic LLM inference cost, not complete present-day service cost'},
 'score_correction_delta':{'base_delta':41.4-52.6,'trained_delta':64.4-60,'difference_of_deltas':(64.4-60)-(41.4-52.6)},
 'illustrative_risk_threshold':{'value_correct':1,'loss_wrong':4,'cost_abstain':0,'required_p_correct_to_submit':4/5},
 'illustrative_ten_step_success':.98**10}
out=Path(__file__).with_name('allocation-results.json')
out.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
for r in rows:
 print(f"B={r['budget_credits']:2} {r['generator']:6} {r['verifier']:6} N={r['candidates']:2} success={r['probability_correct_submission']:.6f} wrong={r['probability_wrong_submission']:.6f} serial={r['single_worker_seconds']:3} four_workers={r['four_worker_wave_seconds']:3}")
print(json.dumps(results['reported_code_monkeys_arithmetic'],indent=2))
