"""Public, provenance-only contract: ITEM02 bounded original source RD terminal zero.
No proprietary art, itemset tables or private PNGs are used in CI.
"""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'research/recovered/STONEAGE-ITEM02-FOUR-TW10-RD-BOUNDED-PREFIX-R1.json'
PARENT = ROOT / 'research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-ORIGINAL-ITEMSETS-AND-TW1-RD-SUMMARY-R1.json'
PARENT_BLOB = '976a5ae0de6538d5d2edca74461f1e5a51bd710b'
TARGETS = (24077, 24137, 24138, 24140)
PHYSICALS = (6722, 6726, 6727, 6729)
EXPECTED_RD_SHA = (
 '49802c55808724dc13b46b67ab45122f4c1cf323f460721cb75479298a2f0829',
 'dee4c4fd59b3d0c36861b71215fa0e49ed398d894f10eaa99e5a223c0ce22be9',
 '8d013a88525c5f6cbb6023ef5d0c57989f1cc7c99c46d2aaebb9b045004ed1b7',
 '6a2e472dfb9d5c08dfdb0176345c7b2935b0fe900f3fffea98f53674b486977e'
)


def require_exact_terminal_zero(row):
    return (
        row['source_terminal_control_is_last_byte'] is True
        and row['terminal_source_control_hex'] == 'c2'
        and row['terminal_source_op_kind'] == 'zero'
        and row['terminal_source_op_emits'] == 2
        and row['pixels_before_terminal_op'] == row['expected_canvas_pixel_count'] - 1
        and row['original_decoded_pixel_count_including_extra_zero'] == row['expected_canvas_pixel_count'] + 1
        and row['terminal_overshoot_pixels'] == 1
        and row['exact_terminal_op_offset'] == row['original_RD_byte_length'] - 1
        and row['final_two_decoded_pixels_zero'] is True
        and row['whole_source_RLE_consumed'] is True
        and row['independent_decoder_A_B_all_bytes_equal'] is True
        and row['strict_original_pixel_count_is_valid'] is False
        and row['bounded_source_prefix_supported'] is True
        and row['original_commercial_native_decoder_accepts_overshoot_proven'] is False
    )


class TestItem02BoundedOriginalRD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(RECEIPT.read_text('utf-8'))
        raw = PARENT.read_bytes()
        cls.parent_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        cls.parent = json.loads(raw)
        cls.rows = cls.d['four_original_RD_individual_evidence']

    def test_01_parent_original_receipt_is_immutable(self):
        self.assertEqual(self.parent_blob, PARENT_BLOB)
        s=self.parent['original_TW1_retail_RD_pixel_source']
        self.assertEqual(s['RD_decode_failed_aliases'], list(TARGETS))
        self.assertEqual((s['RD_fully_decoded'],s['RD_decode_failed'],s['ADRN_not_found']), (832,4,831))

    def test_02_original_authenticated_carrier_scope(self):
        s=self.d['source_identity']
        self.assertEqual(s['source_zip_size'],372626292)
        self.assertEqual(s['source_zip_sha256'],'3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24')
        self.assertEqual(s['original_zip_verified_member_crc_count'],379)
        self.assertEqual(s['original_source_members']['real_1.bin']['bytes'],315842228)
        self.assertEqual(s['original_source_members']['adrn_1.bin']['bytes'],10079680)

    def test_03_alias_and_physical_bitmap_namespaces_separate(self):
        self.assertEqual([r['item_original_image_alias'] for r in self.rows],list(TARGETS))
        self.assertEqual([r['physical_original_ADRN_bitmap_number'] for r in self.rows],list(PHYSICALS))
        self.assertEqual([r['original_ADRN_record_index'] for r in self.rows],list(PHYSICALS))
        self.assertTrue(all(r['original_RD_flag']==1 for r in self.rows))
        self.assertEqual(len(set(r['original_RD_SHA256'] for r in self.rows)),4)

    def test_04_preserve_exact_whole_original_rd_sha(self):
        self.assertEqual(tuple(r['original_RD_SHA256'] for r in self.rows),EXPECTED_RD_SHA)
        self.assertEqual([r['original_RD_byte_length'] for r in self.rows],[449,481,472,511])
        self.assertEqual(self.d['summary']['original_RD_source_bytes_read'],1913)

    def test_05_geometry_and_total_bounded_canvas(self):
        self.assertEqual([(r['original_RD_width'],r['original_RD_height']) for r in self.rows],[(28,28)]*3+[(40,30)])
        self.assertEqual([r['expected_canvas_pixel_count'] for r in self.rows],[784,784,784,1200])
        self.assertEqual(self.d['summary']['bounded_source_pixel_positions'],3552)

    def test_06_every_original_overflow_exact_terminal_c2(self):
        self.assertTrue(all(require_exact_terminal_zero(r) for r in self.rows))
        self.assertEqual(self.d['summary']['source_RLE_strict_pixel_count_success'],0)
        self.assertEqual(self.d['summary']['bounded_original_canvas_prefix_qualified'],4)
        self.assertEqual(self.d['summary']['two_decoder_bytewise_agreements'],4)

    def test_07_arbitrary_clipping_not_generalized(self):
        row=dict(self.rows[0]); row['terminal_source_control_hex']='c3'
        self.assertFalse(require_exact_terminal_zero(row))
        row=dict(self.rows[0]); row['terminal_overshoot_pixels']=3
        self.assertFalse(require_exact_terminal_zero(row))
        row=dict(self.rows[0]); row['whole_source_RLE_consumed']=False
        self.assertFalse(require_exact_terminal_zero(row))
        row=dict(self.rows[0]); row['final_two_decoded_pixels_zero']=False
        self.assertFalse(require_exact_terminal_zero(row))

    def test_08_source_prefix_sha256_conservation(self):
        dig=lambda field:hashlib.sha256(''.join(r[field] for r in self.rows).encode()).hexdigest()
        self.assertEqual(self.d['summary']['all_four_exact_original_raw_RD_SHA256_list_digest'],dig('original_RD_SHA256'))
        self.assertEqual(self.d['summary']['all_four_bounded_canvas_SHA256_list_digest'],dig('bounded_source_canvas_prefix_SHA256'))
        self.assertTrue(all(len(r['bounded_source_canvas_prefix_SHA256'])==64 for r in self.rows))

    def test_09_historical_failure_and_version_limits_preserved(self):
        p=self.d['earlier_source_bound_context'];n=self.d['negative_boundaries']
        self.assertEqual(p['earlier_four_decode_failed_image_aliases'],list(TARGETS))
        self.assertEqual(p['previous_source_strict_RD_decoded'],832)
        self.assertEqual(p['previous_retail_index_aliases_missing'],831)
        self.assertTrue(p['historical_failure_not_overwritten'])
        self.assertTrue(p['community_itemsets_not_authenticated_as_TW10_same_deployment'])
        self.assertFalse(n['strict_RD_decode_result_reclassified_as_success'])
        self.assertFalse(n['native_original_runtime_executed'])
        self.assertFalse(n['community_itemset_and_TW1_retail_same_server_proven'])

    def test_10_private_original_pixels_do_not_enter_git(self):
        p=self.d['private_observation'];n=self.d['negative_boundaries']
        self.assertEqual(p['source_original_png_sheet_count'],2)
        self.assertEqual(p['modern_candidate_palettes'],['Palet_0.sap','Palet_1.sap'])
        self.assertFalse(p['original_source_pixels_publicly_committed'])
        self.assertFalse(n['source_RD_pixels_published'])
        self.assertFalse(n['native_original_color_selection_proven'])
        self.assertEqual(n['stage_a'],'7_PARTIAL_2_OPEN')
        self.assertEqual(n['stage_b_wiki'],'GATED')
        self.assertEqual(n['r79'],'PAUSED_NON_BLOCKING')
        self.assertIsNone(n['overall_restoration_percent'])

if __name__=='__main__':
    unittest.main()