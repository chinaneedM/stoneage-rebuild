"""R55 finite evidence-structure regression; no HTTP or original game execution."""
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
RECORD=ROOT/"research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json"

class TestShellQuestR55(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(RECORD.read_text(encoding="utf-8"))

    def test_provenance_and_scope(self):
        r=self.r
        self.assertEqual(r["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55")
        self.assertEqual([s["id"] for s in r["sources"]],["S2001","S2003_Q","S2003_H"])
        self.assertIn("NOT_JSS1999_TW10",r["version_scope"])
        for s in r["sources"]:
            self.assertIsNone(s["raw_http_bytes"])
            self.assertIsNone(s["raw_html_sha256"])
            self.assertFalse(s["authorship_independently_verified"])
        self.assertFalse(r["source_replay"]["exact_original_source_bytes_downloaded"])
        self.assertFalse(r["source_replay"]["original_game_client_executed"])

    def test_two_directional_quests_do_not_merge(self):
        a,b=self.r["routes_2003"]
        self.assertEqual([a["id"],b["id"]],["Q_A","Q_B"])
        self.assertEqual((a["delivered_item"],a["reward_as_written"]),("仙尼亚的花","不可思议的贝壳"))
        self.assertEqual((b["delivered_item"],b["reward_as_written"]),("不可思议的贝壳","仙尼亚的花"))
        self.assertEqual(a["origin_local_location_as_written"],"东56，南124")
        self.assertEqual(b["recipient_local_location_as_written"],"东57，南124")
        self.assertIsNone(a["repeat_cost_verified_in_original_client"])
        self.assertIsNone(b["repeat_cost_verified_in_original_client"])

    def test_2001_conflicting_reward_and_five_claims(self):
        c=self.r["comparison"]
        self.assertTrue(c["source_claims_contradict"])
        self.assertTrue(c["do_not_force_reconcile"])
        self.assertEqual(c["s2001_route_claim"]["direction"],c["s2003_same_direction_claim"]["direction"])
        self.assertEqual(c["s2001_route_claim"]["claim_reward"],"不可思议的贝壳")
        self.assertEqual(c["s2003_same_direction_claim"]["claim_reward"],"仙尼亚的花")
        self.assertEqual(c["version_patch_conclusion"],"UNKNOWN")
        self.assertEqual(c["writer_error_conclusion"],"UNKNOWN")
        methods=self.r["source_2001_five_reported_methods"]
        self.assertEqual(len(methods),5)
        self.assertEqual([x["sequence"] for x in methods],list(range(1,6)))
        self.assertEqual(methods[3]["quoted_price_stone"],1000)
        self.assertIsNone(methods[4]["fully_parsed_coordinates"])
        self.assertTrue(methods[4]["corrupt_species_label_present"])
        self.assertTrue(all(not x["verified_execution"] for x in methods))

    def test_portal_requires_item_in_guide_not_level_gate_proven(self):
        p=self.r["s2003_hero_island_bridge"]
        self.assertEqual(p["portal_npc"],"黑乌力")
        self.assertEqual(p["hero_prequel_level_requirement_as_guide"],80)
        self.assertEqual(p["hero_prequel_recommended_level_as_guide"],120)
        self.assertIsNone(p["transport_min_level_verified"])
        self.assertIsNone(p["shell_consumed_during_transport"])
        self.assertFalse(p["original_time_travel_engine_proven"])
        self.assertFalse(self.r["s2003_item_restrictions"]["cross_version_enforced_rule_proven"])
        self.assertGreaterEqual(len(self.r["unproven"]),8)

if __name__=="__main__":
    unittest.main()
