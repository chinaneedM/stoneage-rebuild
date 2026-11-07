"""Private candidates from two pinned original DATs and archived TW1 RD PNGs."""
import argparse
import base64
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile
import zlib
from tools.stoneage_map06_private_dat_source import PINS
from tools.stoneage_tw85_map_payload import parse

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
REPORT=REC/'STONEAGE-MAP06-TWO-ORIGINAL-DAT-SCENE-CANDIDATES-R1.json'
TILES=(35673334,'e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37')
META=REC/'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
ADRN=REC/'tw10-resource-metadata/ADRN-R1.tsv.gz'


def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)

def placements(raw):
    info=parse(raw);w,h=info['width'],info['height'];n=w*h
    planes=[struct.unpack_from('<'+'H'*n,raw,8+i*2*n) for i in range(3)]
    order=sorted(((x,y) for y in range(h) for x in range(w)),key=lambda q:(q[0]-q[1],-q[0]))
    selected=[{'layer':label,'xy':[x,y],'image_key':planes[i][y*w+x],
               'anchor':[(x+y)*32,(y-x)*24]}
              for i,label in [(0,'tile'),(1,'parts')] for x,y in order if planes[i][y*w+x]>99]
    info['source_nonzero_first_two_planes']=sum(v!=0 for p in planes[:2] for v in p)
    info['modern_draw_candidate_positions']=len(selected)
    info['source_low_nonzero_not_rendered']=sum(0<v<=99 for p in planes[:2] for v in p)
    return info,selected


def source_images(tiles,wanted):
    from PIL import Image
    with tiles.open('rb') as f:need((tiles.stat().st_size,hashlib.file_digest(f,'sha256').hexdigest())==TILES,'pixel archive identity')
    catalog=json.loads(META.read_bytes());source_rows={r[0]:r for r in catalog['source_TW1_real_RD_rows']}
    need(wanted<=source_rows.keys(),'source alias not in qualified MAP04 batch')
    indices={source_rows[n][1] for n in wanted};headers={}
    with gzip.open(ADRN,'rt') as f:
        for row in csv.DictReader(f,delimiter='\t'):
            if int(row['index']) in indices:headers[int(row['index'])]=row
    images={};records={};public={}
    with zipfile.ZipFile(tiles) as z:
        need(len(z.namelist())==4169 and z.testzip() is None,'pixel archive member CRC')
        receipt=json.loads(z.read('private-pixel-source-receipts.json'))
        source={x['alias']:x for x in receipt['original_TW1_RD_4166_source_receipts']}
        for n in sorted(wanted):
            r=source[n];m=source_rows[n];h=headers[m[1]]
            need(r['original_RD_sha256']==m[5]==h['rd_block_sha256'] and r['original_RD_indexed_pixel_sha256']==m[6], 'original RD fingerprint mismatch')
            png=z.read(f'original-TW1-Palet1-candidate/alias-{n:05d}.png');need(sha(png)==r['candidate_PNG_sha256'],'original candidate PNG mismatch')
            im=Image.open(io.BytesIO(png)).convert('RGBA');need(sha(im.tobytes())==r['candidate_RGBA_sha256'],'original candidate RGBA mismatch')
            need(im.size==(m[2],m[3])==(int(h['width']),int(h['height'])),'source geometry mismatch')
            images[n]=im;records[n]={k:int(h[k]) for k in ['xoff','yoff','width','height']}
            public[str(n)]={**records[n],'source_adrn_index':m[1],'source_record_sha256':r['original_ADRN_record'],
                'source_RD_sha256':m[5],'source_index_pixels_sha256':m[6],
                'candidate_PNG_sha256':sha(png),'candidate_RGBA_sha256':sha(im.tobytes())}
    return images,records,public


def scene_frames(info,selected,images,records):
    from tools.stoneage_scene21_town1000 import render
    rects=[(p['anchor'][0]+records[p['image_key']]['xoff'],p['anchor'][1]+records[p['image_key']]['yoff'],
            records[p['image_key']]['width'],records[p['image_key']]['height']) for p in selected]
    w,h=info['width'],info['height']
    rects.extend(((x+y)*32,(y-x)*24,1,1) for x,y in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)])
    left=min(r[0] for r in rects)-16;top=min(r[1] for r in rects)-16
    right=max(r[0]+r[2] for r in rects)+16;bottom=max(r[1]+r[3] for r in rects)+16
    size=[right-left,bottom-top];origin=[-left,-top];frames={};pngs={}
    for name,items,parts in [('plane0',selected,False),('plane1',[p for p in selected if p['layer']=='parts'],True),('combined',selected,True)]:
        im=render(images,records,items,False,parts,False,origin,size)
        buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue();pngs[name]=png
        frames[name]={'candidate_RGBA_sha256':sha(im.tobytes()),'candidate_PNG_sha256':sha(png)}
    return {'canvas_size':size,'origin':origin,'frames':frames},pngs


def html_page(frames):
    model=json.dumps({name:'data:image/png;base64,'+base64.b64encode(png).decode() for name,png in frames.items()},separators=(',',':'))
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; script-src 'unsafe-inline'; style-src 'unsafe-inline'"><title>MAP06 原地图与原图块来源候选</title><style>body{background:#11232a;color:#e8eee9;font:16px system-ui;margin:24px}select{font:inherit;padding:8px}img{max-width:100%;image-rendering:pixelated}p{max-width:1000px}</style><h1>MAP06 原地图源场景候选</h1><p>社区混合2.5原DAT与台湾1.0原RD候选图；两来源不认证同一官方部署。分层、拼接次序、配色和透明处理只用于现代研究观察，没有原客户端、原生碰撞或互动验证。数字1–99原样保留在源数据中，未将它们直接绘成场景。解压前请保留完整ZIP作为私人来源资料。</p><label>原地图/候选层 <select id="view"></select></label><p id="label"></p><img id="scene" alt="原来源场景候选"><script>const D='''+model+''';const q=document.getElementById('view'),pic=document.getElementById('scene');q.replaceChildren(...Object.keys(D).map(k=>new Option(k,k)));function show(){pic.src=D[q.value];document.getElementById('label').textContent=q.value}q.onchange=show;show();</script></html>'''


def export(dat_dir,tiles,target):
    target=target.resolve();need(ROOT not in target.parents and not target.exists(),'new private output must be outside Git')
    maps={};all_ids=set()
    for name,pin in PINS.items():
        raw=(dat_dir/name).read_bytes();need((len(raw),sha(raw),f'{zlib.crc32(raw)&0xffffffff:08x}')==pin,'original DAT identity')
        info,selected=placements(raw);maps[name]=(raw,info,selected);all_ids|={p['image_key'] for p in selected}
    images,records,resources=source_images(tiles,all_ids)
    report={'schema':'stoneage.map06.two_original_dat_scene_candidates.r1','source_scope':'MIXED25_ORIGINAL_DAT_AND_TW10_ORIGINAL_RD_SEPARATE_SOURCES',
        'source_pixel_archive_bytes':TILES[0],'source_pixel_archive_sha256':TILES[1],
        'source_metadata_git_blobs':{str(p.relative_to(ROOT)):hashlib.sha1(b'blob '+str(len(p.read_bytes())).encode()+b'\0'+p.read_bytes()).hexdigest() for p in [META,ADRN]},
        'resources':resources,'maps':{},'boundaries':{k:False for k in ['original_client_executed','native_scene_rendering_verified',
            'official_same_deployment_verified','native_layer_order_verified','native_palette_verified','native_collision_verified','raw_originals_in_public_git']}}
    observer_frames={};private={}
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as out:
        for name,(raw,info,selected) in maps.items():
            floor=name[:-4];result,pngs=scene_frames(info,selected,images,records)
            report['maps'][floor]={'source_bytes':len(raw),'source_sha256':sha(raw),'source_crc32':f'{zlib.crc32(raw)&0xffffffff:08x}',
                'structure':info,'distinct_draw_candidate_aliases':len({p['image_key'] for p in selected}),**result}
            private[floor]={'placements':selected,'source_sha256':sha(raw),**result}
            out.writestr('source/'+name,raw)
            for mode,png in pngs.items():
                observer_frames[floor+'-'+mode]=png;out.writestr(f'{floor}-{mode}.png',png)
        out.writestr('MAP06.html',html_page(observer_frames))
        out.writestr('private-source-placements.json',json.dumps(private,sort_keys=True))
        with zipfile.ZipFile(tiles) as original_pngs:
            for n in sorted(all_ids):
                out.writestr(f'tiles/{n}.png',original_pngs.read(f'original-TW1-Palet1-candidate/alias-{n:05d}.png'))
    with zipfile.ZipFile(target) as z:need(z.testzip() is None,'private output CRC')
    with target.open('rb') as f:report['private_zip_sha256']=hashlib.file_digest(f,'sha256').hexdigest()
    report['private_zip_bytes']=target.stat().st_size;report['private_zip_members']=len(zipfile.ZipFile(target).namelist())
    return report


def main():
    p=argparse.ArgumentParser();p.add_argument('dat_dir',type=Path);p.add_argument('tiles',type=Path);p.add_argument('private_zip',type=Path);a=p.parse_args()
    r=export(a.dat_dir,a.tiles,a.private_zip);REPORT.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'maps':{k:{'canvas':v['canvas_size'],'placements':v['structure']['modern_draw_candidate_positions']} for k,v in r['maps'].items()},'resources':len(r['resources']),'bytes':r['private_zip_bytes'],'sha256':r['private_zip_sha256'],'members':r['private_zip_members']}))
if __name__=='__main__':main()
