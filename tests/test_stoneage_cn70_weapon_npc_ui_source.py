"""Bounded original-vs-guide-and-screenshot counterexamples for R93."""
import copy
import json
import unittest
from tools.stoneage_cn70_weapon_npc_ui_source import P, verify

class R93SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(P.read_text(encoding="utf-8"))
    def reject(self, modify):
        x = copy.deepcopy(self.d)
        modify(x)
        with self.assertRaises(AssertionError): verify(x)
    def test_original_source_pinned(self):
        self.assertTrue(verify(self.d))
    def test_original_provenance_not_upgrade(self):
        self.reject(lambda x:x["source"].update(official_guide=True))
        self.reject(lambda x:x["source"].update(client_build="official-7.0.0"))
        self.reject(lambda x:x["source"].update(original_html_sha256="fake"))
    def test_guide_requirement_is_not_universal_server_gate(self):
        self.reject(lambda x:x["scene"].update(hidden_conditions_excluded_by_source=True))
        self.reject(lambda x:x["scene"].update(original_npc_id=66293))
    def test_quest_branch_items_are_not_mutated(self):
        self.reject(lambda x:x["routes"][0]["items"].pop())
        self.reject(lambda x:x["routes"][1]["items"].reverse())
    def test_exact_reward_text_is_not_normalized(self):
        self.reject(lambda x:x["routes"][0].update(reward_magic_text="昏迷的精灵"))
        self.reject(lambda x:x["routes"][1]["reward_stats"].update(target_count=5))
    def test_conflicting_stick_name_not_resolved(self):
        self.reject(lambda x:x["source_text_conflicts"][1].update(footnote_name="近藏的棍棒"))
        self.reject(lambda x:x["source_text_conflicts"][1].update(which_is_original_item_name="近藏的棍棒"))
    def test_static_screenshot_not_orig_runtime(self):
        self.reject(lambda x:x["screenshot"].update(button_function_executed=True))
        self.reject(lambda x:x["screenshot"].update(original_screenshot_capture_date="2003-10-27"))
        self.reject(lambda x:x["execution"].update(original_ui_runtime_recovered=True))
    def test_screenshot_article_link_unknown(self):
        self.reject(lambda x:x["screenshot"].update(linked_article_html_img_tag_verified=True))
        self.reject(lambda x:x["screenshot"].update(original_image_bytes_sha256="invented"))
    def test_stage_gate_unchanged(self):
        self.reject(lambda x:x["acceptance"].update(stage_a_closed=True))
        self.reject(lambda x:x["acceptance"].update(overall_restoration_percentage=98))
    def test_extra_unverified_field_rejected(self):
        self.reject(lambda x:x.update(original_quest_script="confirmed"))

    def test_actual_ci_acceptance_receipt_and_blob_identity(self):
        import hashlib
        from pathlib import Path
        path = P.parents[2] / "research/recovered/STONEAGE-CN70-WEAPON-COLLECTION-NPC-UI-ACCEPTANCE-R93.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["schema"], "stoneage.cn70_weapon_npc_ui_content_acceptance.r93")
        self.assertEqual(receipt["accepted_main_content_commit"], "8b95c2571034b164008d7f2f80e118f0ad9b3585")
        raw = P.read_bytes()
        source = receipt["source_derived_json"]
        self.assertEqual(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(), source["git_blob_sha1"])
        self.assertIsNone(source["raw_source_html_sha256"])
        self.assertIsNone(source["raw_screenshot_sha256"])
        self.assertFalse(source["original_binaries_embedded"])
        runs = receipt["original_validation"]
        self.assertEqual(runs["source_candidate_run_id"], 39951549696)
        self.assertEqual(runs["source_candidate_job_id"], 120406954551)
        self.assertEqual(runs["source_candidate_static_tests"], 10)
        self.assertEqual(runs["source_candidate_conclusion"], "success")
        self.assertEqual(len(set(runs["candidate_continuity_runs"])), 9)
        self.assertEqual(len(set(runs["main_content_runs"])), 11)
        self.assertTrue(runs["candidate_continuity_all_success"])
        self.assertTrue(runs["main_content_all_success"])
        self.assertEqual(runs["main_dedicated_run_id"], 39952020028)
        self.assertEqual(runs["main_dedicated_job_id"], 120408510653)
        self.assertEqual(runs["main_dedicated_conclusion"], "success")
        self.assertEqual(runs["main_dedicated_artifact_count"], 0)
        self.assertFalse(receipt["acceptance_receipt_commit_ci_verified_at_generation"])
        self.assertTrue(all(v is False for k,v in receipt["scope"].items() if k != "overall_restoration_percentage"))
        self.assertIsNone(receipt["scope"]["overall_restoration_percentage"])
        self.assertEqual(receipt["next"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-94")

if __name__=="__main__":
    unittest.main()
