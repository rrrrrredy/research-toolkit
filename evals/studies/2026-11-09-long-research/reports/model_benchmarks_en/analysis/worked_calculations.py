"""Interpretation arithmetic only: no model evaluation or measured new success rates."""
from decimal import Decimal as D
from math import sqrt
import json
from pathlib import Path

results = {
    'scope': 'Arithmetic on cited rounded tables and explicitly hypothetical illustrations; no model runs.',
    'mmlu_pro_gpt4o_cot_minus_direct_pp': str(D('72.6')-D('53.5')),
    'humaneval_phind_minus_chatgpt_pp': str(D('71.3')-D('73.2')),
    'humaneval_plus_phind_minus_chatgpt_pp': str(D('67.1')-D('63.4')),
    'tau_equal_domain_mean_percent': str((D('61.2')+D('35.2'))/2),
    'tau_task_weighted_from_rounded_rates_percent': str((D('61.2')*115+D('35.2')*50)/165),
    'hypothetical_homogeneous_independent_success': {
        'p': '0.60', 'k': 4,
        'at_least_one_percent': str((1-(1-D('.6'))**4)*100),
        'all_four_percent': str(D('.6')**4*100),
        'not_an_estimate_from_tau_trajectories': True,
    },
    'hypothetical_binomial_standard_error_pp': sqrt(.8*.2/500)*100,
    'alpaca_verbosity_raw_range_pp': str(D('64.3')-D('22.9')),
    'alpaca_verbosity_length_adjusted_range_pp': str(D('51.6')-D('41.9')),
}
destination=Path(__file__).with_name('worked-calculations.json')
destination.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results))
