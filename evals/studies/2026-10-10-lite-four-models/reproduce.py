#!/usr/bin/env python3
"""Reproduce this fixed five-family pilot in a new directory (paid model calls)."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path);p.add_argument('--prepare-only',action='store_true');p.add_argument('--include-format-supplement',action='store_true',help='Apply the separately declared post-hoc fence policy after primary attempts lock');a=p.parse_args()
 output=a.output.resolve()
 if output.exists():p.error('Output must be a new directory; first attempts are never overwritten.')
 original=json.loads((HERE/'study-plan.json').read_text(encoding='utf-8'))
 driver=HERE/'run_live_study.py'
 if hashlib.sha256(driver.read_bytes()).hexdigest()!=original['driver_sha256']:p.error('Study driver differs from the frozen version.')
 frozen=json.loads((HERE/'runs/deepseek/coordinator/frozen.json').read_text(encoding='utf-8'))
 for name,digest in frozen['method_sha256'].items():
  if hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode()).hexdigest()!=digest:p.error('Toolkit methods changed; use the study revision before reproducing the same intervention.')
 if hashlib.sha256((ROOT/'scripts/run_blinded_evals.py').read_text(encoding='utf-8').encode()).hexdigest()!=hashlib.sha256((HERE/'harness-snapshot.py').read_text(encoding='utf-8').encode()).hexdigest():p.error('Harness changed; use the study revision.')
 if not a.prepare_only:
  for key in ['DEEPSEEK_API_KEY','KIMI_API_KEY','GLM_API_KEY','LONGCAT_API_KEY']:
   if not os.environ.get(key):p.error('Set '+key+' in the process environment; never place keys in source files.')
  if not (os.environ.get('CODEX_BIN') or shutil.which('codex')):p.error('Install and authenticate Codex CLI, or set CODEX_BIN. The judge requests gpt-6-astra.')
 output.mkdir(parents=True)
 shutil.copy2(driver,output/driver.name)
 if a.include_format_supplement:
  for name in ['run_format_supplement.py','format-supplement-policy.json']:shutil.copy2(HERE/name,output/name)
 for name in ['briefs','sources']:shutil.copytree(HERE/'inputs'/name,output/'inputs'/name)
 for name in ['tasks.json','source-manifest.json']:shutil.copy2(HERE/'inputs'/name,output/'inputs'/name)
 env=os.environ.copy();env['RESEARCH_TOOLKIT_ROOT']=str(ROOT)
 subprocess.run([sys.executable,str(output/driver.name),'freeze'],env=env,check=True)
 if a.prepare_only:return 0
 def run(provider):return subprocess.run([sys.executable,str(output/driver.name),'run','--provider',provider],env=env).returncode
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:codes=list(pool.map(run,['deepseek','glm','kimi','longcat']))
 if any(codes):return max(codes)
 if a.include_format_supplement:
  for provider in ['deepseek','glm','kimi','longcat']:
   subprocess.run([sys.executable,str(output/'run_format_supplement.py'),'--provider',provider],env=env,check=True)
 unresolved=sum(row['status']!='judged' for provider in ['deepseek','glm','kimi','longcat'] for row in json.loads((output/'runs'/provider/'results.json').read_text(encoding='utf-8'))['results'])
 print(f'Preserved all primary attempts, including {unresolved} unresolved pairs; inspect original results and the separately labeled supplement.')
 return 1 if unresolved else 0
if __name__=='__main__':raise SystemExit(main())