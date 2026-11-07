"""Synthetic three-map fixture for the same private observer; no historical pixels."""
import argparse
import base64
import json
from pathlib import Path
import shutil
import struct

from tools.stoneage_map09_batch_scenes import placements, verified_frames, sha, ROOT


def create(out):
    import numpy as np
    from PIL import Image
    out.mkdir(parents=True,exist_ok=False);(out/'tiles').mkdir()
    images={100:Image.new('RGBA',(7,9),(220,35,25,255)),
            101:Image.new('RGBA',(11,5),(25,190,75,255)),
            102:Image.new('RGBA',(8,12),(45,85,210,255))}
    images[102].putpixel((0,0),(240,20,20,0))
    records={100:{'xoff':-3,'yoff':-7,'width':7,'height':9},
             101:{'xoff':-8,'yoff':-2,'width':11,'height':5},
             102:{'xoff':-4,'yoff':-10,'width':8,'height':12}}
    arrays={key:np.array(im) for key,im in images.items()}
    for key,im in images.items(): im.save(out/f'tiles/{key}.png')
    model={'synthetic_fixture':True,'maps':{},'records':records,'source_ready_maps':3}
    planes={
        '100':[[100,100,1,99,101,0],[0,102,0,101,0,102],[9,8,7,6,5,4]],
        '200':[[101,0,100,0,101,100],[102,0,0,102,0,0],[1,1,1,1,1,1]],
        '300':[[0,0,99,1,0,0],[0,0,0,0,0,0],[102,102,102,102,102,102]],
    }
    for floor,parts in planes.items():
        raw=struct.pack('<II',2,3)+b''.join(struct.pack('<6H',*part) for part in parts)
        info,selected=placements(raw)
        size,origin,hashes,thumb=verified_frames(raw,info,selected,images,records,arrays)
        model['maps'][floor]={'dat_base64':base64.b64encode(raw).decode(),
            'source_sha256':sha(raw),'geometry':[2,3],'canvas_size':size,'origin':origin,
            'draw_positions':len(selected),'low_nonzero_not_rendered':info['source_low_nonzero_not_rendered'],
            'unique_draw_aliases':len({p['image_key'] for p in selected}),'frame_RGBA_sha256':hashes}
    (out/'dataset.js').write_text('window.MAP09_DATA='+json.dumps(model)+';\n')
    shutil.copyfile(ROOT/'tools/stoneage_map09_viewer.html',out/'MAP09.html')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);create(p.parse_args().out)
