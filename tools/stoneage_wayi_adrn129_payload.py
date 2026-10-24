"""Bounded official Wayi repair archive intake; metadata only, no REAL pixels.

The source list's 2005/7.5 repair description and the actual 2006 archived
payload remain separate. Eighty-byte record parsing is a format observation,
not a source-build or entity-identity certification.
"""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import urllib.request

from tools.stoneage_tw85_map_payload import ROOT, digest, pin
from tools.stoneage_tw10_resource_metadata import parse_adrn_record, DeterministicGzipTsv
from tools.stoneage_wayi85_sixpart_acquisition import safe_7z_members

PARENT = 'research/recovered/STONEAGE-WAYI-OFFICIAL-80-DOWNLOAD-CHAIN-R1.json'
PARENT_BLOB = '8f6ddeb1dd5536194711e5d749f5eb2adf6ddc92'
URL = 'https://web.archive.org/web/20060911180132id_/http://www.wayi.com.tw:80/download/file/onlineGame/adrn_129.rar'
ARCHIVE_BYTES = 3983427
ARCHIVE_SHA = 'b077dcc7f1e944c33c6df4fe629d5e37abce9cb4d40f5b8d800cc69d59416e25'
BASES = {
    'TW10': 'research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz',
    'CN50': 'research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz'}
HEADER = ('bitmapno', 'adder', 'size', 'xoff', 'yoff', 'width', 'height')
ATTR_FIELDS = ('atari_x', 'atari_y', 'hit_raw', 'height_flag', 'broken', 'indamage', 'outdamage',
    'inpoison', 'innumb', 'inquiet', 'instone', 'indark', 'inconfuse', 'outpoison', 'outnumb',
    'outquiet', 'outstone', 'outdark', 'outconfuse', 'effect1', 'effect2', 'damy_a', 'damy_b',
    'damy_c', 'map_number', 'hit_flag', 'priority_type')
FIELDS = ('index', *HEADER, 'record_sha256', 'attr_sha256', *ATTR_FIELDS)


def source_contract():
    if pin(ROOT/PARENT)['git_blob'] != PARENT_BLOB:
        raise ValueError('official parent chain changed')
    source = json.loads((ROOT/PARENT).read_bytes())
    entry = next(x for x in source['binary_response_observations'] if x['query_id'] == 'adrn_rar')
    if (entry['requested_url'], entry['response_bytes'], entry['response_sha256']) != (URL, ARCHIVE_BYTES, ARCHIVE_SHA):
        raise ValueError('original archive byte contract drift')
    return entry


def load_baseline(path):
    result = {}
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            key = int(row['bitmapno'])
            if key in result:
                raise ValueError('ambiguous baseline bitmap ID')
            result[key] = (*[int(row[k]) for k in HEADER], row['attr_sha256'])
    return result


def export_index(raw, out, baselines):
    if not raw or len(raw) % 80 or len(raw) > 256*1024*1024:
        raise ValueError('not a bounded exact 80-byte ADRN record stream')
    counts = {name: Counter() for name in baselines}
    samples = {name: [] for name in baselines}
    seen = Counter()
    maps = set()
    unique_records = set()
    minimum = None
    maximum = None
    max_span_end = 0
    special_dimensions = 0
    with DeterministicGzipTsv(out) as stream:
        stream.write('\t'.join(FIELDS)+'\n')
        for index, offset in enumerate(range(0, len(raw), 80)):
            record = raw[offset:offset+80]
            row = parse_adrn_record(record)
            bno = row['bitmapno']
            seen[bno] += 1
            maps.add(row['map_number'])
            minimum = bno if minimum is None else min(minimum, bno)
            maximum = bno if maximum is None else max(maximum, bno)
            max_span_end = max(max_span_end, row['adder']+row['size'])
            special_dimensions += int(not (0 < row['width'] <= 16384 and 0 < row['height'] <= 16384))
            row['index'] = index
            row['record_sha256'] = digest(record)
            unique_records.add(row['record_sha256'])
            stream.write('\t'.join(str(row[k]) for k in FIELDS)+'\n')
            key = (*[row[k] for k in HEADER], row['attr_sha256'])
            for name, table in baselines.items():
                old = table.get(bno)
                status = 'ABSENT_ID' if old is None else 'EXACT_HEADER_AND_ATTR_HASH' if old == key else 'CHANGED_INDEX_METADATA'
                counts[name][status] += 1
                if status != 'EXACT_HEADER_AND_ATTR_HASH' and len(samples[name]) < 8:
                    samples[name].append({'index': index, 'bitmapno': bno, 'status': status})
    return {'records': len(raw)//80, 'distinct_bitmap_ids': len(seen),
            'duplicate_bitmap_occurrences': sum(v-1 for v in seen.values()),
            'unique_record_hashes': len(unique_records), 'bitmap_min': minimum, 'bitmap_max': maximum,
            'nonzero_distinct_map_numbers': len(maps-{0}), 'max_declared_real_span_end': max_span_end,
            'special_dimensions_preserved': special_dimensions,
            'comparisons_by_bitmap_id': {name: {'counts': dict(sorted(c.items())), 'nonexact_samples': samples[name],
                  'baseline_ids_absent_from_patch': len(set(baselines[name])-set(seen))} for name, c in counts.items()}}


def safe_members(listing):
    members = safe_7z_members(listing)
    if len(members) > 256 or sum(x['bytes'] for x in members) > 256*1024*1024:
        raise ValueError('excessive repair archive namespace')
    return members


def acquire(work, derived):
    entry = source_contract()
    work.mkdir(parents=True, exist_ok=True)
    derived.mkdir(parents=True, exist_ok=True)
    attempt = {'status': 'STARTED', 'expected_archive_sha256': ARCHIVE_SHA, 'archive_verified': False,
               'extractor': 'unar', 'original_code_executed': False}
    def checkpoint():
        (derived/'ATTEMPT-R1.json').write_text(json.dumps(attempt, sort_keys=True, indent=2)+'\n')
    checkpoint()
    archive = work/'adrn_129.rar'
    request = urllib.request.Request(URL, headers={'User-Agent': 'StoneAge-history-research/1.0'})
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read(ARCHIVE_BYTES+1)
        final_url = response.geturl()
    if len(raw) != ARCHIVE_BYTES or digest(raw) != ARCHIVE_SHA:
        raise ValueError('actual repair archive differs from accepted source bytes')
    archive.write_bytes(raw)
    attempt.update(status='ARCHIVE_VERIFIED', archive_verified=True, actual_archive_bytes=len(raw),
                   actual_archive_sha256=digest(raw))
    checkpoint()
    listing = subprocess.run(['7z', 'l', '-slt', str(archive)], capture_output=True, text=True, check=True, timeout=60)
    members = safe_members(listing.stdout)
    attempt.update(status='BOUNDED_MEMBER_LIST_VERIFIED', members=members)
    checkpoint()
    destination = work/'members'
    destination.mkdir(exist_ok=True)
    subprocess.run(['unar', '-f', '-D', '-o', str(destination), str(archive)], check=True,
                   stdout=subprocess.DEVNULL, timeout=90)
    attempt['status'] = 'MEMBERS_STATICALLY_EXTRACTED'
    checkpoint()
    actual = []
    indexes = []
    baselines = {name: load_baseline(ROOT/path) for name, path in BASES.items()}
    allowed = {x['path']: x for x in members}
    for path in sorted(destination.rglob('*')):
        if path.is_symlink():
            raise ValueError('archive symlink refused')
        if not path.is_file():
            continue
        rel = path.relative_to(destination).as_posix()
        if rel not in allowed or path.stat().st_size != allowed[rel]['bytes']:
            raise ValueError('actual member differs from bounded archive listing')
        actual.append({'path': rel, **pin(path)})
        if re.fullmatch(r'adrn_\d+\.bin', path.name, re.I):
            metadata_name = f'INDEX-{len(indexes)+1}-R1.tsv.gz'
            try:
                metrics = export_index(path.read_bytes(), derived/metadata_name, baselines)
                indexes.append({'member_path': rel, 'format': '80_BYTE_HEADER28_ATTR52_LAYOUT',
                                'derived_table': metadata_name, 'derived_pin': pin(derived/metadata_name), **metrics})
            except ValueError as exc:
                indexes.append({'member_path': rel, 'format': 'UNRESOLVED', 'reason': str(exc)})
    expected_files = {x['path'] for x in members if not x['attributes'].startswith('D')}
    if {x['path'] for x in actual} != expected_files:
        raise ValueError('member coverage differs after extraction')
    report = {'schema': 'stoneage.wayi_adrn129_official_patch_payload.r1',
              'task': 'TW-WAYI-ADRN129-OFFICIAL-RESOURCE-PATCH-PAYLOAD-05',
              'source_pins': {p: pin(ROOT/p) for p in (PARENT, *BASES.values())},
              'archive_bytes': len(raw), 'archive_sha256': digest(raw), 'requested_url': URL, 'final_url': final_url,
              'source_capture': '2006-09-11T18:01:32Z', 'listing_display_date': '2005-05-18',
              'source_role': 'OFFICIAL_LIST_DESCRIBED_75_BLACK_SCREEN_INDEX_REPAIR_2006_CAPTURE_BYTES',
              'members': actual, 'indexes': indexes,
              'baseline_records': {k: len(v) for k, v in baselines.items()},
              'boundaries': {key: False for key in ('exact_2005_build_proven', 'version_80_exclusivity_proven',
                  'original_real_pixel_blocks_verified', 'game_or_installer_executed', 'named_pet_npc_identity_proven',
                  'original_server_master_recovered', 'all_official_clients_collected', 'proprietary_payload_published')}}
    (derived/'REPORT-R1.json').write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    attempt.update(status='COMPLETE_DERIVED_METADATA', report_pin=pin(derived/'REPORT-R1.json'))
    checkpoint()
    print(json.dumps({'members': len(actual), 'indexes': indexes}, ensure_ascii=False, sort_keys=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--derived', type=Path, required=True)
    args = parser.parse_args()
    try:
        acquire(args.work.resolve(), args.derived.resolve())
    except Exception as exc:
        args.derived.mkdir(parents=True, exist_ok=True)
        path = args.derived/'ATTEMPT-R1.json'
        state = json.loads(path.read_bytes()) if path.exists() else {}
        state.update(status='FAILURE', error_type=type(exc).__name__, error_detail=str(exc)[:500])
        path.write_text(json.dumps(state, sort_keys=True, indent=2)+'\n')
        raise
