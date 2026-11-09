"""Author arithmetic, not a model benchmark or software test. All quality/time/traffic inputs are scenarios."""
from pathlib import Path
from datetime import datetime,timezone
import json
B=Path(__file__).resolve().parent
RATE={'haiku55':{'input':.1,'output':.5,'write5':.125,'write60':.2,'read':.01},
      'sonnet55':{'input':2,'output':10,'write5':2.5,'write60':4,'read':.1},
      'opus55':{'input':4,'output':20,'write5':5,'write60':8,'read':.2}}
def call(model,i,o):
 r=RATE[model];return (i*r['input']+o*r['output'])/1e6
def support(strong_first=False,wage=.5,review_min=1,output_scale=1,retry_success=.4):
 n=1000
 if strong_first:
  first=900; retry_n=100;retry_ok=50;fallback_n=0;fallback_ok=0;human_n=50;human_ok=46
  api=n*call('sonnet55',1500,500*output_scale)+retry_n*call('sonnet55',3500,500*output_scale)
 else:
  first=700;retry_n=300;retry_ok=retry_n*retry_success;fallback_n=retry_n-retry_ok;fallback_ok=.6*fallback_n
  human_n=fallback_n-fallback_ok;human_ok=human_n*(66/72)
  api=n*call('haiku55',1500,500*output_scale)+retry_n*call('haiku55',2500,500*output_scale)+fallback_n*call('sonnet55',3500,500*output_scale)
 machine=first+retry_ok+fallback_ok;accepted=machine+human_ok
 human_minutes=human_n*6+machine*.05*review_min
 overhead=1.2
 total=api+human_minutes*wage+overhead
 return dict(strategy='strong_first' if strong_first else 'cheap_first',incoming=n,first_accepted=first,retry_attempts=retry_n,retry_accepted=retry_ok,fallback_attempts=fallback_n,fallback_accepted=fallback_ok,human_attempts=human_n,human_accepted=human_ok,accepted=accepted,unresolved=n-accepted,api_usd=api,human_minutes=human_minutes,human_usd=human_minutes*wage,other_usd=overhead,total_usd=total,cost_per_incoming=total/n,cost_per_accepted=total/accepted)
TIMES=[0,2,4,10,12,14,30,32,34,90,92,94]
def cache_queries(ttl,changed_at=(),output=800):
 r=RATE['sonnet55'];expiry=-1;rows=[];prefix=120000
 for t in TIMES:
  if t in changed_at:expiry=-1
  status='read' if ttl and t<expiry else 'write' if ttl else 'uncached'
  p=r['read'] if status=='read' else r['write5' if ttl==5 else 'write60'] if ttl else r['input']
  if ttl:expiry=t+ttl
  prefix_cost=prefix*p/1e6;other=call('sonnet55',1000,output)
  rows.append(dict(minute=t,prefix_tokens=prefix,status=status,expires_at=expiry if ttl else None,prefix_usd=prefix_cost,new_input_output_usd=other,total_usd=prefix_cost+other))
 return dict(ttl_min=ttl,changed_at=list(changed_at),rows=rows,api_usd_per_set=sum(x['total_usd'] for x in rows),writes=sum(x['status']=='write' for x in rows),reads=sum(x['status']=='read' for x in rows))
def documents(strategy,quality=.9,review_min=.5,wage=1,changed_at=(),output=800):
 sets=100;tasks=sets*12
 if strategy=='rag':
  api=tasks*call('sonnet55',11000,output);preparation=sets*3;retrieval=tasks*.002
 else:
  ttl={'uncached':0,'cache5':5,'cache60':60}[strategy]
  api=sets*cache_queries(ttl,changed_at,output)['api_usd_per_set'];preparation=sets*2;retrieval=0
 failures=tasks*(1-quality);accepted=tasks*quality+failures*.9
 human_minutes=tasks*review_min+failures*6
 total=api+preparation+retrieval+human_minutes*wage
 return dict(strategy=strategy,first_quality=quality,incoming=tasks,first_accepted=tasks*quality,repair_attempts=failures,repair_accepted=failures*.9,accepted=accepted,unresolved=tasks-accepted,api_usd=api,preparation_usd=preparation,retrieval_usd=retrieval,human_minutes=human_minutes,total_usd=total,cost_per_incoming=total/tasks,cost_per_accepted=total/accepted)
def trajectory(model,contexts,out_per_step,output_scale=1):
 r=RATE[model];prev=0;rows=[]
 for k,total in enumerate(contexts,1):
  new=total-prev;cost=(new*r['write5']+prev*r['read']+out_per_step*output_scale*r['output'])/1e6
  rows.append(dict(step=k,input_total=total,cache_read=prev,cache_write=new,output_total=out_per_step*output_scale,cost_usd=cost));prev=total
 return dict(model=model,rows=rows,total_usd=sum(x['cost_usd'] for x in rows),sum_input=sum(contexts),sum_output=out_per_step*len(contexts)*output_scale)
def agents(strong_first=False,wage=1,output_scale=1,first_review=3,retry_success=.4):
 n=100;model='opus55' if strong_first else 'sonnet55'
 base=trajectory(model,[4000,8000,14000,22000,32000,44000,58000,74000],2000,output_scale)
 retry=trajectory(model,[24000,36000,50000],3000,output_scale)
 compact=call(model,74000,2000*output_scale)
 fallback=trajectory('opus55',[30000,45000,60000],4000,output_scale)
 first=75 if strong_first else 60;retry_n=n-first;retry_ok=retry_n*retry_success
 remaining=retry_n-retry_ok;fallback_n=0 if strong_first else remaining;fallback_ok=.5*fallback_n
 human_n=remaining if strong_first else remaining-fallback_ok
 human_ok=human_n*(.8 if strong_first else 2/3)
 accepted=first+retry_ok+fallback_ok+human_ok
 api=n*base['total_usd']+retry_n*(retry['total_usd']+compact)+fallback_n*fallback['total_usd']
 tools=n*.2+retry_n*.15+fallback_n*.25
 minutes=n*first_review+retry_n*2+fallback_n*3+human_n*20
 total=api+tools+minutes*wage
 return dict(strategy='strong_first' if strong_first else 'standard_first',incoming=n,first_accepted=first,retry_attempts=retry_n,retry_accepted=retry_ok,fallback_attempts=fallback_n,fallback_accepted=fallback_ok,human_attempts=human_n,human_accepted=human_ok,accepted=accepted,unresolved=n-accepted,base=base,retry=retry,compaction_usd_each=compact,fallback=fallback,api_usd=api,tools_usd=tools,human_minutes=minutes,total_usd=total,cost_per_incoming=total/n,cost_per_accepted=total/accepted)
def host(nodes=1,monthly_tasks=1e6,qps_capacity=10,q_local=.9,q_api=.9,api_model='sonnet55'):
 hours=730;fixed=nodes*13.96*hours+3000+300
 api_unit=call(api_model,512,256)
 cap=nodes*qps_capacity*hours*3600
 crossover=fixed*q_api/(api_unit*q_local)
 return dict(nodes=nodes,node_rate_usd_hour=13.96,host_usd_month=fixed,api_unit_usd=api_unit,monthly_tasks=monthly_tasks,capacity_tasks=cap,load_fraction=monthly_tasks/cap,local_quality=q_local,api_quality=q_api,local_cost_per_accepted=fixed/(monthly_tasks*q_local),api_cost_per_accepted=api_unit/q_api,break_even_requests=crossover,break_even_capacity_fraction=crossover/cap)
results={'author':'/root/ttc_research','generated_at':datetime.now(timezone.utc).isoformat(),'status':'executed deterministic scenario arithmetic; no measured model success or latency',
 'rates':RATE,'rate_source':'TE05 dated 2026-10-22 Claude API global standard USD/MTok; tool prices separate',
 'training':{'gpu_hours':2664000+119000+5000,'usd_at_2_per_gpu_hour':(2664000+119000+5000)*2},
 'allocation':[dict(investment_usd=f,allocated_share=a,lifetime_output_tokens=q,allocation_usd_per_million=f*a/q*1e6) for f in [1e7,1e8,1e9] for a in [.25,1] for q in [1e12,1e13]],
 'support':[support(),support(True)],
 'support_wage':[dict(wage_usd_min=w,rows=[support(False,w),support(True,w)]) for w in [0,.1,.5,1]],
 'support_retry':[dict(conditional_retry_success=p,row=support(retry_success=p)) for p in [.1,.4,.7]],
 'support_output':[dict(output_scale=m,rows=[support(output_scale=m),support(True,output_scale=m)]) for m in [.5,1,2,4]],
 'cache_ledgers':[cache_queries(x) for x in [0,5,60]]+[cache_queries(60,changed_at=(30,90))],
 'documents':[documents(s,.86 if s=='rag' else .9) for s in ['uncached','cache5','cache60','rag']],
 'document_quality':[documents(s,q) for s in ['cache60','rag'] for q in [.86,.9,.94]],
 'document_output':[dict(output=m,row=documents('cache60',output=m)) for m in [400,800,1600]],
 'agents':[agents(),agents(True)],
 'agent_output':[dict(output_scale=m,row=agents(output_scale=m)) for m in [.5,1,2,4]],
 'agent_retry':[dict(conditional_retry_success=p,row=agents(retry_success=p)) for p in [.1,.4,.7]],
 'agent_review':[dict(review_min=m,row=agents(first_review=m)) for m in [1,3,6]],
 'hosting':[host(nodes=n,monthly_tasks=v,q_local=q,api_model=a) for n in [1,2] for v in [1e5,1e6,1e7] for q in [.8,.9] for a in ['haiku55','sonnet55']],
 'google_cache':{'prefix_tokens':120000,'hours':1,'queries':12,'input_rate':.3,'read_rate':.03,'storage_rate_per_million_hour':1,'storage_usd':.12,'prefix_reads_usd':12*.12*.03,'uncached_prefix_usd':12*.12*.3,'break_even_queries_storage_only':1/(.3-.03)},
 'threshold':{'gemini25pro_200000in_800out':200000*1.25/1e6+800*10/1e6,'gemini25pro_200001in_800out':200001*2.5/1e6+800*15/1e6},
 'historical_calibration':{'gpt4omini_1500in_500out':(1500*.15+500*.6)/1e6,'gpt41_1500in_500out':(1500*2+500*8)/1e6},
 'research_variant':{'search_success':20,'fetch_success':40,'deepseek_total_usd':60*.75/1000,'openai_search_call_fees_usd':20*10/1000,'openai_search_content_tokens_excluded':True},
 'derived_checks':{'support_equal_accepted_cost_wage_usd_min':(10.4*994-3.91*996)/(478.4*996-347.5*994),'support_false_accepted_unseen_at_1pct_error':928*.01*.95,'document_repair_cost_per_1pp_quality':1200*.01*6,'claude_cache5_uncached_reuse_threshold':(1.25-.05)/(1-.05),'claude_cache60_uncached_reuse_threshold':(2-.05)/(1-.05),'google24h_prefix_storage':.12*24}}
(B/'calculation-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for key in ['support','documents','agents','cache_ledgers']:
 print(key,json.dumps([{k:v for k,v in r.items() if k not in ['rows','base','retry','fallback']} for r in results[key]],ensure_ascii=False))
print('hosting_example',json.dumps(host()))
