"""Dispatch only the twenty already planned reviews as paired reports become ready."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util, time
from pathlib import Path
spec=importlib.util.spec_from_file_location('review',Path(__file__).with_name('quality-study-review.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
p=r.s.plan();done=set();started=time.monotonic()
with ThreadPoolExecutor(max_workers=2) as pool:
 while len(done)<len(p['tasks'])*2:
  for t in p['tasks']:
   if all((r.s.OUT/'authors'/t['id']/c/'report.md').exists() for c in ['before','after']):
    for swap in [False,True]:
     key=(t['id'],swap)
     if key not in done:
      done.add(key)
      def execute(task=t,orientation=swap):
       try:r.judge(p,task,orientation)
       except Exception as e:print('ERROR',repr(e),flush=True)
      pool.submit(execute)
  if time.monotonic()-started>7200:raise RuntimeError('Author pairs still incomplete after two hours; original records retained')
  if len(done)<len(p['tasks'])*2:time.sleep(10)
print('All planned review dispatches finished.',flush=True)
