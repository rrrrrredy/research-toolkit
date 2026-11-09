"""Arithmetic for source analysis; no model experiment or software tests are run."""
import json
from pathlib import Path

out = Path(__file__).with_name('calculation-record.json')
inventory = 18543*27 + 120*20*80 + 186*7*80 + 3600*4*80
release = 120*20*80 + 186*4*80 + 3600*4*80
budgets = [500,2000,4000,6000,8000,12000,16000]
accuracy = [.282,.378,.465,.502,.538,.558,.549]
mu = [(accuracy[i+1]-accuracy[i])*100/((budgets[i+1]-budgets[i])/500) for i in range(6)]
p,tpr,fpr = .2,.9,.1
s=tpr*p+fpr*(1-p)
result = {
 'producer':'/root/ttc_research',
 'kind':'actual arithmetic over reported or explicitly hypothetical inputs, not reproduction',
 'ttc003v2':{'study_inventory':inventory,'declared_public_release':release,'difference':inventory-release,'broad_block':18543*27,'extra_repeats':186*3*80},
 'ttc005_nominal_schedule':{'steps':50,'proposer_slots':50*2*8,'solver_slots':50*48*8,'total_slots':50*(2*8+48*8),'excluded':'test reconstruction, execution, evaluation, gradients, sequence lengths and invalid proposal handling'},
 'ttc006':{'one_question_percentage_points':100/60,'interval_mu_pp_per_500':mu,'utilities_lambda_0_5':dict(zip(budgets,[a-.5*b/16000 for a,b in zip(accuracy,budgets)])),'flip_endpoint_differences':[142-31,11-83]},
 'ttc007':{'trajectories':6*963*16,'micro_mean_stored_thinking_tokens':576688123/(6*963*16),'single_probe_binomial_sd_p_0_5_n_16':(.25/16)**.5},
 'ttc008_hypothetical':{'p':p,'tpr':tpr,'fpr':fpr,'acceptance_rate':s,'ceiling':tpr*p/s,'selected_success':{n:tpr*p/s*(1-(1-s)**n) for n in [1,4,8,16]},'oracle_coverage_16':1-(1-p)**16},
}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
