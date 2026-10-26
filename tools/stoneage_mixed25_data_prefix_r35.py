"""Retrieve three exact data files from a bounded existing mixed25 RAR prefix.

No new official build is claimed. Original data leaves the runner only as CMS
ciphertext; public output is source/member metadata. Never execute the archive.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile
from tools.stoneage_wayi85_sixpart_acquisition import direct_link

ROOT=Path(__file__).resolve().parents[1]
LIMIT=16*1024*1024
PART_BYTES=209715200
KEY='ev7l29fw77891go'
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5主程式/stoneage2.5/data/'
TARGETS={
 'AISetting.dat':(612,'0914e844e391f9ae51d255dee83b504198cdd9a3700085bd7fea715200ac4558'),
 'album_4.dat':(161424,'0b6427ec8a38a5d203ddd3b3c47fc3c0eba8daa68ff8c848a64bbf364812e59f'),
 'auto.dat':(250010,'2f8c858ed4ef2bdeb960d302682bffad4f534e595f2e9ad0e0ca8485f79746a3')}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)

def original_members(directory):
 out={}
 for name,(size,digest) in TARGETS.items():
  matches=[p for p in directory.rglob(name) if p.is_file() and p.as_posix().endswith(PREFIX+name)]
  need(len(matches)==1,'missing or ambiguous exact member '+name)
  raw=matches[0].read_bytes();need(len(raw)==size and sha(raw)==digest,'old full member identity mismatch '+name)
  out[name]=raw
 return out

def acquire(work):
 ua={'User-Agent':'Mozilla/5.0'};normal=f'https://www.mediafire.com/file/{KEY}/'
 with urllib.request.urlopen(urllib.request.Request(normal,headers=ua),timeout=60) as r:
  page=r.read(4*1024*1024+1);need(len(page)<=4*1024*1024,'public page bound');referer=r.geturl();page_status=r.status
 direct=direct_link(page.decode('utf-8','replace'))
 with urllib.request.urlopen(urllib.request.Request(direct,headers={**ua,'Referer':referer,'Range':f'bytes=0-{LIMIT-1}'}),timeout=120) as r:
  content_range=r.headers.get('Content-Range','');need(r.status==206 and content_range==f'bytes 0-{LIMIT-1}/{PART_BYTES}','exact bounded HTTP206 required')
  raw=r.read(LIMIT+1);need(len(raw)==LIMIT,'prefix extent mismatch')
 need(raw.startswith(b'Rar!\x1a\x07\x00'),'known RAR4 prefix signature')
 path=work/'prefix.rar';path.write_bytes(raw);dst=work/'members';dst.mkdir()
 cmd=['7z','x','-y','-r',f'-o{dst}',str(path),*[PREFIX+n for n in TARGETS]]
 proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 members=original_members(dst)
 return members,{'normal_download':referer,'public_page_status':page_status,'public_page_bytes':len(page),'public_page_sha256':sha(page),
   'range_status':206,'content_range':content_range,'prefix_bytes':len(raw),'prefix_sha256':sha(raw),
   'whole_part_or_whole_archive_rehashed':False,'sevenzip_return_code':proc.returncode,
   'truncated_archive_is_not_failure_if_all_selected_original_members_match_exact_full_sha':True}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--sealed',type=Path,required=True);args=ap.parse_args()
 args.work.mkdir(parents=True,exist_ok=False)
 result={'schema':'stoneage.mixed25_three_data_prefix.r35','status':'NOT_ACQUIRED','task':'ORIGINAL_CLIENT_ACQUISITION_AND_MATERIAL_ROTATION_35',
   'source_scope':'EXISTING_MIXED_COMMUNITY_PRESERVATION_NOT_OFFICIAL_CLEAN_BUILD',
   'quick_key':KEY,'original_client_executed':False,'new_official_clients':0,'raw_original_data_published':False,
   'named_species_or_auto_data_semantics_proven':False,'members':[]}
 try:
  members,fetch=acquire(args.work);result['fetch']=fetch
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
   for name,raw in members.items():
    z.writestr(name,raw)
    result['members'].append({'path':PREFIX+name,'name':name,'bytes':len(raw),'sha256':sha(raw),
     'nonzero_bytes':sum(v!=0 for v in raw),'first_four_le_u32':[int.from_bytes(raw[i:i+4],'little') for i in range(0,16,4)]})
  bundle=stream.getvalue();plain=args.work/'selected.zip';plain.write_bytes(bundle)
  cert=ROOT/'research/recovered/STONEAGE-R35-DATA-RECIPIENT-CERT.pem'
  subprocess.run(['openssl','cms','-encrypt','-binary','-aes-256-cbc','-in',str(plain),'-out',str(args.sealed),'-outform','DER',str(cert)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  result.update(status='THREE_ORIGINAL_MEMBER_FULL_HASHES_MATCH',private_transfer={'plaintext_zip_bytes':len(bundle),'plaintext_zip_sha256':sha(bundle),'ciphertext_bytes':args.sealed.stat().st_size,'ciphertext_sha256':sha(args.sealed.read_bytes()),'recipient_certificate_sha256':sha(cert.read_bytes())})
 except Exception as e:
  result['error']={'type':type(e).__name__,'message':str(e)[:400]}
 raw=(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode();args.output.write_bytes(raw)
 print('R35_METADATA_BEGIN');print(raw.decode(),end='');print('R35_METADATA_END')

if __name__=='__main__':main()
