"""Illustrative merchant economics and randomized holdout, not real campaign data."""
import json, math
from pathlib import Path

def merchant(name,refund,cogs,fee,affiliate,fulfil,return_cost,creative,organic_orders):
    orders=1000; price=100; ad=20000
    kept=orders*(1-refund); sales=kept*price
    before_ad=sales*(1-cogs-fee-affiliate)-orders*fulfil-orders*refund*return_cost
    profit=before_ad-ad-creative
    # Counterfactual same order economics; naturally occurring orders incur fulfilment/returns too.
    baseline=before_ad*organic_orders/orders
    incremental=before_ad-baseline-ad-creative
    return dict(name=name,assumptions=dict(orders=orders,price=price,ad_spend=ad,refund_fraction=refund,cogs_fraction_retained_sales=cogs,fee_fraction_retained_sales=fee,affiliate_fraction_retained_sales=affiliate,fulfil_per_original_order=fulfil,extra_return_cost=return_cost,creative_cost=creative,counterfactual_orders=organic_orders),gross_roas=orders*price/ad,retained_revenue=sales,pre_ad_contribution=before_ad,accounting_contribution=profit,counterfactual_contribution=baseline,incremental_contribution=incremental,incremental_retained_revenue_roas=(sales-sales*organic_orders/orders)/ad,breakeven_incremental_pre_ad_margin=ad+creative)

rows=[merchant('A低退货低佣金',.10,.40,.05,.05,5,5,2000,300),merchant('B高退货高佣金',.30,.40,.05,.15,5,5,2000,600)]
n=10000; t=500; c=400; diff=t/n-c/n
se=math.sqrt((t/n)*(1-t/n)/n+(c/n)*(1-c/n)/n)
out={'kind':'author_assumed_sensitivity_not_empirical','currency':'RMB','merchant_scenarios':rows,'holdout':dict(randomized_equal_groups_assumed=True,users_each=n,treatment_conversions=t,control_conversions=c,absolute_lift_pp=round(diff*100,4),relative_lift=round(diff/(c/n),4),incremental_conversions=round(diff*n),approx_95pct_CI_pp=[round((diff-1.96*se)*100,4),round((diff+1.96*se)*100,4)],assumed_spend=10000,cpic=10000/(diff*n)),'marginal_reinvestment':dict(additional_spend=5000,additional_retained_sales=12000,pre_ad_margin=.40,incremental_profit=12000*.40-5000),'repeat_sensitivity':dict(incremental_new_customers=100,repeat_probability=.30,repeat_pre_marketing_contribution=40,retention_cost=200,discount_factor=.95,expected_future_contribution=100*.30*40*.95-200)}
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
