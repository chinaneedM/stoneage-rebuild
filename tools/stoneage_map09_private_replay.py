"""Standalone verifier for the private MAP09 directory; requires Pillow and NumPy."""
import base64
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import zipfile

import numpy as np
from PIL import Image


def sha(raw): return hashlib.sha256(raw).hexdigest()


def verify(root):
    script=(root/'dataset.js').read_text()
    assert script.startswith('window.MAP09_DATA=') and script.endswith(';\n')
    model=json.loads(script[len('window.MAP09_DATA='):-2])
    report=json.loads((root/'scene-source-receipt.json').read_bytes())
    assert len(model['maps'])==len(report['maps'])==691
    sources=json.loads((root/'private-image-source-records.json').read_bytes())
    assert sha((root/'private-image-source-records.json').read_bytes())==report['private_image_source_records_sha256']
    archive=(root/'source-all-955-original-DAT.zip').read_bytes()
    assert sha(archive)==report['original_DAT_archive']['sha256']
    original=zipfile.ZipFile(io.BytesIO(archive));assert original.testzip() is None and len(original.namelist())==955
    images={}
    for key,row in sources.items():
        raw=(root/f'tiles/{key}.png').read_bytes();assert sha(raw)==row['candidate_PNG_sha256']
        with Image.open(io.BytesIO(raw)) as im: pixels=np.array(im.convert('RGBA'))
        assert sha(memoryview(pixels))==row['candidate_RGBA_sha256']
        assert set(np.unique(pixels[:,:,3]))<={0,255};images[int(key)]=pixels
    states=0
    for i,(floor,entry) in enumerate(model['maps'].items(),1):
        raw=base64.b64decode(entry['dat_base64']);assert raw==original.read(floor+'.dat')
        assert sha(raw)==report['maps'][floor]['source_sha256']
        w,h=struct.unpack_from('<II',raw);assert [w,h]==entry['geometry'] and len(raw)==8+6*w*h
        positions=[]
        for plane in (0,1):
            for diagonal in range(1-h,w):
                for x in range(w-1,-1,-1):
                    y=x-diagonal
                    if 0<=y<h:
                        start=8+2*(plane*w*h+y*w+x);key=int.from_bytes(raw[start:start+2],'little')
                        if key>99: positions.append((plane,x,y,key))
        assert len(positions)==entry['draw_positions']
        width,height=entry['canvas_size'];ox,oy=entry['origin']
        for mode in ('plane0','plane1','combined'):
            canvas=np.empty((height,width,4),dtype=np.uint8);canvas[:]=[17,35,42,255]
            for plane,x,y,key in positions:
                if (mode=='plane0' and plane==1) or (mode=='plane1' and plane==0): continue
                row=model['records'][str(key)];pixels=images[key];hh,ww=pixels.shape[:2]
                left=ox+(x+y)*32+row['xoff'];top=oy+(y-x)*24+row['yoff']
                assert 0<=left<=width-ww and 0<=top<=height-hh
                dest=canvas[top:top+hh,left:left+ww];mask=pixels[:,:,3]==255;dest[mask]=pixels[mask]
            digest=sha(memoryview(canvas))
            assert digest==entry['frame_RGBA_sha256'][mode]==report['maps'][floor]['frame_RGBA_sha256'][mode]
            del canvas;states+=1
        if i%50==0: print(json.dumps({'replayed_maps':i}),flush=True)
    return {'maps':691,'images':len(images),'complete_canvas_states':states,'all_equal':True,
            'original_client_executed':False,'actual_original_assets_browser_executed':False}


if __name__=='__main__': print(json.dumps(verify(Path(sys.argv[1]))),flush=True)
