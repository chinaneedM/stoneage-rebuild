"""Boundary tests for qualified same-build pet identity triage; no historical claim promotion."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "research/recovered/STONEAGE-PET-IDENTITY-SAME-BUILD-TRIAGE-R1.json"
OLD = ROOT / "research/recovered/STONEAGE-EARLY-MEDIA-ARTICLE-PET-SOURCE-R1.json"
ASSETS = ROOT / "research/recovered/STONEAGE-PET-ASSET-GROWTH-CATALOG-MATRIX-R1.json"
ORIGINAL_VERIFIED = ROOT / "research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-VERIFIED-R1.json"
ORIGINAL_INPUT = ROOT / "research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"

class SameBuildPetIdentityTriageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(NEW.read_text(encoding="utf-8"))
        cls.old = json.loads(OLD.read_text(encoding="utf-8"))
        cls.assets = json.loads(ASSETS.read_text(encoding="utf-8"))
        cls.verified = json.loads(ORIGINAL_VERIFIED.read_text(encoding="utf-8"))
        cls.original_input = json.loads(ORIGINAL_INPUT.read_text(encoding="utf-8"))

    def test_two_distinct_named_late_migration_sources(self):
        sources = self.data["newly_examined_sources"]
        self.assertEqual(len(sources), 2)
        self.assertEqual({x["as_displayed_date"] for x in sources}, {"2001-06-14"})
        self.assertEqual(len({x["url"] for x in sources}), 2)
        self.assertTrue(all(x["read_method"] == "CURRENT_MIGRATED_PUBLIC_PAGE_TEXT" for x in sources))
        self.assertTrue(all(not x["original_2001_page_snapshot_verified"] for x in sources))
        lv1 = next(x for x in sources if x["id"] == "MEDIA17173_LV1_124")
        self.assertEqual((lv1["numbered_from"], lv1["numbered_to"], lv1["observed_numbered_player_entries"]), (1, 124, 124))
        self.assertFalse(lv1["reported_spawns_authenticated"])
        self.assertEqual(lv1["source_material_status"], "NEW_LEXICAL_EVIDENCE_ADDED_THIS_PACKAGE")
        stonepic = next(x for x in sources if x["id"] == "MEDIA17173_STONEPIC_RANGES")
        self.assertEqual(stonepic["source_material_status"], "RECHECKED_PREEXISTING_GIT_EVIDENCE_NOT_NEW")
        self.assertFalse(stonepic["tw10_semantic_categories_verified"])

    def test_alias_joins_are_lexical_only_and_existing_candidates_preserved(self):
        original = {x["record_id"]: x for x in self.old["pet_name_candidates"]}
        self.assertEqual(len(original), 20)
        joins = self.data["selected_lexical_overlaps"]
        self.assertEqual(len(joins), 7)
        self.assertEqual(len({x["lv1_row"] for x in joins}), 7)
        self.assertEqual(sum(x["relation"] == "EXACT_NAME_STRING" for x in joins), 1)
        for item in joins:
            self.assertEqual(item["source_name"], original[item["old_candidate_id"]]["source_name"])
            if item["relation"] == "EXACT_NAME_STRING":
                self.assertEqual(item["source_name"], item["lv1_label"])
            self.assertFalse(item["same_species_certified"])
            self.assertIsNone(original[item["old_candidate_id"]]["tw10_graphic_id"])
            self.assertIsNone(original[item["old_candidate_id"]]["spr_no"])
            self.assertIsNone(original[item["old_candidate_id"]]["original_species_id"])

    def test_player_image_ranges_not_confused_with_original_resource_ids(self):
        ranges = self.data["image_category_claims"]
        self.assertEqual([(r["first_inclusive"], r["last_inclusive"]) for r in ranges],
                         [(7246, 7366), (95883, 125995)])
        self.assertTrue(all(not r["tw10_adrn_certified"] and not r["tw10_spr_group_certified"] for r in ranges))
        counts = self.assets["resource_report"]["record_counts"]
        self.assertEqual(counts["adrn_bitmap_records"], self.data["image_numbering_boundary"]["tw10_adrn_record_count"])
        self.assertEqual(counts["spr_groups"], 464)
        self.assertFalse(self.data["image_numbering_boundary"]["comparable_as_id_range_without_index_and_build_proof"])
        self.assertFalse(self.data["image_numbering_boundary"]["contradiction_of_raw_tw10_resource_index_claimed"])

    def test_prior_exact_tw10_bitmap_membership_not_reported_as_new(self):
        rep = self.verified["verified_range_report"]
        self.assertEqual(rep["tw10_bitmap_range"], [0, 125995])
        self.assertEqual(rep["tw10_adrn_bitmap_records"], 125996)
        b = self.data["image_numbering_boundary"]
        self.assertTrue(b["tw10_adrn_record_ids_verified_contiguous"])
        self.assertEqual((b["tw10_adrn_min_bitmap_id"], b["tw10_adrn_max_bitmap_id"]), (0, 125995))
        self.assertTrue(b["stonepic_source_previously_examined_in_repo"])
        self.assertTrue(b["tw10_id_membership_before_this_package"])
        ranges = {x["id"]: x for x in rep["ranges"]}
        for key, count in [("pet_portrait", 121), ("pet_actions", 30113)]:
            self.assertEqual(ranges[key]["present_in_tw10_adrn"], count)
            self.assertFalse(ranges[key]["category_tw10_verified"])
            self.assertFalse(ranges[key]["actual_tw10_semantic_certified"])
        claims = self.data["image_category_claims"]
        self.assertEqual([x["tw10_adrn_present_count"] for x in claims], [121, 30113])
        self.assertTrue(all(x["tw10_id_membership_verified_in_preexisting_repo"] for x in claims))
        self.assertTrue(all(not x["tw10_semantic_label_verified"] for x in claims))
        path_to_blob = {x["path"]: x["git_blob"] for x in self.data["base_evidence"]}
        self.assertEqual(path_to_blob[str(ORIGINAL_INPUT.relative_to(ROOT))], "11bb14ef00c2ed354c5f00f510da8783376f1f28")
        self.assertEqual(path_to_blob[str(ORIGINAL_VERIFIED.relative_to(ROOT))], "0007030347a635b19ec9739897f2b582bd92e98f")
        self.assertTrue(self.data["correction"]["preexisting_source_is_duplicate_not_new"])

    def test_all_pet_identity_and_game_production_gates_remain_unproven(self):
        self.assertEqual(self.data["disposition"], "OPEN_EVIDENCE_LIMITED_SAME_BUILD_PET_IDENTITY_NOT_OBTAINED")
        self.assertTrue(self.data["stop_condition_met"])
        self.assertTrue(all(v is None or v is False for v in self.data["identity_fields"].values()))
        self.assertTrue(all(v is False for k, v in self.data["source_boundaries"].items() if k != "raw_taiwan_resource_asset_join_preserved" and k != "no_copyrighted_original_source_payload_committed"))
        self.assertTrue(self.data["source_boundaries"]["raw_taiwan_resource_asset_join_preserved"])
        self.assertTrue(self.data["source_boundaries"]["no_copyrighted_original_source_payload_committed"])
        self.assertTrue(self.data["no_restoration_percentage"])
        self.assertEqual(self.data["next_priority"], "ORIGINAL-SERVER-NPC-QUEST-SAME-BUILD-SOURCE-TRIAGE-01")

if __name__ == "__main__":
    unittest.main()
