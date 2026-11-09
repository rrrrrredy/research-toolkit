"""Executed analytical scenarios; all scenario inputs are assumptions, not platform terms."""
import json
from pathlib import Path

def paid(conversion=.04,cac=1.2,budget=600000,refund=.05):
    n=1_000_000; spend=75; fee=.10; royalty=.10
    gross=n*conversion*spend; refunds=gross*refund; consumption=gross-refunds
    channel=consumption*fee; settlement=consumption-channel
    rights=settlement*royalty; acquisition=n*cac
    residual=settlement-rights-acquisition-budget
    # Contract assumption: producer recoups budget before equal surplus split.
    pool=settlement-rights-acquisition
    producer_cash=max(0,min(pool,budget))+max(residual,0)*.5
    distributor_cash=max(residual,0)*.5
    return dict(conversion=conversion,cac=cac,production=budget,gross=gross,refunds=refunds,consumed_net_refunds=consumption,channel_fee=channel,settlement=settlement,rights=rights,media=acquisition,project_surplus=residual,producer_cash=producer_cash,producer_profit=producer_cash-budget,distributor_cash=distributor_cash)

def free(days=14,completion=.6,share=.35,cac=.7,budget=600000):
    n=1_000_000; opportunities=4+8*completion; fill=.8; ecpm=20; network=.2; operating=100000
    # completion is fraction reaching the later episode block; no inferred actual retention.
    impressions=n*days*opportunities*fill
    advertising=impressions*ecpm/1000
    network_cash=advertising*network; publisher=advertising-network_cash
    content=publisher*share; platform=publisher-content
    return dict(days=days,later_block_completion=completion,content_share=share,impressions=impressions,advertiser_cash=advertising,network_cash=network_cash,publisher_net=publisher,content_cash=content,producer_profit=content-budget,platform_before_cost=platform,platform_profit=platform-n*cac-operating,joint_surplus=publisher-budget-n*cac-operating)

out={
 'input_status':'All commercial scenario inputs are expressly assumed; actual quoted figures below preserve source denominators. Excludes tax, financing and unspecified corporate overhead.',
 'observed_arithmetic':{
  'cnn_users_pct':(664/662-1)*100,
  'feb_cross_channel_overlap_millions':335+427-718,
  'feb_overlap_pct_app':44/335*100,
  'jan2025_minutes_per_app_use':13*60/62,
  'may2026_minutes_per_app_use':26.9*60/125.6,
  'monthly_hours_pct':(26.9/13-1)*100,
  'monthly_uses_pct':(125.6/62-1)*100,
  'minutes_per_use_pct':((26.9/125.6)/(13/62)-1)*100,
  'sept_hongguo_app_penetration_pct':429.69/487*100,
  'may_channels_sum_millions':402+508+14,
  'may_sum_minus_union_millions':402+508+14-851,
  'col_2025_gross_profit':1656556589.87-1057239561.26,
  'col_2025_gross_less_sales':1656556589.87-1057239561.26-953175245.88,
  'ireader_2025_gross_profit':3242735278.10-1002002285.45,
  'ireader_2025_gross_less_sales':3242735278.10-1002002285.45-2078568856.21,
  'ireader_promotion_to_sales_pct':1985608898.44/2078568856.21*100,
  'col_q3_cashflow_derived':42795996.82-126801681.39,
  'ireader_q3_cashflow_derived':52734303.86-(-116528498.87)
 },
 'paid_base':paid(),
 'paid_sensitivity':[paid(c,cac) for c in [.025,.04,.055] for cac in [1.,1.2,1.4]],
 'paid_budget_sensitivity':[paid(budget=b) for b in [400000,600000,1000000]],
 'paid_refund_sensitivity':[paid(refund=r) for r in [.02,.05,.12]],
 'paid_break_even_conversion':(1200000+600000)/(1000000*75*.95*.9*.9),
 'free_base':free(),
 'free_sensitivity':[free(d,c) for d in [10,14,18] for c in [.4,.6,.8]],
 'free_share_sensitivity':[free(share=s) for s in [.25,.35,.45]],
 'free_break_even_active_days_producer':600000/(1000000*8.8*.8*.02*.8*.35),
 'free_break_even_active_days_platform':800000/(1000000*8.8*.8*.02*.8*.65),
 'gold_scenario':{
  'assumed_incentive_cost_removed':60000,
  'base_operating_cost_includes_incentive':100000,
  'max_days_lost_before_saving_erased':60000/(1000000*8.8*.8*.02*.8*.65),
  'max_active_day_loss_pct':60000/(1000000*14*8.8*.8*.02*.8*.65)*100
 },
 'hybrid_scenario':{
  'converters':50000,'price':7,'refund':.05,'payment_fee':.10,
  'net_payment':50000*7*.95*.9,
  'ad_net_displaced_average_viewer':free()['publisher_net']*.05,
  'increment_before_new_costs_average_viewer':50000*7*.95*.9-free()['publisher_net']*.05,
  'increment_before_new_costs_double_ad_value_viewer':50000*7*.95*.9-free()['publisher_net']*.10
 }
}
# Financial reconciliation is calculation verification, not a software test suite.
b=out['paid_base']
assert abs(b['gross']-sum(b[k] for k in ['refunds','channel_fee','rights','media','producer_cash','distributor_cash']))<1e-6
f=out['free_base']
assert abs(f['advertiser_cash']-f['network_cash']-f['content_cash']-f['platform_before_cost'])<1e-6
Path(__file__).with_name('calculation-output.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
