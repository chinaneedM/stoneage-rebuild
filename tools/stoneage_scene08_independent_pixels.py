"""Independently verify private pet RD/PNG bytes, original SPR and canvas."""
import argparse,base64,io,json,struct,zipfile
from pathlib import Path
from PIL import Image,ImageDraw
from tools.stoneage_scene07_independent_pixels import independent_rd,sha

def verify(directory,source):
    directory=Path(directory);source=Path(source)
    text=(directory/'stoneage-room-r8-pet-observer.html').read_text()
    pack=json.loads(text.split('<script id="evidence" type="application/json">')[1].split('</script>')[0]);r=pack['pet_evidence']
    spr=(source/'spr_4.bin').read_bytes();palette=(source/'Palet_1.sap').read_bytes()
    if sha(spr)!=r['source_files']['spr_4.bin']['sha256'] or sha(palette)!=r['source_files']['Palet_1.sap']['sha256']:raise ValueError('full original SPR/palette identity')
    selected=0
    for g in pack['actors']['groups']:
        if sha(spr[g['offset']:g['end_offset']])!=g['whole_group_segment_sha256']:raise ValueError('whole original SPR group')
        for a in g['animations']:
            raw=struct.pack('<HHII',a['direction'],a['action'],a['duration_word'],len(a['frames']))+b''.join(struct.pack('<IhhH',*f) for f in a['frames'])
            if raw!=spr[a['header_offset']:a['end_offset']] or sha(raw)!=a['source_animation_span_sha256']:raise ValueError('all original selected SPR frames')
            selected+=1
    colors={i+16:tuple(palette[i*3:i*3+3][::-1]) for i in range(224)};colors[0]=(0,0,0);colors[168]=(0,0,0)
    decoded=0
    with zipfile.ZipFile(directory/'private-source-rd-subset.zip') as z:
        if set(z.namelist())!={str(b['bitmapno'])+'.rd' for b in pack['actors']['bitmaps']}:raise ValueError('complete private RD source subset')
        for b in pack['actors']['bitmaps']:
            raw=z.read(str(b['bitmapno'])+'.rd')
            if sha(raw)!=b['RD_sha256'] or len(raw)!=b['size']:raise ValueError('original RD block identity')
            w,h,indices=independent_rd(raw)
            if (w,h)!=(b['width'],b['height']) or sha(indices)!=b['index_pixels_sha256']:raise ValueError('independent original index pixels')
            rgba=bytes(c for y in reversed(range(h)) for n in indices[y*w:(y+1)*w] for c in (*colors[n],0 if n==0 else 255))
            if sha(rgba)!=b['candidate_RGBA_sha256']:raise ValueError('independent color-row/key candidate')
            png=base64.b64decode(pack['actor_images'][str(b['bitmapno'])],validate=True)
            with Image.open(io.BytesIO(png)) as im:
                if im.convert('RGBA').tobytes()!=rgba:raise ValueError('private PNG versus actual original index pixels')
            decoded+=1
    result={'schema':'stoneage.scene08.independent_pixels.r1','raw_RD_blocks':decoded,
        'selected_SPR_spans_byte_exact':selected,'all_index_and_png_rgba_equal':True,
        'source_RD_zip_sha256':sha((directory/'private-source-rd-subset.zip').read_bytes()),
        'original_world_entered':False,'official_species_identity_authenticated':False}
    canvas=directory/'browser/internal-canvas-rgba.bin'
    if canvas.exists():
        # Browser checker ends with direction0/action2/frame0, default pet100250,
        # the human reference visible, scale3 and a reset modern camera.
        bg=Image.new('RGBA',(960,720),(17,35,42,255))
        def stamp(encoded,x,y):
            im=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA')
            im=im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST)
            bg.alpha_composite(im,(210+x*3,420+y*3))
        for i in pack['room']['R6_native_sorted_queue_numbers']:
            b=pack['room']['placements'][i];stamp(pack['room']['sprites'][str(b['map_id'])],b['draw_x'],b['draw_y'])
        x,y=210+128*3,420;draw=ImageDraw.Draw(bg)
        draw.rectangle((x-12,y,x+14,y+2),fill=(224,182,110,255));draw.rectangle((x,y-12,x+2,y+14),fill=(224,182,110,255))
        for i,g in enumerate([pack['actors']['groups'][0],pack['actors']['groups'][1]]):
            a=next(a for a in g['animations'] if a['direction']==0 and a['action']==2);f=a['frames'][0]
            b=next(b for b in pack['actors']['bitmaps'] if b['bitmapno']==f[0])
            stamp(pack['actor_images'][str(f[0])],128+i*32+f[1]+b['xoff'],i*24+f[2]+b['yoff'])
        actual=canvas.read_bytes();expected=bg.tobytes()
        if actual!=expected:raise ValueError('independent Pillow/browser canvas pixels differ')
        result.update(canvas_pixels_compared=960*720,canvas_RGBA_sha256=sha(actual),canvas_all_pixels_identical=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('source',type=Path);p.add_argument('report',type=Path);a=p.parse_args();r=verify(a.directory,a.source);a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
