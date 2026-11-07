"""Private source-ready map catalogue; reused extraction, independent full-frame replay."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import zipfile

from tools.stoneage_map06_two_original_scenes import META, TILES, placements, source_images, sha, need
from tools.stoneage_map08_private_dat_batch import pinned

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
SOURCE_ZIP = (1988312, 'c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a')


def ready_names(index):
    cols = index['per_floor_source_row_columns']
    rows = [dict(zip(cols, row)) for row in index['per_floor_source_rows']]
    return {r['original_DAT_file_basename']: r for r in rows
            if r['number_of_nonzero_positions_missing_source_qualified_TW1_RD'] == 0}


def independent_positions(raw):
    """Separate byte addressing/diagonal traversal, without placements()/unpack arrays."""
    w, h = struct.unpack_from('<II', raw)
    found = []
    for plane, label in ((0, 'tile'), (1, 'parts')):
        for diagonal in range(1-h, w):
            for x in range(w-1, -1, -1):
                y = x-diagonal
                if not 0 <= y < h: continue
                start = 8+2*(plane*w*h+y*w+x)
                key = int.from_bytes(raw[start:start+2], 'little')
                if key > 99:
                    found.append({'layer': label, 'xy': [x,y], 'image_key': key,
                                  'anchor': [(x+y)*32, (y-x)*24]})
    return found


def bounds(info, selected, records):
    rects = [(p['anchor'][0]+records[p['image_key']]['xoff'],
              p['anchor'][1]+records[p['image_key']]['yoff'],
              records[p['image_key']]['width'], records[p['image_key']]['height']) for p in selected]
    w,h = info['width'],info['height']
    rects.extend(((x+y)*32,(y-x)*24,1,1) for x,y in ((0,0),(w-1,0),(0,h-1),(w-1,h-1)))
    left,top = min(r[0] for r in rects)-16,min(r[1] for r in rects)-16
    right,bottom = max(r[0]+r[2] for r in rects)+16,max(r[1]+r[3] for r in rects)+16
    return [right-left,bottom-top],[-left,-top]


def verified_frames(raw, info, selected, images, records, arrays):
    import numpy as np
    from PIL import Image
    from tools.stoneage_scene21_town1000 import render
    independent = independent_positions(raw)
    need(independent == selected, 'independent source-plane/diagonal traversal mismatch')
    size,origin = bounds(info,selected,records)
    hashes,thumb = {},None
    for mode in ('plane0','plane1','combined'):
        items = selected if mode != 'plane1' else [p for p in selected if p['layer']=='parts']
        primary = render(images,records,items,False,mode!='plane0',False,origin,size)
        # Independent byte-wise NumPy overwrite is valid only for verified binary alpha.
        canvas = np.empty((size[1],size[0],4),dtype=np.uint8)
        canvas[:] = [17,35,42,255]
        for p in independent:
            if mode=='plane0' and p['layer']=='parts': continue
            if mode=='plane1' and p['layer']=='tile': continue
            r=records[p['image_key']]; pixels=arrays[p['image_key']]
            x=origin[0]+p['anchor'][0]+r['xoff'];y=origin[1]+p['anchor'][1]+r['yoff']
            h,w=pixels.shape[:2]
            need(0<=x<=size[0]-w and 0<=y<=size[1]-h,'source tile outside candidate canvas')
            target=canvas[y:y+h,x:x+w];mask=pixels[:,:,3]==255;target[mask]=pixels[mask]
        first=hashlib.sha256(primary.tobytes()).hexdigest()
        second=hashlib.sha256(memoryview(canvas)).hexdigest()
        need(first==second,'independent complete RGBA canvas mismatch: '+mode)
        hashes[mode]=first
        if mode=='combined':
            thumb=primary.convert('RGB');thumb.thumbnail((480,360))
        del primary,canvas
    return size,origin,hashes,thumb


def export(dat_zip,tiles,out):
    import numpy as np
    from PIL import Image, ImageDraw
    need(not out.exists() and ROOT not in out.resolve().parents,'new private directory outside Git required')
    need((dat_zip.stat().st_size,sha(dat_zip.read_bytes()))==SOURCE_ZIP,'955 source ZIP identity')
    index=json.loads(META.read_bytes()); ready=ready_names(index);pins=pinned()
    need(len(ready)==691,'source-ready catalogue changed')
    maps,wanted={},set()
    with zipfile.ZipFile(dat_zip) as z:
        need(z.testzip() is None and set(z.namelist())==set(pins),'955 archive CRC/member inventory')
        for name in sorted(z.namelist(),key=lambda s:int(s[:-4])):
            raw=z.read(name);need((len(raw),sha(raw))==pins[name],'source DAT identity: '+name)
            if name not in ready: continue
            info,selected=placements(raw);maps[name[:-4]]=(raw,info,selected)
            wanted.update(p['image_key'] for p in selected)
    images,records,public_images=source_images(tiles,wanted)
    arrays={key:np.array(im) for key,im in images.items()}
    need(all(set(np.unique(a[:,:,3]))<={0,255} for a in arrays.values()),'nonbinary original candidate alpha')
    out.mkdir();(out/'tiles').mkdir();(out/'thumbnails').mkdir()
    with zipfile.ZipFile(tiles) as z:
        for key in sorted(wanted):
            (out/f'tiles/{key}.png').write_bytes(z.read(f'original-TW1-Palet1-candidate/alias-{key:05d}.png'))
    shutil.copyfile(dat_zip,out/'source-all-955-original-DAT.zip')
    (out/'private-image-source-records.json').write_text(json.dumps(public_images,sort_keys=True))
    report={'schema':'stoneage.map09.691_source_ready_scenes.r1',
        'source_scope':'MIXED25_ORIGINAL_DAT_AND_TW10_ORIGINAL_RD_SEPARATE_SOURCES',
        'source_main':'a9d9ed742c0242a75d6523d243e3701b195fe34e',
        'original_DAT_archive':{'bytes':SOURCE_ZIP[0],'sha256':SOURCE_ZIP[1],'members':955},
        'original_pixel_archive':{'bytes':TILES[0],'sha256':TILES[1]},
        'qualified_image_aliases':sorted(wanted),
        'private_image_source_records_sha256':sha((out/'private-image-source-records.json').read_bytes()),
        'maps':{},'boundaries':{k:False for k in ('original_client_executed','official_same_deployment_verified',
            'native_palette_verified','native_layer_order_verified','native_collision_verified','actual_original_assets_browser_executed','raw_originals_in_public_git')},
        'stage_A':'7_PARTIAL_2_OPEN','stage_B':'GATED','wiki':'GATED','overall_percent':None,
        'new_original_RD_decodes':0}
    model={'maps':{},'records':{str(k):v for k,v in records.items()},'source_ready_maps':691}
    for no,(floor,(raw,info,selected)) in enumerate(maps.items(),1):
        size,origin,hashes,thumb=verified_frames(raw,info,selected,images,records,arrays)
        summary={'source_sha256':sha(raw),'source_bytes':len(raw),'geometry':[info['width'],info['height']],
                 'canvas_size':size,'origin':origin,'draw_positions':len(selected),
                 'low_nonzero_not_rendered':info['source_low_nonzero_not_rendered'],
                 'unique_draw_aliases':len({p['image_key'] for p in selected}),
                 'frame_RGBA_sha256':hashes,'independent_all_three_frames_equal':True}
        report['maps'][floor]=summary
        model['maps'][floor]={'dat_base64':base64.b64encode(raw).decode(),**summary}
        thumb.save(out/f'thumbnails/{floor}.jpg',quality=85)
        if no%25==0 or no==len(maps): print(json.dumps({'verified_maps':no,'total':len(maps)}),flush=True)
        # Keep a reproducible checkpoint while large maps are being processed.
        if no%50==0: (out/'progress.json').write_text(json.dumps({'completed_maps':no,'total':len(maps)}))
    (out/'dataset.js').write_text('window.MAP09_DATA='+json.dumps(model,separators=(',',':'))+';\n')
    (out/'scene-source-receipt.json').write_text(json.dumps(report,separators=(',',':'))+'\n')
    shutil.copyfile(ROOT/'tools/stoneage_map09_viewer.html',out/'MAP09.html')
    # Contact page deliberately samples 36 IDs; the catalogue contains all 691.
    ids=list(maps);chosen=[ids[i*(len(ids)-1)//35] for i in range(36)]
    contact=Image.new('RGB',(1800,1500),'#11232a');draw=ImageDraw.Draw(contact)
    for i,floor in enumerate(chosen):
        with Image.open(out/f'thumbnails/{floor}.jpg') as im:
            im.thumbnail((290,220));x=(i%6)*300;y=(i//6)*250
            contact.paste(im,(x+(300-im.width)//2,y+24));draw.text((x+8,y+5),'DAT '+floor,fill='white')
    contact.save(out.parent/'StoneAge-MAP09-691-scenes-contact.jpg',quality=90)
    (out/'progress.json').unlink(missing_ok=True)
    report['verified_maps']=len(maps);report['verified_full_canvas_states']=len(maps)*3
    report['qualified_images']=len(wanted)
    REPORT.write_text(json.dumps(report,separators=(',',':'))+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('dat_zip',type=Path);p.add_argument('tiles',type=Path);p.add_argument('private_directory',type=Path)
    a=p.parse_args();r=export(a.dat_zip,a.tiles,a.private_directory)
    print(json.dumps({'verified_maps':r['verified_maps'],'states':r['verified_full_canvas_states'],'images':r['qualified_images']}))
