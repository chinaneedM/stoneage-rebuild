"""PET107 source-grade acceptance: 2016 Taozhu original PC pet evidence is not native release proof."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
AUDIT = REC / "STONEAGE-PET107-TW2016-BEETLE-DUANWU-2016-SOURCE-GRADES-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET107-TW2016-BEETLE-DUANWU-PLAYER-CLIENT-BOUNDARY-20261118.md"


class TestPet107Year2016SourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_2016_still_open_no_unqualified_module_switch(self):
        a, q = self.a, self.q
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2016)
        self.assertEqual((a["module"], q["active_module"]), ("PET", "PET"))
        self.assertEqual((a["year_cursor_before"], a["year_cursor_after"]), (2016, 2016))
        self.assertEqual(q["current_frontier"]["year"], 2016)
        self.assertEqual(y["research_gate"], "NOT_YEAR_AUDITED")
        self.assertFalse(a["historically_complete"])
        self.assertFalse(a["year_source_bounded_reviewed"])
        self.assertIsNone(a["global_pet_species_count"])
        self.assertIsNone(a["tw2016_new_species_count"])
        self.assertEqual(q["current_frontier"]["latest_2016_partial_source_receipt"], a["id"])
        self.assertEqual(y["partial_source_review_receipts"][-1]["id"], a["id"])
        self.assertTrue(a["next"].startswith("PET108:"))  # historical receipt next survives future cursor progress
        self.assertIn("PET107", REPORT.read_text(encoding="utf-8"))

    def test_dated_spring_and_duanwu_are_distinct_graded_layers(self):
        a = self.a
        sources = {s["id"]: s for s in a["sources"]}
        self.assertEqual(len(sources), 5)
        o = sources["TW2016-0202-BEETLE-OPERATOR-VOICE-MIRROR"]
        self.assertEqual(o["publication_date"], "2016-02-02")
        self.assertFalse(o["authentic_original_operator_domain"])
        self.assertFalse(o["operator_live_pet_grant_proved"])
        self.assertEqual(o["source_kind"], "DATED_THIRD_PARTY_FULL_HTML_OPERATOR_VOICE_RELAY")
        p = sources["TW2016-0316-BEETLE-FIRST-PERSON-PLAYER"]
        self.assertIn("2016-03-16", p["source_edit_date"])
        self.assertTrue(a["beetle"]["first_person_player_reports_pet_ownership"])
        self.assertTrue(a["beetle"]["first_person_player_reports_capture"])
        self.assertIsNone(a["beetle"]["named_final_reward_pet"])
        self.assertFalse(p["original_pc_same_build_verified"])
        self.assertEqual(p["content_access"], "SEARCH_INDEX_EXCERPT_ONLY_DIRECT_PAGE_403")
        d = a["dragon_boat"]
        self.assertEqual(d["monster_label_count_not_species_count"], 10)
        self.assertEqual(sum(len(names) for names in d["monster_labels_by_group"].values()), 10)
        self.assertEqual(len(set(sum(d["monster_labels_by_group"].values(), []))), 10)
        self.assertEqual(len(d["reward_item_labels"]), 3)
        self.assertIsNone(d["claimed_2016_new_pet_species_count"])
        self.assertTrue(d["monster_name_is_not_necessarily_released_catchable_pet"])
        self.assertTrue(d["reward_bag_is_not_native_pet_identity"])

    def test_client_source_attempts_not_promoted_to_verified_bytes(self):
        a = self.a
        self.assertEqual(a["client_version"]["player_mentioned_version"], "205")
        self.assertFalse(a["client_version"]["authenticated_client_version_build"])
        self.assertEqual(len(a["source_attempts"]), 3)
        for attempt in a["source_attempts"]:
            self.assertEqual(attempt["file_bytes_obtained"], 0)
            self.assertFalse(attempt["source_build_authenticated"])
        self.assertTrue(all(a["negative_controls"].values()))
        self.assertTrue(all(x["not_classic_pc"] for x in a["separate_product_lines"]))

    def test_zero_new_native_pc_and_unmodified_historical_state(self):
        a, q = self.a, self.q
        for key in (
            "newly_retrieved_original_taiwan_2016_pc_client_bytes",
            "newly_retrieved_original_taiwan_2016_pc_patch_bytes",
            "new_native_pet_ids",
            "new_original_spr_pixel_replays",
            "new_same_build_pet_skill_rows",
            "new_original_operator_server_grant_logs",
        ):
            self.assertEqual(a[key], 0)
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["baseline"]["current_state_original_size"])
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(digest, a["baseline"]["current_state_original_blob"])
        self.assertTrue(a["current_state_unchanged"])
        self.assertEqual(
            (a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_game_completion_percent"]),
            (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"])
        )


if __name__ == "__main__":
    unittest.main()
