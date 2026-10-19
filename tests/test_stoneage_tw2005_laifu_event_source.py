import json
from pathlib import Path
import unittest

FILE=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-TW2005-LAIFU-EVENT-SOURCE-R1.json"

class LaifuEventSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(FILE.read_text(encoding="utf-8"))
    def test_task_and_next(self):
        self.assertEqual(self.r["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19")
        self.assertEqual(self.r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-20")
    def test_period_press_not_firstparty_web_or_server(self):
        p=self.r["historical_sources"][0]
        self.assertEqual(p["visible_publication_datetime"],"2005-04-20 19:26:02")
        self.assertEqual(p["journalist"],"小賢")
        self.assertFalse(p["operator_first_party_website"])
        self.assertIsNone(p["original_byte_sha256"])
        self.assertFalse(p["press_report_is_server_runtime_replay"])
        self.assertEqual(p["direct_browser_open"],"HTTP_403")
    def test_later_guide_edit_date_not_original_post(self):
        guide=self.r["historical_sources"][1]
        self.assertEqual(guide["visible_edited_datetime"],"2006-10-04 18:22:48")
        self.assertIsNone(guide["first_post_date"])
        self.assertFalse(guide["first_party_operator_source"])
        self.assertIsNone(guide["original_byte_sha256"])
    def test_quest_named_pet_actor_and_story(self):
        p=self.r["press_qualified_2005"]["quest"]
        self.assertEqual((p["named_child"],p["reported_reward_name"]),("乎契","萊福"))
        self.assertIsNone(p["father_name"])
        self.assertIsNone(p["reward_pet_template_id"])
        self.assertEqual(p["mission_document"],"任務委託書")
        self.assertTrue(self.r["press_qualified_2005"]["separate_product"]["separate_from_mission"])
    def test_no_2005_skill_formula_inference(self):
        p=self.r["press_qualified_2005"]["reported_pet_skill"]
        self.assertEqual(p["name"],"相棲共生")
        for field in ["numeric_threshold","action_type","cost","activation_policy"]:
            self.assertIsNone(p[field])
        self.assertFalse(p["client_runtime_verified"])
    def test_later_player_guide_has_eight_bounded_steps(self):
        g=self.r["later_guide_as_reported"]
        self.assertEqual([i["id"] for i in g["numbered_guide_steps"]],list(range(1,9)))
        self.assertIn("乎卓",g["npc_names"])
        self.assertIn("多格樂",g["npc_names"])
        self.assertFalse(g["npc_spawn_verified"])
        self.assertTrue(g["craft_grade_and_quantity_not_confirmed"])
    def test_qualifier_relations_all_accounted_for(self):
        rel=self.r["source_relations"]
        self.assertEqual(len(rel),9)
        self.assertEqual([r["id"] for r in rel],[f"SR{i:02d}" for i in range(1,10)])
        for row in rel:
            self.assertTrue(row["boundary"])
            self.assertTrue(row["press"])
            self.assertTrue(row["guide"])
    def test_no_identity_merge_of_pet_and_distributor(self):
        r={x["id"]:x for x in self.r["source_relations"]}
        self.assertIn("cannot automatically equal",r["SR06"]["boundary"])
        self.assertIn("Do not promote",r["SR04"]["boundary"])
    def test_no_original_runtime_or_artifact(self):
        v=self.r["original_version_identification"]
        self.assertIsNone(v["precise_executable_build"])
        self.assertFalse(v["original_TW10"])
        self.assertFalse(v["original_JSS1999"])
        self.assertEqual(v["original_server_quest_executions"],0)
        self.assertEqual(self.r["art_and_rights"]["original_client_binary_committed"],0)
        self.assertEqual(self.r["historical_status"]["domains_22_promoted"],0)

if __name__=="__main__":
    unittest.main()
