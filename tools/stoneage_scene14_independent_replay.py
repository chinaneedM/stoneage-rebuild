"""Independent private NPC source/pixel replay; public CI does not use originals."""
import argparse,base64,hashlib,io,json,struct
from pathlib import Path
from PIL import Image,ImageDraw


def digest(b):return hashlib.sha256(b).hexdigest()

def decode(b):
    assert b[:2]==b'RD';w,h=struct.unpack_from('<II',b,4);encoded=b[16:];out=bytearray();p=0
    if b[2]==0:return w,h,encoded[:w*h]
    assert b[2]==1
    while p<len(encoded):
        c=encoded[p];p+=1;family=c>>6;extension=(c>>4)&3;n=c&15
        assert family in (0,2,3) and extension<3
        if family==2:value=encoded[p];p+=1
        for _ in range(extension):n=n*256+encoded[p];p+=1
        if family==0:out.extend(encoded[p:p+n]);p+=n
        elif family==2:out.extend([value]*n)
        else:out.extend([0]*n)
        assert len(out)<=w*h
    assert len(out)==w*h;return w,h,bytes(out)


def source_blocks(raw):
    groups=[];current=None;offset=0
    for line in raw.splitlines(keepends=True):
        token=line.strip()
        if token==b'{':assert current is None;current={'start':offset,'fields':{}}
        elif token==b'}':
            assert current is not None;current['end']=offset+len(line.rstrip(b'\r\n'));groups.append(current);current=None
        elif current is not None and token and not token.startswith(b'#'):
            key,value=token.split(b'=',1);assert key not in current['fields'];current['fields'][key]=value
        offset+=len(line)
    assert current is None;return groups


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);p.add_argument('--originals',type=Path,required=True);a=p.parse_args()
    folder=a.private_dir.resolve();root=Path(__file__).resolve().parents[1];assert folder!=root and root not in folder.parents
    r=json.loads((folder/'source-derived-report.json').read_bytes());pack=json.loads((folder/'stoneage-room-r14-shop-observer.html').read_bytes().split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);actual=json.loads((folder/'browser-replay.json').read_bytes())
    for name,meta in r['source_members'].items():
        raw=(a.originals/name).read_bytes();assert len(raw)==meta['bytes'] and digest(raw)==meta['sha256']
    for name,key,selector,value in [('npc/genout/shop_m.create','selected_create',b'enemy',b'npcgen_shop|file:genout/ss_1001_17_13'),('npc/genout/npcgen.template','selected_template',b'templatename',b'npcgen_shop')]:
        raw=(a.originals/name).read_bytes();groups=source_blocks(raw);selected=[g for g in groups if g['fields'].get(selector)==value];assert len(selected)==1;g=selected[0];old=r[key];assert (g['start'],g['end'],digest(raw[g['start']:g['end']]))==(old['byte_start'],old['byte_end'],old['block_sha256'])
    raw=(folder/'private-npc-5863.rd').read_bytes();assert digest(raw)==r['candidate_graphic']['RD_sha256'];w,h,indices=decode(raw);assert digest(indices)==r['candidate_graphic']['index_pixels_sha256']
    sap=(folder/'private-palette.sap').read_bytes();pal={i+16:tuple(sap[i*3:i*3+3][::-1]) for i in range(224)};pal[0]=(0,0,0);pal[168]=(0,0,0)
    rgba=bytes(v for y in range(h-1,-1,-1) for n in indices[y*w:(y+1)*w] for v in (*pal[n],0 if n==0 else 255));assert digest(rgba)==r['candidate_graphic']['candidate_RGBA_sha256']
    npc=Image.open(io.BytesIO(base64.b64decode(pack['npc_image']))).convert('RGBA');assert npc.tobytes()==rgba
    room=pack['room'];maps={int(n):Image.open(io.BytesIO(base64.b64decode(v))).convert('RGBA') for n,v in room['sprites'].items()};result=[]
    for label,show,anchor in [('default',True,True),('npc_hidden',False,True),('anchor_hidden',True,False),('map_only',False,False)]:
        c=Image.new('RGBA',(960,720),'#11232a')
        def paste(im,x,y):c.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(480+2*(x-128),360+2*(y+80)))
        for no in room['R6_native_sorted_queue_numbers']:
            v=room['placements'][no];paste(maps[v['map_id']],v['draw_x'],v['draw_y'])
        if anchor:
            d=ImageDraw.Draw(c);d.rectangle((472,328,489,329),fill='#f0c979');d.rectangle((480,320,481,337),fill='#f0c979')
        if show:paste(npc,128+r['candidate_graphic']['xoff'],-96+r['candidate_graphic']['yoff'])
        h=digest(c.tobytes());assert h==next(x['canvas_sha256'] for x in actual['frames'] if x['label']==label);result.append({'label':label,'canvas_sha256':h})
    print(json.dumps({'independent_config_spans_match':2,'independent_source_members':5,'independent_NPC_RD_index_RGBA_PNG_match':True,'integer_scale_frames':result,'fractional_scale_not_verified_by_this_replay':True,'original_world_entered':False}))
if __name__=='__main__':main()
