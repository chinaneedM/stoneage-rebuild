"""Analyze two exact early CAB members; retain metadata only, never waveforms."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct

from tools.stoneage_tw10_audio_metadata import parse_wave

OUTPUT = Path('research/recovered/STONEAGE-SOUND3-ORIGINAL-CONTENT-R1.json')
TABLE_SHA = '5afc6a80352d5254c926129e4acdd023cabdc9e67e5f8cf5bf824520ea2be5e7'
CONTAINER_SHA = 'f5c0b5b0bf3dc7e010c3cde867536929b1f51d81a7ace5ff30d143ccff33b148'
MIXED_SHA = '32906404a97609aab90f5c22ae57e0619aeac820cac1f965ca2bf1d631c3ec94'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def address_rows(table):
    rows = []
    for line in table.decode('ascii').splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'(\d+):(\d+):([A-Za-z0-9_]+\.wav)', line)
        need(match is not None, 'unparsed original address-table text')
        offset, size, name = match.groups()
        rows.append({'table_index': len(rows), 'offset': int(offset), 'bytes': int(size), 'table_name': name})
    return rows


def inspect(table, container):
    rows = address_rows(table)
    need(bool(rows), 'empty table')
    end = 0
    for row in rows:
        need(row['offset'] == end and row['bytes'] >= 12, 'table gap/overlap or invalid record')
        end += row['bytes']
        need(end <= len(container), 'table outside actual container')
    need(end > 0 and len(container) % end == 0, 'unclassified container tail')
    copies = []
    for offset in range(0, len(container), end):
        data = container[offset:offset+end]
        need(data == container[:end], 'tail is not an exact repeated byte segment')
        copies.append({'offset': offset, 'bytes': end, 'sha256': sha(data),
                       'directly_addressed_by_retained_table': offset == 0})
    records = []
    for row in rows:
        data = container[row['offset']:row['offset']+row['bytes']]
        need(data[:4] == b'RIFF' and data[8:12] == b'WAVE', 'not original RIFF/WAVE')
        need(struct.unpack_from('<I', data, 4)[0]+8 == len(data), 'RIFF outer extent mismatch')
        wave = parse_wave(data)
        need(wave['riff'] == wave['wave'] == 1 and wave['audio_format'] == 1
             and wave['data_sha256'] and ':truncated' not in wave['chunk_signature'],
             'original waveform structure not qualified')
        records.append({**row, 'sha256': sha(data), 'wave': wave,
            'physical_offsets_in_full_container': [c['offset']+row['offset'] for c in copies]})
    counts = Counter((r['bytes'], r['sha256']) for r in records)
    return {'table_records': records, 'table_declared_end': end, 'copies': copies,
        'distinct_full_wave_blocks': len(counts), 'physical_record_occurrences': len(records)*len(copies),
        'duplicate_table_wave_groups': [
            {'bytes': size, 'sha256': digest,
             'table_indices': [r['table_index'] for r in records if (r['bytes'], r['sha256']) == (size, digest)]}
            for (size, digest), n in sorted(counts.items()) if n > 1],
        'sample_rate_counts': dict(sorted(Counter(str(r['wave']['sample_rate']) for r in records).items())),
        'effective_runtime_table_or_tail_selection': None}


def produce(directory, cab):
    table = (directory/'soundaddr_3.txt').read_bytes()
    container = (directory/'sound_3.bin').read_bytes()
    need(len(table) == 691 and sha(table) == TABLE_SHA, 'not pinned original table')
    need(len(container) == 2696934 and sha(container) == CONTAINER_SHA, 'not pinned original container')
    result = inspect(table, container)
    need(len(result['table_records']) == 27 and result['table_declared_end'] == 898978
         and len(result['copies']) == 3 and all(c['sha256'] == MIXED_SHA for c in result['copies']),
         'actual source segment/mixed25 identity differs')
    with cab.open('rb') as f:
        prefix = f.read(8388608)
    need(len(prefix) == 8388608 and prefix[:4] == b'MSCF' and cab.stat().st_size == 612584670,
         'bounded CAB prefix witness differs')
    need(sha(prefix) == '87973df39afea068021d64a71fc9fb4f290cc0d7447fd3fae6beeea2bdb3c937',
         'actual bounded source prefix digest differs')
    return {'schema': 'stoneage.sound3_original_content.r1',
        'source': {'archive_identifier': 'Stoneage-5', 'carrier': 'CD [STA5].bin',
            'carrier_catalogue_sha1_not_full_rehashed': '6053dce3df2723250ddb52a98b3e8cf2552cd791',
            'carrier_bytes': 733057248, 'cab_logical_bytes': 612584670,
            'cab_prefix_bytes': len(prefix), 'cab_prefix_sha256': sha(prefix),
            'http_raw_range': 'bytes 65856-9699647/733057248',
            'logical_prefix_reconstructed_from_sector_payloads': True,
            'full_disc_or_full_cab_downloaded': False, 'official_clean_build_proven': False},
        'members': {'soundaddr_3.txt': {'bytes': len(table), 'sha256': sha(table)},
                    'sound_3.bin': {'bytes': len(container), 'sha256': sha(container)}},
        **result,
        'boundaries': {'original_code_executed': False, 'waveform_played': False,
            'waveform_payload_or_original_table_text_in_git': False,
            'tail_copies_are_new_sounds': False, 'same_file_suffix_proves_runtime_selection': False,
            'same_deployed_build_proven': False, 'named_scene_pet_or_battle_event': None}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, required=True)
    p.add_argument('--cab', type=Path, required=True)
    p.add_argument('--output', type=Path, default=OUTPUT)
    args = p.parse_args()
    result = produce(args.directory, args.cab)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'table_records': len(result['table_records']),
        'physical_occurrences': result['physical_record_occurrences'],
        'copies': len(result['copies']), 'distinct_wave_blocks': result['distinct_full_wave_blocks']}))


if __name__ == '__main__':
    main()
