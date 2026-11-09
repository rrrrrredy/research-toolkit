"""Preserve author records and prepare a review handoff; never marks independent acceptance."""
import csv, hashlib, json, re
from pathlib import Path
from datetime import datetime, timezone

here = Path(__file__).resolve().parent
pack = here.parents[2] / 'frozen-alternate-inputs' / 'microdrama_market_en'
sources = json.loads((pack / 'sources.json').read_text(encoding='utf-8-sig'))
byid = {s['source_id']: s for s in sources}
now = datetime.now(timezone.utc).isoformat()
def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

# Record actual access, including incomplete tool displays rather than treating a saved
# extraction or a metadata assertion as proof that the author read its entire contents.
ledger = json.loads((here / 'reading-ledger.json').read_text(encoding='utf-8'))
for n, rec in enumerate(ledger, 1):
    rec['read_event_id'] = f'READ-{n:03}'
    rec.setdefault('read_status', 'read_recorded_scope')
    if n in (2,3,4,44,49):
        rec['attempted_line_ranges'] = rec['actual_line_ranges']
        rec['read_status'] = 'tool_display_truncated; relied_on_followup_for_claims'
        rec['truncation_note'] = 'Saved extracted output may contain more text than was visible in the tool response. Only ranges below count as confirmed reading in this event.'
        rec['actual_line_ranges'] = {2:[[1,344]],3:[],4:[],44:[[69,97],[108,114],[124,129]],49:[[69,86],[100,129]]}[n]
    if rec['source_id']=='CP23':
        rec['read_status']='access_failure_record_only_no_substantive_evidence'
        rec['access_note']='Three-line TimeoutError record; no original announcement body obtained in this independent input. Inherited locator text claiming earlier search access is not treated as available evidence.'

chart_notes = {
 '2d52bc46d8803cd23525c580c9b09010.png': 'Full chart: microdrama-video app MAU 487m September 2026; threshold-crossing dates and units read. CAGR from small base is not used as industry revenue growth.',
 '5abf475a35249f4ce88a9e5176c8217d.png': 'Full chart and footnote: year-on-year change in total monthly time, not absolute time share; microdrama 133.29 hundred-million hours, short video 57.17; contribution to net growth may exceed 100%. Not used as revenue share.',
 'ab089f4e9c4ca8a2c97e05e7be0112db.png': 'Full September 2026 app and WeChat-mini-program ranking: unit 10,000 MAU; Hongguo 42,969, animation 7,883, Hema 3,080, Xifan 834, Lüpao Pao 15,635; year-on-year labels and dash footnote read.',
 'e15d12b81e8ada19f3a096549d587df3.png': 'Full September overlap chart: main Douyin/Hongguo 380m and 88.5% of Hongguo; Kuaishou/Xifan 6.32m and 75.8%; overlap is not attributed acquisition.',
 'users.jpg': 'Full May 2026 channel chart: 851m union of apps, WeChat mini-programs, Douyin mini-programs only; individual counts 402/508/14m; 472m short-video related-content reach separate. Unit, grouping brackets, dates and footnote read.',
 'time.jpg': 'Full January 2025–May 2026 app-use chart: 13.0 to 26.9 monthly hours and 62.0 to 125.6 usage occasions; time window and app scope read.',
 'apps.jpg': 'Full May 2026 ranking: Hongguo 356.781m, Hema 38.535m, Xifan 11.018m; units and growth labels read.'
}
for sid in ['CP16','CP24']:
    for att in byid[sid].get('additional_originals', []):
        p=pack/att['path']
        if p.name not in chart_notes: continue
        ledger.append({'read_event_id':f'READ-{len(ledger)+1:03}','source_id':sid,'url':byid[sid]['url'],'path':str(p),'sha256':sha(p),'reading_mode':'direct_image_visual','actual_read_position':'Full image including chart labels, units, dates and footnotes','reading_note':chart_notes[p.name],'read_status':'visually_read','access_note':'Same frozen original attachment restored after initial input-copy omission; no live factual expansion.'})
pdf=pack/'original-attachments/CP17/original.pdf'
ledger.append({'read_event_id':f'READ-{len(ledger)+1:03}','source_id':'CP17','url':byid['CP17']['url'],'path':str(pdf),'sha256':sha(pdf),'reading_mode':'rendered_pdf_visual','actual_read_position':'PDF pages 6, 9, 11, 18; complete rendered pages including footnotes','reading_note':'p6 current-app selection >100,000 MAU and separate-year WeChat selection >1m; p9 January 2026 26.2h vs February 22.1h; p11 February ranking/daily-use distinction; p18 secondary compilation of platform-sharing policies. All four rendered images opened and inspected.','rendered_paths':[str(here/f'pdf-checks/CP17-page-{p}.png') for p in [6,9,11,18]],'read_status':'visually_read'})
dump(here/'reading-ledger.json',ledger)

claims=[]
def add(cid, claim, sids, section, uncertainty='Directly reported within the stated source, period and population.', **extra):
    claims.append(dict(claim_id=cid, claim=claim, source_ids=sids.split() if sids else [], report_section=section, uncertainty=uncertainty, **extra))
add('EN001','NRTA rules effective 1 September 2026 define microdramas as episodes shorter than 20 minutes with continuous story and characters; AI and multiple distribution devices are covered.','MD004','1','Statutory definition at cutoff; not a backcast classification of every historical publisher series.')
add('EN002','The report treats viewer expenditure and external advertising as final-demand measures and production, licensing, distribution and acquisition transfers as distinct chain flows.','CP27 CP14 MD012','1','Author accounting framework; proprietary published aggregate methodologies cannot be reconstructed.')
add('EN003','Top-ups, consumed virtual currency, recognized revenue and cash collection are different measures.','CP14 MD012','1,4','Company accounting/audit examples; principal-agent revenue policy depends on actual contract.')
add('EN004','PKU reports domestic market estimates RMB37.39bn 2023, 50.4bn 2024, about 100bn 2025; possible 200bn 2026 is a forecast.','MD006','1','Construction uses leading-company flows/third-party information without full elimination bridge; not an audited expenditure total.')
add('EN005','COL 2024 annual report cites 50.5bn 2024 estimate and 63.43bn 2025 forecast; Beijing June 2026 release calls national 2025 total 100bn output value and Beijing 58.57bn.','MD012 MD010','1','Different vintages and output-value perimeter; do not average or treat Beijing output as resident consumption.')
add('EN006','Association white paper forecasts free viewing at 66.3% of full-year 2025 market.','MD009','1','Forecast, with insufficient monetary definition to equate directly to final advertiser spending.')
add('EN007','CNNIC estimates 662m/59.7% at December 2024 and 664m/59.0% at December 2025; implied count growth about 0.3%.','CP19 CP08','2','Survey estimates for mainland 6+ internet users; general proportion sampling errors are not a significance test for this category difference.',calculation='observed_arithmetic.cnn_users_pct')
add('EN008','CSM January 2026 adult survey reports 70.2% watching by end-2025, 84.2% future willingness to pay, and 71.8% having watched paid dramas in prior year.','MD003','2','Adult/sample boundary differs; willingness and watching paid content are not verified current paying conversion.')
add('EN009','QuestMobile February 2026 app MAU335m, WeChat mini-program427m and deduplicated union718m use different channel selection rules.','CP17','2','Apps selected at current MAU>100k and looked back; mini-programs independently selected each year MAU>1m; chart p6 visually confirmed.')
add('EN010','The February channel counts imply about 44m overlap; May three-channel sum exceeds 851m union by 73m memberships.','CP17 CP24','2','Rounded source values; three-group excess is not a distinct count of overlapping people.',calculation='observed_arithmetic.feb_cross_channel_overlap_millions;may_sum_minus_union_millions')
add('EN011','May2026 apps402m, WeChat mini-program508m, Douyin mini-program14m comprise the851m application union;472m related-content reach is separately defined.','CP24','2','Original grouping chart visually read; adding reach to union would double-count unknown overlap.')
add('EN012','September microdrama app MAU487m and Hongguo429.69m imply88.2% category penetration;380m co-use main Douyin,88.5% of Hongguo.','CP16','2,3','Penetration/overlap, not exclusive share, revenue share or causally attributed acquisition.',calculation='observed_arithmetic.sept_hongguo_app_penetration_pct')
add('EN013','January2025–May2026 monthly app hours13.0→26.9 and use occasions62.0→125.6 imply+106.9% hours,+102.6% occasions,and+2.1% minutes per occasion.','CP24','2','Aggregate ratios; not same-person cohort retention or episode completion.',calculation='observed_arithmetic.monthly_hours_pct;monthly_uses_pct;minutes_per_use_pct')
add('EN014','Douyin documents organic, paid, and return traffic routes including feed, sidebar, search and subscriptions plus attributed ad yield information.','CP27','2,3','Documented capabilities, not measured favorable acquisition economics.')
add('EN015','Growth can be decomposed into active viewers, paying conversion/spend or repeat viewing, eligible ad inventory, fill and price.','CP27 MD003 CP24','2','Author causal framework; missing common conversion, fill, price and cohort series prevents numerical industry growth attribution.')
add('EN016','Association reports>140k vertical launches Jan–Aug2025 including repeats/re-edits, forecasts about40k independently completed annual productions, ordinary budgets400k–700k.','MD009','2','Research/interview findings; launches are not unique completed titles and annual production is forecast.')
add('EN017','Kuaishou reports supply increase>500% June2026 vsJanuary and microdrama online marketing expenditure growth>100% inQ2 year on year.','CP20','2,3','Retained official release output; marketing expenditure is not producer profit or consumer receipts.')
add('EN018','September HongguoMAU+81.8%,Hema−40.3%,Xingya−76.8%;Xifan8.34m+123.9% but belowMay11.018m.','CP16 CP24','2','App-level adjustments and unlike comparison periods; no confirmed company exit inferred.')
add('EN019','CSM reports>35% criticism of repetitive/unrealistic/unoriginal plots and11.8% preference for a fixed studio/account.','MD003','2','Survey attitudes; proposed series/brand economics remain inference.')
add('EN020','WeChat mini-program users aged51+ comprise31.2% versus13.9% of app users inQMFebruary sample.','CP17','3','Audience differences preclude attributing all observed outcomes to platforms.')
add('EN021','PKU describes commissioned work, rights partnerships, finished-title submissions and reported seven-day exclusive opening windows.','MD006','3,4','Observed cooperation forms; seven days is not every platform contract.')
add('EN022','Hongguo announced planned content-budget growth>40% and greater sharing transparency;Douyin announcedRMB500m live-action support inApril.','CP26 MD013','3','Plans/commitments, not proof all money was disbursed or all settlements transparent.')
add('EN023','October reporting describes planned coin removal for newusers1Nov andallusersbyDecend, existing balance arrangements, and denial ofRMB40bn annualized revenue rumor.','MD014','3','News report of notice/denial; transition and actual retention/revenue effects unobserved at cutoff.')
add('EN024','WeChat Lüpao Pao free service uses ads,social/regional recommendations and small-window viewing;Tencent agreement counterparty and third-party content suppliers.','CP25','3','Journalist interface/agreement observations; not quantified retention superiority.')
add('EN025','Same titles appear onHongguo andLüpao Pao;SeptemberLüpao PaoMAU156.35m precedesOctoberrecent-launch reporting.','CP25 CP16','3','Catalog overlap established, share of nonexclusive rights and exact launch/renaming chronology unresolved.')
add('EN026','MayDouyin mini-program MAU declined83.3%YoY while standalone apps andWeChat grew.','CP24','3','Channel observations do not causally identify substitution to particular services.')
add('EN027','SeptemberXifan8.34m MAU;mainKuaishou overlap6.32m.','CP16','3','Corporate affiliation/overlap does not identify traffic transfer price or guarantee equivalent adoption.')
add('EN028','Tencent March2026 policy describes extra15% onpure-share boxoffice portion aboveRMB1m andconditional extended recovery/series incentives.','CP26','3','Exclusive horizontal long/mid/short common policy; contractual boxoffice is not cinema sales or raw top-ups.')
add('EN029','QM policy compilation describesiQIYI attributed platform-revenue shares andYouku member-value/effective-play incentives.','CP17','3','Secondary compilation of public policies, not executed universal contracts or directly comparable percentages.')
add('EN030','CSM paid-option preferences include membership andadremoval alongsidead-supported/sharedfreeaccess.','MD003','3','Stated preferences do not identify price elasticity or realized hybrid profitability.')
add('EN031','Douyin creator promotion commission choices1–29% andautomatic initiation maximum0–3days differ fromtransaction settlementT+7.','CP27 CP18','4','Different recipients/processes; neither range is a universal platform take rate.')
add('EN032','COLgrouprevenue2023/24/25=1408.9/1159.1/1656.6m,parentprofit89.4/−242.9/−671.0m,CFO−10.1/−52.5/−203.7m.','CP12','4','Consolidated multiple businesses/geographies, not domesticmicrodrama margin.')
add('EN033','iReadergrouprevenue2023/24/25=2778.4/2583.3/3242.7m,parentprofit34.8/49.3/−176.5m,CFO338.4/−75.0/−232.5m.','CP14','4','Consolidated multiple businesses/geographies, not domesticmicrodrama margin.')
add('EN034','COL9m2026revenue832.7m,parentloss132.1m,CFO42.8m;iReader2775.3m,loss68.4m,CFO52.7m.','CP01 CP02','4','Unauditednine-month periods;not directly full-year comparisons.')
add('EN035','COL2025shortdrama/IPderivativesrevenue896.0m+125.02%,grossmargin38.41%,down8.95pp;restated2024base398.2m differsoriginalcategory454.9m.','CP12 MD012','4','Reclassification prevents splicing original segment labels into growth calculation.')
add('EN036','COL2025groupgross599.3m lesssalesexpense953.2m leaves−353.9m beforeotheritems;foreignrevenue40.98%,increasedsellingexpenseprimarilyoverseas.','CP12','4','Does not allocate group deficit to domestic dramas.',calculation='observed_arithmetic.col_2025_gross_profit;col_2025_gross_less_sales')
add('EN037','CMSdeconsolidatedfromMay2023withownership49.16%,votes47.81%,board3/7;reportednonrecurringprofit effect55.9237m.','CP13','4','Control,ownership,equityreturns andplatformreceipts have different accounting boundaries.')
add('EN038','iReader2025derivatives1854.9m,grossmargin68%;groupsales2078.6m,promotion1985.6m;grosslesssales162.2m.','CP14','4','Derivatives includeother/geographic activity;promotion not fully allocated toshortdrama segment.',calculation='observed_arithmetic.ireader_2025_gross_less_sales')
add('EN039','COLH12026shortdrama/IPderivative revenue411.3m+108.72%,margin48.62%;groupCFO126.8m vs9m42.8m impliesQ3−84.0m.','MD005 CP01','4','Groupcash improvement mainly overseas;Q3difference is derived,not domestic title recovery.',calculation='observed_arithmetic.col_q3_cashflow_derived')
add('EN040','iReaderH12026derivatives1185.1m+41.45%;CFO−116.5m vs9m52.7m impliesQ3169.3m;9mrevenue+12.73%,Q3+5.96%.','MD008 CP02','4','Derivedquartercashflow andgroupgrowth;notisolateddomesticdrama economics.',calculation='observed_arithmetic.ireader_q3_cashflow_derived')
add('EN041','COLreportsYipinBuyifirstseason>3bnplaysandsequels;OctoberreportcitesoneMarchtitle>10msharingand200+titlesmonthly>1m.','CP07 MD014','4','Company/news-selectedhits;playsnotuniqueusers,andsettlementsnotprofits;nofullslatedenominator.')
add('EN042','Paidscenario:1mstarts,4%conversion,RMB75spend,5%refund,10%channelthen10%rights,CAC1.20,budget600k yield508.5kprojectsurplus.','','5','All commercial parameters assumed; full cash waterfall and exclusions explicit.',calculation='paid_base')
add('EN043','Paidscenario:at2.5%conversionproducerloses357187.50aftermediafirstrecovery;break-evenconversion3.12%.','','5','Lossallocation followsassumedpriority;moreseverelossmayimpairmediarecovery.',calculation='paid_sensitivity;paid_break_even_conversion')
add('EN044','Paidscenario:budget1m reducestotal surplus108.5k;12%refundrate reducesit338.4k,otherbaseinputsheldfixed.','','5','Independent one-variable sensitivities, notobserved industryranges.',calculation='paid_budget_sensitivity;paid_refund_sensitivity')
add('EN045','Freescenario:1mviewers×14days×(4+8×60%)adopportunities×80%fill×RMB20/1000=1971200advertiseroutlay.','','5','Assumptions, completion meansdefinedlater-blockreach; notactualretention oradcompletion.',calculation='free_base')
add('EN046','Freescenario:20%networkdeduction,35%publishercontentshare,CAC.70,ops100k,production600k yieldplatform225024,producer−48064,joint176960.','','5','Assumed allocation andcosts;platformprofitcan coexistwithproducerloss.',calculation='free_base')
add('EN047','Atfreebaseyieldplatformbreakseven10.93days,producer15.22days;45%share movesprofitproducer109632/platform67328withoutchangingjointsurplus.','','5','Deterministic comparative statics;contract sharing doesnot itselfcreateadditionalrevenue.',calculation='free_break_even_active_days_platform;free_break_even_active_days_producer;free_share_sensitivity')
add('EN048','Removing60krewardcost isoffsetbylosing0.82daysor5.85%ofbaseactive days.','','5','Hypothetical sensitivity, notforecast ofHongguo coin-removalresults.',calculation='gold_scenario')
add('EN049','Hybridscenario:50kRMB7passesafterrefund/fees299250;subtractaverageadvalue78848 yieldsincrement220402;doubleadvaluebuyers yield141554.','','5','Beforeextra service/contentsharingcosts;notoptimalpriceoractualconversionestimate.',calculation='hybrid_scenario')
add('EN050','Production,campaignpayment,receivable recognition and cashcollectioncan occuratdifferenttimes;T+7 isonepaymentstep.','CP18 MD005','4,5','Author cash-cycle implications;noindustryworking-capitalduration inferred.')
add('EN051','EarlierNRTA noticeJune2024node differswebpublicationFeb2025;livethresholdsadjustedJan2026;AIthresholdsJuly2026;newmeasuresSeptember2026.','CP05 CP09 CP21 MD004','6','Document effective dates separatedfrompagepublicationandURL dates.')
add('EN052','CategoryI:specialsubjectsorlive>=3m/AI>=800k;IIordinarylive1m–<3m/AI300k–<800k;IIIbelowwithplatformreview.','CP04 MD004','6','Thresholdsfromlocalofficialimplementationexplanation,notclaimedoriginalnationalthresholdcircular.')
add('EN053','CategoryIreview20daysfromacceptance including10expertreview;modificationresubmission;nonexclusiveIIIownplatformnumbersandrebroadcastreview;AIepisodelabels.','MD004','6','Notguaranteedend-to-endproductionapprovalperiod.')
add('EN054','2026qualityplan1000worksisyearendtargetwithfunding,creativeanddistribution support andeligibility/deliveryconditions.','MD011','6','Targetandpolicyresources,notachievedcountordisbursedfunds.')
add('EN055','6Novannouncementcovers1Nov–Decendcampaign;75kworksand1500+accountsactionedearlierin2026,notnewcampaigncompletedoutcomes.','CP03','6','Campaignfocus includesAIrights,renamedrepeatsandhomogeneousrecommendations;effectonactualprofitunmeasured.')
add('EN056','Consumerregulationrequirespricing/renewalnotice,limitsunfairstandardterms,andprepaidservicecontracts/refundobligations.','CP10','6','Retainedofficialtext;doesnotsupplyuniversal5dayrenewalnotice.')
add('EN057','Douyinrequiresfullprice/stabletokens/consent,quartermaxmembership,10h×7dayssupport,15minresponses,48hcomplaints.','CP18','6','Platform-specificoperatingrulesatfrozenversion,notindustry-widecontracts.')
add('EN058','Douyinminorvirtualgoodsrefundsfullregardlessfulfillment;CivilCodecapacityvariesbyage/transaction/guardianratification.','CP18 CP22','6','Do notconflateplatformcommercialruleswithnationalrulevoidingallminortransactions.')
add('EN059','Courtcaseintroductiondescribesrenamedunauthorizeddrama,paidtrafficroutingand46kdamages/enforcementexpenses.','CP11','6','Caseintroductionnotfulljudgment;46knotuniversalpiracytariff.')
add('EN060','Repeataccess,rightsandcashrecoveryarekeycompetitiveassets;platform/modeluniversalsuccessnotestablished.','CP16 CP24 CP12 CP14','7','Author synthesis;notcausalidentificationfromunmatchedplatformcohorts.')
add('EN061','Platforminvestmentshouldcomparelostcohortadvaluewithrewardcostsavingsandretainviablecontentsupply.','MD014 CP16','7','Recommendation conditional onmeasuredretention/yield/supplierresponse;scenario thresholdsarenotpredictions.')
add('EN062','Producerchoicebetweenguaranteesandcontingentsharingdependsfinancing,rights,windowandrecoverypriority.','MD006 CP26 CP18','7','Author recommendation;fullcontractdetailsandportfoliofailuresrequired.')
add('EN063','Investorsshouldreconcilecontrolledentities,domestic/foreignsegments,acquisitionexpenseandcashrecoverybeforeusingmarketgrowth.','CP12 CP13 CP14 CP01 CP02','7','Author recommendation;sectorprofitconclusionwouldchangewithrepresentativepost-costcashrecoveryevidence.')
add('EN064','CP23containsonlyaccessfailure;CP10/20retainedweboutputs;MDX002/CP27duplicateandCP15/CP17sameunderlyingresearch.','CP23 CP10 CP20 MDX002 CP27 CP15 CP17','Evidence notes','Input/access characterization,notexternalfact;CP23isneverclaimsupportforexternalannouncement.')
jsonl(here/'claims.jsonl',claims)

(here/'data').mkdir(exist_ok=True)
with (here/'data/claims_registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['claim_id','claim','source_ids','report_section','uncertainty','calculation']);w.writeheader()
    for c in claims: w.writerow({**c,'source_ids':';'.join(c['source_ids']),'calculation':c.get('calculation','')})
with (here/'data/source_registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['source_id','title','url','frozen_text_path','sha256','actual_read_events','read_boundary','used_in_report']);w.writeheader()
    used=set(json.loads((here/'assembly-record.json').read_text())['used_source_ids'])
    for s in sources:
        events=[x for x in ledger if x['source_id']==s['source_id']]
        p=pack/s['local_original']
        boundary='See reading-ledger.json: recorded relevant text/page/image scopes, not automatic full-document reading.'
        if s['source_id'] in ['CP10','CP20']: boundary='Retained prior official web output; not a saved complete original website.'
        if s['source_id']=='CP23': boundary='Only TimeoutError record; substantive announcement unavailable and excluded.'
        w.writerow(dict(source_id=s['source_id'],title=s['title'],url=s['url'],frozen_text_path=str(p),sha256=sha(p),actual_read_events=';'.join(x['read_event_id'] for x in events),read_boundary=boundary,used_in_report=s['source_id'] in used))

task=json.loads((pack/'task.json').read_text(encoding='utf-8-sig'))
(here/'state').mkdir(exist_ok=True)
(here/'state/task_spec.md').write_text('# Effective independent English task specification\n\n'+task['prompt']+'\n\nAuthor boundary: current Codex continuation; no API call and no Astra authorship claim. Chinese report, calculations, claims and reviews were not read. Root coordinates independent review and final acceptance.\n\nFrozen input: '+str(pack)+'\n',encoding='utf-8')
requirements=[
 ('R01','Mainland domestic scope,2023–2026-11-09,annual/forecast/YTD distinctions','Opening;1;4;6'),
 ('R02','Defineformatsandconsistentmarketstructure','1,marketstructuretable'),
 ('R03','Payment/ad/acquisition/transactions/net-revenue accounting and double counting','1;4;5'),
 ('R04','Reconcileconflictingestimateswithoutaveraging','1,monetarycomparison'),
 ('R05','Users/time/frequency/paymentconversion/admonetization andretentionboundaries','2;5'),
 ('R06','Overlappingaudiences,multichannels,viewers/MAU/plays/payments','2;3;4'),
 ('R07','Paid/free/hybridacrossnative,mini-program,standalone','1;3;5'),
 ('R08','Recommendation/search,paid/organic,rights/exclusivity/sharing/supply','3,platformtable'),
 ('R09','Success/adjustmentexamplesandnoinferredexits','2;3;4'),
 ('R10','Valueflow,revenue,costsandworkingcapital','4;5'),
 ('R11','Executedassumedexampleandbudget/CAC/share/completion/retentionsensitivity','5;calculations.py;calculation-output.json'),
 ('R12','Regulation,copyright,minors,refundsandplatformpolicies','6'),
 ('R13','Participantdecisions,counterevidenceandreversalconditions','7,decisiontable'),
 ('R14','EnglishChina-specificexplanationandclaim-levelcitations','Allsections;claims.jsonl'),
 ('R15','Frozenfacts,sourceaccesslimitationsandindependentEnglishauthorship','Evidence notes;reading-ledger.json;handoff.md')
]
jsonl(here/'state/requirements.jsonl',[{'requirement_id':i,'requirement':r,'coverage':p,'author_assessment':'addressed_in_manuscript','independent_acceptance':'pending_root_review'} for i,r,p in requirements])
dump(here/'state/progress.json',{'case_id':task['case_id'],'stage':'independent_review_pending','author_draft_complete':True,'completed':False,'author':'current Codex','updated_at':now,'current_draft':'draft-current.md','independent_review_owner':'root','author_self_review_is_not_independent_acceptance':True})
dump(here/'state/final_delivery.json',{'case_id':task['case_id'],'completed':False,'accepted':False,'candidate':'draft-current.md','final_path':None,'reason':'Author handoff only; independent content review, audit and acceptance remain with root. Root will populate accepted final.md and final delivery state.'})
print(json.dumps({'claim_records':len(claims),'source_records':len(sources),'read_events':len(ledger),'status':'author records prepared; acceptance pending'}))
