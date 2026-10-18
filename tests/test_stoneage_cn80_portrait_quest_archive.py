import json
import unittest
from pathlib import Path

class ArchiveContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(Path("research/recovered/STONEAGE-CN80-PORTRAIT-QUEST-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads(Path("research/recovered/STONEAGE-CN80-PORTRAIT-QUEST-CATALOG-R1.json").read_text(encoding="utf-8"))
    def test_source_hash_identity(self):
        s=self.a["source_chain"]
        self.assertEqual(s["index"]["bytes"],34236)
        self.assertEqual(s["detail"]["bytes"],24459)
        self.assertEqual(s["index"]["actual_named_href"],s["detail"]["url"])
        self.assertEqual(s["detail"]["sha256"],"328571c2dbabbb337f27f06a76ecaf3eeae621fdad4a0979d8089e980dfd8e19")
        self.assertFalse(s["page_bytes_retained_in_git"])
    def test_pet_join_and_reward_are_descriptive_only(self):
        p=self.a["pet_to_pigment"]
        self.assertEqual(self.a["step_count"],14)
        self.assertEqual([x["source_step_capture"] for x in p],[3,5,7,9,11])
        self.assertEqual([x["source_step_turn_in"] for x in p],[4,6,8,10,12])
        self.assertEqual([x["pigment_color"] for x in p],["红色","黄色","黑色","白色","蓝色"])
        self.assertEqual(self.b["quest_count"],1)
        self.assertFalse(self.b["quest_state_machine_executable"])
        self.assertFalse(self.a["completion"]["server_script_or_actual_reward_state_proven"])
    def test_cross_version_prerequisite_not_assumed(self):
        old,late=self.b["prerequisite_evidence"]
        self.assertEqual(old["claimed_version"],"8.0")
        self.assertIsNone(old["stated_prerequisite"])
        self.assertFalse(old["no_prerequisite_inferred"])
        self.assertEqual(late["claimed_version"],"8.5")
        self.assertEqual(late["requires_prior_quest"],"无法逃离的审判")
        self.assertEqual(late["reported_reward_count_from_narrative"],1)
        self.assertFalse(late["independent_original_server_script"])
    def test_missing_original_identifiers(self):
        self.assertTrue(all(x is None for x in self.a["unknowns"].values()))
        self.assertFalse(self.a["name_variants"]["identity_equivalence_confirmed"])
        self.assertFalse(self.b["same_build_tw10_proven"])
        self.assertFalse(self.a["r79_unpaused"])
if __name__=="__main__":
    unittest.main()
