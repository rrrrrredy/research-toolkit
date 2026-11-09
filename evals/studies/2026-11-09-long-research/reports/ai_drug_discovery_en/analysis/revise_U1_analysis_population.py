from pathlib import Path
import json, hashlib
from datetime import datetime, timezone
B=Path(__file__).resolve().parent
src=B/'U1-rentosertib.md'
t=src.read_text(encoding='utf-8')
old='The most encouraging lung-function signal was in the 60 mg once-daily group:'
start=t.index(old)
end=t.index('\n\nOther outcomes reinforce',start)
new='''The publication reports two distinct FVC analyses. Figure 2a summarizes participants with observed week-12 measurements; Figure 2b uses baseline-adjusted ANCOVA and multiple imputation under a missing-at-random assumption for the randomized groups. The registry's absolute-FVC outcome likewise separates the available-data means from the model-based least-squares means. These are different populations and estimators, not interchangeable presentations of one result. [Original Figure 2](https://www.nature.com/articles/s41591-025-03743-2/figures/2), [registered results](https://clinicaltrials.gov/study/NCT05938920).

| FVC change at week 12 | 60 mg once daily | Placebo | Author subtraction of reported group point estimates |
|---|---|---|---|
| Observed cases, Figure 2a | n = 10; +98.4 mL (95% CI 10.9 to 185.9) | n = 14; −20.3 mL (95% CI −116.1 to 75.6) | 118.7 mL |
| ANCOVA with multiple imputation, Figure 2b | Randomized n = 18; +89.2 mL (95% CI −8.7 to 187.2) | Randomized n = 17; −8.2 mL (95% CI −98.1 to 81.7) | 97.4 mL |

Both analyses contain a favorable high-dose point estimate, but the observed-case result describes the people who contributed the measurement, while the imputed analysis extends to the randomized groups under its model assumptions. The high-dose group's modeled confidence interval includes zero. Neither subtraction above is a newly estimated between-group effect with a confidence interval; neither a within-group interval nor the overlap of separate group intervals is a valid substitute for the randomized treatment-contrast test.

Week-12 spirometry was missing for 22 of 71 participants, including 8 of 18 at the highest once-daily dose and 3 of 17 on placebo. Thus, 44.4% of the high-dose group lacked the measurement, compared with 17.6% of placebo. The observed-case analysis can be affected by which patients remained measurable; the full-group model depends on how unobserved outcomes are imputed. Discontinuation and missing lung-function measurements may relate to tolerability or clinical course, making missing-not-at-random sensitivity analyses important. These concerns do not erase the directionally favorable signal. They define what a larger, longer trial must resolve before the change can be interpreted as established clinical benefit.'''
t=t[:start]+new+t[end:]
t += '\n\nRevision 01 author note: independent clinical review identified conflation of observed-case and imputed FVC analyses in the initial unit. Original U1-rentosertib.md and original calculations are preserved. The author subsequently viewed the actual Figure 2 PNG and read R01W resultsSection absolute-FVC rows and analyses. This correction does not claim an independent pass.\n'
(B/'U1-rentosertib-revision-01.md').write_text(t,encoding='utf-8')
r=json.loads((B/'calculations-results.json').read_text(encoding='utf-8'))
r['revision_01_executed_utc']=datetime.now(timezone.utc).isoformat()
r['rentosertib']={
 'observed_cases':{'active_n':10,'placebo_n':14,'active_change_ml':98.4,'placebo_change_ml':-20.3,'difference_ml':98.4-(-20.3),'equation':'98.4 - (-20.3)'},
 'ANCOVA_multiple_imputation_MAR':{'active_randomized_n':18,'placebo_randomized_n':17,'active_LS_change_ml':89.2,'placebo_LS_change_ml':-8.2,'difference_ml':89.2-(-8.2),'equation':'89.2 - (-8.2)'},
 'meaning':'Two distinct analyses; differences are subtraction of reported group point estimates, not a new contrast CI or hypothesis test',
 'missing_total_pct':100*22/71,'missing_60qd_pct':100*8/18,'missing_placebo_pct':100*3/17,'withdrawal_pct':100*16/71
}
(B/'calculations-results-revision-01.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
note={'author':'Codex /root/ttc_research','reason':'Independent clinical domain major finding: observed-case FVC numbers had been conflated with ANCOVA+MI analysis','original_unit':src.name,'original_unit_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'revised_unit':'U1-rentosertib-revision-01.md','original_calculation':'calculations-results.json','revised_calculation':'calculations-results-revision-01.json','new_actual_reading':['supplemental-sources/AIDD-S02/figure-2.png:actual visual inspection panels a and b','supplemental-sources/AIDD-R01W/download.bin:resultsSection.outcomeMeasuresModule Absolute Change From Baseline in FVC in L,denoms/classes/analyses'],'figure_url':'https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41591-025-03743-2/MediaObjects/41591_2025_3743_Fig2_HTML.png','review_status':'requires original reviewer confirmation; not self-passed','math_execution':'Only revised descriptive arithmetic; prior other calculations carried forward without rerun'}
(B/'U1-revision-01-notes.json').write_text(json.dumps(note,indent=2),encoding='utf-8')
print(json.dumps(note,indent=2))
