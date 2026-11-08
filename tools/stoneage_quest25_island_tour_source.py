"""Restore four source tour dossiers, not a quest interpreter or native route map.

Exact original files remain in the explicitly supplied private ZIPs. Public
output contains numeric controls, source locations and hashes only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest08_mining_source import load_private_source
from tools.stoneage_quest17_dino_ranch_source import ITEM_ZIP_SHA, NPC_ZIP_SHA, source_info, sha
from tools.stoneage_quest21_liuli_source import ROOT, REC, QUEST01, CHAR01, load, pin
from tools.stoneage_quest23_poru_source import catalog_sections, WORLD21

OUTPUT = REC / 'STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json'
Q05 = 'STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json'
CREATES = ('jaruga/event/oev.create', 'sainasu/event/oev2.create')
ROUTES = (
    ('A', 'jaruga/event/oev_', '', 'jaruga/event/oev_0', 'jaruga/event/oev_ed1', 2552),
    ('B', 'jaruga/event/oev_', 'b', 'jaruga/event/oev_0', 'jaruga/event/oev_edb', 2552),
    ('C', 'sainasu/event/oev_', 'c', 'sainasu/event/oev_0cd', 'sainasu/event/oev_edc', 2575),
    ('D', 'sainasu/event/oev_', 'd', 'sainasu/event/oev_0cd', 'sainasu/event/oev_edd', 2575),
)


def section_text(raw, event):
    """Find the exact old-catalogue section, without treating messages as controls."""
    lines = raw.decode('cp950').replace('\r\n', '\n').splitlines(keepends=True)
    start = event['type_line'] - 2  # EventNo immediately precedes TYPE in this batch.
    assert lines[start].startswith('EventNo:')
    end = next(i + 1 for i in range(start, len(lines)) if lines[i].strip() == 'EventEnd')
    text = ''.join(lines[start:end])
    assert sha(text.encode()) == event['section_sha256']
    return text


def derive(npc_path, item_path):
    _, character, data = load_private_source(npc_path)
    quest, world, crosswalk = load(QUEST01), load(WORLD21), load(Q05)
    source_rows = [r for r in character['create_rows'] if r[0] in CREATES]
    assert len(source_rows) == 54
    templates = {(r[0], r[1]): r for r in character['template_rows']}
    files = set(CREATES)
    creates = []
    for r in source_rows:
        assert sha(data[r[0]][r[2]:r[3]]) == r[4]
        assert len(r[15]) == len(r[13]) == 1
        path, _, digest = r[15][0]
        assert sha(data[path]) == digest
        tp, ordinal = r[13][0]; template = templates[(tp, ordinal)]
        assert r[11] == 'changeevent' and template[4] == 'ExChangeMan'
        files.update((path, tp))
        creates.append(dict(create_path=r[0], create_ordinal=r[1], block_sha256=r[4],
                            floor=r[5], borncorner=r[7], borncenter=r[8], direction=r[10],
                            graphic_alias=r[6], script_path=path, template_path=tp,
                            template_ordinal=ordinal, functionset=template[4]))
    by_path = {c['script_path']: c for c in creates}
    assert len(by_path) == 54
    scripts = []
    for path in sorted(by_path):
        old = [b for b in quest['source_event_blocks'] if b['script_path'] == path]
        scripts.append(dict(**source_info(path, data[path]), events=catalog_sections(data[path], old)))
    by_script = {s['path']: s for s in scripts}
    # This is an explicit-reference inventory, not a claim of complete analysis.
    previous = sorted(p for p in REC.glob('STONEAGE-QUEST*.json')
                      if re.match(r'STONEAGE-QUEST(?:0[8-9]|1[0-9]|2[0-4])-', p.name)
                      and 'PUBLICATION' not in p.name)
    old_paths = {s['path'] for s in quest['source_scripts']}
    mentioned = set()
    for p in previous:
        text = p.read_text('utf-8')
        mentioned.update(path for path in old_paths if json.dumps(path) in text)
    routes = []
    for label, prefix, suffix, start, finish, first in ROUTES:
        checkpoints = []
        for number in range(1, 13):
            path = f'{prefix}{number}{suffix}'
            matches = [e for e in by_script[path]['events'] if 'GetItem' in e['commands']]
            assert len(matches) == 1
            event = matches[0]; incoming = first + number - 1; outgoing = incoming + 1
            assert event['commands']['GetItem'] == [str(outgoing)]
            assert event['commands']['DelItem'] == [str(incoming)]
            text = section_text(data[path], event)
            block = data[by_path[path]['create_path']].decode('cp950')
            assert re.search(r'^name=.*' + re.escape(f'({label}-{number})') + r'\s*$', block, re.M)
            keywords = re.findall(r'(?m)^KeyWord:([^\r\n]*)', text)
            assert len(keywords) == 1
            kw = keywords[0]
            checkpoints.append(dict(number=number, source=by_path[path], event_ordinal=event['ordinal'],
                incoming_item=incoming, outgoing_item=outgoing, condition_literal=event['condition_literal'],
                keyword_CP950_bytes=len(kw.encode('cp950')), keyword_UTF8_sha256=sha(kw.encode()),
                keyword_raw_text_published=False))
        routes.append(dict(label=label, registration=by_path[start], finish=by_path[finish],
                           initial_proof_item=first, final_proof_item=first + 12, checkpoints=checkpoints,
                           source_order_is_native_reachability=False))
    events = [e for s in scripts for e in s['events']]
    item_ids = set()
    for event in events:
        item_ids.update(map(int, re.findall(r'ITEM[!=<>]+(\d+)', event['condition_literal'])))
        for key in ('GetItem', 'DelItem', 'GetRandItem'):
            for value in event['commands'].get(key, []):
                item_ids.update(map(int, re.findall(r'(?:^|,)\s*(\d+)', value)))
    private = {'original-npc/' + p: data[p] for p in sorted(files)}
    public_items = {r[0]: r for n in range(1, 8) for r in load(
        f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    assert sha(item_path.read_bytes()) == ITEM_ZIP_SHA
    items = []; labels = {}
    with zipfile.ZipFile(item_path) as z:
        assert len(z.namelist()) == 838 and z.testzip() is None
        catalog = json.loads(z.read('private-full-catalog.json'))
        item_index = {r['id']: r for r in catalog['items']}
        images = {r['source_itemset_image_number_alias']: r for r in catalog['image_source_receipts']}
        for item in sorted(item_ids):
            source_rows_i = []
            for column, table in ((1, 'itemset.txt'), (2, 'itemset0710.txt')):
                row = item_index[item][table]; columns = row['original_94_columns']
                raw = ','.join(columns).encode('cp950')
                assert len(columns) == 94 and int(columns[16]) == item
                assert sha(raw) == row['original_row_sha256'] == public_items[item][column]
                private[f'original-itemrows/{table}/{item}.txt'] = raw + b'\n'
                source_rows_i.append(dict(table=table, row=row['source_row_1based'], sha256=sha(raw), image_alias=int(columns[17])))
            cols = item_index[item]['itemset.txt']['original_94_columns']; labels[item] = (cols[0], cols[2])
            image = images[int(cols[17])]
            candidate = None
            if image['tw1_original_RD_status'] == 'VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':
                alias = int(cols[17]); png = z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png')
                assert sha(png) == image['candidate_PNG_SHA256']
                private[f'cross-carrier-TW1-item-candidates/{alias}.png'] = png
                candidate = dict(alias=alias, PNG_sha256=sha(png), original_RD_sha256=image['original_RD_SHA256'])
            items.append(dict(item_ID=item, source_rows=source_rows_i, cross_carrier_TW1_candidate=candidate))
    pet_sources = [s for s in world['source_GetPet_scripts_and_event_blocks'] if s['path'] in by_script]
    assert len(pet_sources) == 4
    for source in pet_sources:
        assert source['source_sha256'] == by_script[source['path']]['sha256']
        current = [list(map(int, value.split(','))) for e in by_script[source['path']]['events']
                   for value in e['commands'].get('GetPet', [])]
        assert current == [c['raw_integer_tokens_in_order'] for c in source['commands']]
    pet_ids = {i for s in pet_sources for c in s['commands'] for i in c['raw_integer_tokens_in_order']}
    floor_index = {r['source_floor_id']: r for r in crosswalk['floors']}
    floors = [floor_index[f] for f in sorted({c['floor'] for c in creates})]
    report = dict(schema='stoneage.quest25.four_island_tour_source_routes.r1', date='2026-11-08',
        initial_remote=dict(head='85d10f40670418f583db40c4a939a550b01219fe', tree='b75a665a537eec6731d286be97b6f8f5479d7e3b',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        verified_private_carriers=dict(NPC_ZIP_sha256=NPC_ZIP_SHA, NPC_members_SHA_CRC=2205,
                                       ITEM_ZIP_sha256=ITEM_ZIP_SHA, ITEM_members_CRC=838, parent_RAR_reread=False),
        old_evidence_inputs=[pin(p) for p in (QUEST01, CHAR01, WORLD21, Q05)],
        module_review=dict(previous_specialty_reports=[pin(p.name) for p in previous],
            QUEST01_scripts=295, previous_explicit_script_mentions=len(mentioned),
            this_batch_previously_mentioned_in_these_reports=sorted(set(by_script) & mentioned),
            this_batch_all_54_already_QUEST01_indexed=True, new_original_script_discoveries=0,
            four_reward_files_already_WORLD21=True, source_mentions_are_not_analysis_or_game_completion=True),
        source_manifest=[source_info(p, data[p]) for p in sorted(files)],
        source_creates=creates, source_scripts=scripts, routes=routes, source_items=items,
        source_map_metadata_reused=floors, original_DAT_reread=False, new_original_RD_decodes=0,
        existing_WORLD21_pet_sources=pet_sources,
        existing_WORLD21_instance_links=[p for p in world['original_enemy_instance_to_template_lookups'] if p['getpet_integer'] in pet_ids],
        event_counts=dict(old_QUEST01_TYPE_sections=len(events), keywords=48,
                          operations=dict(sorted(Counter(k for e in events for k in e['commands']).items()))),
        embedded_PetFullMsg_physical_lines=[dict(path=path, line=i, line_CP950_sha256=sha(line))
            for path in sorted(by_path) for i, line in enumerate(data[path].splitlines(keepends=True), 1)
            if b'PetFullMsg:' in line and not line.lstrip().startswith(b'PetFullMsg:')],
        boundaries=dict(source_branch_order_is_runtime_selection=False, keyword_matching_executed=False,
            comma_conditions_interpreted=False, reward_list_probabilities_verified=False,
            GetPet_lists_are_new_pet_discoveries=False, native_client_or_server_executed=False,
            original_assets_or_dialogue_published=False, official_same_deployment_authenticated=False,
            source_route_is_geographical_or_walkable_world_map=False, quest_origin='UNRESOLVED'),
        stage_A={'PARTIAL': 7, 'OPEN': 2}, stage_B='GATED', wiki='GATED', R79='PAUSED_NON_BLOCKING',
        overall_percent=None, next='QUEST26_SOURCE_READY_TASK_FAMILY_AFTER_FOUR_ROUTE_SOURCE_STOP')
    private['source-summary-derived.json'] = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    page = '<!doctype html><meta charset="utf-8"><title>QUEST25 四路线环岛任务原资料</title><style>body{font:16px sans-serif;max-width:1150px;margin:30px auto;background:#13252b;color:#eee}a{color:#ffe073}table{border-collapse:collapse;width:100%}td,th{padding:9px;border:1px solid #49616b}pre{white-space:pre-wrap;background:#243c44;padding:15px}summary{cursor:pointer;padding:10px}img{image-rendering:pixelated;max-width:100px}</style><h1>两岛环岛任务：A／B／C／D 原资料</h1><p>后期社区保存材料。路线按原NPC名称和文件字段分组；证明石序列不是可行走世界地图。所有问答、条件顺序、奖励重复位置按原文保留，未执行原游戏。原活动名称不证明运营限时起源。</p>'
    page += '<nav>' + ' · '.join(f'<a href="#route-{r["label"]}">{r["label"]}路线</a>' for r in routes) + ' · <a href="#items">道具</a> · <a href="#originals">完整原文</a></nav>'
    for route in routes:
        page += f'<h2 id="route-{route["label"]}">{route["label"]}路线</h2>'
        for role in ('registration', 'finish'):
            c = route[role]; page += f'<p>{role}: DAT {c["floor"]} / {c["borncorner"]} / <a href="#src-{c["script_path"]}">{c["script_path"]}</a></p>'
        page += '<table><tr><th>站</th><th>源floor／borncorner</th><th>证明石原命令</th><th>原条件／完整问答</th></tr>'
        for cp in route['checkpoints']:
            c = cp['source']; path = c['script_path']
            page += f'<tr><td>{cp["number"]}</td><td>{c["floor"]} / {c["borncorner"]}</td><td>{cp["incoming_item"]} → {cp["outgoing_item"]}</td><td>{html.escape(cp["condition_literal"])}<br><a href="#src-{path}">查看原问答和关键词</a></td></tr>'
        page += '</table>'
    page += '<h2 id="items">后期原道具与台湾1.0跨来源候选图</h2>'
    for item in items:
        i = item['item_ID']; name, description = labels[i]
        page += f'<details><summary>{i} {html.escape(name)}</summary><p>{html.escape(description)}</p>'
        if item['cross_carrier_TW1_candidate']:
            page += f'<img src="cross-carrier-TW1-item-candidates/{item["cross_carrier_TW1_candidate"]["alias"]}.png">'
        page += '</details>'
    page += '<h2 id="originals">完整来源原文，保留物理顺序</h2>'
    for path in sorted(files):
        page += f'<details id="src-{path}"><summary>{html.escape(path)}</summary><pre>{html.escape(data[path].decode("cp950"))}</pre></details>'
    private['index.html'] = page.encode()
    return report, private


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('npc-zip', 'item-zip', 'private-zip'):
        p.add_argument('--' + key, type=Path, required=True)
    p.add_argument('--output', type=Path, default=OUTPUT)
    a = p.parse_args(); assert ROOT not in a.private_zip.resolve().parents
    report, private = derive(a.npc_zip, a.item_zip)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(a.private_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        for name, raw in sorted(private.items()):
            z.writestr(name, raw)
    print(json.dumps(dict(scripts=54, events=report['event_counts'], item_IDs=len(report['source_items']), private_members=len(private))))


if __name__ == '__main__':
    main()
