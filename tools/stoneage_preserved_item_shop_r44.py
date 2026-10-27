"""Three bounded original members; six named item projections, never raw prose.

The preserved community server is not authenticated as an official release or
same-deployment client/server. Inventory expansion is a descendant-code model,
not evidence that an original server displayed or sold these items.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zlib
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar, need
from tools.stoneage_itemset_schema_probe import INDEX, SCHEMA

ROOT=Path(__file__).resolve().parents[1]
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/'
EXPECTED={
 'setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'),
 'data/itemset.txt':(3392473,'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688'),
 'data/npc/my/shop/ACCESSORY1.arg':(882,'d2b7a25ca2d5b200a5d2fdf10230c0f3fb9aff294b3db23eeb4ae5fe199c4548')}
SCOPE='COMMUNITY_MIXED25_ORIGINAL_SERVER_MEMBERS_NOT_OFFICIAL_TW10_OR_SAME_DEPLOYMENT'
NUMBER_FIELDS=('id','imagenumber','cost','type','level','attack_raw_a','attack_raw_b',
 'defence_raw_a','defence_raw_b','quick_raw_a','quick_raw_b','charm_raw_a','charm_raw_b')

def sha(raw):return hashlib.sha256(raw).hexdigest()

def acquire(work,receipt,extractor='unar'):
 import rarfile
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);selected={};count=0
 def visit(info):
  nonlocal count
  count+=1;need(count<=10000,'bounded header traversal')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+p for p in EXPECTED}:return
  key=name[len(PREFIX):];need(key not in selected,'duplicate selected original path')
  need(info.file_size==EXPECTED[key][0] and info.compress_size<=1024*1024,'bounded original member extent')
  need(info.flags&(1|2|4|16)==0,'independent non-solid original member required')
  selected[key]={'path':name,'bytes':info.file_size,'compressed_bytes':info.compress_size,
   'flags':info.flags,'crc32':info.CRC,'header_offset':info.header_offset,
   'data_offset':info.data_offset,'compression_method':info.compress_type}
 try:
  rarfile.RarFile(reader,info_callback=visit,errors='strict')
  need(set(selected)==set(EXPECTED),'all three original members required')
  result={};receipt['members']=[]
  for n,(key,entry) in enumerate(selected.items()):
   header=reader.at(entry['header_offset'],entry['data_offset']-entry['header_offset'])
   packed=reader.at(entry['data_offset'],entry['compressed_bytes'])
   wrapped=isolated_rar(header,packed,entry['flags'])
   if extractor=='libarchive':
    import libarchive
    from libarchive import ffi
    with libarchive.memory_reader(wrapped) as archive:
     entries=[(e.pathname,b''.join(e.get_blocks())) for e in archive]
    need(len(entries)==1 and entries[0][0].replace('\\','/')==entry['path'],'single exact libarchive member')
    raw=entries[0][1];version=str(ffi.version_number())
   else:
    need(extractor=='unar','unsupported extraction backend')
    path=work/f'{n}.rar';path.write_bytes(wrapped);out=work/f'out-{n}'
    proc=subprocess.run(['unar','-f','-o',str(out),str(path)],capture_output=True,timeout=90)
    need(proc.returncode==0,'independent unar extraction failed')
    matches=[p for p in out.rglob('*') if p.is_file() and p.as_posix().endswith(entry['path'])]
    need(len(matches)==1,'single exact unar original path');raw=matches[0].read_bytes();version='system unar return_code0'
   need((len(raw),sha(raw))==EXPECTED[key],'complete original member size/SHA')
   need(zlib.crc32(raw)&0xffffffff==entry['crc32'],'complete original member CRC')
   result[key]=raw;receipt['members'].append({**entry,'sha256':sha(raw),
    'header_sha256':sha(header),'compressed_payload_sha256':sha(packed),
    'extractor':extractor,'extractor_version':version})
  return result
 finally:
  receipt.update(headers_visited=count,range_requests=len(reader.receipts),actual_range_bytes=reader.fetched,
   range_receipts=reader.receipts,public_pages=pages,whole_archive_or_parts_rehashed=False)

def arg_fields(raw):
 fields={}
 for line in raw.splitlines():
  line=line.strip()
  if not line or line.startswith(b'#'):continue
  need(b':' in line,'unsupported original ARG line grammar')
  key,value=line.split(b':',1);key=key.strip().decode('ascii','strict').lower()
  need(re.fullmatch('[a-z_][a-z_0-9 ]*',key) and key not in fields,'ARG duplicate/invalid key')
  fields[key]=value.strip()
 return fields

def inventory_tokens(value):
 tokens=[]
 for raw in value.split(b','):
  token=raw.strip();need(re.fullmatch(rb'\d+(?:\s*-\s*\d+)?',token) is not None,'noncanonical inventory token')
  ends=[int(x.strip()) for x in token.split(b'-')];lo=ends[0];hi=ends[-1]
  need(0<=lo<=hi<=1000000,'reversed or excessive inventory range is unqualified')
  tokens.append([lo,hi])
 need(0<len(tokens)<=100,'finite inventory token count')
 return tokens

def expand_inventory(tokens,ids,limit=33):
 all_occurrences=[]
 for token_index,(lo,hi) in enumerate(tokens):
  for item_id in sorted(i for i in ids if lo<=i<=hi):
   all_occurrences.append({'token_index':token_index,'item_id':item_id})
 need(len(all_occurrences)<=1000,'inventory occurrence budget')
 return {'listed_defined_occurrences':all_occurrences,
  'descendant_model_visible_occurrences':all_occurrences[:limit],
  'descendant_model_truncated_occurrences':all_occurrences[limit:],
  'limit':limit,'undefined_ids_are_skipped':True,'model_is_original_runtime':False}

def parse_items(raw):
 rows={};offset=0;count=0
 for line_no,line in enumerate(raw.splitlines(keepends=True),1):
  body=line.rstrip(b'\r\n');value=body.strip()
  if value and not value.startswith(b'#'):
   fields=[v.strip() for v in value.replace(b'\t',b' ').split(b',')]
   need(len(fields)==len(SCHEMA)==94,'94-column original item extent')
   item_id=int(fields[INDEX['id']]);need(item_id not in rows,'duplicate original template ID')
   rows[item_id]=(line_no,offset,body,fields);count+=1
  offset+=len(line)
 return rows,count

def derive(members):
 for key,expected in EXPECTED.items():need((len(members[key]),sha(members[key]))==expected,'original member changed before derivation')
 config={}
 for line in members['setup.cf'].splitlines():
  line=line.split(b'#',1)[0].strip()
  if b'=' not in line:continue
  key,val=line.split(b'=',1);key=key.strip().decode('ascii','strict').lower()
  if key in ('itemset3file','itemset4file','itemset5file','itemset6file'):
   need(key not in config,'duplicate configured table key');config[key]=val.strip().decode('ascii','strict')
 need(set(config)=={'itemset3file','itemset4file','itemset5file','itemset6file'} and
      set(config.values())=={'data/itemset.txt'},'actual configured itemset path')
 fields=arg_fields(members['data/npc/my/shop/ACCESSORY1.arg'])
 need('itemlist' in fields,'actual shop inventory list absent')
 tokens=inventory_tokens(fields['itemlist']);rows,count=parse_items(members['data/itemset.txt'])
 need(count==13252,'complete original table row count')
 inventory=expand_inventory(tokens,set(rows));selected=[]
 # Exactly the first six defined visible occurrences, selected before name decoding.
 for rank,occurrence in enumerate(inventory['descendant_model_visible_occurrences'][:6],1):
  item_id=occurrence['item_id'];line_no,offset,body,columns=rows[item_id]
  names={}
  for label in ('name','secretname'):
   token=columns[INDEX[label]];a=token.decode('cp950','strict');b=token.decode('big5','strict')
   need(a==b,'selected item name encoding ambiguity')
   names[label]={'text_cp950_big5':a,'bytes_sha256':sha(token)}
  values={}
  for name in NUMBER_FIELDS:
   cell=columns[INDEX[name]];values[name]=int(cell) if cell else None
  selected.append({'model_visible_rank':rank,'token_index':occurrence['token_index'],'item_id':item_id,
    'physical_line':line_no,'byte_offset':offset,'row_sha256':sha(body),'names':names,'numeric_fields':values})
 rates={}
 for key in ('buy_rate','sell_rate'):
  cell=fields.get(key)
  if cell is None:rates[key]={'present':False,'raw_decimal':None}
  else:
   text=cell.decode('ascii','strict');need(re.fullmatch(r'-?\d+(?:\.\d+)?',text) is not None,'unqualified rate grammar')
   rates[key]={'present':True,'raw_decimal':text}
 return {'configured_itemset_keys':config,'arg_keys_in_source_order':list(fields),
  'arg_value_fingerprints':{k:{'bytes':len(v),'sha256':sha(v)} for k,v in fields.items()},
  'inventory_tokens':tokens,'inventory':inventory,'rate_fields':rates,
  'original_item_rows':count,'original_unique_template_ids':len(rows),
  'selected_rule':'FIRST_SIX_DEFINED_VISIBLE_OCCURRENCES_BEFORE_NAME_DECODING',
  'selected_items':selected,'numeric_field_semantics':'EXISTING_DESCENDANT94_COLUMN_SCHEMA_NOT_ORIGINAL_BINARY_LOADER_PROOF',
  'computed_runtime_prices':None,'source_arg_is_authenticated_original_shop_execution':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
 p.add_argument('--extractor',choices=('unar','libarchive'),default='unar');args=p.parse_args()
 report={'schema':'stoneage.preserved_item_shop_source.r44','source_scope':SCOPE,'status':'NOT_ACQUIRED',
  'official_tw10_items_authenticated':0,'original_server_executed':False,
  'original_payload_or_dialogue_published':False,'receipt':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='r44-private-') as temp:
   members=acquire(Path(temp),report['receipt'],args.extractor)
   report['status']='THREE_ORIGINAL_MEMBERS_ACQUIRED_DERIVATION_PENDING'
   report['material']=derive(members)
   report['status']='THREE_ORIGINAL_MEMBERS_SHA_CRC_AND_FINITE_NAMED_INVENTORY_QUALIFIED'
 except Exception as exc:report['error']={'type':type(exc).__name__,'message':str(exc)[:300]}
 args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print('R44_METADATA_BEGIN');print(args.output.read_text(),end='');print('R44_METADATA_END')
if __name__=='__main__':main()
