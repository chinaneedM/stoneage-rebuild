"""Read qualified private mining scripts; publish numeric evidence, never dialogue.

This is a static source extractor, not a game interpreter. In particular a bare
DelItem ID remains quantity=None, and EVENT punctuation has no runtime meaning
assigned here. The private ZIP is supplied explicitly and never downloaded.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
ITEMS = ROOT / 'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
MAPS = ROOT / 'research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json'
REPORT = ROOT / 'research/recovered/STONEAGE-QUEST08-MINING-APPRAISAL-AND-LIMITSHOP-SOURCE-R1.json'
PARAMETERS = [f'sainasu/event/nevent03_{n}' for n in range(1, 7)] + [
    'genout/lbis_10605_41_24', 'genout/lbis_1212_17_13', 'genout/lbis_1212_17_17']
ZIP_SHA = 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def numeric_item(value):
    """Keep omitted quantity different from explicit *1; reject unknown syntax."""
    match = re.fullmatch(r'(\d+)(?:\*(\d+))?', value)
    if not match:
        raise ValueError('Unsupported item operand')
    return {'item_id': int(match[1]), 'explicit_quantity': int(match[2]) if match[2] else None}


def events(raw):
    """Keep physical byte/line identities and ASCII controls, not commercial text."""
    rows, current, offset = [], None, 0
    for line_no, line in enumerate(raw.splitlines(keepends=True), 1):
        stripped = line.strip()
        if stripped.lower().startswith(b'eventno:'):
            if current is not None:
                raise ValueError('Unclosed event')
            current = {'ordinal': len(rows), 'start_byte': offset, 'start_line': line_no,
                       'event_number': int(stripped.split(b':', 1)[1]), 'commands': []}
        if current is not None:
            for key in (b'TYPE', b'EVENT', b'DelItem', b'GetItem'):
                if stripped.lower().startswith(key.lower() + b':'):
                    value = stripped.split(b':', 1)[1].decode('ascii')
                    if key in (b'TYPE', b'EVENT'):
                        current[key.decode().lower()] = value
                    else:
                        current['commands'].append({'name': key.decode(), 'line': line_no,
                                                    'line_sha256': sha(line), **numeric_item(value)})
            if stripped.lower() == b'eventend':
                current.update(end_byte=offset + len(line), end_line=line_no,
                               block_sha256=sha(raw[current['start_byte']:offset + len(line)]))
                rows.append(current)
                current = None
        offset += len(line)
    if current is not None:
        raise ValueError('Unclosed event')
    return rows


def extract(source_zip):
    archive_raw = source_zip.read_bytes()
    if len(archive_raw) != 995176 or sha(archive_raw) != ZIP_SHA:
        raise ValueError('Private source ZIP identity mismatch')
    source = json.loads(SOURCE.read_text())
    with zipfile.ZipFile(source_zip) as archive:
        expected = {'npc/' + row[0]: row for row in source['source_files']}
        if set(archive.namelist()) != set(expected) or len(archive.infolist()) != len(expected):
            raise ValueError('Private source member population mismatch')
        data = {}
        for name, row in expected.items():
            raw = archive.read(name)
            if [len(raw), sha(raw), f'{zlib.crc32(raw):08x}'] != row[1:4]:
                raise ValueError('Original member identity mismatch: ' + name)
            data[row[0]] = raw
    selected = {}
    for path in PARAMETERS:
        raw = data[path]
        text = raw.decode('cp950')
        if text.encode('cp950') != raw:
            raise ValueError('Non-reversible source text')
        selected[path] = raw
    create_rows = [r for r in source['create_rows'] if any(ref[0] in PARAMETERS for ref in r[15])]
    if len(create_rows) != 9:
        raise ValueError('Expected six event and three limitshop creates')
    creates = []
    for row in create_rows:
        raw = data[row[0]]
        if sha(raw[row[2]:row[3]]) != row[4]:
            raise ValueError('Original CREATE byte slice mismatch')
        selected[row[0]] = raw
        for path, _ordinal in row[13]:
            selected[path] = data[path]
        creates.append({'source_file': row[0], 'source_block_ordinal': row[1],
                        'source_start_byte': row[2], 'source_end_byte': row[3],
                        'source_block_sha256': row[4], 'floor': row[5], 'graphic_alias': row[6],
                        'borncorner': row[7], 'borncenter': row[8], 'direction': row[10],
                        'template_token': row[11], 'parameter_file': row[15][0][0],
                        'parameter_sha256': row[15][0][2]})
    scripts = [{'path': path, 'bytes': len(data[path]), 'sha256': sha(data[path]),
                'crc32': f'{zlib.crc32(data[path]):08x}', 'events': events(data[path])}
               for path in PARAMETERS[:6]]
    shops = []
    for path in PARAMETERS[6:]:
        controls = {}
        for line in data[path].splitlines():
            if b':' not in line:
                continue
            key, value = line.split(b':', 1)
            if key in (b'sell_rate', b'LimitItemNo', b'special_item', b'special_rate'):
                controls[key.decode()] = value.decode('ascii')
        shops.append({'path': path, 'sha256': sha(data[path]), 'raw_numeric_controls': controls})
    item_rows = json.loads(ITEMS.read_text())['rows']
    items = [row for row in item_rows if 2469 <= row[0] <= 2474]
    map_rows = json.loads(MAPS.read_text())['floors']
    maps = [row for row in map_rows if row['source_floor_id'] in {1212, 10603, 10605}]
    report = {
        'schema': 'stoneage.quest08.original_mixed25_mining_static_source.r1',
        'origin_class': 'ORIGIN_UNRESOLVED',
        'source_scope': 'LATER_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
        'baseline': {'head': 'ceb75f7f2b0d5f1d1aab4cb4e32d92cdf06f31a3',
                     'tree': 'd5ac2af43986b31d547105f36eb3db5bb5024e94',
                     'preserved_current_blob': 'c89e0e33537990aa2132b47c40fef49a985a935c'},
        'parent_rar_sha256': source['original_rar_sha256'],
        'private_source_zip': {'bytes': len(archive_raw), 'sha256': ZIP_SHA,
                               'verified_members': len(data), 'verified_member_bytes': sum(map(len, data.values()))},
        'derived_input_blobs': {p.relative_to(ROOT).as_posix(): blob(p.read_bytes()) for p in (SOURCE, ITEMS, MAPS)},
        'selected_original_files': [{'path': p, 'bytes': len(b), 'sha256': sha(b),
                                     'crc32': f'{zlib.crc32(b):08x}'} for p, b in sorted(selected.items())],
        'source_creates': creates, 'source_scripts': scripts, 'source_limitshops': shops,
        'prior_item01_numeric_rows_2469_to_2474': items,
        'prior_quest05_map_qualification': maps,
        'boundaries': {'native_execution_verified': False, 'actual_item_delivery_verified': False,
                       'actual_deletion_quantity_verified': False, 'cash_payout_formula_verified': False,
                       'event_comma_or_ampersand_interpreted': False, 'official_origin_verified': False,
                       'original_map_pixels_newly_read': False, 'original_item_pixels_newly_read': False},
        'status': {'stage_A': '7_PARTIAL_2_OPEN', 'stage_B_wiki': 'GATED',
                   'R79': 'PAUSED_NON_BLOCKING', 'overall_percent': None}}
    return report, selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_zip', type=Path)
    parser.add_argument('--report', type=Path, default=REPORT)
    parser.add_argument('--private-dir', type=Path)
    args = parser.parse_args()
    report, selected = extract(args.source_zip)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if args.private_dir:
        args.private_dir.mkdir(parents=True, exist_ok=True)
        for path, raw in selected.items():
            out = args.private_dir / 'original' / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(raw)
        body = ''.join('<details><summary>' + html.escape(path) + '</summary><pre>' +
                       html.escape(raw.decode('cp950')) + '</pre></details>'
                       for path, raw in sorted(selected.items()))
        (args.private_dir / 'index.html').write_text(
            '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>QUEST08 原採礦資料</title>'
            '<style>body{max-width:1000px;margin:40px auto;font:17px system-ui;background:#f5f1e7;color:#24332b}'
            'summary{padding:14px;cursor:pointer}pre{white-space:pre-wrap;background:white;padding:18px}</style>'
            '<h1>原採礦、鑒定與兌幣配置</h1><p>後期社群 mixed25 保存檔。這是原文查閱，不是原遊戲執行。'
            '未認證官方初版歸屬、真實扣物數或兌幣公式。原有文字與可疑字段不修正。</p>' + body + '</html>', encoding='utf-8')
    print(json.dumps({'scripts': len(report['source_scripts']), 'creates': len(report['source_creates']),
                      'events': sum(len(s['events']) for s in report['source_scripts']),
                      'selected_files': len(selected)}, sort_keys=True))


if __name__ == '__main__':
    main()
