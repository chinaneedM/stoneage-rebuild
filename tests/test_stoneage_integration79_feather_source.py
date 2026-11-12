"""Source-derived-only public metadata guards; never reads proprietary original bytes."""
import json
import re
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-INTEGRATION79-FEATHER-SHOP-ORIGINAL-NPC-ITEM-PIXEL-R1.json'


class OriginalFeatherSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding='utf8'))
        cls.shops = cls.data['shops']
        cls.items = cls.data['item_rows']
        cls.by_id = {x['item_id']: x for x in cls.items}

    def test_01_schema_source_provenance(self):
        self.assertEqual(self.data['schema'], 'stoneage.integration79.feather_shops_original_source_bound.v1')
        self.assertIn('mixed25', self.data['source_scope'])
        self.assertIn('TW1', self.data['source_scope'])

    def test_02_original_archive_crc_and_sizes(self):
        expected = {'npc_mixed25': (995176, 2205), 'item01_prior_catalog': (5868386, 838), 'TW1_prior_motions': (11182099, 4154)}
        self.assertEqual(set(self.data['raw_archive_custody']), set(expected))
        for k,(size,n) in expected.items():
            a=self.data['raw_archive_custody'][k]
            self.assertEqual((a['size_bytes'],a['zip_members'],a['all_crc_pass']), (size,n,True))
            self.assertRegex(a['sha256'], r'^[a-f0-9]{64}$')

    def test_03_exact_create_block_count_offsets(self):
        self.assertEqual(len(self.shops), 13)
        self.assertEqual(self.data['npc_creation_file']['total_active_brace_blocks'], 13)
        self.assertEqual([s['source_index'] for s in self.shops], list(range(1,14)))
        self.assertEqual(len({(s['byte_offset_start'],s['byte_offset_end_exclusive']) for s in self.shops}), 13)
        for s in self.shops:
            self.assertLess(s['byte_offset_start'],s['byte_offset_end_exclusive'])
            self.assertRegex(s['source_block_sha256'],r'^[0-9a-f]{64}$')

    def test_04_all_parameter_refs_direct_and_distinct(self):
        self.assertEqual(len({s['linked_parameter_file'] for s in self.shops}),13)
        for s in self.shops:
            self.assertTrue(s['linked_parameter_file'].startswith('npc/genout/ss_'))
            self.assertGreater(s['linked_parameter_size'],100)
            self.assertRegex(s['linked_parameter_sha256'], r'^[0-9a-f]{64}$')
            self.assertEqual((s['buy_rate_literal'],s['sell_rate_literal']),('1.0','0.2'))

    def test_05_npc_floors_and_graphic_category(self):
        self.assertEqual({s['floorid'] for s in self.shops}, {1000,2000,3000,4000,5001,3400,5106,1102,3100,1400,3300,1302,3209})
        self.assertEqual({g:sum(s['graphicname']==g for s in self.shops) for g in [16067,16218,16300]}, {16067:5,16218:1,16300:7})

    def test_06_all_twenty_eight_item_links(self):
        ids=sorted({i for s in self.shops for i in s['stock_ids_expanded_candidate']})
        self.assertEqual(ids,sorted(self.by_id))
        self.assertEqual(len(ids),28)
        self.assertEqual(self.data['unique_stock_count'],28)
        self.assertTrue(all(len(s['stock_ids_expanded_candidate'])>=1 for s in self.shops))

    def test_07_shop_groups_and_one_necklace(self):
        self.assertEqual(sum(s['source_stock_literal']=='13041-13053,13088-13092' for s in self.shops),4)
        self.assertEqual(len([s for s in self.shops if s['stock_ids_expanded_candidate']==[13065,18546]]),1)
        self.assertEqual(sum(18546 in s['stock_ids_expanded_candidate'] for s in self.shops),1)
        self.assertEqual(self.by_id[18546]['source_type'],'SILENCE_ACCESSORY_SOURCE_TEXT')

    def test_08_all_original_item_source_rows_sha_preserved(self):
        for item in self.items:
            v=item['sources']
            self.assertEqual(set(v),{'itemset.txt','itemset0710.txt'})
            for t in v.values():
                self.assertGreater(t['row_1based'],0)
                self.assertRegex(t['row_sha256'],r'^[0-9a-f]{64}$')
        self.assertEqual(self.data['source_qualifications']['itemset_original_row_SHA_verified_count'],56)

    def test_09_exact_two_table_bitmap_differences(self):
        delta=[x for x in self.items if x['original_two_table_row_class']!='IDENTICAL_RAW_LINE']
        self.assertEqual([x['item_id'] for x in delta],list(range(13088,13093)))
        self.assertTrue(all(x['row_difference_columns_zero_based']==[17] for x in delta))
        self.assertTrue(all(x['sources']['itemset.txt']['alias_or_source_imagenumber']==24076 for x in delta))
        self.assertEqual([x['sources']['itemset0710.txt']['alias_or_source_imagenumber'] for x in delta],[24381,24378,24379,24377,24380])
        self.assertEqual(self.data['source_qualifications']['itemset_identical_full_original_row_count'],23)

    def test_10_warp_vs_accessory_and_preserved_target(self):
        warp=[x for x in self.items if x['sources']['itemset.txt']['warp_numeric_4tuple']]
        self.assertEqual(len(warp),27)
        self.assertIsNone(self.by_id[18546]['sources']['itemset.txt']['warp_numeric_4tuple'])
        self.assertEqual(self.by_id[13041]['sources']['itemset.txt']['warp_numeric_4tuple'], {'flag_0_or_1_literal':1,'floorid':1000,'x':92,'y':99})
        self.assertEqual(self.by_id[13092]['sources']['itemset.txt']['warp_numeric_4tuple'], {'flag_0_or_1_literal':0,'floorid':30502,'x':44,'y':41})
        for x in warp:
            self.assertEqual(x['sources']['itemset.txt']['warp_numeric_4tuple'],x['sources']['itemset0710.txt']['warp_numeric_4tuple'])

    def test_11_three_retained_original_candidates_and_missing_boundaries(self):
        pix=self.data['previously_retained_original_TW1_png_candidates']
        self.assertEqual([x['alias_numeric_candidate'] for x in pix],[24076,22030,16300])
        self.assertEqual([(x['width'],x['height']) for x in pix],[(32,26),(32,27),(52,70)])
        self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}',x['retained_png_sha256']) for x in pix))
        self.assertFalse(self.data['source_qualifications']['TW1_motion_zip_has_npc_image_16067'])
        self.assertFalse(self.data['source_qualifications']['TW1_motion_zip_has_npc_image_16218'])

    def test_12_no_inferred_runtime_or_new_art(self):
        neg=self.data['negative_evidence_boundary']
        for k in ['official_same_runtime_deployment_proven','historical_shop_purchases_or_item_use_native_playback_proven','static_warp_targets_are_actual_reached_locations_proven','original_native_client_image_appearance_proven','public_original_image_or_script_bytes']:
            self.assertIs(neg[k],False)
        self.assertEqual((neg['new_RD_decoded_this_round'],neg['new_unique_original_artwork_this_round']),(0,0))
        self.assertEqual((neg['stage_a_partial'],neg['stage_a_open'],neg['stage_b'],neg['wiki'],neg['R79'],neg['overall_percent']),(7,2,'GATED','GATED','PAUSED_NON_BLOCKING',None))
        self.assertEqual(self.data['historical_current_unchanged']['git_blob_sha'],'c89e0e33537990aa2132b47c40fef49a985a935c')


if __name__ == '__main__':unittest.main()
