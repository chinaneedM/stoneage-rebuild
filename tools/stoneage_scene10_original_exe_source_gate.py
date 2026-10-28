"""One bounded MediaFire RAR prefix attempt for original SCENE10 EXE callsites.
16 MiB max original archive data; never publish original EXE, PNG, RAR or raw opcodes.
Positive conclusion requires exact whole executable SHA and individual original E8 rel32 bytes.
No branch/body/caller state, full-frame sequence, or world execution is implied.
"""
from __future__ import annotations
import argparse,hashlib,json,re,struct,subprocess,urllib.request
from pathlib import Path
from tools.stoneage_wayi85_sixpart_acquisition import direct_link
ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/'research/recovered/STONEAGE-SCENE10-PRIVATE-CALLS-R1.json'
KEY='ev7l29fw77891go'
LIMIT=16*1024*1024
P1_BYTES=209715200
ORIGINAL_BYTES=561152
EXE_SHA='ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16'
KEY_TARGETS=(0x42a924,0x401137,0x44ca11,0x427aa4,0x44c4a3)
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise ValueError(msg)
def validate_candidate(c):
 need(c['schema']=='stoneage.scene10.private_numeric_callsite_candidate.r1','candidate schema')
 need(c['source_exe_sha256_claim']==EXE_SHA and c['key_targets']==list(KEY_TARGETS),'source claim')
 paths=c['paths'];need(len(paths)==4 and sum(len(x['direct_calls']) for x in paths)==43,'call count')
 need(c['total_calls']==43 and c['unreplayed_intervening_calls']==23,'unreplayed count')
 for p in paths:
  calls=p['direct_calls'];need(len(calls)>=5,'calls')
  addrs=[x['call_va'] for x in calls];targets=[x['target_va'] for x in calls]
  need(addrs==sorted(set(addrs)) and addrs[0]==p['start_va'] and all(p['start_va']<=x and x+5<=p['end_va_exclusive'] for x in addrs),'callsite range')
  need([t for t in targets if t in KEY_TARGETS]==list(KEY_TARGETS),'required phase order')
  need(p['full_outer_path_executed'] is False,'not live execution')
 need(c['original_exe_independently_qualified'] is False and c['original_world_entered'] is False,'negative qualification')
 return 43
def rel32_target(exe,va):
 off=va-0x400000
 need(0<=off and off+5<=len(exe),'source VA outside bounded executable')
 op=exe[off:off+5]
 need(op[0]==0xe8,'not direct relative CALL at VA')
 delta=struct.unpack('<i',op[1:5])[0]
 return va+5+delta, sha(op)
def check_source(exe,c):
 need(len(exe)==ORIGINAL_BYTES and sha(exe)==EXE_SHA,'whole EXE SHA mismatch')
 results=[]
 for p in c['paths']:
  row=[]
  for item in p['direct_calls']:
   actual,hash5=rel32_target(exe,item['call_va'])
   need(actual==item['target_va'],'native call target differs from unverified private candidate')
   row.append({'call_va':item['call_va'],'target_va':actual,'five_source_bytes_sha256':hash5})
  results.append({'path_index':p['path_index'],'calls':row,'verified_calls':len(row),'outer_path_executed':False})
 return results
def try_source(work,c):
 ua={'User-Agent':'Mozilla/5.0'}
 with urllib.request.urlopen(urllib.request.Request(f'https://www.mediafire.com/file/{KEY}/',headers=ua),timeout=60) as r:
  page=r.read(4*1024*1024+1);need(len(page)<=4*1024*1024,'source page too large')
  ref=r.geturl()
 url=direct_link(page.decode('utf-8','replace'))
 with urllib.request.urlopen(urllib.request.Request(url,headers={**ua,'Referer':ref,'Range':f'bytes=0-{LIMIT-1}'}),timeout=120) as r:
  cr=r.headers.get('Content-Range','')
  need(r.status==206 and cr==f'bytes 0-{LIMIT-1}/{P1_BYTES}','exact content-range required')
  raw=r.read(LIMIT+1)
 need(len(raw)==LIMIT and raw.startswith(bytes.fromhex('526172211a0700')),'original RAR prefix qualification')
 src=work/'source-prefix.rar';src.write_bytes(raw)
 meta={'http_status':206,'content_range':cr,'prefix_bytes':len(raw),'prefix_sha256':sha(raw)}
 listing=subprocess.run(['7z','l','-slt',str(src)],capture_output=True,text=True,errors='replace',timeout=90)
 paths=[]
 for line in listing.stdout.splitlines():
  if line.startswith('Path = ') and line[7:].lower().endswith('/sa_2903.exe'):
   paths.append(line[7:])
 if len(paths)!=1:
  meta.update(list_returncode=listing.returncode,listed_matching_paths=len(paths))
  return 'PREFIX_DOES_NOT_PROVE_EXE_AVAILABILITY',meta,None
 target=paths[0]
 out=work/'selected';out.mkdir()
 proc=subprocess.run(['7z','x','-y',f'-o{out}',str(src),target],capture_output=True,text=True,errors='replace',timeout=90)
 hits=[x for x in out.rglob('sa_2903.exe') if x.is_file()]
 if len(hits)!=1:
  meta.update(list_returncode=listing.returncode,extract_returncode=proc.returncode,matching_files=len(hits))
  return 'TARGET_NOT_EXTRACTABLE_FROM_PREFIX',meta,None
 exe=hits[0].read_bytes()
 if len(exe)!=ORIGINAL_BYTES or sha(exe)!=EXE_SHA:
  meta.update(extract_returncode=proc.returncode,extracted_bytes=len(exe),source_sha256=sha(exe))
  return 'TARGET_WHOLE_SHA_NOT_QUALIFIED',meta,None
 result=check_source(exe,c)
 meta.update(extract_returncode=proc.returncode,source_exe_bytes=len(exe),source_exe_sha256=sha(exe),native_verified_paths=len(result),native_verified_call_sites=sum(x['verified_calls'] for x in result))
 return 'ORIGINAL_EXE_SOURCE_CALLS_VERIFIED_NO_OUTER_EXECUTION',meta,result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args()
 c=json.loads(CANDIDATE.read_text());validate_candidate(c)
 a.work.mkdir(mode=0o700,parents=True,exist_ok=False)
 result={'schema':'stoneage.scene10.bounded_original_exe_source_gate.r1','status':'NOT_ATTEMPTED','carrier':'PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_TW10','range_limit_bytes':LIMIT,'claimed_exe_sha256':EXE_SHA,'unverified_candidate_calls':43,'native_exe_source_verified':False,'full_original_frame_authenticated':False,'original_world_entered':False,'raw_original_payload_published':False,'source_path_execution':False,'release_completed_percentage':None}
 try:
  status,meta,calls=try_source(a.work,c);result['status']=status;result['fetch_metadata']=meta
  if calls is not None:
   result['native_exe_source_verified']=True;result['verified_source_calls']=calls
 except Exception as e:
  result['status']='BOUNDED_SOURCE_UNAVAILABLE_OR_UNQUALIFIED';result['error']={'type':type(e).__name__,'message':str(e)[:240]}
 finally:
  import shutil
  shutil.rmtree(a.work,ignore_errors=True)
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print('R10_GATE_RESULT '+json.dumps({k:v for k,v in result.items() if k!='verified_source_calls'},sort_keys=True))
if __name__=='__main__':main()
