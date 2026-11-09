from pathlib import Path
import csv,json,re,hashlib
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
R=B.parents[2]
now=datetime.now(timezone.utc).isoformat()
author='Codex /root/ttc_research; substantive author, not independent reviewer'
readings=[
 ('AIDD04','2020-02-20','Original PDF29pages','pp4–5,7–8,11–12,e6; extracted340–437,720–820,1318–1384,2140–2190','Model training;prospective Hub and ZINC testing;mechanism;animal routes/limitations'),
 ('AIDD05','2020-01-30','Sponsor release','Announcement of initiated Japanese phaseI','DSP identity and start announcement,not exact dosing date'),
 ('AIDD06','2021','Scientific technical account','opening100lines and pp3–4/extracted154–306','DSP loop,350th compound,clock excludes safety;only selected biological-context passages'),
 ('AIDD08','2022-01-31','Management transcript','p12/extracted232–249','DSP discontinued after unmet expected phaseI criterion'),
 ('AIDD03','2026-09-10','Sponsor first-dose release','Firstdose announcement and registryID','Oral phaseIII advancement'),
 ('AIDD-A13','2026-04-28','Sponsor inhalation release','extracted462–481','Separate inhaled IND and proposed phaseI design'),
 ('AIDD-S01','2024-03-08 online;2025 print','Nature fullHTML','114–146,147–175,175–184','Targetfilters/design/ADME/geneticcellularanimalphaseI;not all references or supplementary files'),
 ('AIDD-S02','2025-06-03','Nature fullHTML','119–182;188–191;Figure2 actual PNG panelsa/b after review','Safety/flow/FVC/missingness/MAR;observed vs modeled analysis corrected'),
 ('AIDD-S11','2020','ACTT2 original fullHTML','333–356','Design,protocolresponsibility,randomizedcounts,recovery,mortality,backgroundtreatment'),
 ('AIDD-S12','2021','COVBARRIER original fullHTML','188–195;506–530','Primaryfail,multiplicityhierarchy,secondarymortality,safety'),
 ('AIDD-S13','2022','RECOVERY original fullHTML','92–105','Randomizeddesign,mortality,backgroundmedications'),
 ('AIDD-S14','2015','CCM original fullHTML','192–245;252','Automatedvsmanualscreen;orthogonalassay;tempolmouseP.0518'),
 ('AIDD-S15','2021','BenevolentAI workflow originalHTML','305–352','KG/NLP,expertquerying,networkmethods;noautonomyassumption'),
 ('AIDD-S20','2025-05-05','Sponsorstatement on patientorganization site','185–192','REC994 stop and loss of sustained MRI/functional trends'),
 ('AIDD-S21','authorupdated2025-04-02','Nature Reporting Summary PDF','Rendered actual view pages1,2,3','Not protocol/SAP;outlieranalysis mentioned;trial dates'),
 ('AIDD-S23','2025-06-03','Nature original Table2HTML','33–96','Safety counts and footnotes;all relevant rows'),
 ('AIDD-S24','2020-02-04 online;corrected2020-06-18','Original baricitinib correspondence','128–141','Repurposinghypothesis,AAK1,JAK,expertfiltering'),
 ('AIDD-S25','2022-05-10','FDA dated bulletin','Complete short notice (also weboriginalread)','Adultapproval and2020/2021EUAhistory'),
 ('AIDD-S27','2022-01','Issuer mirror original6-KPDF','Sanofi agreement summary;corroborated web6-K71–109','Paymentcategories,roles,license,governance'),
 ('AIDD-R01W','lastpost2025-12-11','ClinicalTrials.gov rawJSON','protocol identification/status/design/arms/outcomes;after review results absoluteFVC denoms/classes/analyses','71randomized;observed13/12/10/14 vs modeledn18/18/18/17'),
 ('AIDD-R02W','lastpost2026-10-13','ClinicalTrials.gov rawJSON','identification/status/design/arms/outcomes','Oral tablets;320estimated;actualstartSep9;firstpostJuly7;52weeks'),
 ('AIDD-R03W','firstresultspost andlastpost2026-10-22','ClinicalTrials.gov rawJSON','protocol/status;participantFlow;alloutcomeMeasures summaryrows,populations,denominators','62;21/21/20groups;different safety exposure windows;month12functionaloutcomes'),
 ('AIDD-R04','lastpost2023-11-08','ClinicalTrials.gov rawJSON','protocol identification,status,design,description,arms,outcomes','6actual;terminated;therapeuticindexreason;combinationdescription'),
 ('AIDD-R05','lastpost2022-05-16','ClinicalTrials.gov rawJSON','protocol identification,status,design,arms,outcomes','64healthy men;phaseIstart/completion'),
 ('AIDD-R06','lastpost2026-06-05','ClinicalTrials.gov rawJSON','protocol status/design/arms/outcomes','TUPELO recruiting/openlabel/nonrandomized;67estimated;startJuly2023')
]
rows=[]
for sid,pub,kind,scope,purpose in readings:
    d=(B/'supplemental-sources'/sid) if sid.startswith('AIDD-') and not sid.startswith('AIDD-A') else R/'sources'/sid
    meta=json.loads((d/'retrieval.json').read_text(encoding='utf-8-sig'))
    originals=[x for x in ['original.pdf','original.html','download.bin'] if (d/x).exists()]
    rows.append({'source_id':sid,'url':meta.get('url',''),'publication_or_version':pub,'kind':kind,'original_path':str(d/originals[0]) if originals else '', 'text_path':str(d/('reading-lines.txt' if (d/'reading-lines.txt').exists() else 'original.txt')),'actual_reading_scope':scope,'use':purpose,'read_by':author,'retrieved_at':meta.get('accessed_at',meta.get('extraction_recovered_at','2026-11-09')),'sha256':meta.get('sha256',''),'access_status':meta.get('status','')})
webs=[
 ('WEB-EXAI2023','https://www.sec.gov/Archives/edgar/data/1865408/000186540824000018/exai-20231231.htm','2023annual,filed2024','603,2134–2150,2946,4050–4058,6059','Termination/roles/ownership;not fullfiling'),
 ('WEB-EXAI2022','https://d18rn0p25nwr6d.cloudfront.net/CIK-0001865408/2107e6d3-671e-4154-ba91-4e0c84f7bb7a.pdf','2022annual','Primary indexed excerptp90','9month/163designclaim;notfullPDFread'),
 ('WEB-EXAIUK2023','https://s28.q4cdn.com/460399462/files/doc_financials/2023/ar/fy23-exs-plc-uk-ar_final.pdf','2023annual','Primary indexed JointOperations passage','Original50/50,Evotecoptout40%,floor10%'),
 ('WEB-RXRX2025','https://www.sec.gov/Archives/edgar/data/1601830/000160183026000039/rxrx-20251231.htm','2025annual,filed2026','613–627;1350–1369;1450–1466;2014;5134–5143','REC4881origin,licensedrights,Takedapayment;Rocheaccountingcheckedbutnotallfactsused'),
 ('WEB-R4881CGA','https://ir.recursion.com/static-files/e3eb390d-76f3-4899-bb92-922eaaaf3c30','2026-11-02;data2026-09-10','Web-extracted17pagePDF pp4–6;lowerGIfootnotes','Naturalhistory47;26=5+21;16/21efficacy;no successful localvisualreview'),
 ('WEB-R4881EARN','https://ir.recursion.com/static-files/644d572d-a9f8-430a-9412-559e361c3dd5','2026-11-03;data2026-09-10','Web-extracted52pagePDF pp20–21,23–24,29footnotes','15/16week13;13/16week25;excisionsaddedback;not32pages'),
 ('WEB-R4881PR','https://ir.recursion.com/news-releases/news-release-details/new-phase-2-rec-4881-data-presented-cga-igc-show-deep-durable','2026-11-02','lines13–75','Currentclinicalresults and safety;plan2027notachieved'),
 ('WEB-R994PR','https://ir.recursion.com/node/10581/pdf','2024-09-03','Primaryindexed datedheadlineandopening','OriginalsafetyandMRItrendannouncement'),
 ('WEB-R994P1','https://pubmed.ncbi.nlm.nih.gov/38655895/','2024','Primaryindexedabstract;lateropenreturnedemptybody','AliasREC994=tempol;noadditionalphaseIdataasserted'),
 ('WEB-EVOTEC','https://www.evotec.com/sciencepool/translational-biomarkers-in-oncology','availableby2026-11-09','84–115','WholebloodpCREBCD8targetengagementcase;notclinicalefficacy'),
 ('WEB-EVOTECPOSTER','https://f.hubspotusercontent40.net/hubfs/462745/Sciencepool/Posters/Evotec%20posters/non-brain-penetrant-a2ar-inhibitor-immunotherapy.pdf','historical poster;date not independently established','singlepageextracted123–192,218','EVOEXS21546alias and predevelopmentprofile;noapprovalclaim'),
 ('WEB-SANOFICONTRACT','https://www.sec.gov/Archives/edgar/data/1865408/000186540822000005/exscientia-sanoficollabora.htm','2022-01-04 agreement','1309–1370;clauses20–23','PlatformIP,programlicenses,datause restrictions,redactions'),
 ('WEB-SANOFIOPTION','https://ir.recursion.com/news-releases/news-release-details/recursion-announces-sanofi-options-potential-first-class','2026-10-15','17–31','10Mmilestone,144Mtotal,developmenthandoff,phaseIplanned2027'),
 ('WEB-ROCHE2021','https://www.sec.gov/Archives/edgar/data/1601830/000119312521349657/d242203d8k.htm','2021-12-05agreement,filedDec7','96–121','Mapdataaccess,externaluseoptions,programrights/payments'),
 ('WEB-ROCHERECEIPT','https://www.sec.gov/Archives/edgar/data/1601830/000160183022000012/R26.htm','2021financialsubsequentevents','PrimaryshortnotereceivedJanuary2022','150MreceiptseparatefromDec2021announcement'),
 ('WEB-GENENTECH','https://recursion.com/news/unlocking-the-first-neuroscience-target-for-the-recursion-and-genentech-collaboration','2026-08-05','12–44','Firsttargetoption andjointearlydiscovery;identityundisclosed'),
 ('WEB-AICOHORT','https://www.researchgate.net/publication/380223979_How_successful_are_AI-discovered_drugs_in_clinical_trials_A_first_analysis_and_emerging_lessons','2024;authoruploadedMay9','345–429;504–595;632–795;720–724/803–806','21/24,4/10,broadcohort,COVIDexclusion,stoppingcategories;nosupplementrowreaudit'),
 ('WEB-INSILICODOSE','https://insilico.com/news/isn1009261-insilico-medicine-doses-first-patient-genesis-ipf-3','2026-09-10','Datedfirstdoseannouncement','PhaseIIIannouncementnotJulyregistration')
]
for sid,url,pub,scope,purpose in webs:
    rows.append({'source_id':sid,'url':url,'publication_or_version':pub,'kind':'Primary material read through web tool; method qualified in scope','original_path':'','text_path':'web-reading/ (partial captures when present); actual tools history otherwise','actual_reading_scope':scope,'use':purpose,'read_by':author,'retrieved_at':'2026-11-09','sha256':'','access_status':'web text; original download status separate'})
(B/'reading-ledger.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
with (B/'source-registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
claims=[
 ('C01','AI contributes identifiable selection and optimization steps; whole-pipeline causality is not established','synthesis','AIDD-S01;AIDD06;AIDD-S14;AIDD04','U1,U2,U3','Interpretation based on distinct demonstrated mechanisms'),
 ('C02','Rentosertib target ranking and design were constrained by existing biology,tractability and pharmacophore choices','sourcefact','AIDD-S01','U1','No claim that TNIK biology was whollyunknown'),
 ('C03','Rentosertib discovery clock ends at preclinical nomination','sourcefact','AIDD-S01','U1','18months notapproval'),
 ('C04','Rentosertib observedFVC n10/14 +98.4/−20.3; modeledn18/17 +89.2/−8.2','correctedsourcefact','AIDD-S02 Figure2;AIDD-R01W results','U1revision01','Independentclinicalmajor identified prior conflation;correction awaiting confirmation'),
 ('C05','FVC descriptivedifferences118.7/97.4mL;22/71missing8/18vs3/17','authorarithmetic','AIDD-S02;AIDD-R01W;calculations-results-revision-01.json','U1revision01','Neither subtraction is contrastCI;MAR assumption retained'),
 ('C06','Rentosertib oralphaseIII recruitingSep2026;inhaledbranchINDseparate','sourcefact','AIDD-R02W;AIDD03;AIDD-A13','U1','Registration/start/doseannouncementseparated'),
 ('C07','DSP loop<12months excludes safety,350th compound;discontinuedJan2022','sourcefact','AIDD06;AIDD08','U2','Exact clinicalcriterion notpubliclyresolved'),
 ('C08','EXS21546 healthyvolunteer64 vs patientstudy6terminatedfor therapeuticindexconcern','sourcefact','AIDD-R04;AIDD-R05;WEB-EXAI2023','U2','No inventedtoxicityorresponserate'),
 ('C09','CCM MLscreen7/38 orthogonalhits versusmanual1/38','sourcefactandarithmetic','AIDD-S14','U2','Matchedselectedsets only;mouse temposevidenceP≈.052 separately'),
 ('C10','REC994 initialMRItrend notsustained;developmentstoppedMay2025','sourcefact','AIDD-S20;AIDD-R03W;WEB-R994PR','U2','Registrycompleted doesnotmeancontinueddevelopment'),
 ('C11','REC994 registryresultspostOct22,2026;combinedsafety exposurewindowsnotmatched','sourcefact','AIDD-R03W','U2','Do notcomparecountsas12monthrandomizedsafety'),
 ('C12','REC4881 islicensedTAK733 withnewFAP phenotypichypothesis','sourcefact','WEB-RXRX2025;AIDD-R06','U2','Notdenovogeneratedstructure'),
 ('C13','REC4881 safety26=5+21;efficacy16;week13 n15;week25 n13','sourcefact','WEB-R4881CGA;WEB-R4881EARN;WEB-R4881PR','U2','Selectedexposure/adherencepopulation;naturalhistorynotcontrol'),
 ('C14','Baricitinib AIassociatedrepurposing precedes strongrandomized COVIDevidenceandadultapproval','sourcefactandsynthesis','AIDD-S24;AIDD-S15;AIDD-S11;AIDD-S12;AIDD-S13;AIDD-S25','U3','Existingdrug;COVBARRIERprimarynegative,mortalitynominal;noAIcausalefficacyestimate'),
 ('C15','HalicinHub51/99highvs2/63low;separateZINC8/23anyspecies','sourcefactandarithmetic','AIDD04','U3','Halicinnotfrom107Mbranch;nohumanclinicalclaim'),
 ('C16','Historicalcohort21/24and4/10 notcurrentcausalAIprobabilities','sourcefactandarithmetic','WEB-AICOHORT;calculations-results-revision-01.json','U4','AuthorWilsonconditionalonly;notfullcohortreaudit'),
 ('C17','Sanofi candidatehandoff leavesclinicalmanufacturingcommercializationwithSanofi','sourcefact','AIDD-S27;WEB-SANOFICONTRACT;WEB-SANOFIOPTION','U4','PlatformIP/dataprogramrightsseparate;redactedallocationsunresolved'),
 ('C18','Sanofi100Mupfront,~5.2Bcontingentceilings;Oct2026 10Mtrigger144Mtotal','sourcefactandarithmetic','AIDD-S27;WEB-SANOFIOPTION','U4','No ceilingascash/revenue;candidateplanned2027phaseI'),
 ('C19','Takedaexclusiveworldwidelicense1.5Mupfront39.5Mmilestonesplusroyalties','sourcefact','WEB-RXRX2025','U4','Existingassetlicense,currentFAPprogram'),
 ('C20','Rochemaps/rawimage/programoptions aredifferentrights;firsttargetearlydiscovery2026','sourcefact','WEB-ROCHE2021;WEB-ROCHERECEIPT;WEB-GENENTECH','U4','NounnamedtargetmappedontoREC4881orclinicalsuccess'),
 ('C21','Fundnextfalsifiableexperimentalorclinicaldeliverable ratherthanplatformlabel','authorrecommendation','C01-C20','U4','Conditionaldecisions;noindustrycensus')
]
fields=['claim_id','claim','type','sources','unit','qualification']
with (B/'claims-registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(fields);w.writerows(claims)
(B/'claims-registry.json').write_text(json.dumps([dict(zip(fields,c)) for c in claims],indent=2,ensure_ascii=False),encoding='utf-8')
# Preserve the complete first manuscript. Current copy fixes only observed spacing defects.
t=(B/'draft-first.md').read_text(encoding='utf-8')
parts=re.split(r'(\]\([^\n]*?\))',t)
for i,s in enumerate(parts):
    if s.startswith(']('):continue
    s=re.sub(r'\b(than|that|of|to|completion|uses|on|through|baseline|population|with|and|by|disclosed|announced)(?=\d)',r'\1 ',s)
    s=re.sub(r'(?<=\d), (?=\d{3}(?:\D|$))',',',s)
    s=re.sub(r'(?<=[,;])(?=\d{1,2}%|95%|P=)', ' ',s)
    s=s.replace('confidence interval0','confidence interval 0').replace('odds ratio0','odds ratio 0')
    for old,new in [('announcement10','announcement 10'),('disclosure2','disclosure 2'),('REC-994,400','REC-994, 400'),('CI0.','CI 0.'),('HR0.','HR 0.'),('P=.','P = 0.'),('IIa,11','IIa, 11'),('III,13','III, 13'),('study,16','study, 16'),('IGNITE,8','IGNITE, 8'),('SYCAMORE,22','SYCAMORE, 22'),('TUPELO,5','TUPELO, 5'),('participants,21','participants, 21'),('at4 mg,16','at 4 mg, 16'),('participants,15','participants, 15')]:
        s=s.replace(old,new)
    parts[i]=s
current=''.join(parts)
(B/'draft-current.md').write_text(current,encoding='utf-8')
manifest={'author':author,'created_utc':now,'first':'draft-first.md','first_sha256':hashlib.sha256((B/'draft-first.md').read_bytes()).hexdigest(),'current':'draft-current.md','current_sha256':hashlib.sha256((B/'draft-current.md').read_bytes()).hexdigest(),'current_words':len(current.split()),'current_change':'Typographic spacing only after actual artifact inspection; first complete retained','substantive_basis':'U1 revision01 plusU2–U4; U1 initial text/calculations retained','source_reading_records':len(rows),'claim_records':len(claims),'independent_review':'Not claimed; coordinator owns independent review'}
(B/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
