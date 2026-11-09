"""INTEGRATION22 source-bounded public checks.

No private original RAR/DAT/RD/PNG is read by CI; private replay is separate.
"""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
Q = 'STONEAGE-INTEGRATION22-THREE-VILLAGE-TEN-SHOPS-SOURCE-R1.json'
S = 'STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'
M = 'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
PINS = {
    S: '3bde3b7df43725f28cdac355823667a0ba87e9b1',
    M: '137580e7c25aadf3d679b6ebfb5080b79912cc4f',
}

def original_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def source():
    data = {}
    for n, expected in PINS.items():
        raw = (R / n).read_bytes()
        assert original_blob(raw) == expected, ('source Git blob changed', n)
        data[n] = json.loads(raw)
    return json.loads((R / Q).read_bytes()), data[S], data[M]

def validate(q, shops, maps):
    floors = [1101,1102,1201,1202,2001,2002]
    assert len(q['six_rooms']) == 6
    assert [r['floor'] for r in q['six_rooms']] == floors
    assert q['source_only_shop_total'] == 10
    assert q['schema'].startswith('stoneage.integration22.')
    assert q['source_scope'].startswith('LATER_COMMUNITY_MIXED25_')
    assert q['original_shop_create_file_sha256'] == 'd540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b'
    assert q['original_mapwarp_sha256'] == 'b7b50f42efa8e5a3f740d49a8d0c01cbf994d1bb66151b16ff5b5e7c14e7595c'
    assert q['parent_source_sha256']['RAR'] == shops['source_original_mixed25_community_RAR_SHA256']
    bypath = {x['path']:x for x in shops['shop_argument_rows']}
    assert len(bypath) == len(shops['shop_argument_rows'])
    explicit = ranges = 0
    selected = []
    roles = []
    for room in q['six_rooms']:
        floor = str(room['floor'])
        upstream = maps['maps'][floor]
        assert room['original_DAT_sha256'] == upstream['source_sha256']
        assert room['original_DAT_map_geometry'] == upstream['geometry'] == [30,30]
        assert room['verified_TW1_tile_candidate_placements'] == upstream['draw_positions']
        assert room['distinct_TW1_tile_candidate_aliases'] == upstream['unique_draw_aliases']
        assert room['verified_full_combined_RGBA_sha256'] == upstream['frame_RGBA_sha256']['combined']
        assert room['server_vs_client_layers_changed_cells'][0] == 0
        assert room['server_vs_client_layers_changed_cells'][1] in [31,32,60,88]
        assert room['same_source_changed_pairs_only'] == ['client_u16_0__server_u16_2']
        for itemshop in room['shop_configs']:
            role = itemshop['shop_role_original']
            roles.append(role)
            path = itemshop['original_parameter_path']
            orig = bypath[path]
            assert itemshop['original_parameter_sha256'] == orig['source_sha256']
            assert itemshop['raw_buy_rate'] == orig['source_buy_rate_text']
            assert itemshop['raw_sell_rate'] == orig['source_sell_rate_text']
            assert itemshop['source_DAT_three_u16_at_create'][-1] == 49152
            items = itemshop['items']
            assert sorted(x['original_item_id'] for x in items) == sorted(orig['expanded_candidate_IDs_not_proven_runtime'])
            for item in items:
                assert re.fullmatch(r'[0-9a-f]{64}',item['both_original_itemset_rows_sha256'])
                assert re.fullmatch(r'[0-9a-f]{64}',item['verified_TW10_candidate_PNG_sha256'])
                assert re.fullmatch(r'[0-9a-f]{64}',item['verified_TW10_candidate_RGBA_sha256'])
            selected.extend(x['original_item_id'] for x in items)
            if role == 'MATERIAL_SHOP_NAME_ONLY_LIMIT_TYPE_EMPTY':
                ranges += len(itemshop['original_range_expression_tokens'])
                assert floor == '1102'
                assert orig['range_expressions_literal'] == [[11960,11967],[11970,11977]]
                assert orig['explicit_numeric_item_ID_count'] == 0
                assert itemshop['original_ItemList_count'] == 0
                assert itemshop['range_expansion_candidate_count'] == 16
                assert itemshop['original_LimitItemType_literal'] == ''
                assert itemshop['original_LimitItemNo_literal'] == '11960-11967,11970-11977'
                assert all(x['item_id_membership_evidence'] == 'RANGE_INCLUSIVE_CANDIDATE_NOT_NATIVE_PROVEN' for x in items)
            else:
                assert role in ['OFFENCE','DEFENCE','ACCESSORY']
                assert not orig['range_expressions_literal']
                assert not itemshop['original_range_expression_tokens']
                assert orig['explicit_numeric_item_ID_count'] == itemshop['original_ItemList_count'] == len(items)
                assert itemshop['range_expansion_candidate_count'] == 0
                assert itemshop['original_LimitItemType_literal'] == role
                assert all(x['item_id_membership_evidence'] == 'EXPLICIT_ORIGINAL_ITEMLIST_ID' for x in items)
                explicit += len(items)
    assert len(roles) == 10
    assert roles.count('OFFENCE') == roles.count('DEFENCE') == roles.count('ACCESSORY') == 3
    assert roles.count('MATERIAL_SHOP_NAME_ONLY_LIMIT_TYPE_EMPTY') == 1
    assert explicit == 108 and ranges == 2
    metrics = q['metrics']
    assert metrics['rooms'] == 6
    assert metrics['original_ItemShop_CREATEs'] == 10
    assert metrics['literal_original_ItemList_explicit_ID_mentions'] == explicit
    assert metrics['original_ItemList_range_expression_tokens'] == ranges
    assert metrics['candidate_expanded_IDs_from_two_ranges_not_native_verified'] == 16
    assert metrics['different_original_item_IDs'] == len(set(selected)) == 120
    assert metrics['verified_original_itemset_both_table_rows'] == len(selected) == 124
    assert metrics['selected_item_rows_with_same_sha_in_both_tables'] == 124
    assert metrics['source_ready_candidate_item_RD_aliases_distinct'] == len({x['source_image_alias_numeric'] for r in q['six_rooms'] for s in r['shop_configs'] for x in s['items']}) == 89
    assert metrics['original_sprite_NPC_images_newly_decoded'] == 0
    return True

def validate_edges(q):
    edges = q['original_directed_warp_rows']
    assert len(edges) == q['metrics']['original_directed_mapwarp_rows'] == 23
    direct = {(tuple(e['start']),tuple(e['target'])) for e in edges}
    assert len(direct) == len(edges)
    missing = []
    for e in edges:
        r = (tuple(e['target']),tuple(e['start'])) in direct
        assert e['explicit_reverse_in_selected_mapwarp'] is r
        assert e['start'][0] in (1100,1101,1102,1200,1201,1202,2000,2001,2002)
        assert e['target'][0] in (1100,1101,1102,1200,1201,1202,2000,2001,2002)
        assert re.fullmatch(r'[0-9a-f]{64}',e['row_sha256_CP950_line'])
        for point,field in [('start','source_original_DAT_three_u16'),('target','target_original_DAT_three_u16')]:
            cell = e[field]
            if e[point][0] == 1100:
                assert cell is None
            else:
                assert len(cell) == 3 and cell[2] == 49155
        if not r:missing.append(e)
    assert len(missing) == q['metrics']['original_warp_rows_without_explicit_reverse'] == 1
    assert q['metrics']['original_warp_rows_with_explicit_reverse'] == 22
    assert missing[0]['start'] == [1101,16,21]
    assert missing[0]['target'] == [1100,52,72]
    assert q['single_unpaired_source_direction'] == {'start':missing[0]['start'],'target':missing[0]['target'],'source_line':missing[0]['original_line']}
    assert q['exterior_original_DAT_qualifications']['1100']['three_u16_values'] is None
    assert q['exterior_original_DAT_qualifications']['1100']['status'].startswith('NAMED_IN_WARP_BUT_NO_READABLE')
    return True

def validate_bounds(q):
    assert q['Stage_A'] == '7_PARTIAL_2_OPEN'
    assert q['Stage_B_wiki'] == 'GATED'
    assert q['R79'] == 'PAUSED_NON_BLOCKING'
    assert q['overall_percent'] is None
    for flag in ('cross_version_same_official_deployment_proven', 'native_shop_or_warp_transaction_executed',
                 'retail_TW1_candidate_bitmap_is_original_mixed25_runtime_selection_proven',
                 'source_original_proprietary_bytes_published_to_Git'):
        assert q[flag] is False
    assert q['private_OBSERVER']['browser_execution_claimed'] is False
    assert q['private_delivery']['persistent_Library_upload_verified'] is True
    assert q['private_delivery']['Library_roundtrip_whole_zip_SHA256_CRC_verified'] is True
    assert q['private_delivery']['zip_member_count'] == 131
    assert q['private_delivery']['zip_sha256'] == '12239bcab57215586fe4ca755a9503900daaa91be7abdecb6e21621db9d6b92d'
    return True

class Integration22PublicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q,cls.shops,cls.maps=source()

    def test_six_original_map_fingerprints_and_ten_shop_source_parameters(self):
        self.assertTrue(validate(self.q,self.shops,self.maps))

    def test_23_directed_source_warps_without_invented_reverse(self):
        self.assertTrue(validate_edges(self.q))

    def test_unqualified_1100_exterior_not_fabricated(self):
        self.assertTrue(all(e['source_original_DAT_three_u16'] is None for e in self.q['original_directed_warp_rows'] if e['start'][0] == 1100))
        mutated=copy.deepcopy(self.q)
        next(e for e in mutated['original_directed_warp_rows'] if e['start'][0] == 1100)['source_original_DAT_three_u16']=[0,0,49155]
        with self.assertRaises(AssertionError):validate_edges(mutated)

    def test_material_two_range_tokens_not_16_explicit_real_shop_items(self):
        changed=copy.deepcopy(self.q)
        material=next(s for r in changed['six_rooms'] for s in r['shop_configs'] if s['shop_role_original'].startswith('MATERIAL_'))
        material['original_ItemList_count']=16
        with self.assertRaises(AssertionError):validate(changed,self.shops,self.maps)

    def test_original_npc_graphics_alias_and_service_role_not_rewritten(self):
        changed=copy.deepcopy(self.q)
        changed['six_rooms'][0]['shop_configs'][0]['shop_role_original']='DEFENCE'
        with self.assertRaises(AssertionError):validate(changed,self.shops,self.maps)

    def test_source_map_fingerprint_mutation_fails(self):
        changed=copy.deepcopy(self.q)
        changed['six_rooms'][0]['verified_full_combined_RGBA_sha256']='0'*64
        with self.assertRaises(AssertionError):validate(changed,self.shops,self.maps)

    def test_no_native_transaction_or_early_official_same_deployment_claim(self):
        self.assertTrue(validate_bounds(self.q))
        changed=copy.deepcopy(self.q)
        changed['native_shop_or_warp_transaction_executed']=True
        with self.assertRaises(AssertionError):validate_bounds(changed)

if __name__ == '__main__':unittest.main()
