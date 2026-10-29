"""Retained native-frame audit and correction of an already-completed NEXT.

Original PNGs stay private. Public mode joins immutable raw runtime, later visual
review and subsequent primary-surface evidence; raw false is not 'never viewed'.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE32-RETAINED-NATIVE-FRAMES-R1.json'
BASE='research/recovered/'
PINS={
 'STONEAGE-P3H-WINDOWS-ACTUAL-R1.json':'d4417e3b4f415ff18fc816bcd556311da4ca44885e62ab03746c027c6c5615ea',
 'STONEAGE-P3H-VISUAL-REVIEW-R1.json':'5f279c2d4b931e2caa02beab87c31fa85bdb420e3554e89876895ecf9bcea050',
 'STONEAGE-P3I-PRIMARY-ACTUAL-R1.json':'1272e5639907ab5687475ed8a57082737d1aa2d2f5fac459b0f93e9a01fe7bd8',
}
ZIP_SHA='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
PRIVATE_REPORT_SHA='d5b2ddbc82512f72531f46a6277cb8f1d064533055002779bcd0a0f1b4a453df'

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def sources():
    result={}
    for name,pin in PINS.items():
        raw=(ROOT/BASE/name).read_bytes();need(sha(raw)==pin,'pinned historical evidence: '+name)
        result[name]=json.loads(raw)
    return result

def join_evidence(raw,review,primary):
    obs=raw['runtime']['observations']
    need(len(obs)==len(review['frames'])==3,'complete frame occurrences')
    need(all(o['frame']['assistant_viewed_original'] is False for o in obs),'preserve raw report flags')
    need(review['assistant_directly_viewed_frame_indices']==[0,1] and
         review['third_frame_identical_to_directly_viewed_first'] is True,'existing later visual witness')
    need(review['source_report_sha256']==PINS['STONEAGE-P3H-WINDOWS-ACTUAL-R1.json'],'review source link')
    need(review['visible_game_picture_verified'] is False and review['original_world_entered'] is False,
         'black display is not game entry')
    for i,o in enumerate(obs):
        for key in ('png_sha256','rgb_sha256'):
            need(o['frame'][key]==review['frames'][i][key],'frame occurrence identity')
    need(obs[0]['frame']['png_sha256']==obs[2]['frame']['png_sha256'],'retained duplicate frame')
    need(primary['assessment']=='PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED','primary attribution boundary')
    need(primary['probe']['primary_lock_hr']=='0x00000000' and
         primary['probe']['original_private_surface_read'] is False and primary['probe']['palette_read'] is False,
         'global primary is not original private backbuffer')
    need(primary['original_run']['original_world_entered'] is False,'no native-world promotion')
    return dict(schema='stoneage.scene32.retained_native_frame_review.r1',
        source_evidence=[dict(path=BASE+n,sha256=h)for n,h in PINS.items()],
        raw_report_viewed_flags=[False]*3,prior_visual_witness_frame_indices=[0,1],
        prior_review_date=review['recorded_on'],frame_occurrences=review['frames'],
        distinct_original_pngs=2,duplicate_original_frame_groups=[[0,2],[1]],
        raw_false_does_not_override_later_review=True,
        scene31_next_assumed_unseen_in_error=True,previous_visual_task_already_satisfied=True,
        new_original_images_discovered=0,new_original_process_executions=0,new_historical_world_content=0,
        old_primary_surface=dict(assessment=primary['assessment'],bpp=primary['probe']['surface_bpp'],
            original_private_surface_read=False,game_pixels_attributed=False),
        p3i_reopening_authorized_by_these_same_images=False,
        original_world_entered=False,overall_percent=None,
        next='SCENE33-WORLD-ENTRY-SOURCE-PAIR-FEASIBILITY')

def derive():
    s=sources()
    return join_evidence(s['STONEAGE-P3H-WINDOWS-ACTUAL-R1.json'],s['STONEAGE-P3H-VISUAL-REVIEW-R1.json'],s['STONEAGE-P3I-PRIMARY-ACTUAL-R1.json'])

def decode_rgb_png(raw):
    """Bounded standard-library RGB8 PNG reader, independent of Pillow."""
    need(raw[:8]==b'\x89PNG\r\n\x1a\n','PNG signature');pos=8;parts=[];header=None;end=False
    while pos<len(raw):
        need(pos+12<=len(raw),'PNG chunk extent')
        n=struct.unpack_from('>I',raw,pos)[0];kind=raw[pos+4:pos+8];data=raw[pos+8:pos+8+n]
        need(pos+12+n<=len(raw),'PNG chunk payload extent')
        need(zlib.crc32(kind+data)&0xffffffff==struct.unpack_from('>I',raw,pos+8+n)[0],'PNG chunk CRC')
        if kind==b'IHDR':
            need(header is None and pos==8 and n==13,'unique initial IHDR')
            w,h,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',data)
            need(0<w<=640 and 0<h<=480 and (depth,color,compression,filtering,interlace)==(8,2,0,0,0),'bounded RGB8 noninterlaced PNG')
            header=(w,h)
        elif kind==b'IDAT':parts.append(data)
        elif kind==b'IEND':
            need(n==0 and pos+n+12==len(raw),'terminal IEND');end=True
        pos+=n+12
    need(header is not None and parts and end,'complete RGB PNG')
    w,h=header;stride=w*3;expected=(stride+1)*h;decoder=zlib.decompressobj()
    scan=decoder.decompress(b''.join(parts),expected+1)
    need(len(scan)==expected and decoder.eof and not decoder.unused_data,'PNG decompressed extent')
    output=bytearray();previous=bytearray(stride)
    for y in range(h):
        start=y*(stride+1);filter_type=scan[start];row=bytearray(scan[start+1:start+1+stride])
        need(filter_type<=4,'PNG row filter')
        for x in range(stride):
            left=row[x-3]if x>=3 else 0;up=previous[x];corner=previous[x-3]if x>=3 else 0
            if filter_type==1:pred=left
            elif filter_type==2:pred=up
            elif filter_type==3:pred=(left+up)//2
            elif filter_type==4:
                p=left+up-corner;dist=(abs(p-left),abs(p-up),abs(p-corner));pred=(left,up,corner)[dist.index(min(dist))]
            else:pred=0
            row[x]=(row[x]+pred)&255
        output.extend(row);previous=row
    return w,h,bytes(output)

def pixel_metrics(w,h,rgb):
    need(len(rgb)==w*h*3,'RGB pixel extent')
    colors=Counter(zip(rgb[::3],rgb[1::3],rgb[2::3]));points=[]
    for i in range(w*h):
        if rgb[3*i:3*i+3]!=b'\0\0\0':points.append((i%w,i//w))
    bbox=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1]if points else None
    return dict(rgb_sha256=sha(rgb),black_pixels=colors.get((0,0,0),0),nonblack_pixels=len(points),nonblack_bbox=bbox,colors=len(colors))

def private_audit(path):
    from PIL import Image
    import io
    with path.open('rb')as f:need(hashlib.file_digest(f,'sha256').hexdigest()==ZIP_SHA,'entire original retained package')
    old=sources();raw=old['STONEAGE-P3H-WINDOWS-ACTUAL-R1.json'];review=old['STONEAGE-P3H-VISUAL-REVIEW-R1.json'];frames=[]
    with zipfile.ZipFile(path)as z:
        private_raw=z.read('private-source-report.json');need(sha(private_raw)==PRIVATE_REPORT_SHA,'private source report')
        original=json.loads(private_raw);need(all(original[k]==raw[k]for k in original),'private/public source report unchanged shared fields')
        for i in range(3):
            png=z.read(f'frames/original-frame-{i}.png');need(sha(png)==review['frames'][i]['png_sha256'],'retained original PNG identity')
            w,h,rgb=decode_rgb_png(png);need((w,h)==(640,480),'original client frame size')
            with Image.open(io.BytesIO(png))as im:need(im.convert('RGB').tobytes()==rgb,'independent Pillow/standard-library RGB decode')
            m=pixel_metrics(w,h,rgb);need(m=={k:v for k,v in review['frames'][i].items()if k not in ('index','png_sha256')},'existing review exact pixel metrics')
            frames.append(dict(index=i,png_bytes=len(png),png_sha256=sha(png),**m))
    return dict(schema='stoneage.scene32.private_frame_byte_audit.r1',parent_zip_sha256=ZIP_SHA,
        private_source_report_sha256=PRIVATE_REPORT_SHA,private_source_report_bytes=len(private_raw),
        all_private_report_shared_fields_equal_public=True,standard_library_and_Pillow_full_rgb_agree=True,
        frames=frames,preserves_all_three_occurrences_and_duplicate=True,new_original_images_discovered=0,
        original_process_executed_in_this_package=False,original_world_entered=False)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');ap.add_argument('--original-zip',type=Path);args=ap.parse_args()
    r=derive()
    if args.write:REPORT.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    else:need(json.loads(REPORT.read_text())==r,'published continuity join differs')
    print(json.dumps(private_audit(args.original_zip)if args.original_zip else {'continuity_join':'PASS','new_images':0,'prior_visual_review_preserved':True}))

if __name__=='__main__':main()
