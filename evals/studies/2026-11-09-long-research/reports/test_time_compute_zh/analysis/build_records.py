import csv, hashlib, json, re, shutil
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
F=B.parents[2]/'frozen-alternate-inputs'/'test_time_compute_zh'
manifest=json.loads((F/'sources.json').read_text('utf-8-sig'))
ledger=json.loads((B/'reading-ledger.json').read_text('utf-8'))
# Correct the first batched tool output where an acknowledgement tail was truncated.
for e in ledger:
    if e['source_id']=='TTC001' and e['start']==174 and e['end']==215:
        e['end']=211
        e['note']='Only substantive lines through 211 retained; acknowledgement tail was truncated.'
    if e['source_id']=='TTC002' and e['start']==102 and e['end']==173:
        e['start']=110
        e['note']='Initial 102-109 were truncated in batched output and separately re-read in a later ledger entry.'
    if e['source_id']=='TTC012' and e['start']==95 and e['end']==188:
        e['note']='Lines 134-145 were truncated in this call and separately re-read in a later entry; union is the actual scope.'
        e['excluded_ranges_this_call']=[[134,145]]
dates={}
for source in manifest:
    path=F/source['local_original']; raw=path.read_bytes(); actual=hashlib.sha256(raw).hexdigest()
    if actual!=source['sha256']:
        raise ValueError('Frozen source hash mismatch: '+source['source_id'])
    for i,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        if line.startswith('arXiv:'):
            dates[source['source_id']]=line
            ledger.append(dict(source_id=source['source_id'],path=str(path),sha256=actual,
                               range_type='line',start=i,end=i,actual_read_scope='metadata line displayed in rg output',
                               at=datetime.now(timezone.utc).isoformat()))
            break
(B/'reading-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),'utf-8')
data=B/'data'; data.mkdir(exist_ok=True)
with (data/'source_registry.csv').open('w',encoding='utf-8-sig',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=['source_id','title','url','local_original','sha256','version_metadata','actual_read_ranges','read_scope','limitation'])
    writer.writeheader()
    for s in manifest:
        entries=[x for x in ledger if x['source_id']==s['source_id']]
        writer.writerow({k:s[k] for k in ['source_id','title','url','sha256']}|{
            'local_original':str(F/s['local_original']),
            'version_metadata':dates.get(s['source_id'],'Frozen conference/journal text; no arXiv metadata'),
            'actual_read_ranges':'; '.join(str(e['start'])+'-'+str(e['end'])+(' except 134-145 in this call' if e.get('excluded_ranges_this_call') else '') for e in entries),
            'read_scope':'relevant_sections','limitation':'Not a full-text reading claim; see line ledger and source original.'})
claims=[json.loads(x) for x in (B/'claims.jsonl').read_text('utf-8').splitlines() if x.strip()]
with (data/'claims_registry.csv').open('w',encoding='utf-8-sig',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=['claim_id','claim','source_ids','report_section','uncertainty']);writer.writeheader()
    for c in claims:writer.writerow(c|{'source_ids':';'.join(c['source_ids'])})
rawdir=B/'raw-responses';rawdir.mkdir(exist_ok=True)
for unit in sorted((B/'units').glob('*.md')):shutil.copyfile(unit,rawdir/unit.name)
shutil.copyfile(B/'draft-first.md',rawdir/'complete-author-response.md')
meta={'producer':'native Codex subagent /root/ttc_chinese_independent_author',
      'model_identity':'Current Codex session; no claim of Astra and no OpenAI API request in this author run.',
      'response_format':'Files authored through native tools, not an API response JSON. Full original authored units and first complete response retained.',
      'first_complete_sha256':hashlib.sha256((B/'draft-first.md').read_bytes()).hexdigest(),
      'units':sorted(p.name for p in (B/'units').glob('*.md')),
      'scope':'No English counterpart or other research task directories read.',
      'independent_review_status':'Outline requirements and structure/depth passed by other contexts; full-content review, audit and acceptance remain coordinator responsibilities.'}
(rawdir/'provenance.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),'utf-8')
state=B/'state';state.mkdir(exist_ok=True)
task=json.loads((F/'task.json').read_text('utf-8-sig'))
(state/'task_spec.md').write_text('# 原始任务\n\n'+task['prompt']+'\n\n# 本作者边界\n\n只完成独立中文研究作者成果；不读取英文稿，不运行Toolkit产品测试，不伪造完成回执。\n','utf-8')
(state/'progress.json').write_text(json.dumps({'stage':'draft','status':'awaiting_independent_content_review',
    'selected_draft':str(B/'draft-current.md'),'author_complete':True,'delivery_complete':False,
    'source_count':len(manifest),'claims_count':len(claims),'calculation_executed':True},ensure_ascii=False,indent=2),'utf-8')
report=(B/'draft-current.md').read_text('utf-8')
summary={'source_count':len(manifest),'sources_with_actual_reads':len({e['source_id'] for e in ledger}),
    'all_source_hashes_match_manifest':True,'claim_count':len(claims),
    'report_bytes':len(report.encode('utf-8')),'report_chinese_characters_including_tables_refs':len(re.findall(r'[\u4e00-\u9fff]',report)),
    'report_sha256':hashlib.sha256(report.encode('utf-8')).hexdigest(),
    'first_current_identical':(B/'draft-first.md').read_bytes()==(B/'draft-current.md').read_bytes()}
(B/'author-artifacts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
