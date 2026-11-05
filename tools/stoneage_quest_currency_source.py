#!/usr/bin/env python3
"""Extract source-bound currency branches; never evaluate a game condition.

The private CHAR01 ZIP must match every previously published original member.
Only numeric/ASCII control fields and hashes are published. Optional HTML keeps
original commercial dialogue private. No client/server is executed.
"""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
RECO = ROOT / 'research/recovered'
MANIFEST = 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
PRIOR = 'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
ZIP_SHA = 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
CURRENCY = {'GetStone', 'DelStone'}
CONTROL = {'EventNo', 'TYPE', 'EVENT', 'GetStone', 'DelStone', 'DelItem',
           'GetItem', 'GetRandItem', 'GetPet', 'DelPet', 'EndSetFlg', 'CleanFlg', 'NotDel'}
FIELD = re.compile(rb'^\s*([A-Za-z][A-Za-z0-9_]*):([^|]*)(?:\|\s*)?$')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((RECO / name).read_text(encoding='utf-8'))


def parse_fields(data):
    # Physical lines and hashes exclude CR/LF only; do not normalize source text.
    out = []
    for n, raw in enumerate(data.splitlines(), 1):
        m = FIELD.fullmatch(raw)
        if m:
            key = m[1].decode('ascii')
            if key in CONTROL:
                out.append({'line': n, 'key': key, 'value': m[2].decode('ascii'),
                            'source_line_sha256': sha(raw)})
    return out


def source_command_blocks(data, command_keys):
    """Locate selected source fields within original TYPE/EventNo/EventEnd spans."""
    fields = parse_fields(data)
    types = [f for f in fields if f['key'] == 'TYPE']
    result = []
    for f in fields:
        if f['key'] not in command_keys:
            continue
        previous = [t for t in types if t['line'] < f['line']]
        if not previous:
            raise ValueError('source directive has no preceding TYPE')
        t = previous[-1]
        following = next((x['line'] for x in types if x['line'] > t['line']), len(data.splitlines()) + 1)
        # EventNo belongs to the next TYPE, rather than the previous event.
        next_event = next((x['line'] for x in fields if x['key'] == 'EventNo'
                           and t['line'] < x['line'] < following), following)
        start = max((x['line'] for x in fields if x['key'] == 'EventNo' and x['line'] < t['line']), default=t['line'])
        end_marker = next((n for n, line in enumerate(data.splitlines(), 1)
                           if t['line'] < n < next_event and line.strip() == b'EventEnd'), None)
        end = end_marker if end_marker is not None else next_event - 1
        if f['line'] > end:
            raise ValueError('source directive outside TYPE event scope')
        section = [x for x in fields if start <= x['line'] <= end]
        conditions = [x['value'] for x in section if x['key'] == 'EVENT']
        if len(conditions) != 1:
            raise ValueError('expected exactly one source EVENT predicate')
        result.append({'command': f, 'type_line': t['line'], 'type_literal': t['value'],
                       'event_predicate_literal': conditions[0], 'scope_first_line': start,
                       'scope_last_line': end, 'source_EventEnd_found': end_marker is not None,
                       'ordered_control_fields': section})
    return result


def currency_blocks(data):
    result = []
    for b in source_command_blocks(data, CURRENCY):
        f = b['command']
        literal = f['value']
        if re.fullmatch(r'[+-]?\d+', literal):
            amount = {'kind': 'INTEGER_LITERAL', 'integer': int(literal)}
        elif re.fullmatch(r'LV\*\d+', literal):
            amount = {'kind': 'UNEXECUTED_LEVEL_EXPRESSION', 'level_multiplier_literal': int(literal[3:])}
        else:
            amount = {'kind': 'UNRESOLVED_LITERAL'}
        result.append({'currency_line': f['line'], 'directive': f['key'], 'literal': literal,
                       'source_line_sha256': f['source_line_sha256'], 'amount': amount,
                       **{k: v for k, v in b.items() if k != 'command'}})
    return result


def verified_members(zip_path, manifest):
    raw = Path(zip_path).read_bytes()
    if sha(raw) != ZIP_SHA:
        raise ValueError('private source ZIP SHA differs')
    expected = {x[0]: x for x in manifest['source_files']}
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or set(names) != {'npc/' + p for p in expected}:
            raise ValueError('source ZIP member set differs')
        result = {}
        for path, row in expected.items():
            data = z.read('npc/' + path)  # ZIP CRC checked by zipfile.
            if [len(data), sha(data), f'{zlib.crc32(data):08x}'] != row[1:4]:
                raise ValueError('original member SHA/size/CRC differs: ' + path)
            result[path] = data
    return raw, result


def derive(zip_path):
    manifest = read_json(MANIFEST)
    raw, members = verified_members(zip_path, manifest)
    prior = read_json(PRIOR)
    old_blocks = {(x['script_path'], x['source_type_line']): x for x in prior['source_event_blocks']}
    rows, private = [], []
    for path, data in sorted(members.items()):
        blocks = currency_blocks(data)
        if not blocks:
            continue
        refs = []
        for row in manifest['create_rows']:
            if any(x[0] == path and x[1] == 'EXACT_SAME_NPC_SUBTREE_PATH' and x[2] == sha(data) for x in row[15]):
                refs.append({'create_path': row[0], 'block_ordinal': row[1], 'block_sha256': row[4],
                             'floorid': row[5], 'graphic_literal': row[6],
                             'borncorner': row[7], 'borncenter': row[8], 'template_token': row[11],
                             'template_candidates': row[13]})
        for b in blocks:
            old = old_blocks.get((path, b['type_line']))
            b['previous_QUEST01_currency_field_count'] = 0 if old is None else old['source_operations'].get(b['directive'], 0)
            b['previous_QUEST01_block_present'] = old is not None
            b['origin_class'] = 'UNRESOLVED'
        rows.append({'path': path, 'source_bytes': len(data), 'source_sha256': sha(data),
                     'source_crc32': f'{zlib.crc32(data):08x}', 'exact_create_refs': refs, 'branches': blocks})
        private.append({'path': path, 'source': data.decode('cp950', 'replace'), 'branches': blocks})
    branches = [b for r in rows for b in r['branches']]
    ids = set()
    for b in branches:
        for f in b['ordered_control_fields']:
            if f['key'] in {'GetItem', 'DelItem', 'GetRandItem'}:
                for token in f['value'].split(','):
                    m = re.fullmatch(r'(\d+)(?:\*\d+)?', token.strip())
                    if m:
                        ids.add(int(m[1]))
            elif f['key'] == 'EVENT':
                ids.update(int(x) for x in re.findall(r'(?<![A-Za-z])ITEM(?:!=|>=|<=|=|>|<)(\d+)', f['value']))
    item_rows = {r[0]: r for p in sorted((RECO / 'item-module-01').glob('*.json')) for r in json.loads(p.read_text())['rows']}
    joins = [{'item_id': i, 'item01_row': item_rows.get(i)} for i in sorted(ids)]
    counts = {'source_files': len(rows), 'currency_directives': len(branches),
              'directive_counts': dict(sorted(Counter(b['directive'] for b in branches).items())),
              'type_counts': dict(sorted(Counter(b['type_literal'] for b in branches).items())),
              'amount_kind_counts': dict(sorted(Counter(b['amount']['kind'] for b in branches).items())),
              'exact_create_refs': sum(len(r['exact_create_refs']) for r in rows),
              'item_ids_from_explicit_item_fields': len(joins), 'missing_item01_ids': [x['item_id'] for x in joins if x['item01_row'] is None],
              'item_ids_absent_from_itemset_A': [x['item_id'] for x in joins if x['item01_row'] is not None and x['item01_row'][1] is None],
              'currency_fields_already_recorded_by_QUEST01': sum(b['previous_QUEST01_currency_field_count'] > 0 for b in branches)}
    report = {'schema': 'stoneage.world22.original_quest_currency_source.r1',
              'source_scope': 'PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
              'private_source_zip': {'bytes': len(raw), 'sha256': sha(raw), 'members': len(members),
                                     'member_bytes': sum(map(len, members.values())), 'all_member_SHA_size_CRC_verified': True},
              'prior_original_RAR_sha256': manifest['original_rar_sha256'],
              'original_parent_RAR_reread_this_work_unit': False,
              'published_input_git_blobs': {
                  str(p.relative_to(ROOT)): hashlib.sha1(b'blob ' + str(len(p.read_bytes())).encode() + b'\0' + p.read_bytes()).hexdigest()
                  for p in [RECO / MANIFEST, RECO / PRIOR, *sorted((RECO / 'item-module-01').glob('*.json'))]},
              'counts': counts, 'source_scripts': rows, 'item01_source_joins': joins,
              'limits': {'original_conditions_executed': False, 'currency_transferred': False,
                         'formula_evaluation_verified': False, 'same_official_deployment_verified': False,
                         'permanent_vs_event_quest_verified': False, 'original_game_entered': False,
                         'overall_restoration_percent': None},
              'next': 'WORLD23: source-backed item/quest content gap; no currency evaluator or MMO infrastructure'}
    return report, private


def private_html(report, private, item_names=None):
    # Static document uses browser-native find and details. No custom viewer engine.
    blocks = []
    for script in private:
        blocks.append('<article><h2>' + html.escape(script['path']) + '</h2>')
        for b in script['branches']:
            blocks.append('<p><b>' + html.escape(f"L{b['currency_line']} {b['directive']}:{b['literal']}") +
                          '</b><br>' + html.escape(b['type_literal'] + ' | ' + b['event_predicate_literal']) + '</p>')
        blocks.append('<details><summary>原脚本全文（私人资料）</summary><pre>' + html.escape(script['source']) + '</pre></details></article>')
    glossary = '' if not item_names else '<article><h2>关联道具原名（itemset.txt）</h2>' + ''.join(
        '<p>' + html.escape(str(i) + ' · ' + name) + '</p>' for i, name in sorted(item_names.items())) + '</article>'
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>WORLD22 原任务石币分支</title><style>body{max-width:1000px;margin:36px auto;padding:0 24px;background:#f5f1e8;color:#252b30;font:16px/1.65 system-ui}article{background:white;padding:18px 24px;margin:20px 0;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 monospace}h1{font-size:28px}h2{font-size:19px}p{overflow-wrap:anywhere}</style><h1>WORLD22 · 原任务石币分支</h1><p>保存社区混合2.5原件。26份原脚本，99条 GetStone、16条 DelStone。使用浏览器查找（Ctrl+F）检索金额、道具和条件；展开原文核对行。金额和等级表达式保留原值，未执行条件或实际奖励扣费，未认证早期官方同服。原文保持来源繁体候选，不能解码者显示替换字。</p>' + ''.join(blocks) + glossary + '</html>'


def verified_item_names(path, report):
    data = path.read_bytes()
    if sha(data) != 'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688':
        raise ValueError('original itemset A SHA differs')
    wanted = {x['item_id']: x['item01_row'] for x in report['item01_source_joins']}
    names = {}
    for raw in data.splitlines():
        if not raw.strip() or raw.lstrip().startswith(b'#'):
            continue
        fields = raw.split(b',')
        if len(fields) != 94:
            raise ValueError('original itemset A field count differs')
        iid = int(fields[16])
        if iid in wanted:
            if sha(raw) != wanted[iid][1]:
                raise ValueError('original itemset A row SHA differs')
            names[iid] = fields[0].decode('cp950')
    expected = {i for i, row in wanted.items() if row is not None and row[1] is not None}
    if set(names) != expected:
        raise ValueError('original itemset A missing required ID')
    for iid in set(wanted) - expected:
        names[iid] = '本份 itemset.txt 无记录；另一候选表有记录，原名本轮未重读'
    return names


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--npc-zip', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--private-html', type=Path)
    p.add_argument('--private-itemset-a', type=Path, help='Optional original item names for private HTML only')
    a = p.parse_args()
    report, private = derive(a.npc_zip)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if a.private_html:
        names = verified_item_names(a.private_itemset_a, report) if a.private_itemset_a else None
        a.private_html.write_text(private_html(report, private, names), encoding='utf-8')
    print(json.dumps(report['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
