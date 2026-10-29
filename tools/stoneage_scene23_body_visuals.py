"""Twelve R16 source-number candidates: 8 direction/action2 first frames each.

Originals, PNGs and private HTML stay outside Git. This is not a creation UI,
character roster, action-name/FPS certification, or an original game process.
"""
from __future__ import annotations
import argparse,base64,csv,functools,gzip,hashlib,io,json,struct,zipfile
from pathlib import Path
from tools.stoneage_private_scene_actor_r7 import select_animations,resolve_bitmaps
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_tw10_palette import initial_rgb
from tools.stoneage_private_scene_palette_r3 import candidate_rgba
ROOT=Path(__file__).resolve().parents[1]
META=ROOT/'research/recovered/tw10-resource-metadata'
REPORT=ROOT/'research/recovered/STONEAGE-SCENE23-BODY-VISUALS-R1.json'
KEYS=tuple(range(100000,100221,20))
BODY=ROOT/'research/recovered/STONEAGE-TW10-CREATION-BODY-WINDOW-R16.json'
BODY_SHA='03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59'
WINDOW_SHA='0e9687f40dae13f8b700426b44b8fcd1b5b462396541b0123464034fbb755d65'
PIXEL_MANIFEST_SHA='6b62eed7d933de04252d4b542da67ee80b6a629c50498712c8d4fb481ed8fc67'
PINS={
 'sa_3.exe':(425984,'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'),
 'spr_1.bin':(2889630,'53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'),
 'spradrn_1.bin':(5568,'275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25'),
 'adrn_1.bin':(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'real_1.bin':(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
 'Palet_1.sap':(708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0'),
 'Palet_0.sap':(708,'89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf'),
}
FALSE=('original_character_roster_authenticated','all_twelve_are_selectable_proven',
 'original_character_names_proven','face_id_binding_proven','runtime_palette_verified',
 'original_client_executed','original_world_entered','original_server_create_accepted',
 'native_action_name_verified','native_fps_verified','complete_animations_visually_verified',
 'source_action_executed','original_source_browser_verified','proprietary_pixels_published')
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise ValueError(m)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

@functools.lru_cache(maxsize=1)
def archived_selectors():
 need(sha(BODY.read_bytes())==BODY_SHA,'original R16 source report')
 r16=json.loads(BODY.read_bytes());need(tuple(v['dword'] for v in r16['bounded_window']['values'][:12])==KEYS,'R16 source order')
 tables={}
 for name in ['SPR-GROUP-R1.tsv.gz','SPR-ANIMATION-R1.tsv.gz','SPR-FRAME-R1.tsv.gz']:
  with gzip.open(META/name,'rt') as f:
   tables[name]=[r for r in csv.DictReader(f,delimiter='\t') if int(r['spr_no']) in KEYS]
 groups={int(r['spr_no']):r for r in tables['SPR-GROUP-R1.tsv.gz']}
 animations={(int(r['spr_no']),int(r['direction'])):r for r in tables['SPR-ANIMATION-R1.tsv.gz'] if int(r['anim_no'])==2 and 0<=int(r['direction'])<8}
 frames={(int(r['spr_no']),int(r['anim_index'])):r for r in tables['SPR-FRAME-R1.tsv.gz'] if int(r['frame_index'])==0}
 need(len(groups)==12 and len(animations)==96,'archived selector uniqueness')
 wanted={int(frames[(g,int(a['anim_index']))]['bmp_no']) for (g,d),a in animations.items()}
 with gzip.open(META/'ADRN-R1.tsv.gz','rt') as f:
  adr=[r for r in csv.DictReader(f,delimiter='\t') if int(r['bitmapno']) in wanted]
 need(len(adr)==len(wanted),'archived bitmap uniqueness')
 allframes={}
 for row in tables['SPR-FRAME-R1.tsv.gz']:
  key=(int(row['spr_no']),int(row['anim_index']));allframes.setdefault(key,[]).append(row)
 return groups,animations,frames,{int(r['bitmapno']):r for r in adr},allframes

def validate(r):
 need(r['schema']=='stoneage.scene23.TW10_body_candidate_first_frames.r1','schema')
 need(r['source_scope']=='TW10_RETAIL_ORIGINAL_RESOURCES_R16_CANDIDATE_NUMBERS_ONLY','source scope')
 need(all(r[k] is False for k in FALSE),'historical/runtime/publishing boundary')
 need(r['overall_completion_percent'] is None and r['source_action_run_id'] is None and r['original_selectable_character_count'] is None,'no count/run invention')
 need(r['source_files']=={k:dict(bytes=n,sha256=h)for k,(n,h)in PINS.items()},'all seven original source pins')
 need(r['R16_source_report_sha256']==BODY_SHA and r['body_window_sha256']==WINDOW_SHA,'original body window')
 need(r['action_code']==2 and r['observed_frame_index']==0,'finite action and first-frame scope')
 need(r['palette_mode']=='TWO_ORIGINAL_SAP_INITIAL_RGB_CANDIDATES_NOT_RUNTIME_SELECTION','palette scope')
 gmeta,ameta,fmeta,adr,fullframes=archived_selectors();need([g['spr_no']for g in r['groups']]==list(KEYS),'source-number order')
 allids=[]
 for g in r['groups']:
  gm=gmeta[g['spr_no']];need(g['source_group_index']==int(gm['index']) and g['full_segment_sha256']==gm['segment_sha256'],'original full group identity')
  need(len(g['directions'])==8 and [a['direction']for a in g['directions']]==list(range(8)),'all and only eight ordered directions')
  for a in g['directions']:
   am=ameta[(g['spr_no'],a['direction'])];fm=fmeta[(g['spr_no'],int(am['anim_index']))]
   need((a['source_animation_index'],a['header_offset'],a['end_offset'],a['duration_word'],a['source_frame_count'])==tuple(int(am[k])for k in ['anim_index','offset','end_offset','duration','frame_count']),'original animation span/count/duration')
   need(a['first_frame']==[int(fm[k])for k in ['bmp_no','pos_x','pos_y','sound_no']] and a['first_frame_offset']==int(fm['offset']),'actual source first frame')
   fs=fullframes[(g['spr_no'],a['source_animation_index'])]
   encoded=struct.pack('<HHII',a['direction'],2,a['duration_word'],a['source_frame_count'])+b''.join(struct.pack('<IhhH',*[int(f[k])for k in ['bmp_no','pos_x','pos_y','sound_no']])for f in fs)
   need(sha(encoded)==a['animation_span_sha256'],'entire original selected animation span')
   allids.append(a['first_frame'][0])
 need(r['first_frame_occurrences']==96 and r['distinct_first_frame_bitmaps']==len(set(allids)),'first-frame occurrence conservation')
 rows=r['bitmaps'];need(len(rows)==len(set(allids)) and {b['bitmapno']for b in rows}==set(allids),'no missing/extraneous source pixels')
 need(sha(canonical(rows))==PIXEL_MANIFEST_SHA,'actual private-derived pixel metadata immutable')
 for b in rows:
  old=adr[b['bitmapno']]
  need([b[k]for k in ['source_adrn_index','offset','size','xoff','yoff','width','height']]==[int(old[k])for k in ['index','adder','size','xoff','yoff','width','height']],'original ADRN geometry')
  need(b['RD_sha256']==old['rd_block_sha256'],'original RD block identity')
 need(r['first_frame_occurrences']-r['distinct_first_frame_bitmaps']==r['repeated_first_frame_positions'],'do not silently deduplicate positions')
 return dict(candidate_groups=12,first_frame_occurrences=96,distinct_original_bitmaps=len(rows),original_selectable_character_count=None,original_world_entered=False)

def export(source,out):
 from PIL import Image,ImageDraw
 out=out.resolve();need(ROOT not in out.parents and out!=ROOT and not out.exists(),'new private folder outside git')
 originals={}
 for name,pin in PINS.items():
  b=(source/name).read_bytes();need((len(b),sha(b))==pin,'source file SHA '+name);originals[name]=b
 window=originals['sa_3.exe'][364072:364200];need(sha(window)==WINDOW_SHA and struct.unpack('<32I',window)[:12]==KEYS,'actual original body-table window')
 groups=select_animations(originals['spradrn_1.bin'],originals['spr_1.bin'],KEYS,(2,));records=[];ids=[]
 for g in groups:
  directions=[]
  for a in sorted(g['animations'],key=lambda a:a['direction']):
   directions.append(dict(direction=a['direction'],source_animation_index=a['source_animation_index'],header_offset=a['header_offset'],end_offset=a['end_offset'],duration_word=a['duration_word'],source_frame_count=len(a['frames']),first_frame_offset=a['header_offset']+12,first_frame=a['frames'][0],animation_span_sha256=a['source_animation_span_sha256']))
   ids.append(a['frames'][0][0])
  records.append(dict(spr_no=g['spr_no'],source_group_index=g['source_group_index'],full_segment_sha256=g['whole_group_segment_sha256'],directions=directions))
 rows=resolve_bitmaps(originals['adrn_1.bin'],set(ids),len(originals['real_1.bin']));palettes={str(i):initial_rgb(originals['Palet_'+str(i)+'.sap'])for i in (0,1)};images={'0':{},'1':{}};blocks={};out.mkdir(mode=0o700,parents=True)
 for n,b in sorted(rows.items()):
  rd=originals['real_1.bin'][b['offset']:b['offset']+b['size']];header,px=decode_rd_block(rd,authoritative_block_size=b['size']);need((header['width_s'],header['height_s'])==(b['width'],b['height']),'original image geometry')
  blocks[str(n)+'.rd']=rd;b.update(RD_sha256=sha(rd),indices_sha256=sha(px),palette_candidates={})
  for palette,rgb in palettes.items():
   rgba=candidate_rgba(px,b['width'],b['height'],rgb);im=Image.frombytes('RGBA',(b['width'],b['height']),rgba);buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue()
   b['palette_candidates'][palette]=dict(RGBA_sha256=sha(rgba),PNG_sha256=sha(png));images[palette][str(n)]=base64.b64encode(png).decode()
 report=dict(schema='stoneage.scene23.TW10_body_candidate_first_frames.r1',source_scope='TW10_RETAIL_ORIGINAL_RESOURCES_R16_CANDIDATE_NUMBERS_ONLY',source_files={k:dict(bytes=n,sha256=h)for k,(n,h)in PINS.items()},R16_source_report_sha256=BODY_SHA,body_window_sha256=sha(window),groups=records,bitmaps=list(rows.values()),action_code=2,observed_frame_index=0,first_frame_occurrences=len(ids),distinct_first_frame_bitmaps=len(set(ids)),repeated_first_frame_positions=len(ids)-len(set(ids)),palette_mode='TWO_ORIGINAL_SAP_INITIAL_RGB_CANDIDATES_NOT_RUNTIME_SELECTION',original_selectable_character_count=None,source_action_run_id=None,overall_completion_percent=None,**{k:False for k in FALSE})
 validate(report)
 (out/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n');
 for i in (0,1):(out/('Palet_'+str(i)+'.sap')).write_bytes(originals['Palet_'+str(i)+'.sap'])
 with zipfile.ZipFile(out/'private-first-frame-RD.zip','w',zipfile.ZIP_DEFLATED)as z:
  for n,rd in blocks.items():z.writestr(n,rd)
 # Canvases are 2x integer nearest-neighbor with modern common anchors.
 canvases=[]
 for palette in ('0','1'):
  sheet=Image.new('RGBA',(960,840),'#142129')
  for gi,g in enumerate(records):
   for a in g['directions']:
    b=rows[a['first_frame'][0]];im=Image.open(io.BytesIO(base64.b64decode(images[palette][str(b['bitmapno'])]))).convert('RGBA');c=Image.new('RGBA',(240,260),'#142129');big=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);x=120+2*(b['xoff']+a['first_frame'][1]);y=200+2*(b['yoff']+a['first_frame'][2]);need(0<=x<=240-big.width and 0<=y<=260-big.height,'finite modern display bounds');c.alpha_composite(big,(x,y));canvases.append(dict(group=g['spr_no'],direction=a['direction'],palette=palette,RGBA_sha256=sha(c.tobytes())))
    if a['direction']==0:
     xx=gi%4*240;yy=gi//4*280;sheet.alpha_composite(c,(xx,yy+20));ImageDraw.Draw(sheet).text((xx+12,yy+6),str(g['spr_no']),fill='#e8d394')
  buf=io.BytesIO();sheet.save(buf,format='PNG');(out/('StoneAge-SCENE23-body-Palet'+palette+'-candidates.png')).write_bytes(buf.getvalue())
 model=dict(report=report,images=images,canvas_hashes=canvases,synthetic_fixture=False)
 template=(ROOT/'tools/stoneage_scene23_observer.html').read_text();need(template.count('__SCENE23_MODEL__')==1,'HTML model marker');(out/'StoneAge-SCENE23-body-observer.html').write_text(template.replace('__SCENE23_MODEL__',json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')))
 print(json.dumps(dict(pixel_manifest_sha256=sha(canonical(report['bitmaps'])),groups=12,first_frames=len(ids),distinct=len(rows))))
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-source',type=Path);p.add_argument('--private-output',type=Path);a=p.parse_args()
 if a.private_source:
  need(a.private_output is not None,'private output required');export(a.private_source,a.private_output)
 else:print(json.dumps(validate(json.loads(REPORT.read_bytes())),sort_keys=True))
if __name__=='__main__':main()
