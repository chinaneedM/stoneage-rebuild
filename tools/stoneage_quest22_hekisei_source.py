"""Bounded water-spirit quest links and three private, source-qualified scenes.

Reuses the previous CP950/event and MAP09 dual-render implementations. Public
output contains numeric metadata and hashes; original content stays private.
"""
from __future__ import annotations
import argparse
import base64
import html
import io
import json
from pathlib import Path
import re
import struct
import zipfile

from tools.stoneage_quest17_dino_ranch_source import (
    NPC_ZIP_SHA, ITEM_ZIP_SHA, PARENT_RAR_SHA, parse_creates, source_info, sha,
)
from tools.stoneage_quest21_liuli_source import numeric_events, load, pin, QUEST01, CHAR01

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'research/recovered/STONEAGE-QUEST22-HEKISEI-ORIGINAL-SOURCE-AND-THREE-SCENES-R1.json'
CREATE = 'jaruga/event/hekisei.create'
SCRIPTS = ['jaruga/event/hekisei' + s for s in ('', '01', '02', '03', '04', '05', '06')]
FILES = [CREATE, *SCRIPTS, 'jaruga/event/event.template']
ITEM_IDS = list(range(2766, 2771))
FLOORS = (21215, 21308, 31302)
MAP09 = 'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
WORLD23 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
MAP_ZIP_SHA = 'd84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a'


def encode_image(image):
    out = io.BytesIO(); image.save(out, format='PNG'); return out.getvalue()


def scene_observation(map_path, creates, private, *, floors=FLOORS, coordinate_field='borncorner'):
    import numpy as np
    from PIL import Image, ImageDraw
    from tools.stoneage_map06_two_original_scenes import placements
    from tools.stoneage_map09_batch_scenes import verified_frames
    from tools.stoneage_scene21_town1000 import render

    assert sha(map_path.read_bytes()) == MAP_ZIP_SHA
    ledger = load(MAP09)
    results = []; thumbs = []
    with zipfile.ZipFile(map_path) as z:
        assert len(z.namelist()) == 4195 and z.testzip() is None
        dataset = z.read('dataset.js').decode('utf-8')
        assert dataset.startswith('window.MAP09_DATA=') and dataset.endswith(';\n')
        model = json.loads(dataset[len('window.MAP09_DATA='):-2])
        raw_sources = z.read('private-image-source-records.json')
        assert sha(raw_sources) == ledger['private_image_source_records_sha256']
        sources = json.loads(raw_sources)
        original_zip = z.read('source-all-955-original-DAT.zip')
        assert sha(original_zip) == ledger['original_DAT_archive']['sha256']
        archive = zipfile.ZipFile(io.BytesIO(original_zip))
        assert len(archive.namelist()) == 955 and archive.testzip() is None
        assert '3400.dat' not in archive.namelist()
        for floor in floors:
            name = str(floor); old = ledger['maps'][name]
            raw = archive.read(name + '.dat')
            assert raw == base64.b64decode(model['maps'][name]['dat_base64'])
            assert sha(raw) == old['source_sha256']
            info, selected = placements(raw)
            keys = sorted({p['image_key'] for p in selected})
            images = {}; records = {}; arrays = {}
            for key in keys:
                b = z.read(f'tiles/{key}.png'); rec = sources[str(key)]
                assert sha(b) == rec['candidate_PNG_sha256']
                im = Image.open(io.BytesIO(b)).convert('RGBA')
                assert sha(im.tobytes()) == rec['candidate_RGBA_sha256']
                images[key] = im; arrays[key] = np.array(im); records[key] = model['records'][str(key)]
                assert set(np.unique(arrays[key][:,:,3])) <= {0,255}
                private[f'map-source/tiles/{key}.png'] = b
            size, origin, digests, _ = verified_frames(raw, info, selected, images, records, arrays)
            assert digests == old['frame_RGBA_sha256']
            assert size == old['canvas_size'] and origin == old['origin']
            full = render(images, records, selected, False, True, False, origin, size)
            assert sha(full.tobytes()) == digests['combined']
            marked = full.copy(); draw = ImageDraw.Draw(marked)
            w, h = struct.unpack_from('<II', raw)
            points = []
            for c in creates:
                if c['floor'] != floor: continue
                x,y = c[coordinate_field][:2]; assert 0 <= x < w and 0 <= y < h
                values = [struct.unpack_from('<H', raw, 8 + 2*(p*w*h + y*w+x))[0] for p in range(3)]
                center = [origin[0]+(x+y)*32, origin[1]+(y-x)*24]
                draw.ellipse((center[0]-10, center[1]-10, center[0]+10, center[1]+10), fill='#ffdf00', outline='black', width=2)
                draw.text((center[0]+13, center[1]-12), str(c['ordinal'])+':'+str(x)+','+str(y), fill='#ffdf00', stroke_width=2, stroke_fill='black')
                points.append(dict(create_ordinal=c['ordinal'], xy=[x,y], raw_three_u16=values,
                                   modern_projected_center=center, original_NPC_sprite_drawn=False))
                if coordinate_field != 'borncorner':
                    points[-1].update(source_coordinate_field=coordinate_field,
                                      source_coordinate_literal=c[coordinate_field],
                                      actual_spawn_cell_verified=False)
            marked_png = encode_image(marked)
            private[f'map-source/{floor}.dat'] = raw
            private[f'scenes/{floor}-original-candidate.png'] = encode_image(full)
            private[f'scenes/{floor}-source-points.png'] = marked_png
            thumb = marked.convert('RGB'); thumb.thumbnail((700,550)); thumbs.append((floor,thumb))
            results.append(dict(floor=floor, original_DAT_bytes=len(raw), original_DAT_sha256=sha(raw),
                                geometry=[w,h], source_draw_positions=len(selected),
                                unique_source_images=len(keys), canvas_size=size, origin=origin,
                                three_candidate_RGBA_sha256=digests,
                                independent_Pillow_and_NumPy_all_three_equal=True,
                                marked_candidate_RGBA_sha256=sha(marked.tobytes()),
                                marked_candidate_PNG_sha256=sha(marked_png), source_points=points))
        # Keep only the needed source records for these three finite replays.
        wanted = {int(Path(n).stem) for n in private if n.startswith('map-source/tiles/')}
        private['map-source/records.json'] = json.dumps({str(k): model['records'][str(k)] for k in sorted(wanted)}).encode()
        private['map-source/image-source-receipts.json'] = json.dumps({str(k): sources[str(k)] for k in sorted(wanted)}).encode()
    columns=min(3,len(thumbs))
    contact = Image.new('RGB', (720*columns,600*((len(thumbs)+columns-1)//columns)), '#11232a'); draw = ImageDraw.Draw(contact)
    for i,(floor,im) in enumerate(thumbs):
        left,top=720*(i%columns),600*(i//columns)
        contact.paste(im,(left+(720-im.width)//2,top+45+(550-im.height)//2))
        draw.text((left+20,top+15), 'DAT '+str(floor)+' / source coordinates only',fill='white')
    private['three-original-scenes-contact.png'] = encode_image(contact)
    return results, len(wanted)


def derive(npc_path, item_path, map_path):
    assert sha(npc_path.read_bytes()) == NPC_ZIP_SHA
    assert sha(item_path.read_bytes()) == ITEM_ZIP_SHA
    q, ch, world = load(QUEST01), load(CHAR01), load(WORLD23)
    index = {r[0]:r for r in ch['source_files']}
    oldblocks = {(r['script_path'],r['script_block_ordinal']):r for r in q['source_event_blocks']}
    private = {}
    with zipfile.ZipFile(npc_path) as z:
        assert len(z.namelist()) == 2205 and z.testzip() is None
        for n in z.namelist():
            b=z.read(n); assert [len(b),sha(b),f'{z.getinfo(n).CRC:08x}'] == index[n[4:]][1:4]
        raw = {p:z.read('npc/'+p) for p in FILES}
        private.update({'original-npc/'+p:b for p,b in raw.items()})
        creates = parse_creates(raw[CREATE])
        for c in creates:
            # Only two box labels are required to disambiguate actual source binding.
            c['box_size_source_label'] = c['original_name'] if c['ordinal'] in (5,6) else None
            del c['original_name']
        scripts=[]
        for path in SCRIPTS:
            events=numeric_events(raw[path])
            for e in events:
                old=oldblocks[(path,e['ordinal'])]
                assert (e['event_no'],e['type'],e['condition_sha256'],e['section_sha256']) == (
                    old['event_number'],old['raw_type'],old['condition_expression_decoded_cp950_UTF8_sha256'],old['source_section_decoded_cp950_normalized_UTF8_sha256'])
            scripts.append(dict(**source_info(path,raw[path]),events=events))
        grants = {str(i):[] for i in ITEM_IDS}
        for n in z.namelist():
            for line_no,line in enumerate(z.read(n).splitlines(),1):
                m=re.match(rb'\s*GetItem:\s*(.*)',line)
                if not m: continue
                for i in ITEM_IDS:
                    if re.search(rb'(?<![0-9])'+str(i).encode()+rb'(?![0-9])',m.group(1)):
                        grants[str(i)].append(dict(path=n[4:],physical_line=line_no,source_line_sha256=sha(line)))
    # Original catalogue has more than one script that sets each flag. Keep all;
    # an integer match is not an exclusive quest identity or a runtime dependency.
    prerequisite_sources = {str(f):[dict(script=b['script_path'],ordinal=b['script_block_ordinal'],
                                       section_sha256=b['source_section_decoded_cp950_normalized_UTF8_sha256'],
                                       catalog_only_cross_reference=True)
                                  for b in q['source_event_blocks'] if f in b['end_set_flags']]
                            for f in (39,40,42)}
    items=[]
    public_items={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    with zipfile.ZipFile(item_path) as z:
        assert z.testzip() is None
        cat=json.loads(z.read('private-full-catalog.json'))
        itemindex={x['id']:x for x in cat['items']}
        imageindex={x['source_itemset_image_number_alias']:x for x in cat['image_source_receipts']}
        for i in ITEM_IDS:
            rows=[]
            for col,table in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                record=itemindex[i][table];columns=record['original_94_columns']
                b=','.join(columns).encode('cp950');assert len(columns)==94 and int(columns[16])==i
                assert sha(b)==record['original_row_sha256']==public_items[i][col]
                private[f'original-itemrows/{table}/{i}.txt']=b+b'\n'
                rows.append(dict(table=table,row=record['source_row_1based'],sha256=sha(b),image_alias=int(columns[17])))
            alias=rows[0]['image_alias'];assert rows[1]['image_alias']==alias
            image=imageindex[alias];assert image['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png=z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png');assert sha(png)==image['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-item-candidates/{alias}.png']=png
            items.append(dict(item_ID=i,source_rows=rows,cross_carrier_candidate_alias=alias,
                              original_RD_sha256=image['original_RD_SHA256'],candidate_PNG_sha256=sha(png)))
    observations, scene_images=scene_observation(map_path,creates,private)
    oldpoolrows=[x for x in world['WORLD09_additive_correction']['source_comparison_rows'] if x[0] in SCRIPTS[5:]]
    report=dict(schema='stoneage.quest22.hekisei_source_and_three_scene_observations.r1',date='2026-11-08',
        initial_remote=dict(head='0234d90c0e0c961c83fe9159cc14b825baf05935',tree='2cf6dd796295da869618955c34b8cf56e5de29a0',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        private_verified_carriers=dict(NPC_sha256=NPC_ZIP_SHA,NPC_all_member_CRC_and_SHA=2205,
            item_ZIP_sha256=ITEM_ZIP_SHA,item_ZIP_CRC_members=838,MAP09_ZIP_sha256=MAP_ZIP_SHA,MAP09_ZIP_CRC_members=4195,
            parent_RAR_sha256=PARENT_RAR_SHA,parent_RAR_reread=False),
        old_evidence_inputs=[pin(n) for n in [QUEST01,CHAR01,WORLD23,MAP09]],
        source_manifest=[source_info(p,raw[p]) for p in FILES], source_creates=creates, source_scripts=scripts,
        original_events_already_in_QUEST01=sum(len(s['events']) for s in scripts),newly_discovered_original_scripts=0,
        prerequisites=dict(original_three_request_conditions=[e['condition_literal'] for e in scripts[0]['events'][:3]],
                           all_existing_catalog_flag_setter_occurrences=prerequisite_sources,
                           flags_are_exclusive_quest_IDs_verified=False,original_three_requests_collapsed_into_AND=False),
        preserved_crafting_condition=dict(script=SCRIPTS[3],ordinal=1,
            literal=scripts[3]['events'][1]['condition_literal'],
            second_comma_clause_explicitly_checks_2767_and_2768=False,
            native_boolean_evaluation_priority_or_bug_verified=False),
        old_WORLD09_and_WORLD23_pools=dict(old_comparison_rows=oldpoolrows,new_random_pool_discoveries=0,
            ordered_source_positions=[list(map(int,s['events'][0]['commands']['GetRandItem'][0].split(','))) for s in scripts[5:]],
            original_probability_distribution_verified=False),
        core_items=items,full_2205_NPC_GetItem_literal_occurrences=grants,
        three_actual_DAT_scene_observations=observations,
        distinct_replayed_original_scene_candidate_PNGs=scene_images,
        map_3400=dict(source_create_ordinal=1,xy=[63,72],matching_original_DAT_in_955_batch=False,
                      original_NPC_sprite_or_scene_drawn=False),
        private_new_observation=dict(original_DAT_files_reread=3,source_NPC_positions_measured=6,
            complete_candidate_frames_independently_replayed=9,new_original_RD_decodes=0,
            original_assets_browser_executed=False,original_game_executed=False),
        boundaries=dict(official_JSS1999_TW10_CN182_deployment_authenticated=False,
            native_item_exchange_random_reward_or_NPC_executed=False,
            source_condition_punctuation_promoted_to_runtime_semantics=False,
            original_NPC_sprites_drawn=False,native_palette_layer_order_or_collision_verified=False,
            private_original_dialogue_DAT_or_image_published=False,task_permanent_or_event_origin='UNRESOLVED'),
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',R79='PAUSED_NON_BLOCKING',overall_percent=None,
        next='QUEST23_MODULE_MATERIAL_REVIEW_AFTER_LIULI_AND_HEKISEI_SOURCE_INTEGRATION')
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    sections=[]
    for path in FILES:
        sections.append('<details><summary>'+html.escape(path)+'</summary><pre>'+html.escape(raw[path].decode('cp950'))+'</pre></details>')
    page='<!doctype html><meta charset="utf-8"><title>QUEST22 原资料</title><style>body{font:16px sans-serif;max-width:1100px;margin:30px auto;background:#11232a;color:#eee}img{max-width:100%}pre{white-space:pre-wrap;background:#20343b;padding:18px}summary{cursor:pointer;padding:8px}a{color:#ffdf00}</style><h1>碧青洞窟：原配置与三张地图候选</h1><p>后期社区保存本原资料。黄色圆点只标原CREATE坐标，没有绘制原NPC、验证原生任务或进入原游戏。3400地图本批缺源。展开原文保留CP950原字节的Unicode解码；原文件另存。</p>'
    page+='<img src="three-original-scenes-contact.png" alt="三张原DAT候选画面与来源点">'
    page+=''.join(f'<p><a href="scenes/{f}-source-points.png">查看 {f} 完整来源标记画面</a></p>' for f in FLOORS)
    page+=''.join(sections)
    private['index.html']=page.encode('utf-8')
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('npc-zip','item-zip','map-zip','private-zip'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT)
    a=p.parse_args()
    assert ROOT not in a.private_zip.resolve().parents, 'original assets must stay outside the Git checkout'
    r,private=derive(a.npc_zip,a.item_zip,a.map_zip)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name,b in sorted(private.items()):z.writestr(name,b)
    contact=a.private_zip.parent/'quest22-three-scenes-contact.png';contact.write_bytes(private['three-original-scenes-contact.png'])
    print(json.dumps(dict(old_event_count=r['original_events_already_in_QUEST01'],measured_points=6,
                         scene_candidates=3,verified_frames=9,private_members=len(private))))


if __name__=='__main__':main()
