import json
import unittest
from tools.stoneage_pet_high_first_cn50_fusion import TARGET as FUSION_REPORT, verify as verify_fusion
from tools.stoneage_pet_high_first_cn50_sina import REPORT, element_claim, make_report
from tools.stoneage_pet16_lookup import (
    CN50_COMPILED_ALBUM, CLIENT_ALBUM, GRAPHIC_DATASETS, load_catalog, lookup, graphic_trace
)
class PET126RLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=load_catalog()
        cls.rows=cls.c["datasets"][CN50_COMPILED_ALBUM]
    def test_full_named_source_only_catalog(self):
        self.assertEqual(len(self.rows),305)
        self.assertEqual(self.c["metrics"]["source_namespace_row_counts_NOT_species"][CN50_COMPILED_ALBUM],305)
        self.assertEqual(len({row["source_ordinal"] for row in self.rows}),305)
        self.assertTrue(all(row["name_as_written"] and row["graphic_number"] is None for row in self.rows))
        self.assertTrue(all(not row["official_live_release_confirmed"] for row in self.rows))
    def test_ordinary_lookup_preserves_original_region_and_no_graphic_id(self):
        matches=lookup(self.c,"乌力",CN50_COMPILED_ALBUM,limit=30)
        self.assertTrue(matches)
        self.assertEqual(matches[0]["source"],"CN50_THIRD_PARTY_PRESERVED_PC_5_0_CAB")
        self.assertIsNone(matches[0]["graphic_number"])
        complete=lookup(self.c,"乌力",CN50_COMPILED_ALBUM,limit=20,details=True)
        self.assertIsNone(complete[0]["graphic_number"])
        self.assertEqual(complete[0]["TW10_ordinal_based_candidate_SPR_only"],100250)
        self.assertTrue(all(not x["native_same_build_graphic_selector_proven"] for x in complete))
    def test_native_sprite_routes_query_without_singular_graphic_id(self):
        [monkey] = lookup(self.c, "蒙奇", CN50_COMPILED_ALBUM, details=True)
        self.assertEqual(monkey["cn50_native_spr_group_numbers"], [101165, 101289, 101412])
        self.assertIsNone(monkey["graphic_number"])
        self.assertEqual(lookup(self.c, "101412", CN50_COMPILED_ALBUM, details=True), [monkey])
        [zodiac] = lookup(self.c, "葛雷马恩", CN50_COMPILED_ALBUM, details=True)
        self.assertEqual(zodiac["cn50_native_spr_group_numbers"], [101155, 101279])
        self.assertEqual(zodiac["cn50_native_held_pet_spr_group_numbers"], [101155])

    def test_sina_claims_keep_source_and_native_identifiers_separate(self):
        [monkey] = lookup(self.c, "蒙奇", CN50_COMPILED_ALBUM, details=True)
        [sina] = monkey["sina_2003_editorial_same_name_rows"]
        self.assertEqual(sina["printed_catalogue_number"], 238)
        self.assertEqual(sina["reported_elements"], {"fire": 3, "wind": 7})
        self.assertTrue(sina["level_one_acquisition_cell_has_text"])
        self.assertIsNone(monkey["graphic_number"])
        self.assertFalse(monkey["official_live_release_confirmed"])

    def test_sina_homonyms_and_rebirth_forms_remain_distinct(self):
        [pet] = lookup(self.c, "乌力布鲁", CN50_COMPILED_ALBUM, details=True)
        rows = pet["sina_2003_editorial_same_name_rows"]
        self.assertEqual([row["printed_catalogue_number"] for row in rows], [4, 8])
        self.assertNotEqual(rows[0]["reported_elements"], rows[1]["reported_elements"])
        [rebirth_pet] = lookup(self.c, "乌力斯坦", CN50_COMPILED_ALBUM, details=True)
        self.assertEqual([row["rebirth_variant_label"] for row in
                          rebirth_pet["sina_2003_editorial_same_name_rows"]], [False, True])

    def test_sina_receipt_counts_duplicates_and_unmatched_rows(self):
        report = json.loads(REPORT.read_bytes())
        year_card = report["cn30_year_card_announcement"]
        self.assertEqual(make_report(report["rows"], year_card["named_variants"]), report)
        self.assertEqual(year_card["displayed_article_date"], "2002-04-18")
        self.assertEqual(len(year_card["named_variants"]), 4)
        self.assertFalse(year_card["individual_awards_verified"])
        [zodiac] = lookup(self.c, "葛雷马恩", CN50_COMPILED_ALBUM, details=True)
        self.assertEqual(zodiac["cn30_2002_year_card_same_name_announcement"]["main_element"], "wind")
        self.assertFalse(zodiac["official_live_release_confirmed"])
        metrics = report["metrics"]
        self.assertEqual(metrics["compiled_name_slots_with_sina_citation"], 219)
        self.assertEqual(metrics["single_name_links_without_earlier_tw10_link"], 100)
        self.assertEqual(metrics["single_name_links_without_earlier_tw10_link_with_acquisition_cell"], 46)
        self.assertEqual(metrics["unmatched_sina_rows"], 16)
        self.assertEqual(metrics["duplicate_printed_numbers"], [145])
        self.assertEqual(len(metrics["other_number_among_single_name_links"]), 16)
        self.assertEqual(element_claim("火2 风8"), {"fire": 2, "wind": 8})
        with self.assertRaises(ValueError):
            element_claim("火3风8")

    def test_fusion_panels_support_observed_values_only(self):
        report = json.loads(FUSION_REPORT.read_bytes())
        verify_fusion(report)
        self.assertEqual(len(report["records"]), 41)
        self.assertEqual(report["summary"]["exact_ordered_triplets_linked_to_multiple_results"], 18)
        self.assertEqual(report["summary"]["ordered_triplet_lines"], 533)
        self.assertEqual([x["linked_printed_numbers"] for x in report["conflict_examples"]],
                         [[262, 274], [272, 274]])
        [pet] = lookup(self.c, "邦欧里", CN50_COMPILED_ALBUM, details=True)
        panel = pet["sina_2003_fusion_panel"]
        self.assertEqual(panel["displayed_name"], "邦歐里")
        self.assertEqual(panel["printed_number"], 289)
        self.assertEqual(panel["image"]["observed_stats"]["max_hp"], 51)
        self.assertEqual(panel["image"]["observed_elements"], {"earth": 8, "water": 2, "fire": 0, "wind": 0})
        self.assertEqual(pet["source_ordinal"], 345)
        self.assertFalse(pet["official_live_release_confirmed"])
        [gap] = lookup(self.c, "史奈克特", CN50_COMPILED_ALBUM, details=True)
        self.assertIsNone(gap["sina_2003_fusion_panel"])
        self.assertEqual(gap["sina_2003_may_fusion_editorial_entry"]["reported_elements"], {"earth": 7, "wind": 3})
        [variant_name] = lookup(self.c, "贝库尔", CN50_COMPILED_ALBUM, details=True)
        self.assertIsNotNone(variant_name["sina_2003_fusion_panel"])
        self.assertIsNone(variant_name["sina_2003_may_fusion_editorial_entry"])
        [parent] = lookup(self.c, "艾迪希洛", CN50_COMPILED_ALBUM, details=True)
        self.assertIsNone(parent["sina_2003_fusion_panel"])

    def test_tw10_true_graphics_not_overwritten_or_merged(self):
        self.assertNotIn(CN50_COMPILED_ALBUM,GRAPHIC_DATASETS)
        self.assertEqual(len(self.c["datasets"][CLIENT_ALBUM]),124)
        trace=graphic_trace(self.c,100250)
        self.assertEqual(trace["tw10_same_client_album_record"]["name_as_written"],"烏力")
        self.assertIn("tw10_visual",trace["source_separated_matches"])
    def test_name_rows_not_species_or_official_proof(self):
        self.assertTrue(all(row["source_evidence"]=="SAME_CAB_STATIC_NATIVE_SPR_TO_COMPILED_ALBUM_SLOT" for row in self.rows))
        self.assertTrue(any(row["same_carrier_candidate_SPR_present"] for row in self.rows))
if __name__=="__main__":unittest.main()
