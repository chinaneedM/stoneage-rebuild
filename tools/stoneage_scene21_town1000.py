"""Finite town1000 source window and prefix-qualified original graphics.

Original bytes stay private. The old full REAL-prefix comparison is reused,
not falsely described as a new full mixed25 REAL read or native game session.
"""
import argparse,base64,hashlib,io,json,struct,zipfile
from pathlib import Path
from tools.stoneage_scene15_exit_observer import REPORT as PRIOR_REPORT, validate as prior_validate
from tools.stoneage_scene17_derived_acceptance import REPORT as NPC_REPORT, validate as npc_validate
from tools.stoneage_private_scene_palette_r3 import sweep,candidate_rgba
from tools.stoneage_tw10_palette import initial_rgb
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_scene14_independent_replay import decode as independent_decode

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE21-TOWN1000-SOURCE-R1.json'
PREFIX_PATH=ROOT/'research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt'
PREFIX_SHA='3b47bebc704e8a2245b6bb9ec366f3d76d797b54378142bf1618fe5058ff9b4c'
PINS={
 'r3':(3356562,'fa296ad8e5afb9065fd8a7894fed4f783ad6f393901509f8491383c56a9ee285'),
 'r15':(529126,'cfe5d60d64188ea15fb5758af0220cf47f3234be7bd896cebddb2936fe6bb21d'),
 'tw':(372626292,'3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'),
 'adrn':(18765120,'92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74'),
 'tw_adrn':(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'tw_real':(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
 'map':(153608,'94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e'),
 'pal':(708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0')}
BOUNDS=[60,96,66,106];OLD=[60,96,66,102];CENTER=[63,103]
GAPS={150:2,151:3,152:1,153:2,155:1,160:1,187:1,191:1,207:2,211:1,219:1,429:1,799:1,802:1,812:1,822:1,825:1,12837:1,12845:1}
FALSE=('original_world_entered','same_official_deployed_build_authenticated',
 'native_palette_selection_verified','native_occlusion_verified','native_NPC_draw_selection_verified',
 'map_third_plane_interpreted_as_collision','original_NPC_name_or_dialogue_authenticated',
 'copyrighted_assets_in_public_git','current_full_mixed_REAL_prefix_reverification')

def need(ok,label):
 if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def check(b,key):need((len(b),sha(b))==PINS[key],'whole original '+key)
def package(path,key):
 with path.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 need((path.stat().st_size,d)==PINS[key],'private package '+key)
 return zipfile.ZipFile(path)

def prefix_evidence(raw=None):
 raw=PREFIX_PATH.read_bytes() if raw is None else raw
 need(sha(raw)==PREFIX_SHA,'immutable archived full byte-prefix evidence')
 lines=raw.decode().splitlines()
 need('REAL_DIFF|tw_bytes=315842228|v25_bytes=763908374|common_prefix_bytes=315842228' in lines,'complete same-parent REAL prefix')
 need(any(x.startswith('ADRN_DIFF|tw_records=125996|v25_records=234564|exact_prefix_records=125996|') for x in lines),'complete ADRN prefix')
 return {'path':str(PREFIX_PATH.relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw),
         'mixed_REAL_sha256':'c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d',
         'REAL_prefix_bytes':315842228,'ADRN_prefix_records':125996,
         'claim':'PRIOR_VERIFIED_EXACT_FULL_PREFIX_SAME_AUTHENTICATED_PARENT_HASHES'}

def map_cells(dat):
 check(dat,'map');w,h=struct.unpack_from('<II',dat);need((w,h)==(160,160),'original map dimensions')
 cells=[];placements=[]
 for y in range(96,107):
  for x in range(60,67):
   values=[struct.unpack_from('<H',dat,8+2*(p*w*h+y*w+x))[0] for p in range(3)]
   cells.append({'xy':[x,y],'tile':values[0],'parts':values[1]})
 for p,layer in [(0,'tile'),(1,'parts')]:
  for rx,ry in sweep(7,11):
   x,y=60+rx,96+ry;no=struct.unpack_from('<H',dat,8+2*(p*w*h+y*w+x))[0]
   if no>99:placements.append({'layer':layer,'xy':[x,y],'image_key':no,'anchor':[(x-63+y-103)*32,(y-103-(x-63))*24]})
 return cells,placements,[struct.unpack_from('<H',dat,8+2*(p*w*h+103*w+63))[0] for p in range(3)]

def query(adrn,ids):
 check(adrn,'adrn');need(len(ids)==56,'finite map55 plus NPC1 source key set')
 out={k:[] for k in ids}
 for off in range(0,len(adrn),80):
  key=struct.unpack_from('<I',adrn,off+76)[0]
  if key not in out:continue
  row=adrn[off:off+80];bitmap,start,size,xoff,yoff,w,h=struct.unpack_from('<IIIiiii',row)
  out[key].append(dict(index=off//80,image_key=key,bitmapno=bitmap,offset=start,size=size,
   xoff=xoff,yoff=yoff,width=w,height=h,record_sha256=sha(row)))
 need(all(len(v)==1 for v in out.values()),'full mixed ADRN exact alias multiplicity, no first/last-wins')
 for rows in out.values():
  r=rows[0];need(r['index']<125996 and 16<r['size']<=315842228-r['offset'] and r['offset']>=0,'whole RD in proven common prefix')
 return {k:v[0] for k,v in out.items()}

def render(images,records,placements,old,parts,npc,origin,size):
 from PIL import Image
 c=Image.new('RGBA',tuple(size),'#11232a')
 for p in placements:
  if old and p['xy'][1]>102:continue
  if not parts and p['layer']=='parts':continue
  r=records[p['image_key']];x,y=p['anchor'];c.alpha_composite(images[p['image_key']],(origin[0]+x+r['xoff'],origin[1]+y+r['yoff']))
 if npc and not old:
  r=records[16048];c.alpha_composite(images[16048],(origin[0]+r['xoff'],origin[1]+r['yoff']))
 return c

def export(r3,r15,tw,destination):
 from PIL import Image
 destination=destination.resolve();need(destination!=ROOT and ROOT not in destination.parents and not destination.exists(),'new private output outside Git')
 bridge=prefix_evidence();npc_validate(json.loads(NPC_REPORT.read_bytes()))
 with package(r3,'r3') as z:adrn=z.read('r2-original-observation/source-adrn_15.bin')
 with package(r15,'r15') as z:
  dat=z.read('originals/1000.DAT');pal=z.read('private-palette.sap');old_r=json.loads(z.read('source-derived-report.json'))
  prior_validate(old_r);need(old_r==json.loads(PRIOR_REPORT.read_bytes()),'preserved R15 exact metadata')
  old_rd=zipfile.ZipFile(io.BytesIO(z.read('private-source-rd-subset.zip')));retained={int(n[:-3]):old_rd.read(n) for n in old_rd.namelist()}
 check(pal,'pal');cells,placements,words=map_cells(dat);ids={p['image_key'] for p in placements}|{16048};records=query(adrn,ids)
 images={};originals={};resources={};retained_keys=set(retained);new_keys=sorted(ids-retained_keys-{16048})
 with package(tw,'tw') as z:ta=z.read('source/data/adrn_1.bin');real=z.read('source/data/real_1.bin')
 check(ta,'tw_adrn');check(real,'tw_real');need(adrn[:len(ta)]==ta,'actual full ADRN prefix comparison repeated now')
 for key,r in records.items():
  rd=real[r['offset']:r['offset']+r['size']];header,px=decode_rd_block(rd,authoritative_block_size=r['size']);w,h,independent=independent_decode(rd)
  need((w,h,independent)==(r['width'],r['height'],px),'independent original RD decoder and geometry')
  if key in retained:need(rd==retained[key],'current exact retained mixed RD equals recovered common prefix')
  rgba=candidate_rgba(px,w,h,initial_rgb(pal));im=Image.frombytes('RGBA',(w,h),rgba);b=io.BytesIO();im.save(b,format='PNG')
  originals[key]=rd;images[key]=im;resources[str(key)]={**r,'RD_sha256':sha(rd),'index_sha256':sha(px),'RGBA_candidate_sha256':sha(rgba),'PNG_sha256':sha(b.getvalue()),
   'source_route':'RETAINED_MIXED_RD_AND_CURRENT_TW_PREFIX_EQUAL' if key in retained else 'FULL_MIXED_ADRN_PLUS_ARCHIVED_EXACT_REAL_PREFIX_AND_CURRENT_TW_RD'}
 r=records[16048];need(r['bitmapno']==5894 and resources['16048']['RD_sha256']=='ce21e49856dde81b79afa5854f400df31393b1d87a08e6357b0eb8fd2e5ad252','exact full-source NPC candidate')
 rects=[(p['anchor'][0]+records[p['image_key']]['xoff'],p['anchor'][1]+records[p['image_key']]['yoff'],records[p['image_key']]['width'],records[p['image_key']]['height']) for p in placements]+[(r['xoff'],r['yoff'],r['width'],r['height'])]
 left=min(q[0] for q in rects);top=min(q[1] for q in rects);right=max(q[0]+q[2] for q in rects);bottom=max(q[1]+q[3] for q in rects);origin=[24-left,24-top];size=[right-left+48,bottom-top+48]
 frames={};pngs={}
 for old in (False,True):
  for parts in (False,True):
   for npc in (False,True):
    name=f'{"old" if old else "expanded"}_parts{int(parts)}_npc{int(npc)}';image=render(images,records,placements,old,parts,npc,origin,size);b=io.BytesIO();image.save(b,format='PNG');pngs[name]=b.getvalue();frames[name]={'RGBA_sha256':sha(image.tobytes()),'PNG_sha256':sha(b.getvalue()),'NPC_candidate_actually_drawn':npc and not old}
 missing_before={k:sum(p['image_key']==k for p in placements) for k in new_keys};need(missing_before==GAPS,'finite19 prior subset gap locations')
 report=dict(schema='stoneage.scene21.original_town1000_common_prefix_observer.r1',scope='PRESERVED_MIXED25_MAP_AND_SOURCE_PREFIX_PIXELS_MODERN_CANDIDATE_NOT_NATIVE_GAME',
  source_packages={k:{'bytes':PINS[k][0],'sha256':PINS[k][1]} for k in ('r3','r15','tw')},prefix_bridge=bridge,
  current_full_mixed_ADRN_prefix_reverified=True,current_mixed_REAL_bytes_read=0,current_TW_REAL_bytes_verified=len(real),
  source_map_sha256=sha(dat),source_palette_sha256=sha(pal),floor=1000,old_bounds=OLD,expanded_bounds=BOUNDS,projection_center=CENTER,
  old_cells=49,expanded_cells=len(cells),additional_cells=28,map_occurrences=len(placements),old_map_occurrences=54,additional_map_occurrences=31,
  map_distinct_source_images=55,retained_source_images=36,recovered_common_prefix_map_images=19,recovered_image_occurrences=24,
  missing_from_prior_subset={str(k):v for k,v in missing_before.items()},remaining_unresolved_map_image_keys=[],
  cells=cells,placements=placements,resources=resources,NPC_source=dict(floor=1000,xy=[63,103],graphic_key=16048,direction_raw=4,functionset='TownPeople',unique_full_ADRN_matches=1),
  NPC_cell_original_three_u16=words,NPC_cell_old_window_covered=False,NPC_image_byte_identity_supported_by_prior_full_prefix=True,
  new_images_independently_decoded=20,all56_RD_decoders_equal=True,current_retained_RD_full_byte_comparisons=36,
  canvas_size=size,origin=origin,frames=frames,scene_order='MODERN_TILE_THEN_PARTS_THEN_OPTIONAL_NPC_NO_NATIVE_OCCLUSION_CLAIM',
  actual_source_browser_verified=False,source_CI_run_id=None,**{k:False for k in FALSE},overall_completion_percent=None)
 destination.mkdir(mode=0o700)
 (destination/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 for n,b in pngs.items():(destination/(n+'.png')).write_bytes(b)
 with zipfile.ZipFile(destination/'private-original-subset.zip','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('1000.DAT',dat);z.writestr('Palet_1.sap',pal)
  for key,rd in originals.items():z.writestr(str(key)+'.rd',rd)
 model={'report':report,'frames':{k:base64.b64encode(v).decode() for k,v in pngs.items()}}
 html=(ROOT/'tools/stoneage_scene21_observer.html').read_text(encoding='utf-8').replace('__PRIVATE_SCENE_JSON__',json.dumps(model,separators=(',',':')))
 (destination/'stoneage-town1000-scene21-observer.html').write_text(html,encoding='utf-8');return report

def validate(r):
 prefix_evidence();prior_validate(json.loads(PRIOR_REPORT.read_bytes()));npc_validate(json.loads(NPC_REPORT.read_bytes()))
 need(r['schema']=='stoneage.scene21.original_town1000_common_prefix_observer.r1' and r['scope']=='PRESERVED_MIXED25_MAP_AND_SOURCE_PREFIX_PIXELS_MODERN_CANDIDATE_NOT_NATIVE_GAME','scope')
 need(all(r[k] is False for k in FALSE) and r['current_mixed_REAL_bytes_read']==0 and r['current_TW_REAL_bytes_verified']==315842228 and r['current_full_mixed_ADRN_prefix_reverified'] is True,'exact historical/current byte-source distinction')
 need(r['prefix_bridge']==prefix_evidence() and r['source_map_sha256']==PINS['map'][1] and r['source_palette_sha256']==PINS['pal'][1],'same parent and prior complete prefix chain')
 need((r['old_bounds'],r['expanded_bounds'],r['projection_center'])==(OLD,BOUNDS,CENTER) and r['floor']==1000,'finite original window')
 need([r[k] for k in ('old_cells','expanded_cells','additional_cells','map_occurrences','old_map_occurrences','additional_map_occurrences','map_distinct_source_images','retained_source_images','recovered_common_prefix_map_images','recovered_image_occurrences')]==[49,77,28,85,54,31,55,36,19,24],'finite coverage conservation')
 need(r['missing_from_prior_subset']=={str(k):v for k,v in GAPS.items()} and r['remaining_unresolved_map_image_keys']==[],'specific19 recovered resources, no invented gap closure')
 need(r['NPC_cell_original_three_u16']==[187,0,49152] and r['NPC_cell_old_window_covered'] is False and r['NPC_image_byte_identity_supported_by_prior_full_prefix'] is True,'NPC source cell and new evidence qualification')
 need(r['NPC_source']==dict(floor=1000,xy=[63,103],graphic_key=16048,direction_raw=4,functionset='TownPeople',unique_full_ADRN_matches=1),'exact archived NPC configuration')
 need(len(r['cells'])==77 and len(r['placements'])==85 and len(r['resources'])==56 and len(r['frames'])==8,'complete bounded records')
 need(r['actual_source_browser_verified'] is False and r['source_CI_run_id'] is None and r['overall_completion_percent'] is None,'no false original browser/source CI/completion')
 need(r['new_images_independently_decoded']==20 and r['all56_RD_decoders_equal'] is True and r['current_retained_RD_full_byte_comparisons']==36,'actual pixel decode and retained-byte witnesses')
 need(sha(json.dumps(r,sort_keys=True,separators=(',',':')).encode())=='0fc157bce499520179d6ae12f7dcfb986107068706abcf1ef1fb81a25557899a','complete immutable source-derived map/record/pixel metadata')
 return {'source_map_cells':77,'source_map_image_occurrences':85,'map_source_images':55,'new_map_images':19,'NPC_image_candidates':1,'original_world_entered':False}

def validate_actual_replay(a,r):
 need(a['schema']=='stoneage.scene21.independent_actual_source_pixel_replay.r1' and a['source_report_sha256']==sha(REPORT.read_bytes()),'actual private replay source identity')
 need(a['actual_original_RD_images_verified']==56 and a['full_canvas_states_verified']==8 and a['independent_DAT_cells']==77 and a['canvas_size']==r['canvas_size'],'complete independent source/pixel counts')
 need(a['frames']=={k:v['RGBA_sha256'] for k,v in r['frames'].items()},'all full canvas pixel hashes')
 need(a['assistant_actual_composite_viewed'] is True and a['viewed_frame']=='expanded_parts1_npc1' and a['viewed_PNG_sha256']==r['frames'][a['viewed_frame']]['PNG_sha256'],'actual source candidate image viewed')
 need(a['actual_source_browser_verified'] is False and a['original_world_entered'] is False,'source image view not browser/native game')
 return {'independent_original_RD_images':56,'full_canvas_states':8,'actual_candidate_image_viewed':True}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('r3','r15','tw','private-output'):p.add_argument('--'+name,type=Path)
 a=p.parse_args()
 if a.private_output:
  need(a.r3 and a.r15 and a.tw,'three original private packages required');r=export(a.r3,a.r15,a.tw,a.private_output)
 else:r=json.loads(REPORT.read_bytes())
 result=validate(r)
 if not a.private_output:result.update(validate_actual_replay(json.loads((REPORT.parent/'STONEAGE-SCENE21-ACTUAL-PIXEL-ACCEPTANCE-R1.json').read_bytes()),r))
 print(json.dumps(result,sort_keys=True))
