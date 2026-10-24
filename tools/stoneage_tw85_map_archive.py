"""Validate durable map metadata against its qualified inventory and receipt.

This checks derived metadata integrity, not a second execution of source maps.
The source run and a later main replay remain separate evidence.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

from tools.stoneage_tw85_map_payload import ROOT, REVIEW, RAW, pin

REPORT = 'research/recovered/STONEAGE-TW85-MAP-PAYLOAD-STRUCTURE-R1.json'
RECEIPT = 'research/recovered/STONEAGE-TW85-MAP-PAYLOAD-CUSTODY-R1.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def validate_report(report):
    review = json.loads((ROOT/REVIEW).read_bytes())
    require(report['source_pins'] == {p: pin(ROOT/p) for p in (RAW, REVIEW)}, 'source pin drift')
    require(report['schema'] == 'stoneage.tw85_map_payload_structure.r1', 'schema drift')
    raw = json.loads((ROOT/RAW).read_bytes())
    require(report['wrapper_sha256'] == raw['assembled_installer']['sha256'] and
            report['msi_sha256'] == raw['inspection']['msi_sha256'], 'carrier identity drift')
    require(report['source_scope'] == 'COMMUNITY_PRESERVED_WAYI_MSI_8.50.0000_PAYLOAD', 'source promotion')
    boundaries = {'runtime_or_installer_executed', 'publisher_clean_disc_authenticated',
                  'plane_semantics_proven_for_this_build', 'filename_token_is_authenticated_floor_id',
                  'named_place_attribution_proven', 'npc_quest_spawn_tables_recovered',
                  'tw10_or_jss1999_map_geometry_proven', 'full_world_coverage_proven',
                  'grid_or_proprietary_asset_published', 'walkability_or_teleports_inferred'}
    require(set(report['boundaries']) == boundaries and all(x is False for x in report['boundaries'].values()),
            'evidence boundary promotion')
    rows = report['files']
    expected = {x['path']: x for x in review['numeric_map_dat_candidates']}
    require(len(rows) == report['numeric_map_files'] == report['exact_layout_matches'] == 42, 'map count drift')
    require(len({x['path'] for x in rows}) == 42 and {x['path'] for x in rows} == set(expected), 'map path coverage')
    groups = defaultdict(list)
    for row in rows:
        source = expected[row['path']]
        require(all(row[k] == source[k] for k in ('path', 'bytes', 'sha256')), 'source file drift')
        require(row['filename_numeric_token'] == source['map_id_filename_token'] and
                row['original_place_name'] is None, 'unqualified identity')
        cells = row['cells']
        require(row['width'] > 0 and row['height'] > 0 and cells == row['width']*row['height'] and
                row['bytes'] == 8+6*cells, 'map extent drift')
        require(row['status'] == 'EXACT_LAYOUT_MATCH' and
                row['layout'] == 'LE_U32_WIDTH_HEIGHT_THREE_LE_U16_PLANES_EXACT_LENGTH', 'layout promotion')
        require([x['ordinal'] for x in row['planes']] == [1, 2, 3], 'plane order drift')
        for plane in row['planes']:
            require(plane['bytes'] == 2*cells and 0 <= plane['nonzero_cells'] <= cells and
                    1 <= plane['distinct_values'] <= min(cells, 65536), 'invalid plane extent/count')
            require(0 <= plane['minimum'] <= plane['maximum'] <= 65535, 'invalid uint16 range')
            frequent = plane['most_frequent']
            require(len(frequent) == min(10, plane['distinct_values']) and
                    len({x['value'] for x in frequent}) == len(frequent), 'frequency coverage drift')
            require(frequent == sorted(frequent, key=lambda x: (-x['cells'], x['value'])), 'frequency order drift')
            require(all(0 <= x['value'] <= 65535 and 0 < x['cells'] <= cells for x in frequent), 'invalid frequency')
            require(sum(x['cells'] for x in frequent) <= cells, 'frequency total overflow')
            if plane['distinct_values'] <= 10:
                require(sum(x['cells'] for x in frequent) == cells, 'incomplete full frequency set')
            for entry in frequent:
                if entry['value'] == 0:
                    require(entry['cells'] == cells-plane['nonzero_cells'], 'zero count drift')
        groups[(row['width'], row['height'])].append(row['path'])
    require(report['dimension_groups'] == [{'width': wh[0], 'height': wh[1], 'paths': paths}
            for wh, paths in sorted(groups.items())], 'dimension grouping drift')
    require(report['same_path_mixed25_byte_comparison'] == review['numeric_map_same_path_comparison_with_mixed25'] and
            report['excluded_auxiliary_dat_files'] == review['map_directory_auxiliary_dat_files'], 'cross-version/auxiliary drift')
    return {'files': len(rows), 'cells': sum(x['cells'] for x in rows),
            'nonzero_cells_by_ordinal': [sum(x['planes'][i]['nonzero_cells'] for x in rows) for i in range(3)]}


def validate():
    receipt = json.loads((ROOT/RECEIPT).read_bytes())
    require(pin(ROOT/REPORT) == receipt['permanent_report'], 'permanent derived report drift')
    for path, expected in receipt['historical_prefixes'].items():
        base = subprocess.check_output(['git', 'show', receipt['base_main']+':'+path], cwd=ROOT)
        require(len(base) == expected['bytes'] and hashlib.sha256(base).hexdigest() == expected['sha256'] and
                (ROOT/path).read_bytes().startswith(base), 'historical prefix loss: '+path)
    result = validate_report(json.loads((ROOT/REPORT).read_bytes()))
    require(receipt['source_run']['conclusion'] == 'success' and receipt['independently_downloaded_zip_sha256'] ==
            receipt['actions_api_zip_sha256'], 'source custody not accepted')
    return {'status': 'PASS', **result}


if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
