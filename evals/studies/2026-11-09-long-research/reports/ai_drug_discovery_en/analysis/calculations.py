"""Author research arithmetic. No model/API experiment or software test."""
from pathlib import Path
import json, math
from datetime import datetime, timezone
B=Path(__file__).resolve().parent
def wilson(k,n,z=1.959963984540054):
    p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [c-h,c+h]
out={
 'author':'Codex /root/ttc_research; not independent reviewer',
 'executed_utc':datetime.now(timezone.utc).isoformat(),
 'rentosertib':{'reported_change_difference_ml':98.4-(-20.3),'equation':'98.4 - (-20.3); no derived CI or causal estimate',
 'missing_total_pct':100*22/71,'missing_60qd_pct':100*8/18,'missing_placebo_pct':100*3/17,'withdrawal_pct':100*16/71},
 'CCM_screen':{'machine_orthogonal_validation_fraction':7/38,'manual_fraction':1/38,'selected_set_yield_ratio':(7/38)/(1/38),'meaning':'Same screen, matched selected-set sizes; no clinical success inference'},
 'halicin_screen':{'hub_top_fraction':51/99,'hub_bottom_fraction':2/63,'top_bottom_yield_ratio':(51/99)/(2/63),'zinc_selected_any_species_fraction':8/23,'meaning':'Selected compounds and different endpoints; not global library sensitivity or clinical probability'},
 'REC4881':{'week13_response_fraction':13/15,'week25_below_baseline_fraction':11/13,'phase2_efficacy_evaluable_fraction':16/21,'phase2_week13_measured_fraction':15/21,'meaning':'Denominators kept distinct; no imputation of absent outcomes as failures or successes'},
 'baricitinib':{'COV_BARRIER_raw_absolute_mortality_reduction':100/761-62/764,'COV_BARRIER_raw_risk_ratio':(62/764)/(100/761),'RECOVERY_raw_absolute_mortality_reduction':546/4008-514/4148,'RECOVERY_raw_risk_ratio':(514/4148)/(546/4008),'meaning':'Raw proportions; not adjusted HR/rate ratio, not causal AI attribution, not cross-trial ranking'},
 'historical_AI_cohort':{'phase1':{'k':21,'n':24,'fraction':21/24,'wilson_95':wilson(21,24)},'phase2':{'k':4,'n':10,'fraction':4/10,'wilson_95':wilson(4,10)},'meaning':'Descriptive binomial uncertainty conditional on published classifications; neither selection bias nor causal contrast addressed'},
 'Sanofi_initial_2022_terms':{'per_program_milestone_ceiling_million':193+150,'fifteen_program_product_million':15*(193+150),'announced_rounded_ceiling_million':5200,'upfront_fraction_of_upfront_plus_announced_ceiling':100/(100+5200),'meaning':'Arithmetic on ceilings, not forecast, fair value, revenue, or received cash'},
 'Sanofi_Oct2026_inflows':{'announced_total_million':144,'initial_upfront_million':100,'difference_million':144-100,'meaning':'Aggregate additional announced upfront/milestone inflows; not all from latest candidate'}
}
(B/'calculations-results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
