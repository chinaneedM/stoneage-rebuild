"""One prehashed same-carrier ADRN index, three aliases, bounded source only."""
import argparse
from collections import Counter
import io
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib
from tools.stoneage_native_album_source_r36 import (
 ROOT, PREFIX, SparseParts, fetcher_factory, isolated_rar, sha, need,
)

NAME='adrn_15.bin'
MEMBER=PREFIX+'data/'+NAME
IDENTITY=(18765120,'92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74')
ALIASES=(28001,28002,28003)

def select_rows(raw):
 need(len(raw)>0 and len(raw)%80==0,'complete ADRN80 records')
 aliases={str(n):[] for n in ALIASES};same={str(n):[] for n in ALIASES};counts=Counter()
 for i in range(len(raw)//80):
  record=raw[i*80:(i+1)*80];bitmapno,adder,size,x,y,w,h=struct.unpack_from('<IIIiiii',record)
  logical=struct.unpack_from('<I',record,76)[0];counts[logical]+=1
  if logical not in ALIASES and bitmapno not in ALIASES:continue
  row={'index':i,'source_offset':i*80,'bitmapno':bitmapno,'adder':adder,'size':size,
   'xoff':x,'yoff':y,'width':w,'height':h,'logical_alias':logical,
   'record_sha256':sha(record),'attr_sha256':sha(record[28:80])}
  if logical in ALIASES:aliases[str(logical)].append(row)
  if bitmapno in ALIASES:same[str(bitmapno)].append(row)
 return {'record_bytes':80,'records_scanned':len(raw)//80,'selected_logical_aliases':aliases,
  'physical_same_number_counterexamples':same,'nonzero_duplicate_alias_occurrences':sum(n-1 for k,n in counts.items() if k!=0 and n>1),
  'all_occurrences_retained':True,'original_real_payload_read':False}

def acquire(work,context):
 import rarfile
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);selected={};visited=0
 class Found(Exception):pass
 def cb(info):
  nonlocal visited
  visited+=1;need(visited<=10000,'finite header traversal')
  if info.type!=rarfile.RAR_BLOCK_FILE or info.filename.replace('\\','/')!=MEMBER:return
  need(info.file_size==IDENTITY[0] and 0<info.compress_size<=8*1024*1024,'bounded exact original ADRN member')
  need(info.flags&(1|2|4|16)==0,'original ADRN depends on split/encrypted/solid context')
  selected.update(filename=MEMBER,header_offset=info.header_offset,data_offset=info.data_offset,
   compressed_bytes=info.compress_size,original_crc32=info.CRC,flags=info.flags,compression_method=info.compress_type)
  raise Found()
 try:rarfile.RarFile(reader,info_callback=cb,errors='strict')
 except Found:pass
 need(bool(selected),'original ADRN not found within finite budget')
 context.update(headers_visited=visited,selected_header=selected,range_receipts=reader.receipts,public_pages=pages)
 header=reader.at(selected['header_offset'],selected['data_offset']-selected['header_offset'])
 # Retain the existing2MiB per-read guard; selected payloads are read as finite
 # 1MiB pieces within the unchanged total source budget.
 packed=b''.join(reader.at(selected['data_offset']+i,min(1024*1024,selected['compressed_bytes']-i))
  for i in range(0,selected['compressed_bytes'],1024*1024))
 carrier=work/'selected.rar';carrier.write_bytes(isolated_rar(header,packed,selected['flags']))
 out=work/'out';out.mkdir();p=subprocess.run(['unar','-f','-o',str(out),str(carrier)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 context['extractor']={'name':'unar','return_code':p.returncode,'diagnostic':(p.stdout+p.stderr).decode('utf-8','replace')[-1200:] if p.returncode else ''}
 need(p.returncode==0,'bounded original ADRN independent extraction failed')
 files=[p for p in out.rglob('*') if p.is_file() and p.as_posix().endswith(MEMBER)]
 need(len(files)==1,'one exact original ADRN member path');raw=files[0].read_bytes()
 need((len(raw),sha(raw))==IDENTITY and zlib.crc32(raw)&0xffffffff==selected['original_crc32'],'complete old original ADRN SHA/CRC required')
 context.update(actual_range_bytes=reader.fetched,range_requests=len(reader.receipts),
   original_file_header_sha256=sha(header),compressed_payload_sha256=sha(packed))
 return raw

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--sealed',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
 d={'schema':'stoneage.album_adrn_source.r37','source_scope':'EXISTING_MIXED25_SAME_PRESERVED_CLIENT_SUBTREE_NOT_OFFICIAL_BUILD',
  'status':'NOT_ACQUIRED','new_official_clients':0,'original_program_executed':False,
  'whole_bundle_or_real_reacquired':False,'original_payload_published':False};context={}
 try:
  raw=acquire(a.work,context);d['source_member']={'path':MEMBER,'bytes':len(raw),'sha256':sha(raw)};d['selected_metadata']=select_rows(raw)
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:z.writestr(NAME,raw)
  plain=stream.getvalue();file=a.work/'selected.zip';file.write_bytes(plain);cert=ROOT/'research/recovered/STONEAGE-R35-DATA-RECIPIENT-CERT.pem'
  subprocess.run(['openssl','cms','-encrypt','-binary','-aes-256-cbc','-in',str(file),'-out',str(a.sealed),'-outform','DER',str(cert)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  d.update(status='ORIGINAL_ADRN_FULL_HASH_MATCH',private_transfer={'plaintext_zip_bytes':len(plain),'plaintext_zip_sha256':sha(plain),
   'ciphertext_bytes':a.sealed.stat().st_size,'ciphertext_sha256':sha(a.sealed.read_bytes()),'recipient_certificate_sha256':sha(cert.read_bytes())})
 except Exception as e:d['error']={'type':type(e).__name__,'message':str(e)[:400]}
 if context:
  context['actual_range_bytes']=sum(r['bytes'] for r in context['range_receipts']);context['range_requests']=len(context['range_receipts']);d['receipt']=context
 raw=(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode();a.output.write_bytes(raw)
 print('R37_SOURCE_METADATA_BEGIN');print(raw.decode(),end='');print('R37_SOURCE_METADATA_END')

if __name__=='__main__':main()
