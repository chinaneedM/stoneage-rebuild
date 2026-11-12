"""Public source-bounded assertions. These do not read proprietary original files."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

PATH = (Path(__file__).resolve().parents[1] / 'research/recovered' /
        'STONEAGE-INTEGRATION84-JBA-ITEM-SOURCE-R1.json')
DATA = json.loads(PATH.read_text(encoding='utf-8'))
SHA = re.compile(r'^[0-9a-f]{64}$')


class TestIntegration84JBASource(unittest.TestCase):
    def test_schema_and_retained_source_custody(self):
        self.assertEqual(DATA['schema'], 'stoneage.integration84.jba_original_npc_item_2d_source_r1')
        p = DATA['provenance']
        self.assertEqual(p['npc_archive_member_count'], 2205)
        self.assertEqual(p['item_archive_member_count'], 838)
        self.assertEqual(p['npc_archive_sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(p['item_archive_sha256'], 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')
        self.assertEqual(p['create_sha256'], 'ac3eb1246f29158d6851f78d2a01320aaa9272d34457aee8a4b694982168775c')

    def test_nine_source_creates_bounded_to_floor(self):
        r = DATA['static_create_records']
        self.assertEqual(len(r), 9)
        self.assertEqual([x['index_zero_based'] for x in r], list(range(2, 11)))
        self.assertEqual({x['floorid'] for x in r}, {20712})
        self.assertEqual([x['borncorner'][:2] for x in r],
                         [[45,32],[45,36],[25,4],[22,4],[20,4],[18,4],[17,4],[45,15],[45,19]])

    def test_original_create_offset_and_sha_shape(self):
        r = DATA['static_create_records']
        self.assertTrue(all(0 <= x['raw_byte_start_inclusive'] < x['raw_byte_end_exclusive']
                            <= DATA['provenance']['create_bytes'] for x in r))
        self.assertEqual(len({x['raw_byte_start_inclusive'] for x in r}), 9)
        self.assertTrue(all(SHA.fullmatch(x['source_block_sha256']) for x in r))

    def test_npc_functions_not_equated_with_character_count(self):
        r = DATA['static_create_records']
        funcs = [x['enemy_function_name'] for x in r]
        self.assertEqual(funcs.count('npcgen_shop'), 4)
        self.assertEqual(funcs.count('npcgen_petskillshop'), 2)
        self.assertEqual(funcs.count('npcgen_mugon'), 2)
        self.assertEqual(funcs.count('npcgen_winhealer'), 1)
        self.assertTrue(all(x['original_createnum']==1 for x in r))

    def test_argument_join_exact_and_unique(self):
        a = DATA['argument_files'];r=DATA['static_create_records']
        refs={x['argument_file_path'] for x in r if x['argument_file_path']}
        self.assertEqual(refs, {x['path'] for x in a})
        self.assertEqual(len(refs), 6)
        self.assertTrue(all(SHA.fullmatch(x['sha256']) and x['bytes']>0 for x in a))

    def test_shop_argument_field_roles(self):
        a=[x for x in DATA['argument_files'] if x['argument_kind']=='shop']
        self.assertEqual(len(a),4)
        self.assertEqual(sum(bool(x['line_key_ItemList_exists']) for x in a),3)
        self.assertEqual(sorted(len(x['literal_line_key_item_ids']) for x in a),[0,13,15,16])
        self.assertEqual(sum(len(x['literal_line_key_item_ids']) for x in a),44)

    def test_embedded_itemlist_must_remain_negative(self):
        broken=next(x for x in DATA['argument_files'] if x['path'].endswith('ss_20712_25_4'))
        self.assertFalse(broken['line_key_ItemList_exists'])
        self.assertTrue(broken['embedded_ItemList_substring_in_other_field'])
        self.assertEqual(broken['literal_line_key_item_ids'],[])
        self.assertEqual(len(broken['embedded_only_candidate_ids_NOT_shop_offer_evidence']),16)
        self.assertEqual(broken['literal_LimitItemType'],'ACCESSORY')

    def test_shop_rates_are_literal_only(self):
        d={x['path'].split('/')[-1]:x for x in DATA['argument_files'] if x['argument_kind']=='shop'}
        self.assertEqual((d['ss_20712_45_19']['literal_buy_rate'],d['ss_20712_45_19']['literal_sell_rate']),('2.0','0.2'))
        for k in ('ss_20712_45_32','ss_20712_45_36','ss_20712_25_4'):
            self.assertEqual((d[k]['literal_buy_rate'],d[k]['literal_sell_rate']),('1.0','0.15'))

    def test_skill_shops_remain_distinct_from_item_offers(self):
        a=[x for x in DATA['argument_files'] if x['argument_kind']=='petskillshop']
        self.assertEqual(sorted(len(x['pet_skill_line_key_ids']) for x in a),[9,12])
        self.assertEqual(sum(len(x['pet_skill_line_key_ids']) for x in a),21)
        self.assertTrue(all(not x['line_key_ItemList_exists'] for x in a))
        self.assertTrue(all(x['literal_skill_rate']=='1.0' for x in a))

    def test_items_distinct_and_source_role_preserved(self):
        r=DATA['item_rows']; self.assertEqual(len(r),60)
        self.assertEqual(len({x['id'] for x in r}),60)
        self.assertEqual(sum(x['original_line_itemlist'] for x in r),44)
        self.assertEqual(sum(x['original_embedded_only_NOT_confirmed_itemlist'] for x in r),16)
        self.assertTrue(all(x['original_line_itemlist'] != x['original_embedded_only_NOT_confirmed_itemlist'] for x in r))

    def test_item_original_94_column_line_custody(self):
        for x in DATA['item_rows']:
            self.assertTrue(x['source_94_column_original_line_sha256'])
            self.assertTrue(all(SHA.fullmatch(z) for z in x['source_94_column_original_line_sha256'].values()))
            self.assertTrue(all(isinstance(z,int) for z in x['candidate_item_image_alias_by_source'].values()))

    def test_cross_carrier_pixel_aliases_verified_no_invention(self):
        refs={int(a) for x in DATA['item_rows'] for a,v in x['original_TW1_2d_candidate_by_alias'].items() if 'original_RD_SHA256' in v}
        self.assertEqual(len(refs),54)
        self.assertTrue(all(any('original_RD_SHA256' in v for v in x['original_TW1_2d_candidate_by_alias'].values()) for x in DATA['item_rows']))
        self.assertTrue(all(SHA.fullmatch(v['candidate_PNG_SHA256']) for x in DATA['item_rows'] for v in x['original_TW1_2d_candidate_by_alias'].values() if 'candidate_PNG_SHA256' in v))
        self.assertEqual(DATA['counts']['TW1_original_RD_newly_decoded'],0)

    def test_public_counts_replay(self):
        c=DATA['counts']
        self.assertEqual(c['floor_20712_original_create_records'],len(DATA['static_create_records']))
        self.assertEqual(c['distinct_original_item_candidate_ids'],len(DATA['item_rows']))
        self.assertEqual(c['item_candidates_with_at_least_one_tw1_png'],60)
        self.assertEqual(c['item_candidates_without_tw1_png'],0)

    def test_only_three_original_shop_itemlists_are_known(self):
        offers={id for a in DATA['argument_files'] for id in a['literal_line_key_item_ids']}
        raw_text={id for a in DATA['argument_files'] for id in a['embedded_only_candidate_ids_NOT_shop_offer_evidence']}
        self.assertEqual(len(offers),44);self.assertEqual(len(raw_text),16)
        self.assertTrue(offers.isdisjoint(raw_text))
        self.assertEqual(offers|raw_text,{x['id'] for x in DATA['item_rows']})

    def test_boundary_record_does_not_claim_original_game_execution(self):
        b=' '.join(DATA['boundaries'])
        self.assertIn('No historical JSS/TW1 official same-deployment',b)
        self.assertIn('zero newly decoded original RD',b)
        self.assertIn('not a line-key ItemList',b)


if __name__=='__main__':
    unittest.main()
