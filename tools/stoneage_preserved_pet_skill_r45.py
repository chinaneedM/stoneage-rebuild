"""Bounded original pet-skill names/fields; never a launch-era or runtime claim."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import zlib
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar, need

ROOT=Path(__file__).resolve().parents[1]
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/'
EXPECTED={
 'setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'),
 'data/petskill.txt':(15112,'f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4')}
SCOPE='PRESERVED_COMMUNITY_MIXED25_SKILL_TABLE_NOT_OFFICIAL_TW10_OR_SAME_DEPLOYMENT'
INT_NAMES=('ID','FIELD','TARGET','COST','ILLEGAL')
SELECTION='FIRST_SIX_ORIGINAL_TABLE_OCCURRENCES_INCLUDING_ID_ZERO'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def fingerprint(raw):return {'bytes':len(raw),'sha256':sha(raw)}

def skill_config(raw):
 config={}
 for line in raw.splitlines():
  line=line.split(b'#',1)[0].strip()
  if b'=' not in line:continue
  key,value=line.split(b'=',1);key=key.strip().decode('ascii','strict').lower()
  if key not in ('petskillfile1','petskillfile2'):continue
  need(key not in config,'duplicate pet-skill configuration key')
  value=value.strip().decode('ascii','strict')
  need(value and not value.startswith('/') and '\\' not in value and '..' not in value.split('/'),'unsafe original skill path')
  config[key]=value
 need(set(config)=={'petskillfile1','petskillfile2'},'both compile-time skill configuration alternatives required')
 need({str(PurePosixPath(v)) for v in config.values()}=={'data/petskill.txt'},'different or unqualified configured skill tables')
 return config

def parse_table(raw):
 rows=[];ids=set();offset=0
 for line_no,line in enumerate(raw.splitlines(keepends=True),1):
  body=line.rstrip(b'\r\n');value=body.strip()
  if value and not value.startswith(b'#'):
   fields=[v.strip() for v in value.split(b',')]
   need(len(fields)==12,'exact twelve-column six-string/five-int/trailing field extent')
   numbers={k:int(fields[6+i]) for i,k in enumerate(INT_NAMES)}
   need(0<=numbers['ID']<=1000000 and numbers['ID'] not in ids,'duplicate or invalid original skill ID')
   ids.add(numbers['ID']);callback=fields[2].decode('ascii','strict')
   need(re.fullmatch(r'PETSKILL_[A-Za-z_0-9]+',callback) is not None,'unqualified skill callback token')
   rows.append({'line':line_no,'offset':offset,'body':body,'fields':fields,'numbers':numbers,'callback':callback})
  offset+=len(line)
 return rows

def derive(members):
 for key,pin in EXPECTED.items():need((len(members[key]),sha(members[key]))==pin,'original skill member changed')
 config=skill_config(members['setup.cf']);rows=parse_table(members['data/petskill.txt'])
 need(len(rows)==147,'preexisting147-row original table extent')
 selected=[]
 for order,row in enumerate(rows[:6]):
  fields=row['fields'];a=fields[0].decode('cp950','strict');b=fields[0].decode('big5','strict')
  need(a==b and 0<len(a)<=48,'selected name ambiguity/extent')
  selected.append({'source_order':order,'physical_line':row['line'],'byte_offset':row['offset'],
   'row_sha256':sha(row['body']),'name':{'text_cp950_big5':a,'token':fingerprint(fields[0])},
   'callback':row['callback'],'numeric_fields':row['numbers'],
   'non_name_text_fingerprints':{key:fingerprint(fields[col]) for key,col in
    [('comment',1),('option',3),('free',4),('kindcode',5),('trailing_preserved_column',11)]}})
 return {'configured_skill_paths_as_written':config,'normalized_configured_skill_path':'data/petskill.txt',
  'all_original_rows':len(rows),'all_unique_skill_ids':len({r['numbers']['ID'] for r in rows}),
  'field_count_distribution':{'12':len(rows)},'raw_name_token_count':len({r['fields'][0] for r in rows}),
  'callback_token_count':len({r['callback'] for r in rows}),
  'trailing_field_equals_callback_rows':sum(r['fields'][11]==r['fields'][2] for r in rows),
  'integer_column_counts':{k:dict(sorted(Counter(str(r['numbers'][k]) for r in rows).items())) for k in ('FIELD','TARGET','COST','ILLEGAL')},
  'selected_rule':SELECTION,'selected_rows':selected,
  'column_semantics':'DESCENDANT_CFREE6_PREFIX_NOT_THIS_BINARY_LOADER_PROOF',
  'cost_is_mp_or_training_price_proven':False,'original_callback_execution_proven':False,
  'original_learning_npc_or_species_eligibility_proven':False}

def acquire(work,receipt):
 import rarfile
 import libarchive
 from libarchive import ffi
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);chosen={};headers=0
 def visit(info):
  nonlocal headers
  headers+=1;need(headers<=10000,'finite archive header traversal')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+k for k in EXPECTED}:return
  key=name[len(PREFIX):];need(key not in chosen,'duplicate original source path')
  need(info.file_size==EXPECTED[key][0] and info.compress_size<=65536,'bounded independent original member')
  need(info.flags&(1|2|4|16)==0,'split/encrypted/solid original source is unqualified')
  chosen[key]={'path':name,'bytes':info.file_size,'compressed_bytes':info.compress_size,'flags':info.flags,
   'crc32':info.CRC,'header_offset':info.header_offset,'data_offset':info.data_offset,'compression_method':info.compress_type}
 try:
  rarfile.RarFile(reader,info_callback=visit,errors='strict')
  need(set(chosen)==set(EXPECTED),'both original source files required')
  result={};receipt['members']=[]
  for n,(key,entry) in enumerate(chosen.items()):
   header=reader.at(entry['header_offset'],entry['data_offset']-entry['header_offset'])
   packed=reader.at(entry['data_offset'],entry['compressed_bytes']);wrapped=isolated_rar(header,packed,entry['flags'])
   path=work/f'{n}.rar';path.write_bytes(wrapped);out=work/f'out-{n}'
   proc=subprocess.run(['unar','-f','-o',str(out),str(path)],capture_output=True,timeout=90)
   need(proc.returncode==0,'unar static source extraction failed')
   candidates=[p for p in out.rglob('*') if p.is_file() and p.as_posix().endswith(entry['path'])]
   need(len(candidates)==1,'exact extracted original path');raw=candidates[0].read_bytes()
   need((len(raw),sha(raw))==EXPECTED[key] and zlib.crc32(raw)&0xffffffff==entry['crc32'],'complete original SHA/CRC')
   with libarchive.memory_reader(wrapped) as archive:
    independent=[(e.pathname,b''.join(e.get_blocks())) for e in archive]
   need(len(independent)==1 and independent[0][0].replace('\\','/')==entry['path'] and independent[0][1]==raw,'independent libarchive decode disagrees')
   result[key]=raw;receipt['members'].append({**entry,'sha256':sha(raw),
    'header_sha256':sha(header),'compressed_payload_sha256':sha(packed),'unar_return_code':0,
    'libarchive_version_number':ffi.version_number(),'independent_decoded_bytes_equal':True})
  return result
 finally:
  receipt.update(headers_visited=headers,actual_range_bytes=reader.fetched,range_requests=len(reader.receipts),
   range_receipts=reader.receipts,public_pages=pages,whole_archive_or_parts_rehashed=False,
   same_http_bytes_two_decompressors_not_two_network_acquisitions=True)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 d={'schema':'stoneage.preserved_pet_skill_source.r45','source_scope':SCOPE,'status':'NOT_ACQUIRED',
  'official_tw10_skills_authenticated':0,'original_server_executed':False,
  'raw_table_comment_option_or_script_published':False,'receipt':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='r45-private-') as temp:
   members=acquire(Path(temp),d['receipt']);d['status']='ORIGINAL_MEMBERS_ACQUIRED_DERIVATION_PENDING'
   d['material']=derive(members);d['status']='TWO_ORIGINAL_MEMBERS_DUAL_DECODE_SHA_CRC_AND_SIX_NAMES_QUALIFIED'
 except Exception as exc:d['error']={'type':type(exc).__name__,'message':str(exc)[:300]}
 args.output.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print('R45_METADATA_BEGIN');print(args.output.read_text(),end='');print('R45_METADATA_END')
if __name__=='__main__':main()
