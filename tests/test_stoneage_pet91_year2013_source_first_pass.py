"""PET91: 2013 operator-origin pet announcements, version and product-line gates."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"
EVIDENCE = "STONEAGE-PET91-YEAR2013-CN-PET-OPERATOR-KR-MOBILE-SCOPE-FIRST-PASS-R1.json"
QUEUE = "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"

class Pet91Year2013(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads((DATA / EVIDENCE).read_text(encoding="utf-8"))
        cls.q = json.loads((DATA / QUEUE).read_text(encoding="utf-8"))

    def test_2013_open_no_false_closure(self):
        a, q = self.a, self.q
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2013, 2013, 2013))
        self.assertEqual(q["current_frontier"]["year"], 2013)
        self.assertEqual(q["yearly_work_queue"][14]["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(a["review_status"], "PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["source_bounded_annual_audit_complete"])
        self.assertFalse(a["historically_complete"])
        self.assertIsNone(a["global_original_pc_pet_species_count_2013"])
        self.assertIsNone(a["first_release_2013_species_count"])
        self.assertIsNone(q["yearly_work_queue"][14].get("historical_species_count"))

    def test_forward_only_source_receipt(self):
        a, q = self.a, self.q
        self.assertEqual(q["yearly_work_queue"][14]["partial_source_review_receipts"][-1]["id"], a["id"])
        self.assertEqual(q["root_source_census_receipts"][-1]["id"], a["id"])
        self.assertEqual(sum(x["id"] == a["id"] for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))
        self.assertEqual(q["yearly_work_queue"][13]["research_gate"], "SOURCE_BOUNDED_REVIEWED")

    def test_distinct_sources_and_names_not_species_count(self):
        a = self.a
        self.assertEqual(a["source_count"], len(a["sources"]))
        self.assertEqual(a["source_count"], 7)
        self.assertEqual(len({x["id"] for x in a["sources"]}), 7)
        self.assertEqual(len({x["url"] for x in a["sources"]}), 7)
        self.assertEqual([x["date_published"] for x in a["sources"]],
                         sorted(x["date_published"] for x in a["sources"]))
        self.assertEqual(a["named_pc_pet_labels_not_species"], 7)
        self.assertEqual(len(a["grouped_published_name_tokens"]), 7)
        self.assertTrue(all(not x["native_client_verified"] for x in a["sources"]))
        self.assertTrue(all(a["source_negative_controls"].values()))

    def test_named_and_2_5_8_5_reward_separation(self):
        src = {x["id"]: x for x in self.a["sources"]}
        march = src["CN2013-03-14-BLUDIBAN-SUANNI-ANNOUNCED"]
        self.assertIn("布鲁迪斑", march["pet_name_attestations"])
        self.assertEqual(march["evidence_status"], "OFFICIAL_ANNOUNCED_OR_WEB_LISTED_RELEASE_UNVERIFIED")
        april = src["CN2013-04-25-YAAN-25-85-REWARDS"]
        self.assertEqual(april["version"], "CN_2_5_AND_8_5_DISTINCT")
        self.assertIn("机暴证", april["advertised_reward_lanes"]["2.5"]["5_chars"])
        self.assertIn("贝莱瑞贡", april["advertised_reward_lanes"]["8.5"]["5_chars"])
        self.assertIn("巴雅", april["advertised_reward_lanes"]["8.5"]["4_chars"])
        self.assertEqual(set(april["explicit_non_pet_items"]), {"机暴证", "兽环"})
        self.assertFalse(april["actual_server_reward_verified"])

    def test_korean_mobile_and_non_pet_contamination(self):
        src = {x["id"]: x for x in self.a["sources"]}
        self.assertTrue(src["KR2013-10-08-NETMARBLE-MOBILE-DISTINCT"]["excluded_from_original_pc_roster"])
        self.assertEqual(src["KR2013-10-08-NETMARBLE-MOBILE-DISTINCT"]["pet_name_attestations"], [])
        self.assertEqual(src["CN2013-01-18-DEEP-RED-CAVE-ITEM-NOT-PET"]["pet_name_attestations"], [])
        self.assertIn("NOT_OWNED_PET", src["CN2013-01-18-DEEP-RED-CAVE-ITEM-NOT-PET"]["negative_control"]["entity"])
        self.assertEqual(self.a["native_2013_source"]["original_pet_ids"], 0)
        self.assertEqual(self.a["native_2013_source"]["server_reward_receipts"], 0)

    def test_current_blob_and_stage_guard(self):
        a, q = self.a, self.q
        self.assertEqual(a["baseline"]["current_git_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["baseline"]["current_bytes"], 2709173)
        self.assertTrue(a["historical_current_blob_untouched"])
        self.assertEqual((q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))

if __name__ == "__main__":
    unittest.main()
