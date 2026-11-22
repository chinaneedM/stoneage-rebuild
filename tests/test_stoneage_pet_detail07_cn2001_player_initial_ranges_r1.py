"""PET-DETAIL07: 20 historic player numeric rows, source dedup and non-promotion."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = "research/pets/PET-DETAIL-EVIDENCE07-CN2001-LEVEL1-20-NUMERIC-SOURCE-CLAIMS-R1.json"
DOC = "docs/pets/CN2001-LV1-20-PLAYER-NUMERIC-RANGES.md"
PREVIOUS = "research/recovered/STONEAGE-PET55-2001-KR20-CNPLAYER-TW1-SPR-R1.json"
REGISTRY = "research/pets/PET-ID-REGISTRY-R1.json"

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def blob_sha(path):
    b = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + bytes([0]) + b).hexdigest()

class Historical2001PlayerRanges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_json(DATA)
        cls.previous = read_json(PREVIOUS)
        cls.registry = read_json(REGISTRY)

    def test_exact_pinned_antecedents(self):
        a = self.data["antecedents"]["source_2001_pet20"]
        b = self.data["antecedents"]["TW10_registry"]
        self.assertEqual(blob_sha(a["path"]), a["git_blob_sha"])
        self.assertEqual(blob_sha(b["path"]), b["git_blob_sha"])
        self.assertEqual(len(self.registry["catalog_entries"]), 124)
        self.assertTrue(a["existing_20_names"])
        self.assertTrue(a["existing_7_crosslinks"])
        self.assertFalse(a["existing_stat_slot_ranges_transcribed"])

    def test_all_twenty_names_values_and_source_republication(self):
        rows = self.data["records"]
        previous = self.previous["player_2001_cn_list"]["derived_source_rows"]
        self.assertEqual(len(rows), 20)
        self.assertEqual([x["player_article_row"] for x in rows], list(range(1, 21)))
        self.assertEqual(len(set(x["obs_id"] for x in rows)), 20)
        self.assertEqual([x["pet_name_as_2001_player_page"] for x in rows],
                         [x["name"] for x in previous])
        self.assertEqual(self.data["sources"]["canonical_player_text"]["page_date_label"],
                         "2001-06-14")
        mirror = self.data["sources"]["duplicate_text_republication"]
        self.assertEqual(mirror["page_date_label"], "2003-10-19")
        self.assertEqual(mirror["embedded_attribution"], "服6：俄罗斯牛奶")
        self.assertFalse(mirror["independent_original_stat_observation"])
        self.assertEqual(self.data["counts"]["independent_stat_sources"], 1)
        self.assertEqual(self.data["counts"]["duplicated_reprint_pages"], 1)

        for x in rows:
            self.assertEqual(len(x["numeric_slots_as_page"]), 4)
            self.assertEqual(len(x["numeric_slots_bounds_without_stat_labels"]), 4)
            self.assertEqual(x["source_stat_slot_count"], 4)
            for raw, parsed in zip(x["numeric_slots_as_page"],
                                   x["numeric_slots_bounds_without_stat_labels"]):
                self.assertRegex(raw, r"^\d+(?:-\d+)?$")
                parts = [int(n) for n in raw.split("-")]
                expected = parts if len(parts) == 2 else [parts[0], parts[0]]
                self.assertEqual([parsed["min"], parsed["max"]], expected)
                self.assertLessEqual(parsed["min"], parsed["max"])
        self.assertEqual(self.data["counts"]["parsed_numeric_slots"], 80)
        self.assertEqual(rows[0]["numeric_slots_as_page"], ["60-64", "8-9", "5", "3"])
        self.assertEqual(rows[5]["element_text_as_player_page"], "火水3")
        self.assertEqual(rows[10]["numeric_slots_as_page"], ["49-54", "10-12", "7-9", "6-8"])
        self.assertEqual(rows[-1]["numeric_slots_as_page"], ["38-45", "6-8", "6-7", "6-7"])

    def test_seven_bounded_links_reuse_existing_PET55_witness(self):
        graded = {x["source_row"]: x for x in
                  self.previous["graded_cross_source_links"]["rows"]}
        self.assertEqual(len(graded), 7)
        used = set()
        for x in self.data["records"]:
            previous_link = graded.get(x["player_article_row"])
            if previous_link is None:
                self.assertIsNone(x["linked_tw10_pet_id"])
                self.assertIsNone(x["linked_tw10_dossier_path"])
                self.assertIsNone(x["linked_tw10_source_grade"])
                continue
            candidates = [v for v in self.registry["catalog_entries"]
                          if v["original_client_name"] ==
                          previous_link["TW1_original_client_album_name"]]
            self.assertEqual(len(candidates), 1)
            v = candidates[0]
            self.assertEqual(x["linked_tw10_pet_id"], v["catalog_pet_id"])
            self.assertEqual(x["linked_tw10_dossier_path"], v["visible_dossier_path"])
            self.assertEqual(x["linked_tw10_source_grade"], previous_link["grade"])
            self.assertTrue((ROOT / v["visible_dossier_path"]).is_file())
            used.add(v["catalog_pet_id"])
        self.assertEqual(len(used), 7)
        self.assertEqual(self.data["counts"]["matched_existing_source_tier_tw10_dossiers"], 7)
        self.assertEqual(self.data["counts"]["unlinked_with_current_TW10_client_dossier"], 13)

    def test_no_server_master_or_first_year_identity_promoted(self):
        self.assertFalse(self.data["numeric_semantics"]["original_native_column_ids_verified"])
        self.assertTrue(self.data["numeric_semantics"]["guide_intervals_are_not_proven_full_server_population_bounds"])
        for x in self.data["records"]:
            self.assertFalse(x["qualified_official_2001_PC_live_release"])
            self.assertFalse(x["linked_tw10_same_species_or_server_proven"])
            self.assertFalse(x["fourth_slot_semantic_proven_from_page"])
            for key in ("original_official_server_pet_id", "official_initial_stat_range",
                        "actual_original_server_element_values", "original_skill_id"):
                self.assertIsNone(x[key])
        c = self.data["counts"]
        for key in ("new_official_PC_pet_master_rows", "new_native_original_skill_ids",
                    "official_initial_stat_ranges_verified", "new_permanent_pet_ids",
                    "fully_complete_original_pc_pet_dossiers"):
            self.assertEqual(c[key], 0)
        self.assertIsNone(c["overall_percent"])
        self.assertIsNone(c["original_PC_pet_species_count"])
        p = self.data["preservation"]
        self.assertTrue(p["source_claims_are_separate_from_official_profile_values"])
        self.assertTrue(p["do_not_backfill_tw10_combat_stats_or_acquisition"])
        self.assertTrue(p["no_standalone_authoritative_2003_witness"])
        self.assertTrue(p["no_mobile_or_private_server_content"])
        self.assertEqual(blob_sha("docs/CURRENT-STATE.md"),p["preserve_CURRENT_original_blob"])

    def test_human_document_has_all_rows_links_and_limits(self):
        doc = (ROOT / DOC).read_text(encoding="utf-8")
        index = (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8")
        for x in self.data["records"]:
            self.assertIn(x["pet_name_as_2001_player_page"], doc)
            self.assertIn(" / ".join(x["numeric_slots_as_page"]), doc)
            if x["linked_tw10_pet_id"]:
                self.assertIn(x["linked_tw10_pet_id"], doc)
                self.assertIn(x["linked_tw10_dossier_path"].replace("docs/pets/",""), doc)
        self.assertIn("CN2001-LV1-20-PLAYER-NUMERIC-RANGES.md", index)
        self.assertIn("2003",doc)
        self.assertIn("不是",doc)

if __name__ == "__main__":
    unittest.main()
