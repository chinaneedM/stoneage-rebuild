import json
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-CN2004-SIX-QUEST-STORY-VIGNETTES-R1.json"

class SixVignettes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(FILE.read_text(encoding="utf-8"))
    def test_source_date_and_type(self):
        r=self.r["sources"][0]
        self.assertEqual(r["publication"],"2004-02-11 14:10")
        self.assertEqual(r["visible_author"],"新浪游戏")
        self.assertFalse(r["operator_first_party"])
        self.assertIsNone(r["original_raw_html_sha256"])
    def test_six_nonduplicated_entries(self):
        rows=self.r["task_vignettes"]
        self.assertEqual(len(rows),6)
        self.assertEqual(len(set(x["name"] for x in rows)),6)
        self.assertEqual([x["id"] for x in rows],[f"T{i:02d}" for i in range(1,7)])
        self.assertEqual([x["walkthrough_link_number"] for x in rows],list(range(61,67)))
    def test_five_social_story_hooks_and_one_job_entry(self):
        self.assertEqual(self.r["bounded_summary"]["distinct_story_vignettes_not_jobs"],5)
        self.assertEqual(self.r["profession_groups"],["闇灵法师","追猎者","白狼勇士"])
        self.assertEqual(self.r["identified_actor_strings"],["尊尼","迪克","阿喇吉","契雷多"])
    def test_no_added_runtime_fact(self):
        self.assertTrue(all(not x["quest_steps_verified"] for x in self.r["task_vignettes"]))
        self.assertTrue(all(x["reported_outcome"] is None for x in self.r["task_vignettes"][1:]))
        self.assertEqual(self.r["bounded_summary"]["actual_game_quest_instances"],0)
        self.assertEqual(self.r["bounded_summary"]["original_server_reward_items"],0)
        self.assertFalse(self.r["release_scope"]["source_is_first_party_official_quest_script"])
    def test_2004_friendship_link_is_image_only(self):
        detail=self.r["sources"][1]
        self.assertEqual(detail["url"],"https://games.sina.com.cn/z/sta/2004-02-11/rw4.shtml")
        self.assertEqual(detail["publication"],"2004-02-11 14:40")
        self.assertEqual(detail["qualified_from"],"INDEX_ACTUAL_LINK_64")
        self.assertFalse(detail["visible_text_for_quest_steps"])
        self.assertTrue(detail["main_detail_is_image_references"])
        self.assertEqual(detail["images_opened"],0)
    def test_no_silent_typo_or_version_correction(self):
        b={r["id"]:r["qualification"] for r in self.r["source_boundaries"]}
        self.assertIn("舍身相救s",b["B05"])
        self.assertIn("真低能",b["B05"])
        self.assertIn("6.0/7.0",b["B02"])
        self.assertFalse(self.r["release_scope"]["tw1_original"])
        self.assertFalse(self.r["release_scope"]["jss1999_original"])
    def test_source_boundary_entries(self):
        self.assertEqual(len(self.r["source_boundaries"]),8)
        self.assertTrue(all(x["qualification"] for x in self.r["source_boundaries"]))
    def test_no_artifact_promotion_and_next(self):
        self.assertEqual(self.r["bounded_summary"]["original_proprietary_images_downloaded"],0)
        self.assertEqual(self.r["stage_a"],"7_PARTIAL_2_OPEN")
        self.assertEqual(self.r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-21")
if __name__=="__main__":
    unittest.main()
