"""Independent private RD/color/full-frame canvas verification, no browser or EXE."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile
from PIL import Image
from tools.stoneage_scene14_independent_replay import decode

def sha(b): return hashlib.sha256(b).hexdigest()

def replay(folder, original_zip):
    root=Path(__file__).resolve().parents[1]
    assert root not in folder.resolve().parents and folder.resolve()!=root
    r=json.loads((folder/'source-derived-report.json').read_bytes())
    html=(folder/'SCENE31-original-TW1-actor-observer.html').read_bytes()
    model=json.loads(html.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0])
    assert model['report']==r
    with original_zip.open('rb')as f: assert hashlib.file_digest(f,'sha256').hexdigest()==r['source_parent_zip_sha256']
    # Independent full group parser, without production selectors or metadata tables.
    with zipfile.ZipFile(original_zip)as original:
        idx=original.read('source/data/spradrn_1.bin');spr=original.read('source/data/spr_1.bin')
        assert sha(idx)==r['source_files']['spradrn_1.bin']['sha256'] and sha(spr)==r['source_files']['spr_1.bin']['sha256']
        no,start,count,reserved=struct.unpack_from('<IIHH',idx,0)
        assert no==100000 and start==0 and count==104
        parsed={};pos=start
        for ai in range(count):
            h=pos;direction,action,duration,n=struct.unpack_from('<HHII',spr,pos);pos+=12
            frames=[list(struct.unpack_from('<IhhH',spr,pos+i*10))for i in range(n)];pos+=n*10
            if action==2:
                assert direction not in parsed
                parsed[direction]=dict(frames=frames,sha256=sha(spr[h:pos]),duration=duration)
        assert pos==6128 and len(parsed)==8
        for a in r['sequences']:
            p=parsed[a['direction']];assert p['frames']==a['frames'] and p['sha256']==a['source_animation_span_sha256'] and p['duration']==a['duration_word']
    frames=[];images={};indices_count=0
    with zipfile.ZipFile(folder/'private-original-RD-and-palettes.zip')as z:
        assert len(z.namelist())==50 and len(set(z.namelist()))==50
        for palette in ('0','1'):
            sap=z.read('Palet_'+palette+'.sap');assert sha(sap)==r['source_files']['Palet_'+palette+'.sap']['sha256']
            colors={n+16:tuple(sap[n*3:n*3+3][::-1])for n in range(224)};colors[0]=(0,0,0);colors[168]=(0,0,0)
            for b in r['bitmaps']:
                raw=z.read(str(b['bitmapno'])+'.rd');assert sha(raw)==b['RD_sha256']
                w,h,px=decode(raw);assert (w,h)==(b['width'],b['height']) and sha(px)==b['indices_sha256']
                assert all(n in colors for n in px)
                rgba=bytes(c for y in range(h-1,-1,-1)for n in px[y*w:(y+1)*w]for c in (*colors[n],0 if n==0 else 255))
                old=b['palette_candidates'][palette];assert sha(rgba)==old['RGBA_sha256']
                png=base64.b64decode(model['images'][palette][str(b['bitmapno'])],validate=True);assert sha(png)==old['PNG_sha256']
                im=Image.open(io.BytesIO(png)).convert('RGBA');assert im.tobytes()==rgba
                images[(palette,b['bitmapno'])]=im
                if palette=='0':indices_count+=len(px)
        rows={b['bitmapno']:b for b in r['bitmaps']}
        for palette in ('0','1'):
            for a in r['sequences']:
                for fi,(no,x,y,sound) in enumerate(a['frames']):
                    b=rows[no];im=images[(palette,no)];c=Image.new('RGBA',(240,260),(20,33,41,255))
                    c.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(120+2*(b['xoff']+x),200+2*(b['yoff']+y)))
                    row=dict(palette=palette,direction=a['direction'],frame_index=fi,bitmapno=no,RGBA_sha256=sha(c.tobytes()))
                    assert row==next(v for v in model['canvas_hashes']if v['palette']==palette and v['direction']==a['direction'] and v['frame_index']==fi)
                    frames.append(row)
    result=dict(schema='stoneage.scene31.independent_actual_pixel_replay.r1',source_report_sha256=sha((folder/'source-derived-report.json').read_bytes()),
        independently_parsed_original_sequences=8,original_frame_positions=48,original_RD_blocks=48,original_indices_compared=indices_count,
        RGBA_and_PNG_comparisons=96,full_canvas_comparisons=96,all_source_sequence_index_RGBA_PNG_canvas_checks_equal=True,
        original_source_browser_verified=False,original_executable_executed=False,original_world_entered=False,frames=frames)
    (folder/'independent-original-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);p.add_argument('--original-zip',type=Path,required=True);a=p.parse_args()
    print(json.dumps({k:v for k,v in replay(a.private_dir,a.original_zip).items()if k!='frames'}))
