"""The 22-domain plan retains all original source grades without asserting completed gameplay."""
import unittest, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NEW=ROOT/"research/recovered/STONEAGE-22-DOMAIN-SOURCE-READY-PORTFOLIO-R2.json"
OLD=ROOT/"research/recovered/STONEAGE-22-DOMAIN-EVIDENCE-COVERAGE-CHECKPOINT-R1.json"

class SourceReadyPortfolio(unittest.TestCase):
 def test_original_statuses_preserved(self):
  d=json.loads(NEW.read_text(encoding="utf-8"))
  old=json.loads(OLD.read_text(encoding="utf-8"))
  self.assertEqual(d["domain_count"],22)
  self.assertEqual(len(d["all_domain_rows"]),22)
  self.assertEqual({x["domain_id"] for x in d["all_domain_rows"]}, {x["domain_id"] for x in old["reviewed_domains"]})
  for x in d["all_domain_rows"]:
   prior=next(y for y in old["reviewed_domains"] if y["domain_id"]==x["domain_id"])
   self.assertEqual(x["original_order"],prior["original_order"])
   self.assertEqual(x["baseline_evidence_status"],prior["baseline_evidence_status"])
   self.assertEqual(x["missing_original_evidence"],prior["remaining_material_gap"])
   self.assertFalse(x["version_promotion_allowed"])
   self.assertFalse(x["original_source_complete"])
 def test_no_stage_transition_or_percent(self):
  d=json.loads(NEW.read_text(encoding="utf-8"))
  self.assertTrue(d["historical_statuses_unchanged"])
  self.assertTrue(d["source_readiness_is_not_restoration_completion"])
  self.assertTrue(d["blocked_same_build_npc_and_pet_quests_preserved"])
  self.assertEqual(d["system_family_review"],"7_PARTIAL_2_OPEN")
  self.assertFalse(d["stage_b_production_started"])
  self.assertFalse(d["original_game_world_fully_restored"])
  self.assertIsNone(d["overall_restoration_percentage"])
  self.assertEqual(d["current_execution"]["id"],"T01_SPR_ACTION_CATEGORY_SOURCE_JOIN")
if __name__=="__main__": unittest.main()
