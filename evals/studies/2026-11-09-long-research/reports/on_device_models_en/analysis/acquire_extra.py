from acquire_sources import raw, f, B
import concurrent.futures,json
W='268eff10a1e38118a2734745b9db14f7419a08a5'
L='eaa380eee74b677f9f305eb2a92ae0fcc14ffc39'
items=[
('ODM-S10',f'https://raw.githubusercontent.com/NVIDIA-AI-IOT/whisper_trt/{W}/README.md'),
('ODM-S11',f'https://api.github.com/repos/NVIDIA-AI-IOT/whisper_trt/git/trees/{W}?recursive=1'),
('ODM-S12',f'https://raw.githubusercontent.com/google-ai-edge/LiteRT-LM/{L}/README.md'),
('ODM-S13','https://raw.githubusercontent.com/basecompute/baseRT/main/benchmarks/README.md'),
('ODM-S14','https://raw.githubusercontent.com/basecompute/baseRT/main/benchmarks/scripts/three_way_benchmark.sh'),
('ODM-S15','https://raw.githubusercontent.com/basecompute/baseRT/main/benchmarks/results/m4-pro_baseRT.csv'),
('ODM-S16','https://api.github.com/repos/zzadiues3338/ASR-energy-jetson'),
]
pdfs=[{'id':'ODM-S17','url':'https://arxiv.org/pdf/2507.13575v1'},
{'id':'ODM-S18','url':'https://raw.githubusercontent.com/mlresearch/v267/main/assets/narayan25a/narayan25a.pdf'}]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  for r in pool.map(lambda x:raw(*x),items):print(json.dumps(r),flush=True)
  for r in pool.map(f.fetch,pdfs):print(json.dumps(r),flush=True)
