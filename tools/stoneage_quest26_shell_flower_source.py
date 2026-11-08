"""Source-only shell/flower courier and flag-2 dossier; never execute predicates."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest08_mining_source import load_private_source
from tools.stoneage_quest17_dino_ranch_source import ITEM_ZIP_SHA, NPC_ZIP_SHA, source_info, sha
from tools.stoneage_quest21_liuli_source import ROOT, REC, QUEST01, CHAR01, load, pin
from tools.stoneage_quest23_poru_source import catalog_sections
from tools.stoneage_quest25_island_tour_source import section_text, Q05

OUTPUT = REC / 'STONEAGE-QUEST26-SHELL-FLOWER-FLAG2-SOURCE-R1.json'
CREATE = 'sainasu/event/event02.create'
SCRIPTS = ('sainasu/event/event02_1', 'sainasu/event/event02_2')
Q24 = 'STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-R1.json'
Q25 = 'STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json'


def read_source_items(item_path, item_ids, private):
    """Reuse exact two-table source rows and qualified candidate images."""
    public = {r[0]: r for n in range(1, 8) for r in load(
        f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
    assert sha(item_path.read_bytes()) == ITEM_ZIP_SHA
    items = []; item_labels = {}
    with zipfile.ZipFile(item_path) as z:
        assert len(z.namelist()) == 838 and z.testzip() is None
        cat = json.loads(z.read('private-full-catalog.json'))
        index = {x['id']: x for x in cat['items']}
        images = {x['source_itemset_image_number_alias']: x for x in cat['image_source_receipts']}
        for item in item_ids:
            source_rows = []
            for col, table in ((1, 'itemset.txt'), (2, 'itemset0710.txt')):
                r = index[item][table]; columns = r['original_94_columns']; raw = ','.join(columns).encode('cp950')
                assert len(columns) == 94 and int(columns[16]) == item
                assert sha(raw) == r['original_row_sha256'] == public[item][col]
                private[f'original-itemrows/{table}/{item}.txt'] = raw + b'\n'
                source_rows.append(dict(table=table, row=r['source_row_1based'], sha256=sha(raw), image_alias=int(columns[17])))
            alias = source_rows[0]['image_alias']; assert source_rows[1]['image_alias'] == alias
            image = images[alias]; assert image['tw1_original_RD_status'] == 'VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png = z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png')
            assert sha(png) == image['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-item-candidates/{alias}.png'] = png
            columns = index[item]['itemset.txt']['original_94_columns']; item_labels[item] = (columns[0], columns[2])
            items.append(dict(item_ID=item, source_rows=source_rows, cross_carrier_candidate_alias=alias,
                              original_RD_sha256=image['original_RD_SHA256'], candidate_PNG_sha256=sha(png)))
    return items, item_labels


def derive(npc_path, item_path):
    _, character, data = load_private_source(npc_path)
    quest, poru, tours = load(QUEST01), load(Q24), load(Q25)
    rows = [r for r in character['create_rows'] if r[0] == CREATE]
    assert len(rows) == 2
    files = {CREATE, *SCRIPTS}; creates = []
    templates = {(r[0], r[1]): r for r in character['template_rows']}
    for row in rows:
        assert sha(data[CREATE][row[2]:row[3]]) == row[4]
        assert len(row[13]) == len(row[15]) == 1
        path, _, digest = row[15][0]; assert sha(data[path]) == digest
        tp, ordinal = row[13][0]; files.add(tp)
        assert templates[tp, ordinal][4] == 'ExChangeMan'
        creates.append(dict(create_ordinal=row[1], block_sha256=row[4], floor=row[5],
            graphic_alias=row[6], borncorner=row[7], borncenter=row[8], direction=row[10],
            template_token=row[11], template_path=tp, template_ordinal=ordinal,
            functionset=templates[tp, ordinal][4], script_path=path))
    scripts = []; flag_controls = []
    for path in SCRIPTS:
        old = [b for b in quest['source_event_blocks'] if b['script_path'] == path]
        events = catalog_sections(data[path], old)
        assert len(events) == 3
        for event in events:
            section = section_text(data[path], event)
            clean = re.findall(r'(?m)^CleanFlg:([^\r\n]*)', section)
            if clean:
                event['commands']['CleanFlg'] = clean
            event['source_SP_literals_in_order'] = list(map(int, re.findall(r'(?<![A-Z_])SP=(\d+)', event['condition_literal'])))
            for field in ('CleanFlg', 'EndSetFlg'):
                for value in event['commands'].get(field, []):
                    assert value == '2'
                    flag_controls.append(dict(script_path=path, event_ordinal=event['ordinal'],
                        type=event['type'], field=field, value=2,
                        condition_literal=event['condition_literal'], section_sha256=event['section_sha256']))
        scripts.append(dict(**source_info(path, data[path]), events=events))
    private = {'original-npc/' + p: data[p] for p in sorted(files)}
    items, item_labels = read_source_items(item_path, (2414, 2415), private)
    # Exact numeric-token match: never confuse ENDEV=2 with ENDEV=20 or =28.
    consumers = [dict(script_path=s['path'], event_ordinal=e['ordinal'], type=e['type'],
                     condition_literal=e['condition_literal'], section_sha256=e['section_sha256'])
                 for s in tours['source_scripts'] for e in s['events']
                 if re.search(r'(?<![A-Z_])ENDEV=2(?!\d)', e['condition_literal'])]
    old_setters = [dict(script_path=b['script_path'], event_ordinal=b['script_block_ordinal'],
                       section_sha256=b['source_section_decoded_cp950_normalized_UTF8_sha256'])
                   for b in quest['source_event_blocks'] if 2 in b['end_set_flags']]
    assert old_setters == [dict(script_path=s['path'], event_ordinal=1,
                               section_sha256=s['events'][1]['section_sha256']) for s in scripts]
    floors = [f for f in load(Q05)['floors'] if f['source_floor_id'] in (1000, 2000)]
    report = dict(schema='stoneage.quest26.shell_flower_courier_flag2.r1', date='2026-11-08',
        initial_remote=dict(head='697cc471c3643e78e1036b53f8fbb69fe108f627', tree='1d36517b5256d526f0d1f65c3f75322ff54aba99',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        verified_private_carriers=dict(NPC_ZIP_sha256=NPC_ZIP_SHA, NPC_members_SHA_CRC=2205,
            ITEM_ZIP_sha256=ITEM_ZIP_SHA, ITEM_members_CRC=838, parent_RAR_reread=False),
        old_evidence_inputs=[pin(p) for p in (QUEST01, CHAR01, Q05, Q24, Q25)],
        source_manifest=[source_info(p, data[p]) for p in sorted(files)], source_creates=creates,
        source_scripts=scripts, existing_QUEST01_TYPE_sections=6, new_original_script_discoveries=0,
        source_flag2_controls=flag_controls, old_QUEST01_flag2_setters=old_setters,
        existing_QUEST25_ENDEV2_consumers=consumers,
        existing_QUEST24_same_item2414_gates=poru['actual_source_warpman_parameters'],
        existing_QUEST24_alternative_item2414_grant=poru['meat_shell_source'],
        source_items=items, source_map_metadata_reused=floors,
        boundaries=dict(SP_interpreted_as_sex_birthplace_or_location=False,
            comma_conditions_interpreted=False, omitted_quantity_replaced_with_one=False,
            CLEAN_resets_runtime_or_persistence_verified=False, flag2_called_tour_completion=False,
            sole_shell_source_assumed=False, same_item_ID_merges_quest_identities=False,
            original_DAT_or_NPC_sprite_replayed=False, original_client_or_server_executed=False,
            public_CI_reads_private_assets=False, original_assets_or_dialogue_published=False,
            official_same_deployment_authenticated=False, quest_origin='UNRESOLVED'),
        stage_A={'PARTIAL': 7, 'OPEN': 2}, stage_B='GATED', wiki='GATED', R79='PAUSED_NON_BLOCKING',
        overall_percent=None, next='QUEST27_SOURCE_READY_QUEST_BATCH_AFTER_SHELL_FLOWER_FLAG2_STOP')
    private['source-summary-derived.json'] = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    page = '<!doctype html><meta charset="utf-8"><title>QUEST26 贝壳与花互送原资料</title><style>body{font:16px sans-serif;max-width:1050px;margin:30px auto;background:#14272c;color:#eee}a{color:#ffe073}pre{white-space:pre-wrap;background:#29434c;padding:16px}td,th{border:1px solid #52717b;padding:10px}table{border-collapse:collapse;width:100%}summary{cursor:pointer;padding:10px}img{image-rendering:pixelated;max-width:160px}</style><h1>贝壳／花互送与旗标2</h1><p>后期社区保存原件的静态关系。SP只保留原整数，不推性别／出生村；清除、交换、分支顺序和传送效果均未运行验证。原文、道具和图像各保留来源；本页不是原游戏。</p><table><tr><th>原NPC配置</th><th>原段</th><th>原条件</th><th>原命令</th></tr>'
    for c, s in zip(creates, scripts, strict=True):
        for e in s['events']:
            page += '<tr><td>'+str(c['floor'])+' / '+str(c['borncorner'])+'</td><td>'+e['type']+'</td><td>'+html.escape(e['condition_literal'])+'</td><td>'+html.escape(json.dumps(e['commands']))+'</td></tr>'
    page += '</table><h2>相关原道具与台湾1.0跨来源候选图</h2>'
    for item in items:
        i = item['item_ID']; name, description = item_labels[i]
        page += f'<h3>{i} {html.escape(name)}</h3><img src="cross-carrier-TW1-item-candidates/{item["cross_carrier_candidate_alias"]}.png"><p>{html.escape(description)}</p>'
    page += '<h2>已恢复的其他任务引用</h2><p>原ENDEV2条件出现在环岛路线，原ITEM2414条件也出现在波拉岛WarpMan；不据相同数字合并任务身份或宣称贝壳只能来自本任务。</p>'
    page += '<pre>'+html.escape(json.dumps(dict(tour_flag2_consumers=consumers, poru_gates=poru['actual_source_warpman_parameters'], alternative_grant=poru['meat_shell_source']), ensure_ascii=False, indent=2))+'</pre>'
    page += '<h2>完整来源原文</h2>'
    for path in sorted(files):
        page += f'<details><summary>{html.escape(path)}</summary><pre>{html.escape(data[path].decode("cp950"))}</pre></details>'
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
    print(json.dumps(dict(source_files=len(report['source_manifest']), events=6,
                         flag2_tour_consumers=len(report['existing_QUEST25_ENDEV2_consumers']), private_members=len(private))))


if __name__ == '__main__':
    main()
