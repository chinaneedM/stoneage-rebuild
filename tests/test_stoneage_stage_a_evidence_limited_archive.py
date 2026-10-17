"""Guard complete historical prefixes and the real delegated approval receipt."""
from __future__ import annotations
import json,unittest
from tools.stoneage_stage_a_evidence_limited_acceptance import ROOT,DEFAULT,validate,blob
RECEIPT=ROOT/"research/recovered/STONEAGE-STAGE-A-EVIDENCE-LIMITED-ACCEPTANCE-RECEIPT-R1.json"
class ArchivePreservationTests(unittest.TestCase):
 def test_old_prefix_exact_git_blob(self):
  r=json.loads(RECEIPT.read_text(encoding="utf-8"))
  self.assertEqual(len(r["historical_original_prefixes"]),5)
  for row in r["historical_original_prefixes"]:
   with self.subTest(row["path"]):
    b=(ROOT/row["path"]).read_bytes()
    self.assertGreater(len(b),row["bytes"])
    self.assertEqual(blob(b[:row["bytes"]]),row["blob"])
 def test_real_source_failure_never_recast_success(self):
  r=json.loads(RECEIPT.read_text(encoding="utf-8"))
  self.assertEqual(r["early_source_ci"]["run"],39004208069)
  self.assertEqual(r["early_source_ci"]["conclusion"],"failure")
  self.assertTrue(r["early_source_ci"]["preserved"])
  self.assertEqual(r["source_commit"],"b4c5cf7fb43216c6fbb1b591c6863d95182156a5")
 def test_later_decision_does_not_overwrite_old(self):
  p=json.loads(DEFAULT.read_text(encoding="utf-8"))
  self.assertEqual(validate(p)["status"],"PASS")
  r=json.loads(RECEIPT.read_text(encoding="utf-8"))
  self.assertTrue(r["stage_a_research_review_accepted"])
  self.assertFalse(r["entire_original_game_restored"])
  self.assertFalse(r["stage_b_production_started"])
  self.assertIn(r["archive_ci"]["status"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertIn(r["post_merge_ci"]["status"],("PENDING_NOT_CLAIMED","SUCCESS"))
if __name__=="__main__":
 unittest.main()
