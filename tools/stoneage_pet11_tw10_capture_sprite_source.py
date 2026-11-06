#!/usr/bin/env python3
"""Read authenticated private TW1 original animation/RD files for PET11.

No original bitmap or complete game bytes are emitted: stdout is source-derived
numeric metadata/hashes. The separate mixed25 SPRADRN must be supplied to verify
12-byte index identity; matching index bytes do NOT prove identical sprite
payloads or same deployed server. Never run an original executable.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ZIP_BYTES=372626292
ZIP_SHA='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
MEMBERS={
 'spradrn_1.bin':(5568,'275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25'),
 'spr_1.bin':(2889630,'53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'),
 'adrn_1.bin':(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'real_1.bin':(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
}
MIXED_SHA='5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6'
KEYS=(100329,100355)

def require(value,description):
 if not value:raise ValueError('PET11 original source: '+description)

def sha(data):return hashlib.sha256(data).hexdigest()

def file_sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def records(raw):
 require(len(raw)%12==0,'12-byte SPRADRN records')
 return [struct.unpack_from('<IIHH',raw,i*12) for i in range(len(raw)//12)]

def rd_indices(rd):
 """Strict original RD decode, with one separately qualified terminal overflow."""
 require(len(rd)>=16 and rd[:2]==b'RD','original RD magic')
 w,h=struct.unpack_from('<ii',rd,4)
 require(0<w<=1024 and 0<h<=1024,'RD dimension')
 flag=rd[2]
 if flag==0:
  require(len(rd)>=16+w*h,'raw RD length')
  return w,h,bytes(rd[16:16+w*h]),w*h,True
 require(flag==1,'unknown RD flag')
 out=bytearray();pos=16;last=None
 while pos<len(rd):
  ctl=rd[pos];pos+=1;family=ctl&0xf0
  if family in (0,16,32):base=0;kind='literal'
  elif family in (128,144,160):base=128;kind='repeat'
  elif family in (192,208,224):base=192;kind='zero'
  else:raise ValueError('unrecognized original RD control')
  if kind=='repeat':
   require(pos<len(rd),'missing repeat byte');value=rd[pos];pos+=1
  k=ctl&15
  extra=(family-base)//16
  require(pos+extra<=len(rd),'truncated length')
  for _ in range(extra):k=(k<<8)+rd[pos];pos+=1
  before=len(out)
  if kind=='literal':
   require(pos+k<=len(rd),'truncated literal')
   out.extend(rd[pos:pos+k]);pos+=k
  elif kind=='repeat':out.extend(bytes([value])*k)
  else:out.extend(bytes(k))
  last=(ctl,kind,k,before,len(out),pos)
 good=len(out)==w*h
 if not good:
  require(len(out)==w*h+1 and last==(0xc2,'zero',2,w*h-1,w*h+1,len(rd)) and out[-2:]==b'\0\0','unqualified original RLE anomaly')
 return w,h,bytes(out[:w*h]),len(out),good

def derive(original_zip:Path,mixed_index:Path):
 require(original_zip.stat().st_size==ZIP_BYTES and file_sha(original_zip)==ZIP_SHA,'entire private TW1 ZIP identity')
 require(mixed_index.stat().st_size==10164 and file_sha(mixed_index)==MIXED_SHA,'mixed25 same-archive original index identity')
 with zipfile.ZipFile(original_zip) as z:
  require(len(z.infolist())==379 and z.testzip() is None,'original ZIP member CRC')
  source={}
  for name,(length,digest) in MEMBERS.items():
   raw=z.read('source/data/'+name)
   require(len(raw)==length and sha(raw)==digest,'complete original source member '+name)
   source[name]=raw
 adrn=source['adrn_1.bin'];real=source['real_1.bin'];spr=source['spr_1.bin']
 tw=records(source['spradrn_1.bin']);mixed=records(mixed_index.read_bytes())
 selections=[];wanted=set();groups=[]
 for key in KEYS:
  q=[(i,v) for i,v in enumerate(tw) if v[0]==key]
  m=[(i,v) for i,v in enumerate(mixed) if v[0]==key]
  require(len(q)==len(m)==1 and q[0][1]==m[0][1],'two original indexes not exact equal')
  ix,(number,start,count,unused)=q[0]
  end=tw[ix+1][1] if ix+1<len(tw) else len(spr)
  require(start<end<=len(spr) and count==56 and unused==16,'original group extents')
  pos=start;actions=[];bitmaps=[];sound=Counter()
  for ai in range(count):
   require(pos+12<=end,'short original animation header')
   direction,act,duration,frames=struct.unpack_from('<HHII',spr,pos);pos+=12
   require(0<frames<=112 and pos+10*frames<=end,'original frame bounds')
   for fi in range(frames):
    no,x,y,voice=struct.unpack_from('<IhhH',spr,pos);pos+=10
    require(0<no!=0xffffffff,'unqualified original sprite bitmap sentinel')
    wanted.add(no);bitmaps.append(no)
    if voice:sound[voice]+=1
   actions.append((direction,act,frames,duration))
  require(pos==end,'source animation extents differ')
  require(sorted((direction,act) for direction,act,_,_ in actions)==[(d,a) for d in range(8) for a in (0,1,2,3,4,9,10)],'original action/direction matrix')
  groups.append({'spr_no':key,'original_tw1_index':ix,'original_mixed25_index':m[0][0],
   'source_index_record_sha256':sha(source['spradrn_1.bin'][ix*12:(ix+1)*12]),
   'original_source_segment_bytes':end-start,'original_source_segment_sha256':sha(spr[start:end]),
   'original_animation_sequences':count,'original_frame_positions':len(bitmaps),
   'source_distinct_bitmap_keys':len(set(bitmaps)),'original_source_sound_field_counts':dict(sorted(sound.items()))})
  selections.append(set(bitmaps))
 require(len(wanted)==496 and len(selections[0])==len(selections[1])==248 and not (selections[0]&selections[1]),'source set conservation')
 found={n:[] for n in wanted}
 for i in range(0,len(adrn),80):
  n=struct.unpack_from('<I',adrn,i)[0]
  if n in found:found[n].append((i//80,adrn[i:i+80]))
 require(all(len(v)==1 for v in found.values()),'source bitmap record ambiguity')
 rows=[]
 for n in sorted(wanted):
  i,b=found[n][0];num,offset,length,x,y,w,h=struct.unpack_from('<7i',b)
  require(num==n and 16<=length<=100000 and offset>=0 and offset+length<=len(real),'original REAL source extent')
  rd=real[offset:offset+length];width,height,pixels,count,strict_ok=rd_indices(rd)
  require((width,height)==(w,h),'source bitmap geometry')
  rows.append({'bitmapno':n,'adrn_record_sha256':sha(b),'rd_sha256':sha(rd),'indices_sha256':sha(pixels),
   'strict_rd':strict_ok,'decoded_count':count,'canvas_count':w*h,'source_size':length})
 require(len(rows)==496 and sum(x['strict_rd'] for x in rows)==495,'source strict count')
 require([x['bitmapno'] for x in rows if not x['strict_rd']]==[113576],'specific bounded original source RD')
 for i,g in enumerate(groups):
  chosen=[x for x in rows if x['bitmapno'] in selections[i]]
  g['strict_rd_complete']=sum(x['strict_rd'] for x in chosen)
  g['bounded_original_source_canvas_prefix']=len(chosen)-g['strict_rd_complete']
  for kind,field in [('original_adrn_record_sha256_sequence_sha256','adrn_record_sha256'),
                      ('original_rd_sha256_sequence_sha256','rd_sha256'),
                      ('canvas_index_sha256_sequence_sha256','indices_sha256')]:
   g[kind]=sha(''.join(x[field] for x in chosen).encode('ascii'))
 return {'groups':groups,'frame_positions':sum(g['original_frame_positions']for g in groups),
  'bitmap_count':len(rows),'strict_bitmap_count':495,'bounded_bitmap_count':1,
  'all_original_adrn_sha256_sequence_sha256':sha(''.join(x['adrn_record_sha256']for x in rows).encode('ascii')),
  'all_original_rd_sha256_sequence_sha256':sha(''.join(x['rd_sha256']for x in rows).encode('ascii')),
  'all_original_canvas_index_sha256_sequence_sha256':sha(''.join(x['indices_sha256']for x in rows).encode('ascii')),
  'bounded_source_bitmap_record':next(x for x in rows if not x['strict_rd']),
  'native_gameplay_run':False,'native_palette_selection_proven':False,
  'same_historical_deployment_as_mixed25_proven':False}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--private-tw1-zip',type=Path,required=True)
 p.add_argument('--private-mixed25-spradrn',type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(derive(a.private_tw1_zip,a.private_mixed25_spradrn),ensure_ascii=False,indent=2))

if __name__=='__main__':main()