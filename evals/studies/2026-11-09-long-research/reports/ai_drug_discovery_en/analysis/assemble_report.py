"""Assemble the first complete English author manuscript from actual research units."""
from pathlib import Path
import re,json,hashlib
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
def space_prose(t):
    # Protect Markdown URL/path targets while correcting author typing spacing.
    parts=re.split(r'(\]\([^\n]*?\))',t)
    words='about among and approximate approximately are abstract account clauses counts day derived distinguishes explanations for from full historical initial its lines methods operations original passages publication published ratio release revision scored services start The through versus was with'.split()
    for i,s in enumerate(parts):
        if s.startswith(']('): continue
        s=re.sub(r'\b('+ '|'.join(words)+r')(?=\d)',r'\1 ',s)
        s=re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)(?=\d)',r'\1 ',s)
        s=re.sub(r'(?<=\d)(?=January|February|March|April|May|June|July|August|September|October|November|December)', ' ',s)
        s=re.sub(r'(?<=\d)(?=million\b|billion\b|percentage\b|points\b|mL\b|mg\b)', ' ',s)
        s=re.sub(r'(?<=%)(?=CI\b|and\b|Wilson\b)', ' ',s)
        s=re.sub(r'(?<=,)(?=\d)', ' ',s) if '|' in s and '1,033' not in s else s
        for a,z in [('E.coli','E. coli'),('A.baumannii','A. baumannii'),('C.difficile','C. difficile'),('EUA2020','EUA 2020'),('95%CI','95% CI'),('1.16,95','1.16, 95'),('0.57,95','0.57, 95'),('0.87,95','0.87, 95'),('programs: $100','programs: $100')]: s=s.replace(a,z)
        parts[i]=s
    return ''.join(parts)
def body(name,stop):
    t=(B/name).read_text(encoding='utf-8').split('\n',2)[2]
    t=re.sub(r'^Author:.*?\n\n','',t,count=1,flags=re.S)
    t=t.split(stop)[0].strip()
    return t
sections=[(B/'report-opening.md').read_text(encoding='utf-8')]
for title,name,stop in [
 ('3. Rentosertib: connecting target discovery, molecular design and clinical testing','U1-rentosertib-revision-01.md','## Author evidence notes'),
 ('4. Designed molecules and phenotypic repositioning: four development histories','U2-clinical-programs-and-attrition.md','## Author reading and unresolved'),
 ('5. Repurposing and prospective selection: baricitinib and halicin','U3-repurposing-and-prospective-discovery.md','## Author evidence and calculations')]:
    t=body(name,stop)
    t=re.sub(r'^## ', '### ',t,flags=re.M)
    sections.append('## '+title+'\n\n'+t)
t=body('U4-comparison-partnerships-decisions.md','## Author reading scope and calculations')
t=t.replace('## What the selected programs support','## 6. Stage-aware comparison: what the selected programs support')
t=t.replace('## How to interpret speed and success-rate comparisons','### How to interpret speed and success-rate comparisons')
t=t.replace('## Partnership structures determine whether information becomes an asset','## 7. Partnership structures, rights and economics')
t=t.replace('## Decisions for R&D, business-development and investment teams','## 8. Decisions for R&D, business-development and investment teams')
sections.append(t)
sections.append((B/'report-appendix.md').read_text(encoding='utf-8').replace(' Independent review of this manuscript is a separate step from author production.',''))
text=space_prose('\n\n'.join(s.strip() for s in sections))+'\n'
# Correct targeted punctuation without changing numbers or source URLs.
text=text.replace('day28','day 28').replace('95% on','95% on').replace('covariate.','covariate.')
target=B/'draft-first.md'
with target.open('x',encoding='utf-8') as f:f.write(text)
manifest={'author':'Codex /root/ttc_research','created_utc':datetime.now(timezone.utc).isoformat(),'language':'en','evidence_cutoff':'2026-11-09','artifact':'draft-first.md','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'word_count':len(text.split()),'basis':['report-opening.md','U1-rentosertib-revision-01.md','U2-clinical-programs-and-attrition.md','U3-repurposing-and-prospective-discovery.md','U4-comparison-partnerships-decisions.md','report-appendix.md'],'first_complete_manuscript':True,'independent_review_status':'not claimed; U1 revision awaiting original reviewer confirmation; full report pending independent review','calculations_current':'calculations-results-revision-01.json','prior_unit_and_calculations_preserved':True}
(B/'first-draft-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
