"""Integrate two accepted private observations; no new historical source or transaction."""
from __future__ import annotations
import argparse,base64,hashlib,io,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE25-ROOM-SHOP-INTEGRATION-R1.json'
R14=ROOT/'research/recovered/STONEAGE-SCENE14-ROOM-SHOP-SOURCE-R1.json'
R24=ROOT/'research/recovered/STONEAGE-SCENE24-SHOP-ITEM-IMAGES-R1.json'
PINS={
 'room_archive':(351231,'7684267ab528d13ceecb23a25632543ae839225607cbda702a32736e4c4d366a'),
 'items_archive':(375924,'194d93d6f21dcfd906384b23ca122c3aa42d57067d92ea6a0e171b874ef422c7'),
 'room_html':(85928,'4c564b41a4daea15a6a3a6760e87b336062d7c1ec4589ebdaedea78e7bdcc105'),
 'room_report':(10317,'b6311a35777501f6cc0cfaf360ad82ed6077d388a6fd0b6ddc39ef57628ac985'),
 'items_report':(11936,'9edbd464e100c536c2814a1ae69d16546f59fc8352e4f015eb5336a5994e6a2c')}
FALSE=('new_historical_source_acquired','original_source_browser_verified','original_server_executed',
 'original_world_entered','original_shop_UI_authenticated','native_imagenumber_namespace_verified',
 'same_deployed_build_authenticated','original_transaction_verified','inventory_or_gold_modified',
 'copyrighted_assets_published')

def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(b,key):need((len(b),sha(b))==PINS[key],'accepted parent identity: '+key)
def unpack_html(b):
 return json.loads(b.split(b'<script id="evidence" type="application/json">',1)[1].split(b'</script>',1)[0])
def draw_body(s):return s.split('function draw(){',1)[1].split('function inspect(){',1)[0]

def validate_binding(room,r14,r24):
 pin(R14.read_bytes(),'room_report');pin(R24.read_bytes(),'items_report')
 need(r14==json.loads(R14.read_bytes()) and r24==json.loads(R24.read_bytes()),'immutable source reports')
 need(room['floor']==1001 and room['source_dat_sha256']==r14['source_members']['client-map/1001.dat']['sha256'],'same room DAT')
 need(room['original_game_world_entered'] is False,'observer is not original world')
 need(r14['npc']['borncorner']==[17,13,17,13] and r14['npc']['graphicname']==16017,'one authored shop binding')
 need(len(room['sprites'])==10 and len(room['R6_native_sorted_queue_numbers'])==len(room['placements']),'finite room images and queue')
 need(r14['selected_items']==[x['source_row'] for x in r24['items']],'exact item rows across observations')
 need([x['id'] for x in r24['items']]==[0,4,10],'zero valid, original order')
 need([x['alias_candidate']['bitmapno'] for x in r24['items']]==[6006,6005,5986],'alias candidates only')
 need(r24['native_imagenumber_namespace_verified'] is False,'candidate namespace remains unverified')

def validate(r):
 need(r['schema']=='stoneage.scene25.accepted_observation_integration.r1','schema')
 need(r['scope']=='MODERN_OFFLINE_ROOM_SHOP_SOURCE_READER_NO_NEW_HISTORICAL_SOURCE','scope')
 need(r['parents']=={k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},'accepted parent custody')
 a=json.loads(R14.read_bytes());b=json.loads(R24.read_bytes())
 need(r['binding']==dict(floor=1001,xy=[17,13],graphicname=16017,npc_bitmap=5863,template='npcgen_shop',functionset='ItemShop',argument_file='genout/ss_1001_17_13'),'exact static binding')
 expected=[dict(id=x['id'],name_original=x['name_original'],imagenumber=x['imagenumber'],candidate_bitmap=x['alias_candidate']['bitmapno'],source_row_sha256=x['source_row']['row_sha256'],PNG_sha256=x['alias_candidate']['palette_candidates']['1']['PNG_sha256'],RGBA_sha256=x['alias_candidate']['palette_candidates']['1']['RGBA_sha256'])for x in b['items']]
 need(r['items']==expected and [x['id']for x in a['selected_items']]==[0,4,10],'three source rows and candidate images')
 need(r['palette_candidate']=='Palet_1.sap' and r['palette_candidate_is_native_active_palette'] is False,'candidate palette only')
 need(r['room_PNGs_preserved']==10 and r['NPC_PNGs_preserved']==1 and r['added_item_PNGs']==3 and r['total_PNGs']==14,'bounded image set')
 need(r['world_draw_body_unchanged'] is True and r['world_draw_body_sha256']==sha(draw_body((ROOT/'tools/scene-room-shop-viewer-r14.html').read_text()).encode()),'identical room draw implementation')
 need(r['room_model_sha256']=='aee041fcba9e2192b5c7a9c46f279fcccf1597386868fe0422943b80307c2e25','immutable private model fingerprint')
 need(r['reader_interactions']==['explicit_open','candidate_image_click','close','Escape','select_source_row','reset_closes_reader'],'finite modern reader controls')
 need(r['computed_runtime_prices'] is None and r['source_Action_run_id'] is None and r['overall_completion_percent'] is None,'no runtime/source CI promotion')
 need(all(r[k] is False for k in FALSE),'historical boundaries')
 need(r['original_assets_and_scripts_location']=='PRIVATE_ARCHIVE_ONLY','private original material')
 return dict(source_rows=3,original_PNGs=14,room_draw_unchanged=True,new_historical_sources=0,original_world_entered=False)

def render(pack):
 t=(ROOT/'tools/stoneage_scene25_observer.html').read_text()
 need(t.count('"PRIVATE_PACK_PLACEHOLDER"')==1,'template marker')
 old=(ROOT/'tools/scene-room-shop-viewer-r14.html').read_text()
 need(draw_body(t)==draw_body(old),'world drawing must stay byte-identical')
 return t.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))

def validate_actual(a,r):
 need(sha(json.dumps(a,sort_keys=True,separators=(',',':')).encode())=='43885130d672331197a3cf22de9a2eb0ee711bdaae222262e92aebf14d496174','exact independent private replay')
 need(a['integration_report_sha256']==sha(REPORT.read_bytes()),'integration report identity')
 need(a['original_PNGs']==14 and a['original_item_rows_reparsed']==3 and a['integer_room_frames_equal_prior_browser']==4 and a['new_integer_card_frames']==3,'finite actual integration coverage')
 prior=json.loads((ROOT/'research/recovered/STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes())
 for frame in a['references']['room']:
  need(frame['RGBA_sha256']==next(x['canvas_sha256']for x in prior['browser_states']if x['label']==frame['label']),'unchanged prior accepted room pixels')
 need(len(a['assets'])==14 and [x['PNG_sha256']for x in a['assets'][-3:]]==[x['PNG_sha256']for x in r['items']],'actual image identities')
 need(a['original_source_browser_verified'] is False and a['original_world_entered'] is False and a['original_transaction_verified'] is False,'local Pillow is not original-image browser/runtime')
 return dict(original_images=14,old_room_frames=4,new_card_frames=3,source_browser=False)

def validate_browser(a):
 from tools.stoneage_scene25_fixture import build
 need(a['schema']=='stoneage.scene25.synthetic_room_shop_browser.r1' and a['scope']=='SYNTHETIC_PIXELS_AND_TEXT_ONLY','synthetic browser scope')
 need(a['loaded_images']==14 and a['room_frames']==4 and a['item_card_frames']==3,'synthetic finite coverage')
 ref=build()['item_observation']['synthetic_references'];need(a['frames']==ref['room']+ref['cards'],'all seven synthetic canvas hashes')
 for flag in ['all7_complete_canvas_hashes_equal','reader_open_close_Escape_reset_verified','explicit_button_and_candidate_image_click_verified','outside_and_hidden_NPC_click_do_not_open','ID0_and_last_source_row_verified','other_stock_ID_refused','room_pixels_unchanged_during_reader_operations','source_model_unchanged']:need(a[flag] is True,'browser interaction '+flag)
 need(a['JS_errors']==[] and a['external_requests']==[],'browser errors or external IO')
 need(a['original_source_browser_verified'] is False and a['original_world_entered'] is False and a['original_transaction_verified'] is False,'synthetic execution not original runtime')
 return dict(synthetic_images=14,canvas_states=7,original_source_browser=False)

def export(room_archive,items_archive,target):
 from PIL import Image
 target=target.resolve();need(ROOT!=target and ROOT not in target.parents and not target.exists(),'new private output outside Git')
 rb=room_archive.read_bytes();ib=items_archive.read_bytes();pin(rb,'room_archive');pin(ib,'items_archive')
 with zipfile.ZipFile(io.BytesIO(rb))as rz,zipfile.ZipFile(io.BytesIO(ib))as iz:
  rh=rz.read('stoneage-room-r14-shop-observer.html');pin(rh,'room_html');rp=rz.read('source-derived-report.json');pin(rp,'room_report')
  ip=iz.read('source-derived-report.json');pin(ip,'items_report');pack=unpack_html(rh)
  ih=iz.read('StoneAge-SCENE24-item-observer.html');imodel=unpack_html(ih);r14=json.loads(rp);r24=json.loads(ip)
  need(pack['source']==r14 and imodel['report']==r24,'page report bindings');validate_binding(pack['room'],r14,r24)
  images={};items=[]
  for item in r24['items']:
   row=item['alias_candidate'];key=str(item['id']);png64=imodel['images']['1'][str(row['bitmapno'])];png=base64.b64decode(png64,validate=True);im=Image.open(io.BytesIO(png)).convert('RGBA')
   need((im.width,im.height)==(row['width'],row['height']) and sha(png)==row['palette_candidates']['1']['PNG_sha256'] and sha(im.tobytes())==row['palette_candidates']['1']['RGBA_sha256'],'unchanged candidate source PNG and RGBA')
   images[key]=png64;items.append(dict(id=item['id'],name_original=item['name_original'],imagenumber=item['imagenumber'],candidate_bitmap=row['bitmapno'],source_row_sha256=item['source_row']['row_sha256'],PNG_sha256=sha(png),RGBA_sha256=sha(im.tobytes())))
  report=dict(schema='stoneage.scene25.accepted_observation_integration.r1',scope='MODERN_OFFLINE_ROOM_SHOP_SOURCE_READER_NO_NEW_HISTORICAL_SOURCE',parents={k:dict(bytes=v[0],sha256=v[1])for k,v in PINS.items()},binding=dict(floor=1001,xy=[17,13],graphicname=16017,npc_bitmap=5863,template='npcgen_shop',functionset='ItemShop',argument_file='genout/ss_1001_17_13'),items=items,palette_candidate='Palet_1.sap',palette_candidate_is_native_active_palette=False,room_model_sha256=sha(canonical(pack['room'])),room_PNGs_preserved=10,NPC_PNGs_preserved=1,added_item_PNGs=3,total_PNGs=14,world_draw_body_unchanged=True,world_draw_body_sha256=sha(draw_body(rh.decode()).encode()),reader_interactions=['explicit_open','candidate_image_click','close','Escape','select_source_row','reset_closes_reader'],computed_runtime_prices=None,source_Action_run_id=None,overall_completion_percent=None,original_assets_and_scripts_location='PRIVATE_ARCHIVE_ONLY',**{k:False for k in FALSE})
  validate(report);pack['item_observation']=dict(report=report,images=images,synthetic_fixture=False)
  target.mkdir(parents=True,mode=0o700);(target/'StoneAge-SCENE25-room-shop-observer.html').write_text(render(pack));(target/'integration-report.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
  # Preserve the finite prior image/config evidence for reproducible private custody.
  (target/'parent-room-observation.zip').write_bytes(rb);(target/'parent-item-observation.zip').write_bytes(ib)
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--room-archive',type=Path);p.add_argument('--items-archive',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
 r=export(a.room_archive,a.items_archive,a.output_dir)if a.room_archive else json.loads(REPORT.read_bytes());result=validate(r)
 if not a.room_archive:
  result['actual_replay']=validate_actual(json.loads((ROOT/'research/recovered/STONEAGE-SCENE25-ACTUAL-PIXEL-REPLAY-R1.json').read_bytes()),r)
  browser=ROOT/'research/recovered/STONEAGE-SCENE25-SYNTHETIC-BROWSER-R1.json'
  if browser.exists():result['synthetic_browser']=validate_browser(json.loads(browser.read_bytes()))
 print(json.dumps(result,ensure_ascii=False))
