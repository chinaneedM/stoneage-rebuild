import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"research/recovered/STONEAGE-CN30-WATERCITY-TWO-SOURCE-STORY-BRANCHES-R1.json"

class WatercityBranchComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(SRC.read_text(encoding="utf-8"))

    def test_actual_two_web_sources_with_separate_dates(self):
        s=self.r["sources"]
        self.assertEqual(len(s),2)
        self.assertIsNone(s[0]["original_publication_date"])
        self.assertEqual(s[1]["visible_publication_datetime"],"2003-06-05 15:23")
        self.assertEqual(s[1]["visible_byline"],"新浪游戏")
        self.assertIsNone(s[0]["raw_html_sha256"])
        self.assertIsNone(s[1]["raw_html_sha256"])

    def test_alternative_branch_outcomes_not_single_canon(self):
        b=self.r["branch_model_as_reported_by_sina"]
        self.assertEqual([(r["source_branch"],r["name"]) for r in b],[("A","力之手环"),("B","心之手环")])
        self.assertTrue(all(not r["runtime_verified"] for r in b))
        self.assertEqual(self.r["relationship_assertion"],"STORY_BRANCH_ONLY_NOT_UNIVERSAL_WORLDLINE")

    def test_crafter_conditional(self):
        r=next(d for d in self.r["qualified_differences"] if d["topic"]=="necklace_crafter")
        self.assertIn("莉娜",r["source_17173"])
        self.assertIn("喀尔斯",r["source_sina"])
        self.assertIn("Sina B",r["source_sina"])

    def test_coordinate_conflict_not_offset_rule(self):
        d=next(d for d in self.r["qualified_differences"] if d["topic"]=="npc_coordinates")
        self.assertIn("55",d["source_17173"])
        self.assertIn("54",d["source_sina"])
        self.assertIn("cannot infer",d["scope"])

    def test_level_recommendation_not_minimum(self):
        d=next(d for d in self.r["qualified_differences"] if d["topic"]=="level_requirement")
        self.assertEqual(d["relation"],"MANDATORY_CLAIM_VS_RECOMMENDED_LEVEL")
        self.assertIn("recommendation",d["scope"])

    def test_reward_question_marks_preserved(self):
        d=next(d for d in self.r["qualified_differences"] if d["topic"]=="reward_values")
        self.assertIn("?",d["source_sina"])

    def test_no_original_script_or_tw10_promotion(self):
        self.assertEqual(self.r["material_scope"]["unverified_script_count"],0)
        self.assertEqual(self.r["material_scope"]["tw10_entity_promotions"],0)
        self.assertFalse(self.r["material_scope"]["original_historical_html_sha_verification"])
        self.assertFalse(self.r["candidate_mapping"]["shared_quest_identity_proven"])

    def test_all_eight_relations_anchored(self):
        ds=self.r["qualified_differences"]
        self.assertEqual(len(ds),8)
        self.assertEqual(len(set(d["topic"] for d in ds)),8)
        for d in ds:
            self.assertTrue(d["refs_17173"])
            self.assertTrue(d["refs_sina"])
            self.assertTrue(d["scope"])

    def test_finite_next(self):
        self.assertEqual(self.r["stop"],"ONE_ADDITIONAL_DATED_EDITORIAL_ARTICLE_AFTER_MATERIAL_BRANCH_DISCOVERY_NO_SIBLINGS_NO_IMAGES")
        self.assertEqual(self.r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18")
