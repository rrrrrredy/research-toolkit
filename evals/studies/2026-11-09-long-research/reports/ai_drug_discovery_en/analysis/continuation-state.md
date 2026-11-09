# AI drug discovery author continuation — paused between author turns for review capacity

Author: Codex `/root/ttc_research`. This is temporary research state, **not a completed report or an independent review**. Parent requested ending this turn to free an execution slot for early structure review. No model API calls, product edits, software tests, commits or publishing occurred. Existing TTC/Token/On-device files were not changed during this assignment.

## Scope and ready outline

Read the complete authoritative case `P/evals/cases/ai_drug_discovery_en.json`, existing `codex-inputs/outline.md` and `handoff.md`, the completed Astra planning JSON's structure and first two retained source observations. Original source observations are inherited and provisional; no Astra substantive unit output exists in the inspected topic directory.

New actual outline: `outline-v1.md`. Parent has been notified outline-ready. Seven retained cases: rentosertib, DSP-1181, EXS21546, REC-994, REC-4881, baricitinib, halicin. Four author units: U1rentosertib/mechanisms;U2otherclinicalcases;U3baricitinib/halicin;U4deals/comparison/synthesis. Complete English long report remains required; no length quota. All candidate/indication/formulation histories and cutoff distinctions retained.

P = `C:/Users/luosong03/Documents/ChatGPT/Others/work/toolkit-long-research-20261109`

R = `C:/Users/luosong03/Documents/ChatGPT/Others/work/astra-api-current-chat-20261109/work/implementation`

B = `R/research/ai_drug_discovery_en/codex-production`

## Acquired original material, not all read

Original packet has27source records,8downloaded originals andmany failures. Preserve all old folders. New acquisitions are in `supplemental-sources/`, each with raw bytes and timestamp/hash metadata. `acquire_sources.py` uses original existing HTML extractor; Python TLS failures on some hosts were solved through Windows PowerShell's working native HTTPS trust, without disabling certificate validation. `fetch_with_windows.ps1` is the successful alternative. `extract_downloads.py` produced original.txt and line-numbered `reading-lines.txt` that removes inline href annotations but retains original line numbers.

- **S01** official Nature HTML `https://www.nature.com/articles/s41587-024-02143-0`, retrieved748789bytes/text233297chars. Discovery fulltext. Fresh reading detailed below.
- **S02** official Nature HTML `https://www.nature.com/articles/s41591-025-03743-2`, retrieved562416bytes/text127476chars. Phase2a fulltext. Fresh reading below.
- **R01W** ClinicalTrials.govAPI JSON NCT05938920,92145bytes. **Acquired, not yet substantively read.**
- **R02W** NCT07687459,20627bytes. PhaseIII locator. **Acquired, not yet substantively read.**
- **R03W** NCT05085561,107522bytes. SYCAMORE. **Acquired, not yet substantively read.**
- **R04** NCT05920408,6616bytes. IGNITE oncology. **Acquired, not yet substantively read.**
- **R05** NCT04727138,7383bytes. EXS21546 early trial. **Acquired, not yet substantively read.**
- **S11** PMC7745180 ACTT-2 fulltext,547311bytes. **Acquired/extracted, not yet read.**
- **S12** PMC8409066 COV-BARRIER locator,246356bytes. **Identity and methods still to read.**
- **S13** PMC9333998 RECOVERY locator,1035741bytes. **Identity and methods still to read.**
- **S14** PMC4356181 CCM original,245528bytes. **Acquired, not yet read.**
- **S15** Frontiers2021expert-augmentedbaricitinibworkflow,1042326bytes. **Acquired, not yet read.**
- **S20** Alliance to Cure page carrying Recursion's May5,2025patientstatement,159556bytes/text30569chars. Web-read sponsor statement below; local fullpage acquired.
- **S03/S04** Recursion presentation/PDF urllib403; **S16/S17** corresponding Windows requests timedout40s. Preserve failures. Can use web PDF open/screenshot or actualissuerlinks as fallback.
- **S05/S18** Recursion2025SEC10K; **S19** Exscientia2023SEC20F:direct403. **Web tool opens succeeded**, but only initial no-body summaries returned; need explicit find/open relevant clauses. Do notcountfullfilingsread.
- S06–S10 andR01–R03 are earlierPythonTLSfailuremetadata, supersededacquisitionbyW/newIDs butnotdeleted.

All acquisition sessions have finished; no background process remains.

## Actual fresh substantive reading and findings

### Rentosertib discovery S01

Read `reading-lines.txt` lines114–142, including methods narrative,Figure1/2captions andselectivitypassage; previoustooloutputalso included selectedanimal/inhalation paragraphs but final use should revisitexactchosenmethods. PublicationMarch8,2024online/January2025print.

- PandaOmics combines IPFpatientmultiomics,network/textevidence andtemporalmodelvalidation. TNIKrankedfirstafter **protein/receptorkinase,novelty,smallmoleculedruggability** filters. Notunconstraineddiscoveryofunknownbiology.
- ExistingTNIK/WNT/TGFβ/Hippo/JNK/NFkBbiology andcrystalstructures contributed. TheprescribedATPpocket,Cys108hingeHbondandhydrophobicbackpocketpharmacophore areexpertconstraints inChemistry42.
- Synthesisselectionusesaccessibility,novelty,medicinalchemistryproperties. Earlynanomolarhits hadhighmicrosomalclearance,CYPinhibitionIC50<10μM,solubility<2μM. ADMEoptimizationledINS018_055. Needreadactualsupplementlinksandchemistry ratherthanassumeeveryloopretrainedmodel.
- SurfaceplasmonresonanceKd4.32nM. Kinasepanel10μMthen42top-hitIC50followup;TNIKIC5031nMmostinhibited,otherfibrosisrelevantkinasesalsohit. Notuniquetargetpurity. Existingbindingmodecomparisonsarepredictedvscrystalnotnew055cocrystalproof.
- Claimedrough18monthsendatpreclinicalcandidatenomination,nottrial/approval. ActualphaseIidentity/timing/supplementsnotyetread.

### Rentosertib Phase2a S02

Read `reading-lines.txt`119–143 (patientflow,primarysafety,secondarylungfunction,Figure2caption,PKopening). Directoriginalcontainsapparenttyposinhypokalemia/ALTlisting; do notcopythosefragileindividualAEcounts. NeedactualTable2and supplement.

-128screened,71randomized,30mgQD18/30mgBID18/60mgQD18/placebo17.12weeks.55completed(16/12/12/15respective);16discontinued(2/6/6/2).Allincludedinsafety/efficacyanalyses.
-PrimaryTEAE13/18,15/18,15/18,12/17. Treatment-relatedAE9/18,11/18,14/18,5/17. SeriousrelatedAE1/18,2/18,2/18,0/17.
-12of16discontinuationsAEs;7liverinjury/dysfunction:0lowQD,4BID,3highQD.4of7concurrentnintedanib. Thisisobservationalcoadministration,notprovedinteraction.
-MeanFVCchange-27.0(lowQD),+19.7(BID),+98.4highQD(95%CI10.9to185.9),-20.3placebo(CI-116.1to75.6). Rawdifference118.7mLnotreportedbetween-groupCI. Figure2bANCOVAwithmultipleimputationMAR. **Missing22week12spirometrycountfrominheritednoteNOTyetfreshread**;mustreadStatisticalanalysis/ExtendedData2.
-HighQDwithoutSOCsubgroup+187.8mL(CI68.6to306.9);withSOCnotsignificant. Needcounts/interactionbeforeinterpreting. DLCO/FEV1/QOL/6MWDmostlysimilar;LCQmodeledP.0495exploratory.3highQDvs1placeboacuteexacerbationswith3hospitalizationsinhighgroup;verysmallnumbers.
-ReadonlyPKopeninghalflife10.9–12h;notnecessaryforfullnumericalclaimunlessused.

### DSP1181 original AIDD06

Freshreadfirst100linesopening andtransitiontojointresearchhistory:2021technicalpaper,less12monthexploratorydiscoveryclaim,PhaseIJapan2020,OCD,combinedAI/optogenetics/translationalbiomarkerapproach. Mainmethods/optogenetics/researchclockexclusionsstillneedread. AIDD08stopcriterionprevioushandoffnotfreshlyreadthisturn.

### SponsorstatementREC994, webactualread

https://www.alliancetocure.org/statement-from-recursion-regarding-rec-994-trial/ May5,2025,nowlocalS20. ClearlyattributedRecursionpatientmessage: early400mgtrendsnotmaintainedLTEin400→400,200→400orplacebo→400;no significantMRI/functional improvement;stopfollowingtotality/long-termreview. Allianceisdistributionhostforprimarysponsormessage,notindependentclinicalpublication. Needseparateformaltrialresults/registerfortables.

### REC4881latestwebactualread, originalsnotyetlocal

https://ir.recursion.com/news-releases/news-release-details/new-phase-2-rec-4881-data-presented-cga-igc-show-deep-durable published **Nov2,2026**,beforecutoff;PDFhttps://ir.recursion.com/node/13186/pdf. 4mgQD12weekson12off;15evaluableWeek13,13/15reducedtotalburden,median47%;Week25 11/13belowbaseline. Safety26:21maxgrade1/2,4grade3,1noTRAE,no4/5;registrationaltrialanticipatedH22027pendingFDA. Mustreadpresentationtoexplain16efficacyevaluableversus15endoscopies,age18+expandedvsold55+,baselineexcision,adherence/missingness.

Presentation officialURLs located:
https://ir.recursion.com/static-files/644d572d-a9f8-430a-9412-559e361c3dd5 (32pages,cutoffSep10,2026)
https://ir.recursion.com/static-files/e3eb390d-76f3-4899-bb92-922eaaaf3c30 (possiblyotherpresentationversion;don'tmergeunchecked).
Webreturnedpage13oflatter:lowerGIWeek13n11of16efficacyevaluable,3nobaselinepolyps,1nolowerGIanatomy,1noWeek13endoscopy(openzerosquare);Week25n10withanotherdiscontinuedandoneunavailable,3baselinezero+1anatomy.4/11≥65%reductionWeek13;7/10belowbaselineWeek25. Week13excisedpolypburdenaddedbacktoWeek25. Needvieworiginalfigureandwholepresentationbeforefinaluse.

### PhaseIIIrentosertibwebactualread

OfficialInsilicofirstdoseSept10,2026 https://insilico.com/news/isn1009261-insilico-medicine-doses-first-patient-genesis-ipf-3 :GENESISIPF3aliasesISM001-055/INS018_055/rentosertib,NCT07687459,CTR20262475,52weekrandomizeddoubleblindplacebo. Distinguish fromothercompanypagecallingJuly2026"initiated". RegistryJSONR02Wmustreadfirstposted/updateandstudydate. ExistingR/sources/AIDD03samePRretained;oralvsinhaledA13indication/formulationseparate.

### EXS21546 registrylocator

SearchlocatedNCT05920408andNCT04727138viaindexrecords. **Do nottreatsecondaryindexasfinalevidence**;newprimaryJSONR04/R05obtained. Secondarysuggests6patients,April11,2023start,terminationforchallengeachievingsuitabletherapeuticindex,Nov8,2023update. These remainunverifieduntilprimaryJSONread. SEC20Fcanreconcileportfolio/competitionexplanationwithregistrywording.

## Immediate next work

1. Receiveparent'searlyindependentoutlineoutcome;donotselfreview.
2. ReadregistryJSONmodulesandrecordpublicdates. Ifcurrentrecordupdatedaftercutoff,obtainhistoryorusecontemporaneousdisclosureonlyforcutoffprogress. Lateractualresultsnotbackdated.
3. NatureS01/S02rawHTMLcontainsreal supplement/table URLs. ParsehrefstoMOESM/tablePDFlinks;downloadwithWindowsHTTPSifTLSfailure;readcriticalmethods/SAP/missingness/safetytables andoriginalfigures.
4. ReadS11–S15originals;acquireoriginalFDAactionsandFeb2020hypothesis. ExistingAIDD04CellPDFhalicinfulltextavailableandneedread.
5. ReadDSPpaperbeyondopening;Japaneseclinicalrecordandstoporiginal;REC994originalscreen/phaseI/trialdisposition;REC4881slidefiguresandTAK733rights;EXSfiling/registry.
6. Fileddealsmayrequirewebfind/openorofficialissuerPDFmirrorbecauseSECdirect403. Readoriginalclauses,notjustheadlinevalues. AggregateAIclinicalsuccesspaperstillunacquiredandcohortunread.
7. Executeonlyresearcharithmetic;writefullsubstantiveunits,claims,readingledger,firstcompleteEnglishreportandhandoff. No newmodelbenchmarks/tests/productmutations. No independentlyapprovedstatusclaimed.
