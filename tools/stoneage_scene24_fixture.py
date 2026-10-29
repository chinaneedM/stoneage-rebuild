"""Synthetic shop cards, preserving only source geometry and public numbers."""
import argparse,base64,hashlib,io,json
from pathlib import Path
from PIL import Image
from tools.stoneage_scene24_shop_images import REPORT
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=json.loads(REPORT.read_bytes());images={'0':{},'1':{}};ims={};hashes=[]
rows=[row for item in r['items']for row in[item['alias_candidate'],item['literal_bitmap_control']]]
for palette in('0','1'):
 for i,row in enumerate(rows):
  im=Image.new('RGBA',(row['width'],row['height']),((i*39+int(palette)*70)%255,(i*61+40)%255,(i*77+50)%255,255));buf=io.BytesIO();im.save(buf,format='PNG');images[palette][str(row['bitmapno'])]=base64.b64encode(buf.getvalue()).decode();ims[(palette,row['bitmapno'])]=im
for mode in('alias','literal'):
 for palette in('0','1'):
  for scale in(2,4):
   for item in r['items']:
    row=item['alias_candidate'if mode=='alias'else'literal_bitmap_control'];im=ims[(palette,row['bitmapno'])];im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);c=Image.new('RGBA',(320,360),'#142129');c.alpha_composite(im,((320-im.width)//2,(360-im.height)//2));hashes.append(dict(item=item['id'],mode=mode,palette=palette,scale=scale,RGBA_sha256=hashlib.sha256(c.tobytes()).hexdigest()))
model=dict(synthetic_fixture=True,report=r,images=images,canvas_hashes=hashes);s=Path(__file__).with_name('stoneage_scene24_observer.html').read_text().replace('__SCENE24_MODEL__',json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')).replace('<h1>','<h1>全部合成色块｜',1);a.output.write_text(s)
