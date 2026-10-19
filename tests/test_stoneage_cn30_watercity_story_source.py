import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "research" / "recovered" / "STONEAGE-CN30-WATERCITY-HEART-BRACELET-GUIDE-R1.json"

class WaterCitySourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_exact_source_link_and_scope(self):
        s = self.record["source"]
        self.assertEqual(s["article_url"], "https://news.17173.com/z/stoneage/renwu/sa30_08.htm")
        self.assertEqual(s["byline"], "微笑赢家 多多")
        self.assertFalse(s["operator_first_party"])
        self.assertIsNone(s["actual_publication_date"])
        self.assertIsNone(s["raw_page_sha256"])
        self.assertTrue(s["no_raw_byte_attestation"])

    def test_npc_unique_and_count(self):
        n = self.record["named_npc_mentions"]
        self.assertEqual([r["name"] for r in n], ["喀尔斯", "莉娜", "麦特", "卡蜜儿"])
        self.assertEqual(len(set(r["name"] for r in n)), 4)

    def test_guide_steps_ordered_bounded(self):
        seq = self.record["ordered_guide_steps"]
        self.assertEqual(len(seq), 11)
        self.assertEqual([s["number"] for s in seq], list(range(1,12)))
        self.assertEqual(seq[6]["actor"], None)
        self.assertEqual(seq[-1]["reported_output"], "心之手环")
        for s in seq:
            self.assertTrue(s["lines"][0] >= 26 and s["lines"][-1] <= 48)

    def test_preconditions_source_limits(self):
        self.assertEqual(len(self.record["preconditions"]), 5)
        self.assertTrue(self.record["preconditions"][2]["inclusive_100_ambiguous"])
        self.assertTrue(self.record["preconditions"][4]["consumption_unproven"])

    def test_material_grades_not_quantities(self):
        self.assertEqual([x["grade_token"] for x in self.record["reported_materials"]],["麟11","黏土4","线2","花10"])
        self.assertTrue(self.record["material_grade_tokens_are_not_item_quantities"])
        for material in self.record["reported_materials"]:
            self.assertNotIn("required_quantity",material)

    def test_reward_and_mutual_exclusivity_remain_guide_claims(self):
        self.assertEqual(self.record["reported_reward"]["stats_as_printed"],{"攻":-37,"防":37,"敏":37,"魅":8})
        self.assertIsNone(self.record["reported_reward"]["item_id"])
        self.assertTrue(self.record["reported_choice_constraint"]["server_predicate_unknown"])

    def test_no_original_server_or_early_version_attribution(self):
        self.assertFalse(self.record["version_claim"]["original_TW10"])
        self.assertFalse(self.record["version_claim"]["same_build_proven"])
        self.assertFalse(self.record["version_claim"]["original_server_execution_verified"])
        self.assertEqual(self.record["bounds"]["original_TW10_entities"],0)
        self.assertEqual(self.record["bounds"]["confirmed_runtime_entities"],0)
        self.assertEqual(self.record["bounds"]["new_original_client_files"],0)

    def test_route_not_map_identity(self):
        a = self.record["access_route"]
        self.assertEqual(a["claimed_start"],"伊甸园")
        self.assertEqual(a["claimed_end"],"水城")
        self.assertTrue(a["coordinate_strings_are_player_waypoints_not_map_ids"])
        self.assertTrue(a["intermediate_coordinates_excluded_from_engine_spec"])

    def test_finite_stop_and_next(self):
        self.assertEqual(self.record["bounds"]["new_source_bodies"],1)
        self.assertEqual(self.record["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18")
        self.assertEqual(self.record["source"]["read_method"],"WEB_RENDERED_PAGE_AND_ACTUAL_INDEX_CLICK")

if __name__ == "__main__":
    unittest.main()
