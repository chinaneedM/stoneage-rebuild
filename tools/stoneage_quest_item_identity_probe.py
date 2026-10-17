"""Extract only bounded logging-item numeric metadata from hash-pinned late tables.

Names are query inputs, never a proof of early item identity. No source names,
descriptions, scripts or whole rows are retained in the derived report.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
try:
    from tools.stoneage_itemset_schema_probe import SCHEMA, INDEX, setup_itemsets
except ModuleNotFoundError:
    from stoneage_itemset_schema_probe import SCHEMA, INDEX, setup_itemsets

EXPECTED = {
    'itemset.txt': {'bytes': 3392473, 'sha256': 'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688', 'rows': 13252},
    'itemset0710.txt': {'bytes': 3668487, 'sha256': '6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb', 'rows': 13910},
}
CODECS = ('utf-8', 'gb18030', 'big5')
# Literal query alternatives stay distinct. Partial matches only select candidates.
QUERIES = {
    'BRACELET': ('杉之手环', '杉之手環', '衫之手环', '衫之手環', '杉的手环', '杉的手環'),
    'PERMIT': ('伐木许可证', '伐木許可證', '采伐许可证', '采伐許可證', '採伐許可證'),
    'BROKEN_AXE': ('折断的斧头', '折斷的斧頭', '断斧', '斷斧', '折断斧', '折斷斧'),
    'REPAIRED_AXE': ('哈恩改造斧', '哈恩的改造斧'),
    'ERRAND_AXE': ('哈恩的斧头', '哈恩的斧頭'),
}
NUMBER_FIELDS = ('id', 'imagenumber', 'cost', 'type', 'level', 'campile', 'attack_raw_a', 'attack_raw_b',
                 'defence_raw_a', 'defence_raw_b', 'quick_raw_a', 'quick_raw_b', 'charm_raw_a', 'charm_raw_b',
                 'magicid', 'dropatlogout', 'vanishatdrop', 'canpetmail', 'canmergefrom', 'canmergeto')
FLAGS = ('dropatlogout', 'vanishatdrop', 'canpetmail', 'canmergefrom', 'canmergeto')


def require(value, message):
    if not value:
        raise ValueError(message)


def extraction_contract_fingerprint(source):
    """Keep the actual-source-tested extractor frozen across metadata-only replay."""
    functions = {'require', 'name_matches', 'extract', 'report', 'main'}
    constants = {'EXPECTED', 'CODECS', 'QUERIES', 'NUMBER_FIELDS', 'FLAGS'}
    selected = []
    found = set()
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name in functions:
            selected.append(ast.dump(node, include_attributes=False))
            found.add(node.name)
        elif isinstance(node, ast.Assign):
            names = {x.id for x in node.targets if isinstance(x, ast.Name)}
            if names & constants:
                selected.append(ast.dump(node, include_attributes=False))
                found |= names & constants
    require(found == functions | constants, 'incomplete extraction contract')
    return hashlib.sha256('\n'.join(selected).encode()).hexdigest()


def name_matches(raw):
    result = []
    for codec in CODECS:
        try:
            name = raw.decode(codec, errors='strict')
        except UnicodeError:
            continue
        for role, tokens in QUERIES.items():
            for token in tokens:
                if token in name:
                    result.append({'codec': codec, 'role': role, 'query': token, 'exact_name_match': name == token})
    return result


def extract(body):
    rows, candidates, ids = 0, [], set()
    for physical_line, raw in enumerate(body.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(b'#'):
            continue
        fields = [x.strip() for x in line.replace(b'\t', b' ').split(b',')]
        require(len(fields) == len(SCHEMA) == 94, f'wrong 94-column row at {physical_line}')
        rows += 1
        try:
            item_id = int(fields[INDEX['id']])
        except ValueError as error:
            raise ValueError(f'invalid template id at {physical_line}') from error
        require(item_id not in ids, f'duplicate template id {item_id}')
        ids.add(item_id)
        matches = []
        for field in ('name', 'secretname'):
            matches.extend(dict(match, field=field) for match in name_matches(fields[INDEX[field]]))
        if not matches:
            continue
        values = {}
        for field in NUMBER_FIELDS:
            cell = fields[INDEX[field]]
            try:
                values[field] = int(cell) if cell else None
            except ValueError as error:
                raise ValueError(f'non-numeric selected field {field} at {physical_line}') from error
            if field in FLAGS:
                require(values[field] in (None, 0, 1), f'non-boolean selected flag {field}')
        candidates.append({'physical_line': physical_line, 'row_sha256': hashlib.sha256(raw).hexdigest(),
                           'name_bytes_sha256': hashlib.sha256(fields[0]).hexdigest(),
                           'secretname_bytes_sha256': hashlib.sha256(fields[1]).hexdigest(),
                           'matches': matches, 'numeric_fields': values})
        require(len(candidates) <= 100, 'candidate bound exceeded; requalify queries')
    return {'row_count': rows, 'candidates': candidates}


def report(data_dir, setup):
    require(setup.is_file(), 'missing actual setup')
    configured = setup_itemsets(setup)
    require(configured, 'missing configured itemset paths')
    selected_names = {Path(v.replace('\\', '/')).name.lower() for v in configured.values()}
    require(selected_names <= set(EXPECTED), 'setup selected an unpinned table')
    tables = {}
    for filename, expected in EXPECTED.items():
        body = (data_dir / filename).read_bytes()
        require(len(body) == expected['bytes'] and hashlib.sha256(body).hexdigest() == expected['sha256'], f'table hash/size changed: {filename}')
        table = extract(body)
        require(table['row_count'] == expected['rows'], f'table rows changed: {filename}')
        tables[filename] = dict(table, bytes=len(body), sha256=expected['sha256'], selected_by_actual_setup=filename in selected_names)
    roles = set(QUERIES)
    found = {m['role'] for t in tables.values() for row in t['candidates'] for m in row['matches']}
    selected_by_id = {r['numeric_fields']['id']: r for r in tables['itemset.txt']['candidates']}
    revision_by_id = {r['numeric_fields']['id']: r for r in tables['itemset0710.txt']['candidates']}
    comparisons = []
    for item_id in sorted(set(selected_by_id) & set(revision_by_id)):
        a, b = selected_by_id[item_id], revision_by_id[item_id]
        comparisons.append({'template_id': item_id, 'same_name_bytes': a['name_bytes_sha256'] == b['name_bytes_sha256'],
                            'same_secretname_bytes': a['secretname_bytes_sha256'] == b['secretname_bytes_sha256'],
                            'numeric_changes': {f: {'itemset.txt': a['numeric_fields'][f], 'itemset0710.txt': b['numeric_fields'][f]} for f in NUMBER_FIELDS if a['numeric_fields'][f] != b['numeric_fields'][f]}})
    return {'schema': 'stoneage.quest_item_identity.r1', 'source_role': 'LATER_RECOVERED25_MASTER_CANDIDATES',
            'setup': {'bytes': setup.stat().st_size, 'sha256': hashlib.sha256(setup.read_bytes()).hexdigest(), 'configured_itemsets': configured},
            'tables': tables, 'cross_table_candidate_comparisons': comparisons, 'unmatched_query_roles': sorted(roles - found),
            'name_match_is_quest_identity_proof': False, 'whole_file_encoding_authenticated': False,
            'raw_stat_pairs_are_final_equipped_stats': False, 'original_early_template_ids_recovered': False,
            'guide_charm_conflict_resolved_for_early_build': False, 'original_server_executed': False,
            'runtime_code_changed': False, 'stage_a_accepted': False, 'stage_b_gate': 'GATED'}


def validate_derived(data):
    """Replay metadata consistency without pretending to reacquire original bytes."""
    require(data['schema'] == 'stoneage.quest_item_identity.r1', 'wrong derived schema')
    require(data['source_role'] == 'LATER_RECOVERED25_MASTER_CANDIDATES', 'source role promotion')
    for flag in ('name_match_is_quest_identity_proof', 'whole_file_encoding_authenticated',
                 'raw_stat_pairs_are_final_equipped_stats', 'original_early_template_ids_recovered',
                 'guide_charm_conflict_resolved_for_early_build', 'original_server_executed', 'runtime_code_changed', 'stage_a_accepted'):
        require(data[flag] is False, f'evidence promotion: {flag}')
    require(data['stage_b_gate'] == 'GATED', 'stage promotion')
    require(set(data['tables']) == set(EXPECTED), 'table coverage')
    selected = {Path(v.replace('\\', '/')).name.lower() for v in data['setup']['configured_itemsets'].values()}
    require(selected and selected <= set(EXPECTED), 'unqualified setup')
    found = set()
    indexes = {}
    for filename, table in data['tables'].items():
        for key, value in EXPECTED[filename].items():
            require(table['row_count' if key == 'rows' else key] == value, f'table source drift {filename}')
        require(table['selected_by_actual_setup'] is (filename in selected), 'setup selection mismatch')
        require(len(table['candidates']) <= 100, 'candidate bound')
        by_id = {}
        for row in table['candidates']:
            values = row['numeric_fields']
            require(set(values) == set(NUMBER_FIELDS), 'unknown or missing numeric field')
            require(type(values['id']) is int and values['id'] not in by_id, 'duplicate/missing candidate identity')
            by_id[values['id']] = row
            require(type(row['physical_line']) is int and row['physical_line'] > 0, 'invalid row position')
            for key in ('row_sha256', 'name_bytes_sha256', 'secretname_bytes_sha256'):
                require(re.fullmatch('[a-f0-9]{64}', row[key]) is not None, 'invalid source digest')
            for field, value in values.items():
                require(value is None or type(value) is int, 'non-integer numeric metadata')
                if field in FLAGS:
                    require(value in (None, 0, 1), 'invalid lifetime flag')
            require(row['matches'], 'unmatched candidate row')
            for match in row['matches']:
                require(match['role'] in QUERIES and match['query'] in QUERIES[match['role']], 'invented query match')
                require(match['codec'] in CODECS and match['field'] in ('name', 'secretname'), 'invalid codec/name field')
                require(type(match['exact_name_match']) is bool, 'invalid exact-match status')
                found.add(match['role'])
        indexes[filename] = by_id
    require(data['unmatched_query_roles'] == sorted(set(QUERIES) - found), 'unmatched-role drift')
    comparisons = []
    left, right = indexes['itemset.txt'], indexes['itemset0710.txt']
    for item_id in sorted(set(left) & set(right)):
        a, b = left[item_id], right[item_id]
        comparisons.append({'template_id': item_id, 'same_name_bytes': a['name_bytes_sha256'] == b['name_bytes_sha256'],
                            'same_secretname_bytes': a['secretname_bytes_sha256'] == b['secretname_bytes_sha256'],
                            'numeric_changes': {f: {'itemset.txt': a['numeric_fields'][f], 'itemset0710.txt': b['numeric_fields'][f]} for f in NUMBER_FIELDS if a['numeric_fields'][f] != b['numeric_fields'][f]}})
    require(data['cross_table_candidate_comparisons'] == comparisons, 'cross-table comparison drift')
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir', type=Path, required=True)
    p.add_argument('--setup', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = report(a.data_dir, a.setup)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'tables': len(result['tables']), 'candidates': {k: len(v['candidates']) for k, v in result['tables'].items()}, 'unmatched_roles': result['unmatched_query_roles'], 'original_server_executed': False}))


if __name__ == '__main__':
    main()
