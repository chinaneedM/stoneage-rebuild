"""Synthetic pixels in real-size cards; never reads private original pixels."""
import argparse,base64,copy,hashlib,io,json
from pathlib import Path
from PIL import Image
from tools.stoneage_scene23_body_visuals import REPORT
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=json.loads(REPORT.read_bytes());images={'0':{},'1':{}};ims={};hashes=[]
for palette in ('0','1'):
 for i,b in enumerate(r['bitmaps']):
  im=Image.new('RGBA',(b['width'],b['height']),((i*23+int(palette)*50)%255,(i*53+30)%255,(i*71+40)%255,255));buf=io.BytesIO();im.save(buf,format='PNG');images[palette][str(b['bitmapno'])]=base64.b64encode(buf.getvalue()).decode();ims[(palette,b['bitmapno'])]=im
 rows={b['bitmapno']:b for b in r['bitmaps']}
 for g in r['groups']:
  for d in g['directions']:
   n,x,y,sound=d['first_frame'];b=rows[n];im=ims[(palette,n)];c=Image.new('RGBA',(240,260),'#142129');c.alpha_composite(im.resize((b['width']*2,b['height']*2),Image.Resampling.NEAREST),(120+2*(x+b['xoff']),200+2*(y+b['yoff'])));hashes.append(dict(group=g['spr_no'],direction=d['direction'],palette=palette,RGBA_sha256=hashlib.sha256(c.tobytes()).hexdigest()))
model=dict(synthetic_fixture=True,report=r,images=images,canvas_hashes=hashes)
s=Path(__file__).with_name('stoneage_scene23_observer.html').read_text().replace('__SCENE23_MODEL__',json.dumps(model,separators=(',',':'))).replace('<h1>','<h1>全部合成色块｜',1)
a.output.write_text(s)
