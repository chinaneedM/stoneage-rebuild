"""Negative-boundary and precise ordered flow tests for R91."""
import copy
import json
import unittest
from tools.stoneage_cn2003_goya_pig_npc_flow_source import P, verify

class TestGoyaPigNpcFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))

    def test_baseline(self):
        self.assertTrue(verify(self.d))
    def reject(self, mutation):
        x=copy.deepcopy(self.d)
        mutation(x)
        with self.assertRaises(AssertionError):
            verify(x)
    def test_different_entry_coordinates_not_flattened(self):
        self.reject(lambda x:x["coordinate_frames"].update(cave_world_entry_footer=[99,425]))
        self.reject(lambda x:x["coordinate_frames"].update(entry_coordinates_equivalent_proven=True))
    def test_reader_suggestion_not_gate_and_no_original_ids(self):
        self.reject(lambda x:x.update(suggested_level_not_gate=80))
        self.reject(lambda x:x["guide_rewards"].update(original_item_ids=[123]))
    def test_pet_not_two_guaranteed_and_stat_exact(self):
        self.reject(lambda x:x["guide_rewards"].update(pet_alternatives=["特洛昆","呼拔拔","乌力斯凯"]))
        self.reject(lambda x:x["guide_rewards"]["bracelet"].update(agility=2))
    def test_dialogue_not_verbatim_and_two_contacts(self):
        self.reject(lambda x:x["interaction_flow"][5].update(talk_count_in_guide=1))
        self.reject(lambda x:x["interaction_flow"][3].update(dialogue_verbatim=True))
    def test_no_runtime_or_source_authority_escalation(self):
        self.reject(lambda x:x["execution"].update(original_server_executed=True))
        self.reject(lambda x:x["source"].update(raw_html_sha256="fabricated"))
        self.reject(lambda x:x["acceptance"].update(stage_a_closed=True))
    def test_order_and_reward_cannot_be_swapped(self):
        self.reject(lambda x:x["interaction_flow"].reverse())
        self.reject(lambda x:x["interaction_flow"][4].update(out=["月光花，需付费"]))
        self.reject(lambda x:x["interaction_flow"][2].update(out=["宠物：两只保证获得"]))

if __name__=="__main__":
    unittest.main()
