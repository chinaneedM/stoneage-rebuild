"""Bounded same-carrier server template facts; no official/same-build promotion."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zlib
import rarfile
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar, need

ROOT=Path(__file__).resolve().parents[1]
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/'
EXPECTED={
 'setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'),
 'data/enemybase.txt':(147750,'1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7')}
NAMES=('烏力','烏力烏力','烏力斯坦')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def lines(raw):
 offset=0
 for number,line in enumerate(raw.splitlines(keepends=True),1):
  value=line.strip()
  if value and not value.startswith(b'#'):yield number,offset,value
  offset+=len(line)

def derive(raw,setup):
 config=[]
 for _,_,line in lines(setup):
  line=line.split(b'#',1)[0].strip()
  if b'=' in line:
   k,v=line.split(b'=',1)
   if k.strip().lower()==b'enemybasefile':config.append(v.strip().decode('ascii','strict'))
 need(config==['./data/enemybase.txt'],'unique original configured template path')
 rows=[];counts={};selected=[];encoding_difference=[]
 for number,offset,line in lines(raw):
  fields=line.split(b',');counts[str(len(fields))]=counts.get(str(len(fields)),0)+1
  need(len(fields)==56,'original 56-column template extent')
  name=fields[0].strip();a=name.decode('cp950','strict');b=name.decode('big5','strict')
  if a!=b:encoding_difference.append({'line':number,'name_token_sha256':sha(name)})
  identity=[int(fields[i].strip()) for i in (6,36,37)]
  rows.append((a,identity))
  if a in NAMES:
   need(a==b,'selected name encoding ambiguity')
   selected.append({'line':number,'byte_offset':offset,'row_sha256':sha(line),
    'name':a,'name_token_sha256':sha(name),'template_number_column_7':identity[0],
    'graphic_field_column_37':identity[1],'pet_flag_column_38':identity[2]})
 need(len(rows)==988,'preexisting exact source row count')
 need(len(selected)<=48,'finite three-name projection')
 return {'configured_enemybase_path':config[0],'all_template_rows':len(rows),
  'field_count_distribution':counts,'distinct_template_numbers':len({r[1][0] for r in rows}),
  'distinct_name_tokens':len({r[0] for r in rows}),'cp950_big5_different_names':encoding_difference,
  'selected_name_queries':list(NAMES),'selected_rows':selected,
  'unmatched_name_queries':[n for n in NAMES if not any(r['name']==n for r in selected)],
  'numeric_semantics':'COLUMN_7_TEMPNO_COLUMN_37_IMGNUMBER_COLUMN_38_PETFLG_FROM_PREEXISTING_DESCENDANT_PREFIX_NOT_NATIVE_BUILD_PROOF',
  'original_server_executed':False,'same_client_server_build_proven':False,
  'client_sprite_binding_proven':False,'official_species_master_authenticated':False}

def acquire(work,receipt):
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);chosen={};count=0
 def visit(info):
  nonlocal count
  count+=1;need(count<=10000,'finite header traversal')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+p for p in EXPECTED}:return
  key=name[len(PREFIX):];need(key not in chosen,'duplicate selected original member')
  need(info.file_size==EXPECTED[key][0] and info.compress_size<=1024*1024,'original member bounded size')
  need(info.flags&(1|2|4|16)==0,'independent original member required')
  chosen[key]={'name':name,'header_offset':info.header_offset,'data_offset':info.data_offset,
   'compressed_bytes':info.compress_size,'bytes':info.file_size,'flags':info.flags,'crc32':info.CRC,
   'compression_method':info.compress_type}
 try:
  rarfile.RarFile(reader,info_callback=visit,errors='strict')
  need(set(chosen)==set(EXPECTED),'both original configured source files present')
  result={};receipt['members']=[]
  for i,(key,entry) in enumerate(chosen.items()):
   header=reader.at(entry['header_offset'],entry['data_offset']-entry['header_offset'])
   packed=reader.at(entry['data_offset'],entry['compressed_bytes'])
   archive=work/f'member-{i}.rar';archive.write_bytes(isolated_rar(header,packed,entry['flags']))
   dst=work/f'out-{i}'
   proc=subprocess.run(['unar','-f','-o',str(dst),str(archive)],capture_output=True,timeout=90)
   need(proc.returncode==0,'bounded unar static extraction failed')
   matches=[p for p in dst.rglob('*') if p.is_file() and p.as_posix().endswith(entry['name'])]
   need(len(matches)==1,'exact selected original path')
   raw=matches[0].read_bytes()
   need((len(raw),sha(raw))==EXPECTED[key],'whole original member SHA and size')
   need(zlib.crc32(raw)&0xffffffff==entry['crc32'],'whole original member CRC')
   result[key]=raw
   receipt['members'].append({**entry,'sha256':sha(raw),'header_sha256':sha(header),
    'compressed_payload_sha256':sha(packed),'extractor':'unar','extractor_returncode':0})
  return result
 finally:
  receipt.update(headers_visited=count,range_requests=len(reader.receipts),actual_range_bytes=reader.fetched,
   range_receipts=reader.receipts,public_pages=pages,whole_package_rehashed=False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 report={'schema':'stoneage.preserved_pet_template_source.r39','status':'NOT_ACQUIRED',
  'source_scope':'COMMUNITY_MIXED25_SAME_ARCHIVE_SERVER_SUBTREE_NOT_AUTHENTICATED_OFFICIAL_OR_SAME_DEPLOYED_BUILD',
  'original_payload_published':False,'new_official_clients':0,'original_program_executed':False,
  'receipt':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='r39-private-') as tmp:
   raw=acquire(Path(tmp),report['receipt'])
   report['material']=derive(raw['data/enemybase.txt'],raw['setup.cf'])
   report['status']='ORIGINAL_CONFIG_AND_TEMPLATE_SHA_CRC_MATCH'
 except Exception as e:report['error']={'type':type(e).__name__,'message':str(e)[:400]}
 a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print('R39_METADATA_BEGIN');print(a.output.read_text(),end='');print('R39_METADATA_END')
if __name__=='__main__':main()
