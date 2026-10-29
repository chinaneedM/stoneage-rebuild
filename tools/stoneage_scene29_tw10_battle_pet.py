#!/usr/bin/env python3
"""Source-qualified ORIGINAL TW1 battle SAB x pet sprites: private manual viewer.

Public CI validates only exact derived source metadata. Private mode reads two fully
pinned local original-source archives, never executes originals, writes proprietary
images only into a selected existing directory OUTSIDE the repository.
"""
import argparse
import copy
import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-SCENE29-TW10-BATTLE-PET-ACTUAL-R1.json'
SCENE28 = ROOT/'research/recovered/STONEAGE-SCENE28-TW10-ACTION1-PIXELS-R1.json'
ORIGINAL_SHA = '3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
PRIVATE28_SHA = 'f707d196acb6c449e2b6b11345a02db36ac6726131ce51f9a93587b32c3ad492'
SCENE28_SOURCE_GIT_BLOB = 'bb23ced85462f5edec3f9cc5037216773a694d9d'
PUBLIC_REPORT_SHA = '7a2699c3db96fd4c2fcfb478e805b9be81018c5f470de8a6e8b8b95e0f83d7b2' 
PINS = {
 'source/data/adrn_1.bin': (10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'source/data/real_1.bin': (315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
 'source/data/pal/Palet_1.sap': (708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0'),
 'source/data/battlemap/battle00.sab': (804,'881850de822d7d5e44578dd11d309e9b2c3ae3455cfa71380199212cb368dec2'),
 'source/data/battlemap/battle100.sab': (804,'f7637c356b78bded96ceacac20cd09e1de03a90571fa6ee9ec617c108bf0b549'),
 'source/data/battlemap/battle145.sab': (804,'b3e6c9a3c3dd7375d4898ab4f8e1a5e2c684f60a0ab9c045e95fcd4c20b33476'),
}
MAPS=(0,100,145)
GRID_PAYLOAD_SHA={0:'e6eeb98e76d4f551afd9f109dc8fdbea3bac8788a9160367e8cbd36a7780ac6d',100:'1d6423df8dfedc59ce33579b4911ec3683cd6b4b3ad50a08d41c0a8ac4572c62',145:'a328637919ac10ae6a977efcd0b272913b4d7b0c34e31af2fa84cf867dd8e1d6'}
FALSE=('original_game_world_entered','native_battle_render_authenticated','official_battle_map_name_known',
       'original_battle_sab_selected_at_runtime','native_battle_palette_verified',
       'native_battle_actor_placement_verified','original_executable_executed_in_this_package',
       'original_battle_encounter_link_verified','original_pet_species_verified','original_action1_semantics_verified',
       'proprietary_art_published_in_git')

def need(b,msg):
 if not b:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def git_blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sha_file(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def validate_map(raw,num):
 need(type(raw) is bytes and len(raw)==804 and raw[:4]==b'SAB ','original SAB envelope')
 grid=[list(struct.unpack_from('>20H',raw,4+r*40)) for r in range(20)]
 need(len(grid)==20 and all(len(row)==20 for row in grid),'SAB finite 20x20 candidate')
 return grid

def alternate_rle(block,width,height):
 """Independent fixed-extent RLE cursor, distinct from repository RD codec append loop."""
 need(block[:2]==b'RD' and block[2] in (0,1),'RD magic or flag')
 encoded=memoryview(block)[16:];size=width*height
 if block[2]==0:
  need(len(encoded)>=size,'raw RD too short')
  return bytes(encoded[:size])
 dst=bytearray(size);dstpos=0;pos=0
 while pos<len(encoded):
  c=encoded[pos];pos+=1;family=c>>4;count=c&15
  if family in (8,9,10):
   need(pos<len(encoded),'repeat value missing');val=encoded[pos];pos+=1
  if family in (1,9,13):
   need(pos<len(encoded),'12 bit run missing');count=(count<<8)|encoded[pos];pos+=1
  elif family in (2,10,14):
   need(pos+1<len(encoded),'20 bit run missing');count=(count<<16)|(encoded[pos]<<8)|encoded[pos+1];pos+=2
  need(dstpos+count<=size,'RD output overflow')
  if family in (0,1,2):
   need(pos+count<=len(encoded),'literal payload missing')
   dst[dstpos:dstpos+count]=encoded[pos:pos+count];pos+=count
  elif family in (8,9,10):dst[dstpos:dstpos+count]=bytes([val])*count
  elif family in (12,13,14):pass
  else:raise ValueError('RD unknown RLE control')
  dstpos+=count
 need(dstpos==size,'RD output length mismatch')
 return bytes(dst)

def original_report(zip_path, pet28_zip):
 need(zip_path.is_file() and zip_path.stat().st_size==372626292 and sha_file(zip_path)==ORIGINAL_SHA,'original TW10 entire private package SHA')
 need(pet28_zip.is_file() and pet28_zip.stat().st_size==347996 and sha_file(pet28_zip)==PRIVATE28_SHA,'SCENE28 private observer entire ZIP SHA')
 old=json.loads(SCENE28.read_text(encoding='utf-8'))
 need(git_blob(SCENE28.read_bytes())==SCENE28_SOURCE_GIT_BLOB,'SCENE28 immutable published original image receipts')
 need(old['reproduces_scene26_released_frame_sequences']['distinct_bitmap_numbers']==48 and old['reproduces_scene26_released_frame_sequences']['frame_positions']==80,'SCENE28 source count')
 with zipfile.ZipFile(zip_path) as z:
  need(len(z.namelist())==379,'P3H ZIP original+observation source tree count')
  raws={p:z.read(p) for p in PINS}
  for p,(size,digest) in PINS.items():need(len(raws[p])==size and sha(raws[p])==digest,'original source bytes changed: '+p)
  battle=z.read('source/data/battle_1.bin')
  need(len(battle)==185892,'original TW10 battle container bytes')
  maps=[];all_ids=set()
  for n in MAPS:
   path=f'source/data/battlemap/battle{n:02}.sab';raw=raws[path];start=804*n
   need(battle[start:start+804]==raw,'original standalone SAB != same-source battle_1 slice')
   grid=validate_map(raw,n);ids={v for row in grid for v in row};all_ids.update(ids)
   maps.append(dict(index=n,path=path,bytes=804,sha256=sha(raw),battle_container_slice_offset=start,
     battle_container_slice_sha256=sha(battle[start:start+804]),grid=grid,unique_tile_bitmaps=len(ids),cells=400,
     render_algorithm='MODERN_ISOMETRIC_32_24_VISUAL_CANDIDATE_NOT_NATIVE_DRAW'))
  need(len(all_ids)==158,'three maps original bitmap union changed')
  adrn=raws['source/data/adrn_1.bin'];needed={n:[] for n in all_ids}
  for i in range(0,len(adrn),80):
   record=adrn[i:i+80];n,off,size,x,y,w,h=struct.unpack_from('<7i',record)
   if n in needed:needed[n].append(dict(bitmapno=n,source_adrn_index=i//80,offset=off,size=size,xoff=x,yoff=y,width=w,height=h,
    record_sha256=sha(record)))
  need(all(len(v)==1 for v in needed.values()),'original same-version physical bitmap ambiguity')
  from tools.stoneage_rd_codec import decode_rd_block
  rows=[];index_payloads={};rd_byte_count=0
  with z.open('source/data/real_1.bin') as f:
   # streaming ZIP is not seekable on all clients; authenticated raw is memory-bounded here
   real=f.read()
  need(len(real)==315842228 and sha(real)==PINS['source/data/real_1.bin'][1],'original REAL source whole SHA')
  for n in sorted(needed):
   d=needed[n][0];need(16<=d['size']<=30000 and 0<=d['offset']<=len(real)-d['size'],'original ADRN bounds')
   raw=real[d['offset']:d['offset']+d['size']]
   rd,pixels=decode_rd_block(raw,authoritative_block_size=d['size'])
   need((rd['width_s'],rd['height_s'])==(d['width'],d['height']),'ADRN/RD geometry mismatch')
   need(alternate_rle(raw,d['width'],d['height'])==pixels,'independent RD pixels unequal')
   need(all(v==0 or 16<=v<=239 for v in pixels),'requires reserved palette slot proof')
   d.update(rd_sha256=sha(raw),pixel_indices_sha256=sha(pixels),rd_flag=rd['flag'],decoded_pixel_bytes=len(pixels),
    nonzero_index_pixels=sum(v!=0 for v in pixels),visible_palette_index_min=min(pixels),visible_palette_index_max=max(pixels))
   rows.append(d);index_payloads[n]=pixels;rd_byte_count+=len(raw)
 return dict(schema='stoneage.scene29.tw10_battlemap_pet_source.actual_v1',original_source_scope='TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630',
    original_private_zip=dict(bytes=372626292,sha256=ORIGINAL_SHA),source_files={p:dict(bytes=k[0],sha256=k[1]) for p,k in PINS.items()},
    battle_container=dict(bytes=len(battle),sha256=sha(battle),read_from_same_original_zip=True),
    sab_maps=maps,actual_battle_map_ids=list(MAPS),source_sab_files=3,source_sab_cell_occurrences=1200,
    unique_source_tile_bitmaps=158,original_rd_decoded=158,original_rd_total_encoded_bytes=rd_byte_count,
    original_rd_pixel_index_count=sum(r['decoded_pixel_bytes'] for r in rows),unique_tile_bitmaps=rows,
    pet_source=dict(source='SCENE28 actual original TW10 action1 source',private_zip_bytes=347996,private_zip_sha256=PRIVATE28_SHA,
      original_animation_count=24,frame_occurrences=80,unique_pet_bitmaps=48,pet_role='MODERN_MANUAL_SCENE_OVERLAY_NOT_NATIVE_ENCOUNTER'),
    provenance=dict(selected_map_runtime_witness=None,original_battle_grid_native_draw_call_witness=None,
      source_SAB_grid_model='SOURCE_20X20_BE_U16_CANDIDATE',palette_initialization='SOURCE_PAL1_CANDIDATE_NOT_NATIVE_SELECTION',
      bitmap_RLE_independent_agreement=True,battle_source_equals_original_container_slices=True),
    original_pictures_privately_rendered=True,actual_private_chromium_observation=False,
    **{x:False for x in FALSE},stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING',overall_restoration_percentage=None),index_payloads,raws

def public_derivation(original):
 result=copy.deepcopy(original)
 for m in result['sab_maps']:
  grid=m.pop('grid')
  encoded=b''.join(struct.pack('>H',v) for row in grid for v in row)
  need(len(encoded)==800 and sha(encoded)==GRID_PAYLOAD_SHA[m['index']],'original private map grid digest')
  m['original_grid_payload_sha256']=sha(encoded)
  m['unique_tile_bitmap_ids']=sorted({v for row in grid for v in row})
  m['original_grid_layout_publicly_included']=False
 result['original_tile_position_payload_publicly_included']=False
 return result


def check_public(report=None):
 if report is None:
  raw=REPORT.read_bytes()
  need(sha(raw)==PUBLIC_REPORT_SHA,'released source metadata report SHA changed')
  r=json.loads(raw)
 else:r=report
 need(git_blob(SCENE28.read_bytes())==SCENE28_SOURCE_GIT_BLOB,'original prior SCENE28 report mutated')
 need(r['schema']=='stoneage.scene29.tw10_battlemap_pet_source.actual_v1','public schema')
 need(r['original_source_scope']=='TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630','original provenance')
 need(r['original_private_zip']=={'bytes':372626292,'sha256':ORIGINAL_SHA},'source ZIP identity')
 need(r['source_files']=={p:{'bytes':size,'sha256':digest} for p,(size,digest) in PINS.items()},'source originals')
 need(r['source_sab_files']==3 and r['actual_battle_map_ids']==list(MAPS) and r['source_sab_cell_occurrences']==1200,'source scope')
 need(r['unique_source_tile_bitmaps']==158 and r['original_rd_decoded']==158,'unique source bitmap evidence count')
 need(r['battle_container']['bytes']==185892 and r['battle_container']['read_from_same_original_zip'] is True,'original container binding')
 need(len(r['sab_maps'])==3 and len(r['unique_tile_bitmaps'])==158,'map/report census')
 original=[]
 for i,x in enumerate(r['sab_maps']):
  n=MAPS[i];p=f'source/data/battlemap/battle{n:02}.sab'
  need(x['index']==n and x['path']==p and x['bytes']==804 and x['sha256']==PINS[p][1] and
   x['battle_container_slice_offset']==804*n and x['battle_container_slice_sha256']==x['sha256'],'original SAB identity/container slice')
  need('grid' not in x and x['original_grid_layout_publicly_included'] is False,'original grid copyrighted positions must remain private')
  need(x['original_grid_payload_sha256']==GRID_PAYLOAD_SHA[n], 'actual private 800-byte source grid identity')
  tileids=x['unique_tile_bitmap_ids']
  need(type(tileids) is list and all(type(v) is int and 0<=v<=65535 for v in tileids) and
       tileids==sorted(set(tileids)),'original source tile-id set')
  for key in ('candidate_background_png_sha256','candidate_background_rgba_sha256'):
   need(re.fullmatch('[0-9a-f]{64}',x[key]) is not None,'private pixel observation SHA missing')
  need(x['cells']==400 and x['unique_tile_bitmaps']==len(tileids) and
   x['render_algorithm']=='MODERN_ISOMETRIC_32_24_VISUAL_CANDIDATE_NOT_NATIVE_DRAW','non-native draw qualification')
  original.extend(tileids)
 need(r['original_tile_position_payload_publicly_included'] is False,'source original map grid leaked')
 need(set(original)=={x['bitmapno'] for x in r['unique_tile_bitmaps']},'source tile membership/ADRN bitmap closure')
 need(len(set(original))==158,'source 3x20x20 distinct bitmaps')
 total_index=0;total_rd=0
 for row in r['unique_tile_bitmaps']:
  need(all(type(row[k]) is int for k in ('bitmapno','source_adrn_index','offset','size','xoff','yoff','width','height','decoded_pixel_bytes','nonzero_index_pixels')),'original pixel types')
  need(row['bitmapno'] in original and row['source_adrn_index']>=0 and 16<=row['size']<=30000 and
   0<=row['offset'] and row['offset']+row['size']<=315842228,'source RD offsets')
  need(0<row['width']<=1024 and 0<row['height']<=1024 and row['decoded_pixel_bytes']==row['width']*row['height'],'source pixel geometry')
  need(0<=row['nonzero_index_pixels']<=row['decoded_pixel_bytes'] and row['rd_flag'] in (0,1) and
   0<=row['visible_palette_index_min']<=row['visible_palette_index_max']<=239,'source pixel flags')
  for field in ('record_sha256','rd_sha256','pixel_indices_sha256'):
   need(re.fullmatch('[0-9a-f]{64}',row[field]) is not None,'source digest absent')
  total_index+=row['decoded_pixel_bytes'];total_rd+=row['size']
 need(total_index==r['original_rd_pixel_index_count'] and total_rd==r['original_rd_total_encoded_bytes'],'source size summary')
 need(r['pet_source']==dict(source='SCENE28 actual original TW10 action1 source',private_zip_bytes=347996,
   private_zip_sha256=PRIVATE28_SHA,original_animation_count=24,frame_occurrences=80,unique_pet_bitmaps=48,
   pet_role='MODERN_MANUAL_SCENE_OVERLAY_NOT_NATIVE_ENCOUNTER'),'original pet evidence linkage')
 q=r['provenance'];need(q['selected_map_runtime_witness'] is None and q['original_battle_grid_native_draw_call_witness'] is None
  and q['source_SAB_grid_model']=='SOURCE_20X20_BE_U16_CANDIDATE' and q['bitmap_RLE_independent_agreement'] is True
  and q['battle_source_equals_original_container_slices'] is True,'original runtime evidence boundary')
 for k in FALSE:need(r[k] is False,'unsupported native/world/palette/identity claim '+k)
 need(r['stage_a']=='7_PARTIAL_2_OPEN' and r['stage_b_and_wiki']=='GATED' and r['r79']=='PAUSED_NON_BLOCKING'
  and r['overall_restoration_percentage'] is None,'project stage not certified')
 need(r['original_pictures_privately_rendered'] is True and r['actual_private_chromium_observation'] is True,'private visual verification missing')
 browser=r['private_chromium_observation_receipt']
 need(browser['checks_passed']==13 and browser['page_errors']==0 and browser['network_requests']==0,'real browser acceptance')
 need(re.fullmatch('[0-9a-f]{64}',browser['screenshot_png_sha256']) is not None and browser['screenshot_bytes']>100000,'private screenshot reception')
 return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check-public',action='store_true');ap.add_argument('--original-zip',type=Path);ap.add_argument('--scene28-private-zip',type=Path);ap.add_argument('--private-output-dir',type=Path)
 a=ap.parse_args()
 if a.check_public:
  need(not any((a.original_zip,a.scene28_private_zip,a.private_output_dir)),'no original files with public replay')
  d=check_public();print('SCENE29 public derived original SAB/pixel join PASS: 3 maps, 1200 source cells, 158 source RD, 48 separate original pet bitmaps, no game runtime');return
 need(all((a.original_zip,a.scene28_private_zip,a.private_output_dir)),'private render requires both original sources and output')
 d,pixels,raws=original_report(a.original_zip,a.scene28_private_zip)
 archived=check_public()
 source_public=public_derivation(d)
 need(source_public['battle_container']==archived['battle_container'],'source re-read battle container drift')
 need(source_public['unique_tile_bitmaps']==archived['unique_tile_bitmaps'],'source re-read 158 physical RD or indexed pixels drift')
 for i,m in enumerate(d['sab_maps']):
  for key,value in source_public['sab_maps'][i].items():need(archived['sab_maps'][i][key]==value,'source re-read original SAB changed: '+key)
 # Private renderer implementation lives in the same package file below.
 render_private(d,pixels,raws,a.scene28_private_zip,a.private_output_dir)
 for i,m in enumerate(d['sab_maps']):
  for key in ('candidate_background_png_sha256','candidate_background_rgba_sha256'):
   need(archived['sab_maps'][i][key]==m[key],'source re-render image candidate drift')
 (a.private_output_dir/'SCENE29-public-derived-source-report.json').write_text(json.dumps(public_derivation(d),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# PRIVATE renderer is deliberately after public integrity checker. CI never calls it.
def render_private(d,indices,raws,scene28zip,out):
 from PIL import Image
 need(out.is_dir() and out.resolve()!=ROOT and ROOT not in out.resolve().parents,'private out of repository')
 with zipfile.ZipFile(scene28zip) as z:
  htmlfiles=[n for n in z.namelist() if n.endswith('observer.html')]
  need(len(htmlfiles)==1,'SCENE28 private observer absent')
  old=z.read(htmlfiles[0]).decode('utf-8')
  match=re.search(r'<script id="private-data" type="application/json">(.*?)</script>',old,re.S)
  need(match is not None,'SCENE28 source images missing')
  oldimages=json.loads(match[1]);need(len(oldimages['images']['0'])==48 and len(oldimages['images']['1'])==48,'old pet PNG inventory')
 # Actual candidate palette from source Palet_1, never a qualified runtime selection.
 from tools.stoneage_tw10_palette import initial_rgb
 table=initial_rgb(raws['source/data/pal/Palet_1.sap'])
 need(len(table)==768,'palette candidate size')
 original_images={};rgba_images={}
 for row in d['unique_tile_bitmaps']:
  no=row['bitmapno'];w=row['width'];h=row['height'];px=indices[no]
  raw=bytes(t for y in range(h-1,-1,-1) for v in px[y*w:(y+1)*w] for t in (*table[v*3:v*3+3],0 if v==0 else 255))
  rgba_images[no]=Image.frombytes('RGBA',(w,h),raw)
  original_images[no]=sha(raw)
 backgrounds={}
 for m in d['sab_maps']:
  im=Image.new('RGBA',(1350,1220),(9,19,29,255))
  for y,row in enumerate(m['grid']):
   for x,no in enumerate(row):
    tile=next(v for v in d['unique_tile_bitmaps'] if v['bitmapno']==no)
    cx=675+(x-y)*32+tile['xoff'];cy=55+(x+y)*24+tile['yoff']
    im.alpha_composite(rgba_images[no],(cx,cy))
  bio=io.BytesIO();im.save(bio,format='PNG');png=bio.getvalue()
  backgrounds[str(m['index'])]='data:image/png;base64,'+base64.b64encode(png).decode()
  m['candidate_background_png_sha256']=sha(png)
  m['candidate_background_rgba_sha256']=sha(im.tobytes())
  (out/f'SCENE29-private-original-battle{m["index"]:03}-candidate.png').write_bytes(png)
 data=dict(backgrounds=backgrounds,actor_images=oldimages['images'],frames=oldimages['frames'],source_zip_sha=ORIGINAL_SHA)
 encoded=json.dumps(data,separators=(',',':')).replace('<','\\u003c')
 template='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>SCENE29 台湾1.0 原图复原研究台（私人）</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0c1624;color:#e9f1fc;font:14px/1.55 system-ui,"Microsoft Yahei",sans-serif}header,main,footer{max-width:1220px;margin:auto;padding:16px 24px}h1{font-size:24px;margin:0}.caution{padding:12px 16px;border-left:4px solid #f2b76c;background:#202b3c}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}label{display:inline-flex;gap:6px;align-items:center}button,select{border:1px solid #7891b5;background:#23354c;color:#fff;border-radius:6px;padding:8px;cursor:pointer}.stage{position:relative;background:#09131d;border:1px solid #3d546f;border-radius:12px;max-width:100%;overflow:hidden}.stage>img{width:100%;height:auto;display:block;image-rendering:pixelated}.actor{position:absolute;width:7%;height:auto;max-width:110px;image-rendering:pixelated;transform:translate(-50%,-85%);filter:drop-shadow(1px 2px 1px #000)}.metric{font-family:monospace;font-size:12px;color:#b6c6db}footer{color:#9bacbe}
</style></head><body><header><h1>《石器时代》台湾1.0 原始战斗场景 · SCENE29 私人观察台</h1><p class="caution"><b>非原游戏、非原战斗执行。</b> 同一已验零售客户端的真实 SAB 网格、ADRN／REAL 地表图与宠物 action=1 原位图。地图等角拼接、层次及角色放置为现代研究候选；不知道原游戏选用哪张地图、原场景色表、宠物角色身份、帧率或战斗行为。可手动移动只是查看原图组合，不是游戏世界碰撞/行走。</p></header><main><div class="controls"><label>原战斗图编号 <select id="map"><option value="0">SAB 0 · 地表候选</option><option value="100">SAB 100 · 地表＋物件候选</option><option value="145">SAB 145 · 立体建筑候选</option></select></label><label>宠物资源组 <select id="pet"><option>100250</option><option>100251</option><option>100252</option></select></label><label>原方向 <select id="direction"></select></label><label>候选配色 <select id="palette"><option value="1">Palet_1</option><option value="0">Palet_0</option></select></label><button id="previous">上一原帧</button><button id="next">下一原帧</button><button id="reset">复位</button></div><p class="metric" id="line"></p><div class="stage" id="stage"><img id="scene" alt="TW1 原 SAB/REAL 候选场景" draggable="false"><img id="actor" class="actor" alt="TW1 原宠物候选帧" draggable="false"></div><p>单击地图可移动<strong>现代人工观察标记</strong>；键盘方向键每次改变标记2%。地图只是同源原位图的候选合成，任何移动/碰撞/遇敌均未发生。按原帧编号逐帧查看，不将源 duration 字段解释成毫秒。</p></main><footer>全部图像仅存储于私人离线文件；无账号、网络请求、商业客户端执行。原包 SHA-256 <span id="sourcehash"></span></footer><script id="data" type="application/json">__SOURCE_PLACEHOLDER__</script><script>(function(){"use strict";const data=JSON.parse(document.getElementById('data').textContent),q=id=>document.getElementById(id),st={x:.52,y:.49,frame:0};q('sourcehash').textContent=data.source_zip_sha;q('direction').innerHTML=Array.from({length:8},(_,i)=>'<option value="'+i+'">方向 '+i+'</option>').join('');const clamp=v=>Math.min(.92,Math.max(.08,v));function update(){const m=q('map').value,p=q('pet').value,dr=+q('direction').value,pal=q('palette').value,seq=data.frames[p][dr];st.frame%=seq.positions.length;const n=seq.positions[st.frame];q('scene').src=data.backgrounds[m];q('actor').src=data.actor_images[pal][n];q('actor').style.left=(st.x*100)+'%';q('actor').style.top=(st.y*100)+'%';q('line').textContent='原 SAB '+m+' (400格) | 宠物源 '+p+' | 原方向 '+dr+' | action=1 | 帧位置 '+(st.frame+1)+'/'+seq.positions.length+' | 原 bitmap '+n+' | duration word '+seq.duration_word+' (时间单位未知)';}function next(n){const v=data.frames[q('pet').value][+q('direction').value];st.frame=(st.frame+n+v.positions.length)%v.positions.length;update()}for(const v of ['map','pet','direction','palette'])q(v).onchange=()=>{st.frame=0;update()};q('previous').onclick=()=>next(-1);q('next').onclick=()=>next(1);q('reset').onclick=()=>{st.x=.52;st.y=.49;st.frame=0;q('map').value='0';q('pet').value='100250';q('direction').value='0';q('palette').value='1';update()};q('stage').onclick=e=>{const r=q('stage').getBoundingClientRect();st.x=clamp((e.clientX-r.left)/r.width);st.y=clamp((e.clientY-r.top)/r.height);update()};addEventListener('keydown',e=>{const f={'ArrowLeft':[-.02,0],'ArrowRight':[.02,0],'ArrowUp':[0,-.02],'ArrowDown':[0,.02]}[e.key];if(!f||['SELECT','BUTTON'].includes(document.activeElement.tagName))return;e.preventDefault();st.x=clamp(st.x+f[0]);st.y=clamp(st.y+f[1]);update()});update()})();</script></body></html>'''
 html=template.replace('__SOURCE_PLACEHOLDER__',encoded)
 need('__SOURCE_PLACEHOLDER__' not in html,'HTML embedding')
 (out/'SCENE29-private-original-TW10-battle-pet-observer.html').write_text(html,encoding='utf-8')
 (out/'SCENE29-private-build-custody.json').write_text(json.dumps({'original_zip_sha256':ORIGINAL_SHA,'pet_source_zip_sha256':PRIVATE28_SHA,'source_bitmaps':158,
   'source_map_count':3,'source_map_cell_count':1200,'rendered_private_images_sha256':[{'map':m['index'],'PNG_sha256':m['candidate_background_png_sha256']} for m in d['sab_maps']],
   'observer_html_sha256':sha(html.encode()),'rendering_is_native_authenticated':False,'original_game_runtime_executed':False},indent=2)+'\n')

if __name__=='__main__':main()