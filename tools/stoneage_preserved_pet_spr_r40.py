"""Original mixed-carrier SPR evidence for three server graphic integers.

Only source-qualified metadata is exported. No runtime deployment or official
species identity follows from common archive membership or equal numeric keys.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zlib
import rarfile
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar, need, PREFIX
from tools.stoneage_pet_template_material_r39 import SOURCE as SERVER_SOURCE, validate as validate_server

EXPECTED={
 'spradrn_5.bin':(10164,'5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6'),
 'spr_4.bin':(5588120,'865b58860c7fe025850bf942f6ce6a5deb4464993ceeecbc20a034c99e159749')}
SCOPE='MIXED25_PRESERVED_SAME_ARCHIVE_CLIENT_SERVER_SUBTREES_NOT_SAME_DEPLOYED_BUILD_OR_OFFICIAL_RELEASE'
SERVER_SHA='09dc73e801f5020059812acb71b1db6d41e8987a3730ee2126348ee349a24d3b'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def source_keys():
 raw=SERVER_SOURCE.read_bytes();need(sha(raw)==SERVER_SHA,'exact R39 original server source report')
 material=validate_server(json.loads(raw))
 keys=sorted({r['graphic_field_column_37'] for r in material['selected_rows']})
 need(keys==[100250,100251,100252],'bounded R39 graphic integer set')
 return keys

def parse_pair(index,body,keys):
 need(len(index)>0 and len(index)%12==0,'integral original 12-byte SPR index')
 rows=[]
 for i in range(len(index)//12):
  no,start,count,reserved=struct.unpack_from('<IIHH',index,12*i)
  need(0<=start<len(body),'original SPR index start in source body')
  rows.append([i,no,start,count,reserved])
 offsets=sorted({r[2] for r in rows});end_for={o:(offsets[i+1] if i+1<len(offsets) else len(body)) for i,o in enumerate(offsets)}
 groups=[]
 for gi,no,start,count,reserved in rows:
  if no not in keys:continue
  end=end_for[start];cursor=start;animations=[];all_bmp=[]
  for ai in range(count):
   need(cursor+12<=end,'original selected animation header bounds')
   header_offset=cursor;direction,anim_no,duration,nframes=struct.unpack_from('<HHII',body,cursor);cursor+=12
   need(nframes<=(end-cursor)//10,'original selected frame span bounds')
   frames=[]
   for _ in range(nframes):
    bmp,x,y,sound=struct.unpack_from('<IhhH',body,cursor);cursor+=10
    frames.append([bmp,x,y,sound]);all_bmp.append(bmp)
   animations.append({'index':ai,'header_offset':header_offset,'direction':direction,'anim_no':anim_no,
    'duration':duration,'frame_count':nframes,'end_offset':cursor,'frames':frames})
  need(cursor==end,'selected original SPR exact physical boundary')
  groups.append({'group_index':gi,'spr_no':no,'offset':start,'anim_count':count,'reserved':reserved,
   'index_record_sha256':sha(index[12*gi:12*gi+12]),'end_offset':cursor,'segment_sha256':sha(body[start:cursor]),
   'frame_count':len(all_bmp),'sentinel_frames':all_bmp.count(0xffffffff),
   'distinct_non_sentinel_bitmap_keys':len(set(all_bmp)-{0xffffffff}),'animations':animations})
 counts=Counter(r[1] for r in rows);offset_counts=Counter(r[2] for r in rows)
 return {'all_index_rows':rows,'index_rows_count':len(rows),'index_record_layout':'u32_spr_no_u32_offset_u16_anim_count_u16_reserved',
  'duplicate_group_keys':{str(k):v for k,v in sorted(counts.items()) if v>1},
  'duplicate_physical_offsets':{str(k):v for k,v in sorted(offset_counts.items()) if v>1},
  'selected_graphic_keys':list(keys),'unmatched_graphic_keys':[k for k in keys if not any(g['spr_no']==k for g in groups)],
  'selected_groups':groups,'selected_animation_occurrences':sum(g['anim_count'] for g in groups),
  'selected_frame_occurrences':sum(g['frame_count'] for g in groups),
  'selected_sentinel_occurrences':sum(g['sentinel_frames'] for g in groups),
  'frame_layout':'u32_bitmap_i16_x_i16_y_u16_sound','physical_boundary_rule':'NEXT_STRICTLY_GREATER_OFFSET_PRESERVE_DUPLICATE_INDEX_OCCURRENCES'}

def read_extent(reader,start,size):
 reader.seek(start);parts=[]
 while size:
  n=min(size,1024*1024);part=reader.read(n);need(len(part)==n,'exact bounded compressed extent');parts.append(part);size-=n
 return b''.join(parts)

def acquire(work,receipt):
 fetch,pages=fetcher_factory();reader=SparseParts(fetch);chosen={};count=0
 def visitor(info):
  nonlocal count
  count+=1;need(count<=10000,'finite 10k archive header limit')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name not in {PREFIX+'data/'+n for n in EXPECTED}:return
  leaf=name.rsplit('/',1)[1];need(leaf not in chosen,'ambiguous duplicate selected original')
  need(info.file_size==EXPECTED[leaf][0] and info.compress_size<=6*1024*1024,'bounded expected selected original size')
  need(info.flags&(1|2|4|16)==0,'independent unencrypted unsplit nonsolid original member')
  chosen[leaf]={'name':name,'header_offset':info.header_offset,'data_offset':info.data_offset,
   'bytes':info.file_size,'compressed_bytes':info.compress_size,'flags':info.flags,'crc32':info.CRC,'compression_method':info.compress_type}
 try:
  rarfile.RarFile(reader,info_callback=visitor,errors='strict')
  need(set(chosen)==set(EXPECTED),'both exact original SPR members in full header walk')
  result={};receipt['members']=[]
  for i,(leaf,entry) in enumerate(chosen.items()):
   header=read_extent(reader,entry['header_offset'],entry['data_offset']-entry['header_offset'])
   packed=read_extent(reader,entry['data_offset'],entry['compressed_bytes'])
   archive=work/f'member-{i}.rar';archive.write_bytes(isolated_rar(header,packed,entry['flags']))
   dst=work/f'out-{i}';proc=subprocess.run(['unar','-f','-o',str(dst),str(archive)],capture_output=True,timeout=120)
   need(proc.returncode==0,'finite original SPR extraction failed')
   matches=[p for p in dst.rglob('*') if p.is_file() and p.as_posix().endswith(entry['name'])]
   need(len(matches)==1,'unique extracted original SPR path');raw=matches[0].read_bytes()
   need((len(raw),sha(raw))==EXPECTED[leaf],'whole original SPR SHA and size')
   need(zlib.crc32(raw)&0xffffffff==entry['crc32'],'whole original SPR CRC')
   result[leaf]=raw;receipt['members'].append({**entry,'sha256':sha(raw),'header_sha256':sha(header),
    'compressed_payload_sha256':sha(packed),'extractor':'unar','extractor_returncode':proc.returncode})
  return result
 finally:
  receipt.update(headers_visited=count,range_requests=len(reader.receipts),actual_range_bytes=reader.fetched,
   range_receipts=reader.receipts,public_pages=pages,whole_package_rehashed=False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 report={'schema':'stoneage.preserved_pet_spr_source.r40','source_scope':SCOPE,'status':'NOT_ACQUIRED',
  'server_source_sha256':SERVER_SHA,'original_payload_published':False,'original_program_executed':False,
  'same_deployed_build_proven':False,'official_species_identity_authenticated':False,'actual_render_or_audio_proven':False,
  'new_official_clients':0,'receipt':{}}
 try:
  keys=source_keys()
  with tempfile.TemporaryDirectory(prefix='r40-private-') as tmp:
   files=acquire(Path(tmp),report['receipt']);material=parse_pair(files['spradrn_5.bin'],files['spr_4.bin'],keys)
   need(material['index_rows_count']==847,'old original full SPR index count')
   report.update(status='ORIGINAL_PAIR_SHA_CRC_MATCH_SELECTED_SPR_DERIVED',material=material)
 except Exception as e:report['error']={'type':type(e).__name__,'message':str(e)[:400]}
 a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print('R40_METADATA_BEGIN');print(a.output.read_text(),end='');print('R40_METADATA_END')
if __name__=='__main__':main()
