"""Preserve complete continuity and do not conflate a source audit with a user decision."""
import json,unittest
from tools.stoneage_stage_a_joint_review_decision import ROOT,DEFAULT,validate,hash_git
R=ROOT/"research/recovered/STONEAGE-STAGE-A-JOINT-REVIEW-ACCEPTANCE-R1.json"
class JointReviewArchiveTests(unittest.TestCase):
 def test_two_complete_historical_prefixes(self):
  receipt=json.loads(R.read_text(encoding="utf-8"))
  for row in receipt["old_full_prefixes"]:
   raw=(ROOT/row["path"]).read_bytes()
   with self.subTest(row["path"]):
    self.assertGreater(len(raw),row["bytes"])
    self.assertEqual(hash_git(raw[:row["bytes"]]),row["sha"])
    self.assertIn(b"STAGE-A-JOINT-REVIEW-DECISION-01",raw[row["bytes"]:])
 def test_receipt_does_not_claim_user_approval(self):
  packet=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(packet["source_head"],"59fd3bcf482226c0d29fa51e840ec3529b2c2b4f")
  self.assertEqual(packet["source_tree"],"d8461ca61d288c49fd1ac3359b50e3d9d5f8cde4")
  self.assertEqual(packet["independent_workflow"]["run_id"],39002948717)
  self.assertEqual(packet["independent_workflow"]["result"],"SUCCESS")
  for key in ("new_original_server_evidence","new_original_playthrough","all_historical_claims_originally_restored",
              "stage_a_user_review_completed","stage_a_accepted","stage_b_started"):
   self.assertIs(packet[key],False)
  self.assertEqual(packet["extra_ci"],"PENDING_NOT_CLAIMED")
  self.assertEqual(packet["main_integration"],"PENDING_NOT_CLAIMED")
 def test_report_mapping_still_valid(self):
  self.assertEqual(validate(json.loads(DEFAULT.read_text(encoding="utf-8")))["status"],"PASS")
if __name__=="__main__":
 unittest.main()
