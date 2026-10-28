"""Independent private composition for the controlled source-order observer."""
import argparse,base64,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw

def sha(b):return hashlib.sha256(b).hexdigest()
def pack_at(path):return json.loads(Path(path).read_text().split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
def compose(pack,x,y,native=True,pet=100250,direction=0,frame=0,marker=True,camera_dy=0):
    maps={};actors={}
    for no,b64 in pack['room']['sprites'].items():
        raw=base64.b64decode(b64,validate=True)
        if sha(raw)!=pack['room']['sprite_sha256'][no]:raise ValueError('original room PNG identity')
        maps[int(no)]=Image.open(io.BytesIO(raw)).convert('RGBA')
    for no,b64 in pack['actor_images'].items():
        b=next(v for v in pack['actors']['bitmaps'] if v['bitmapno']==int(no));raw=base64.b64decode(b64,validate=True)
        if sha(raw)!=b['PNG_sha256']:raise ValueError('original actor PNG identity')
        im=Image.open(io.BytesIO(raw)).convert('RGBA')
        if sha(im.tobytes())!=b['candidate_RGBA_sha256']:raise ValueError('source RGBA identity')
        actors[int(no)]=im
    bg=Image.new('RGBA',(960,720),(17,35,42,255))
    c=next(c for c in pack['actor_order_evidence']['cases'] if c['anchor']==[x,y] and c['pet_spr']==100250 and c['direction']==0)
    order=c['native_draw_tokens'] if native else pack['room']['R6_native_sorted_queue_numbers']+['human','pet']
    for token in order:
        if isinstance(token,int):
            p=pack['room']['placements'][token];im=maps[p['map_id']];px,py=p['draw_x'],p['draw_y']
        else:
            idx=0 if token=='human' else 1;no=100000 if idx==0 else pet
            g=next(g for g in pack['actors']['groups'] if g['spr_no']==no)
            a=next(a for a in g['animations'] if a['direction']==direction and a['action']==2);f=a['frames'][frame%len(a['frames'])]
            b=next(b for b in pack['actors']['bitmaps'] if b['bitmapno']==f[0]);im=actors[f[0]]
            px=(x+y-26)*32+idx*32+f[1]+b['xoff'];py=(y-x)*24+idx*24+f[2]+b['yoff']
        im=im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST);bg.alpha_composite(im,(210+px*3,420+camera_dy+py*3))
    if marker:
        ax=210+(x+y-26)*96;ay=420+camera_dy+(y-x)*72;d=ImageDraw.Draw(bg)
        d.rectangle((ax-12,ay,ax+14,ay+2),fill=(224,182,110,255));d.rectangle((ax,ay-12,ax+2,ay+14),fill=(224,182,110,255))
    return bg

def verify(directory):
    directory=Path(directory);pack=pack_at(directory/'stoneage-room-r9-order-observer.html');cases=[]
    for y in range(13,18):
        for x in range(13,18):
            before=compose(pack,x,y,False,marker=False).tobytes();after=compose(pack,x,y,True,marker=False).tobytes()
            count=sum(before[i:i+4]!=after[i:i+4] for i in range(0,len(before),4))
            cases.append({'anchor':[x,y],'changed_pixels_without_modern_marker':count,'old_RGBA_sha256':sha(before),'candidate_RGBA_sha256':sha(after)})
    result={'schema':'stoneage.scene09.independent_pixels.r1','source_PNGs':218,'position_cases':cases,
        'changed_positions':sum(c['changed_pixels_without_modern_marker']>0 for c in cases),
        'complete_original_frame_phase_order_proven':False,'original_world_entered':False}
    for name,x,y,mode in [('example-native',17,13,True),('example-overlay',17,13,False),('default-native',15,15,True)]:
        p=directory/'browser'/('internal-'+name+'-rgba.bin')
        if p.exists():
            expected=compose(pack,x,y,mode,camera_dy=80 if name.startswith('example') else 0).tobytes();actual=p.read_bytes()
            if expected!=actual:raise ValueError('independent Pillow/Chromium pixels differ: '+name)
            result[name]={'pixels':691200,'all_RGBA_identical':True,'sha256':sha(actual)}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('report',type=Path);a=p.parse_args();r=verify(a.directory);a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='position_cases'}))
