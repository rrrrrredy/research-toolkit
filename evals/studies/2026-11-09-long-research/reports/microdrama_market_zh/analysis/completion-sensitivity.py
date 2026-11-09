"""Explicit completion extension for the research report; no observed industry rates."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
baseline=json.loads((p/'scenario-results.json').read_text(encoding='utf-8'))
params=baseline['free_inputs']
base=next(x['results'] for x in baseline['scenarios'] if x['mode']=='free' and x['scenario']=='base')
rows=[]
for completion in [.45,.60,.75]:
    # Hypothesis only: 20 episode starts per active day; one ad opportunity
    # after each completed episode; all other behavior and price fixed.
    slots=20*completion
    ratio=slots/params['slots']
    demand=base['external_demand']*ratio
    pool=base['distributable']*ratio
    content=pool*params['content_share']
    operator=pool-content
    rows.append(dict(completion=completion,episode_starts_per_active_day=20,
                     ad_opportunities_per_active_day=slots,external_demand=demand,
                     content_profit=content-params['budget'],
                     operator_profit=operator-params['users']*params['cac']-params['operating'],
                     combined_profit=pool-params['budget']-params['users']*params['cac']-params['operating']))
out=dict(identity='/root/microdrama_research',status='illustrative assumptions, not estimates',
         mechanism='ad opportunity occurs after completed episode; retention held fixed',rows=rows)
(p/'completion-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
