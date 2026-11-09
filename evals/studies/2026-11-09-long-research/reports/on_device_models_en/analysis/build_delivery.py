"""Assemble the first author manuscript and provenance records; never overwrite a first draft."""
from pathlib import Path
import json,hashlib,re
B=Path(__file__).resolve().parent;R=B.parents[2]
producer='Codex /root/ttc_research; substantive author, not independent reviewer'
units=['ODM-U1-mechanisms-and-evidence.md','ODM-U2-workload-envelopes.md','ODM-U3-architecture-economics-decisions.md']
u=B/units[0]
u.write_text(u.read_text(encoding='utf-8').replace('https://news.samsung.com/us/enter-the-new-era-of-mobile-ai-with-samsung-galaxy-s24-series/','https://news.samsung.com/us/enter-new-era-of-mobile-ai-samsung-galaxy-s24-series/'),encoding='utf-8')
records=[]
def read(sid,scope,findings,supp=False):
 d=(B/'supplemental-sources' if supp else R/'sources')/sid
 meta=json.loads((d/'retrieval.json').read_text(encoding='utf-8'))
 records.append({'source_id':sid,'url':meta.get('url'),'version_or_access':meta.get('accessed_at'), 'original_path':str(d/('original.pdf' if (d/'original.pdf').exists() else 'original.txt')),'reading_path':str(d/'original.txt'),'sha256':meta.get('sha256'),'reading_location':scope,'findings_used':findings,'reader':producer,'read_scope':'selected original passages actually read, not a claim to have read every page'})
read('ODM01','Device table; §§5.2.2–5.4, especially continuous50prompt experiment and quantization discussion','Older iPhone14Pro/S23/JetsonAGX mechanisms; sustained performance, responsiveness, dequantization. Not an S24 forecast.')
read('ODM02','On-device architecture, compression and framework overview','Later Apple update is version context; July report supplies version-specific numerical quality table.')
read('ODM03','Gemma3n effective parameter and PLE/MatFormer explanation','Total and effective parameter distinction; no fabricated universal memory footprint.')
read('ODM04','Super hardware specification and software enablement','102GB/s,67sparseTOPS,25Wmodulemode;historical$249kitprice,notall-inbox.')
read('ODM05','Current platform/model performance table and SDK status','Current table is Gemma4/S26; excluded from historicalS24 arithmetic.')
read('ODM07','§§3–4.1,Tables1–3 and comparisons; §4.4 selected','M4Pro16GPU24GB273GB/s;117.3decode,835prefill;no universal runtime win;separate-phase limits.')
read('ODM11','Requirements,statelessprocessing,node encryption,logging/transparency architecture','Vendor-described privacy architecture;not third-party app/tool guarantee.')
read('ODM12','Capabilities/device lists,modelversions,quotas/background;updated2026-11-06','Topforegroundonly;foregroundservicealso blocked;feature-specific eligibility;noS24systemAPIclaim.')
read('ODM13','Data use;abusemonitoring;retention controls and endpoint-state table','No training bydefault differs from retention;30-daystandardabusemonitoring subjectexceptions.')
read('ODM14','QNNHTPquantization,fixedshapes,calibration,CPUfallbackoption','Operation/backend graph and driver constraints;not a measured NPUtokenrate.')
read('ODM15','Abstract;§§3.2–4.2','Activation-aware scaling and hardware-dependent packing/fusion;no blanket4xrealizedclaim.')
read('ODM17','pp4–7 experimentalsetup;pp9–10precision/Table4;visuallyreadp10','Independent70clipstudy;baseline-subtractedCPU+GPUenergy;int8basecounterexample;paperWERformula typo not inherited.')
read('ODM18','2026WWDCpanel opening model-selection question and local/PCCcontext discussion','Conference support context;currentAPI originalsS25/S28/S29 establish documented interfaces.')
read('ODM21','S24Ultrahardwaretable,availabilitydate,chipsetdiscussion','12GBandSnapdragon8Gen3;installednotavailablememory.')
read('ODM23','WWDC2025 framework modelpurpose,typedgeneration,sessions,availability','Task-oriented API and structural versus semantic validity.')
read('ODM-S01','Complete configuration JSON','36layers,16query/2KVheads,hidden2048,slidingwindowdisabled,max32768.',True)
read('ODM-S02','Actual3Bmodel paragraph;requirements and licensing header','3.09Bparameters,32768context;family128Kdoesnotapplyto3B;model-specificlicense remains relevant.',True)
read('ODM-S06','Quantizationmethod,English instructionquality rows,OnePlus12CPUperformance table','3BMMLU63.4/60.5/62/62.4;rewritequality;OnePlusnumbers readbutnotusedasS24benchmark.',True)
read('ODM-S10','Complete pinnedREADMEperformanceandusage','20sclip0.86vs2.55;base439vs666;engineinitializationdistinct.',True)
read('ODM-S12','PinnedREADME2025-07-21lines55–77,benchmarkCLIandmodel-loadingnotes','S24actualGemma3n/Gemma3rows;1024prefill256decode;4Kcontext;firstloadcompilation.',True)
read('ODM-S13','CompletebenchmarkREADME','SavedCSVolderreference;currentcomparison harness not proof of paper configuration.',True)
read('ODM-S14','Defaults,modelmap,KVprecision,invocations andaggregation','5reps20scooldowncurrent defaults;f16KVsetting cannot retrospectively establish paper settings.',True)
read('ODM-S17','§2architecture,§6compression,§7framework,§8Tables1–3;visuallyp17','July2025v1quality67.8→64.4MMLU85.1→82.3IFEval;adapterversiondependence.',True)
read('ODM-S18','FinalICML38pp;§§3–6.5,Table1p7,Table2p9,discussionprivacy;visuallyp7','FinalMinions cost-quality andtenLongHealthlatencies;localfreeaccountingnotdeploymentTCO.',True)
read('ODM-S19','Complete profilingcode','Warmup+singledefaultiteration;GPU synchronization;RSSdeltaMiBnotpeak.',True)
read('ODM-S20','VAD and transcriptionprocess bodies;initialization/queues','End-of-utteranceoutput;unbounded VADsegment needslongstream handling.',True)
read('ODM-S21','transcribe andbuilderprecision/engine sections','Meltruncate;greedyargmax;FP16engine default;modelbuildoutsidebenchmarktimer.',True)
read('ODM-S23','RawMicrosoftdocs introduction/readiness/code','OlderJan2026rawrepo differs currentOct2026Learnpage;retainedratherthanblended.',True)
read('ODM-S25','FoundationModels currentoverview andmodel/API links','LocalandPCCsupport,taskfocus andsystemrequirements.',True)
read('ODM-S26','Completeavailabilitysymbolmetadata','OS26localavailability;futuretvOS27.3metadata not claimedavailable.',True)
read('ODM-S27','Audiohyperparameterconstants','30secchunk,16kHz,3000melframes;confirmswindowinterpretation.',True)
read('ODM-S28','Overview,capabilitytable,platformrequirements,entitlementandquota','Local4K/PCC32K;version27PCC;managedentitlement,dailyquota,networkdependence.',True)
read('ODM-S29','Availabilitymethods,entitlement,quotas,unavailablereasons andversionheading','Modelreadiness/versionchecks;OS26enabledstate;OS27changeddefaultnotgeneralized.',True)
for sid,url,scope,find in [
('ODM-W01','https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica','Currentwebpage lines34–116,updated2026-10-19','LAF;Chinaexcluded;NPUavailable;GPUexperimental;AionNovInsiderJan2027retailplan;notallrolledout.'),
('ODM-W02','https://learn.microsoft.com/en-us/surface/tech-specs/surface-laptop-snapdragon-tech-specs','HardwaretableCPU/NPU/RAM/OS;currentofficialwebpage','SurfaceX1E80100and32GBsupportedconfiguration;45TOPSnotLLMmeasurement.')]:
 records.append({'source_id':sid,'url':url,'reading_location':scope,'findings_used':find,'reader':producer,'access_date':'2026-11-09','access_scope':'Actual web tool read; no locally captured fullcurrentpage claimed'})
(B/'reading-ledger.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
claims=[
('ODM-C01','App available memory and fullworking set determine admission; installedRAMandfilefitinsufficient.',['ODM01','ODM-S01','ODM-S02'],'measured mechanisms plus scenario'),
('ODM-C02','Qwen3B BF16KV36KiB/token;phone8Kplanned3.792GiBunderassumed4GiB.',['ODM-S01','ODM-S02'],'calculated scenario'),
('ODM-C03','S24Gemma3nE2BGPUacceleratesprefillwithoutincreasingreporteddecode.',['ODM-S12'],'historical vendor measurement'),
('ODM-C04','M4ProBaseRTLlama3BQ4winsdecodebutnot2048prefillagainstllamacpp;MLXwinsoneMoErow.',['ODM07'],'author measurement'),
('ODM-C05','Quantizationhas task-specificqualitycost; recoverytraininghelps.',['ODM-S06','ODM-S17','ODM15'],'vendor evaluation plus mechanism'),
('ODM-C06','Shortmobilebenchmarks cannot establishsustainedservice.',['ODM01'],'independent measured mechanism'),
('ODM-C07','Minions tradeslocalwork forcloudcost atnearremotequality;notphoneorprivacyproof.',['ODM-S18'],'author study withexplicitboundary'),
('ODM-C08','WhisperTRT.043RTF iswarmclipcapacity,notstreamingfirstwordlatency.',['ODM-S10','ODM-S19','ODM-S20','ODM-S21','ODM-S27'],'vendor benchmark pluscodeinspection'),
('ODM-C09','WhisperXbaseint8useslessreportedmemory butmoreincrementalenergy/slowerthanfp16inthestudy.',['ODM17'],'independent study'),
('ODM-C10','MLKitforegroundquotasanddeviceeligibilityconstrainbackgroundproductarchitecture.',['ODM12'],'documentedcurrentcapability'),
('ODM-C11','Localinference,PCC,andstandardAPIretentionhavedifferentboundaries.',['ODM11','ODM13','ODM-S28'],'documented architecture/policy'),
('ODM-C12','Platformmodelversionandentitlementaredeploymentdependencies.',['ODM-W01','ODM-S17','ODM-S29'],'documented integration'),
('ODM-C13','Engineeringandcorrectioncanoutweighlocalenergy;ownershipandacceptancedenominatorchangeeconomics.',['calculation-results.json'],'explicit hypotheticalscenario')]
(B/'claims.jsonl').write_text('\n'.join(json.dumps({'claim_id':cid,'claim':claim,'sources':src,'type':kind,'author':producer},ensure_ascii=False) for cid,claim,src,kind in claims)+'\n',encoding='utf-8')
appendix='''
## Appendix: provenance and interpretation of the worked envelopes

The report uses public material from 2023 through 9 November 2026, including dated historical measurements where they explain the selected hardware. The cited web pages are access-date snapshots unless a release or commit is specified. Numerical scenarios are author calculations, not observed acceptance, price, power or throughput measurements. Decimal MB/GB are used for transfer sizes; MiB/GiB are binary memory units. Device manufacturers' installed-memory labels are retained as published.

| Evidence item | Preserved version and actual reading | Interpretation retained in the report |
|---|---|---|
| Qwen2.5-3B-Instruct | Official model card and full configuration JSON, acquired at cutoff | Model-specific 32K context, full-attention cache formula; weight and application reservations remain scenarios |
| S24 phase measurements | LiteRT-LM README commit `eaa380eee74b677f9f305eb2a92ae0fcc14ffc39`, 21 July 2025 | 1,024-token prefill, 256-token decode, four-bit per-channel artifacts and 4K context. Current Gemma 4/S26 table is a different experiment |
| M4 Pro comparison | BaseRT arXiv `2607.00501v1`, §§4.1–4.3 and Tables 1–3 | Paper rates and baseline versions; later repository CSV and KV defaults do not retroactively establish the paper's full setup |
| Quantization quality | Meta official Llama 3.2 card; Apple `2507.13575v1`, Table 3 visually inspected | Task and optimization-method differences; July Apple quality values kept separate from later updates |
| Sustained mobile behavior | MELT `2403.12844v4`, §5.2.3 | Historical iPhone 14 Pro/Jetson AGX mechanisms, not an inferred S24 thermal curve |
| Collaborative documents | Final ICML 2025 Minions paper, 38 pages; Table 1 visually inspected, Table 2 and methods read | Historical cloud prices, local-free accounting, workstation latency; no formal privacy guarantee |
| Speech optimization | WhisperTRT commit `268eff10a1e38118a2734745b9db14f7419a08a5`, 15 October 2024; README and profiling/live/model code read | Warm single-clip timing, RSS delta, decoder differences and 30-second-window handling |
| Speech noise and precision | ASR energy paper `2405.01004`, setup pp.4–7 and Table 4 visually inspected on p.10 | Aggregate experiment, incremental CPU/GPU energy, synthetic-noise procedure; repository unavailable at access time |
| Current APIs | ML Kit page updated 6 November 2026; current Apple developer Markdown; Microsoft Learn page updated 19 October 2026 | Availability, quotas, entitlement, channel and planned transitions; older raw Microsoft repository page preserved separately |

Several source details affect the arithmetic. The WhisperTRT README labels memory as MB, while its profiler computes MiB and samples an RSS difference rather than a peak. Its `base.en` ratio is 439/666 = 65.9% of the original path's reported memory; the report uses the actual values rather than treating the promotional “about 60%” as precise. The independent speech paper's printed WER formula contains an apparent insertion-term typo; the interpretation here uses the conventional `(substitutions + deletions + insertions) / reference words`. Its unavailable code and unspecified exact aggregate audio duration prevent a precise reconstruction of real-time factor or wall energy.

The original handoff's S24 attribution was checked against the current LiteRT page, found to refer to a different table, and resolved by retrieving the historical S24 commit. An unrelated PMLR page acquired during the Minions search is excluded; the final Narayan et al. paper is the source used. Earlier notes and originals are retained rather than rewritten as if these distinctions were known at acquisition.

The accompanying `deployment_calculations.py` and `calculation-results.json` contain the executed memory, phase-time, clip-RTF, power-duty, transfer and economic arithmetic. They run no model inference and make no claim to validate a device. `reading-ledger.json` records the original paths and selected locations actually read; `key-premises-for-review.md` maps the material assumptions for independent review.

For a concrete deployment, the remaining measurements are specific: available and peak working memory on the intended device state; first usable and complete-result latency with the real prompt/output distribution; sustained behavior for the actual operating duration and concurrent apps; task quality on representative documents, languages or acoustic conditions; and endpoint-level power if battery or thermal sizing depends on it. Those missing deployment measurements bound the recommendations here. They are not filled by transferring a rate from another device, runtime or task.
'''
draft='\n\n'.join((B/x).read_text(encoding='utf-8').strip() for x in units)+'\n\n'+appendix
target=B/'draft-first.md'
if target.exists():raise SystemExit('First manuscript already exists; preserve and write a separately named revision.')
target.write_text(draft,encoding='utf-8')
sha=hashlib.sha256(target.read_bytes()).hexdigest()
handoff={'topic':'on_device_models_en','producer':producer,'status':'complete first author manuscript; independent review pending','first_manuscript':str(target),'sha256':sha,'word_count':len(re.findall(r"\b[\w’-]+\b",draft)),'units':units,'calculations':'deployment_calculations.py;calculation-results.json','reading_records':len(records),'claims':len(claims),'preservation':'Original API outputs and product files unchanged; first complete manuscript must not be overwritten.'}
(B/'handoff.json').write_text(json.dumps(handoff,indent=2),encoding='utf-8')
(B/'full-response.json').write_text(json.dumps({'author':producer,'report_markdown':draft,'handoff':handoff,'reading_notes':records,'claim_registry':[{'id':x[0],'claim':x[1],'source_ids':x[2],'type':x[3]} for x in claims]},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(handoff,indent=2))
