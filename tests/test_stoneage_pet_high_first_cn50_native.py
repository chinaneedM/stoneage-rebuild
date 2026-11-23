from collections import Counter
import unittest

from tools.stoneage_pet_high_first_cn50_native import (
    TARGET, album_ordinal, build_catalog, read_inputs, render,
)


class CN50NativeAlbum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_catalog(*read_inputs())
        cls.by_name = {row["compiled_name"]: row for row in cls.result["records"]}

    def test_all_named_slots_and_earlier_link_not_required(self):
        self.assertEqual(render(self.result), TARGET.read_text(encoding="utf-8"))
        counts = self.result["metrics"]
        self.assertEqual(counts["named_album_slots"], 305)
        self.assertEqual(counts["old_formula_agrees"], 124)
        self.assertEqual(counts["old_formula_present_but_does_not_select_this_slot"], 66)
        self.assertEqual(counts["old_formula_absent_now_mapped"], 115)
        self.assertEqual(counts["action_object_path_named_spr_groups"], 594)
        self.assertEqual(counts["held_pet_path_named_spr_groups"], 590)
        self.assertEqual(counts["named_slots_with_multiple_spr_groups"], 250)
        self.assertEqual(Counter(row["earlier_tw10_relation"] for row in self.by_name.values()), {
            "EARLY_TW10_PORTRAIT_FULL_RD_SHA_EXACT": 120,
            "EARLY_TW10_NAMED_SPR_PORTRAIT_ABSENT": 4,
            "EARLY_TW10_NOT_LINKED": 181,
        })
        self.assertTrue(all(row["spr_groups"] for row in self.by_name.values()))

    def test_piecewise_cutovers_special_case_and_held_pet_exclusion(self):
        cases = {100249: None, 100250: 0, 100430: 180, 100431: None,
                 100820: 181, 100885: 246, 101176: 305, 101177: 293,
                 101178: 285, 101179: 286, 101180: 286}
        for graphic, slot in cases.items():
            with self.subTest(graphic=graphic):
                self.assertEqual(album_ordinal(graphic), slot)
                self.assertEqual(album_ordinal(graphic, held_pet=True), slot)
        self.assertEqual(album_ordinal(101279), 284)
        self.assertIsNone(album_ordinal(101279, held_pet=True))
        self.assertEqual(album_ordinal(101155, held_pet=True), 284)

    def test_original_sprite_rows_are_multiple_and_have_frame_metadata(self):
        groups = self.by_name["蒙奇"]["spr_groups"]
        self.assertEqual([group["spr_group"] for group in groups], [101165, 101289, 101412])
        self.assertEqual([group["animation_header_count"] for group in groups], [104, 1, 56])
        self.assertTrue(all(group["frame_record_count"] for group in groups))
        self.assertEqual(len({group["sha256"] for group in groups}), 3)
        self.assertFalse(self.result["evidence_boundaries"]["single_canonical_spr_group_per_name_established"])
        self.assertFalse(self.result["evidence_boundaries"]["official_retail_pressing_or_live_release_verified"])

    def test_complete_adrn_order_has_four_dual_images(self):
        counts = self.result["metrics"]
        self.assertEqual(counts["portrait_adrn_original_records_scanned"], 303197)
        self.assertEqual(counts["portrait_alias_adrn_records"], 309)
        self.assertEqual(counts["portrait_aliases_with_multiple_records"], 4)
        lokes = self.by_name["洛克斯"]
        self.assertEqual(lokes["portrait_bitmap_numbers_in_file_order"], [126066, 126222])
        self.assertEqual(lokes["portrait_lookup_after_ordered_load"], 126222)
        self.assertFalse(self.result["evidence_boundaries"]["portrait_bitmap_observed_in_original_runtime"])


if __name__ == "__main__":
    unittest.main()
