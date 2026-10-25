"""Bounded TW1.0 -> mixed25 byte-span audio integration from pinned metadata.

Equal complete containers transfer byte spans, not a later selector table,
filenames, playback indices, event triggers or official build authenticity.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('research/recovered/STONEAGE-CROSSVERSION-AUDIO-CONTENT-R1.json')
AUDIO = 'research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt'
TW = 'research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt'
BRIDGE = 'research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt'
PRIOR = 'research/recovered/STONEAGE-TW10-PRESERVED25-FILE-SHA-INTERSECTION-R1.json'
SOUND3 = 'research/recovered/STONEAGE-SOUND3-ORIGINAL-CONTENT-R1.json'
CN50 = 'research/recovered/STONEAGE-STONEAGE5-REAL-CAB-MSI-PATH-JOIN-R1.json'
TW85 = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json'
PINS = {
    AUDIO: 'f5e5826967da197bafb05f092da620edff91e85d6ac8cda89e29ad11f280bf02',
    TW: '413d197d19ea405490bfffc2bdbf021089177671445ca567533b2eb2576dae7b',
    BRIDGE: '48feb98aa977c88dcc236b530e0428ab665032ec923787eac0c293d5960159b0',
    PRIOR: '1443a12c3ec0d8c7aee5b498c8bc1d978a839cc79d892195ff76abb60574caeb',
    SOUND3: 'ed5d9387a6f8e70da5ad269fc9fa46f8ad5d0b6e0aaf25e3b6d969fe2e1934d0',
    CN50: '69b19fc3ea988a6e3ed3047291082096a2d955f8ca24423d4280a37487fc8a92',
    TW85: '4ea7b43a7e3427ab4443afe801ae7d3e156e6193e1d42ce1b261f733e07de1d8',
}
CLIENT_ROOT = '/SA2.5主程式/stoneage2.5/'
FORMAT = ['audio_format', 'channels', 'sample_rate', 'byte_rate', 'block_align', 'bits_per_sample', 'data_size']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def fields(line):
    tokens = line.split('|')
    out = {}
    for token in tokens[1:]:
        key, value = token.split('=', 1)
        need(key not in out, 'duplicate metadata field')
        out[key] = value
    return tokens[0], out


def bridge_files(text):
    """Join independent size/hash sections, restricted to the actual client subtree."""
    sizes, hashes = {}, {}
    after = False
    for line in text.splitlines():
        match = re.fullmatch(r'(.+)\|(\d+)', line)
        if match and CLIENT_ROOT in match[1]:
            path = match[1].split(CLIENT_ROOT, 1)[1]
            need(path not in sizes, 'duplicate client size path')
            sizes[path] = int(match[2])
        if line == 'ALL-FILE SHA256':
            need(not after, 'repeated full-file hash section')
            after = True
            continue
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line) if after else None
        if match and CLIENT_ROOT in match[2]:
            path = match[2].split(CLIENT_ROOT, 1)[1]
            need(path not in hashes, 'duplicate client hash path')
            hashes[path] = match[1]
    need(after and sizes.keys() == hashes.keys(), 'size/hash occurrence coverage differs')
    return {p: {'path': p, 'bytes': sizes[p], 'sha256': hashes[p]} for p in sorted(hashes)}


def wave(row, prefix):
    need(row[prefix+'riff'] == row[prefix+'wave'] == '1', 'original span is not qualified RIFF/WAVE')
    need(re.fullmatch('[0-9a-f]{64}', row[prefix+'data_sha256']) is not None, 'missing original PCM digest')
    return {**{k: int(row[prefix+k]) for k in FORMAT},
            'data_sha256': row[prefix+'data_sha256'],
            'chunk_signature': row[prefix+'chunk_signature']}


def pcm_identity(w):
    return tuple(w[k] for k in [*FORMAT, 'data_sha256'])


def validate_partition(segments, extent):
    end = 0
    for index, s in enumerate(segments):
        need(s['tw10_index'] == index, 'original span ordering/occurrence differs')
        need(s['offset'] == end and s['bytes'] > 0, 'original span gap/overlap/invalid extent')
        end += s['bytes']
        need(end <= extent, 'original span outside container')
    need(end == extent, 'original partition leaves container tail')


def transfer(segments, original, preserved):
    for container in (original, preserved):
        need(type(container.get('bytes')) is int and container['bytes'] > 0
             and isinstance(container.get('sha256'), str)
             and re.fullmatch('[0-9a-f]{64}', container['sha256']) is not None,
             'missing complete container size/SHA256 witness')
    need((original['bytes'], original['sha256']) == (preserved['bytes'], preserved['sha256']),
         'whole-container identity not proven; cannot transfer spans')
    validate_partition(segments, original['bytes'])
    return {'profile': 'PRESERVED25_MIXED_CLIENT_SUBTREE', 'container': preserved,
            'qualification': 'EXACT_COMPLETE_CONTAINER_SHA256_AND_BOUNDED_TW10_PARTITION',
            'inherited_byte_span_occurrences': len(segments),
            'later_runtime_indices': None, 'later_source_filenames': None,
            'later_table_assignment_for_these_legacy_spans_available': False}


def sound3_binding(original, files, cn, tw, legacy, loose, bgm):
    """Transfer actual table rows only after both member identities are established."""
    profiles = {'PRESERVED25_MIXED': files,
        'CN50_PRESERVED': {r['installed_path']: {'bytes': r['size'], 'sha256': r['sha256']}
                           for r in cn['installed_files']},
        'TW85_PRESERVED': {r['path'].split('/data/', 1)[1]: {'bytes': r['size'], 'sha256': r['sha256']}
                          for r in tw['inspection']['inventory']['samples'][0]['files'] if '/data/' in r['path']}}
    # The TW85 directory is normalized separately, never by suffix equality alone.
    profiles['TW85_PRESERVED'] = {'data/'+p: r for p, r in profiles['TW85_PRESERVED'].items()}
    bindings = []
    for profile, manifest in profiles.items():
        table = manifest['data/soundaddr_3.txt']; carrier = manifest['data/sound_3.bin']
        need((table['bytes'], table['sha256']) == (original['members']['soundaddr_3.txt']['bytes'],
                                                  original['members']['soundaddr_3.txt']['sha256']),
             'sound3 table content differs across specimens')
        valid = original['members']['sound_3.bin'] if profile != 'PRESERVED25_MIXED' else original['copies'][0]
        need((carrier['bytes'], carrier['sha256']) == (valid['bytes'], valid['sha256']),
             'sound3 container identity unavailable for table transfer')
        copies = original['copies'] if profile != 'PRESERVED25_MIXED' else original['copies'][:1]
        bindings.append({'profile': profile, 'source_table_path': 'data/soundaddr_3.txt',
            'table_bytes': table['bytes'], 'table_sha256': table['sha256'],
            'source_container_path': 'data/sound_3.bin', 'container_bytes': carrier['bytes'],
            'container_sha256': carrier['sha256'], 'table_records': len(original['table_records']),
            'physical_wave_span_occurrences': len(copies)*len(original['table_records']),
            'copy_offsets': [c['offset'] for c in copies],
            'table_addresses_first_copy_only': True, 'effective_runtime_choice': None})
    comparisons = []
    for r in original['table_records']:
        comparisons.append({'sound3_table_index': r['table_index'], 'table_name': r['table_name'],
            'exact_tw10_indexed_matches': [s['tw10_index'] for s in legacy
                if (s['bytes'], s['sha256']) == (r['bytes'], r['sha256'])],
            'pcm_format_tw10_indexed_matches': [s['tw10_index'] for s in legacy
                if pcm_identity(s['wave']) == pcm_identity(r['wave'])],
            'exact_tw10_loose_sfx_or_bgm_paths': [s['path'] for s in loose+bgm
                if (s['bytes'], s['sha256']) == (r['bytes'], r['sha256'])],
            'pcm_format_tw10_loose_sfx_or_bgm_paths': [s['path'] for s in loose+bgm
                if pcm_identity(s['wave']) == pcm_identity(r['wave'])]})
    return {'original_source_metadata': original, 'specimen_bindings': bindings,
            'comparison_to_tw10_surfaces': comparisons,
            'original_filenames_are_gameplay_event_labels': False}


def compare_loose(loose, segments, files):
    exact = [s['tw10_index'] for s in segments
             if (s['bytes'], s['sha256']) == (loose['bytes'], loose['sha256'])]
    pcm = [s['tw10_index'] for s in segments if pcm_identity(s['wave']) == pcm_identity(loose['wave'])]
    return {**loose, 'exact_legacy_span_indices': exact, 'matching_pcm_and_format_span_indices': pcm,
            'standalone_exact_file_paths_in_mixed25': [p for p, f in files.items()
                if (f['bytes'], f['sha256']) == (loose['bytes'], loose['sha256'])],
            'original_loose_path_present_in_mixed25': loose['path'] in files,
            'relation_to_inherited_sound1': 'EXACT_FULL_WAVE_BYTES' if exact else
                'EXACT_PCM_AND_FORMAT_ONLY' if pcm else 'NO_MATCH_IN_LEGACY_CONTAINER_SPANS'}


def build(root=ROOT):
    source, pins = {}, {}
    for path, digest in PINS.items():
        raw = (root/path).read_bytes()
        pins[path] = fingerprint(raw)
        need(pins[path]['sha256'] == digest, 'pinned source metadata changed: '+path)
        source[path] = raw.decode()
    files = bridge_files(source[BRIDGE])
    need(len(files) == 2302, 'complete client subtree file count differs')
    core = {}
    for line in source[TW].splitlines():
        if line.startswith('CORE_FILE|'):
            _, r = fields(line)
            p = r['path'].removeprefix('StoneAge/')
            need(p not in core, 'duplicate original core file path')
            core[p] = {'path': p, 'bytes': int(r['size']), 'sha256': r['sha256']}
    need(len(core) == 383, 'original core inventory count differs')
    segments, loose, bgm, sources = [], [], [], {}
    for line in source[AUDIO].splitlines():
        if '|' not in line or line.startswith('SCOPE|'):
            continue
        kind, r = fields(line)
        if kind == 'SOURCE':
            p = r['path'].removeprefix('StoneAge/')
            sources[p] = {'path': p, 'bytes': int(r['bytes']), 'sha256': r['sha256']}
            need(sources[p] == core[p], 'audio catalog and original file inventory disagree')
        elif kind == 'INDEXED':
            segments.append({'tw10_index': int(r['index']), 'offset': int(r['offset']),
                'bytes': int(r['size']), 'tw10_table_name': r['name'],
                'sha256': r['container_sha256'], 'wave': wave(r, 'container_')})
            loose.append({'path': r['loose_path'].removeprefix('StoneAge/'),
                'bytes': int(r['loose_size']), 'sha256': r['loose_sha256'], 'wave': wave(r, 'loose_')})
        elif kind in ('UNINDEXED_SFX', 'BGM'):
            entry = {'path': r['path'].removeprefix('StoneAge/'), 'bytes': int(r['size']),
                     'sha256': r['sha256'], 'wave': wave(r, 'wave_')}
            (loose if kind == 'UNINDEXED_SFX' else bgm).append(entry)
    need((len(segments), len(loose), len(bgm)) == (114, 116, 11), 'original audio surface counts differ')
    for item in loose+bgm:
        need({k: item[k] for k in ['path', 'bytes', 'sha256']} == core[item['path']],
             'original loose waveform differs from independent file inventory')
    inherited = transfer(segments, sources['data/sound_1.bin'], files['data/sound_1.bin'])
    prior = json.loads(source[PRIOR])
    previous = [r for r in prior['matched'] if r['path'] == 'data/sound_1.bin']
    need(len(previous) == 1 and previous[0]['sha256'] == inherited['container']['sha256']
         and previous[0]['size'] == inherited['container']['bytes']
         and previous[0]['bridge_paths'] == ['data/sound_1.bin'], 'prior whole-file join differs')
    comparisons = [compare_loose(r, segments, files) for r in loose]
    bgm_comparisons = [compare_loose(r, segments, files) for r in bgm]
    groups = defaultdict(list)
    for s in segments:
        groups[(s['bytes'], s['sha256'])].append(s['tw10_index'])
    for indices in groups.values():
        need(all(segments[i]['wave'] == segments[indices[0]]['wave'] for i in indices),
             'equal full-WAVE digest has conflicting metadata')
    unique_bytes = sum(size for size, digest in groups)
    audio_files = [r for p, r in files.items() if p.lower().endswith(('.wav', '.mp3', '.ogg', '.mid', '.midi'))
                   or re.fullmatch(r'data/sound(?:addr)?_\d+\.(?:bin|txt)', p.lower())]
    s3 = sound3_binding(json.loads(source[SOUND3]), files, json.loads(source[CN50]),
                        json.loads(source[TW85]), segments, loose, bgm)
    return {'schema': 'stoneage.crossversion_audio_content.r1', 'date': '2026-10-25',
        'task': 'CROSSVERSION-AUDIO-ORIGINAL-CONTENT-15', 'source_pins': pins,
        'novelty': 'Transfer 114 legacy spans; actually read the bounded original sound3 table/container, prove 27 entries/26 different WAVE blocks and three exact full-container copies; link the smaller mixed25 file and equal later sample members without selecting runtime behavior.',
        'preexisting_facts_not_new': ['original 114/116/11 audio surfaces and 107/1/6 same-name comparison',
            'unindexed sak_91/92 equal original indexed sak_01/02', 'whole sound_1.bin file SHA shared with mixed25'],
        'original_tw10_sources': sources, 'mixed25_inheritance': inherited,
        'legacy_byte_spans': segments, 'original_loose_sfx_comparison': comparisons,
        'original_bgm_comparison': bgm_comparisons,
        'sound3_original_content': s3,
        'scope': {'tw10_core_files': len(core), 'mixed25_client_subtree_files': len(files),
            'mixed25_audio_named_files': audio_files, 'nested_archive_payloads_scanned': False},
        'summary': {'inherited_legacy_span_occurrences': len(segments), 'distinct_full_wave_blocks': len(groups),
            'distinct_pcm_and_format_blocks': len({pcm_identity(s['wave']) for s in segments}),
            'loose_sfx_relations': dict(sorted(Counter(r['relation_to_inherited_sound1'] for r in comparisons).items())),
            'standalone_tw10_sfx_files_exactly_matched_in_client_subtree': sum(bool(r['standalone_exact_file_paths_in_mixed25']) for r in comparisons),
            'standalone_tw10_bgm_files_exactly_matched_in_client_subtree': sum(bool(r['standalone_exact_file_paths_in_mixed25']) for r in bgm_comparisons),
            'same_container_span_reference_budget': {'two_specimen_references': len(segments)*2,
                'logical_segment_bytes': sources['data/sound_1.bin']['bytes']*2,
                'distinct_segment_bytes': unique_bytes,
                'repeated_reference_bytes': sources['data/sound_1.bin']['bytes']*2-unique_bytes,
                'actual_original_bytes_deleted': 0}},
        'duplicate_legacy_wave_blocks': [{'bytes': size, 'sha256': digest, 'tw10_indices': indices}
            for (size, digest), indices in sorted(groups.items()) if len(indices) > 1],
        'precise_missing_evidence': {'soundaddr_1_file_in_mixed25': 'data/soundaddr_1.txt' in files,
            'soundaddr_3_complete_numeric_rows_retained_in_permanent_metadata': True,
            'sound_3_all_wave_metadata_and_copy_offsets_retained': True,
            'sound_3_waveform_payload_retained_in_git': False, 'mixed25_effective_sound_selector': None,
            'named_scene_pet_battle_event_mapping': None},
        'boundaries': {'bounded_source_prefix_newly_downloaded': True,
            'full_client_or_full_cab_newly_downloaded': False, 'original_audio_played': False,
            'waveforms_or_programs_in_git': False, 'same_deployed_official_build_proven': False,
            'soundaddr_suffix_proves_pairing': False, 'old_loose_paths_absent_means_audio_deleted': False,
            'tw10_indices_or_names_promoted_to_later_runtime': False, 'new_named_gameplay_audio_events': 0,
            'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING',
            'large_private_custody': 'PAUSED', 'overall_restoration_percentage': None},
        'reopen': 'Matching original executable sound-table selection and a named gameplay trigger. Actual table rows/content now retained as metadata; no further container or API helper expansion without that dependency.',
        'next': 'ORIGINAL-CHARACTER-CREATION-CONTENT-16'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    args = p.parse_args()
    result = build()
    if args.verify:
        need(result == json.loads((ROOT/OUTPUT).read_bytes()), 'audio content semantic replay differs')
        print('114 inherited spans, 116 loose SFX, 11 BGM and exact later selector gaps verified')
    else:
        (ROOT/OUTPUT).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
        print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
