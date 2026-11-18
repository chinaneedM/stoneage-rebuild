"""PET109: exact source-grade boundaries for Taiwan 2016 original PC rewards."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "research/recovered/STONEAGE-PET109-TW2016-PLAYER-PET-REWARDS-HALLOWEEN-2015-CROSSYEAR-BOUNDARY-R1.json"
QUEUE = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
PRIOR = ROOT / "research/recovered/STONEAGE-PET104-TW2015-HALLOWEEN-RELAY-PRIZE-EGG-BOUNDARY-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET109-TW2016-CONTEMPORANEOUS-PLAYER-AND-HALLOWEEN-CROSSYEAR-20261118.md"

class TestPet109DatedPlayerAndCrossyear(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))
        cls.old = json.loads(PRIOR.read_text(encoding="utf-8"))

    def test_year_pet_lock_and_forward_only(self):
        a, q = self.a, self.q
        y = next(z for z in q["yearly_work_queue"] if z["year"] == 2016)
        self.assertEqual((a["module"], q["active_module"]), ("PET", "PET"))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2016)
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2016, 2016))
        self.assertIn(y["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertFalse(a["source_bounded_year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertIn(a["id"], [x["id"] for x in y["partial_source_review_receipts"]])
        self.assertEqual(q["current_frontier"]["latest_2016_partial_source_receipt"], a["id"])
        self.assertTrue(a["next"].startswith("PET110:"))  # historical NEXT retained
        self.assertGreaterEqual(len(y["partial_source_review_receipts"]), 4)
        self.assertIn("PET109", REPORT.read_text(encoding="utf-8"))

    def test_2016_player_and_later_2025_edited_guide_not_confounded(self):
        a = self.a
        sources = {z["id"]: z for z in a["sources"]}
        self.assertEqual(len(sources), 4)
        player = sources["TW2016-1030-CONTEMPORANEOUS-PLAYER-GUIDE"]
        edited = sources["TW2016-1026-HALLOWEEN-LATER-EDITED-GUIDE"]
        self.assertIn("2016-10-30", player["visible_post_edit_timestamp"])
        self.assertIn("PLAYER", player["source_kind"])
        self.assertEqual(player["access_grade"], "SEARCH_INDEX_EXTENDED_TEXT_DIRECT_ORIGINAL_FORUM_403")
        self.assertIn("2025-02-01", edited["visible_edit_timestamp"])
        self.assertTrue(edited["original_2016_date_is_heading_only"])
        self.assertEqual(edited["string_count_not_species_count"], len(edited["reported_reward_strings"]))
        self.assertEqual(edited["string_count_not_species_count"], 7)
        self.assertFalse(edited["claimed_player_live_issuance_logs_obtained"])
        self.assertTrue(a["unverified_details"]["later_2025_edited_guide_cannot_upgrade_to_2016_original_text"])

    def test_reward_items_dedup_and_old_record_present(self):
        a = self.a
        prior = next(z for z in a["sources"] if z["id"] == "TW2015-1028-HALLOWEEN-CROSSYEAR-EXISTING-PET104")
        self.assertEqual(prior["already_registered_pet_receipt"], self.old["id"])
        self.assertEqual(prior["year"], 2015)
        self.assertTrue(a["dedup"]["historical_2015_pet104_unchanged"])
        self.assertEqual(set(a["dedup"]["overlapping_pet_names_from_2015"]), {"史凱勒頓", "古斯特"})
        self.assertEqual(set(prior["crossyear_overlap_named_reward_candidates"]), {"史凱勒頓", "古斯特"})
        self.assertTrue(a["dedup"]["halloween_2016_potential_reward_reuse_not_equal_2016_first_release"])
        self.assertIsNone(a["dedup"]["original_2016_amido_variant_pet_id"])
        self.assertIsNone(a["dedup"]["original_2016_fossil_archaeopteryx_pet_id"])
        self.assertTrue(all(a["negative_controls"].values()))

    def test_native_provenance_no_client_bytes_and_current_sha(self):
        a, q = self.a, self.q
        for field in (
            "new_original_2016_pc_client_bytes", "new_original_2016_pc_patch_bytes",
            "new_original_pc_pet_ids", "new_original_pc_spr_frames",
            "new_verified_original_pc_skill_rows", "new_verified_official_server_reward_grants"
        ):
            self.assertEqual(a[field], 0)
        self.assertIsNone(a["first_release_2016_species_count"])
        self.assertIsNone(a["global_2016_species_count"])
        current = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(current), a["starting_remote"]["current_bytes"])
        blob_sha = hashlib.sha1(b"blob " + str(len(current)).encode("ascii") + b"\x00" + current).hexdigest()
        self.assertEqual(blob_sha, a["starting_remote"]["current_blob"])
        self.assertEqual(a["exact_current_blob_unchanged"], blob_sha)
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_game_completion_percent"]),
                         (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]))

if __name__ == "__main__":
    unittest.main()
