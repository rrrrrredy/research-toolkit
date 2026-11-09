from acquire_sources import raw
import concurrent.futures,json
W='268eff10a1e38118a2734745b9db14f7419a08a5'
items=[('ODM-S25','https://developer.apple.com/documentation/foundationmodels.md'),('ODM-S26','https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel/availability-swift.property.md'),('ODM-S27','https://raw.githubusercontent.com/openai/whisper/main/whisper/audio.py')]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:
  for r in p.map(lambda x:raw(*x),items):print(json.dumps(r),flush=True)
