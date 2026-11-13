"""INTEGRATION98: qualified cross-carrier original item-identity / original RD provenance.

Only public, rights-safe derived metadata is tested in GitHub.  Private original
itemset source text and TW1 bitmap are verified separately, never fetched by CI.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research' / 'recovered'
DATA_PATH = REC / 'STONEAGE-INTEGRATION98-FOUR-MANOR-EIGHT-ORIGINAL-ITEM-2D-CANDIDATE-R1.json'
ITEM_PATH = REC / 'item-module-01' / 'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-07-R1.json'
GATE_PATH = REC / 'STONEAGE-INTEGRATION97-FOUR-MANOR-SOURCE-GATES-SHOPS-R1.json'


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\x00' + raw).hexdigest()


class SourceBoundEightItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA_PATH.read_bytes())
        cls.old_item = json.loads(ITEM_PATH.read_bytes())
        cls.old_gate = json.loads(GATE_PATH.read_bytes())
        cls.rows = cls.data['source_rows']

    def test_preserved_prior_public_git_identity(self):
        b = self.data['prior_public_git_anchors']
        self.assertEqual(git_blob(ITEM_PATH.read_bytes()), b['ITEM01_shard_07_git_blob'])
        self.assertEqual(git_blob(GATE_PATH.read_bytes()), b['INTEGRATION97_sourced_gate_catalog_git_blob'])
        self.assertEqual(b['CURRENT_state_git_blob_must_remain'], 'c89e0e33537990aa2132b47c40fef49a985a935c')

    def test_eight_exact_source_ids_four_pairs(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(sorted(x['item_id'] for x in self.rows),
                         [19001,19002,19003,19004,19330,19331,19332,19333])
        self.assertEqual({x['manor_group'] for x in self.rows}, {1,2,3,4})

    def test_each_item_is_a_distinct_old_original_row_sha(self):
        shas=[x['original_complete_row_sha256_same_in_both_saved_tables'] for x in self.rows]
        self.assertEqual(len(set(shas)),8)
        self.assertTrue(all(len(v)==64 and all(c in '0123456789abcdef' for c in v) for v in shas))

    def test_exact_full_old_source_item_shard_replay(self):
        cols = self.old_item['column_labels']
        self.assertEqual(cols[:6], [
            'item_id', 'source_a_complete_row_sha256_if_present',
            'source_b_complete_row_sha256','source_a_image_no_if_present',
            'source_b_image_no','source_b_cost_raw'])
        indexed = {row[0]:row for row in self.old_item['rows']}
        for x in self.rows:
            with self.subTest(id=x['item_id']):
                row=indexed[x['item_id']]
                self.assertEqual(row[1],row[2])
                self.assertEqual(row[2],x['original_complete_row_sha256_same_in_both_saved_tables'])
                self.assertEqual(row[3:5],[24176,24176])
                self.assertEqual(row[5],x['source_price_field_raw'])
                self.assertEqual(row[6:8],[x['source_type_raw'],x['source_level_raw']])
                self.assertEqual(row[8:10], ['REAL_RD_DECODED_CROSS_CARRIER']*2)
                self.assertEqual(row[10],[])
                self.assertTrue(x['same_source_row_verified_both_preserved_itemset_tables'])

    def test_four_prior_guard_and_shop_item_links_replay(self):
        gate=self.old_gate['family_pass_invitation_crossfile_bridge']
        for family in range(1,5):
            old=gate[str(family)]
            xs=[x for x in self.rows if x['manor_group']==family]
            inv=next(x for x in xs if x['role_from_prior_same_carrier_script']=='invitation')
            pas=next(x for x in xs if x['role_from_prior_same_carrier_script']=='shop_pass')
            self.assertEqual(old['invitation_item_ID_literal'], inv['item_id'])
            self.assertEqual(old['pass_item_ID_literal'],pas['item_id'])
            self.assertTrue(old['prior_shop_ItemList_same_pass_ID'])
            self.assertEqual(old['MANOR_literal_index'], family-1)

    def test_price_type_fields_and_zero_price_not_native_free_sale(self):
        for x in self.rows:
            expected='0' if x['role_from_prior_same_carrier_script']=='invitation' else '1000'
            self.assertEqual(x['source_price_field_raw'], expected)
            self.assertEqual(x['source_type_raw'], '16')
            self.assertEqual(x['source_level_raw'], '0')
        self.assertTrue(self.data['negative_evidence_guards']['price_field_0_or_1000_is_not_proven_actual_store_transaction'])

    def test_one_original_bitmap_alias_not_eight_artifacts(self):
        self.assertEqual({x['source_itemset_image_number_alias'] for x in self.rows},{24176})
        self.assertEqual(self.data['counts']['different_original_itemset_art_alias_count'],1)
        self.assertTrue(self.data['negative_evidence_guards']['eight_item_IDs_do_not_mean_eight_distinct_images'])
        self.assertEqual(self.data['counts']['original_TW1_RD_source_graphics_decoded_new_this_unit'],0)

    def test_actual_private_pixel_custody_is_explicit_without_public_pixel(self):
        v=self.data['original_TW1_retail_private_single_2d_source']
        self.assertEqual(v['original_bitmap_dimensions'], [52,44])
        self.assertEqual(v['physical_bitmap_number'],6840)
        self.assertEqual(v['original_ADRN_record_unique_matches'],1)
        self.assertEqual(v['original_ADRN_record_sha256'], 'f13c5fe8ea0a87ae9f56a0658959b169c66f50b3436cb12fdd0455060b572c00')
        self.assertEqual(v['source_original_RD_SHA256'], 'cddd1a18dec031cec9d9d128da11f41500d8d101663ab1100eb17f066b9d0146')
        self.assertEqual(v['actual_private_PNG_SHA256_verified_now'],v['candidate_PNG_SHA256'])
        self.assertEqual(v['actual_decoded_RGBA_SHA256_verified_now'],v['candidate_RGBA_SHA256'])
        self.assertEqual(v['actual_private_PNG_bytes_read'],2786)
        self.assertTrue(v['not_original_native_UI'])

    def test_archive_provenance_is_bounded_not_claiming_raw_reread(self):
        src=self.data['private_source_custody']
        self.assertEqual(src['item01_observer_archive_bytes'],5868386)
        self.assertEqual(src['item01_observer_archive_SHA256'], 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')
        self.assertEqual(src['zip_members_and_crc_success'],'838/838')
        self.assertFalse(src['original_two_itemset_raw_bytes_directly_re_read_this_unit'])
        self.assertFalse(src['parent_mixed25_original_RAR_re_read_this_unit'])
        self.assertTrue(src['actual_private_original_png_candidate_re_read_this_unit'])

    def test_no_gameplay_same_deployment_or_original_assets_public(self):
        neg=self.data['negative_evidence_guards']
        for k in ['original_game_item_rendered_or_inventory_shown',
                  'same_historical_official_deployment_of_mixed25_item_and_TW1_pixels',
                  'native_manor_pass_permission_or_item_consumption_executed',
                  'unqualified_early_mainland_182_or_JSS1999_identity_promoted',
                  'proprietary_bitmap_or_original_item_text_in_public_Git']:
            self.assertIs(neg[k],False,k)
        self.assertEqual(neg['Stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertEqual(neg['Stage_B'],'GATED')
        self.assertEqual(neg['wiki'],'GATED')
        self.assertEqual(neg['R79'],'PAUSED_NON_BLOCKING')
        self.assertIsNone(neg['overall_percent'])

if __name__ == '__main__':
    unittest.main()
