"""PET17: exact-source numeric trace preserves all source and species boundaries."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import lookup, graphic_trace

CATALOG_PATH = ROOT / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"


class Pet17GraphicTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    def test_same_number_has_many_distinct_template_identities(self):
        t = graphic_trace(self.c, 100329)
        g = t["source_separated_matches"]
        self.assertEqual(
            [g[k]["matching_original_rows"] for k in (
                "later2016_templates", "later2016_graphics",
                "mixed25_main", "mixed25_alternative", "tw10_visual")],
            [4, 1, 4, 2, 1])
        self.assertEqual(
            [r["template_id"] for r in g["mixed25_main"]["records"]],
            [163, 193, 524, 1214])
        named = [r for r in g["mixed25_main"]["records"] if r["name_as_written"]]
        self.assertEqual([(r["template_id"], r["name_as_written"]) for r in named],
                         [(524, "卡特利奴")])
        self.assertEqual(g["tw10_visual"]["records"][0]["id"], "TW10_SPR:100329")
        self.assertIsNone(t["tw10_original_species_name"])
        self.assertFalse(t["official_pet_species_identity_verified"])
        self.assertFalse(t["same_historical_build_or_server_deployment_verified"])

    def test_original_animation_source_stays_with_original_visual_row(self):
        t = graphic_trace(self.c, 100329)
        visual = t["source_separated_matches"]["tw10_visual"]["records"][0]
        self.assertEqual(visual["source"], "AUTHENTICATED_TW10_RETAIL_SPR_REAL")
        self.assertEqual(visual["source_sequences"], 104)
        self.assertEqual(len(visual["spr_original_segment_sha256"]), 64)
        self.assertIs(visual["official_species_identity"], False)
        self.assertFalse(visual["native_palette_or_timing_verified"])

    def test_alternative_only_is_not_upgraded_to_main_source(self):
        g = graphic_trace(self.c, 100400)["source_separated_matches"]
        self.assertEqual(g["mixed25_main"]["matching_original_rows"], 0)
        self.assertEqual(g["later2016_templates"]["matching_original_rows"], 0)
        self.assertEqual(g["mixed25_alternative"]["matching_original_rows"], 2)
        self.assertEqual(g["tw10_visual"]["matching_original_rows"], 1)

    def test_late_named_row_without_tw10_visual(self):
        g = graphic_trace(self.c, 101737)["source_separated_matches"]
        self.assertEqual(g["tw10_visual"]["matching_original_rows"], 0)
        self.assertEqual(g["mixed25_main"]["records"][0]["name_as_written"], "薩德迪比")

    def test_unknown_number_is_not_an_imagined_pet(self):
        t = graphic_trace(self.c, 123456789)
        self.assertTrue(all(g["matching_original_rows"] == 0
                            for g in t["source_separated_matches"].values()))
        self.assertIsNone(t["tw10_original_species_name"])
        self.assertTrue(t["official_JP_CN_web_ordinal_or_image_URL_not_mappable_to_graphic"])

    def test_limit_never_changes_total_evidence_and_retains_original_fields(self):
        g = graphic_trace(self.c, 100329, limit=1)["source_separated_matches"]
        self.assertEqual(g["mixed25_main"]["matching_original_rows"], 4)
        self.assertEqual(g["mixed25_main"]["returned_rows"], 1)
        self.assertTrue(g["mixed25_main"]["truncated"])
        self.assertEqual(g["mixed25_main"]["records"][0]["original_row"], 163)
        self.assertIn("original_fields_sha256", g["mixed25_main"]["records"][0])

    def test_full_row_lookup_is_source_separated_and_web_pages_not_joined(self):
        detail = lookup(self.c, "卡特利奴", "mixed25_main", details=True)
        self.assertEqual(len(detail), 1)
        self.assertEqual(detail[0]["source"], "MIXED25_MAIN")
        self.assertEqual(detail[0]["graphic_number"], 100329)
        self.assertIn("stats_original_literals", detail[0])
        self.assertIn("original_skill_slot_ids", detail[0])
        web = lookup(self.c, "朱利洛斯", "cn_official_web", details=True)
        self.assertEqual(len(web), 1)
        self.assertIsNone(web[0]["actual_client_species_id"])
        self.assertFalse("graphic_number" in web[0])

    def test_invalid_graphic_numbers_rejected(self):
        for bad in (0, -1, True, "100329", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                graphic_trace(self.c, bad)


if __name__ == "__main__":
    unittest.main()
