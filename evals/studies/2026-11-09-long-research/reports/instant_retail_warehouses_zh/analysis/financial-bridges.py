"""Author arithmetic for cited statements and clearly assumed scenarios; no software tests."""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
out={
 'missfresh_2021_million':{'revenue':6951.535,'cost':6131.038,'gross':6951.535-6131.038,'fulfillment':2121.370,'gross_less_fulfillment':6951.535-6131.038-2121.370},
 'dingdong_2026q2_million':{'reported_net':271.7,'ceased_depreciation_effect':199.1,'mechanical_ex_effect':271.7-199.1,'prior_net':107.2},
 'demand':{'mature_social':10000*.45*6*.45/30,'new_neighborhood':5000*.35*6*.4/30,'fresh_share_at_697':697*30/(10000*.5*8)},
 'store_incremental':{'daily':200,'contribution_without_incentive':5.5,'incremental_fixed':20000,'incremental_result':200*30*5.5-20000,'full_allocated_fixed':60000,'full_allocated_result':200*30*5.5-60000},
 'inventory_opportunity_cost_monthly_8pct':{'fresh':124605*.08/12,'social':298200*.08/12},
 'social_baseline_cash_simplification':{'monthly_profit':12000,'monthly_depreciation':4000,'monthly_operating_cash_before_stockchanges':16000,'assumed_equipment':120000,'assumed_deposit':30000,'opening_stock':298200,'total_initial':448200,'simple_months':448200/16000},
 'peak_capacity':{'fresh_6pickers_perhour':6*24*.85,'social_2pickers_perhour':2*45*.9,'social_3pickers_perhour':3*45*.9},
}
(B/'financial-bridges.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
