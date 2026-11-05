#!/usr/bin/env python3
"""Batch original handover quest content. Lexical evidence, never pet deletion."""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import zlib

from tools.stoneage_quest_currency_source import (
    MANIFEST, PRIOR, RECO, ROOT, read_json, sha, source_command_blocks,
    verified_members, verified_item_names,
)

W21 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json'
W22 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json'
W23 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
O70 = 'STONEAGE-O70-FOUR-VILLAGE-COMMISSION-R1.json'
SELECTOR = re.compile(r'PET(>=|<=|!=|>|<|=)(\d+)-(\d+)(?:\*(\d+))?')


def selector_lexeme(value):
    """No species namespace, level unit, default quantity or EVDEL expansion."""
    if value == 'EVDEL':
        return {'raw': value, 'kind': 'UNEXPANDED_EVDEL_MARKER'}
    m = SELECTOR.fullmatch(value)
    if not m:
        return {'raw': value, 'kind': 'UNQUALIFIED_LITERAL'}
    return {'raw': value, 'kind': 'SOURCE_PET_SELECTOR_LEXEME',
            'comparison_literal': m[1], 'first_integer_literal': int(m[2]),
            'second_integer_literal': int(m[3]),
            'explicit_quantity_literal': None if m[4] is None else int(m[4])}


def condition_flags(value):
    flags = []
    if any(a == '' for a in re.split('[,&]', value)):
        flags.append('EMPTY_COMMA_OR_AMPERSAND_COMPONENT')
    if re.search(r'\d(?:LV|ITEM|PET|NOWEV|ENDEV)[=!<>]', value):
        flags.append('ADJACENT_SCALAR_AND_CONDITION_KEY')
    return flags


def derive(npc_zip):
    manifest = read_json(MANIFEST)
    raw, members = verified_members(npc_zip, manifest)
    old = read_json(PRIOR)
    old_blocks = {(b['script_path'], b['source_type_line']): b for b in old['source_event_blocks']}
    w21, w22, w23 = read_json(W21), read_json(W22), read_json(W23)
    reward_sources = {(s['path'], c['getpet_line']): c for s in w21['source_GetPet_scripts_and_event_blocks'] for c in s['commands']}
    reward_masters = {r['getpet_integer']: r for r in w21['original_enemy_instance_to_template_lookups']}
    currency_blocks = {(s['path'], b['type_line']) for s in w22['source_scripts'] for b in s['branches']}
    items23 = {(f[0], op[0]): op for f in w23['files'] for op in f[6]}
    rows, private, item_ids, reward_ids = [], [], set(), set()
    for path, data in sorted(members.items()):
        branches = source_command_blocks(data, {'DelPet'})
        if not branches:
            continue
        refs = [r for r in manifest['create_rows'] if [path, 'EXACT_SAME_NPC_SUBTREE_PATH', sha(data)] in r[15]]
        for b in branches:
            prior = old_blocks.get((path, b['type_line']))
            if prior and (prior['source_file_sha'] != sha(data) or prior['condition_expression_decoded_cp950_UTF8_sha256'] != sha(b['event_predicate_literal'].encode('ascii'))):
                raise ValueError('earlier quest source or condition differs')
            b['origin_class'] = 'ORIGIN_UNRESOLVED'
            b['previous_QUEST01_DelPet_field_count'] = 0 if prior is None else prior['source_operations'].get('DelPet', 0)
            b['same_block_currency_already_in_WORLD22'] = (path, b['type_line']) in currency_blocks
            b['DelPet_comma_lexemes'] = [dict(comma_position=i, **selector_lexeme(s)) for i, s in enumerate(b['command']['value'].split(','), 1)]
            b['condition_lexical_flags'] = condition_flags(b['event_predicate_literal'])
            b['explicit_item_field_positions'] = []
            b['reward_GetPet_source_joins'] = []
            for f in b['ordered_control_fields']:
                if f['key'] in {'GetItem', 'DelItem', 'GetRandItem'}:
                    op = items23.get((path, f['line']))
                    if op is None or (op[1], op[2], op[3]) != (f['key'], f['value'], f['source_line_sha256']):
                        raise ValueError('WORLD23 raw item field differs')
                    for i, token in enumerate(f['value'].split(','), 1):
                        m = re.fullmatch(r'(\d+)(?:\*(\d+))?', token)
                        if m:
                            item_ids.add(int(m[1]))
                            b['explicit_item_field_positions'].append([f['line'], f['key'], i, token, int(m[1]), None if m[2] is None else int(m[2])])
                elif f['key'] == 'GetPet':
                    previous = reward_sources.get((path, f['line']))
                    if previous is None or previous['getpet_line_sha256'] != f['source_line_sha256']:
                        raise ValueError('WORLD21 reward field differs')
                    ids = previous['raw_integer_tokens_in_order']
                    reward_ids.update(ids)
                    b['reward_GetPet_source_joins'].append({'line': f['line'], 'ordered_instance_integers': ids,
                                                           'WORLD21_master_row_evidence': [reward_masters[i] for i in ids]})
            # Preserve item predicates without repairing fused/empty source syntax.
            for atom in re.split('[,&]', b['event_predicate_literal']):
                m = re.fullmatch(r'ITEM(?:!=|>=|<=|=|>|<)(\d+)(?:\*\d+)?', atom)
                if m:
                    item_ids.add(int(m[1]))
        row = {'path': path, 'source_bytes': len(data), 'source_sha256': sha(data),
               'source_crc32': f'{zlib.crc32(data):08x}',
               'exact_create_refs': [{'create_path': r[0], 'ordinal': r[1], 'block_sha256': r[4],
                                      'floorid': r[5], 'graphic_literal': r[6], 'borncorner': r[7],
                                      'borncenter': r[8], 'template_token': r[11], 'template_candidates': r[13]} for r in refs],
               'branches': branches}
        rows.append(row)
        decoded = data.decode('cp950', 'strict')
        if decoded.encode('cp950') != data:
            raise ValueError('source CP950 roundtrip differs')
        private.append({'path': path, 'source': decoded, 'branches': branches})
    shards = sorted((RECO / 'item-module-01').glob('*.json'))
    index = {r[0]: r for p in shards for r in json.loads(p.read_text())['rows']}
    branches = [b for s in rows for b in s['branches']]
    inputs = [RECO / n for n in [MANIFEST, PRIOR, W21, W22, W23, O70]] + shards
    report = {'schema': 'stoneage.world27.original_pet_handover_quest_branches.r1',
              'source_scope': 'PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_EARLY_DEPLOYMENT',
              'private_source_zip': {'bytes': len(raw), 'sha256': sha(raw), 'members': len(members),
                                     'member_bytes': sum(map(len, members.values())), 'all_member_SHA_size_CRC_verified': True},
              'input_git_blobs': {str(p.relative_to(ROOT)): hashlib.sha1(b'blob ' + str(p.stat().st_size).encode() + b'\0' + p.read_bytes()).hexdigest() for p in inputs},
              'counts': {'source_files': len(rows), 'DelPet_physical_fields': len(branches),
                         'TYPE_literals': dict(Counter(b['type_literal'] for b in branches)),
                         'source_CREATE_refs': sum(len(s['exact_create_refs']) for s in rows),
                         'DelPet_comma_lexeme_classes': dict(Counter(x['kind'] for b in branches for x in b['DelPet_comma_lexemes'])),
                         'branches_with_lexical_condition_flags': sum(bool(b['condition_lexical_flags']) for b in branches),
                         'previous_QUEST01_blocks_with_DelPet': sum(b['previous_QUEST01_DelPet_field_count'] > 0 for b in branches),
                         'same_blocks_with_WORLD22_currency_evidence': sum(b['same_block_currency_already_in_WORLD22'] for b in branches),
                         'same_block_GetPet_fields': sum(len(b['reward_GetPet_source_joins']) for b in branches),
                         'distinct_reward_GetPet_instances': len(reward_ids), 'explicit_item_field_or_predicate_ID_candidates': len(item_ids),
                         'origin_classification': {'ORIGIN_UNRESOLVED': len(branches)}},
              'source_scripts': rows,
              'item01_source_joins': [{'item_id': i, 'item01_row': index.get(i)} for i in sorted(item_ids)],
              'old_content_reused': 'O70 commissions and QUEST01 command-presence records are prior work; new output consolidates exact handover literals, complete branch context and private source reading',
              'limits': {'parent_RAR_reread': False, 'original_pet_or_item_transaction_executed': False,
                         'selector_second_integer_namespace_proven_here': False, 'selector_first_integer_unit_proven_here': False,
                         'EVDEL_expanded_or_executed': False, 'source_condition_anomalies_repaired': False,
                         'permanent_or_operator_event_origin_proven': False, 'reward_master_files_reread_this_round': False,
                         'official_TW1_JSS1999_CN182_deployment_authenticated': False, 'overall_percent': None},
              'next': 'WORLD28: consolidate existing source-qualified quest content at a single module entry; no selector/EVDEL helper expansion'}
    return report, private


def private_html(report, private, names):
    cards = []
    for i, s in enumerate(private):
        content = []
        for b in s['branches']:
            f = b['command']
            fields = '\n'.join(f"L{x['line']} {x['key']}:{x['value']}" for x in b['ordered_control_fields'])
            flags = '；'.join(b['condition_lexical_flags']) or '未检出本工具限定的两类拼接异常'
            content.append('<section><h3>源 L' + str(f['line']) + ' · ' + html.escape(f['value']) + '</h3><p>归属待考；原条件字面标记：' + html.escape(flags) + '</p><pre>' + html.escape(fields) + '</pre></section>')
        cards.append('<article id="s' + str(i) + '"><h2>' + html.escape(s['path']) + '</h2>' + ''.join(content) + '<details><summary>原脚本全文（私人资料；含未筛选分支）</summary><pre>' + html.escape(s['source']) + '</pre></details></article>')
    nav = ' · '.join('<a href="#s' + str(i) + '">' + html.escape(s['path']) + '</a>' for i, s in enumerate(private))
    glossary = ''.join('<p>' + html.escape(str(i) + ' · ' + name) + '</p>' for i, name in sorted(names.items()))
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>WORLD27 原交宠任务分支</title><style>body{max-width:1120px;margin:32px auto;padding:0 20px;background:#f5f1e8;color:#25303a;font:16px/1.65 system-ui}article{background:white;padding:20px;margin:24px 0;border-radius:8px}section{border-top:1px solid #ddd}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 monospace}nav,p,h3{overflow-wrap:anywhere}h2{font-size:21px}h3{font-size:16px}</style><h1>WORLD27 · 原交宠任务分支</h1><p>保存社区混合2.5来源：17份原脚本、97条DelPet所属分支，不是97个已认证任务。使用浏览器查找（Ctrl+F），按路径跳转，展开原繁体全文。原条件、重复奖励、EVDEL和拼接异常完整保留；未执行条件、交宠、发奖或原游戏。PET两侧数字的单位与命名空间在此不作推定。全部归属待考，不混入已认证本体/永久任务或运营活动目录。</p><nav>' + nav + '</nav>' + ''.join(cards) + '<article><h2>关联道具原名（原候选表A）</h2>' + glossary + '</article></html>'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--npc-zip', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--private-html', type=Path)
    p.add_argument('--private-itemset-a', type=Path)
    a = p.parse_args()
    report, private = derive(a.npc_zip)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if a.private_html:
        names = verified_item_names(a.private_itemset_a, report) if a.private_itemset_a else {}
        a.private_html.write_text(private_html(report, private, names), encoding='utf-8')
    print(json.dumps(report['counts']))


if __name__ == '__main__':
    main()
