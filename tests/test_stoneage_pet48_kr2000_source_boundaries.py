"""PET48: guard period Korean pet claims against unproven live rosters."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"


def load_json(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


class Korean2000PetSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load_json("STONEAGE-PET48-KR2000-EARLY-PET-SOURCE-BOUNDARIES-R1.json")

    def test_early_124_is_period_marketing_not_same_build_roster(self):
        d = self.d
        by_id = {s["id"]: s for s in d["sources"]}
        self.assertEqual(len(by_id), 6)
        self.assertEqual(by_id["PET48-KR-2000-JUL04-INEWS24"]["published_date"], "2000-07-04")
        self.assertEqual(by_id["PET48-KR-2000-JUL12-ETNEWS"]["published_date"], "2000-07-12")
        self.assertTrue(by_id["PET48-KR-2000-JUL04-INEWS24"]["source_previously_known_for_distribution"])
        self.assertEqual(by_id["PET48-KR-2000-JUL04-INEWS24"]["time_claims"][0]["kind"], "PLANNED_KR_TRIAL_NOT_PROVEN_LIVE")
        cnt = d["source_count_vs_asset_count"]
        self.assertEqual(cnt["korean_early_marketed_pet_count"], 124)
        self.assertEqual(cnt["tw10_original_client_album_named_graphic_count"], 124)
        self.assertEqual(len(load_json("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")["records"]), 124)
        self.assertFalse(cnt["identical_pet_roster_proven"])
        self.assertFalse(cnt["official_korean_live_pets_from_124_proven"])
        self.assertIsNone(cnt["first_release_year_pet_total"])

    def test_sources_have_no_fake_bytes_or_native_execution(self):
        d = self.d
        self.assertTrue(all(s["source_sha256"] is None for s in d["sources"]))
        self.assertTrue(all(s["access"] == "WEB_ARTICLE_TEXT_READ_NOT_RAW_BYTES" for s in d["sources"]))
        review = next(s for s in d["sources"] if s["id"] == "PET48-KR-2000-DEC21-GAMEMECA-REVIEW")
        self.assertFalse(review["native_program_execution_verified"])
        self.assertEqual(d["new_original_kr2000_client_bytes"], 0)
        self.assertIsNone(d["new_kr2000_original_binary_sha256"])
        self.assertEqual(d["new_pet_names_with_same_deployment_availability_evidence"], 0)
        self.assertEqual(d["new_confirmed_official_in_game_pet_release_evidence"], 0)

    def test_pet47_forward_correction_is_not_rewritten_as_new_fulltext(self):
        d = self.d
        c = d["forward_only_correction"]
        self.assertTrue(c["do_not_mutate_previous_report"])
        self.assertFalse(c["article_full_content_read_this_turn"])
        self.assertIn("PET47", c["historical_record"])
        self.assertTrue(any("200010121149020000950_26" in x.get("legacy_perma_article", "") for x in d["prior_repository_evidence_reused"]))

    def test_only_pet_module_and_year_2000_stays_open(self):
        d = self.d
        self.assertEqual((d["active_module"], d["frontier_year"], d["frontier_status"]), ("PET", 2000, "OPEN"))
        self.assertEqual(d["current_state_git_blob_preserved"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_B_wiki"], "GATED")
        self.assertIsNone(d["overall_completion_percent"])


if __name__ == "__main__":
    unittest.main()
