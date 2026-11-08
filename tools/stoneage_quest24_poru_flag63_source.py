"""Source-bounded Poru prerequisite, real function bindings and four DAT scenes."""
from __future__ import annotations
import argparse
import html
import io
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest08_mining_source import load_private_source
from tools.stoneage_quest17_dino_ranch_source import NPC_ZIP_SHA, ITEM_ZIP_SHA, source_info, sha
from tools.stoneage_quest21_liuli_source import load, pin, QUEST01, CHAR01
from tools.stoneage_quest22_hekisei_source import scene_observation, MAP09, MAP_ZIP_SHA
from tools.stoneage_quest23_poru_source import catalog_sections, WORLD21

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'research/recovered/STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-R1.json'
CREATE='poru/poru01.create';BOSS='poru/boss.create'
FLOORS=(5500,5509,5510,5511)
ITEM_IDS=[*range(2248,2254),2414,18544,*range(18556,18560)]
Q23='STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-R1.json'


def derive(npc_path,item_path,map_path):
    _,ch,data=load_private_source(npc_path);q=load(QUEST01);w=load(WORLD21);previous=load(Q23)
    rows=[r for r in ch['create_rows'] if r[0]==CREATE]+[r for r in ch['create_rows'] if r[0]==BOSS and r[1]==0]
    assert len(rows)==33
    templates={(r[0],r[1]):r for r in ch['template_rows']}
    paths={CREATE,BOSS};creates=[]
    for marker,r in enumerate(rows):
        assert sha(data[r[0]][r[2]:r[3]])==r[4]
        refs=[]
        for p,kind,digest in r[15]:
            assert sha(data[p])==digest;paths.add(p);refs.append(p)
        bindings=[]
        for p,n in r[13]:
            paths.add(p);t=templates[(p,n)]
            bindings.append(dict(template_path=p,template_ordinal=n,source_template_name=t[3],source_functionset=t[4]))
        # Marker IDs are modern page-local identifiers, not NPC/game IDs.
        creates.append(dict(marker_id=marker,source_create_path=r[0],source_create_ordinal=r[1],
            original_block_sha256=r[4],floor=r[5],graphic_alias=r[6],borncorner=r[7],borncenter=r[8],
            original_direction=r[10],source_template_token=r[11],source_bindings=bindings,argument_paths=refs,
            original_borncenter_borncorner_precedence_verified=False,native_NPC_executed=False))
    refs=[x for x in q['source_creation_references'] if x['create_source_path']==CREATE]
    scripts=sorted({x['original_script_path'] for x in refs}|{'poru/boy04'})
    assert len(scripts)==12
    records=[dict(**source_info(p,data[p]),events=catalog_sections(data[p],[b for b in q['source_event_blocks'] if b['script_path']==p])) for p in scripts]
    assert sum(len(r['events']) for r in records)==39
    private={'original-npc/'+p:data[p] for p in sorted(paths)}
    by_script={r['path']:r for r in records}
    core_items=[];item_labels={};assert sha(item_path.read_bytes())==ITEM_ZIP_SHA
    public={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    with zipfile.ZipFile(item_path) as z:
        assert len(z.namelist())==838 and z.testzip() is None
        cat=json.loads(z.read('private-full-catalog.json'));items={r['id']:r for r in cat['items']}
        images={r['source_itemset_image_number_alias']:r for r in cat['image_source_receipts']}
        for i in ITEM_IDS:
            rows_i=[]
            for col,table in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                r=items[i][table];columns=r['original_94_columns'];b=','.join(columns).encode('cp950')
                assert len(columns)==94 and int(columns[16])==i and sha(b)==r['original_row_sha256']==public[i][col]
                private[f'original-itemrows/{table}/{i}.txt']=b+b'\n'
                rows_i.append(dict(table=table,row=r['source_row_1based'],sha256=sha(b),image_alias=int(columns[17])))
            alias=rows_i[0]['image_alias'];assert rows_i[1]['image_alias']==alias;image=images[alias]
            assert image['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png=z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png');assert sha(png)==image['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-item-candidates/{alias}.png']=png
            core_items.append(dict(item_ID=i,source_rows=rows_i,cross_carrier_candidate_alias=alias,
                                   candidate_PNG_sha256=sha(png),original_RD_sha256=image['original_RD_SHA256']))
            columns=items[i]['itemset.txt']['original_94_columns'];item_labels[i]=(columns[0],columns[2])
    observation_input=[dict(ordinal=c['marker_id'],floor=c['floor'],borncenter=c['borncenter']) for c in creates]
    observations,image_count=scene_observation(map_path,observation_input,private,floors=FLOORS,coordinate_field='borncenter')
    for s in observations:
        for point in s['source_points']:
            marker=point.pop('create_ordinal');c=creates[marker]
            point.update(modern_marker_id=marker,source_create_path=c['source_create_path'],source_create_ordinal=c['source_create_ordinal'])
    # Reflow the existing research contact sheet into a compact 2x2 grid.
    from PIL import Image
    old=Image.open(io.BytesIO(private.pop('three-original-scenes-contact.png'))).convert('RGB')
    contact=Image.new('RGB',(1440,1200),'#11232a')
    for i in range(4):contact.paste(old.crop((720*(i%3),600*(i//3),720*(i%3)+720,600*(i//3)+600)),(720*(i%2),600*(i//2)))
    buffer=io.BytesIO();contact.save(buffer,format='PNG');private['four-original-scenes-contact.png']=buffer.getvalue()
    gates=[]
    for c in creates:
        if c['source_template_token']!='npcgen_warpman':continue
        p=c['argument_paths'][0];text=data[p].decode('cp950')
        values={k:re.search(rf'(?m)^{k}:([^\r\n]*)',text).group(1) for k in ('WARP','FREE','MONEY')}
        gates.append(dict(marker_id=c['marker_id'],path=p,source_values=values,actual_warp_or_fee_executed=False))
    old_pet=next(r for r in w['original_enemy_instance_to_template_lookups'] if r['getpet_integer']==352)
    report=dict(schema='stoneage.quest24.poru_flag63_function_bindings_four_scenes.r1',date='2026-11-08',
        initial_remote=dict(head='f26565d75231eb0d90cc7258b2496ec7eb22ea05',tree='bce8b799ff8f2b3eec208720f0e3d7ad940b2e58',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        old_evidence_inputs=[pin(n) for n in [QUEST01,CHAR01,WORLD21,MAP09,Q23]],
        verified_private_carriers=dict(NPC_ZIP_sha256=NPC_ZIP_SHA,NPC_members_SHA_CRC=2205,item_ZIP_sha256=ITEM_ZIP_SHA,
            item_members_CRC=838,MAP09_ZIP_sha256=MAP_ZIP_SHA,MAP09_members_CRC=4195,parent_RAR_reread=False),
        source_manifest=[source_info(p,data[p]) for p in sorted(paths)],source_creates=creates,source_scripts=records,
        old_QUEST01_event_count=39,new_original_script_discoveries=0,
        flag63_bridge=dict(provider_script='poru/boy04',event_ordinal=1,provider_CREATE=BOSS,provider_CREATE_ordinal=0,
            original_provider_condition=by_script['poru/boy04']['events'][1]['condition_literal'],
            original_provider_commands=by_script['poru/boy04']['events'][1]['commands'],
            next_source_QUEST23_request_conditions=None,
            original_GetPet_352_existing_WORLD21_lookup=old_pet,existing_pet_not_new_discovery=True,
            original_flag_saved_or_reward_delivered=False),
        wpm_named_dialogue=dict(path='poru/wpm_5510_16_50',source_template_token='changeevent',source_functionset='ExChangeMan',
            actual_type='MESSAGE',has_original_WARP_field=False,classified_as_warp_from_filename=False),
        actual_source_warpman_parameters=gates,
        meat_shell_source=dict(script='poru/boy05',condition=by_script['poru/boy05']['events'][0]['condition_literal'],
            commands=by_script['poru/boy05']['events'][0]['commands'],original_boolean_or_deletion_semantics_verified=False),
        source_four_object_message_difference=dict(script='poru/samugiru01',event_ordinal=1,
            original_message_condition=by_script['poru/samugiru01']['events'][1]['condition_literal'],
            later_QUEST23_finale_condition=previous['four_stones_finale']['original_condition'],
            original_18544_replaced_with_18558=False),
        core_items=core_items,original_scene_observations=observations,distinct_candidate_tile_PNGs=image_count,
        source_center_observation=dict(original_DAT_files=4,complete_independent_candidate_frames=12,
            measured_centers=sum(len(s['source_points']) for s in observations),new_original_RD_decodes=0,
            borncenter_last_two_integers_and_field_precedence_unresolved=True,original_NPC_sprites_drawn=False),
        source_floor500=dict(modern_marker_ids=[c['marker_id'] for c in creates if c['floor']==500],matching_original_DAT_in_955=False),
        boundaries=dict(original_client_or_server_executed=False,official_early_deployment_authenticated=False,
            source_conditions_interpreted_as_original_runtime=False,source_WPM_filename_assumed_function=False,
            native_palette_layer_order_or_collision_verified=False,original_assets_or_dialogue_published=False,
            task_origin='UNRESOLVED'),
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',R79='PAUSED_NON_BLOCKING',overall_percent=None,
        next='QUEST25_MODULE_CONTENT_REVIEW_AFTER_PORU_FLAG63_AND64_SOURCE_LINKS')
    # Explicitly retrieve the corresponding event64 request, preserving its old source.
    mary=next(s for s in previous['source_scripts'] if s['path']=='poru/mary')
    report['flag63_bridge']['next_source_QUEST23_request_conditions']=[e['condition_literal'] for e in mary['events'] if e['type']=='REQUEST']
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    page='<!doctype html><meta charset="utf-8"><title>QUEST24 波拉岛前段原资料</title><style>body{font:16px sans-serif;max-width:1100px;margin:30px auto;background:#11232a;color:#eee}img{max-width:100%}pre{white-space:pre-wrap;background:#20343b;padding:18px}a{color:#ffdf00}summary{padding:8px;cursor:pointer}</style><h1>波拉岛前段剧情与ENDEV63来源</h1><p>后期社区保存本。黄点仅标borncenter前两数，图上编号为现代marker ID，不是原NPC ID。保留borncorner/center双字段，未认定原生出生格、碰撞、战斗或任务运行。boss.create只核龙王第0配置，其余配置原文保留但不宣称逐一恢复。</p><img src="four-original-scenes-contact.png">'
    page+=''.join(f'<p><a href="scenes/{f}-source-points.png">DAT {f}完整来源标记画面</a></p>' for f in FLOORS)
    page+='<h2>后期原物品表与TW1跨来源候选图</h2>'
    for item in core_items:
        i=item['item_ID'];name,desc=item_labels[i];page+='<article><h3>'+str(i)+' '+html.escape(name)+'</h3><img style="image-rendering:pixelated;max-width:160px" src="cross-carrier-TW1-item-candidates/'+str(item['cross_carrier_candidate_alias'])+'.png"><p>'+html.escape(desc)+'</p></article>'
    for p in sorted(paths):page+='<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(data[p].decode('cp950'))+'</pre></details>'
    private['index.html']=page.encode()
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('npc-zip','item-zip','map-zip','private-zip'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT);a=p.parse_args();assert ROOT not in a.private_zip.resolve().parents
    r,private=derive(a.npc_zip,a.item_zip,a.map_zip);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name,b in sorted(private.items()):z.writestr(name,b)
    (a.private_zip.parent/'quest24-four-scenes-contact.png').write_bytes(private['four-original-scenes-contact.png'])
    print(json.dumps(dict(configurations=33,old_events=39,scenes=4,measured_centers=r['source_center_observation']['measured_centers'],private_members=len(private))))


if __name__=='__main__':main()
