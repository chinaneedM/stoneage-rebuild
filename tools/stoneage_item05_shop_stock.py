"""Reconcile saved mixed25 ItemShop configurations with both original item tables."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import zipfile
import zlib

from tools.stoneage_preserved_item_shop_r44 import EXPECTED, PREFIX, inventory_tokens, need

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
STOCK = REC / 'STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'
R18 = REC / 'STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json'
REPORT = REC / 'STONEAGE-ITEM05-MIXED25-SHOP-STOCK-AND-ITEMSET-RECONCILIATION-R1.json'
ARCHIVE = (361255180, 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')
TABLES = ('itemset.txt', 'itemset0710.txt')
NPC = 'data/npc/'
KEYS = ('npcdir', 'itemset3file', 'itemset4file', 'itemset5file', 'itemset6file')
STRICT_ICONS = (5868386, 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')
BOUNDED_ICONS = (39918, '8bdfe6396217dfe380fd4259216ed2e4f2706e4fc1b4857fe26f356c34b241b5')
LINK = re.compile(rb'npcgen_shop[ \t]*\|[ \t]*file:([^\r\n]+)')
ITEM_LIST = re.compile(rb'^[ \t]*ItemList[ \t]*:[ \t]*(.*)$', re.I)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fingerprint(path, pin):
    with path.open('rb') as stream:
        need((path.stat().st_size, hashlib.file_digest(stream, 'sha256').hexdigest()) == pin,
             'whole-file source pin: ' + path.name)


def read_sources(path):
    import libarchive
    import rarfile

    fingerprint(path, ARCHIVE)
    members = rarfile.RarFile(path).infolist()
    need(len(members) == 7952, 'RAR directory extent')
    r18 = json.loads(R18.read_bytes())
    expected = {f'data/{r["path"]}': (r['size'], r['sha256'])
                for r in r18['all_server_occurrences']
                if r['path'].startswith('npc/') or r['path'] in TABLES}
    expected['setup.cf'] = EXPECTED['setup.cf']
    original = {m.filename.removeprefix(PREFIX): m for m in members
                if m.is_file() and m.filename.startswith(PREFIX)}
    need({p for p in original if p.startswith(NPC)} == {p for p in expected if p.startswith(NPC)},
         'whole original NPC subtree identity')
    contents = {}
    with libarchive.file_reader(str(path)) as archive:
        for entry in archive:
            full_name = entry.pathname.replace('\\', '/')
            if not full_name.startswith(PREFIX):
                continue
            name = full_name[len(PREFIX):]
            if name not in expected:
                continue
            raw = b''.join(entry.get_blocks())
            need(name not in contents and (len(raw), sha(raw)) == expected[name] and
                 zlib.crc32(raw) == original[name].CRC, 'source SHA/CRC or duplicate member: ' + name)
            contents[name] = raw
    need(contents.keys() == expected.keys(), 'incomplete source extraction')
    return contents


def setup_keys(raw):
    result = {}
    for line in raw.splitlines():
        key, found, value = line.split(b'#', 1)[0].partition(b'=')
        if not found or key.strip() not in {k.encode() for k in KEYS}:
            continue
        key = key.strip().decode('ascii')
        need(key not in result, 'duplicate setup selector')
        result[key] = value.strip().decode('ascii')
    need(result == {key: 'data/npc' if key == 'npcdir' else 'data/itemset.txt' for key in KEYS},
         'original config table or NPC directory changed')
    return result


def blocks(raw):
    """Read brace-delimited definitions without guessing nested script syntax."""
    start = None
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        line_type = line.strip()
        if line_type == b'{':
            need(start is None, 'nested original definition')
            start, block, fields = number, [], defaultdict(list)
        if start is None:
            continue
        block.append(line)
        if line_type == b'}':
            yield start, sha(b''.join(block)), fields
            start = None
            continue
        key, separator, value = line_type.partition(b'=')
        if separator and not key.startswith(b'#'):
            fields[key.strip().lower()].append(value.strip())
    need(start is None, 'unclosed original definition')


def source_links(sources):
    templates = []
    creations = []
    private_names = []
    for name, raw in sorted(sources.items()):
        if not name.startswith(NPC):
            continue
        path = name[len(NPC):]
        if path.endswith('.template') and b'npcgen_shop' in raw:
            for line, digest, fields in blocks(raw):
                if fields[b'templatename'] == [b'npcgen_shop']:
                    need(fields[b'functionset'] == [b'ItemShop'], 'source shop template function')
                    templates.append([path, line, digest, sha(raw)])
        if not path.endswith('.create'):
            continue
        for line, digest, fields in blocks(raw):
            for enemy in fields[b'enemy']:
                match = LINK.fullmatch(enemy)
                if match is None:
                    continue
                locations = {key.decode('ascii'): fields[key][0].decode('ascii')
                             for key in (b'borncenter', b'borncorner') if len(fields[key]) == 1}
                need(len(fields[b'floorid']) == 1 and locations and
                     all(len(fields[key]) <= 1 for key in (b'borncenter', b'borncorner')),
                     'source creation position field')
                prior_location_key = next(iter(locations))
                need(len(fields[b'name']) == 1, 'source creation name')
                private_names.append(fields[b'name'][0].decode('cp950'))
                argument = match[1].strip().decode('cp950').replace('\\', '/')
                need(NPC + argument in sources, 'source creation argument missing')
                creations.append({
                    'create_path': path, 'create_full_sha256': sha(raw),
                    'source_floorid_raw': int(fields[b'floorid'][0]),
                    'source_location_raw': locations[prior_location_key],
                    'source_location_fields': locations,
                    'argument_path': argument, 'argument_sha256': sha(sources[NPC + argument]),
                    'source_block_open_line': line, 'source_block_sha256': digest,
                })
    need(len(templates) == 1, 'source npcgen_shop template ambiguity')
    return templates[0], creations, private_names


def parse_argument(raw):
    matches = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        match = ITEM_LIST.fullmatch(line.rstrip(b'\r\n'))
        if match:
            matches.append((number, sha(line), match[1].strip()))
    need(len(matches) <= 1, 'duplicate source ItemList field')
    if not matches:
        return None
    number, digest, value = matches[0]
    tokens = inventory_tokens(value) if value else []
    ordered = [[lo, hi] if b'-' in raw_token else lo
               for raw_token, (lo, hi) in zip(value.split(b','), tokens)]
    return {'source_sha256': sha(raw), 'value_sha256': sha(value), 'line': number,
            'line_sha256': digest, 'tokens': ordered}


def parse_table(raw):
    rows = {}
    for line_no, line in enumerate(raw.splitlines(), 1):
        text = line.decode('cp950')
        fields = text.split(',')
        need(len(fields) == 94 and text.encode('cp950') == line, 'itemset CP950 or column count')
        item = int(fields[16])
        need(item not in rows, 'duplicate original item ID')
        rows[item] = {'line': line_no, 'sha256': sha(line), 'name': fields[0], 'alias': int(fields[17]),
                      'cost': fields[18], 'type': fields[19], 'level': fields[22],
                      'marked': fields[0].startswith('#')}
    return rows


def old_items():
    rows = {}
    for index in range(1, 8):
        source = REC / 'item-module-01' / f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{index:02d}-R1.json'
        for row in json.loads(source.read_bytes())['rows']:
            need(row[0] not in rows, 'duplicate archived item row')
            rows[row[0]] = row[1:]
    return rows


def occurrences(tokens):
    for index, token in enumerate(tokens):
        if type(token) is int:
            yield index, token, 'literal'
        else:
            for item in range(token[0], token[1] + 1):
                yield index, item, 'range'


def validate_projection(arguments, creations, prior):
    """Check ordered source evidence against prior independent per-file sets and references."""
    expected = {r['path']: r for r in prior['shop_argument_rows']}
    need(arguments.keys() == expected.keys(), 'ItemList discovery differs from ITEM01')
    for path, row in arguments.items():
        old = expected[path]
        tokens = row['tokens']
        legacy_expression = '|'.join(str(t) if type(t) is int else '-'.join(map(str, t)) for t in tokens)
        need(row['source_sha256'] == old['source_sha256'] and
             sha(legacy_expression.encode('ascii')) == old['raw_ItemList_expression_sha256'],
             'original argument or legacy canonical expression fingerprint')
        need(sum(type(t) is int for t in tokens) == old['explicit_numeric_item_ID_count'] and
             [t for t in tokens if isinstance(t, list)] == old['range_expressions_literal'] and
             sorted({item for _, item, _ in occurrences(tokens)}) ==
             old['expanded_candidate_IDs_not_proven_runtime'], 'original inventory expression scope')
    comparable = ('create_path', 'create_full_sha256', 'source_floorid_raw',
                  'source_location_raw', 'argument_path', 'argument_sha256')
    actual = Counter(tuple(r[k] for k in comparable) + (r['argument_path'] in arguments,) for r in creations)
    expected_links = Counter(tuple(r[k] for k in comparable) + (r['argument_has_itemlist'],)
                             for r in prior['npcgen_shop_creation_rows'])
    need(actual == expected_links, 'original creation blocks differ from ITEM01')


def stock_projection(arguments, creations, items, marked):
    bound = Counter(r['argument_path'] for r in creations)
    scoped = {k: Counter() for k in ('all', 'linked_files', 'unlinked_files', 'linked_creations')}
    distinct = {k: set() for k in scoped}
    exceptions = []
    repeated = []
    used = set()
    for path, row in sorted(arguments.items()):
        slots = list(occurrences(row['tokens']))
        ids = {item for _, item, _ in slots}
        duplicates = len(slots) - len(ids)
        if duplicates:
            repeated.append([path, duplicates])
        stats = Counter(files=1, explicit_tokens=sum(type(t) is int for t in row['tokens']),
                        range_tokens=sum(type(t) is list for t in row['tokens']),
                        expanded_occurrences=len(slots), duplicates_inside_file=duplicates)
        for token, item, kind in slots:
            record = items.get(item)
            status = ('missing_both' if record is None else 'only_alternate' if record[0] is None
                      else 'configured_row_marked' if item in marked[0]
                      else 'alternate_row_marked' if item in marked[1]
                      else 'both_tables')
            stats[status] += 1
            if status != 'both_tables':
                exceptions.append([path, token + 1, item, kind, status, bound[path]])
            used.add(item)
        key = 'linked_files' if bound[path] else 'unlinked_files'
        for scope, multiplier in (('all', 1), (key, 1), ('linked_creations', bound[path])):
            if multiplier:
                scoped[scope].update({k: v * multiplier for k, v in stats.items()})
                distinct[scope].update(ids)
    for key, counts in scoped.items():
        counts['distinct_ids'] = len(distinct[key])
    return {
        'counts': scoped,
        'exception_slots': exceptions,
        'repeated_ids_within_one_file': repeated,
        'shared_arguments_by_creation_count': [[path, count] for path, count in sorted(bound.items()) if count > 1],
        'creations_without_itemlist': [i for i, row in enumerate(creations) if row['argument_path'] not in arguments],
        'all_slot_ids_including_zero': sorted(used),
    }


def derive(sources):
    prior = json.loads(STOCK.read_bytes())
    arguments = {}
    for path, raw in sources.items():
        if path.startswith(NPC) and (row := parse_argument(raw)) is not None:
            arguments[path[len(NPC):]] = row
    arguments = dict(sorted(arguments.items()))
    template, creations, private_names = source_links(sources)
    validate_projection(arguments, creations, prior)
    tables = [parse_table(sources['data/' + t]) for t in TABLES]
    items = old_items()
    need(tables[0].keys() <= tables[1].keys() == items.keys(), 'item master ID sets changed')
    for number, row in items.items():
        a, b = (table.get(number) for table in tables)
        need((a['sha256'] if a else None, b['sha256'], a['alias'] if a else None, b['alias']) == tuple(row[:4]),
             'source table row bytes or image alias differs from ITEM01')
    marked = [sorted(item for item, row in table.items() if row['marked']) for table in tables]
    report = {
        'schema': 'stoneage.item05.mixed25_itemshop_stock_and_itemsets.r1',
        'source_archive_sha256': ARCHIVE[1],
        'npc_subtree_files_verified': sum(path.startswith(NPC) for path in sources),
        'npc_create_files_checked': sum(path.startswith(NPC) and path.endswith('.create') for path in sources),
        'source_setup_sha256': sha(sources['setup.cf']), 'setup_fields': setup_keys(sources['setup.cf']),
        'source_template': template, 'item_table_row_counts': [len(table) for table in tables],
        'item_table_hash_marked_ids': marked,
        'ordered_argument_tokens': arguments, 'creations': creations,
        'projection': stock_projection(arguments, creations, items, marked),
        'range_expansion_is_candidate': True,
        'native_server_executed': False,
        'actual_sale_price_computed': False,
        'official_same_deployment_authenticated': False,
        'original_art_or_item_names_published': False,
    }
    return report, tables, private_names


def icons_for(aliases, paths):
    images = {}
    for path, pin, pattern, state in (
        (paths[0], STRICT_ICONS, r'source-TW1-original-RD-candidates/alias-(\d+)\.png', 'strict'),
        (paths[1], BOUNDED_ICONS, r'alias-(\d+)-Palet1-verticalflip-candidate\.png', 'bounded'),
    ):
        fingerprint(path, pin)
        with zipfile.ZipFile(path) as archive:
            need(archive.testzip() is None, 'private source art ZIP CRC')
            for member in archive.namelist():
                if (match := re.fullmatch(pattern, member)) is not None and int(match[1]) in aliases:
                    key = int(match[1])
                    need(key not in images, 'conflicting source art alias')
                    images[key] = [state, base64.b64encode(archive.read(member)).decode('ascii')]
    return images


def private_page(report, tables, private_names, icon_paths):
    keys = report['projection']['all_slot_ids_including_zero']
    items = {i: [table.get(i) for table in tables] for i in keys}
    images = icons_for({v['alias'] for row in items.values() for v in row if v}, icon_paths)
    grouped = defaultdict(list)
    for entry, name in zip(report['creations'], private_names, strict=True):
        grouped[entry['argument_path']].append({**entry, 'name': name})
    arguments = {path: row['tokens'] for path, row in report['ordered_argument_tokens'].items()}
    model = {'shops': {p: [arguments.get(p), grouped[p]] for p in sorted(arguments.keys() | grouped.keys())},
             'items': items, 'images': images}
    marker = '/* PRIVATE_SOURCE_DATA */'
    template = (ROOT / 'tools/stoneage-item05-private-shop-observer.html').read_text(encoding='utf-8')
    need(template.count(marker) == 1, 'private observer data marker')
    data = json.dumps(model, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')
    return template.replace(marker, data), Counter(kind for kind, _ in images.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('strict_icons', type=Path)
    parser.add_argument('bounded_icons', type=Path)
    parser.add_argument('public_report', type=Path)
    parser.add_argument('private_html', type=Path)
    args = parser.parse_args()
    need(ROOT not in args.private_html.resolve().parents, 'private content must stay outside Git')
    report, tables, private_names = derive(read_sources(args.archive))
    html, counts = private_page(report, tables, private_names, (args.strict_icons, args.bounded_icons))
    payload = html.encode('utf-8')
    args.private_html.write_bytes(payload)
    report['private_observer'] = {'bytes': len(payload), 'sha256': sha(payload), 'prior_icon_counts': counts}
    args.public_report.write_text(json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
