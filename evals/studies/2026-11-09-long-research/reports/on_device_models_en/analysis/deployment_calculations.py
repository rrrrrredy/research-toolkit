"""Author arithmetic, not model inference or software tests. All scenarios labelled."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
GiB=2**30; MiB=2**20
kv_per_token=2*36*2*128*2
index=10000*384*2*1.5
fixed=1.8+.6+.25+index/GiB+.35+.5
memory={'architecture':'Qwen2.5-3B-Instruct official config; BF16 KV; batch 1',
 'raw_weight_GiB':{str(bits):3.09e9*bits/8/GiB for bits in [16,8,4,2]},
 'kv_bytes_per_token':kv_per_token,'index_bytes':index,'index_MiB':index/MiB,
 'scenario_fixed_GiB':fixed,'phone_budget_GiB':4,'PC_budget_GiB':10,
 'phone_Q4':{},'PC_Q8':{}}
for c in [4096,8192,32768]:
 m=fixed+c*kv_per_token/GiB
 memory['phone_Q4'][str(c)]={'kv_MiB':c*kv_per_token/MiB,'total_GiB':m,'margin_GiB':4-m}
 memory['PC_Q8'][str(c)]={'total_GiB':m+1.8,'margin_GiB':10-m-1.8}
latency={}
for backend,prefill,decode in [('S24_Gemma3n_E2B_CPU',110.5,16.1),('S24_Gemma3n_E2B_GPU',816.4,15.6),('S24_Gemma3_1B_GPU',1876.5,44.57)]:
 latency[backend]={'prefill_1024_s':1024/prefill,'token_interval_ms':1000/decode,
 'warm_phase_sum_128_s':1024/prefill+128/decode,'warm_phase_sum_256_s':1024/prefill+256/decode,
 'extrapolated_phase_sum_512_s':1024/prefill+512/decode}
latency['M4Pro_Llama3_2_3B_Q4']={'prefill_2048_s':2048/835,'decode_128_s':128/117.3,'separate_phase_sum_128_s':2048/835+128/117.3,'extrapolated_phase_sum_512_s':2048/835+512/117.3}
speech={'TRT_base_clip_RTF':.86/20,'TRT_tiny_clip_RTF':.64/20,'PyTorch_base_clip_RTF':2.55/20,
 'TRT_base_speedup':2.55/.86,'TRT_base_memory_fraction':439/666,
 'memory_MiB_semantics':'process RSS delta sampled after call; code shifts >>20; not peak',
 'whole_device_scenario':[]}
for d in [.1,.5,1]:
 for active in [10,15,25]:
  avg=4+d*(active-4)
  speech['whole_device_scenario'].append({'compute_duty':d,'active_W':active,'idle_W':4,'average_W':avg,'daily_kWh':24*avg/1000,'annual_USD_at_0_20_kWh':365*24*avg/1000*.2})
speech['linear_clip_projection']={'hour_audio_compute_s':3600*.86/20,'ASR_duty_if_no_overlap':.86/20,'ASR_duty_if_2x_overlap':2*.86/20}
speech['ASR_paper_base_fp16_int8']={'time_ratio':80.1/78,'energy_ratio':169/155,'memory_ratio':3908/4029,'clean_WER_delta_pp':7.83-7.4,'noisy_WER_delta_pp':30.69-28.84}
network={'PCM16k_mono_16bit_hour_MB':16000*2*3600/1e6,'Opus_assumed_24kbps_hour_MB':24000/8*3600/1e6,'one_20s_PCM_MB':16000*2*20/1e6,
 '20MB_document_upload_s_at_Mbps':{str(x):20*8/x for x in [1,10,100]},'40kB_excerpt_upload_s_at_10Mbps':.04*8/10,
 '3GB_model_download_s_at_Mbps':{str(x):3000*8/x for x in [10,100]},'raw_RGB_1080p30_MB_per_s':1920*1080*3*30/1e6}
# Hypothetical task economics; these are not observed model acceptance rates.
# $0.01 cloud task is scenario, no vendor rate attributed.
cost={}
for tasks in [10000,100000,1000000]:
 cost[str(tasks)]={}
 for fallback in [.05,.2,.5]:
  local_energy=5*20/3600000*.2
  local=(120000/3+24000)/tasks+local_energy+fallback*.01
  cloud=(15000/3+6000)/tasks+.01
  cost[str(tasks)][str(fallback)]={'local_hybrid_USD_per_incoming':local,'cloud_USD_per_incoming':cloud,
    'local_hybrid_per_accepted_at_0_92':local/.92,'cloud_per_accepted_at_0_96':cloud/.96}
cost['break_even_incoming_equal_quality_f20']=53000/(.01-.2*.01-5*20/3600000*.2)
cost['correction_2pp_5min_at_30_hour_per_task']=.02*5*.5
cost['dedicated_box_scenario']={'hardware_USD':400,'life_years':3,'support_USD_year':60,'electricity_10W_24h_year_USD':10*24*365/1000*.2,'annual_total_USD':400/3+60+10*24*365/1000*.2,
 'per_audio_hour_at_8h_day':(400/3+60+10*24*365/1000*.2)/(8*365),
 'per_audio_hour_at_24h_day':(400/3+60+10*24*365/1000*.2)/(24*365)}
minions={'accuracy_retained':.709/.724,'cost_fraction':.042/.233,'cost_reduction_factor':.233/.042,'absolute_accuracy_gap_pp':100*(.724-.709)}
out={'producer':'Codex /root/ttc_research; author, not independent reviewer','kind':'deterministic arithmetic with explicitly assumed deployment reservations, workload and prices','memory':memory,'latency':latency,'speech':speech,'network':network,'economics':cost,'Minions_published_rounded_values':minions}
(B/'calculation-results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
