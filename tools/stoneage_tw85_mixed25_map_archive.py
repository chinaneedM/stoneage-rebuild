"""Offline acceptance for the actual-byte map comparison and immutable custody.

Recompute all hash equality classifications and summaries from pinned sources;
do not claim that metadata validation rereads original proprietary maps.
"""
from collections import Counter
import hashlib
import json
import re
import subprocess

from tools.stoneage_tw85_map_payload import ROOT, pin
from tools.stoneage_tw85_map_archive import REPORT as TW85, validate as validate_tw85
from tools.stoneage_tw85_mixed25_map_diff import BRIDGE, BUNDLE_SHA, PARTS, expected_files

REPORT = 'research/recovered/STONEAGE-TW85-MIXED25-MAP-PLANE-DIFF-R1.json'
RECEIPT = 'research/recovered/STONEAGE-TW85-MIXED25-MAP-PLANE-CUSTODY-R1.json'
DEDUP = 'research/recovered/STONEAGE-TW85-MIXED25-MAP-LAYER-DEDUP-R1.json'
LEGACY = ('research/recovered/STONEAGE-25-MAP-DAT-RELATION-R1.txt',
          'research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LAYER-DIFF-R1.txt')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def legacy_controls(report):
    rows = {x['path'].split('/')[-1].casefold(): x for x in report['compared_files']}
    controls = {}
    for path in LEGACY:
        matched = []
        for line in (ROOT/path).read_text().splitlines():
            if path == LEGACY[0] and line.startswith('PAIR_SAMPLE|'):
                fields = line.split('|')
                if len(fields) != 12 or not fields[1].isdigit():
                    continue
                key = fields[1]+'.dat'
                dimensions = [int(fields[2]), int(fields[3])]
                hashes = fields[9:12]
            elif path == LEGACY[1] and line.startswith('LAYER_DIFF|'):
                fields = dict(x.split('=', 1) for x in line.split('|')[1:])
                key = fields['name'].casefold()
                dimensions = [int(x) for x in fields['dims'].split('x')]
                hashes = [fields['mixed_'+k+'_sha256'] for k in ('tile', 'parts', 'event')]
            else:
                continue
            if key not in rows:
                continue
            actual = rows[key]['mixed25_structure']
            require(dimensions == [actual['width'], actual['height']] and
                    hashes == [x['sha256'] for x in actual['planes']], 'old independent plane control mismatch')
            matched.append(key)
        controls[path] = matched
    require([len(controls[p]) for p in LEGACY] == [7, 8], 'independent control coverage drift')
    return controls


def layer_catalog():
    reference = json.loads((ROOT/TW85).read_bytes())
    compared = json.loads((ROOT/REPORT).read_bytes())
    groups = {}
    for sample, rows in [('TW85', reference['files']), ('MIXED25',
                         [{'path': x['path'], **x['mixed25_structure']} for x in compared['compared_files']])]:
        for row in rows:
            for plane in row['planes']:
                key = (plane['bytes'], plane['sha256'])
                groups.setdefault(key, []).append({'sample': sample, 'path': row['path'],
                    'ordinal': plane['ordinal'], 'width': row['width'], 'height': row['height']})
    return {'schema': 'stoneage.tw85_mixed25_map_layer_dedup.r1',
            'scope': 'ALL_42_TW85_MAPS_AND_ONLY_35_SHARED_MIXED25_PATHS',
            'source_pins': {p: pin(ROOT/p) for p in (TW85, REPORT)},
            'layer_occurrences': sum(len(v) for v in groups.values()),
            'distinct_layer_byte_blocks': len(groups),
            'duplicate_byte_groups': sum(len(v) > 1 for v in groups.values()),
            'cross_sample_duplicate_byte_groups': sum(len({x['sample'] for x in v}) > 1 for v in groups.values()),
            'logical_layer_bytes': sum(size*len(v) for (size, sha), v in groups.items()),
            'distinct_layer_bytes': sum(size for size, sha in groups),
            'groups': [{'bytes': size, 'sha256': sha, 'occurrences': v}
                       for (size, sha), v in sorted(groups.items())],
            'boundaries': {key: False for key in ('proprietary_layer_bytes_embedded',
                'original_files_or_paths_deleted', 'physical_storage_savings_already_realized',
                'equal_bytes_mean_same_named_place_or_geometry', 'complete_mixed25_map_corpus_indexed')}}


def replay(report):
    reference = json.loads((ROOT/TW85).read_bytes())
    wanted = {x['path']: x for x in reference['files']}
    expected = expected_files()
    require(report['schema'] == 'stoneage.tw85_mixed25_map_plane_diff.r1' and
            report['task'] == 'CLIENT-MAP-CROSS-VERSION-PLANE-DIFF-04', 'scope drift')
    require(report['source_class'] == 'MIXED_COMMUNITY_BRIDGE_NOT_AUTHENTICATED_OFFICIAL_25', 'source promotion')
    require(report['source_pins'] == {p: pin(ROOT/p) for p in (TW85, BRIDGE)}, 'parent source drift')
    require(report['bundle_sha256'] == BUNDLE_SHA and report['bundle_bytes'] == 361255180, 'bundle drift')
    require([(p['key'], p['bytes'], p['sha256']) for p in report['acquired_parts']] == PARTS, 'part custody drift')
    keys = {'tw85_package_redownloaded', 'game_or_installer_executed', 'same_named_place_proven',
            'official_patch_chronology_proven', 'changed_cells_computed', 'plane_runtime_semantics_proven',
            'npc_quest_or_spawn_tables_recovered', 'original_payload_published', 'full_world_map_completion_proven'}
    require(set(report['boundaries']) == keys and all(v is False for v in report['boundaries'].values()), 'evidence promotion')
    require(report['tw85_source_bytes_reused_from_qualified_permanent_layer_metadata'] is True, 'TW85 source mode drift')
    present = {path for path in wanted if path.casefold() in expected}
    absent = [path for path in wanted if path.casefold() not in expected]
    rows = report['compared_files']
    require(len(rows) == len(present) == 35 and len({r['path'] for r in rows}) == 35 and
            {r['path'] for r in rows} == present and report['tw85_paths_absent_from_mixed25'] == absent and
            len(absent) == 7, 'path coverage drift')
    masks = Counter()
    for row in rows:
        old = wanted[row['path']]
        require(row['mixed25_sha256'] == expected[row['path'].casefold()] and
                row['tw85_sha256'] == old['sha256'], 'whole file source hash drift')
        require(row['whole_file_equal'] is (row['mixed25_sha256'] == row['tw85_sha256']), 'false whole file equality')
        require(row['original_place_name'] is None, 'unsupported named place attribution')
        require(row['status'] == 'ORDINAL_LAYERS_COMPARED' and row['dimensions_equal'] is True, 'layout scope drift')
        actual = row['mixed25_structure']
        require([actual['width'], actual['height']] == row['tw85_dimensions'] == [old['width'], old['height']], 'dimensions drift')
        cells = actual['width']*actual['height']
        require(cells == actual['cells'] and row['mixed25_bytes'] == 8+6*cells and
                actual['layout'] == old['layout'], 'map byte extent/layout drift')
        planes = actual['planes']
        require([p['ordinal'] for p in planes] == [1, 2, 3], 'plane order drift')
        equal = [a['sha256'] == b['sha256'] for a, b in zip(planes, old['planes'])]
        require(len(row['plane_equal']) == 3 and all(type(v) is bool for v in row['plane_equal']) and
                row['plane_equal'] == equal, 'false layer equality')
        require(row['whole_file_equal'] is all(equal), 'canonical header/layer equality contradicts file equality')
        for p in planes:
            require(p['bytes'] == 2*cells and re.fullmatch('[0-9a-f]{64}', p['sha256']) is not None and
                    0 <= p['nonzero_cells'] <= cells and 1 <= p['distinct_values'] <= min(65536, cells), 'plane digest/count drift')
            require(0 <= p['minimum'] <= p['maximum'] <= 65535, 'plane uint16 range drift')
            freq = p['most_frequent']
            require(len(freq) == min(10, p['distinct_values']) and len({x['value'] for x in freq}) == len(freq) and
                    freq == sorted(freq, key=lambda x: (-x['cells'], x['value'])) and
                    sum(x['cells'] for x in freq) <= cells and
                    all(0 <= x['value'] <= 65535 and 0 < x['cells'] <= cells for x in freq), 'frequency drift')
            if p['distinct_values'] <= 10:
                require(sum(x['cells'] for x in freq) == cells, 'frequency missing values')
            for x in freq:
                if x['value'] == 0:
                    require(x['cells'] == cells-p['nonzero_cells'], 'zero count drift')
        masks[''.join('1' if x else '0' for x in equal)] += 1
    counts = {'tw85_reference_files': 42, 'mixed25_present_paths': 35, 'mixed25_absent_paths': 7,
              'whole_file_equal': sum(x['whole_file_equal'] for x in rows),
              'status_counts': {'ORDINAL_LAYERS_COMPARED': 35}, 'plane_equality_masks': dict(sorted(masks.items()))}
    require(counts == report['counts'], 'summary drift')
    legacy_controls(report)
    return counts


def validate():
    validate_tw85()
    receipt = json.loads((ROOT/RECEIPT).read_bytes())
    require(pin(ROOT/REPORT) == receipt['permanent_report'], 'report bytes changed')
    require(json.loads((ROOT/DEDUP).read_bytes()) == layer_catalog(), 'lossless layer occurrence index drift')
    require(receipt['artifact']['independent_zip_sha256'] == receipt['artifact']['api_zip_sha256'] and
            receipt['source_run']['conclusion'] == 'success', 'source custody not verified')
    require(receipt['legacy_report_pins'] == {p: pin(ROOT/p) for p in LEGACY}, 'legacy control source drift')
    for path, entry in receipt['historical_prefixes'].items():
        raw = subprocess.check_output(['git', 'show', receipt['base_main']+':'+path], cwd=ROOT)
        require(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'] and
                (ROOT/path).read_bytes().startswith(raw), 'historical prefix lost: '+path)
    return {'status': 'PASS', **replay(json.loads((ROOT/REPORT).read_bytes()))}


if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
