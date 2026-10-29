"""Synthetic-only UI fixture: never opens retained original image bytes."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
from PIL import Image
from tools.stoneage_scene31_actor_sequence import REPORT

def build(out):
    r=json.loads(REPORT.read_text());images={'0':{},'1':{}};ims={};canvases=[]
    for palette in ('0','1'):
        for i,b in enumerate(r['bitmaps']):
            im=Image.new('RGBA',(b['width'],b['height']),(0,0,0,0))
            px=im.load()
            for y in range(im.height):
                for x in range(im.width):
                    if (x+y)%7:
                        px[x,y]=((i*17+x*3+int(palette)*61)%256,(i*29+y*5)%256,(i*43+x+y)%256,255)
            buf=io.BytesIO();im.save(buf,format='PNG');images[palette][str(b['bitmapno'])]=base64.b64encode(buf.getvalue()).decode();ims[(palette,b['bitmapno'])]=im
        rows={b['bitmapno']:b for b in r['bitmaps']}
        for a in r['sequences']:
            for fi,(no,x,y,sound)in enumerate(a['frames']):
                b=rows[no];im=ims[(palette,no)];c=Image.new('RGBA',(240,260),'#142129')
                c.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(120+2*(b['xoff']+x),200+2*(b['yoff']+y)))
                canvases.append(dict(palette=palette,direction=a['direction'],frame_index=fi,bitmapno=no,RGBA_sha256=hashlib.sha256(c.tobytes()).hexdigest()))
    model=dict(synthetic_fixture=True,report=r,images=images,canvas_hashes=canvases)
    template=Path(__file__).with_name('scene31-actor-sequence-observer.html').read_text()
    out.write_text(template.replace('PRIVATE_DATA_PLACEHOLDER',json.dumps(model,separators=(',',':'))).replace('<h1>','<h1>合成控件验收素材 · ',1))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);build(p.parse_args().output)
