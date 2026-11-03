"""MAP01: original source-file metadata and cross-directory map relationships.

Replays only rights-safe derived original RAR hashes and bounded source labels.
Original proprietary map bytes and actual game runtime remain outside public Git.
"""
import copy
import json
import unittest
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parents[1]/'research'/'recovered'


def load(name):return json.loads((R/name).read_text(encoding='utf-8'))


def replay(d, char09):
    assert d['schema']=='stoneage.map_scene_module01.original_RAR_MAP_DAT_addon_server_custody_and_pair_diff.r1'
    assert d['original_rar_sha256']==char09['original_rar_sha256']
    assert d['original_rar_bytes']==char09['original_rar_size_bytes']==361255180
    assert d['full_rar_header_entries_seen']==7952
    assert d['group_codes']=={'0':'client_original_saved','1':'addon_SACH_MX_0_30','2':'server_map_metadata'}
    rows=d['original_decoded_source_rows'];errors=d['source_extraction_errors_not_reclassified_as_corruption'];count=d['verified_counts']
    assert len(rows)==count['members_full_bytes_independently_RAR_crc_matched']==2990
    assert len(errors)==count['members_with_local_libarchive_read_error']==63
    assert len(rows)+len(errors)==count['expected_selected_members_in_RAR_manifest']==3053
    assert len({(r[0],r[1].casefold()) for r in rows})==len(rows)
    assert len({(r[0],r[1].casefold()) for r in errors})==len(errors)
    assert not ({(r[0],r[1].casefold()) for r in rows}&{(e[0],e[1].casefold()) for e in errors})
    assert Counter(r[0] for r in rows)=={0:1990,1:997,2:3}
    assert Counter(e[0] for e in errors)=={0:51,1:12}
    assert all(e[2]>=e[3]>=0 and e[4] for e in errors)
    assert all(len(r)==9 and len(r[3])==64 and len(r[4])==8 for r in rows)
    for r in rows:
        assert r[0] in (0,1,2)
        if r[0]==2:
            assert r[5] is None and r[6] is None and r[7] is None and r[8] is None
        elif r[5] is not None and r[2]>=8:
            factor=2 if r[1].lower().endswith('.map') else 6
            assert r[8] is True and r[6]>0 and r[7]>0
            assert r[2]==8+factor*r[6]*r[7]
        else:
            assert r[8] is None
    assert sum(r[8] is True for r in rows)==count['header_cell_size_formula_verified_MAP_DAT_files']==2971

    client={r[1].casefold():r for r in rows if r[0]==0}
    addon={r[1].casefold():r for r in rows if r[0]==1}
    cmap={k:r for k,r in client.items() if k.endswith('.map')}
    cdat={k:r for k,r in client.items() if k.endswith('.dat')}
    amap={k:r for k,r in addon.items() if k.endswith('.map')}
    assert len(cmap)==count['client_original_MAP_full_crc_SHA']==1019
    assert len(cdat)==count['client_original_DAT_full_crc_SHA']==971
    assert len(amap)==count['addon_MAP_full_crc_SHA']==997
    assert sum(r[0]==2 for r in rows)==count['server_original_metadata_full_crc_SHA']==3
    pair={k for k in cdat if k[:-4]+'.map' in cmap}
    empty={k for k in pair if cdat[k][2]==0}
    same_dim={k for k in pair if cdat[k][6:8]==cmap[k[:-4]+'.map'][6:8]}
    assert len(pair)==count['client_MAP_vs_DAT_same_stem_both_full_source_bytes']==965
    assert len(empty)==count['client_MAP_vs_DAT_same_stem_empty_DAT_placeholder']==12
    assert set(d['client_MAP_names_with_verified_empty_DAT_placeholders'])==empty
    assert len(same_dim)==count['client_MAP_vs_DAT_same_stem_same_header_dims_nonempty']==953
    common=set(cmap)&set(amap)
    different={k for k in common if cmap[k][3]!=amap[k][3]}
    assert len(common)==count['client_MAP_vs_addon_MAP_same_stem_both_full_source_bytes']==996
    assert len(different)==count['client_MAP_vs_addon_MAP_exact_sha_different']==98
    assert len(common)-len(different)==count['client_MAP_vs_addon_MAP_exact_sha_equal']==898
    assert set(d['cross_client_addon_MAP_names_with_verified_byte_differences'])==different
    assert d['cross_client_addon_MAP_names_with_verified_byte_differences']==sorted(different)

    meta={r[1]:r for r in rows if r[0]==2}
    for key,original in [('mapset.txt',d['mapset']['main']),('mapset1.txt',d['mapset']['alternate'])]:
        assert meta[key][2]==original['bytes']
        assert meta[key][3]==original['sha256']
    assert d['mapset']['main']['rows']==count['mapset_main_numeric_source_rows']==20157
    assert d['mapset']['alternate']['rows']==count['mapset_alternate_numeric_source_rows']==16803
    assert count['same_mapset_ID_row_sha_equal']==16802
    assert count['same_mapset_ID_row_sha_different']==1
    assert count['mapset_main_only_IDs']==len(d['mapset']['main_only_numeric_IDs'])==3354
    assert count['mapset_alternate_only_IDs']==0
    assert len(set(d['mapset']['main_only_numeric_IDs']))==3354
    assert len(d['mapset']['differing_ID_rows'])==1
    mismatch=d['mapset']['differing_ID_rows'][0]
    assert mismatch['id']==10230
    assert mismatch['main_original_sha256']!=mismatch['alternative_original_sha256']
    assert len(mismatch['source_main_values_ascii'])==len(mismatch['source_alternative_values_ascii'])==20
    assert mismatch['source_main_values_ascii'][0]==mismatch['source_alternative_values_ascii'][0]==10230
    warp=d['mapwarp']
    assert meta['mapwarp.txt'][2]==warp['raw_bytes']==110674
    assert meta['mapwarp.txt'][3]==warp['source_sha256']
    assert warp['source_rows']==count['mapwarp_source_routes_with_two_numeric_floor_endpoints']==2981
    assert (warp['source_and_destination_in_mapset_main'],warp['source_only_in_mapset_main'],warp['destination_only_in_mapset_main'],warp['neither_source_nor_destination_in_mapset_main'])==(2297,79,105,500)
    assert warp['unique_source_floorids']==639 and warp['unique_destination_floorids']==593
    assert all(x is False for x in d['bounds'].values() if x is not None)
    assert d['bounds']['overall_restoration_percent'] is None
    assert d['next']=='MAP_SCENE_MODULE_02_ACTUAL_PASSABLE_TILE_AND_SOURCE_ALIASES_BATCH_WITH_VERIFIED_BYTES_ONLY'


class TestMAP01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load('STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json')
        cls.char09=load('STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json')
    def test_original_metadata_complete_replay(self):replay(self.data,self.char09)
    def reject(self,modify):
        value=copy.deepcopy(self.data);modify(value)
        with self.assertRaises((AssertionError,KeyError,TypeError)):replay(value,self.char09)
    def test_reject_false_verified_map(self):self.reject(lambda d:d['source_extraction_errors_not_reclassified_as_corruption'].pop())
    def test_reject_mutated_original_MAP_SHA(self):self.reject(lambda d:d['original_decoded_source_rows'][0].__setitem__(3,'0'*64))
    def test_reject_original_map_dimension(self):self.reject(lambda d:next(r for r in d['original_decoded_source_rows'] if r[8] is True).__setitem__(6,7))
    def test_reject_false_client_addon_equal(self):self.reject(lambda d:d['cross_client_addon_MAP_names_with_verified_byte_differences'].pop())
    def test_reject_mapset_missing_ID(self):self.reject(lambda d:d['mapset']['main_only_numeric_IDs'].pop())
    def test_reject_mapwarp_fake_route_count(self):self.reject(lambda d:d['mapwarp'].__setitem__('source_rows',2982))
    def test_reject_claim_original_runtime(self):self.reject(lambda d:d['bounds'].__setitem__('full_original_world_entered_or_played',True))

if __name__=='__main__': unittest.main()
