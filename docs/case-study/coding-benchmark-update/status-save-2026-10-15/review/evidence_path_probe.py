"""R2: an explicit retained original path and a separate reading note."""
import sys, json, tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'research-toolkit/scripts'))
import research_workflow as w
from check_research_workflow import BRIEF
with tempfile.TemporaryDirectory(prefix='ar-',dir=BASE/'a14tmp') as d:
    ws=Path(d)
    w.start(ws,'xml',BRIEF,profile='lite')
    root=ws/'xml'
    (root/'source.xml').write_text('<value>12</value>',encoding='utf-8')
    (root/'reading.md').write_text('Read XML value twelve.',encoding='utf-8')
    first=w.save_records(ws,'xml',sources=[{'title':'Source','url':'https://example.org',
        'source_type':'primary','evidence_path':'source.xml','read_scope':'full_text','read_evidence':'reading.md'}],
        claims=[{'claim':'Twelve','claim_type':'fact','supporting_sources':['S1']}],
        draft={'path':'final.md','content':'Twelve [source](https://example.org)'})
    bound=w.required_source_inputs(root)
    (root/'source.xml').write_text('<value>13</value>',encoding='utf-8')
    changed=w.save_records(ws,'xml',sources=[{'source_id':'S1'}])
    changes=changed['changes']
    passed=(changes['source_files']['S1']['status']=='changed' and
        changes['source_files']['S1']['paths']==['reading.md','source.xml'] and
        changes['affected_claims'][0]['claim_id']=='C1')
    result={'passed':passed,'required_source_inputs':bound,'first':first['changes']['source_files'],
        'after_content_change':changes}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if passed else 1)
