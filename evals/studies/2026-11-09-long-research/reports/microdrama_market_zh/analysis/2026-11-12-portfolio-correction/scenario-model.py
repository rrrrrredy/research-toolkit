# Arithmetic correction, 2026-11-12. Original script and results remain in the parent directory.
"""Research arithmetic only. All commercial inputs are explicit illustrative assumptions.
Identity: /root/microdrama_research. Not industry estimates or individual deal advice.
Units: RMB yuan, users, days; no tax or financing cost. Horizon 90 days.
"""
from pathlib import Path
import math,json,csv

ROOT=Path(__file__).resolve().parent
PAID=dict(users=100000, conversion=.15, consumed_per_payer=120,
          refund_rate=.08, channel_rate=.05, content_share=.35,
          cac=6.5, operating=120000, budget=600000)
FREE=dict(users=1000000, d1=.4, d7=.2, d30_ratio=.4, d90_ratio=.1,
          slots=12, fill=.85, gross_ecpm=45, network_rate=.15,
          content_share=.35, cac=1.8, operating=300000, budget=600000)

def paid(p):
    gross=p['users']*p['conversion']*p['consumed_per_payer']
    refunds=gross*p['refund_rate']; demand=gross-refunds
    channel=demand*p['channel_rate']; pool=demand-channel
    content=pool*p['content_share']; operator=pool-content
    creator_profit=content-p['budget']; operator_profit=operator-p['users']*p['cac']-p['operating']
    return dict(gross=gross,refunds=refunds,external_demand=demand,channel=channel,
                distributable=pool,content_income=content,creator_profit=creator_profit,
                operator_income=operator,operator_profit=operator_profit,
                combined_profit=creator_profit+operator_profit,
                operator_max_cac=(operator-p['operating'])/p['users'],
                creator_break_even_conversion=p['budget']/(p['users']*p['consumed_per_payer']*(1-p['refund_rate'])*(1-p['channel_rate'])*p['content_share']))

def curve(p):
    anchors=[(0,1),(1,p['d1']),(7,p['d7']),(30,p['d7']*p['d30_ratio']),(90,p['d7']*p['d90_ratio'])]
    values=[]
    for day in range(91):
        for (da,ra),(db,rb) in zip(anchors,anchors[1:]):
            if da<=day<=db:
                values.append(ra*(rb/ra)**((day-da)/(db-da)));break
    return values

def free(p):
    days=sum(curve(p)); impressions=p['users']*days*p['slots']*p['fill']
    demand=impressions*p['gross_ecpm']/1000
    channel=demand*p['network_rate']; pool=demand-channel
    content=pool*p['content_share']; operator=pool-content
    creator_profit=content-p['budget']; operator_profit=operator-p['users']*p['cac']-p['operating']
    return dict(active_days_per_user=days,filled_impressions=impressions,external_demand=demand,
                channel=channel,distributable=pool,content_income=content,operator_income=operator,
                creator_profit=creator_profit,operator_profit=operator_profit,
                combined_profit=creator_profit+operator_profit,
                operator_max_cac=(operator-p['operating'])/p['users'],
                operator_break_even_gross_ecpm=(p['users']*p['cac']+p['operating'])/(impressions/1000*(1-p['network_rate'])*(1-p['content_share'])))

results=[]
def scenario(mode,name,changes):
    base=PAID if mode=='paid' else FREE
    params={**base,**changes}; out=(paid if mode=='paid' else free)(params)
    results.append(dict(mode=mode,scenario=name,parameters=params,results=out))
for mode,base in [('paid',PAID),('free',FREE)]:
    scenario(mode,'base',{})
    for label,key,change in [('budget_minus30','budget',.7),('budget_plus30','budget',1.3),
                             ('cac_minus20','cac',.8),('cac_plus20','cac',1.2)]:
        scenario(mode,label,{key:base[key]*change})
    scenario(mode,'share_30',{'content_share':.3});scenario(mode,'share_40',{'content_share':.4})
scenario('paid','conversion_minus20',{'conversion':.12})
scenario('paid','conversion_plus20',{'conversion':.18})
scenario('paid','refund_15',{'refund_rate':.15})
scenario('free','ecpm_minus20',{'gross_ecpm':36})
scenario('free','ecpm_plus20',{'gross_ecpm':54})
scenario('free','d7_minus5pp',{'d7':.15})
scenario('free','d7_plus5pp',{'d7':.25})
scenario('free','adload_retention_joint',{'slots':15,'d7':.14})
scenario('free','admarket_acquisition_joint',{'gross_ecpm':36,'cac':2.16,'d7':.15})

def cashflow(mode,delay):
    p=PAID if mode=='paid' else FREE; r=paid(p) if mode=='paid' else free(p)
    gross_daily=curve(p) if mode=='free' else [math.exp(-d/15) for d in range(91)]
    weights=[x/sum(gross_daily) for x in gross_daily]
    total={d:0.0 for d in range(-60,181)};operator=total.copy();creator=total.copy()
    for day,fraction in [(-60,.3),(-30,.5),(0,.2)]: creator[day]-=p['budget']*fraction
    operator[0]-=p['users']*p['cac']
    for d in range(91):
        operator[d]-=p['operating']/91
        creator[d+delay]+=r['content_income']*weights[d]
        operator[d+delay]+=r['operator_income']*weights[d]
    rows=[]; oc=cc=0
    for d in total:
        oc+=operator[d];cc+=creator[d]
        rows.append(dict(day=d,operator_cumulative=oc,creator_cumulative=cc,combined_cumulative=oc+cc))
    summary={k: -min(0,min(x[k] for x in rows)) for k in ['operator_cumulative','creator_cumulative','combined_cumulative']}
    summary['combined_final']=rows[-1]['combined_cumulative'];summary['delay_days']=delay
    with (ROOT/f'cashflow-{mode}-{delay}days.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    return summary

f=free(FREE); guarantee=600000
contracts=[]
for name,content in [('pure_share',f['content_income']),('recoupable_minimum',max(guarantee,f['content_income'])),
                     ('nonrecoupable_additional_grant',guarantee+f['content_income'])]:
    contracts.append(dict(contract=name,creator_income=content,creator_profit=content-FREE['budget'],
                          operator_profit=f['distributable']-content-FREE['users']*FREE['cac']-FREE['operating']))
down=free({**FREE,'gross_ecpm':20})
contracts_down=[]
for name,content in [('pure_share',down['content_income']),('recoupable_minimum',max(guarantee,down['content_income'])),
                     ('nonrecoupable_additional_grant',guarantee+down['content_income'])]:
    contracts_down.append(dict(contract=name,creator_income=content,creator_profit=content-FREE['budget'],
                               operator_profit=down['distributable']-content-FREE['users']*FREE['cac']-FREE['operating']))
margin=f['distributable']-FREE['users']*FREE['cac']-FREE['operating']-FREE['budget']
contracts.append(dict(contract='platform_pays_cost_then_splits_surplus_50_50',creator_income=FREE['budget']+max(0,margin)*.5,
                      creator_profit=max(0,margin)*.5,operator_profit=margin-max(0,margin)*.5))

hybrid=[]
for relative_advalue in [1,3,6]:
    subscribers=50000;price=15;fee=.05;extra_service_cost=50000
    fee_net=subscribers*price*(1-fee)
    lost_ads=subscribers*f['distributable']/FREE['users']*relative_advalue
    hybrid.append(dict(relative_advalue=relative_advalue,net_subscription=fee_net,lost_ad_receipts=lost_ads,
                       incremental_before_content_resplit=fee_net-lost_ads-extra_service_cost,
                       break_even_price=(lost_ads+extra_service_cost)/(subscribers*(1-fee))))

# Arithmetic reconciliation checks, not a software-test suite.
for row in results:
    r=row['results'];p=row['parameters']
    assert abs(r['external_demand']-r['channel']-r['content_income']-r['operator_income'])<.0001
    assert abs(r['combined_profit']-(r['distributable']-p['users']*p['cac']-p['operating']-p['budget']))<.0001

portfolio=dict(failure_pool=300000,ordinary_pool=1000000,hit_pool=5000000,
               probabilities=[.6,.3,.1],content_share=.35,budget=600000)
portfolio['mean_pool']=sum(pool*probability for pool,probability in zip(
    (portfolio['failure_pool'],portfolio['ordinary_pool'],portfolio['hit_pool']),portfolio['probabilities']))
portfolio['mean_creator_profit']=portfolio['mean_pool']*portfolio['content_share']-portfolio['budget']
portfolio['required_mean_pool']=portfolio['budget']/portfolio['content_share']
non_hit_mean=(portfolio['failure_pool']*portfolio['probabilities'][0]
              +portfolio['ordinary_pool']*portfolio['probabilities'][1])/sum(portfolio['probabilities'][:2])
portfolio['break_even_hit_rate']=(portfolio['required_mean_pool']-non_hit_mean)/(portfolio['hit_pool']-non_hit_mean)

output=dict(identity='/root/microdrama_research',assumption_status='All commercial parameters hypothetical, not estimates',
            paid_inputs=PAID,free_inputs=FREE,scenarios=results,contracts_base=contracts,contracts_down_ecpm20=contracts_down,
            cashflows={mode:[cashflow(mode,d) for d in [7,30,60]] for mode in ['paid','free']},hybrid=hybrid,
            portfolio=portfolio)
(ROOT/'scenario-results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
rows=[{'mode':r['mode'],'scenario':r['scenario'],**r['results']} for r in results]
keys=list(dict.fromkeys(k for r in rows for k in r))
with (ROOT/'scenario-results.csv').open('w',encoding='utf-8-sig',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=keys);w.writeheader();w.writerows(rows)
print(json.dumps({k:output[k] for k in ['cashflows','contracts_base','contracts_down_ecpm20','hybrid','portfolio']},ensure_ascii=False,indent=2))
for r in results:
    v=r['results'];print(r['mode'],r['scenario'],*(round(v[k]/10000,3) for k in ['external_demand','creator_profit','operator_profit','combined_profit']))
print(f'Funds reconciled in all {len(results)} scenarios; output arithmetic only.')
