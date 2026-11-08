"""Liuli source comparison; proprietary files are read/written only by explicit private paths.

Reuse QUEST17's CP950-aware parsers. Numeric literals are source evidence, not an
interpreter for ExChangeMan, random rewards, NPC selection, or original movement.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest17_dino_ranch_source import (
    NPC_ZIP_SHA, ITEM_ZIP_SHA, PARENT_RAR_SHA, parse_creates, parse_events,
    source_info, sha,
)

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
OUTPUT = REC / 'STONEAGE-QUEST21-LIULI-ORIGINAL-SOURCE-COMPARISON-R1.json'
QUEST01 = 'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
CHAR01 = 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP04 = 'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
GUIDE = 'STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.json'
CREATE = 'jaruga/event/ruri.create'
SCRIPTS = ['jaruga/event/ruri%02d' % n for n in range(1, 7)]
ALT = 'jaruga/event/ruri03a'
MAP_CREATE = 'genout/ruri.create'
WARP_ARG = 'genout/wpm_21003_34_10'
FILES = [CREATE, *SCRIPTS, ALT, 'jaruga/event/event.template', MAP_CREATE, WARP_ARG]
CORE_ITEMS = [2698, 2699, 2700, 2701, 3900, 19292]


def load(name):
    return json.loads((REC / name).read_text('utf-8'))


def pin(name):
    b = (REC / name).read_bytes()
    return {'path': 'research/recovered/' + name, 'bytes': len(b), 'sha256': sha(b),
            'git_blob': hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()}


def graph(raw):
    """Preserve every decoded CREATE occurrence, including shared source tiles."""
    out = []
    for ordinal, m in enumerate(re.finditer(r'\{[^{}]*\}', raw.decode('cp950', 'strict'))):
        f = dict(re.findall(r'(?m)^\s*([A-Za-z_]+)\s*=\s*(.+?)\s*$', m.group()))
        enemy = f['enemy'].split('|')
        out.append(dict(ordinal=ordinal, block_sha256=sha(m.group().encode('cp950')),
                        floor=int(f['floorid']), borncorner=list(map(int, f['borncorner'].split(','))),
                        template=enemy[0], target=list(map(int, enemy[1:]))
                        if enemy[0] == 'npcgen_warp' else None,
                        argument_path=enemy[1][5:] if len(enemy) == 2 and enemy[1].startswith('file:') else None))
    return out


def shared_warp_tiles(rows):
    groups = defaultdict(list)
    for row in rows:
        if row['target'] is not None:
            groups[(row['floor'], *row['borncorner'][:2])].append(row)
    return [dict(source=list(k), ordinals=[r['ordinal'] for r in v],
                 targets=[r['target'] for r in v]) for k, v in sorted(groups.items()) if len(v) > 1]


def numeric_events(raw):
    events = parse_events(raw)
    text = raw.decode('cp950').replace('\r\n', '\n')
    starts = list(re.finditer(r'(?m)^EventNo:(-?\d+)\s*$', text))
    for e, m in zip(events, starts, strict=True):
        end = re.search(r'(?m)^EventEnd\s*$', text[m.start():])
        section = text[m.start():m.start() + end.end()]
        for key in ('NpcWarp', 'Charm'):
            values = re.findall(rf'(?m)^\s*{key}:([^\r\n]*)', section)
            if values:
                e['commands'][key] = [v.strip() for v in values]
        e['bare_Break_lines'] = len(re.findall(r'(?m)^Break\s*$', section))
    return events


def derive(npc_path: Path, item_path: Path):
    assert sha(npc_path.read_bytes()) == NPC_ZIP_SHA
    assert sha(item_path.read_bytes()) == ITEM_ZIP_SHA
    q, ch, maps, guide = load(QUEST01), load(CHAR01), load(MAP04), load(GUIDE)
    file_index = {r[0]: r for r in ch['source_files']}
    oldscripts = {r['path']: r for r in q['source_scripts']}
    oldblocks = {(r['script_path'], r['script_block_ordinal']): r for r in q['source_event_blocks']}
    private = {}
    with zipfile.ZipFile(npc_path) as z:
        assert len(z.namelist()) == 2205 and z.testzip() is None
        for n in z.namelist():
            b = z.read(n); row = file_index[n.removeprefix('npc/')]
            assert [len(b), sha(b), f'{z.getinfo(n).CRC:08x}'] == row[1:4]
        raw = {p: z.read('npc/' + p) for p in FILES}
        private.update({'original-npc/' + p: b for p, b in raw.items()})
        creates = parse_creates(raw[CREATE])
        for c in creates:
            # Original labels stay private; the public projection uses numbers and paths.
            del c['original_name']
            old = next(r for r in q['source_creation_references']
                       if r['create_source_path'] == CREATE and r['create_brace_ordinal'] == c['ordinal'])
            assert (c['floor'], c['graphic_alias'], c['script_ref']) == (
                old['floorid'], old['graphic_alias_numeric'], old['original_script_path'])
        scripts = []
        for p in SCRIPTS:
            b = raw[p]; info = source_info(p, b); old = oldscripts[p]
            assert (len(b), sha(b), info['crc32']) == (old['original_size'], old['original_sha256'], old['original_crc32'])
            events = numeric_events(b)
            for e in events:
                o = oldblocks[(p, e['ordinal'])]
                assert (e['event_no'], e['type'], e['condition_sha256'], e['section_sha256']) == (
                    o['event_number'], o['raw_type'], o['condition_expression_decoded_cp950_UTF8_sha256'],
                    o['source_section_decoded_cp950_normalized_UTF8_sha256'])
            scripts.append(dict(**info, events=events))
        alt_refs = []
        exact = rb'file:' + ALT.encode() + rb'(?![A-Za-z0-9_./])'
        feather_grants = []
        for n in z.namelist():
            b = z.read(n)
            if n.endswith(('.create', '.bak')) and re.search(exact, b):
                alt_refs.append(n.removeprefix('npc/'))
            if re.search(rb'(?m)^\s*GetItem:\s*[^\r\n]*?(?<![0-9])2700(?![0-9])', b):
                feather_grants.append(n.removeprefix('npc/'))

    events = [e for s in scripts for e in s['events']]
    son = scripts[2]['events'][1]
    npcwarp_literal = son['commands']['NpcWarp'][0]
    npcwarp = [list(map(int, x.split('.'))) for x in npcwarp_literal.split(',')]
    original_graph = graph(raw[MAP_CREATE])
    warp_text = raw[WARP_ARG].decode('cp950')
    warp_values = {k: re.search(rf'(?m)^{k}:(.*)$', warp_text).group(1).strip()
                   for k in ('WARP', 'FREE', 'MONEY')}
    floor_index = {int(Path(r[0]).stem): r for r in maps['per_floor_source_rows']}
    floors = sorted({r['floor'] for r in original_graph} | {r['floor'] for r in creates}
                    | {r['target'][0] for r in original_graph if r['target']})
    map_joins = []
    for f in floors:
        row = floor_index.get(f)
        map_joins.append(dict(floor=f, source_DAT_sha256=row[2] if row else None,
                             geometry=row[3:5] if row else None,
                             status='PREVIOUS_MAP04_ORIGINAL_DAT' if row else 'NO_MATCHING_DAT_IN_955_BATCH',
                             original_DAT_bytes_reread_this_round=0))

    pools = []
    for s in scripts[4:6]:
        literal = s['events'][0]['commands']['GetRandItem'][0]
        ids = list(map(int, literal.split(',')))
        pools.append(dict(script=s['path'], original_argument_sha256=sha(literal.encode()),
                          literal_item_IDs=ids, positions=len(ids), distinct_IDs=len(set(ids)),
                          duplicate_extra_positions=len(ids) - len(set(ids)),
                          probability_or_number_of_rewards=None))
    item_rows, images = [], {}
    public_items = {r[0]: r for n in range(1, 8)
                    for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    with zipfile.ZipFile(item_path) as z:
        assert z.testzip() is None
        catalog = json.loads(z.read('private-full-catalog.json'))
        items = {r['id']: r for r in catalog['items']}
        receipts = {r['source_itemset_image_number_alias']: r for r in catalog['image_source_receipts']}
        for i in CORE_ITEMS:
            item = items[i]; rows = []
            for col, name in ((1, 'itemset.txt'), (2, 'itemset0710.txt')):
                original = item[name]; columns = original['original_94_columns']
                b = ','.join(columns).encode('cp950', 'strict')
                assert len(columns) == 94 and int(columns[16]) == i
                assert sha(b) == original['original_row_sha256'] == public_items[i][col]
                private[f'original-itemrows/{name}/{i}.txt'] = b + b'\n'
                rows.append(dict(table=name, row=original['source_row_1based'], sha256=sha(b),
                                 image_alias=int(columns[17]), columns=94))
            alias = rows[0]['image_alias']; assert rows[1]['image_alias'] == alias
            receipt = receipts[alias]
            image = dict(alias=alias, source_status=receipt['tw1_original_RD_status'],
                         candidate_PNG_sha256=None, original_RD_sha256=None)
            if receipt['tw1_original_RD_status'] == 'VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':
                png = z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png')
                assert sha(png) == receipt['candidate_PNG_SHA256']
                image.update(candidate_PNG_sha256=sha(png), original_RD_sha256=receipt['original_RD_SHA256'])
                private[f'cross-carrier-TW1-original-RD/alias-{alias}.png'] = png
            images[alias] = image
            item_rows.append(dict(item_ID=i, source_rows=rows, source_image_alias=alias))

    guide_son = next(x for x in guide['extraction']['npc_occurrences'] if x['role'] == 'lost_son_diary_handoff')
    report = dict(
        schema='stoneage.quest21.liuli_original_source_comparison.r1', date='2026-11-08',
        initial_remote=dict(head='cdd36eff03dd1131339f9b85b09222b60fc64fa4', tree='8bbceff7c0263ca72b38e4a6c772a06b667f3fb0',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        private_archive_verification=dict(npc_sha256=NPC_ZIP_SHA, NPC_members_CRC_and_full_source_hashes=2205,
                                          item_zip_sha256=ITEM_ZIP_SHA, item_zip_members_CRC=838,
                                          parent_RAR_sha256=PARENT_RAR_SHA, parent_RAR_reread_this_round=False),
        previous_inputs=[pin(n) for n in [QUEST01, CHAR01, MAP04, GUIDE]],
        source_manifest=[source_info(p, raw[p]) for p in FILES],
        source_creates=creates, source_scripts=scripts,
        source_event_count=len(events), source_event_types=dict(Counter(e['type'] for e in events)),
        old_QUEST01_script_count=6, old_QUEST01_event_count=len(events), newly_discovered_original_scripts=0,
        source_unreferenced_alternate=dict(**source_info(ALT, raw[ALT]), events=numeric_events(raw[ALT]),
                                          exact_CREATE_or_backup_references=alt_refs,
                                          actual_loader_selection_verified=False),
        son_relocation=dict(source_script=SCRIPTS[2], raw_NpcWarp_argument_sha256=sha(npcwarp_literal.encode()),
                            source_target_occurrences=npcwarp, different_target_count=len(set(map(tuple, npcwarp))),
                            source_CREATE_is_one_configuration=True, actual_random_weighting=None),
        original_random_pools=pools, core_item_rows=item_rows,
        cross_carrier_candidate_images=list(images.values()),
        feather_2700=dict(source_GetItem_literal_files_in_full_2205_NPC_corpus=feather_grants,
                          scan_proves_enemy_drop_table_or_runtime=False,
                          original_enemy_drop_or_guide_target_ID_verified=False),
        original_map_create=dict(path=MAP_CREATE, sha256=sha(raw[MAP_CREATE]), creates=original_graph,
                                 source_warp_occurrences=sum(r['target'] is not None for r in original_graph),
                                 shared_source_tiles=shared_warp_tiles(original_graph),
                                 original_collision_or_route_executed=False),
        conditional_warp=dict(path=WARP_ARG, sha256=sha(raw[WARP_ARG]), source_values=warp_values,
                              same_archive_CREATE_ordinal=58, actual_admission_or_fee_verified=False),
        map_qualification=map_joins,
        existing_2003_guide_comparison=dict(
            source_profile=guide['version_profile'], source_original_game_build=None,
            current_pages_or_historical_HTML_refetched_this_round=False,
            documentary_son_eight_positions=guide_son['reported_search_positions'],
            source_distinct_positions_equal_documentary_set=(set(map(tuple, guide_son['reported_search_positions'])) == set(tuple(v[1:]) for v in npcwarp)),
            source_duplicate_position=[115, 1011],
            documentary_judgment_floor=4, documentary_judgment_xy=[34, 10],
            source_conditional_CREATE_floor=21003, source_conditional_CREATE_xy=[34, 10],
            source_floor_ID_equals_documentary_ordinal_verified=False,
            same_game_version_or_deployment_verified=False,
            guide_old_original_ID_nulls_preserved=True,
        ),
        boundaries=dict(native_quest_or_random_rewards_executed=False,
                        official_JSS1999_TW10_CN182_source_deployment_authenticated=False,
                        shared_coordinate_CREATE_selection_priority_verified=False,
                        random_candidate_list_duplicates_prove_probabilities=False,
                        item_icon_source_authenticates_same_build=False,
                        new_original_DAT_cells_or_RD_decodes=0,
                        original_game_programs_assets_or_dialogue_published=False,
                        original_permanent_versus_operated_event_origin='UNRESOLVED'),
        stage_A={'PARTIAL': 7, 'OPEN': 2}, stage_B='GATED', wiki='GATED',
        R79='PAUSED_NON_BLOCKING', overall_percent=None,
        next='QUEST22_DISTINCT_SOURCE_READY_FAMILY_AFTER_DEDUP_OR_MATERIAL_GAMEPLAY_REVIEW',
    )
    private['README.txt'] = (
        'QUEST21 琉璃洞窟原资料（私人研究材料）\n'
        'original-npc：后期社区 mixed25 保存本原字节；CP950 编码。\n'
        'original-itemrows：已认证两份94栏物品表的六个道具原行，非本轮整表提取。\n'
        'cross-carrier-TW1-original-RD：既有台湾1.0候选PNG，不能认证同版或同服。\n'
        'source-summary-derived.json：来源散列、条件、地图和攻略比较；不含原对白。\n'
        '未运行原客户端、任务、随机奖品或传送；不能作为可玩游戏。\n'
    ).encode('utf-8')
    private['source-summary-derived.json'] = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    return report, private


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--npc-zip', required=True, type=Path)
    p.add_argument('--item-zip', required=True, type=Path)
    p.add_argument('--output', type=Path, default=OUTPUT)
    p.add_argument('--private-zip', type=Path)
    a = p.parse_args()
    report, private = derive(a.npc_zip, a.item_zip)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if a.private_zip:
        with zipfile.ZipFile(a.private_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
            for name, raw in sorted(private.items()):
                z.writestr(name, raw)
    print(json.dumps({'events': report['source_event_count'], 'NPC_creates': len(report['source_creates']),
                      'warp_occurrences': report['original_map_create']['source_warp_occurrences'],
                      'private_members': len(private)}))


if __name__ == '__main__':
    main()
