"""Address independent evidence finding TE-U2-EV-01; preserve first manuscript and calculations."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
review=B.parent/'native-TE-U2-reviews/evidence/fresh-context/response.json'
finding=json.loads(review.read_text(encoding='utf-8'))['findings'][0]
unit=B/'TE-U2-three-workloads.md'; first=B/'draft-first.md'
backup=B/'TE-U2-three-workloads.first.md'
if backup.exists() or (B/'draft-revision-01.md').exists():raise SystemExit('Revision exists; preserve it.')
backup.write_bytes(unit.read_bytes())
first_sha=hashlib.sha256(first.read_bytes()).hexdigest()
old_intro='The sensitivities show where to work first:'
new_intro='The sensitivities show where to work first. The four output rows are **direct output-charge perturbations with every input history, cached-prefix ledger, retry/fallback path, tool charge, human-work allowance and acceptance rate held fixed**. They isolate the generated-output line of the bill; they do not recompute a fully retained conversation after changing its output lengths:'
old_para='Output compression has value when quality holds; reducing review or failed cycles can have substantially more value. That is why reasoning effort should be treated as a decision variable with a measured success response. Doubling reasoning is beneficial if it reduces sufficiently expensive downstream work; otherwise it is added latency and cost. The table intentionally holds quality fixed to isolate the price effect, not to imply that reasoning is useless.'
new_para='The output rows quantify only the direct billing effect under those fixed inputs. For example, at four times output, the first baseline call generates 8K tokens from 4K input while the next input remains the original 8K in this calculation. A workflow retaining the entire generated output would already require at least 12K tokens before adding new user or tool content. Its later input, cache writes/reads, compaction, timing and possibly quality would need to be recalculated; the $9.0383 figure is not the cost of that full-history workflow. Output compression can save direct output charges when quality holds, while reducing review or failed cycles can have substantially more value in the separate sensitivities shown. Reasoning effort should therefore be treated as a decision variable with a measured success response and a complete downstream trajectory when making an actual deployment choice.'
def revise(text):
 if text.count(old_intro)!=1 or text.count(old_para)!=1:raise ValueError('Expected unique sensitivity passages missing.')
 return text.replace(old_intro,new_intro).replace(old_para,new_para).replace('| Half the billed output per call, unchanged quality |','| Half the billed output per call, fixed input/path/quality |').replace('| Original output |','| Original output, fixed input/path/quality |').replace('| Twice the billed output, unchanged quality |','| Twice the billed output, fixed input/path/quality |').replace('| Four times the billed output, unchanged quality |','| Four times the billed output, fixed input/path/quality |')
unit.write_text(revise(unit.read_text(encoding='utf-8')),encoding='utf-8')
current=B/'draft-revision-01.md';current.write_text(revise(first.read_text(encoding='utf-8')),encoding='utf-8')
if hashlib.sha256(first.read_bytes()).hexdigest()!=first_sha:raise ValueError('First manuscript changed.')
note={'author':'Codex /root/ttc_research; not reviewer','finding_id':finding['finding_id'],'review_path':str(review),'change':'Label output rows as direct output-charge perturbations at fixed input/cache/path/quality; explicitly exclude induced context growth and give the4K+8Kcounterexample. No arithmetic or model rerun.','first_draft':str(first),'first_draft_sha256':first_sha,'first_unit':str(backup),'current_unit':str(unit),'current_draft':str(current),'current_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'independent_review_status':'Revision prepared for original reviewer confirmation; no author pass claim.'}
(B/'revision-01-notes.json').write_text(json.dumps(note,indent=2),encoding='utf-8')
(B/'full-response-revision-01.json').write_text(json.dumps({'report_markdown':current.read_text(encoding='utf-8'),'revision':note,'original_full_response':'full-response.json','reading_notes':'reading-ledger.json','calculations':'calculation-results.json'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(note,indent=2))
