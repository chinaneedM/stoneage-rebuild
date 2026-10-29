"""Three preserved shop rows -> numeric ADRN alias candidates + literal-ID controls.
No original transaction, same-deployment selector, or original UI is executed.
"""
from __future__ import annotations
import argparse,base64,csv,functools,gzip,hashlib,io,json,struct,zipfile,zlib
from pathlib import Path
from tools.stoneage_scene14_room_shop import MEMBERS,IDS,blocks
from tools.stoneage_preserved_item_shop_r44 import parse_items,arg_fields,inventory_tokens,INDEX
from tools.stoneage_private_scene_graphic_join_r1 import resolve_ids
from tools.stoneage_private_scene_palette_r3 import candidate_rgba
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_tw10_palette import initial_rgb
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE24-SHOP-ITEM-IMAGES-R1.json'
PRIOR=ROOT/'research/recovered/STONEAGE-SCENE14-ROOM-SHOP-SOURCE-R1.json'
PRIOR_SHA='b6311a35777501f6cc0cfaf360ad82ed6077d388a6fd0b6ddc39ef57628ac985'
PREFIX=ROOT/'research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt'
PREFIX_SHA='3b47bebc704e8a2245b6bb9ec366f3d76d797b54378142bf1618fe5058ff9b4c'
SERVER={k:v for k,v in MEMBERS.items()if k!='client-map/1001.dat'}
CLIENT={
 'adrn_1.bin':(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'real_1.bin':(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
 'Palet_0.sap':(708,'89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf'),
 'Palet_1.sap':(708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0')}
MIXED_ADRN=(18765120,'92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74')
PIXEL_MANIFEST_SHA='69188a617b214418402dbb7283d0dde86ccaf1a822eea48401510eeb5f7b9d61'
PAIRS=((0,20033,6006),(4,20032,6005),(10,20013,5986))
FALSE=('native_imagenumber_namespace_verified','same_official_deployed_build_authenticated',
 'original_world_entered','original_server_executed','original_transaction_verified',
 'original_shop_UI_verified','native_palette_selection_verified',
 'source_Action_executed','original_source_browser_verified','copyrighted_assets_published',
 'current_full_mixed_REAL_prefix_reverification')
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise ValueError(m)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def source_prior():
 b=PRIOR.read_bytes();need(sha(b)==PRIOR_SHA,'existing R14 source pin');return json.loads(b)
def prefix_proof():
 b=PREFIX.read_bytes();need(sha(b)==PREFIX_SHA,'old complete-prefix proof pin');need(b'common_prefix_bytes=315842228' in b,'complete same-parent REAL prefix');return dict(path=str(PREFIX.relative_to(ROOT)),bytes=len(b),sha256=sha(b),REAL_prefix_bytes=315842228,mixed_REAL_sha256='c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d',prior_verified_complete_byte_comparison=True)
@functools.lru_cache(maxsize=1)
def old_bitmaps():
 wanted={n for _,v,n in PAIRS}|{v for _,v,n in PAIRS};out={}
 with gzip.open(ROOT/'research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz','rt')as f:
  for row in csv.DictReader(f,delimiter='\t'):
   n=int(row['bitmapno'])
   if n in wanted:need(n not in out,'old physical duplicate');out[n]=row
 need(set(out)==wanted,'six archived source rows');return out

def validate(r):
 need(r['schema']=='stoneage.scene24.three_shop_image_candidates.r1','schema')
 need(r['scope']=='PRESERVED_MIXED25_ITEM_ROWS_NUMERIC_ALIAS_CANDIDATES_NOT_TW10_ITEM_MASTER_OR_RUNTIME','scope')
 need(all(r[k] is False for k in FALSE),'no historical/runtime/publication promotion')
 need(r['source_Action_run_id'] is None and r['computed_runtime_prices'] is None and r['overall_completion_percent'] is None,'no invented run/price/completion')
 need(r['R14_source_sha256']==PRIOR_SHA and r['prefix_bridge']==prefix_proof(),'source bridge')
 need(r['source_members']=={k:dict(bytes=n,sha256=h)for k,(n,h)in SERVER.items()},'all four server sources')
 need(r['client_source_files']=={k:dict(bytes=n,sha256=h)for k,(n,h)in CLIENT.items()}and r['mixed_ADRN']==dict(bytes=MIXED_ADRN[0],sha256=MIXED_ADRN[1]),'all original resource source pins')
 need(r['current_full_mixed_ADRN_prefix_reverified']is True and r['current_mixed_REAL_bytes_read']==0,'new ADRN equality vs prior-only REAL equality')
 need(r['source_namespace_grade']=='EXACT_NUMERIC_ADRN_PLUS76_ALIAS_JOIN_ONLY_NOT_NATIVE_DRAW_PROOF','bounded namespace')
 need(len(r['items'])==3 and [x['id']for x in r['items']]==[0,4,10],'original order including valid zero')
 prior=source_prior();old=old_bitmaps();wanted=[]
 for item,expected,(itemid,key,physical)in zip(r['items'],prior['selected_items'],PAIRS):
  need(item['source_row']==expected and item['id']==itemid,'exact original row including numeric fields/name hash')
  need(item['imagenumber']==key,'exact original imagenumber')
  a=item['alias_candidate'];c=item['literal_bitmap_control']
  need((a['bitmapno'],a['alias_value'],a['alias_matches_in_full_mixed_ADRN'])==(physical,key,1),'unique full mixed alias candidate')
  need((c['bitmapno'],c['alias_value'],c['physical_matches_in_full_mixed_ADRN'])==(key,0,1),'literal ID is a separate namespace')
  for row in (a,c):
   o=old[row['bitmapno']];need([row[k]for k in ['index','offset','size','xoff','yoff','width','height']]==[int(o[k])for k in ['index','adder','size','xoff','yoff','width','height']],'original source geometry')
   need(row['RD_sha256']==o['rd_block_sha256'] and row['index']<125996 and row['offset']+row['size']<=315842228,'source RD identity and entire proven prefix range')
   wanted.append(row['bitmapno'])
  need(a['bitmapno']!=c['bitmapno'] and a['RD_sha256']!=c['RD_sha256'],'same integer is not same source art')
 need(r['original_stock_count']==17 and r['whole_item_table_rows']==13252,'original inventory/table counts')
 need(r['selected_images']==6 and r['palette_candidate_views']==12,'three candidates plus three literal controls, two palettes')
 rows=[y for x in r['items']for y in [x['alias_candidate'],x['literal_bitmap_control']]]
 need(sha(canonical(rows))==PIXEL_MANIFEST_SHA,'immutable actual original pixel/record metadata')
 return dict(items=3,ordered_ids=[0,4,10],alias_candidate_bitmaps=[6006,6005,5986],literal_controls=[20033,20032,20013],original_world_entered=False)

def source_items(server):
 originals={}
 for path,pin in SERVER.items():
  b=(server/Path(path).name).read_bytes();need((len(b),sha(b))==pin,'whole original member '+path);originals[path]=b
 create=blocks(originals['npc/genout/shop_m.create'],b'NPCCREATE');chosen=[b for b in create if b['fields'].get('floorid')==b'1001'and b['fields'].get('borncorner')==b'17,13,17,13'];need(len(chosen)==1 and chosen[0]['fields']['enemy']==b'npcgen_shop|file:genout/ss_1001_17_13','one exact original shop dependency')
 templates=blocks(originals['npc/genout/npcgen.template'],b'NPCTEMPLATE');chosen=[t for t in templates if t['fields'].get('templatename')==b'npcgen_shop'];need(len(chosen)==1 and chosen[0]['fields']['functionset']==b'ItemShop','one exact original template')
 args=arg_fields(originals['npc/genout/ss_1001_17_13']);tokens=inventory_tokens(args['itemlist']);need(tokens==[[n,n]for n in IDS],'all17 original item positions')
 rows,count=parse_items(originals['itemset.txt']);need(count==13252,'original whole table count');prior=source_prior();items=[]
 for itemid,old in zip(IDS[:3],prior['selected_items']):
  line,offset,body,cols=rows[itemid];name=cols[INDEX['name']];need(name.decode('cp950')==name.decode('big5'),'source name codec consensus')
  row=dict(id=itemid,physical_line=line,byte_offset=offset,row_sha256=sha(body),name_original=name.decode('cp950'),name_raw_sha256=sha(name),numeric_fields={k:int(cols[INDEX[k]])for k in ['imagenumber','cost','level','type']});need(row==old,'new exact original rows vs R14');items.append(row)
 return items

def record(raw,index):
 off=index*80;values=struct.unpack_from('<IIIiiii',raw,off);alias=struct.unpack_from('<I',raw,off+76)[0];return dict(zip(['bitmapno','offset','size','xoff','yoff','width','height'],values),index=index,alias_value=alias,record_sha256=sha(raw[off:off+80]))

def export(server,client,mixed_file,out):
 from PIL import Image,ImageDraw
 out=out.resolve();need(out!=ROOT and ROOT not in out.parents and not out.exists(),'new private output outside Git');items=source_items(server);mixed=mixed_file.read_bytes();need((len(mixed),sha(mixed))==MIXED_ADRN,'whole original mixed ADRN')
 original={}
 for n,pin in CLIENT.items():
  b=(client/n).read_bytes();need((len(b),sha(b))==pin,'whole original '+n);original[n]=b
 need(mixed[:len(original['adrn_1.bin'])]==original['adrn_1.bin'],'actual whole ADRN prefix equality')
 keys={key for _,key,_ in PAIRS};aliases=resolve_ids(mixed,keys,763908374);physical={key:[]for key in keys}
 for index in range(len(mixed)//80):
  no=struct.unpack_from('<I',mixed,index*80)[0]
  if no in physical:physical[no].append(index)
 need(all(len(aliases[k])==len(physical[k])==1 for k in keys),'all source namespace multiplicities explicit and unique')
 rgb={str(i):initial_rgb(original['Palet_'+str(i)+'.sap'])for i in (0,1)};images={'0':{},'1':{}};rdblocks={};records={};out.mkdir(mode=0o700,parents=True)
 for item,(_,key,_)in zip(items,PAIRS):
  candidate=record(mixed,aliases[key][0]['index']);candidate['alias_matches_in_full_mixed_ADRN']=1
  control=record(mixed,physical[key][0]);control['physical_matches_in_full_mixed_ADRN']=1
  for row in (candidate,control):
   need(row['index']<125996 and 0<=row['offset']<=315842228-row['size'],'qualified whole common source prefix');need(mixed[row['index']*80:row['index']*80+80]==original['adrn_1.bin'][row['index']*80:row['index']*80+80],'exact current raw record equality')
   rd=original['real_1.bin'][row['offset']:row['offset']+row['size']];h,px=decode_rd_block(rd,authoritative_block_size=row['size']);need((h['width_s'],h['height_s'])==(row['width'],row['height']),'actual RD dimensions')
   n=str(row['bitmapno']);rdblocks[n+'.rd']=rd;row.update(RD_sha256=sha(rd),indices_sha256=sha(px),palette_candidates={})
   for palette,colors in rgb.items():
    rgba=candidate_rgba(px,row['width'],row['height'],colors);im=Image.frombytes('RGBA',(row['width'],row['height']),rgba);buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue();row['palette_candidates'][palette]=dict(RGBA_sha256=sha(rgba),PNG_sha256=sha(png));images[palette][n]=base64.b64encode(png).decode()
   records[row['bitmapno']]=row
  item.update(source_row=dict(item),imagenumber=key,alias_candidate=candidate,literal_bitmap_control=control)
  # Keep source_row identical to the earlier finite R14 projection.
  item['source_row']={k:item['source_row'][k]for k in source_prior()['selected_items'][0]}
 r=dict(schema='stoneage.scene24.three_shop_image_candidates.r1',scope='PRESERVED_MIXED25_ITEM_ROWS_NUMERIC_ALIAS_CANDIDATES_NOT_TW10_ITEM_MASTER_OR_RUNTIME',R14_source_sha256=PRIOR_SHA,prefix_bridge=prefix_proof(),source_members={k:dict(bytes=n,sha256=h)for k,(n,h)in SERVER.items()},client_source_files={k:dict(bytes=n,sha256=h)for k,(n,h)in CLIENT.items()},mixed_ADRN=dict(bytes=MIXED_ADRN[0],sha256=MIXED_ADRN[1]),current_full_mixed_ADRN_prefix_reverified=True,current_mixed_REAL_bytes_read=0,source_namespace_grade='EXACT_NUMERIC_ADRN_PLUS76_ALIAS_JOIN_ONLY_NOT_NATIVE_DRAW_PROOF',items=items,original_stock_count=17,whole_item_table_rows=13252,selected_images=6,palette_candidate_views=12,source_Action_run_id=None,computed_runtime_prices=None,overall_completion_percent=None,**{k:False for k in FALSE})
 validate(r)
 (out/'source-derived-report.json').write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 with zipfile.ZipFile(out/'private-source-image-subset.zip','w',zipfile.ZIP_DEFLATED)as z:
  for n,b in rdblocks.items():z.writestr(n,b)
  for n in ['Palet_0.sap','Palet_1.sap']:z.writestr(n,original[n])
  for n,row in records.items():z.writestr(str(n)+'.adrn',mixed[row['index']*80:row['index']*80+80])
 canvases=[];sheet=Image.new('RGBA',(960,780),'#142129');draw=ImageDraw.Draw(sheet)
 for mode in ('alias','literal'):
  for palette in ('0','1'):
   for scale in (2,4):
    for i,item in enumerate(items):
     row=item['alias_candidate'if mode=='alias'else'literal_bitmap_control'];im=Image.open(io.BytesIO(base64.b64decode(images[palette][str(row['bitmapno'])]))).convert('RGBA');c=Image.new('RGBA',(320,360),'#142129');big=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);x=(320-big.width)//2;y=(360-big.height)//2;need(x>=0 and y>=0,'finite modern card bounds');c.alpha_composite(big,(x,y));canvases.append(dict(item=item['id'],mode=mode,palette=palette,scale=scale,RGBA_sha256=sha(c.tobytes())))
     if palette=='1'and scale==4:
      yy=20+(0 if mode=='alias' else 390);sheet.alpha_composite(c,(i*320,yy));draw.text((i*320+8,yy-16),'item '+str(item['id'])+' '+mode+' -> '+str(row['bitmapno']),fill='#ead394')
 buf=io.BytesIO();sheet.save(buf,format='PNG');(out/'StoneAge-SCENE24-item-namespace-candidates.png').write_bytes(buf.getvalue());model=dict(report=r,images=images,canvas_hashes=canvases,synthetic_fixture=False)
 template=(ROOT/'tools/stoneage_scene24_observer.html').read_text();need(template.count('__SCENE24_MODEL__')==1,'one private model marker');(out/'StoneAge-SCENE24-item-observer.html').write_text(template.replace('__SCENE24_MODEL__',json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')))
 rows=[y for x in items for y in [x['alias_candidate'],x['literal_bitmap_control']]];print(json.dumps(dict(items=3,images=6,canvases=24,pixel_manifest_sha256=sha(canonical(rows)))))
 return r

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--server',type=Path);p.add_argument('--client',type=Path);p.add_argument('--mixed-adrn',type=Path);p.add_argument('--private-output',type=Path);a=p.parse_args()
 if a.server:
  need(all([a.client,a.mixed_adrn,a.private_output]),'all private inputs needed');export(a.server,a.client,a.mixed_adrn,a.private_output)
 else:print(json.dumps(validate(json.loads(REPORT.read_bytes())),sort_keys=True))
if __name__=='__main__':main()
