"""Illustrative scenarios, not product measurements. Currency: assumed RMB."""
import json
from pathlib import Path

def scenario(name,n,manual,brief,verify,failure,rework,fixed,variable,hourly,loss):
    net_minutes=n*(manual-brief-verify-failure*rework)
    cash_cost=fixed+n*variable
    net_value=net_minutes/60*hourly-cash_cost-loss
    return dict(name=name,assumptions=dict(tasks_per_month=n,manual_minutes=manual,brief_minutes=brief,verify_minutes=verify,failure_probability=failure,rework_minutes=rework,monthly_fixed_cost=fixed,per_task_cost=variable,time_value_per_hour=hourly,monthly_expected_external_loss=loss),net_minutes=round(net_minutes,2),cash_cost=cash_cost,net_value=round(net_value,2))

results=[scenario('高频票据草稿',20,20,2,4,.15,15,100,1,60,0),scenario('同任务但核对负担高',20,20,2,10,.30,20,100,1,60,0),scenario('低频旅行整理',2,90,10,20,.20,30,100,5,60,0),scenario('旅行整理附带外部损失敏感性',2,90,10,20,.20,30,100,5,60,40)]
out={'kind':'author_assumed_sensitivity_not_empirical','formula':'N*(manual-brief-verify-p_failure*rework)/60*hourly-fixed-N*variable-expected_external_loss','scenarios':results,'break_even_tasks_first_scenario':100/((20-2-4-.15*15)/60*60-1)}
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
