"""First author's check and bounded clarity corrections; preserves first draft and raw units."""
import csv, hashlib, json, re
from pathlib import Path
from datetime import datetime, timezone
here=Path(__file__).resolve().parent
now=datetime.now(timezone.utc).isoformat()
first=here/'draft-first.md'
first_hash=hashlib.sha256(first.read_bytes()).hexdigest()
checks={
 'review_type':'author_self_check_not_independent_review',
 'reviewed_artifact':'draft-first.md',
 'reviewed_sha256':first_hash,
 'reviewed_at':now,
 'scope':'Full assembled manuscript, cited numerical/accounting boundaries, calculations and directly rendered CP17 chart footnotes. This is the author’s first complete-draft check, not root acceptance.',
 'findings':[
  {'id':'A01','severity':'minor','location':'2, supply expansion','issue':'The translation more than fivefold is less explicit than the source 增长超5倍.','action':'Use reported an increase of more than 500% without asserting an exact final supply multiple.'},
  {'id':'A02','severity':'minor','location':'2, audience methods;3 table','issue':'Two instances of micro-program use terminology inconsistent with the defined mini-program.','action':'Normalize to mini-program.'},
  {'id':'A03','severity':'minor','location':'6, minors','issue':'Those aged eight and above could be read as including adults.','action':'Specify minors aged eight and above.'},
  {'id':'A04','severity':'minor','location':'5, hybrid','issue':'The incremental amount is publisher receipts before extra costs and sharing, not platform profit.','action':'Make the publisher-level base explicit.'},
  {'id':'A05','severity':'minor','location':'6, copyright','issue':'One shortcut citation shows only CP03.','action':'Use a descriptive November campaign label.'}
 ],
 'confirmed_boundaries':[
  'Frozen 39-record source set only; no Chinese report, Chinese calculations, claims or reviews used; current Codex authored, not an API/Astra response.',
  'CNNIC 2024/2025 national survey, CSM adult survey, QuestMobile app/mini-program activity and related-content reach retain distinct denominators.',
  'CP17 PDF p6 channel thresholds visually confirmed. On p9 26.2 monthly hours belongs to January 2026 and 22.1 to February; manuscript calculations use CP24 January2025–May2026 values instead.',
  'CP16/24 seven original chart images were actually viewed; raw originals and image hashes are recorded.',
  'Historical forecast63.43bn, retrospective~100bn, outputvalue100bn and2026forecast200bn are never averaged or treated as equivalent audited revenue.',
  'COL reclassified segment comparison, CMS consolidation change, domestic/overseas allocation and YTD/quarter cashflow boundaries are explicit.',
  'Paid/free/hybrid assumptions are disclosed and executed; cash allocations reconcile; examples do not estimate industry margins or rank actual platforms.',
  'No actual industry-wide retention, paying conversion, eCPM, completion, hit rate or profit is invented.',
  'November campaign and earlier2026 takedowns are distinguished; category thresholds use the actual local official explanation; CP23 is access failure only.',
  'Decisions, counterevidence and reversal conditions are supplied for platforms, producers/distributors and investors.'
 ],
 'outcome':'Five bounded clarity edits identified. Independent content review, audit and final acceptance pending.'
}
(here/'author-self-check-first.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
text=first.read_text(encoding='utf-8')
replacements=[
 ('Kuaishou says its supply of live-action and AI dramas by June 2026 had grown more than fivefold relative to January;', 'Kuaishou reports an increase of more than 500% in its supply of live-action and AI dramas between January and June 2026;'),
 ('micro-programs','mini-programs'),
 ('micro-program services','mini-program services'),
 ('while those aged eight and above generally have limited capacity','while minors aged eight and above generally have limited capacity'),
 ('leaving an incremental RMB220,402 before extra service, sales, and content-sharing costs','leaving incremental publisher receipts of RMB220,402 before extra service, sales, and content-sharing costs'),
 ('[NRTA measures and November campaign][MD004]; [CP03]','[NRTA measures][MD004]; [November campaign][CP03]')
]
for a,b in replacements:
 if a not in text: raise ValueError('Expected manuscript wording absent: '+a)
 text=text.replace(a,b)
(here/'draft-current.md').write_text(text,encoding='utf-8')
record={'date':now,'type':'author_revision','first_draft_sha256':first_hash,'current_draft_sha256':hashlib.sha256((here/'draft-current.md').read_bytes()).hexdigest(),'normalized_lf_content_sha256':hashlib.sha256(text.encode()).hexdigest(),'changes':checks['findings'],'independent_review_status':'pending_root'}
(here/'author-revision-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(here/'logs').mkdir(exist_ok=True)
(here/'logs/review.jsonl').write_text(json.dumps({'review_type':'author_self_check','artifact':'draft-first.md','record':'author-self-check-first.json','independent':False,'result':'clarity_edits_identified'})+'\n'+json.dumps({'review_type':'author_revision','artifact':'draft-current.md','record':'author-revision-record.json','independent':False,'result':'submitted_for_independent_review'})+'\n',encoding='utf-8')

# Expand compact drafting labels in the audit registry into readable English.
claims=[json.loads(x) for x in (here/'claims.jsonl').read_text(encoding='utf-8').splitlines()]
readable={
 'EN017':('Kuaishou reports an increase of more than 500% in drama supply from January to June 2026 and more than 100% year-on-year growth in Q2 microdrama online marketing expenditure.','Retained official release output; supplier advertising expenditure is not consumer receipts or supplier profit.'),
 'EN026':('May 2026 Douyin mini-program MAU fell 83.3% year on year while standalone apps and WeChat mini-programs grew.','Channel observations do not identify causal substitution to specific services.'),
 'EN027':('September Xifan MAU was 8.34 million; 6.32 million also used the main Kuaishou app.','Affiliation and overlap do not identify traffic transfer prices or guarantee equivalent app adoption.'),
 'EN028':('Tencent’s March 2026 policy provides an extra 15% on the pure-sharing settlement portion above RMB1 million and conditional longer sharing periods and series incentives.','Policy concerns exclusive horizontal long, mid and short formats; contractual box office is not raw consumer top-ups.'),
 'EN029':('QuestMobile’s policy compilation describes iQIYI platform-revenue-based sharing and Youku new-member and effective-play incentives.','Secondary compilation, not universal executed agreements or directly comparable sharing percentages.'),
 'EN030':('CSM paid-option preferences include membership and ad removal alongside interest in ad-supported or sharing-based free access.','Preferences do not identify price elasticity or realized hybrid profits.'),
 'EN031':('Douyin creator-promotion commissions of 1–29% and automatic initiation periods of up to 0–3 days differ from transaction settlement at T+7.','Different recipients and processes; neither number is a universal platform take rate.'),
 'EN032':('COL group revenue in 2023/2024/2025 was RMB1,408.9/1,159.1/1,656.6 million; parent profit 89.4/−242.9/−671.0 million; operating cash flow −10.1/−52.5/−203.7 million.','Consolidated businesses and geographies, not a domestic microdrama margin.'),
 'EN033':('iReader group revenue in 2023/2024/2025 was RMB2,778.4/2,583.3/3,242.7 million; parent profit 34.8/49.3/−176.5 million; operating cash flow 338.4/−75.0/−232.5 million.','Consolidated businesses and geographies, not a domestic microdrama margin.'),
 'EN034':('COL January–September 2026 revenue was RMB832.7m, parent loss132.1m, operating cash42.8m; iReader revenue2,775.3m, parent loss68.4m, operating cash52.7m.','Unaudited nine-month results; not comparable in duration to full annual results.'),
 'EN035':('COL 2025 short-drama/IP derivatives revenue was RMB896.0m, up125.02%, with38.41% gross margin, down8.95 percentage points; reclassified2024 base398.2m differs from original category454.9m.','Reclassification prevents splicing the old and new segments into one growth series.'),
 'EN036':('COL 2025 group gross profit599.3m less selling expense953.2m leaves a353.9m deficit before other items; foreign revenue40.98%, and selling expense increase mainly overseas.','Does not allocate the group deficit to domestic dramas.'),
 'EN037':('CMS ceased consolidation from May2023: ownership49.16%, voting rights47.81%, three of seven board nominations; reported non-recurring profit effect55.9237m.','Ownership, control, equity returns and consolidated receipts differ.'),
 'EN038':('iReader 2025 derivatives revenue1,854.9m and gross margin68%; group selling expense2,078.6m, promotion1,985.6m, gross profit less selling expense162.2m.','Derivatives and group costs include multiple activities and geographies; promotion is not fully allocated to domestic drama.'),
 'EN039':('COL H1 2026 short-drama/IP derivatives revenue411.3m, up108.72%, margin48.62%; operating cash126.8m versus nine-month42.8m implies Q3 outflow84.0m.','Group cash improvement mainly overseas; quarter difference is derived, not a domestic title cash return.'),
 'EN040':('iReader H1 2026 derivatives revenue1,185.1m, up41.45%; operating cash−116.5m versus nine-month52.7m implies Q3 inflow169.3m; revenue growth12.73% for nine months and5.96% for Q3.','Quarter cash flow is derived from cumulative group figures; not isolated domestic-drama economics.'),
 'EN041':('COL reports Yipin Buyi first-season plays above3bn and sequels; October reporting cites one March title with sharing above10m and200+ titles with monthly sharing above1m.','Selected corporate/news hits; plays are not unique users, settlement is not profit, and the complete slate denominator is unknown.'),
 'EN042':('Paid scenario:1m starts,4% conversion,RMB75 purchases,5% refunds,10% channel then10% rights,CAC1.20,budget600k yield508.5k project surplus.','All commercial inputs assumed; waterfall bases and excluded costs explicit.'),
 'EN043':('At2.5% paid conversion the producer loses357,187.50 after media-first recovery; break-even conversion is3.12%.','Loss allocation follows the assumed priority; more severe failure can also impair media recovery.'),
 'EN044':('A1m production budget cuts paid-case surplus to108.5k; a12% refund rate cuts it to338.4k with other base inputs fixed.','One-variable sensitivities, not observed industry ranges.'),
 'EN045':('Free scenario:1m viewers ×14 active days ×(4+8×60%) ad opportunities ×80% fill ×RMB20/1,000 generates1,971,200 advertiser expenditure.','Assumed later-block reach is distinct from actual observed retention, full-series completion and ad completion.'),
 'EN046':('Free case:20% network deduction,35% content share,CAC0.70,100k operating cost and600k production cost yield platform225,024,producer−48,064,joint176,960.','Explicit assumptions; a platform can earn a positive contribution while its content supplier loses money.'),
 'EN047':('Free-case platform break-even10.93 days and producer15.22 days; content share45% gives producer109,632/platform67,328 without changing joint surplus.','Comparative statics; changing sharing alone creates no additional revenue.'),
 'EN048':('Removing60k of assumed rewards is offset by losing0.82 active days, or5.85% of the14-day base.','Sensitivity threshold, not a prediction of Hongguo’s reward withdrawal.'),
 'EN049':('Hybrid example:50k RMB7 passes net299,250 after refunds/fees; subtracting78,848 displaced average advertising yields incremental publisher receipts220,402; double-ad-value buyers yield141,554.','Before extra service and content-sharing costs; not platform net profit or an optimal price estimate.'),
 'EN050':('Production, acquisition payment, revenue recognition and collection may occur at different times; T+7 is one transaction step.','Cash-cycle inference; no industry-wide recovery duration is asserted.'),
 'EN051':('Earlier NRTA June2024 implementation differs from February2025 webpage date; live-action thresholds adjusted January2026, AI thresholds July2026, and comprehensive measures effective September2026.','Effective dates, signature dates and webpage dates are kept separate.'),
 'EN052':('CategoryI covers special subjects or live-action investment>=3m/AI>=800k; II ordinary live1m–<3m/AI300k–<800k; III lower budgets subject to platform review.','Thresholds come from the local official implementation explanation, not a claimed copy of the original national threshold circular.'),
 'EN053':('CategoryI decision period20 days from acceptance including10 days expert review; changes require resubmission; non-exclusiveIII uses each outlet’s number and rebroadcast review; AI episodes require labels.','The period is not an end-to-end script-to-release guarantee.'),
 'EN054':('The2026 quality plan targets1,000 works by year-end with funding, creative and distribution support plus application/delivery requirements.','Target and policy resources, not an achieved count or confirmed disbursement.'),
 'EN055':('November6 announcement covers a November1–December-end campaign;75,000 removals and1,500+ accounts addressed refer to earlier2026 actions.','Does not present earlier figures as results of the new campaign; profit impacts are not quantified.'),
 'EN056':('Consumer regulation requires clear pricing, renewal notice, limits on unfair terms, and prepaid-service contract/refund obligations.','Retained official text supplies no universal five-day renewal notice period.'),
 'EN057':('Douyin rules require full prices, stable tokens, affirmative consent, quarter-length maximum membership,10h×7days support,15-minute responses and48-hour complaint handling.','Specific to the frozen platform rule, not universal contracts for the whole industry.'),
 'EN058':('Douyin mandates full refunds for minors’ virtual-goods purchases regardless of fulfillment; Civil Code capacity depends on age, transaction and guardian consent or ratification.','Platform commercial rules do not establish that all minors’ transactions are automatically void nationally.'),
 'EN059':('Court case introduction describes a renamed unauthorized drama, paid traffic routing and RMB46,000 covering damages and reasonable enforcement expenses.','Case introduction, not the full judgment; amount includes damages and expenses and is not a general tariff.'),
 'EN060':('Repeat access, rights and cash recovery are central competitive assets, but no universal platform or monetization-model winner is established.','Author synthesis; unmatched platform cohorts do not identify causal advantages.'),
 'EN061':('Platforms should compare reward savings with lost cohort advertising value and maintain viable content supply.','Conditional recommendation; retention, yield and supplier response must be observed.'),
 'EN062':('Producer choices between guarantees and contingent sharing depend on financing, rights, windows and recovery priority.','Recommendation requires actual contracts, full portfolio costs and failure rates.'),
 'EN063':('Investors should reconcile controlled entities, geography, acquisition costs and cash recovery before valuing market growth.','Recommendation would change with representative positive recovery after promotion, failures, obligations and refunds.'),
 'EN064':('CP23 contains only an access failure; CP10/CP20 are retained web outputs; MDX002 duplicates CP27 and CP15/CP17 are the same underlying research.','Input/access characterization; CP23 supports no substantive external-announcement claim.')
}
for c in claims:
 if c['claim_id'] in readable: c['claim'],c['uncertainty']=readable[c['claim_id']]
(here/'claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims),encoding='utf-8')
with (here/'data/claims_registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['claim_id','claim','source_ids','report_section','uncertainty','calculation']);w.writeheader()
 for c in claims: w.writerow({**c,'source_ids':';'.join(c['source_ids']),'calculation':c.get('calculation','')})
src_path=here/'data/source_registry.csv'
with src_path.open(encoding='utf-8-sig',newline='') as f: reader=csv.DictReader(f);fields=reader.fieldnames;srcrows=list(reader)
for row in srcrows:
 if row['source_id']=='MD010':
  row['title']='《2025年北京微短剧研究报告》发布！北京微短剧市场规模居全国首位、领先优势明显'
  row['read_boundary']+=' Actual page title corrected from inherited generic work-report label; frozen manifest preserved unchanged.'
with src_path.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(srcrows)
print(json.dumps({'first_preserved_sha256':first_hash,'current_sha256':record['current_draft_sha256'],'author_findings':len(checks['findings']),'independent_acceptance':'pending'}))
