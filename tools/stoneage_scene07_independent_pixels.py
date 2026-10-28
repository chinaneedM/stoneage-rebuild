"""Independent PRIVATE RD/PNG and selected raw-SPR checks, no original client.

The decoder below deliberately does not call stoneage_rd_codec. The report
contains only source identities/counts/digests; never raw images or RD bytes.
"""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile
from PIL import Image

def sha(b):return hashlib.sha256(b).hexdigest()

def independent_rd(raw):
    if len(raw)<16 or raw[:2]!=b'RD':raise ValueError('RD identity')
    w,h=struct.unpack_from('<ii',raw,4)
    if not 0<w*h<=1000000 or w<=0 or h<=0:raise ValueError('pixel budget')
    data=raw[16:];out=bytearray();p=0
    if raw[2]==0:
        if len(data)!=w*h:raise ValueError('raw image extent')
        return w,h,data
    if raw[2]!=1:raise ValueError('unsupported original RD flag')
    while p<len(data):
        control=data[p];p+=1;family=control>>4
        if family not in (0,1,2,8,9,10,12,13,14):raise ValueError('RLE family')
        kind=family//4;extra=family%4
        value=None
        if kind==2:
            if p>=len(data):raise ValueError('short repeated value')
            value=data[p];p+=1
        if p+extra>len(data):raise ValueError('short count')
        count=control&15
        for n in data[p:p+extra]:count=count*256+n
        p+=extra
        if kind==0:
            if p+count>len(data):raise ValueError('short literal')
            out.extend(data[p:p+count]);p+=count
        elif kind==2:
            out.extend(bytes([value])*count)
        else:out.extend(bytes(count))
        if len(out)>w*h:raise ValueError('pixel overflow')
    if len(out)!=w*h:raise ValueError('pixel underflow')
    return w,h,bytes(out)

def verify(directory,source):
    directory=Path(directory);source=Path(source)
    text=(directory/'stoneage-room-r7-actor-observer.html').read_text()
    pack=json.loads(text.split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
    report=pack['actors'];spr=(source/'spr_4.bin').read_bytes()
    if sha(spr)!=report['source_files']['spr_4.bin']['sha256']:raise ValueError('full SPR digest')
    animations=0
    for g in report['groups']:
        if sha(spr[g['offset']:g['end_offset']])!=g['whole_group_segment_sha256']:raise ValueError('full group SHA')
        for a in g['animations']:
            raw=struct.pack('<HHII',a['direction'],a['action'],a['duration_word'],len(a['frames']))+b''.join(struct.pack('<IhhH',*f) for f in a['frames'])
            if raw!=spr[a['header_offset']:a['end_offset']] or sha(raw)!=a['source_animation_span_sha256']:raise ValueError('selected SPR exact byte replay')
            animations+=1
    palette=(source/'Palet_1.sap').read_bytes()
    if sha(palette)!=report['source_files']['Palet_1.sap']['sha256']:raise ValueError('palette digest')
    # Use only directly sourced 16..239 slots, plus transparent key0. Do not
    # fill reserved colors using the TW1 initializer's unrelated constants.
    colors={16+i:tuple(palette[i*3:i*3+3][::-1]) for i in range(224)}
    colors[168]=(0,0,0);colors[0]=(0,0,0)
    decoded=0
    with zipfile.ZipFile(directory/'private-source-rd-subset.zip') as z:
        if set(z.namelist())!={str(r['bitmapno'])+'.rd' for r in report['bitmaps']}:raise ValueError('RD subset completeness')
        for r in report['bitmaps']:
            raw=z.read(str(r['bitmapno'])+'.rd')
            if len(raw)!=r['size'] or sha(raw)!=r['RD_sha256']:raise ValueError('source raw RD digest')
            w,h,pixels=independent_rd(raw)
            if (w,h)!=(r['width'],r['height']) or sha(pixels)!=r['index_pixels_sha256']:raise ValueError('independent index pixels')
            rgba=bytes(c for y in reversed(range(h)) for n in pixels[y*w:(y+1)*w] for c in (*colors[n],0 if n==0 else 255))
            if sha(rgba)!=r['candidate_RGBA_sha256']:raise ValueError('independent RGB row/key candidate')
            png=base64.b64decode(pack['actor_images'][str(r['bitmapno'])],validate=True)
            with Image.open(io.BytesIO(png)) as image:
                if image.convert('RGBA').tobytes()!=rgba:raise ValueError('Pillow PNG pixels differ')
            decoded+=1
    return {'schema':'stoneage.scene07.independent_pixels.r1','raw_RD_blocks':decoded,
        'independent_index_pixels_and_png_rgba_match':True,'selected_SPR_spans_byte_exact':animations,
        'source_RD_zip_sha256':sha((directory/'private-source-rd-subset.zip').read_bytes()),
        'original_world_entered':False,'historical_palette_or_occlusion_verified':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('source',type=Path);p.add_argument('report',type=Path);a=p.parse_args()
    r=verify(a.directory,a.source);a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
