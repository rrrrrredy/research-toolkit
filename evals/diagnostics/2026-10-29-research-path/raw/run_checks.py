"""Run existing affected checks once; retain commands, timings and complete output."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import re

base=Path(__file__).resolve().parent
repo=base.parents[1]/'research-toolkit'
tmp=repo.parent/'rt150'
tmp.mkdir(exist_ok=True)
env=dict(os.environ,IRF_TEST_TMPDIR=str(tmp),TMP=str(tmp),TEMP=str(tmp),PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
checks=[
 ['scripts/check_research_workflow.py','WorkflowTests'],
 ['scripts/check_draft_contract.py'],
 ['scripts/check_record_workflow.py'],
 ['scripts/check_task_continuity.py'],
 ['scripts/check_release_updates.py'],
 ['scripts/check_task_lock.py'],
 ['scripts/check_profiles_reviewers.py'],
 ['scripts/build_plugin.py','--check'],
 ['scripts/check_plugin_build.py'],
 ['scripts/check_version.py','--self-test'],
 ['scripts/run_dsh_evals.py','validate'],
 ['scripts/build_site.py','--check'],
 ['scripts/check_site.py','--self-test'],
]
previous=json.loads((base/'checks.json').read_text()) if (base/'checks.json').exists() else []
results=[row for row in previous if row['returncode']==0]
passed={Path(row['command'][2]).stem for row in results}
if previous:
    (base/'checks-initial.json').write_text(json.dumps(previous,indent=2),encoding='utf-8')
for args in checks:
    label=Path(args[0]).stem
    if label in passed:
        continue
    log=base/(label+'.log')
    if label=='check_research_workflow' and log.exists():
        old=log.read_text(encoding='utf-8')
        failed=re.findall(r'^(?:ERROR|FAIL): (test_\w+) \(__main__\.WorkflowTests',old,re.M)
        if failed:
            args=[args[0],*[f'WorkflowTests.{name}' for name in dict.fromkeys(failed)]]
    if log.exists():
        log.rename(base/(label+'.initial.log'))
    started=time.monotonic()
    command=[sys.executable,'-B',*args]
    try:
        p=subprocess.run(command,cwd=repo,env=env,capture_output=True,text=True,encoding='utf-8',timeout=180)
        code=p.returncode
        output=p.stdout+'\n'+p.stderr
    except subprocess.TimeoutExpired as e:
        code=None
        output='Timeout; retained partial output.\n'+str(e.stdout or '')+'\n'+str(e.stderr or '')
    (base/(label+'.log')).write_text(output,encoding='utf-8')
    results.append(dict(command=command,returncode=code,elapsed_seconds=round(time.monotonic()-started,3),log=label+'.log'))
    (base/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results[-1]),flush=True)
    if code:
        print(output[-1800:],flush=True)
