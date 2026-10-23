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

    def test_actual_ci_publication_receipt_and_derived_blob(self):
        import hashlib
        from pathlib import Path
        p = P.parents[2] / "research/recovered/STONEAGE-CN2003-GOYA-PIG-NPC-ACCEPTANCE-R91.json"
        receipt = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(receipt["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91")
        raw = P.read_bytes()
        src = receipt["derived_source_json"]
        self.assertEqual(src["raw_utf8_bytes"], len(raw))
        self.assertEqual(src["git_blob_sha1"], hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest())
        self.assertFalse(src["contains_original_html"])
        self.assertIsNone(receipt["source_limit"]["raw_original_html_sha256"])
        self.assertIsNone(receipt["source_limit"]["raw_original_http_bytes"])
        self.assertEqual(receipt["candidate_content_validation"]["tests_passed"], 7)
        self.assertEqual(receipt["candidate_content_validation"]["conclusion"], "success")
        for key, count in [("candidate_continuity_validation", 9), ("main_publication_validation", 11)]:
            obj = receipt[key]
            self.assertEqual(len(obj["run_ids"]), count)
            self.assertEqual(len(set(obj["run_ids"])), count)
            self.assertTrue(obj["all_success"])
        self.assertEqual(receipt["main_publication_validation"]["r91_dedicated_run_id"], 39945765609)
        self.assertFalse(receipt["scope"]["does_not_promote_runtime"] is False)
        self.assertFalse(receipt["scope"]["stage_a_accepted"])
        self.assertFalse(receipt["scope"]["stage_b_open"])
        self.assertIsNone(receipt["scope"]["overall_restoration_percentage"])

if __name__=="__main__":
    unittest.main()
