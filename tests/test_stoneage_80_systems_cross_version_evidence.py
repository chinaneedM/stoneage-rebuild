import json
import unittest
from pathlib import Path

PATH = Path("research/recovered/STONEAGE-80-SYSTEMS-CROSS-VERSION-EVIDENCE-R1.json")

class SourceBridgeBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text(encoding="utf-8"))
        cls.sources = {s["id"]: s for s in cls.data["sources"]}
        cls.claims = {c["id"]: c for c in cls.data["claims"]}

    def test_reuses_original_qualified_source_without_promoting_runtime(self):
        d = self.data
        self.assertEqual(d["previous_verified_official_source"]["git_blob_sha"],
                         "4fb303eb6f8866b5454f994a0d4fedbf52ea76b0")
        self.assertEqual(d["previous_verified_official_source"]["original_html_sha256"],
                         "0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c")
        self.assertFalse(d["irreversible_boundaries"]["exact_80_client_or_server_content_recovered"])
        self.assertIsNone(d["irreversible_boundaries"]["aggregate_restoration_percentage"])

    def test_citation_relationship_and_reprint_not_double_counted(self):
        self.assertEqual(len(self.sources), 5)
        for c in self.claims.values():
            self.assertTrue(c["source_ids"], c["id"])
            self.assertTrue(all(s in self.sources for s in c["source_ids"]), c["id"])
        self.assertEqual(self.sources["CN_17173_20050609"]["lineage"],
                         self.sources["TW_BAHAMUT_20050608"]["lineage"])
        self.assertFalse(self.sources["CN_17173_20050609"]["independent_editorial_corroboration"])
        self.assertEqual(self.data["source_lineage"]["independent_press_reports_on_tw_launch"], 1)
        self.assertFalse(self.data["source_lineage"]["reprint_counted_as_new_origin"])

    def test_regional_claims_and_news_date_are_not_original_build(self):
        self.assertIsNone(self.sources["CN_17173_8_0_FEATURES"]["publication_date"])
        self.assertEqual(self.sources["CN_17173_8_0_FEATURES"]["region"], "CN")
        self.assertFalse(self.sources["TW_BAHAMUT_20050608"]["date_is_client_build"])
        for c in self.claims.values():
            if c["scope"] == "CN_NEW_STONEAGE_8_0_PORTAL":
                self.assertTrue(all(s.startswith("CN_17173_8_0") for s in c["source_ids"]))
        self.assertFalse(self.data["irreversible_boundaries"]["all_official_80_regions_same_patch_verified"])

    def test_quest_lead_is_not_server_quest_record(self):
        quest = self.claims["CN80_NAMED_QUEST_LEAD"]
        self.assertEqual(quest["quest_name_as_written"], "爱作画的少女")
        for missing in ("npc_id","quest_conditions","quest_reward"):
            self.assertIsNone(quest[missing])
        self.assertFalse(self.data["irreversible_boundaries"]["any_quest_script_recovered"])

    def test_no_copyright_or_stage_b_promotion(self):
        self.assertFalse(self.data["irreversible_boundaries"]["copyrighted_original_assets_retained"])
        self.assertFalse(self.data["irreversible_boundaries"]["stage_b_game_and_wiki_production_started"])
        self.assertFalse(self.data["irreversible_boundaries"]["r79_reopened"])
        self.assertIsNone(self.data["source_lineage"]["unpinned_web_page_raw_content_sha256"])

if __name__ == "__main__":
    unittest.main()
