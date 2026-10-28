"""One authored doorway pair and actual source pixels; no original world/server.
Private-only exporter. Public validation never loads proprietary files.
"""
from __future__ import annotations
import argparse,base64,copy,hashlib,io,json,re,struct,zipfile
from pathlib import Path
from tools.stoneage_scene14_room_shop import blocks,public_block
from tools.stoneage_private_scene_actor_r7 import PINS,authenticate,need,sha
from tools.stoneage_private_scene_graphic_join_r1 import resolve_ids
from tools.stoneage_private_scene_palette_r3 import candidate_rgba,sweep
from tools.stoneage_tw10_palette import initial_rgb
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE15-DOORWAY-SOURCE-R1.json'
DERIVED_SHA='3547a6d697d08aedb3ecd0702844c08eb6256ce9e560fd9b3b0c90fe011638a1'
WARP_PIN=(24588,'859ff2ed23baadb20382508874cd3a63e603b84c7205c6f5d8998229f4f4c8b1')
TEMPLATE_PIN=(4950,'0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3')
MAP_PINS={1001:(5408,'62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90'),1000:(153608,'94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e')}
CENTERS={1001:(10,15),1000:(63,99)}
PRIOR_HTML_SHA='ae82aa61120b08a14c9e1b3f3b939a36a9649dba97af555ed1a0ed274f36d99f'
FALSE=('original_client_executed','original_server_executed','original_world_entered','original_warp_runtime_verified','same_deployed_build_authenticated','official_tw10_identity_authenticated','native_occlusion_or_camera_verified','native_player_movement_or_collision_verified','original_assets_in_public_git')


def doorway(warp,template):
    need((len(warp),sha(warp))==WARP_PIN,'whole original warp source')
    need((len(template),sha(template))==TEMPLATE_PIN,'whole original template source')
    gs=blocks(warp,b'NPCCREATE');selected=[]
    for floor,xy,target,dst in [(1001,(10,15),1000,(63,99)),(1000,(63,99),1001,(10,15))]:
        matches=[g for g in gs if g['fields'].get('floorid')==str(floor).encode() and g['fields'].get('borncorner')==(','.join(map(str,xy+xy))).encode()]
        need(len(matches)==1,'unique selected authored doorway, not neighboring door')
        g=matches[0];f=g['fields'];need(f['enemy']==f'npcgen_warp|{target}|{dst[0]}|{dst[1]}'.encode(),'exact original target tuple')
        selected.append({'source_floor':floor,'source_xy':list(xy),'destination_floor':target,'destination_xy':list(dst),'raw_time':int(f['time']),'source_block':public_block(g)})
    ts=[g for g in blocks(template,b'NPCTEMPLATE') if g['fields'].get('templatename')==b'npcgen_warp'];need(len(ts)==1 and ts[0]['fields']['functionset']==b'Warp','unique original Warp template')
    return selected,public_block(ts[0]),len(gs)


def map_view(raw,floor):
    need((len(raw),sha(raw))==MAP_PINS[floor],'whole original DAT identity')
    w,h=struct.unpack_from('<II',raw);need((w,h)==((30,30) if floor==1001 else (160,160)) and len(raw)==8+6*w*h,'source map extent')
    x,y=CENTERS[floor];radius=3;need(0<=x-radius<=x+radius<w and 0<=y-radius<=y+radius<h,'both source viewports bounded')
    values=struct.unpack_from('<'+str(3*w*h)+'H',raw,8);placements=[]
    for layer in (0,1):
        for rx,ry in sweep(7,7):
            gx,gy=x-radius+rx,y-radius+ry;no=values[layer*w*h+gy*w+gx]
            if no<=99:continue
            placements.append({'layer':'tile' if layer==0 else 'parts','source_xy':[gx,gy],'map_id':no,'anchor_relative':[(gx-x+gy-y)*32,((gy-y)-(gx-x))*24]})
    return {'floor':floor,'width':w,'height':h,'source_DAT_sha256':sha(raw),'center_xy':[x,y],'inclusive_viewport':[x-radius,y-radius,x+radius,y+radius],
      'tile_occurrences':sum(p['layer']=='tile' for p in placements),'parts_occurrences':sum(p['layer']=='parts' for p in placements),'placements':placements,
      'original_three_u16_at_door_cell':[values[p*w*h+y*w+x] for p in range(3)]}


def manual_step(state,dx,dy):
    need(set(state)=={'floor','x','y'} and all(type(v) is int for v in state.values()) and type(dx) is type(dy) is int,'integer modern grid state')
    need(state['floor'] in CENTERS and (dx,dy) in ((1,0),(-1,0),(0,1),(0,-1)),'bounded observer single grid step')
    cx,cy=CENTERS[state['floor']];x,y=state['x']+dx,state['y']+dy
    need(cx-3<=x<=cx+3 and cy-3<=y<=cy+3,'outside modern observation window')
    return {'floor':state['floor'],'x':x,'y':y}


def transition(state,doors):
    need(set(state)=={'floor','x','y'} and all(type(v) is int for v in state.values()),'exact integer observer state')
    matches=[d for d in doors if state=={'floor':d['source_floor'],'x':d['source_xy'][0],'y':d['source_xy'][1]}]
    need(len(matches)==1,'no exact selected source doorway here')
    d=matches[0];need(d['destination_floor'] in CENTERS and tuple(d['destination_xy'])==CENTERS[d['destination_floor']],'bounded original destination')
    return {'floor':d['destination_floor'],'x':d['destination_xy'][0],'y':d['destination_xy'][1]}


def validate(r):
    need(sha(json.dumps(r,sort_keys=True,separators=(',',':')).encode())==DERIVED_SHA,'immutable original-source-derived viewport/bitmap metadata')
    need(r['schema']=='stoneage.scene15.authored_doorway_source_observer.r1','schema')
    need(r['scope']=='PRESERVED_MIXED25_STATIC_DOORWAY_PLUS_MODERN_OFFLINE_OBSERVER_NOT_ORIGINAL_GAME','scope')
    need(r['source_warp']=={'bytes':WARP_PIN[0],'sha256':WARP_PIN[1]} and r['source_template']=={'bytes':TEMPLATE_PIN[0],'sha256':TEMPLATE_PIN[1]},'actual original files')
    doors=r['doorway_pair'];need(len(doors)==2,'one finite doorway pair')
    for d,expected in zip(doors,[(1001,[10,15],1000,[63,99],1,229,335,'d35da32a65e7794acf619c4c959c81dcefc0a433c7d78a0c838b9d0c278c3085'),(1000,[63,99],1001,[10,15],0,112,218,'d0b4f955cc6afe909579a3bdb555f549a5fc00e23f5e3555d6041f2dd2028f79')]):
        sf,sxy,df,dxy,ordinal,start,end,digest=expected
        need((d['source_floor'],d['source_xy'],d['destination_floor'],d['destination_xy'],d['raw_time'])==(sf,sxy,df,dxy,0),'exact original doorway pair')
        b=d['source_block'];need((b['ordinal'],b['byte_start'],b['byte_end'],b['block_sha256'])==(ordinal,start,end,digest),'original config spans')
    need(r['template_block']['ordinal']==21 and r['template_block']['block_sha256']=='90fb41954b3e7fc8f168a649163348fb91c3a0f9b9589eb6ffad5391e208a56d','original Warp template')
    need(r['functionset']=='Warp' and r['original_create_blocks']==209,'source metadata, not209 restored doors')
    need(len(r['views'])==2 and [v['floor'] for v in r['views']]==[1001,1000],'two exact private map viewports')
    ids=set()
    for v in r['views']:
        floor=v['floor'];x,y=CENTERS[floor];need(v['center_xy']==[x,y] and v['inclusive_viewport']==[x-3,y-3,x+3,y+3] and v['source_DAT_sha256']==MAP_PINS[floor][1],'source viewport')
        need(v['tile_occurrences']==sum(p['layer']=='tile' for p in v['placements']) and v['parts_occurrences']==sum(p['layer']=='parts' for p in v['placements']),'source layer occurrence conservation')
        for p in v['placements']:
            gx,gy=p['source_xy'];need(x-3<=gx<=x+3 and y-3<=gy<=y+3 and p['layer'] in ('tile','parts'),'bounded source cell')
            need(p['anchor_relative']==[(gx-x+gy-y)*32,((gy-y)-(gx-x))*24],'explicit modern projection candidate')
            ids.add(p['map_id'])
    need(set(map(int,r['resources']))==ids and len(ids)==51,'exact bounded source image set')
    need(r['scene_order']=='MODERN_TILE_THEN_PARTS_SOURCE_SWEEP_NO_NATIVE_R6_R9_PROMOTION','rendering scope')
    need(r['map_third_plane_interpreted_as_collision'] is False and r['time_field_interpreted_as_warp_schedule'] is False,'unknown native semantics')
    need(all(r[k] is False for k in FALSE) and r['overall_completion_percent'] is None,'historical boundaries')
    need(r['modern_observation_start']=={'floor':1001,'x':11,'y':15},'observer starts away from doorway')
    return {'authored_doorway_pairs':1,'actual_map_viewports':2,'distinct_source_images':51,'source_occurrences':sum(len(v['placements']) for v in r['views']),'original_world_entered':False}


def validate_acceptance(a,r):
    need(a['schema']=='stoneage.scene15.actual_source_and_browser_acceptance.r1' and a['scope']=='LOCAL_AUTHENTICATED_STATIC_INPUTS_AND_MODERN_OFFLINE_MAP_SWITCH_NOT_NATIVE_WARP','acceptance scope')
    need(a['source_report_sha256']==sha(REPORT.read_bytes()),'archived original-derived source report')
    b=a['browser'];i=a['independent_pixel_replay'];need(b['actual_decoded_images']==52 and b['errors']==b['external_requests']==[],'actual browser images/errors')
    need(all(b[k] is True for k in ['neighbor_door_refused','exact_forward_and_return_observed','no_automatic_bounce','modern_boundary_refusal_observed','reset_preserves_journal']),'real interaction checks')
    labels=['room_start','neighbor_door_refused','room_door','outside_arrival','outside_no_parts','outside_no_human','outside_scale2','outside_no_marker','returned_room','modern_window_boundary','reset_keeps_log']
    need([v['label'] for v in b['frames']]==labels and [v['label'] for v in i['frames']]==labels,'every observed viewport state')
    need(i['independent_original_RD_index_RGBA_PNGs']==51 and i['human_reference_PNG_verified']==1 and i['all_integer_scale_full_canvas_matches']==11 and i['source_config_spans_verified']==3,'independent original spans and pixels')
    for v,w in zip(b['frames'],i['frames']):need(v['canvas_sha256']==w['canvas_sha256'] and re.fullmatch('[0-9a-f]{64}',v['canvas_sha256']) is not None,'full canvas equality')
    states=[v['state'] for v in b['frames']]
    need((states[0]['floor'],states[0]['x'],states[0]['y'])==(1001,11,15) and (states[1]['floor'],states[1]['x'],states[1]['y'])==(1001,10,16),'not-yet-at-selected-door states')
    need((states[3]['floor'],states[3]['x'],states[3]['y'])==(1000,63,99) and (states[8]['floor'],states[8]['x'],states[8]['y'])==(1001,10,15),'actual exact target tuple and return')
    log=states[-1]['journal'];need(len(log)==2 and [j['source'] for j in log]==[[1001,10,15],[1000,63,99]] and [j['destination'] for j in log]==[[1000,63,99],[1001,10,15]] and all(j['original_runtime_executed'] is False for j in log),'modern observation journal is not original runtime')
    need(set(a['libarchive_independent_matches'])=={'npc/genout/warp_y.create','npc/genout/npcgen.template','client/map/1001.DAT'},'three actual independent extraction matches')
    need(a['libarchive_DAT1000_secondary_failure']['retcode']==-30 and a['sevenzip_secondary_DAT1000_failure']['returncode']==-11 and a['independent_secondary_DAT1000_success'] is False,'failed secondary decoders remain failed')
    need(a['original_DAT1000_corrupt_claimed'] is False and a['primary_DAT1000_matches_previously_preserved_sha256'] is True,'do not call proven primary map corrupt')
    prior=a['reused_prior_world_contract'];raw=(ROOT/prior['path']).read_bytes();need(len(raw)==prior['bytes'] and sha(raw)==prior['sha256'],'reuse immutable old world contract')
    need(prior['world_closure_count_not_changed']==826 and len(prior['exact_existing_rows'])==2 and all(row in raw.decode().splitlines() for row in prior['exact_existing_rows']),'old closure is not new restoration')
    need(a['private_original_source_run_id'] is None and a['public_CI_reads_private_original_files'] is False and a['same_deployed_build_authenticated'] is False and a['original_world_entered'] is False and a['original_warp_runtime_verified'] is False and a['overall_completion_percent'] is None,'bounded historical status')
    return {'actual_source_images':51,'browser_images':52,'all_integer_scale_canvas_matches':11,'actual_MODERN_round_trips':1,'secondary_DAT1000_decoders_succeeded':False,'original_world_entered':False}

def export(warp,template,mapfiles,art,prior,target):
    from PIL import Image
    target=target.resolve();need(ROOT!=target and ROOT not in target.parents and not target.exists(),'new private output outside Git')
    doors,t,n=doorway(warp.read_bytes(),template.read_bytes());views=[map_view(mapfiles[f].read_bytes(),f) for f in (1001,1000)]
    for name in ('adrn_15.bin','real_15.bin','Palet_1.sap'):authenticate(art/name,PINS[name])
    ids=sorted({p['map_id'] for v in views for p in v['placements']});need(len(ids)<=64,'finite source-art budget')
    adrn=(art/'adrn_15.bin').read_bytes();resources={}
    for start in range(0,len(ids),16):
        rows=resolve_ids(adrn,set(ids[start:start+16]),PINS['real_15.bin'][0])
        for key,candidates in rows.items():need(len(candidates)==1,'unqualified/ambiguous alias; no last-wins');resources[str(key)]=candidates[0]
    from tools.stoneage_rd_codec import decode_rd_block
    rgb=initial_rgb((art/'Palet_1.sap').read_bytes());images={};rawblocks={}
    with (art/'real_15.bin').open('rb') as f:
        for key,row in resources.items():
            f.seek(row['offset']);rd=f.read(row['size']);need(len(rd)==row['size'],'short original RD')
            hdr,indices=decode_rd_block(rd,authoritative_block_size=row['size']);need((hdr['width_s'],hdr['height_s'])==(row['width'],row['height']),'source geometry')
            rgba=candidate_rgba(indices,row['width'],row['height'],rgb);out=io.BytesIO();Image.frombytes('RGBA',(row['width'],row['height']),rgba).save(out,format='PNG');png=out.getvalue()
            row.update(RD_sha256=sha(rd),index_pixels_sha256=sha(indices),RGBA_candidate_sha256=sha(rgba),PNG_sha256=sha(png));images[key]=base64.b64encode(png).decode();rawblocks[key+'.rd']=rd
    for v in views:
        bounds=[]
        for p in v['placements']:
            row=resources[str(p['map_id'])];p['draw_relative']=[p['anchor_relative'][0]+row['xoff'],p['anchor_relative'][1]+row['yoff']];px,py=p['draw_relative'];bounds.append((px,py,px+row['width'],py+row['height']))
        v['source_art_bounds']=[min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds)]
    b=prior.read_bytes();need(sha(b)==PRIOR_HTML_SHA,'prior authenticated actual human source PNG')
    pack=json.loads(b.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);human=pack['actors']['groups'][0];anim=next(a for a in human['animations'] if a['direction']==6 and a['action']==2);frame=anim['frames'][0];row=next(x for x in pack['actors']['bitmaps'] if x['bitmapno']==frame[0]);png=base64.b64decode(pack['actor_images'][str(frame[0])]);need(sha(png)==row['PNG_sha256'],'qualified single human reference picture')
    human_info={'spr':100000,'direction':6,'action':2,'source_frame':frame,'bitmap':row,'scope':'STATIC_ORIGINAL_SOURCE_IMAGE_MODERN_MANUAL_CURSOR_NOT_NATIVE_PLAYER_IDENTITY'}
    r={'schema':'stoneage.scene15.authored_doorway_source_observer.r1','scope':'PRESERVED_MIXED25_STATIC_DOORWAY_PLUS_MODERN_OFFLINE_OBSERVER_NOT_ORIGINAL_GAME',
       'source_warp':{'bytes':WARP_PIN[0],'sha256':WARP_PIN[1]},'source_template':{'bytes':TEMPLATE_PIN[0],'sha256':TEMPLATE_PIN[1]},
       'doorway_pair':doors,'template_block':t,'functionset':'Warp','original_create_blocks':n,'views':views,'resources':resources,
       'source_art_files':{k:{'bytes':PINS[k][0],'sha256':PINS[k][1]} for k in ('adrn_15.bin','real_15.bin','Palet_1.sap')},
       'human_reference':human_info,'scene_order':'MODERN_TILE_THEN_PARTS_SOURCE_SWEEP_NO_NATIVE_R6_R9_PROMOTION','modern_observation_start':{'floor':1001,'x':11,'y':15},
       'map_third_plane_interpreted_as_collision':False,'time_field_interpreted_as_warp_schedule':False,**{k:False for k in FALSE},'overall_completion_percent':None}
    validate(r);private={'source':r,'images':images,'human_image':base64.b64encode(png).decode()}
    text=(ROOT/'tools/scene-doorway-viewer-r15.html').read_text();need(text.count('"PRIVATE_PACK_PLACEHOLDER"')==1,'one source pack marker')
    text=text.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(private,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
    target.mkdir(parents=True,mode=0o700);(target/'stoneage-r15-doorway-observer.html').write_text(text);(target/'source-derived-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(target/'private-source-rd-subset.zip','w',zipfile.ZIP_DEFLATED) as z:
        for key,b in rawblocks.items():z.writestr(key,b)
    (target/'private-palette.sap').write_bytes((art/'Palet_1.sap').read_bytes());return r


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--warp',type=Path);p.add_argument('--template',type=Path);p.add_argument('--room-map',type=Path);p.add_argument('--outside-map',type=Path);p.add_argument('--art-dir',type=Path);p.add_argument('--prior-html',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.warp:r=export(a.warp,a.template,{1001:a.room_map,1000:a.outside_map},a.art_dir,a.prior_html,a.output_dir)
    else:r=json.loads(REPORT.read_bytes())
    result=validate(r)
    if not a.warp:result['archived_acceptance']=validate_acceptance(json.loads((ROOT/'research/recovered/STONEAGE-SCENE15-ACCEPTANCE-R1.json').read_bytes()),r)
    print(json.dumps(result))
if __name__=='__main__':main()
