"""Poru story source dossier: preserve comments, malformed EOF and borncenter.

The old catalogue bounds every TYPE section by its source lines and SHA. This
does not repair syntax, interpret predicates or execute original game rules.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest08_mining_source import load_private_source
from tools.stoneage_quest17_dino_ranch_source import NPC_ZIP_SHA, ITEM_ZIP_SHA, source_info, sha
from tools.stoneage_quest21_liuli_source import load, pin, QUEST01, CHAR01
from tools.stoneage_quest22_hekisei_source import scene_observation, MAP09, MAP_ZIP_SHA

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'research/recovered/STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-R1.json'
CREATE='poru/poru02.create'
WORLD21='STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json'
FLOORS=(5530,5532,5533,5535,5537,5538,5541,5542,5543)
FIELDS=('GetItem','DelItem','GetPet','DelPet','GetStone','DelStone','GetRandItem','EndSetFlg','Charm','NpcWarp','NotDel')


def catalog_sections(raw, previous):
    text=raw.decode('cp950','strict').replace('\r\n','\n')
    assert text.encode('cp950').decode('cp950')==text
    lines=text.splitlines(keepends=True);out=[]
    assert [i for i,l in enumerate(lines,1) if l.startswith('TYPE:')]==[r['source_type_line'] for r in previous]
    for ix,old in enumerate(previous):
        start=(old['source_eventno_line'] or old['source_type_line'])-1
        limit=((previous[ix+1]['source_eventno_line'] or previous[ix+1]['source_type_line'])-1) if ix+1<len(previous) else len(lines)
        end=next((i+1 for i in range(old['source_type_line'],limit) if lines[i].strip()=='EventEnd'),None)
        assert (end is not None)==old['source_End_found']
        # EOF is retained verbatim, including the two terminal LFs in titan.
        section=''.join(lines[start:end if end is not None else limit])
        assert sha(section.encode())==old['source_section_decoded_cp950_normalized_UTF8_sha256']
        condition=re.search(r'(?m)^EVENT:([^\r\n]*)',section).group(1)
        assert sha(condition.encode())==old['condition_expression_decoded_cp950_UTF8_sha256']
        commands={key:re.findall(rf'(?m)^\s*{key}:([^\r\n]*)',section) for key in FIELDS}
        commands={k:v for k,v in commands.items() if v}
        out.append(dict(ordinal=ix,type_line=old['source_type_line'],event_no=old['event_number'],type=old['raw_type'],
                        condition_literal=condition,condition_sha256=sha(condition.encode()),
                        section_sha256=sha(section.encode()),exact_EventEnd_found=end is not None,
                        commands=commands,bare_Break_lines=len(re.findall(r'(?m)^Break\s*$',section)),
                        malformed_EventEnd_prefix_lines=[dict(line=start+i+1,line_UTF8_sha256=sha(l.encode()))
                            for i,l in enumerate(section.splitlines()) if l.startswith('EventEnd') and l.strip()!='EventEnd']))
    return out


def derive(npc_path,item_path,map_path):
    _,ch,data=load_private_source(npc_path)
    q=load(QUEST01);world=load(WORLD21)
    oldrefs=[r for r in q['source_creation_references'] if r['create_source_path']==CREATE]
    scripts=sorted({r['original_script_path'] for r in oldrefs})
    assert len(scripts)==20
    filepaths=[CREATE,*scripts,'poru/mary10','jaruga/event/event.template']
    private={'original-npc/'+p:data[p] for p in filepaths}
    raw=data[CREATE];matches=list(re.finditer(r'\{[^{}]*\}',raw.decode('cp950')))
    assert len(matches)==21
    comment=matches[14].group()
    assert not re.search(r'(?m)^\s*(name|floorid|borncenter|enemy)=',comment)
    assert '#enemy=changeevent|file:poru/mary10' in comment and '#}' in comment
    creates=[]
    for row in [r for r in ch['create_rows'] if r[0]==CREATE]:
        assert sha(raw[row[2]:row[3]])==row[4]
        old=next(r for r in oldrefs if r['original_script_path']==row[15][0][0])
        literal=next(i for i,m in enumerate(matches) if re.search(r'(?m)^enemy=changeevent\|file:'+re.escape(old['original_script_path'])+r'\s*$',m.group()))
        assert literal==old['create_brace_ordinal']
        assert row[7] is None and row[8] is not None
        creates.append(dict(ordinal=row[1],raw_brace_match_ordinal=literal,source_block_sha256=row[4],
                            source_byte_start=row[2],source_byte_end=row[3],floor=row[5],graphic_alias=row[6],
                            borncenter=row[8],borncorner=None,script_ref=old['original_script_path'],
                            template_token=row[11],actual_runtime_loader_verified=False))
    records=[]
    for p in scripts:
        blocks=[b for b in q['source_event_blocks'] if b['script_path']==p]
        records.append(dict(**source_info(p,data[p]),events=catalog_sections(data[p],blocks)))
    index={s['path']:s for s in records}
    events=[e for s in records for e in s['events']]
    item_ids=set()
    for e in events:
        item_ids.update(map(int,re.findall(r'ITEM[!=<>]+(\d+)',e['condition_literal'])))
        for field in ('GetItem','DelItem','GetRandItem'):
            for literal in e['commands'].get(field,[]):
                item_ids.update(int(m) for m in re.findall(r'(?:^|,)\s*(\d+)',literal))
    # GetStone/DelStone amounts are not item IDs.
    assert item_ids=={2432,2474,2477,2478,18544,*range(18551,18563)}
    public={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    assert sha(item_path.read_bytes())==ITEM_ZIP_SHA
    items=[];icons=set();private_item_labels={}
    with zipfile.ZipFile(item_path) as z:
        assert len(z.namelist())==838 and z.testzip() is None
        cat=json.loads(z.read('private-full-catalog.json'));itemindex={x['id']:x for x in cat['items']}
        images={x['source_itemset_image_number_alias']:x for x in cat['image_source_receipts']}
        for i in sorted(item_ids):
            original_columns=itemindex[i]['itemset.txt']['original_94_columns']
            private_item_labels[i]=(original_columns[0],original_columns[2])
            rows=[]
            for col,table in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                r=itemindex[i][table];columns=r['original_94_columns'];b=','.join(columns).encode('cp950')
                assert len(columns)==94 and int(columns[16])==i and sha(b)==r['original_row_sha256']==public[i][col]
                private[f'original-itemrows/{table}/{i}.txt']=b+b'\n'
                rows.append(dict(table=table,row=r['source_row_1based'],sha256=sha(b),image_alias=int(columns[17])))
            alias=rows[0]['image_alias'];assert rows[1]['image_alias']==alias;im=images[alias]
            assert im['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png=z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png');assert sha(png)==im['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-item-candidates/{alias}.png']=png;icons.add(alias)
            items.append(dict(item_ID=i,source_rows=rows,cross_carrier_candidate_alias=alias,
                              original_RD_sha256=im['original_RD_SHA256'],candidate_PNG_sha256=sha(png)))
    observations,image_count=scene_observation(map_path,creates,private,floors=FLOORS,coordinate_field='borncenter')
    private['nine-original-scenes-contact.png']=private.pop('three-original-scenes-contact.png')
    getpet=[]
    lookup={r['getpet_integer']:r for r in world['original_enemy_instance_to_template_lookups']}
    for s in records:
        for e in s['events']:
            for literal in e['commands'].get('GetPet',[]):
                assert literal.isdigit()
                getpet.append(dict(script=s['path'],event_ordinal=e['ordinal'],source_GetPet_literal=literal,
                                   existing_WORLD21_lookup=lookup[int(literal)],new_pet_discovery=False))
    relocation=[dict(script=s['path'],event_ordinal=e['ordinal'],source_literal=v,
                     target_occurrences=[list(map(int,p.split('.'))) for p in v.split(',')],
                     original_NPC_relocation_executed=False)
                for s in records for e in s['events'] for v in e['commands'].get('NpcWarp',[])]
    report=dict(schema='stoneage.quest23.poru_story_borncenter_and_nine_scenes.r1',date='2026-11-08',
        initial_remote=dict(head='990b32c090a00bdb85d86f9c5f6c9c7becf66286',tree='94142287c75789f8f71a8ba8c0aeecf8350fed84',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        verified_private_carriers=dict(NPC_ZIP_sha256=NPC_ZIP_SHA,NPC_all_member_SHA_and_CRC=2205,
            item_ZIP_sha256=ITEM_ZIP_SHA,item_ZIP_CRC_members=838,MAP09_ZIP_sha256=MAP_ZIP_SHA,
            MAP09_ZIP_CRC_members=4195,parent_RAR_reread=False),
        old_evidence_inputs=[pin(n) for n in [QUEST01,CHAR01,WORLD21,MAP09]],
        source_manifest=[source_info(p,data[p]) for p in filepaths],source_creates=creates,source_scripts=records,
        existing_QUEST01_event_count=len(events),new_original_script_discoveries=0,
        source_comment_only_block=dict(raw_brace_match_ordinal=14,original_block_cp950_sha256=sha(comment.encode('cp950')),
            all_configuration_fields_prefixed_by_comment=True,closing_brace_also_comment_prefixed=True,
            catalog_active_field_ordinal=None,commented_reference='poru/mary10',
            original_referenced_file_header='LIMITSHOP',source_LimitItemNo=[12174,12175,12176],
            actual_shop_or_runtime_loader_effect_verified=False),
        source_malformed_end=dict(script='poru/titan',event_ordinal=7,exact_EventEnd_lines=7,source_TYPE_sections=8,
                                  malformed_prefix_physical_line=73,original_text_fixed=False),
        source_items=items,distinct_cross_carrier_item_candidate_images=len(icons),
        existing_WORLD21_GetPet_links=getpet,source_NpcWarp_fields=relocation,
        four_stones_finale=dict(script='poru/mary01',event_ordinal=0,
            original_condition=index['poru/mary01']['events'][0]['condition_literal'],
            original_DelItem_literal=index['poru/mary01']['events'][0]['commands']['DelItem'][0],
            GetPet_instance_literal='310',EndSetFlg_literal='64',actual_reward_delivered=False),
        original_scene_observations=observations,distinct_replayed_candidate_tile_PNGs=image_count,
        source_center_observation=dict(original_DAT_files=9,independent_candidate_full_frames=27,
            measured_borncenter_centers=sum(len(s['source_points']) for s in observations),
            marker_is_literal_center_not_actual_spawn=True,borncenter_last_two_integers_not_assigned_semantics=True,
            original_NPC_sprite_drawn=False,new_original_RD_decodes=0),
        original_floor500=dict(source_CREATE_ordinals=[c['ordinal'] for c in creates if c['floor']==500],
            matching_DAT_in_955=False,original_scene_or_relocation_executed=False),
        boundaries=dict(original_client_or_server_executed=False,official_early_deployment_authenticated=False,
            source_conditions_interpreted_as_original_runtime=False,commented_shop_promoted_to_live_CREATE=False,
            pet_instances_equal_template_IDs=False,original_NPC_sprites_or_source_dialogue_published=False,
            native_palette_layer_order_or_collision_verified=False,task_origin='UNRESOLVED'),
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',R79='PAUSED_NON_BLOCKING',overall_percent=None,
        next='QUEST24_SOURCE_READY_DISTINCT_CONTENT_AFTER_PORU_STORY_BATCH_REVIEW')
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    page='<!doctype html><meta charset="utf-8"><title>QUEST23 波拉岛原资料</title><style>body{font:16px sans-serif;max-width:1100px;margin:30px auto;background:#11232a;color:#eee}img{max-width:100%}pre{white-space:pre-wrap;background:#20343b;padding:18px}a{color:#ffdf00}summary{padding:8px;cursor:pointer}</style><h1>波拉岛剧情：原文、道具与九张地图候选</h1><p>后期社区保存本。黄色标记仅为borncenter前两数的现代投影，不是实际出生位置；后两数原样保留，NPC精灵未绘制。500地图缺源。注释商人和粘接的EventEnd原文不修复，没有执行原游戏。</p><img src="nine-original-scenes-contact.png" alt="九张原DAT候选画面">'
    page+=''.join(f'<p><a href="scenes/{f}-source-points.png">查看DAT {f}完整标记图</a></p>' for f in FLOORS)
    page+='<h2>后期原物品表与跨来源TW1候选图</h2><p>同图别名仍保留为不同道具，不认证同版同服。</p>'
    for item in items:
        i=item['item_ID'];name,description=private_item_labels[i]
        page+='<article><h3>'+str(i)+' '+html.escape(name)+'</h3><img style="image-rendering:pixelated;max-width:160px" src="cross-carrier-TW1-item-candidates/'+str(item['cross_carrier_candidate_alias'])+'.png"><p>'+html.escape(description)+'</p></article>'
    for p in filepaths:
        page+='<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(data[p].decode('cp950'))+'</pre></details>'
    private['index.html']=page.encode()
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('npc-zip','item-zip','map-zip','private-zip'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT);a=p.parse_args()
    assert ROOT not in a.private_zip.resolve().parents
    r,private=derive(a.npc_zip,a.item_zip,a.map_zip)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name,b in sorted(private.items()):z.writestr(name,b)
    (a.private_zip.parent/'quest23-nine-scenes-contact.png').write_bytes(private['nine-original-scenes-contact.png'])
    print(json.dumps(dict(existing_events=r['existing_QUEST01_event_count'],source_configs=len(r['source_creates']),
                         measured_centers=r['source_center_observation']['measured_borncenter_centers'],
                         scenes=9,frames=27,private_members=len(private))))


if __name__=='__main__':main()
