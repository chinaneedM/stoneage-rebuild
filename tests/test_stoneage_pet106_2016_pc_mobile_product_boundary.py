"""PET106: source-qualified 2016 classic PC versus mobile Origins first pass."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
AUDIT = REC / "STONEAGE-PET106-YEAR2016-CLASSIC-PC-VS-ORIGINS-MOBILE-FIRST-PASS-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET106-YEAR2016-CLASSIC-PC-AND-ORIGINS-MOBILE-PRODUCT-BOUNDARY-20261118.md"


class TestPet106Year2016ProductLines(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_year_remains_open_with_pet_only_priority(self):
        a, q = self.a, self.q
        y = next(row for row in q["yearly_work_queue"] if row["year"] == 2016)
        self.assertEqual(a["active_module"], q["active_module"])
        self.assertEqual(a["active_module"], "PET")
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2016, 2016))
        self.assertEqual(q["current_frontier"]["year"], 2016)
        self.assertEqual(y["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(a["annual_gate"], "NOT_YEAR_AUDITED")
        self.assertFalse(a["source_bounded_year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertIsNone(a["original_pc_global_pet_species_count"])
        self.assertIsNone(a["original_pc_first_release_species_count"])
        self.assertEqual(y["partial_source_review_receipts"][-1]["id"], a["id"])
        self.assertEqual(q["current_frontier"]["latest_2016_partial_source_receipt"], a["id"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET106:"))
        self.assertIn("PET106", REPORT.read_text(encoding="utf-8"))

    def test_source_grades_and_region_lineage_separation(self):
        a = self.a
        ids = {s["source_id"] for s in a["source_records"]}
        self.assertEqual(len(ids), len(a["source_records"]))
        self.assertEqual(len(ids), 7)
        self.assertEqual(set(a["region_reviews"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        cn = next(s for s in a["source_records"] if s["source_id"].startswith("CN2016"))
        self.assertEqual(cn["source_grade"], "CONTEMPORANEOUS_THIRD_PARTY_VERBATIM_OPERATOR_RELAY_NOT_ORIGINAL_OPERATOR_HTML")
        self.assertFalse(cn["first_party_original_html_retrieved"])
        mobile = [s for s in a["source_records"] if s["product_line"] == "STONEAGE_ORIGINS_MOBILE_SEPARATE_PRODUCT"]
        self.assertEqual(len(mobile), 4)
        self.assertTrue(all(s["source_grade"].startswith("FIRST_PARTY_") for s in mobile))
        updates = [s for s in mobile if s["source_grade"] == "FIRST_PARTY_OPERATOR_UPDATED_MOBILE"]
        self.assertEqual(len(updates), 2)
        self.assertEqual({s["source_date"] for s in updates}, {"2016-10-19", "2016-10-28"})
        self.assertEqual([x["label"] for x in updates[0]["form_labels"]], ["魯泰帕", "卡泰帕", "拉泰帕"])
        self.assertEqual(updates[1]["elemental_forms"], 4)
        self.assertTrue(all(not s["original_pc_issuance_confirmed"] for s in updates))
        self.assertTrue(all(a["negative_controls"].values()))

    def test_no_new_pc_original_or_2016_population_and_history_blob_preserved(self):
        a, q = self.a, self.q
        for key in (
            "newly_acquired_original_2016_pc_client_bytes",
            "newly_acquired_original_2016_pc_patch_bytes",
            "new_verified_same_build_original_pc_pet_ids",
            "new_verified_original_pc_spr_pixels",
            "new_verified_original_pc_skill_definitions",
            "new_verified_original_pc_server_pet_grants",
        ):
            self.assertEqual(a[key], 0)
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["starting_remote"]["unchanged_current_bytes"])
        git_hash = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(git_hash, a["starting_remote"]["unchanged_current_blob"])
        self.assertTrue(a["original_current_unchanged"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]))


if __name__ == "__main__":
    unittest.main()
