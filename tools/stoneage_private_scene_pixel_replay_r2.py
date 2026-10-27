"""Independent byte replay of eight actual private source images, never gameplay.
Requires Pillow; keep every proprietary input and PNG outside public Git.
"""
from pathlib import Path
import hashlib,json,struct
from PIL import Image,ImageDraw,ImageFont
import argparse
parser=argparse.ArgumentParser(description='Independent private RD/PNG replay; not original scene rendering')
parser.add_argument('--private-dir',type=Path,required=True)
parser.add_argument('--source-report',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
if hashlib.sha256(args.source_report.read_bytes()).hexdigest()!='da869a0921fe71970d547210f2d110c4fc643a950fb12a27273580660c7895c9':
 raise ValueError('source report is not the fixed real-source R2 report')
folder=args.private_dir.resolve();base=args.output_dir.resolve()
root=Path(__file__).resolve().parents[1]
if base==root or root in base.parents or folder==root or root in folder.parents:
 raise ValueError('private pixel input/output must be outside public repository')
base.mkdir(parents=True,exist_ok=False)
m=json.loads((folder/'source-manifest.json').read_text());s=json.loads(args.source_report.read_text())
if m!=s['observation']:raise ValueError('source report and private manifest differ')
sha=lambda b:hashlib.sha256(b).hexdigest()
adrn=(folder/'source-adrn_15.bin').read_bytes();mp=(folder/'source-map-1001.dat').read_bytes()
assert sha(adrn)==m['source_adrn_sha256'] and sha(mp)==m['source_map_payload_sha256']
w,h=struct.unpack_from('<II',mp);assert(w,h)==(30,30)
planes=struct.unpack_from('<'+str(w*h*3)+'H',mp,8);x1,y1,x2,y2=m['viewport_inclusive'];ids=set()
for layer in (0,1):
 for y in range(y1,y2+1):
  for x in range(x1,x2+1):
   n=planes[layer*w*h+y*w+x]
   if n>99:ids.add(n)
assert sorted(ids)==m['map_ids_required']
def independent_decode(b):
 assert b[:2]==b'RD';w,h=struct.unpack_from('<II',b,4);data=b[16:];out=bytearray();p=0
 if b[2]==0:return w,h,data[:w*h]
 assert b[2]==1
 while p<len(data):
  c=data[p];p+=1;family=c>>6;count=c&15;extension=(c>>4)&3
  assert family in (0,2,3) and extension<3
  value=None
  if family==2:value=data[p];p+=1
  for _ in range(extension):count=count*256+data[p];p+=1
  if family==0:out.extend(data[p:p+count]);p+=count
  elif family==2:out.extend(bytes([value])*count)
  else:out.extend(bytes(count))
  assert len(out)<=w*h
 assert len(out)==w*h
 return w,h,bytes(out)
rows=[]
try:
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
except OSError:
 font=small=ImageFont.load_default()
canvas=Image.new('RGB',(1000,600),'#172027');d=ImageDraw.Draw(canvas)
d.text((24,18),'StoneAge | Actual source image indices | 8 recovered RD blocks',fill='white',font=font)
d.text((24,44),'Mixed25 preserved carrier; floor 1001 [14,14..16,16]. Grayscale indices; palette/layout unverified.',fill='#ebc37d',font=small)
for i,r in enumerate(m['resources']):
 assert r['rendered_artwork'];row=r['occurrences'][0];record=adrn[row['index']*80:(row['index']+1)*80]
 assert sha(record)==row['source_record_sha256'] and struct.unpack_from('<I',record,76)[0]==r['map_id']
 rd=(folder/(r['filename']+'.rd')).read_bytes();assert sha(rd)==r['rd_block_sha256']
 iw,ih,pixels=independent_decode(rd);assert sha(pixels)==r['decoded_palette_indices_sha256']
 png=(folder/r['filename']).read_bytes();assert sha(png)==r['private_grayscale_png_sha256']
 im=Image.open(folder/r['filename']);im.load();assert im.mode=='L' and im.size==(iw,ih) and im.tobytes()==pixels
 x=(i%4)*250+12;y=82+(i//4)*250
 d.rectangle((x,y,x+236,y+230),fill='#202b33',outline='#4a5b64')
 scale=min(3,195//iw,165//ih);scaled=im.convert('RGB').resize((iw*scale,ih*scale),Image.Resampling.NEAREST)
 canvas.paste(scaled,(x+(236-scaled.width)//2,y+12+(165-scaled.height)//2))
 d.text((x+10,y+182),f"map {r['map_id']} / bitmap {row['bitmapno']}",fill='white',font=small)
 d.text((x+10,y+201),f"{iw} x {ih}; RD {sha(rd)[:14]}",fill='#b8c6ce',font=small)
 rows.append({'map_id':r['map_id'],'bitmapno':row['bitmapno'],'width':iw,'height':ih,'decoded_sha256':sha(pixels),'independent_decoder_matches_Pillow_PNG':True})
d.text((24,574),'Not a game capture. No original world entry, palette selection, alpha or scene projection proved.',fill='#ebc37d',font=small)
canvas.save(base/'stoneage-scene02-source-index-contact-sheet.png')
result={'schema':'stoneage.scene02.independent_pixel_replay.r2','original_source_report_sha256':sha(args.source_report.read_bytes()),'full_adrn_sha_verified':True,'full_map_sha_verified':True,'independent_3x3_map_ID_set_verified':True,'eight_ADRN_records_verified':True,'independent_RD_decoder_and_Pillow_pixels_equal':True,'resources':rows,'contact_sheet_sha256':sha((base/'stoneage-scene02-source-index-contact-sheet.png').read_bytes()),'original_world_entered':False,'original_palette_or_scene_claimed':False}
(base/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
