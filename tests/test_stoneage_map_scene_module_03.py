"""MAP03 public derived-evidence gate; proprietary original MAP/ADRN/REAL not used by CI.

The actual original byte replay was performed privately against the preserved RAR
and previously SHA/CRC-qualified original ADRN and DAT. Do not imply CI
re-extracts proprietary files or verifies the native commercial game.
"""
from __future__ import annotations
import collections
import copy
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-03-98-ORIGINAL-MAP-SOURCE-AND-12-INDEX-R1.json'
MAP01=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'
H64=re.compile(r'^[0-9a-f]{64}$')


def validate(map01, data):
    assert data['schema'].endswith('original_98_both_archive_MAP_source_bytes_and_later_12_graphic_index_scope.r1')
    assert data['source_original_RAR_sha256']==map01['original_rar_sha256']
    assert H64.fullmatch(data['source_independent_previously_saved_ADRN_15_sha256'])
    assert data['source_ADRN_15_original_bytes']==234564*80
    assert data['source_ADRN_15_rar_member_original_crc32']=='3113c408'
    assert data['source_MAP1000_DAT_original_bytes']==8+6*160*160
    assert H64.fullmatch(data['source_MAP1000_DAT_sha256'])
    assert data['source_later_REAL_15_original_claimed_bytes_not_extracted']==763908374
    prior={(g,n.lower()):row for row in map01['original_decoded_source_rows'] for g,n in [(row[0],row[1])]}
    rows=data['different_source_MAP_file_pairs']
    wanted=set(map01['cross_client_addon_MAP_names_with_verified_byte_differences'])
    assert len(rows)==len(wanted)==98
    assert set(r['map_filename'] for r in rows)==wanted
    assert len({r['map_filename'] for r in rows})==98
    assert all(H64.fullmatch(r['client_map_sha256']) and H64.fullmatch(r['addon_map_sha256']) for r in rows)
    assert all(r['client_map_sha256']!=r['addon_map_sha256'] for r in rows)
    for r in rows:
        assert r['source_unique_value_counts'][0]>0 and r['source_unique_value_counts'][1]>0
        assert len(r['source_zero_nonzero_counts'])==2
        for g,which in [(0,'client'),(1,'addon')]:
            m=prior[(g,r['map_filename'])]
            w,h=r[which+'_map_dims']
            assert w>0 and h>0 and (w,h)==(m[6],m[7])
            assert r[which+'_map_sha256']==m[3] and r[which+'_map_bytes']==m[2]
            assert m[2]==8+2*w*h
            assert 0<=r['source_zero_nonzero_counts'][g]<=w*h
        assert r['same_dimensions']==(r['client_map_dims']==r['addon_map_dims'])
        if r['same_dimensions']:
            assert 0<r['source_16bit_cell_changes_when_same_dimensions']<=r['client_map_dims'][0]*r['client_map_dims'][1]
            assert H64.fullmatch(r['source_cell_delta_tuple_sha256_if_comparable'])
        else:
            assert r['source_16bit_cell_changes_when_same_dimensions'] is None
            assert r['source_cell_delta_tuple_sha256_if_comparable'] is None
    c=data['verified_counts']
    assert c['MAP01_names_with_two_actual_different_MAP_source_files']==len(rows)
    assert c['actual_individual_original_MAP_files_whole_byte_SHA_CRC_replayed']==2*len(rows)
    assert c['different_MAP_pairs_with_same_dimensions']==sum(x['same_dimensions'] for x in rows)==95
    assert c['different_MAP_pairs_with_changed_dimensions']==sum(not x['same_dimensions'] for x in rows)==3
    assert c['same_dimension_pairs_comparable_map_cells']==sum(x['client_map_dims'][0]*x['client_map_dims'][1] for x in rows if x['same_dimensions'])==505769
    assert c['same_dimension_pairs_actual_changed_map_cells']==sum(x['source_16bit_cell_changes_when_same_dimensions'] for x in rows if x['same_dimensions'])==6212
    groups=collections.defaultdict(list)
    for row in rows:groups[(row['client_map_sha256'],row['addon_map_sha256'])].append(row['map_filename'])
    assert len(groups)==c['unique_original_content_pair_differences_after_sha_pair_dedup']==94
    assert sorted([sorted(v) for v in groups.values() if len(v)>1])==sorted(data['different_source_MAP_filename_groups_sharing_exact_same_client_and_addon_content_SHA'])
    assert sorted([x['map_filename'] for x in rows if not x['same_dimensions']])==['512.map','5376.map','59904.map']
    assert all(row['content_alias_pair_group']=='|'.join(sorted(groups[(row['client_map_sha256'],row['addon_map_sha256'])])) for row in rows)
    missing=data['map1000_twelve_early_TW1_unmapped_graphics_later_index_and_positions']
    assert len(missing)==c['source_12_early_TW1_unmapped_graphic_aliases']==12
    assert [x['graphic_alias'] for x in missing]==[11208,22413,24305,24306,24307,24308,24309,24310,24311,24312,24316,24322]
    assert sum(x['original_map1000_DAT_occurrences'] for x in missing)==c['source_original_MAP1000_missing_alias_cell_occurrences']==14
    assert c['missing_aliases_with_unique_later_preserved_ADRN_source_record']==11
    assert c['missing_aliases_absent_from_later_preserved_ADRN_index']==1
    for item in missing:
        assert len(item['original_map1000_DAT_cell_locations'])==item['original_map1000_DAT_occurrences']>0
        for plane,x,y in item['original_map1000_DAT_cell_locations']:
            assert plane==1 and 85<=x<=90 and 85<=y<=89
        if item['graphic_alias']==22413:
            assert item['later_ADRN_status']=='NOT_FOUND_IN_PRESERVED_234564_RECORD_INDEX'
            assert item['original_ADRN_record_ordinal'] is None
            assert item['later_REAL_segment_offset_candidate'] is None
            assert item['original_ADRN_record_sha256'] is None
        else:
            assert item['later_ADRN_status']=='UNIQUE_SOURCE_INDEX_RECORD_NO_ACTUAL_LATER_REAL_PIXELS'
            assert 125996<=item['original_ADRN_record_ordinal']<234564
            assert item['later_REAL_segment_length_candidate']>0
            assert item['later_REAL_segment_offset_candidate']>=315842228
            assert item['later_REAL_segment_offset_candidate']+item['later_REAL_segment_length_candidate']<=763908374
            assert item['later_REAL_range_within_preserved_archive_declared_length'] is True
            assert H64.fullmatch(item['original_ADRN_record_sha256'])
    assert c['actual_later_REAL_15_pixel_source_blocks_decoded_this_round']==0
    b=data['bounds']
    for k in ('source_archive_original_is_pure_official_client','client_and_addon_subtrees_same_historical_deployment_verified',
              'this_report_contains_full_original_map_byte_payload_or_full_original_tile_grid',
              'later_ADRN_record_alone_proves_real_original_pixel_decoded',
              'later_REAL_full_file_currently_reextracted_with_crc',
              'map_difference_causal_release_order_known',
              'map_source_16bit_number_known_to_be_rendered_exactly_by_original_runtime'):
        assert b[k] is False,k
    assert b['overall_restoration_percentage'] is None
    assert b['stage_b']=='GATED'


class TestMap03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map01=json.loads(MAP01.read_text(encoding='utf-8'))
        cls.report=json.loads(REPORT.read_text(encoding='utf-8'))

    def test_full_derived_metadata_and_source_manifest_consistency(self):validate(self.map01,self.report)

    def test_aliases_not_equal_unique_independent_content_pairs(self):
        r=copy.deepcopy(self.report);r['verified_counts']['unique_original_content_pair_differences_after_sha_pair_dedup']=98
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_no_silent_pixel_promotion_for_later_index_only(self):
        r=copy.deepcopy(self.report);r['verified_counts']['actual_later_REAL_15_pixel_source_blocks_decoded_this_round']=11
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_no_guess_when_alias_22413_absent(self):
        r=copy.deepcopy(self.report);r['map1000_twelve_early_TW1_unmapped_graphics_later_index_and_positions'][1]['original_ADRN_record_ordinal']=126013
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_no_fake_same_size_for_dimension_changed_file(self):
        r=copy.deepcopy(self.report);row=next(x for x in r['different_source_MAP_file_pairs'] if x['map_filename']=='59904.map');row['same_dimensions']=True
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_do_not_swap_client_and_addon_bytes(self):
        r=copy.deepcopy(self.report);row=r['different_source_MAP_file_pairs'][0];row['client_map_sha256']=row['addon_map_sha256']
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_do_not_infer_native_map_or_official_deployment(self):
        r=copy.deepcopy(self.report);r['bounds']['client_and_addon_subtrees_same_historical_deployment_verified']=True
        with self.assertRaises(AssertionError):validate(self.map01,r)

    def test_cell_cluster_never_as_complete_game_world(self):
        r=copy.deepcopy(self.report);r['map1000_twelve_early_TW1_unmapped_graphics_later_index_and_positions'][0]['original_map1000_DAT_cell_locations'][0][1]=150
        with self.assertRaises(AssertionError):validate(self.map01,r)

if __name__=='__main__':unittest.main()
