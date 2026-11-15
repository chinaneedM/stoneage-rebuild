"""PET18 source-bounded capture item and skill links; no native execution claims."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import capture_trace

R = ROOT / "research/recovered"


class Pet18CaptureSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = json.loads((R / "STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json").read_text(encoding="utf-8"))
        cls.p13 = json.loads((R / "STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json").read_text(encoding="utf-8"))

    def test_exact_four_field_source_join_for_10_petflag1(self):
        traces = [capture_trace(self.c, self.p13, x["original_template_numeric_ID"])
                  for x in self.p13["templates"]]
        self.assertEqual(len(traces), 11)
        found = [x for x in traces if x["pet16_exact_same_source_petflag1_row"]]
        self.assertEqual(len(found), 10)
        for x in found:
            a = x["pet13_original_derived_record"]
            b = x["pet16_exact_same_source_petflag1_row"]
            self.assertEqual((a["original_server_template_physical_row"],
                              a["original_template_numeric_ID"],
                              a["original_graphic_numeric_ID"],
                              a["original_56_column_normalized_sha256"]),
                             (b["original_row"], b["template_id"],
                              b["graphic_number"], b["original_fields_sha256"]))
            self.assertEqual(b["petflag"], 1)
            self.assertFalse(x["official_TW10_pet_identity_verified"])
            self.assertFalse(x["original_capture_success_or_server_execution_verified"])

    def test_named_524_links_original_skill_row_SHA_and_item_candidate(self):
        r = capture_trace(self.c, self.p13, 524)
        self.assertEqual(r["pet13_original_derived_record"]["mixed25_configured_original_name"], "卡特利奴")
        self.assertEqual(r["pet16_exact_same_source_petflag1_row"]["id"], "MIXED25_MAIN:346")
        self.assertEqual(r["compiled_capture_required_item_references_only"], [2456])
        self.assertEqual([x["source_pet_skill_id"] for x in r["qualified_same_archive_skill_definitions"]], [1, 2])
        self.assertEqual(r["qualified_same_archive_skill_definitions"][0]["same_archive_short_name_when_sha_matched"], "攻擊")
        self.assertTrue(all(x["short_name_original_source_sha_verified"] for x in r["qualified_same_archive_skill_definitions"]))
        self.assertTrue(all(not x["native_skill_effect_verified"] for x in r["qualified_same_archive_skill_definitions"]))

    def test_petflag_zero_name_is_retained_but_not_inserted_as_petflag_one(self):
        r = capture_trace(self.c, self.p13, 8)
        self.assertEqual(r["pet13_original_derived_record"]["mixed25_configured_original_name"], "巨大瑪恩摩")
        self.assertEqual(r["pet13_original_derived_record"]["original_PETFLG"], 0)
        self.assertEqual(r["compiled_capture_required_item_references_only"], [1810])
        self.assertIsNone(r["pet16_exact_same_source_petflag1_row"])
        self.assertFalse(r["original_compiled_capture_selector_native_verified"])

    def test_p13_source_scope_item_and_skill_counts(self):
        self.assertEqual(len(self.p13["templates"]), 11)
        self.assertEqual(len([x for x in self.p13["templates"] if x["original_PETFLG"] == 1]), 10)
        ids = {n for x in self.p13["templates"] for n in x["capture_required_item_IDs"]}
        self.assertEqual(len(ids), 12)
        skills = {x["source_pet_skill_id"] for row in self.p13["templates"]
                  for x in row["same_archive_original_skill_links"]}
        self.assertEqual(skills, {1, 2, 60, 90, 110})
        self.assertTrue(self.p13["bounds"]["original_actual_capturable_pets_species_verified"] is False
                        if "original_actual_capturable_pets_species_verified" in self.p13["bounds"] else True)

    def test_unknown_template_id_not_fabricated(self):
        r = capture_trace(self.c, self.p13, 99999999)
        self.assertFalse(r["pet13_original_template_found"])
        self.assertIsNone(r["pet13_original_derived_record"])
        self.assertIsNone(r["pet16_exact_same_source_petflag1_row"])
        self.assertEqual(r["compiled_capture_required_item_references_only"], [])

    def test_bad_template_id_rejected(self):
        for invalid in (0, -2, True, "524", None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                capture_trace(self.c, self.p13, invalid)


if __name__ == "__main__":
    unittest.main()
