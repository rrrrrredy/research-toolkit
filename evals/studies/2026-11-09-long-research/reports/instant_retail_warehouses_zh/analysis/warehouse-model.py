"""Author /root/microdrama_research. CNY, 30-day month; hypothetical warehouse accounts."""
from pathlib import Path
import json,csv,math
B=Path(__file__).resolve().parent
def fixed(p,n):
    return p['fixed_base']+sum(cost for threshold,cost in p['steps'] if n>threshold)
def run(p):
    n=p['daily']; orders=n*30;a=p['aov'];rev=orders*a
    unit=round(a*(p['purchase_margin']-p['loss']-p['platform_rate']-p['franchise_rate'])-p['pick_pack']-p['delivery']-p['ads']+p['subsidy'],10)
    wh=orders*unit-fixed(p,n);full=wh-orders*p['upstream_per_order']-p['hq_fixed']
    inventory=n*(a*(1-p['purchase_margin']+p['loss']))*p['stock_days']
    roots=[]
    for x in range(1,p['capacity']+1):
        if 30*x*(unit-p['upstream_per_order'])-fixed(p,x)-p['hq_fixed']>=0:roots.append(x)
    return {'inputs':p,'orders':orders,'revenue':rev,'unit_contribution':unit,'warehouse_fixed':fixed(p,n),'warehouse_profit':wh,'allocated_full_profit':full,'inventory':inventory,'capacity_feasible':n<=p['capacity'],'minimum_full_breakeven_daily':min(roots) if roots else None,'peak_orders_hour':n*p['peak_fraction'],'pickers_required':math.ceil(n*p['peak_fraction']/(p['picker_rate']*p['picker_use'])),'concurrent_riders_required':math.ceil(n*p['peak_fraction']/(p['rider_rate']*p['rider_use']))}
fresh=dict(mode='fresh self-operated',daily=900,aov=65,purchase_margin=.31,loss=.02,platform_rate=.002,franchise_rate=0,pick_pack=2,delivery=6.5,ads=1,subsidy=0,fixed_base=155000,steps=[(800,20000),(1000,40000)],capacity=1200,upstream_per_order=1.8,hq_fixed=0,stock_days=3,peak_fraction=.12,picker_rate=24,picker_use=.85,rider_rate=4,rider_use=.85,monthly_depreciation=18000)
social=dict(mode='independent social warehouse',daily=400,aov=50,purchase_margin=.3,loss=.01,platform_rate=.05,franchise_rate=0,pick_pack=.8,delivery=4.5,ads=1.2,subsidy=.5,fixed_base=60000,steps=[(450,9000)],capacity=600,upstream_per_order=0,hq_fixed=0,stock_days=21,peak_fraction=.2,picker_rate=45,picker_use=.9,rider_rate=4,rider_use=.85,monthly_depreciation=4000)
cases={'fresh_mature':fresh,'fresh_new':{**fresh,'daily':550,'aov':62,'loss':.025,'delivery':7,'ads':1.5,'upstream_per_order':2.4},'fresh_weak':{**fresh,'daily':400,'aov':60,'purchase_margin':.3,'loss':.035,'pick_pack':2.2,'delivery':7.5,'ads':1.5},'social_base':social,'social_franchise':{**social,'franchise_rate':.02},'social_strong':{**social,'daily':500,'aov':55,'purchase_margin':.32}}
for label,p in [('fresh',fresh),('social',social)]:
    changes={'orders_minus20':{'daily':p['daily']*.8},'orders_plus20':{'daily':p['daily']*1.2},'aov_minus10':{'aov':p['aov']*.9},'margin_minus2pp':{'purchase_margin':p['purchase_margin']-.02},'loss_plus1pp':{'loss':p['loss']+.01},'delivery_plus1':{'delivery':p['delivery']+1},'ads_plus08':{'ads':p['ads']+.8},'no_incentive':{'subsidy':0}}
    for name,c in changes.items():cases[label+'_'+name]={**p,**c}
cases['social_subsidy_withdraw_demand20']={**social,'daily':320,'subsidy':0}
cases['fresh_promote']={**fresh,'daily':1080,'aov':61.75,'purchase_margin':.29,'ads':1.5,'delivery':7}
cases['fresh_radius_extend']={**fresh,'daily':1080,'delivery':8,'peak_fraction':.12,'rider_rate':3}
results={k:run(v) for k,v in cases.items()}
# Same-order cross-entity bridge. Goods net price50, consumer pays48, coupon2 remitted to merchant.
bridge={'consumer_goods':48,'platform_goods_coupon':2,'consumer_delivery_to_platform':2,'merchant_goods_revenue':50,'merchant_incentive':.5,'commission_to_platform':2.5,'merchant_delivery_to_platform':4.5,'merchant_ads_to_platform':1.2,'rider_cost':6.5,'platform_service_cost':1,'platform_refund_service_cost':.2}
bridge['platform_contribution']=2+2.5+4.5+1.2-6.5-1-.2-2-.5
# Same network: existing900, new500 including300 cannibalized => old600, total1100 (net+200).
network={'old_before':run(fresh),'old_after':run({**fresh,'daily':600}),'new':run({**fresh,'daily':500})}
network['profit_delta']=network['old_after']['allocated_full_profit']+network['new']['allocated_full_profit']-network['old_before']['allocated_full_profit']
# Illustrative six-month new-area ramp, capex600k, refundable deposit75k, inventory paid as changes.
cash=-600000-75000; prior_stock=0;ramp=[]
for month,n in enumerate([300,450,600,750,900,950],1):
    p={**fresh,'daily':n,'aov':62,'loss':.025 if month<4 else .02,'delivery':7,'ads':1.5 if month<4 else 1,'upstream_per_order':2.4}
    v=run(p);cash+=v['allocated_full_profit']+p['monthly_depreciation']-(v['inventory']-prior_stock);prior_stock=v['inventory'];ramp.append({'month':month,'daily':n,'profit':v['allocated_full_profit'],'inventory':v['inventory'],'cumulative_cash':cash})
payload={'scenarios':results,'platform_bridge':bridge,'network':network,'ramp':ramp,'assumptions':'No VAT or financing in these operating illustrations; loss is separately excluded from procurement margin; allocated costs are not company audited profit. Rider bill reflects merchant share; consumer shipping excluded from warehouse revenue.'}
(B/'warehouse-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
with (B/'warehouse-results.csv').open('w',newline='',encoding='utf-8-sig') as f:
    keys=['scenario','orders','revenue','unit_contribution','warehouse_fixed','warehouse_profit','allocated_full_profit','inventory','minimum_full_breakeven_daily'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
    for k,v in results.items():w.writerow({'scenario':k,**{a:v[a] for a in keys[1:]}})
print(json.dumps({k:{a:v[a] for a in ['unit_contribution','warehouse_profit','allocated_full_profit','minimum_full_breakeven_daily','inventory','pickers_required','concurrent_riders_required']} for k,v in results.items()},ensure_ascii=False))
print(json.dumps({'bridge':bridge,'network_delta':network['profit_delta'],'ramp':ramp},ensure_ascii=False))
