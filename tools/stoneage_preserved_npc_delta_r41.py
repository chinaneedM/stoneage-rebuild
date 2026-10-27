"""Finite original NPC source bytes versus pinned modern embedded argument.

Reports fingerprints and bounded configuration facts. Dialogue/script bodies
are never printed or committed; optional private transfer is CMS ciphertext.
"""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request
import zipfile
import zlib
import rarfile
from tools.stoneage_native_album_source_r36 import SparseParts,fetcher_factory,isolated_rar,need
from tools.stoneage_npc_genkou_source_gate import analyze as qualify_modern,gitblob,SOURCE_SHA,ARG_SHA
ROOT=Path(__file__).resolve().parents[1]
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/npc/100/'
EXPECTED={
 'sb_kbu.arg':(258,'433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b'),
 'sb_geno.create':(573,'5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1'),
 'sb_geno.template':(321,'76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d')}
MODERN_URL='https://raw.githubusercontent.com/75912001/sa.desktop/e9b3f0cfd63b93c11fc77ca5331173dd6c5d2fc8/map/maps/11208/map.entity.yaml'
CODECS=('cp950','big5','gb18030','gbk','utf-8')
SCOPE='COMMUNITY_MIXED25_PRESERVED_NPC_SCRIPTS_VS_2026_MODERN_RECONSTRUCTION_NOT_OFFICIAL_SAME_BUILD'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def decode_fields(text):
 rows=[]
 for ordinal,line in enumerate(text.splitlines(),1):
  if not line or ':' not in line:return None
  key,value=line.split(':',1)
  if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9 ]*',key):return None
  kind='TEXT_FINGERPRINT';item={'line':ordinal,'key':key,'value_chars':len(value),'value_utf8_sha256':sha(value.encode())}
  if re.fullmatch(r'-?\d+(,-?\d+)*',value):
   kind='INTEGER_LIST' if ',' in value else 'INTEGER';item['numbers']=[int(v) for v in value.split(',')]
  elif value=='':kind='EMPTY'
  item['value_kind']=kind;rows.append(item)
 return rows

def arg_delta(old,modern):
 target=modern.decode('gb18030','strict');profiles=[]
 for codec in CODECS:
  profile={'codec':codec,'strict_decode':False}
  try:text=old.decode(codec,'strict')
  except UnicodeDecodeError:
   profiles.append(profile);continue
  profile.update(strict_decode=True,unicode_text_sha256=sha(text.encode()),unicode_chars=len(text),
   exact_unicode_equal_to_modern_gb18030=text==target,
   newline_normalized_text_equal=text.replace('\r\n','\n')==target.replace('\r\n','\n'),fields=decode_fields(text))
  try:profile['exact_transcode_to_modern_gb18030']=text.encode('gb18030','strict')==modern
  except UnicodeEncodeError:profile['exact_transcode_to_modern_gb18030']=False
  profiles.append(profile)
 return {'old_bytes':len(old),'old_sha256':sha(old),'modern_bytes':len(modern),'modern_sha256':sha(modern),
  'raw_bytes_equal':old==modern,'equal_byte_lengths':len(old)==len(modern),
  'different_byte_offsets':[i for i,(a,b) in enumerate(zip(old,modern)) if a!=b],
  'old_crlf_count':old.count(b'\r\n'),'old_lf_count':old.count(b'\n'),
  'modern_crlf_count':modern.count(b'\r\n'),'modern_lf_count':modern.count(b'\n'),
  'modern_unicode_sha256':sha(target.encode()),'modern_fields':decode_fields(target),'decode_candidates':profiles,
  'exact_transcode_candidates':[p['codec'] for p in profiles if p.get('exact_transcode_to_modern_gb18030')],
  'dialogue_text_published':False}

def configuration_profile(raw,codec):
 text=raw.decode(codec,'strict');out=[]
 for number,line in enumerate(text.splitlines(),1):
  value=line.strip();r={'line':number,'line_utf8_sha256':sha(line.encode())}
  if not value:r['kind']='BLANK'
  elif value.startswith('#'):r['kind']='COMMENT'
  elif value in ('{','}'):r.update(kind='BLOCK_MARKER',marker=value)
  else:
   match=re.fullmatch(r'([A-Za-z_][A-Za-z0-9_ ]*)\s*[:=]\s*(.*)',value)
   if match:
    key,val=match.groups();key=key.strip();r.update(kind='ASSIGNMENT',key=key,value_utf8_sha256=sha(val.encode()),value_chars=len(val))
    if re.fullmatch(r'-?\d+(\s*,\s*-?\d+)*',val):r['numbers']=[int(v) for v in val.split(',')]
    elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_./|:-]{0,99}',val):r['ascii_token']=val
   else:r['kind']='UNCLASSIFIED_FINGERPRINT'
  out.append(r)
 return {'codec':codec,'decoded_text_sha256':sha(text.encode()),'line_count':len(out),'line_profiles':out,
  'raw_crlf_count':raw.count(b'\r\n'),'raw_lf_count':raw.count(b'\n'),'raw_script_body_published':False}

def modern_argument(raw):
 qualified=qualify_modern(raw)
 npcs=[json.loads(line[4:]) for line in raw.decode().splitlines()[3:raw.decode().splitlines().index('warps:')]]
 payloads=[base64.b64decode(n['functionOptions'][0]['config']['legacy']['arguments'][0]['contentBase64'],validate=True) for n in npcs]
 need(len(set(payloads))==1 and sha(payloads[0])==ARG_SHA,'two modern occurrences same exact argument')
 return payloads[0],qualified

def acquire(work,receipt):
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);selected={};headers=0
 def visit(info):
  nonlocal headers
  headers+=1;need(headers<=10000,'finite original header traversal')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+n for n in EXPECTED}:return
  leaf=name.rsplit('/',1)[1];need(leaf not in selected,'unique original NPC member')
  need(info.file_size==EXPECTED[leaf][0] and info.compress_size<=65536,'finite original NPC member size')
  need(info.flags&(1|2|4|16)==0,'independent original NPC member')
  selected[leaf]={'name':name,'bytes':info.file_size,'compressed_bytes':info.compress_size,'flags':info.flags,
   'header_offset':info.header_offset,'data_offset':info.data_offset,'crc32':info.CRC,'compression_method':info.compress_type}
 try:
  rarfile.RarFile(reader,info_callback=visit,errors='strict');need(set(selected)==set(EXPECTED),'three exact original NPC members')
  result={};receipt['members']=[]
  for i,(leaf,entry) in enumerate(selected.items()):
   header=reader.at(entry['header_offset'],entry['data_offset']-entry['header_offset']);packed=reader.at(entry['data_offset'],entry['compressed_bytes'])
   archive=work/f'member-{i}.rar';archive.write_bytes(isolated_rar(header,packed,entry['flags']));dst=work/f'out-{i}'
   proc=subprocess.run(['unar','-f','-o',str(dst),str(archive)],capture_output=True,timeout=90);need(proc.returncode==0,'bounded static unar extraction')
   matches=[p for p in dst.rglob('*') if p.is_file() and p.as_posix().endswith(entry['name'])];need(len(matches)==1,'one exact original NPC extracted path')
   raw=matches[0].read_bytes();need((len(raw),sha(raw))==EXPECTED[leaf],'original NPC full SHA and length')
   need(zlib.crc32(raw)&0xffffffff==entry['crc32'],'original NPC full CRC')
   result[leaf]=raw;receipt['members'].append({**entry,'sha256':sha(raw),'header_sha256':sha(header),'compressed_payload_sha256':sha(packed),'extractor_returncode':proc.returncode})
  return result
 finally:receipt.update(headers_visited=headers,range_requests=len(reader.receipts),actual_range_bytes=reader.fetched,range_receipts=reader.receipts,public_pages=pages,whole_package_rehashed=False)

def seal(members,work,output):
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
  for leaf,raw in sorted(members.items()):z.writestr(leaf,raw)
 raw=buf.getvalue();plain=work/'private.zip';plain.write_bytes(raw);cert=ROOT/'research/recovered/STONEAGE-R35-DATA-RECIPIENT-CERT.pem'
 subprocess.run(['openssl','cms','-encrypt','-binary','-aes-256-cbc','-in',str(plain),'-out',str(output),'-outform','DER',str(cert)],check=True,capture_output=True)
 return {'plaintext_zip_bytes':len(raw),'plaintext_zip_sha256':sha(raw),'ciphertext_bytes':output.stat().st_size,
  'ciphertext_sha256':sha(output.read_bytes()),'recipient_certificate_sha256':sha(cert.read_bytes()),'private_payload_in_public_git':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--sealed',type=Path,required=True);a=p.parse_args()
 report={'schema':'stoneage.preserved_npc_delta_source.r41','source_scope':SCOPE,'status':'NOT_ACQUIRED',
  'original_server_executed':False,'official_same_build_authenticated':False,'verified_base_quests_added':0,
  'origin_class':'ORIGIN_UNRESOLVED','raw_script_bodies_published':False,'receipt':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='r41-private-') as temp:
   members=acquire(Path(temp),report['receipt'])
   with urllib.request.urlopen(MODERN_URL,timeout=60) as response:
    modern_raw=response.read(1024*1024+1);need(len(modern_raw)<=1024*1024,'finite pinned modern source')
   modern,qualified=modern_argument(modern_raw)
   report['modern_source']={'url':MODERN_URL,'bytes':len(modern_raw),'sha256':sha(modern_raw),'git_blob':gitblob(modern_raw),'prior_qualified_report':qualified}
   report['argument_delta']=arg_delta(members['sb_kbu.arg'],modern)
   report['configuration_profiles']={leaf:[configuration_profile(members[leaf],codec) for codec in ('cp950','big5')] for leaf in ('sb_geno.create','sb_geno.template')}
   report['private_transfer']=seal(members,Path(temp),a.sealed)
   report['status']='THREE_ORIGINAL_NPC_SHA_CRC_MATCH_MODERN_DELTA_DERIVED'
 except Exception as e:report['error']={'type':type(e).__name__,'message':str(e)[:400]}
 a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print('R41_METADATA_BEGIN');print(a.output.read_text(),end='');print('R41_METADATA_END')
if __name__=='__main__':main()
