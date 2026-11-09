"""Assemble author artifacts; preserve the first full manuscript, no review-status promotion."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
B=Path(__file__).resolve().parent;R=B.parents[2]
registry=json.loads((B.parent/'codex-inputs'/'sources.json').read_text(encoding='utf-8'))
lookup={x['id']:x for x in registry}
scopes={
'TE01':'Version1, Table1 officialtraininghours/exclusions; architecture total/active; deployment prefill/decode sections selectively read.',
'TE05':'Dated2026-10-22 PDF extracted pages1–4, selected Claude API global/US/batch rows; primarycalculationratesHaiku/Sonnet/Opus5.5.',
'TE07':'Observed2026-11-09 pricing:standard/flex/fast tables and regional footnotes;tools/audio table; noflatteninglongcontext.',
'TE08':'Reasoning billing/context and incomplete output passages; usage total versus reasoning subset.',
'TE09':'Cache pricing, model-generation differences, explicit prefixes, lifetime/refresh/upgrades and billed-vs-physicalreuse.',
'TE11':'Full substantive model/pricing/peak-offpeak/alias table and tool pricing.',
'TE12':'Version3 mechanisms,implementation/faulttolerance,section6.1 settings and SLO metrics; not a replication.',
'TE13':'Version1 sections3–4,5.5–5.6,7.1; co-tenant denominator,output-only comparator; rawcommit retrievalfailed.',
'TE18':'Version2 abstract, sample/context and issuesresolvedperhour passages; not full106page appendices.',
'TE20':'Full main2026-02-24 methodologyupdate and conditional numerical estimates.',
'TE23':'2026-09-23 outcomepricing,resolutiondefinition,reversal and configuredhandoffterms.',
'TE24':'Version1 methods2.1–2.5 and mainresults; rental/depreciatedhardware/energy/staff boundaries.',
'TE26':'DatedV3/R1/2026V4aliases and peak-offpeak change entries; detectednews250120redirectnotoriginal.',
}
supp={
'TE-S03':'GeminiDeveloperAPI pricing original server-rendered Markdown:2.5Pro/Flash standard,cache/storage,reasoning and datedfuturealias notices.',
'TE-S05':'DatedDeepSeekV3announcement API pricechangeeffectiveFeb8; launchpromotionnotreconstructed.',
'TE-S07':'Search/Fetch billing/result/failure criteria and rates.',
'TE-S08':'CurrentDeepSeekpersistedprefix matching/besteffortcache lifecycle, nohistoric64tokenassumption.',
'TE-S09':'Currentthinkingmodebilling andretainedreasoningguide selected passages; notneededfornumericworkloads.',
'TE-S11':'2025stableGemini2.5announcement price/thinking passages.',
'TE-S12':'Claude3.5Sonnet originalannouncement dateddisplayJune21,2024;price/context passage and selectedcapability text.',
'TE-S13':'MetaLlama3.1 officialmodelcard:release/license/architecture and hardwaretraininghourstable; notprivatecost.',
'TE-S15':'NVIDIA2026-08-26 Q2FY27pressrelease actualfinancialtable/revenue/margin.',
'TE-S18':'METR2507.09089v1 abstract,sections2.1–2.3 experimentaldesign/timeoutcome and selectedresults; notfullappendices.',
'TE-S19':'Gemini explicitgenerateContentcache documentation;TTL/update/storagebilling and interactionssupportdistinction.',
'TE-S21':'FullAzureRetailPricesJSON;Consumption USD EastUS NC80adis; selectednonWindowsnonSpotnonLowPriority row13.96/1Hour,2024-03-01effective; allrowsretained.'}
rows=[]
for sid,scope in scopes.items():
 s=lookup[sid];p=Path(s['local_text'])
 rows.append(dict(id=sid,url=s['url'],path=str(p),original=s.get('local_original'),scope=scope,reader='/root/ttc_research',sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None))
for sid,scope in supp.items():
 d=B/'supplemental-sources'/sid;m=json.loads((d/'retrieval.json').read_text(encoding='utf-8'));p=d/('readable-markdown.txt' if (d/'readable-markdown.txt').exists() else 'original.txt')
 rows.append(dict(id=sid,url=m['url'],final_url=m.get('final_url'),path=str(p),scope=scope,reader='/root/ttc_research',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),retrieval_status=m['status']))
notes=(B/'web-reading-notes.md').read_text(encoding='utf-8')
rows.append(dict(id='TE-W01-W09',path=str(B/'web-reading-notes.md'),scope='Nine explicitly recorded web-opened official originals; use each entry originalURL/location; notes are not rawcaptures',reader='/root/ttc_research'))
(B/'reading-ledger.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
units=['TE-U1-cost-prices-and-measurement.md','TE-U2-three-workloads.md','TE-U3-hosting-value-and-decisions.md']
title='# Token Economics: From Model Costs and Pricing to Workload Value\n\nEvidence cutoff: November 9, 2026. English research report for enterprise buyers, AI product operators and investors. Author: Codex research producer `/root/ttc_research`. First complete author manuscript; independent whole-report review remains pending.\n\n'
appendix='''\n\n## Appendix: evidence and calculation boundaries\n\nThe report combines three evidence types. Public prices and technical/financial disclosures retain their version or observation date. Published studies retain their experimental setting. Workload acceptance rates, human time, tool allowances, demand and hosting capacity are explicit economic scenarios. Local tokenizer counts and deterministic arithmetic were actually executed; no model inference experiment was performed.\n\n`workload_calculations.py` and `calculation-results.json` contain all route counts, price inputs, cache request rows, agent step rows and sensitivity cases. `tokenizer_count.py` and `tokenizer-results.json` retain the exact paired strings, package version and encoding-file hashes. `reading-ledger.json` records the original paths and actual reading scope; `web-reading-notes.md` separates successfully read web originals from failed local downloads.\n\nHistorical OpenAI launch pages were read through the web tool after local403responses. The DeepSeek R1 news URL redirected to the current quickstart, so it does not establish a historical R1price here. Gemini's acquired documentation included authoritative Markdown inside server-delivered HTML; that text was extracted separately while preserving originals. The current GPT-6.1model page resolves the short/longpriceboundary. The datedClaude ratecard is used for commercialSKUprices, without inventing an underlyingweight revision absent from that source.\n\nThe Azure quote retains the fullpublicJSON and exactSKUrows. The report does not use post-cutoffLambda rates. It also does not use the concurrency preprint's inaccessible rawcommit or mismatchedGPUcapacity claim to assign a measuredthroughput to its independent hosting scenario. No confidentialmargin, negotiateddiscount, realizedlabor saving or language-wide tokenratio is inferred.\n\nFor a deploymentdecision, replace the scenario quality/time/traffic inputs with a representative matched task evaluation and measuredlatency/availability. Keep failure and delayedreopening in the record. These inputs determine the procurementthresholds; further precision in a postedtokenprice cannot compensate for an unknown accepted-task denominator.\n'''
draft=title+'\n\n'.join((B/u).read_text(encoding='utf-8') for u in units)+appendix
target=B/'draft-first.md'
if target.exists():raise RuntimeError('First complete draft exists; preserve it and create a separately named revision.')
target.write_text(draft,encoding='utf-8')
claims=[
('TE-C001','DeepSeekreportedofficialtraininghours2.788M timesassumed$2=$5.576M,notwholedevelopment.',['TE01']),
('TE-C002','CurrentClaude5.5globalstandardtariffs supplyscenario rates; quality assumptions notmeasurements.',['TE05']),
('TE-C003','Supporttwofinitepaths yield994/996accepted and$243.11/$184.15cohortcost.',['calculation-results.json']),
('TE-C004','Documenttimeindexed5mcache4writes8reads;1h1write11reads, costs1.416/.732perset.',['calculation-results.json','TE-W03']),
('TE-C005','Documentacceptedtaskcostincludesprep,validation,repair andunresolvedwork.',['calculation-results.json']),
('TE-C006','Agent8-stepbasecost.3632;finitepaths96accepted,$789.20cohort.',['calculation-results.json']),
('TE-C007','AzureofficialConsumptionLinuxEastUSfullnode13.96/h;2GPU188GB,80vCPU640GiB.',['TE-S21','TE-W05']),
('TE-C008','Hostingcrossover3.764Mrequestsconditionalonqualityparity and10rpsscenario capacity.',['calculation-results.json']),
('TE-C009','Tokenizeractualsixstringsdemonstrateencoding/contentdifferences,notlanguagewidecostratios.',['tokenizer-results.json']),
('TE-C010','METR2025slowdowniscontextspecific;2026selectionproblemsblockuniversalnewmultiplier.',['TE-S18','TE20']),
('TE-C011','Financialsuppliercompany/segmentresults do notestablishindividualmodelmargins.',['TE-S15','TE-W06','TE-W07']),
('TE-C012','Gemini200Kthresholdrepriceswholeinput/output understatedtier,one-tokenboundarycalculation.',['TE-S03','calculation-results.json']),
]
claimrows=[dict(claim_id=i,claim=t,evidence=s,author='/root/ttc_research',status='author-supported; independent review pending') for i,t,s in claims]
(B/'claims.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in claimrows)+'\n',encoding='utf-8')
handoff={'producer':'/root/ttc_research','case_id':'token_economics_en','stage':'complete first author manuscript; not independent review or acceptance','created_at':datetime.now(timezone.utc).isoformat(),'word_count':len(re.findall(r"\b[\w’-]+\b",draft)),'reading_records':len(rows),'claims':len(claimrows),'draft':str(target),'outputs':[]}
for filename in units+['draft-first.md','workload_calculations.py','calculation-results.json','tokenizer_count.py','tokenizer-results.json','reading-ledger.json','claims.jsonl','web-reading-notes.md']:
 p=B/filename;handoff['outputs'].append(dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(B/'handoff.json').write_text(json.dumps(handoff,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'full-response.json').write_text(json.dumps(dict(analysis=draft,claims=claimrows,reading_notes=rows,handoff=handoff),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:handoff[k] for k in ['case_id','word_count','reading_records','claims','draft']}))
