import json
from pathlib import Path
import unittest

PATH=Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN60-TEARSTONE-STORY-SOURCE-R1.json"

class TearstoneSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_r18_task_and_next(self):
        self.assertEqual(self.data["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18")
        self.assertEqual(self.data["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19")

    def test_period_date_not_original_server_certification(self):
        s=self.data["source_a"]
        self.assertEqual(s["visible_publication"],"2003-05-21 22:59")
        self.assertEqual(s["visible_item_provenance"],"网友投稿")
        self.assertFalse(s["first_party_operator_quest_author"])
        self.assertIsNone(s["historical_original_html_sha256"])
        self.assertEqual(s["source_read"],"WEB_SEARCH_INDEXED_FULL_STEP_TEXT_ONLY_DIRECT_PAGE_OPEN_TIMED_OUT")

    def test_reprinted_text_not_independent(self):
        self.assertEqual(self.data["source_b"]["relation_to_source_a"],"NEAR_VERBATIM_GUIDE_REPRINT")
        self.assertFalse(self.data["boundaries"]["inter_source_independence_of_reposts"])

    def test_historical_build_unknown(self):
        v=self.data["game_lineage"]
        self.assertFalse(v["site_path_is_client_build_proof"] if "site_path_is_client_build_proof" in v else self.data["source_a"]["site_path_is_client_build_proof"])
        self.assertIsNone(v["exact_original_build"])
        self.assertFalse(v["original_TW10"])
        self.assertFalse(v["original_JSS1999"])

    def test_exact_six_steps_and_person_names(self):
        c=self.data["content"]
        self.assertEqual([x["ordinal"] for x in c["ordered_walkthrough_steps"]],list(range(1,7)))
        self.assertEqual([x["name"] for x in c["named_characters"]],["夕姬","洛林","杰夫"])
        self.assertEqual(c["ordered_walkthrough_steps"][2]["claimed_input"],["白星·女戒"])
        self.assertEqual(c["ordered_walkthrough_steps"][2]["claimed_output"],["克林斯首饰"])

    def test_player_waypoints_are_not_map_geometry(self):
        self.assertEqual(len(self.data["content"]["one_way_route_strings"]),16)
        self.assertEqual(self.data["content"]["one_way_route_strings"][0],"146.49")
        self.assertEqual(self.data["content"]["one_way_route_strings"][-1],"245.260")
        self.assertFalse(self.data["content"]["route_transitions_runtime_verified"])

    def test_no_unproven_guaranteed_preconditions(self):
        c=self.data["content"]
        self.assertTrue(c["effect_of_time_locking_unknown"])
        self.assertFalse(c["equipment_hint_is_mandatory_predicate"])
        self.assertTrue(c["ordered_walkthrough_steps"][1]["fish_gill_grass_mandatory_unproven"])

    def test_reward_guide_claim_not_item_master(self):
        r=self.data["content"]["claimed_reward"]
        self.assertEqual(r["quantity"],5)
        self.assertEqual(r["aggregate_basic_stat_point_gain_claim"],5)
        self.assertIsNone(r["original_item_id"])
        self.assertFalse(r["confirmed_game_effect"])

    def test_later_2025_is_not_same_build(self):
        self.assertEqual(self.data["source_c"]["visible_edit_date"],"2025-05-13 23:04:28")
        self.assertEqual(len(self.data["distinct_later_edition_comparison"]),4)
        self.assertTrue(all("NOT_" in d["status"] or "UNKNOWN" in d["status"] for d in self.data["distinct_later_edition_comparison"]))

    def test_no_original_assets_or_server(self):
        b=self.data["boundaries"]
        self.assertEqual(b["actual_original_server_execs"],0)
        self.assertEqual(b["original_pixels_downloaded"],0)
        self.assertEqual(b["first_party_stat_or_quest_master_recovered"],0)
        self.assertTrue(b["all_22_domain_statuses_unchanged"])
        self.assertFalse(b["new_game_canon_or_implementation_started"])

if __name__=="__main__":
    unittest.main()
