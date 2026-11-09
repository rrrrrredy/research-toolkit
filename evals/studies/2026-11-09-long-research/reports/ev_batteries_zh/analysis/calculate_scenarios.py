"""Transparent decision scenarios, not measured factory costs or battery tests."""
import json
from pathlib import Path

out = {'status':'author_scenarios_not_company_estimates',
       'cost_unit':'normalized cost units per nominal kWh; not USD or RMB',
       'formula':'C=(M+V-r*M*(1-y))/y + F/(u*y) + B',
       'inputs':{'M':50,'V':10,'F':10,'B':15,'scrap_material_recovery_fraction_r':0.5},
       'definition':'y is energy-weighted final cell yield; u is line utilization before quality rejects; B is pack cost per saleable nominal kWh. No pack rejects modelled.'}
def cost(M=50,V=10,F=10,B=15,r=.5,y=.95,u=.85):
    return (M+V-r*M*(1-y))/y+F/(u*y)+B
out['yield_utilization']=[{'yield':y,'utilization':u,'cost':round(cost(y=y,u=u),3)} for y in [.95,.85,.70] for u in [.85,.60,.40]]
baseline=cost()
out['maturity_comparison']={'mature':baseline,'new_material_minus20percent_but_ramp':cost(M=40,y=.7,u=.4), 'new_at_same_yield_utilization':cost(M=40)}
out['available_energy']=[{'usable_fraction':f,'cost_per_usable_kwh':round(baseline/f,3)} for f in [.9,.8]]
out['charging']={'nominal_kwh':60,'soc_window':[.1,.8],'energy_kwh':42,'time_minutes':15,'average_cell_power_kw':168,'assumed_wall_to_battery_efficiency':.94,'wall_average_kw':168/.94}
lfp_lce=(73.89/2)/157.76/(160*3.2/1000)
nmc_lce=(73.89/2)/97.28/(190*3.65/1000)
nmc_ni=(.8*58.69)/97.28/(190*3.65/1000)
out['material_stoichiometry_scenario']={'basis':'cathode stoichiometry only, lithium carbonate equivalent; excludes electrode manufacturing losses and excess lithium; capacities and voltages are chosen scenario inputs, not product measurements', 'LFP_assumed_Ah_per_kg':160,'LFP_assumed_V':3.2,'NMC811_assumed_Ah_per_kg':190,'NMC811_assumed_V':3.65,'LFP_kg_LCE_per_kwh':lfp_lce,'NMC811_kg_LCE_per_kwh':nmc_lce,'NMC811_kg_Ni_per_kwh':nmc_ni,'ten_USD_per_kg_LCE_shock_USD_per_kwh':{'LFP':10*lfp_lce,'NMC811':10*nmc_lce},'five_USD_per_kg_Ni_shock_USD_per_kwh':5*nmc_ni}
out['vehicle_constraints']={'nominal_kwh':75,'at160Whkg_pack_kg':75000/160,'at255Whkg_pack_kg':75000/255,'qualification':'same hypothetical energy applied to distinct 2022 manufacturer pack density claims, not measured vehicle mass difference'}
out['utilization_value']={'minutes_saved_per_day':15,'days_per_year':300,'years':4,'value_RMB_per_hour_assumed':50,'undiscounted_gross_RMB':15/60*300*4*50,'scope':'excludes charging fees, queues, opportunity saturation, infrastructure capex and discounting'}
out['throughput_example']={'A':{'pack_cost_RMB':60000,'nominal_kwh':60,'usable_fraction':.9,'full_usable_window_cycles':2000,'mean_capacity_factor':.9},'B':{'pack_cost_RMB':70000,'nominal_kwh':75,'usable_fraction':.9,'full_usable_window_cycles':1600,'mean_capacity_factor':.9},'scope':'synthetic inputs; cyclic throughput only, no calendar limit or vehicle energy effects'}
for v in out['throughput_example'].values():
    if isinstance(v,dict):
        v['throughput_kwh']=v['nominal_kwh']*v['usable_fraction']*v['full_usable_window_cycles']*v['mean_capacity_factor']
        v['capex_RMB_per_kwh']=v['pack_cost_RMB']/v['throughput_kwh']
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
