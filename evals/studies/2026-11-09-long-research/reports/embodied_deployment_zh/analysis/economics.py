"""Author /root/microdrama_research. Explicit illustrative inputs, not vendor ROI."""
from pathlib import Path
import json,csv
from copy import deepcopy
B=Path(__file__).resolve().parent
def evaluate(p):
    crf=p['discount']/(1-(1+p['discount'])**(-p['life']))
    capital=p['capital']*crf if p['capital'] else p['annual_subscription']
    active=p['scheduled_hours']*p['availability']*p['utilization']
    potential_attempts=active*3600/(p['cycle_seconds']+p['intervention_rate']*p['recovery_minutes']*60)
    good=min(potential_attempts*p['quality'],p['annual_demand'])
    attempts=good/p['quality']
    help_hours=attempts*p['intervention_rate']*p['recovery_minutes']/60
    annual_cost=capital+p['fixed_operating']+help_hours*p['human_hourly']+p['local_support_hours']*p['human_hourly']
    manual_hours=good/p['manual_good_per_hour']
    avoided=manual_hours*p['human_hourly']*p.get('labor_realization',1)
    return dict(inputs=p,capital_annualized=capital,active_hours=active,potential_good_tasks=potential_attempts*p['quality'],attempts=attempts,good_tasks=good,help_hours=help_hours,annual_cost=annual_cost,cost_per_good=annual_cost/good,manual_hours=manual_hours,avoidable_labor_value=avoided,annual_difference=avoided-annual_cost)
common=dict(discount=.08,life=5,annual_subscription=0,scheduled_hours=4000,availability=.9,utilization=.65,quality=.98,human_hourly=60,local_support_hours=200,manual_good_per_hour=55,labor_realization=1,annual_demand=170000)
industrial={**common,'currency':'CNY 2026 assumed','task':'same sheet-metal transfer cell, illustrative','capital':520000,'fixed_operating':50000,'cycle_seconds':45,'intervention_rate':.02,'recovery_minutes':3}
special={**industrial,'task':'same bounded cell dedicated alternative, illustrative','capital':280000,'fixed_operating':30000,'life':7,'availability':.95,'quality':.995,'cycle_seconds':30,'intervention_rate':.005,'recovery_minutes':2}
logistics={**common,'currency':'CNY 2026 assumed','task':'carton unloading, not tote handling','capital':700000,'fixed_operating':70000,'utilization':.6,'quality':.99,'cycle_seconds':12,'intervention_rate':.01,'recovery_minutes':2,'local_support_hours':400,'manual_good_per_hour':180,'annual_demand':600000}
home={**common,'currency':'USD 2026 illustrative, subscription sticker price observed','task':'one defined 10-minute household chore','capital':0,'annual_subscription':499*12,'fixed_operating':300,'scheduled_hours':730,'availability':.85,'utilization':.4,'quality':.9,'cycle_seconds':600,'intervention_rate':.15,'recovery_minutes':5,'local_support_hours':24,'human_hourly':25,'manual_good_per_hour':6,'annual_demand':2000}
out={name:evaluate(p) for name,p in [('industrial',industrial),('dedicated',special),('logistics',logistics),('home',home)]}
for key,vals in {'utilization':[.4,.65,.85],'intervention_rate':[.005,.02,.05],'life':[3,5,7],'labor_realization':[.5,1]}.items():
    for v in vals: out[f'industrial_{key}_{v}']=evaluate({**industrial,key:v})
for u in [.2,.4,.8]:out[f'home_utilization_{u}']=evaluate({**home,'utilization':u})
(B/'economics-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (B/'economics-results.csv').open('w',newline='',encoding='utf-8-sig') as f:
    keys=['scenario','good_tasks','help_hours','annual_cost','cost_per_good','avoidable_labor_value','annual_difference']; w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
    for k,v in out.items():w.writerow({'scenario':k,**{a:v[a] for a in keys[1:]}})
print(json.dumps({k:{a:round(v[a],3) for a in ['good_tasks','help_hours','annual_cost','cost_per_good','annual_difference']} for k,v in out.items()},ensure_ascii=False))
