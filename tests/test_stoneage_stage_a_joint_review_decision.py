"""Adversarial gates for cross-family Stage A user decision material."""
import copy,json,unittest
from tools.stoneage_stage_a_joint_review_decision import DEFAULT,validate
class JointReviewDecisionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.packet=json.loads(DEFAULT.read_text(encoding="utf-8"))
 def test_baseline(self):
  self.assertEqual(validate(self.packet),{"status":"PASS","families":9,"flows":7,"blockers":5,"early_services":5,"stage_a_accepted":False,"stage_b":"GATED"})
 def test_no_implicit_approval(self):
  for k in ("user_explicit_decision_received","stage_a_user_review_completed","stage_a_accepted","stage_b_started","production_engine_started"):
   x=copy.deepcopy(self.packet);x["approval_state"][k]=True
   with self.subTest(k=k),self.assertRaises(ValueError):validate(x)
 def test_no_inferred_100_percent_or_original_runtime(self):
  for k in ("original_1999_exact_build_covered","complete_v1_original_playthrough_certified","original_early_server_world_npc_quest_recovered","original_saac_durable_write_relogin_verified","original_ui_rendering_verified"):
   x=copy.deepcopy(self.packet);x["evidence_guard"][k]=True
   with self.subTest(k=k),self.assertRaises(ValueError):validate(x)
  x=copy.deepcopy(self.packet);x["evidence_guard"]["restoration_total_percent"]=100
  with self.assertRaises(ValueError):validate(x)
 def test_no_missing_service_or_flows(self):
  x=copy.deepcopy(self.packet);x["service_to_blockers"].pop()
  with self.assertRaises(ValueError):validate(x)
  x=copy.deepcopy(self.packet);x["flow_to_blockers"].pop()
  with self.assertRaises(ValueError):validate(x)
 def test_unbound_flow_blocker_denied(self):
  x=copy.deepcopy(self.packet);x["flow_to_blockers"][0]["blockers"]=["UNKNOWN_BLOCKER"]
  with self.assertRaises(ValueError):validate(x)
 def test_future_gate_and_option_approval_not_inferred(self):
  x=copy.deepcopy(self.packet);x["approval_state"]["selected_option"]="ACCEPT_EVIDENCE_LIMITED_STAGE_A_REVIEW"
  with self.assertRaises(ValueError):validate(x)
  x=copy.deepcopy(self.packet);x["default_on_ordinary_continue"]="START_STAGE_B"
  with self.assertRaises(ValueError):validate(x)
 def test_pins_prevent_unnoticed_source_replacement(self):
  x=copy.deepcopy(self.packet);x["source_pins"]["review"]["git_blob"]="0"*40
  with self.assertRaisesRegex(ValueError,"pin"):validate(x)
if __name__=="__main__":
 unittest.main()
