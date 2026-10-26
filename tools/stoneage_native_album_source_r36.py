"""Two prehashed client programs via bounded sparse RAR4 reads, no execution.

Compressed streams are independently extracted only if the original file is
neither encrypted, split nor solid. Original programs leave the runner only as
CMS ciphertext. The preserved community bundle is not an official clean build.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import urllib.request
import zipfile
import zlib
from tools.stoneage_wayi85_sixpart_acquisition import direct_link

ROOT=Path(__file__).resolve().parents[1]
PARTS=[('ev7l29fw77891go',209715200),('ytaa168o5jih0lx',151539980)]
MAX_FETCH=16*1024*1024
MAX_REQUESTS=256
PREFIX='石器2.5客戶端+服務端+登入器/SA2.5主程式/stoneage2.5/'
TARGETS={'sa_2903.exe':(561152,'ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16'),
 'sa_2903网通.exe':(561152,'79554dd8526cf30afc50575d178461338afd3c299bd959987390496f106cde50')}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)

class SparseParts:
 def __init__(self,fetcher,sizes=None,chunk=65536,max_bytes=MAX_FETCH,max_requests=MAX_REQUESTS):
  self.fetcher=fetcher;self.sizes=sizes or [v for k,v in PARTS];self.length=sum(self.sizes)
  self.chunk=chunk;self.max_bytes=max_bytes;self.max_requests=max_requests
  self.position=0;self.cache={};self.receipts=[];self.fetched=0
 def tell(self):return self.position
 def seek(self,offset,whence=0):
  pos=offset if whence==0 else self.position+offset if whence==1 else self.length+offset if whence==2 else -1
  need(0<=pos<=self.length,'virtual archive seek bound');self.position=pos;return pos
 def read(self,n=-1):
  need(0<=n<=2*1024*1024,'finite sparse read required');n=min(n,self.length-self.position);out=[]
  while n:
   offset=self.position;part=0
   while offset>=self.sizes[part]:offset-=self.sizes[part];part+=1
   start=offset//self.chunk*self.chunk;size=min(self.chunk,self.sizes[part]-start);key=(part,start)
   if key not in self.cache:
    need(len(self.receipts)<self.max_requests and self.fetched+size<=self.max_bytes,'sparse source budget exhausted')
    data=self.fetcher(part,start,start+size-1);need(len(data)==size,'exact sparse range extent required')
    self.cache[key]=data;self.fetched+=size
    self.receipts.append({'part':part+1,'start':start,'end':start+size-1,'bytes':size,'sha256':sha(data)})
   data=self.cache[key];take=min(n,len(data)-(offset-start));out.append(data[offset-start:offset-start+take]);self.position+=take;n-=take
  return b''.join(out)
 def at(self,offset,size):self.seek(offset);return self.read(size)
 def close(self):pass

def original_main_and_end():
 def block(kind,size,payload):
  body=struct.pack('<BHH',kind,0,size)+payload
  return struct.pack('<H',zlib.crc32(body)&65535)+body
 return b'Rar!\x1a\x07\x00'+block(0x73,13,b'\0'*6),block(0x7b,7,b'')

def isolated_rar(header,packed,flags):
 need(flags & (1|2|4|16)==0,'split, encrypted or solid original member is not independently extractable')
 need(len(header)>=32 and header[2]==0x74 and int.from_bytes(header[5:7],'little')==len(header),'one exact RAR4 file header')
 need(int.from_bytes(header[7:11],'little')==len(packed),'packed extent mismatch')
 main,end=original_main_and_end();return main+header+packed+end

def pe_summary(raw):
 need(raw[:2]==b'MZ' and len(raw)>=64,'DOS program header')
 pos=int.from_bytes(raw[60:64],'little');need(pos+24<=len(raw) and raw[pos:pos+4]==b'PE\0\0','PE signature')
 machine,n,timestamp,_,_,optional_size,flags=struct.unpack_from('<HHIIIHH',raw,pos+4)
 need(machine==0x14c and 0<n<=32 and pos+24+optional_size+40*n<=len(raw),'bounded i386 section table')
 opt=pos+24;need(int.from_bytes(raw[opt:opt+2],'little')==0x10b,'PE32 optional header')
 sections=[]
 for i in range(n):
  p=opt+optional_size+i*40;name=raw[p:p+8].split(b'\0')[0].decode('ascii','strict')
  vsize,rva,size,offset=struct.unpack_from('<IIII',raw,p+8);need(offset+size<=len(raw),'original PE raw section bound')
  sections.append({'name':name,'rva':rva,'virtual_bytes':vsize,'raw_offset':offset,'raw_bytes':size,'raw_sha256':sha(raw[offset:offset+size])})
 return {'machine':machine,'coff_timestamp_untrusted':timestamp,'entrypoint_rva':int.from_bytes(raw[opt+16:opt+20],'little'),
  'image_base':int.from_bytes(raw[opt+28:opt+32],'little'),'sections':sections,'program_executed':False}

def fetcher_factory():
 direct={};pages=[];ua={'User-Agent':'Mozilla/5.0'}
 def fetch(part,start,end):
  key,total=PARTS[part]
  if part not in direct:
   url=f'https://www.mediafire.com/file/{key}/'
   with urllib.request.urlopen(urllib.request.Request(url,headers=ua),timeout=60) as r:
    page=r.read(4*1024*1024+1);need(len(page)<=4*1024*1024,'public page bound');referer=r.geturl()
   direct[part]=(direct_link(page.decode('utf-8','replace')),referer)
   pages.append({'part':part+1,'normal_download':url,'bytes':len(page),'sha256':sha(page)})
  url,referer=direct[part]
  with urllib.request.urlopen(urllib.request.Request(url,headers={**ua,'Referer':referer,'Range':f'bytes={start}-{end}'}),timeout=90) as r:
   need(r.status==206 and r.headers.get('Content-Range')==f'bytes {start}-{end}/{total}','exact original HTTP206 range required')
   raw=r.read(end-start+2);need(len(raw)==end-start+1,'source range extent');return raw
 return fetch,pages

def acquire(work):
 import rarfile
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);selected={};header_count=0;main_flags=None
 class SelectedComplete(Exception):pass
 def callback(info):
  nonlocal header_count,main_flags
  header_count+=1;need(header_count<=10000,'finite original header traversal')
  if info.type==rarfile.RAR_BLOCK_MAIN:main_flags=info.flags
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+n for n in TARGETS}:return
  leaf=name.rsplit('/',1)[1];need(leaf not in selected,'ambiguous duplicate original program')
  need(info.file_size==TARGETS[leaf][0] and info.compress_size<=1024*1024,'expected bounded original program extent')
  need(info.flags & (1|2|4|16)==0,'selected original program has split/encrypted/solid dependency')
  selected[leaf]={'filename':name,'header_offset':info.header_offset,'data_offset':info.data_offset,
    'compressed_bytes':info.compress_size,'uncompressed_bytes':info.file_size,'flags':info.flags,'original_crc32':info.CRC,'compression_method':info.compress_type}
  if len(selected)==2:raise SelectedComplete()
 try:rarfile.RarFile(reader,info_callback=callback,errors='strict')
 except SelectedComplete:pass
 need(set(selected)==set(TARGETS),'two exact original program members not located within budget')
 members={};rows=[]
 for number,(leaf,info) in enumerate(selected.items()):
  header=reader.at(info['header_offset'],info['data_offset']-info['header_offset']);packed=reader.at(info['data_offset'],info['compressed_bytes'])
  carrier=work/f'selected-{number}.rar';carrier.write_bytes(isolated_rar(header,packed,info['flags']));dst=work/f'out-{number}';dst.mkdir()
  proc=subprocess.run(['7z','x','-y',f'-o{dst}',str(carrier)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
  need(proc.returncode==0,'isolated original member static extraction failed')
  matches=[p for p in dst.rglob('*') if p.is_file() and p.as_posix().endswith(info['filename'])]
  need(len(matches)==1,'one exact extracted original program path');raw=matches[0].read_bytes()
  need((len(raw),sha(raw))==TARGETS[leaf] and zlib.crc32(raw)&0xffffffff==info['original_crc32'],'original complete program hash/CRC mismatch')
  members[leaf]=raw;rows.append({**info,'name':leaf,'bytes':len(raw),'sha256':sha(raw),
    'original_file_header_sha256':sha(header),'compressed_payload_sha256':sha(packed),'pe':pe_summary(raw)})
 return members,{'headers_visited':header_count,'original_main_flags':main_flags,'range_requests':len(reader.receipts),'actual_range_bytes':reader.fetched,
   'range_receipts':reader.receipts,'public_pages':pages,'whole_original_archive_or_part_rehashed':False,'two_original_members':rows}

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--sealed',type=Path,required=True);a=p.parse_args()
 a.work.mkdir(parents=True,exist_ok=False)
 d={'schema':'stoneage.native_album_program_sparse_source.r36','status':'NOT_ACQUIRED','source_scope':'EXISTING_MIXED25_SAVED_CLIENT_NOT_AUTHENTICATED_OFFICIAL_BUILD',
  'new_official_clients':0,'original_program_executed':False,'whole_bundle_reacquired':False,'original_binary_published':False,'selected_members':[]}
 try:
  members,receipt=acquire(a.work);d['receipt']=receipt;stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
   for name,raw in members.items():z.writestr(name,raw)
  plaintext=stream.getvalue();plain=a.work/'selected.zip';plain.write_bytes(plaintext)
  cert=ROOT/'research/recovered/STONEAGE-R35-DATA-RECIPIENT-CERT.pem'
  subprocess.run(['openssl','cms','-encrypt','-binary','-aes-256-cbc','-in',str(plain),'-out',str(a.sealed),'-outform','DER',str(cert)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  d.update(status='TWO_ORIGINAL_COMPLETE_PROGRAM_HASHES_MATCH',selected_members=list(members),
    private_transfer={'plaintext_zip_bytes':len(plaintext),'plaintext_zip_sha256':sha(plaintext),'ciphertext_bytes':a.sealed.stat().st_size,
      'ciphertext_sha256':sha(a.sealed.read_bytes()),'recipient_certificate_sha256':sha(cert.read_bytes())})
 except Exception as e:d['error']={'type':type(e).__name__,'message':str(e)[:400]}
 raw=(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode();a.output.write_bytes(raw)
 print('R36_SOURCE_METADATA_BEGIN');print(raw.decode(),end='');print('R36_SOURCE_METADATA_END')

if __name__=='__main__':main()
