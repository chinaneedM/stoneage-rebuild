from pathlib import Path
import json,hashlib,struct,base64,io,zipfile
from PIL import Image,ImageDraw
import argparse
p=argparse.ArgumentParser(description='Independent private action0 RD and full canvas replay; no original runtime')
p.add_argument('--private-dir',type=Path,required=True);a=p.parse_args();base=a.private_dir.resolve()
root=Path(__file__).resolve().parents[1]
if base==root or root in base.parents:raise ValueError('private pixels must remain outside Git')
report=json.loads((base/'source-derived-report.json').read_bytes());html=(base/'stoneage-room-r13-action0-observer.html').read_bytes();pack=json.loads(html.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);sha=lambda b:hashlib.sha256(b).hexdigest()
# Second decoder: independent control families and length arithmetic.
def decode(b):
 assert b[:2]==b'RD';w,h=struct.unpack_from('<II',b,4);data=b[16:];out=bytearray();p=0
 if b[2]==0:
  assert len(data)>=w*h;return w,h,data[:w*h]
 assert b[2]==1
 while p<len(data):
  c=data[p];p+=1;family=c>>6;count=c&15;extension=(c>>4)&3
  assert family in (0,2,3) and extension<3
  if family==2:value=data[p];p+=1
  for _ in range(extension):count=count*256+data[p];p+=1
  if family==0:assert p+count<=len(data);out.extend(data[p:p+count]);p+=count
  elif family==2:out.extend(bytes([value])*count)
  else:out.extend(bytes(count))
  assert len(out)<=w*h
 assert len(out)==w*h;return w,h,bytes(out)
sap=(base/'private-palette.sap').read_bytes();assert sha(sap)==report['source_files']['Palet_1.sap']['sha256'];colors={i+16:tuple(sap[i*3:i*3+3][::-1]) for i in range(224)};colors[168]=(0,0,0);colors[0]=(0,0,0)
ims={}
with zipfile.ZipFile(base/'private-original-rd-subset.zip') as z:
 assert len(z.namelist())==208
 for row in report['bitmaps']:
  n=str(row['bitmapno']);rd=z.read(n+'.rd');assert sha(rd)==row['RD_sha256'];w,h,px=decode(rd);assert sha(px)==row['index_pixels_sha256']
  rgba=bytes(v for y in range(h-1,-1,-1) for p in px[y*w:(y+1)*w] for v in (*colors[p],0 if p==0 else 255))
  assert sha(rgba)==row['candidate_RGBA_sha256'];png=base64.b64decode(pack['actor_images'][n]);assert sha(png)==row['PNG_sha256'];im=Image.open(io.BytesIO(png)).convert('RGBA');assert im.size==(w,h) and im.tobytes()==rgba;ims[int(n)]=im
for n,b in pack['actor_images'].items():ims[int(n)]=Image.open(io.BytesIO(base64.b64decode(b))).convert('RGBA')
room=pack['room'];maps={int(n):Image.open(io.BytesIO(base64.b64decode(b))).convert('RGBA') for n,b in room['sprites'].items()}
rows={b['bitmapno']:b for b in pack['actors']['bitmaps']};canvas=Image.new('RGBA',(960,720),'#11232a')
def paste(im,x,y,dest):
 big=im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST);dest.alpha_composite(big,(480+3*(x-90),360+3*(y+20)))
for no in room['R6_native_sorted_queue_numbers']:
 p=room['placements'][no];paste(maps[p['map_id']],p['draw_x'],p['draw_y'],canvas)
expected=[]
human=pack['actors']['groups'][0]
for g in pack['actors']['groups'][1:]:
 for a in g['animations']:
  ha=next(x for x in human['animations'] if x['direction']==a['direction'] and x['action']==2)
  for fi,f in enumerate(a['frames']):
   c=canvas.copy();draw=ImageDraw.Draw(c);draw.rectangle((582,420,608,422),fill="#e0b66e");draw.rectangle((594,408,596,434),fill="#e0b66e")
   for i,frame in enumerate([ha['frames'][fi%len(ha['frames'])],f]):
    r=rows[frame[0]];paste(ims[frame[0]],128+i*32+frame[1]+r['xoff'],i*24+frame[2]+r['yoff'],c)
   expected.append({'pet':g['spr_no'],'direction':a['direction'],'frame':fi,'bitmap':f[0],'canvas_sha256':sha(c.tobytes())})
(base/'independent-expected-canvases.json').write_text(json.dumps(expected,indent=2)+'\n');print('Independent RD/indices/RGBA/PNG:208; expected canvases:',len(expected))
