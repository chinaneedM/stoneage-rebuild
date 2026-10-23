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

if __name__=="__main__":
    unittest.main()
