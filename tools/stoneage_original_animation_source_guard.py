"""Validate the actual source receipt against independent archived TW1 tables."""
import hashlib
import json
from pathlib import Path
import re

from tools.stoneage_original_animation_lab import ROOT, ORIGINALS, sample_report, require

SOURCE = ROOT / 'research/recovered/STONEAGE-TW10-ANIMATION-OBSERVATION-P2A-ACTUAL-SOURCE-R1.json'
SOURCE_SHA256 = '6840e79c5e237222884c03760c3c832987a133d22783bc3cb684e9d9c04b85bf'


def validate(source, report):
    require(source['schema'] == 'stoneage.original_animation_actual_source.p2a_v1', 'actual source schema')
    require(source['raw_assets_uploaded'] is False, 'raw original publication claim')
    require(source['original_files'] == {n:{'bytes':v[0],'sha256':v[1]} for n,v in ORIGINALS.items()},
            'actual source file identity mismatch')
    require(len(source['cases']) == len(report['cases']) == 3, 'finite source case count')
    for actual, timeline in zip(source['cases'],report['cases']):
        r=timeline['requested']
        require(actual['selectors'] == [r['spr_no'],r['direction'],r['action']], 'source selector mismatch')
        require(actual['frames'] == len(timeline['frames']) and actual['cycle_ticks'] == timeline['cycle_ticks'],
                'source frame count/timing mismatch')
        require(actual['group_sha256'] == timeline['group']['segment_sha256'], 'actual SPR group mismatch')
        for flag in ('original_client_executed','original_colors_reproduced','assistant_viewed_or_heard_original'):
            require(actual[flag] is False, 'unproved source observation claim: '+flag)
        bitmaps={f['bmp_no']:f['bitmap'] for f in timeline['frames']}
        witnesses=actual['bitmap_witnesses']
        require([w['bitmapno'] for w in witnesses] == list(bitmaps), 'bitmap ordering/duplicate/coverage mismatch')
        for w in witnesses:
            require(w['rd_block_sha256'] == bitmaps[w['bitmapno']]['rd_block_sha256'], 'RD source digest mismatch')
            for field in ('rd_block_sha256','adrn_record_sha256','palette_index_sha256','private_grayscale_png_sha256'):
                require(type(w[field]) is str and re.fullmatch('[0-9a-f]{64}',w[field]), 'invalid source witness digest')
    return True


def main():
    raw=SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, 'archived raw source JSON mismatch')
    validate(json.loads(raw), sample_report())
    print('P2A_ACTUAL_SOURCE_AND_ARCHIVED_FULL_GROUP_AND_BITMAP_JOIN=PASS; ORIGINAL_COLOR_AND_CLIENT_BOOT=OPEN')


if __name__ == '__main__':main()
