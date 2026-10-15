from pathlib import Path
from datetime import datetime
import csv, hashlib, json
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
CASE=BASE/'research-toolkit/docs/case-study/coding-benchmark-update/status-save-2026-10-15'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
summary=read(CASE/'execution-summary.json')
calls=[json.loads(line) for line in (CASE/'calls.jsonl').read_text(encoding='utf-8-sig').splitlines()]
start=datetime.fromisoformat(calls[0]['started_at'])
timing={'to_draft':(datetime.fromisoformat(calls[3]['finished_at'])-start).total_seconds(),
        'to_finish':(datetime.fromisoformat(calls[7]['finished_at'])-start).total_seconds(),
        'cli_sum':round(sum(c['elapsed_seconds'] for c in calls),3),
        'calls':len(calls),'nonzero_exits':sum(c['exit_code']!=0 for c in calls)}
original=[]
for name,expected in summary['original_file_sha256'].items():
    path=BASE/'a14tmp/update'/name
    original.append({'name':name,'matches':digest(path)==expected})
source_compare=[{'name':p.name,'exact_bytes_equal':p.read_bytes()==(BASE/'a14tmp/update/sources'/p.name).read_bytes()}
                for p in (BASE/'a14tmp/changes/sources').glob('S*.md')]
def registry(path,kind):
    if kind=='requirements': rows=[json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()]
    else:
        with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    field={'sources':'source_id','claims':'claim_id','requirements':'requirement_id'}[kind]
    return {r[field]:r for r in rows}
changes={}
for kind,name in [('sources','data/source_registry.csv'),('claims','data/claims_registry.csv'),('requirements','state/requirements.jsonl')]:
    old=registry(BASE/'a14tmp/update'/name,kind);new=registry(BASE/'a14tmp/changes'/name,kind)
    changes[kind]={'old_count':len(old),'new_count':len(new),'ids_equal':old.keys()==new.keys(),
                   'updated':[key for key in new if key in old and new[key]!=old[key]]}
copies=[]
for pub,local in [('previous-report.zh-CN.md','previous-final.md'),('first-update.zh-CN.md','drafts/change-first.md'),('report.zh-CN.md','final.md'),('source-checks.md','source-recheck-20261015.md')]:
    copies.append({'published':pub,'local':local,'same_bytes':(CASE/pub).read_bytes()==(BASE/'a14tmp/changes'/local).read_bytes()})
for call in calls:
    for key in ['request','response']:
        pub=CASE/'calls'/call[key];local=BASE/'output/change-continuation-20261015'/call[key]
        copies.append({'published':'calls/'+call[key],'same_bytes':pub.read_bytes()==local.read_bytes()})
result={'timing_recomputed':timing,'original_files':original,'source_texts':source_compare,
        'record_diff':changes,'publication_copies':copies,'report_nonwhitespace_characters':sum(not c.isspace() for c in (BASE/'a14tmp/changes/final.md').read_text(encoding='utf-8'))}
with (OUT/'case-evidence-recheck.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'timing':timing,'original_files_all_equal':all(x['matches'] for x in original),
 'sources_all_equal':all(x['exact_bytes_equal'] for x in source_compare),'record_diff':changes,
 'publication_all_equal':all(x['same_bytes'] for x in copies)},ensure_ascii=False,indent=2))
