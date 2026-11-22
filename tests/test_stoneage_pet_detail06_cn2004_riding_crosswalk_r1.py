"""Source-only CN2004 guide riding references: no cross-version server identity promotion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = "research/pets/PET-DETAIL-EVIDENCE06-CN2004-RIDING-TW10-NAME-CROSSWALK-R1.json"
DOC = "docs/pets/CN2004-RIDING-GUIDE-TEN-NAME-CROSSWALK.md"

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def blob(path):
    b = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + bytes([0]) + b).hexdigest()

class PetDetail06(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read(DATA)
        cls.reg = read("research/pets/PET-ID-REGISTRY-R1.json")
        cls.prior = read("research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json")

    def test_existing_source_and_client_pins_are_exact(self):
        s = self.d["reused_source_registry"]
        r = self.d["TW10_existing_registry"]
        self.assertEqual(blob(s["path"]), s["git_blob_sha"])
        self.assertEqual(blob(r["path"]), r["git_blob_sha"])
        self.assertEqual(self.prior["sources"][0]["id"], "S1")
        self.assertEqual(self.prior["sources"][0]["url"], self.d["source"]["url"])
        self.assertTrue(s["already_indexed_2004_guide"])

    def test_ten_unique_rider_guide_names_link_exact_source_only(self):
        entries = self.d["entries"]
        self.assertEqual(len(entries), 10)
        self.assertEqual(len(set(x["source_observation_id"] for x in entries)), 10)
        self.assertEqual(len(set(x["matched_TW10_catalog_pet_id"] for x in entries)), 10)
        self.assertEqual(sum(x["source_guide_category"] == "MANOR_NINE" for x in entries), 9)
        self.assertEqual(sum(x["source_guide_category"] == "EXTRA_FIVE_REBIRTH" for x in entries), 1)
        for x in entries:
            matches = [v for v in self.reg["catalog_entries"] if v["display_name_simplified"] == x["historical_guide_name"]]
            self.assertEqual(len(matches), 1, x["historical_guide_name"])
            v = matches[0]
            self.assertEqual(v["catalog_pet_id"], x["matched_TW10_catalog_pet_id"])
            self.assertEqual(v["original_client_name"], x["matched_TW10_original_compiled_name"])
            self.assertEqual(v["observations"][0], x["matched_TW10_source_observation"])
            self.assertEqual(v["visible_dossier_path"], x["matched_TW10_dossier_path"])
            self.assertTrue((ROOT / x["matched_TW10_dossier_path"]).is_file())
            self.assertEqual(x["matching_basis"], "EXACT_SIMPLIFIED_NAME_TEXT_ONLY")

    def test_report_is_not_original_master_or_riding_proof(self):
        self.assertEqual(self.d["scope"], "ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(self.d["active_module"], "PET")
        self.assertEqual(self.d["source"]["original_client_exe_or_CAB_new_bytes"], 0)
        self.assertFalse(self.d["source"]["original_http_html_bytes_recovered"])
        self.assertFalse(self.d["source"]["source_guide_is_original_native_PC_build"])
        for x in self.d["entries"]:
            for key in ("same_native_pet_id_verified", "same_official_server_or_build_verified",
                        "historical_capture_location_verified", "historical_riding_mechanics_runtime_verified",
                        "actual_official_release_confirmed_by_this_source"):
                self.assertFalse(x[key])
            for key in ("original_server_pet_id", "original_skill_id", "original_level1_stats",
                        "original_growth_formula", "original_source_graphic_id_in_2004_guide"):
                self.assertIsNone(x[key])

    def test_counts_and_unmodified_original_current(self):
        c = self.d["counts"]
        self.assertEqual((c["dated_guide_name_rows"], c["nine_manor_riding_claims"],
                          c["extra_five_rebirth_rider_claims"]), (10, 9, 1))
        self.assertEqual(c["exact_string_crosslinks_to_existing_TW10_profiles"], 10)
        self.assertEqual(c["new_source_observations"], 10)
        for k in ("new_permanent_PET_IDs", "new_authenticated_original_client_files",
                  "official_live_species_newly_confirmed", "historically_complete_PC_pet_profiles"):
            self.assertEqual(c[k], 0)
        self.assertIsNone(c["original_classic_PC_total_species"])
        self.assertIsNone(c["overall_percent"])
        self.assertEqual(len(self.reg["catalog_entries"]), 124)
        self.assertEqual(blob("docs/CURRENT-STATE.md"), self.d["boundaries"]["original_CURRENT_blob"])

    def test_user_can_navigate_all_ten_without_backfilling_pets(self):
        s = (ROOT / DOC).read_text(encoding="utf-8")
        ix = (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8")
        for x in self.d["entries"]:
            self.assertIn(x["historical_guide_name"], s)
            self.assertIn(x["matched_TW10_catalog_pet_id"], s)
            self.assertIn(x["matched_TW10_dossier_path"].removeprefix("docs/pets/"), s)
        self.assertIn("CN2004-RIDING-GUIDE-TEN-NAME-CROSSWALK.md", ix)
        self.assertTrue(self.d["boundaries"]["not_same_build_identity"])

if __name__ == "__main__":
    unittest.main()
