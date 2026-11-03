"""Public, original-asset-free replay of the MAP02 derived source coverage.

Private-source original replay: /石器时代/StoneAge-MAP02-private-source-replay.py
and stored images remain outside public Git. These tests check the metadata
contract, NOT a replacement for original commercial DAT/ADRN/REAL decoding.
"""
from __future__ import annotations
import collections
import copy
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAP01_PATH = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'
MAP02_PATH = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json'
HEX64 = re.compile(r'^[0-9a-f]{64}$')


def load():
    return json.loads(MAP01_PATH.read_text(encoding='utf-8')), json.loads(MAP02_PATH.read_text(encoding='utf-8'))


def validate(map01, report):
    assert report['schema'].endswith('verified_source_DAT_three_floor_numeric_image_join.r1')
    p=report['provenance']
    assert p['saved_community_mixed25_RAR_sha256'] == map01['original_rar_sha256']
    assert not p['saved_community_RAR_is_official_contemporaneous_same_deployment']
    assert not p['tw1_resource_bytes_prove_commercial_deployment_of_later_map']

    src={int(x):v for x,v in report['source_three_floors'].items()}
    assert set(src)=={1000,1001,1003}
    verified={(r[0],r[1]):r for r in map01['original_decoded_source_rows']}
    errors={(r[0],r[1]):r for r in map01['source_extraction_errors_not_reclassified_as_corruption']}
    assert (0,'1000.DAT') in errors and (0,'1000.DAT') not in verified
    assert errors[(0,'1000.DAT')][2:4]==[153608,131072]
    assert report['qualified_prior_MAP01_error_kept']['MAP01_63_original_error_rows_unmodified']
    for floor,dat in src.items():
        assert dat['cells']==dat['width']*dat['height']
        assert dat['dat_bytes']==8+6*dat['cells']
        assert HEX64.fullmatch(dat['dat_sha256'])
        assert len(dat['plane_sha256'])==3
        assert all(HEX64.fullmatch(x) for x in dat['plane_sha256'])
        assert len(dat['plane_nonzero_positions'])==3
        assert len(dat['unique_nonzero_aliases_by_plane'])==2
        assert all(0<=n<=dat['cells'] for n in dat['plane_nonzero_positions'])
        assert sum(int(v) for v in dat['raw_third_plane_value_counts'].values())==dat['cells']
        if floor in (1001,1003):
            assert verified[(0,f'{floor}.DAT')][3]==dat['dat_sha256']
        assert dat['all_three_planes_source_verified']
    assert (src[1000]['width'],src[1000]['height'])==(160,160)
    assert (src[1001]['width'],src[1001]['height'])==(30,30)
    assert (src[1003]['width'],src[1003]['height'])==(30,30)

    rows=report['per_alias_source_bitmap_metadata_rows']
    alias=[r['alias'] for r in rows]
    assert len(rows)==len(set(alias))==792
    assert alias==sorted(alias)
    floor_alias={floor:set() for floor in src}
    floor_occ={floor:0 for floor in src}
    present,missing=[],[]
    for row in rows:
        assert isinstance(row['alias'],int) and row['alias']>0
        for floor_s,occ in row['source_floors'].items():
            f=int(floor_s)
            assert f in src and 0<occ<=src[f]['cells']*2
            floor_alias[f].add(row['alias'])
            floor_occ[f]+=occ
        if row['tw1_original_ADRN_record']=='UNIQUE':
            assert row['original_rd_decoded'] is True
            assert row['real_segment_bytes']>16
            assert row['rd_width']>0 and row['rd_height']>0
            for key in ('adrn_record_sha256','original_rd_sha256','private_pixel_rgba_sha256','private_png_sha256'):
                assert HEX64.fullmatch(row[key]), key
            present.append(row)
        else:
            assert row['tw1_original_ADRN_record']=='NOT_FOUND'
            assert row['original_rd_decoded'] is False
            assert 'original_rd_sha256' not in row and 'private_png_sha256' not in row
            missing.append(row)

    imagecounts=report['source_nonzero_numeric_alias_counts']
    for f in src:
        assert len(floor_alias[f])==src[f]['unique_nonzero_aliases_union']
        assert floor_occ[f]==sum(src[f]['plane_nonzero_positions'][:2])
        assert imagecounts[f'floor{f}']==len(floor_alias[f])
    assert len(floor_alias[1001]&floor_alias[1003])==imagecounts['floor1001_vs_1003_shared']==31
    assert len(floor_alias[1001]|floor_alias[1003])==imagecounts['floor1001_vs_1003_union']==47
    assert len(floor_alias[1000]&floor_alias[1001])==imagecounts['floor1000_vs_1001_shared']==6
    assert len(floor_alias[1000]&floor_alias[1003])==imagecounts['floor1000_vs_1003_shared']==6
    assert len(set(alias))==imagecounts['three_floors_union']
    assert len(present)==780 and len(missing)==12
    assert len({r['adrn_index'] for r in present})==780
    assert [r['alias'] for r in missing]==report['original_tw1_unique_alias_join']['missing_original_ADRN_aliases']
    assert all(set(r['source_floors'])=={'1000'} for r in missing)
    o=report['original_tw1_unique_alias_join']
    assert o['all_source_aliases']==792 and o['original_ADRN_unique_record_aliases']==780
    assert o['rle_or_RD_source_failures']==0
    assert o['source_floor1000_actual_original_tw1_RD_decoded_aliases']==740
    assert o['o54_prior_RD_aliases_reverified_original_SHA_and_RGBA']==198
    assert o['new_actual_tw1_RD_aliases_outside_o54_prior_set']==542
    assert o['source_floor1000_aliases_missing_tw1_ADRN']==12

    diff=report['same_sized_floor1001_vs_1003_verified_DAT_cell_differences']
    assert set(diff)=={'0','1','2'}
    assert [diff[str(i)]['different_cells'] for i in range(3)]==[8,51,84]
    for d in diff.values():
        assert d['equal_cells']+d['different_cells']==900
        assert HEX64.fullmatch(d['changed_coordinate_set_sha256'])
        assert HEX64.fullmatch(d['change_original_pairs_sha256'])

    bounds=report['bounds']
    assert bounds['source_DAT_three_floors_complete']
    for key in ('full_original_client_world_entered','original_native_layer_and_palette_authenticated',
                'original_same_deployment_proven','all_2990_MAP01_member_bytes_replayed_MAP02',
                'unverified_63_RAR_map_members_reclassified','native_walkability_computed_MAP02',
                'proprietary_RD_or_PNG_published_Git'):
        assert bounds[key] is False, key
    assert bounds['overall_restoration_percent'] is None


class MapSceneModule02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.map01,cls.report=load()

    def test_full_source_derived_metadata(self):validate(self.map01,self.report)

    def test_map01_failure_must_not_be_silently_upgraded(self):
        r=copy.deepcopy(self.report)
        r['qualified_prior_MAP01_error_kept']['MAP01_63_original_error_rows_unmodified']=False
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_no_fabricated_tw1_art_for_missing_alias(self):
        r=copy.deepcopy(self.report)
        missing=next(x for x in r['per_alias_source_bitmap_metadata_rows'] if x['tw1_original_ADRN_record']=='NOT_FOUND')
        missing['original_rd_decoded']=True
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_no_official_deployment_from_cross_carrier_numeric_alias(self):
        r=copy.deepcopy(self.report)
        r['provenance']['tw1_resource_bytes_prove_commercial_deployment_of_later_map']=True
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_pair_data_cannot_be_swapped_to_same_floor(self):
        r=copy.deepcopy(self.report)
        r['same_sized_floor1001_vs_1003_verified_DAT_cell_differences']['0']['different_cells']=0
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_image_source_positions_are_not_pet_counts(self):
        r=copy.deepcopy(self.report)
        r['source_three_floors']['1000']['plane_nonzero_positions'][0]=24248
        with self.assertRaises(AssertionError):validate(self.map01,r)

if __name__ == '__main__':unittest.main()
