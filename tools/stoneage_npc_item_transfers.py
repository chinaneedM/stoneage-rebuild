#!/usr/bin/env python3
"""Index literal NPC item fields by original source family, without execution."""
import argparse
from collections import Counter, defaultdict
import hashlib
import html
import json
from pathlib import Path
import re
import zlib

from tools.stoneage_quest_currency_source import (
    MANIFEST, PRIOR, RECO, ROOT, parse_fields, read_json, sha, verified_members,
)

ITEM_KEYS = {'GetItem', 'DelItem', 'GetRandItem'}
FILE_COLUMNS = ['path', 'bytes', 'sha256', 'crc32', 'exact_create_refs', 'contexts', 'operations']
OP_COLUMNS = ['physical_line', 'field', 'raw_value', 'source_line_sha256', 'context_index_or_null', 'comma_slots']
SLOT_COLUMNS = ['one_based_position', 'raw_value', 'ampersand_components']
COMPONENT_COLUMNS = ['one_based_position', 'raw_value', 'syntax_class', 'item_integer_or_null', 'explicit_quantity_or_null']
REF_COLUMNS = ['create_path', 'block_ordinal', 'block_sha256', 'floorid', 'graphic_literal', 'borncorner', 'borncenter', 'template_candidates', 'function_candidates']


def item_slots(literal):
    """Preserve punctuation and duplicates; a bare ID has no inferred quantity."""
    slots = []
    for i, slot in enumerate(literal.split(','), 1):
        components = []
        for j, raw in enumerate(slot.split('&'), 1):
            token = raw.strip()
            m = re.fullmatch(r'(\d+)(?:\*(\d+))?', token)
            if m:
                kind = 'EXPLICIT_QUANTITY' if m[2] is not None else 'BARE_ITEM_INTEGER'
                iid, qty = int(m[1]), int(m[2]) if m[2] is not None else None
            elif re.fullmatch(r'\d+\*', token):
                kind, iid, qty = 'INCOMPLETE_QUANTITY', int(token[:-1]), None
            else:
                kind = 'EMPTY_COMPONENT' if token == '' else 'SYMBOLIC_OR_UNRESOLVED'
                iid, qty = None, None
            components.append([j, raw, kind, iid, qty])
        slots.append([i, slot, components])
    return slots


def event_contexts(data, fields):
    lines = data.splitlines()
    types = [f for f in fields if f['key'] == 'TYPE']
    contexts = []
    for pos, t in enumerate(types):
        prior_type = types[pos - 1]['line'] if pos else 0
        next_type = types[pos + 1]['line'] if pos + 1 < len(types) else len(lines) + 1
        start = max((f['line'] for f in fields if f['key'] == 'EventNo' and prior_type < f['line'] < t['line']), default=t['line'])
        next_event = next((f['line'] for f in fields if f['key'] == 'EventNo' and t['line'] < f['line'] < next_type), next_type)
        end = next((i for i in range(t['line'] + 1, next_event) if lines[i - 1].strip() == b'EventEnd'), None)
        last = end if end is not None else next_event - 1
        retained = [[f['line'], f['key'], f['value'], f['source_line_sha256']]
                    for f in fields if start <= f['line'] <= last and f['key'] not in ITEM_KEYS]
        contexts.append({'type_line': t['line'], 'type': t['value'], 'first_line': start,
                         'last_line': last, 'EventEnd_line': end, 'ordered_other_control_fields': retained})
    return contexts


def script_operations(data):
    fields = parse_fields(data)
    contexts = event_contexts(data, fields)
    operations = []
    for f in fields:
        if f['key'] not in ITEM_KEYS:
            continue
        matches = [i for i, c in enumerate(contexts) if c['first_line'] <= f['line'] <= c['last_line']]
        if len(matches) > 1:
            raise ValueError('overlapping source TYPE scopes')
        operations.append([f['line'], f['key'], f['value'], f['source_line_sha256'],
                           matches[0] if matches else None, item_slots(f['value'])])
    used = sorted({op[4] for op in operations if op[4] is not None})
    remap = {old: new for new, old in enumerate(used)}
    for op in operations:
        op[4] = remap[op[4]] if op[4] is not None else None
    return [contexts[i] for i in used], operations


def derive(zip_path):
    manifest = read_json(MANIFEST)
    raw_zip, members = verified_members(zip_path, manifest)
    functions = {(r[0], r[1]): r[4] for r in manifest['template_rows']}
    refs = defaultdict(list)
    for row in manifest['create_rows']:
        for path, kind, digest in row[15]:
            if kind != 'EXACT_SAME_NPC_SUBTREE_PATH':
                continue
            candidates = sorted({functions.get(tuple(k), 'UNRESOLVED') for k in row[13]})
            refs[path].append([row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[13], candidates])
    old = read_json(PRIOR)
    old_blocks = {(b['script_path'], b['source_type_line']): b for b in old['source_event_blocks']}
    files = []
    totals, syntax, families = Counter(), Counter(), Counter()
    ids, malformed_ids = set(), set()
    old_counts, outside = Counter(), Counter()
    backup_files = []
    for path, data in sorted(members.items()):
        contexts, ops = script_operations(data)
        if not ops:
            continue
        digest = sha(data)
        # Exact links were previously SHA-qualified; retain every placement.
        for row in manifest['create_rows']:
            if any(r[0] == path and r[1] == 'EXACT_SAME_NPC_SUBTREE_PATH' for r in row[15]):
                if not any(r == [path, 'EXACT_SAME_NPC_SUBTREE_PATH', digest] for r in row[15]):
                    raise ValueError('CREATE source digest differs')
        fr = refs.get(path, [])
        names = sorted({f for ref in fr for f in ref[8]})
        family = ','.join(names) if names else 'NO_EXACT_CREATE_REFERENCE'
        if Path(path).suffix.lower() in {'.old', '.bak'}:
            backup_files.append(path)
        for op in ops:
            totals[op[1]] += 1
            families[op[1] + ' / ' + family] += 1
            if op[4] is None:
                outside[op[1]] += 1
            else:
                c = contexts[op[4]]
                b = old_blocks.get((path, c['type_line']))
                if b and b['source_operations'].get(op[1]):
                    old_counts[op[1]] += 1
            for slot in op[5]:
                for comp in slot[2]:
                    syntax[op[1] + ' / ' + comp[2]] += 1
                    if comp[3] is not None:
                        ids.add(comp[3])
                        if comp[2] == 'INCOMPLETE_QUANTITY':
                            malformed_ids.add(comp[3])
        files.append([path, len(data), digest, f'{zlib.crc32(data):08x}', fr, contexts, ops])
    index_paths = sorted((RECO / 'item-module-01').glob('*.json'))
    items = {row[0]: row for p in index_paths for row in json.loads(p.read_text())['rows']}
    world09_name = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-GETRANDITEM-SOURCE-SLOTS-R1.json'
    world09 = read_json(world09_name)
    by_type = {(f[0], f[5][o[4]]['type_line']): (f, o)
               for f in files for o in f[6] if o[1] == 'GetRandItem' and o[4] is not None}
    corrections = []
    for prev in world09['original_getranditem_blocks']:
        f, op = by_type[prev['script_path'], prev['type_line']]
        nums = [c[3] for s in op[5] for c in s[2] if c[3] is not None]
        old_nums = prev['original_item_candidates_ordered']
        if f[2] != prev['source_file_sha256'] or set(nums) != set(old_nums):
            raise ValueError('WORLD09 same-source ID set mismatch')
        corrections.append([f[0], op[0], prev['type_line'], len(old_nums), len(op[5]), len(nums),
                            len(nums) - len(set(nums)), list(dict.fromkeys(nums)) != old_nums,
                            nums == old_nums, op[3]])
    correction_summary = {
        'status': 'ADDITIVE_CORRECTION_OLD_INDEX_IS_NOT_LITERAL_POSITION_OR_ORDER_EVIDENCE',
        'same_SHA_qualified_source_fields': len(corrections),
        'old_per_block_unique_ID_references': sum(r[3] for r in corrections),
        'actual_source_comma_positions': sum(r[4] for r in corrections),
        'actual_source_integer_positions': sum(r[5] for r in corrections),
        'actual_source_empty_positions': sum(r[4] - r[5] for r in corrections),
        'extra_duplicate_integer_positions': sum(r[6] for r in corrections),
        'fields_containing_duplicate_integers': sum(r[6] > 0 for r in corrections),
        'fields_where_first_occurrence_order_differs_from_old_projection': sum(r[7] for r in corrections),
        'fields_where_numeric_list_matches_old_projection_exactly': sum(r[8] for r in corrections),
        'row_columns': ['path','original_field_line','type_line','old_unique_ID_count','raw_comma_slot_count',
                        'raw_integer_count','extra_duplicate_positions','unique_order_changed','list_identical','raw_line_SHA256'],
        'source_comparison_rows': corrections, 'actual_random_probability_proven': False,
        'old_WORLD09_JSON_and_QUEST01_JSON_rewritten': False}
    inputs = [RECO / MANIFEST, RECO / PRIOR, RECO / world09_name, *index_paths]
    report = {'schema': 'stoneage.world23.npc_item_transfer_literal_index.r1',
              'counting_unit': 'PHYSICAL_LINE_FIELDS_NOT_DISTINCT_QUESTS_OR_EXECUTED_REWARDS',
              'source_scope': 'PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_EARLY_OFFICIAL_DEPLOYMENT',
              'private_source_zip': {'bytes': len(raw_zip), 'sha256': sha(raw_zip), 'members': len(members),
                                     'member_bytes': sum(map(len, members.values())), 'all_members_SHA_size_CRC_verified': True},
              'parent_RAR_reread_this_work_unit': False, 'parent_RAR_sha256': manifest['original_rar_sha256'],
              'input_git_blobs': {str(p.relative_to(ROOT)): hashlib.sha1(b'blob ' + str(p.stat().st_size).encode() + b'\0' + p.read_bytes()).hexdigest() for p in inputs},
              'columns': {'files': FILE_COLUMNS, 'operations': OP_COLUMNS, 'comma_slots': SLOT_COLUMNS,
                          'components': COMPONENT_COLUMNS, 'exact_create_refs': REF_COLUMNS,
                          'other_control_fields': ['physical_line', 'field', 'raw_value', 'source_line_sha256']},
              'counts': {'source_files': len(files), 'operations': sum(totals.values()), 'operations_by_field': dict(sorted(totals.items())),
                         'component_syntax_by_field': dict(sorted(syntax.items())), 'operations_by_source_function_candidates': dict(sorted(families.items())),
                         'operations_already_in_QUEST01': dict(sorted(old_counts.items())),
                         'operations_without_TYPE_scope': dict(sorted(outside.items())),
                         'item_integers_including_incomplete_quantity': len(ids), 'incomplete_quantity_item_integers': sorted(malformed_ids),
                         'missing_from_both_ITEM01_candidate_tables': sorted(ids - items.keys()),
                         'present_only_in_candidate_table_B': sorted(i for i in ids & items.keys() if items[i][1] is None)},
              'named_backup_files_preserved': backup_files, 'files': files,
              'WORLD09_additive_correction': correction_summary,
              'item01_joins': [[i, items.get(i)] for i in sorted(ids)],
              'limits': {'source_punctuation_is_runtime_semantics': False, 'bare_item_quantity_inferred': False,
                         'all_GetItem_fields_are_quest_rewards': False, 'conditions_or_transfers_executed': False,
                         'original_official_deployment_verified': False, 'all_quests_permanent_or_event_classified': False,
                         'original_game_entered': False, 'Stage_B_started': False, 'overall_completion_percent': None},
              'next': 'WORLD24: source-ready original content gap after item-flow batch; no universal evaluator or new game'}
    return report, members


def private_html(report, members, names):
    chunks = []
    lookup = {i: row for i, row in report['item01_joins']}
    def name_for(i):
        if i in names:
            return names[i]
        if lookup.get(i) is None:
            return '两份候选物品表均无此ID'
        if lookup[i][1] is None:
            return '仅B候选表有记录；本轮未重读原名'
        return '本轮未重读原名'
    for f in report['files']:
        path, _, _, _, refs, contexts, ops = f
        funcs = sorted({x for ref in refs for x in ref[8]})
        chunks.append('<article><h2>' + html.escape(path) + '</h2><p>原模板用途：' + html.escape(', '.join(funcs) or '无确切CREATE引用') + '</p>')
        for op in ops:
            context = contexts[op[4]] if op[4] is not None else None
            conditions = [r[2] for r in context['ordered_other_control_fields'] if r[1] == 'EVENT'] if context else []
            info = (context['type'] + ' | ' + ' / '.join(conditions)) if context else '无TYPE事件范围；保留为原参数字段'
            n = sorted({c[3] for s in op[5] for c in s[2] if c[3] is not None})
            labels = '；'.join(str(i) + ' ' + name_for(i) for i in n)
            chunks.append('<p class="operation"><b>' + html.escape(f'L{op[0]} {op[1]}:{op[2]}') + '</b><br>' + html.escape(info) + '<br>' + html.escape(labels) + '</p>')
        chunks.append('<details><summary>原脚本全文（私人资料）</summary><pre>' + html.escape(members[path].decode('cp950', 'replace')) + '</pre></details></article>')
    correction = '<p><b>WORLD09加法订正：</b>旧目录将50条列表的718个去重后ID引用当成原位置；相同SHA原件实际有959个数字位置及1个空位置，其中26条含重复。旧记录保留，真实选择概率和空项处理尚未执行验证。</p>'
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>WORLD23 原NPC物品取得与消耗</title><style>body{max-width:1100px;margin:32px auto;padding:0 24px;background:#f5f1e8;color:#202a32;font:16px/1.65 system-ui}article{background:white;margin:20px 0;padding:18px 24px;border-radius:8px}h1{font-size:28px}h2{font-size:19px}pre{white-space:pre-wrap;font:14px/1.6 monospace}p,pre{overflow-wrap:anywhere}.operation{border-top:1px solid #ddd;padding-top:12px}</style><h1>WORLD23 · 原NPC物品取得与消耗</h1><p>保存社区混合2.5来源。按原模板用途查看字段，不能将所有GetItem都当任务奖励。使用Ctrl+F查找道具ID、原名或文件；展开原文核对。逗号、&amp;、乘数、重复位置和空项保留；没有乘数不猜数量，缺失乘数不补1。未运行原游戏、条件或交易，未认证早期官方同服。</p>' + correction + ''.join(chunks) + '</html>'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--npc-zip', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--private-html', type=Path)
    p.add_argument('--private-itemset-a', type=Path)
    a = p.parse_args()
    report, members = derive(a.npc_zip)
    # Compact rows keep this complete batch readable without thousands of empty lines.
    a.output.write_text(json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    if a.private_html:
        names = {}
        if a.private_itemset_a:
            data = a.private_itemset_a.read_bytes()
            if sha(data) != 'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688':
                raise ValueError('itemset A complete source SHA differs')
            wanted = {i: row for i, row in report['item01_joins'] if row is not None and row[1] is not None}
            for raw in data.splitlines():
                if not raw.strip() or raw.lstrip().startswith(b'#'):
                    continue
                fields = raw.split(b',')
                if len(fields) != 94:
                    raise ValueError('itemset A field count differs')
                iid = int(fields[16])
                if iid in wanted:
                    if sha(raw) != wanted[iid][1]:
                        raise ValueError('itemset A original row SHA differs')
                    names[iid] = fields[0].decode('cp950')
            if names.keys() != wanted.keys():
                raise ValueError('itemset A required original name missing')
        a.private_html.write_text(private_html(report, members, names), encoding='utf-8')
    print(json.dumps(report['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
