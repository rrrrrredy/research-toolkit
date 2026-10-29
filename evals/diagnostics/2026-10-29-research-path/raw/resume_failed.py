import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

base=Path(__file__).resolve().parent
repo=base.parents[1]/'research-toolkit'
commands=[]
for label in ('check_research_workflow','check_record_workflow'):
    text=(base/(label+'.log')).read_text(encoding='utf-8')
    names=re.findall(r'^(?:ERROR|FAIL): (test_\w+) \(__main__\.(\w+)',text,re.M)
    commands.append([f'scripts/{label}.py',*[f'{cls}.{name}' for name,cls in dict.fromkeys(names)]])
with tempfile.TemporaryDirectory(prefix='rt15-',dir=os.environ['PUBLIC']) as tmp:
    env=dict(os.environ,IRF_TEST_TMPDIR=tmp,TMP=tmp,TEMP=tmp,PYTHONIOENCODING='utf-8')
    results=[]
    for args in commands:
        command=[sys.executable,'-B',*args]
        began=time.monotonic()
        run=subprocess.run(command,cwd=repo,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
        label=Path(args[0]).stem
        (base/(label+'.resolved.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
        results.append(dict(command=command,returncode=run.returncode,elapsed_seconds=round(time.monotonic()-began,3),temporary_root=tmp))
        print(json.dumps(results[-1]),flush=True)
        print(run.stderr[-1200:],flush=True)
    (base/'resolved-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
