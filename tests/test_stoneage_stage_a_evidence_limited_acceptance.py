"""Adversarial tests of the separate, reversible Stage A user-delegated gate."""
from copy import deepcopy
import json,unittest
from tools.stoneage_stage_a_evidence_limited_acceptance import DEFAULT,validate
class EvidenceLimitedAcceptTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=json.loads(DEFAULT.read_text(encoding="utf-8"))
 def mutated(self,section,key,val):
  p=deepcopy(self.p);p[section][key]=val;return p
 def test_valid_checkpoint_without_game_completion(self):
  r=validate(self.p);self.assertTrue(r["bounded_review_accepted"])
  self.assertFalse(r["original_game_restored"]);self.assertFalse(r["production_started"])
 def test_no_forged_user_authorization(self):
  for k,v in [("delegated_by_user",False),("selected_option","CONTINUE_STAGE_A_NAMED_EVIDENCE"),("stage_a_review_accepted",False),("scope","COMPLETE_GAME_RESTORED"),("reversible_by_new_evidence",False),("authorization_utterance","continue")]:
   with self.subTest(k=k),self.assertRaises(ValueError):validate(self.mutated("decision",k,v))
 def test_no_historical_fabrication(self):
  for k in ("full_original_game_restored","complete_original_commercial_playthrough","original_1999_exact_build_restored","original_server_world_npc_quest_rewards_recovered","commercial_saac_durable_relogin_verified","original_ui_real_execution_restored","new_original_content_this_decision"):
   with self.subTest(k=k),self.assertRaises(ValueError):validate(self.mutated("historical_status",k,True))
  with self.assertRaises(ValueError):validate(self.mutated("historical_status","overall_restoration_percent",100))
 def test_no_premature_engine_or_production(self):
  for k in ("collaborative_new_game_design_ratified","production_approved","engine_final_selected","engine_build_started","new_world_story_assets_authorized_for_production"):
   with self.subTest(k=k),self.assertRaises(ValueError):validate(self.mutated("stage_b",k,True))
  with self.assertRaises(ValueError):validate(self.mutated("stage_b","status","PRODUCTION_STARTED"))
 def test_no_losing_open_families_or_services(self):
  with self.assertRaises(ValueError):validate(self.mutated("historical_status","family_gates",{"PARTIAL":9,"OPEN":0}))
  with self.assertRaises(ValueError):validate(self.mutated("historical_status","early_services_open",0))
  p=deepcopy(self.p);p["family_ids"].pop()
  with self.assertRaises(ValueError):validate(p)
 def test_no_source_rewrite(self):
  p=deepcopy(self.p);p["source_pins"]["review"]["blob"]="0"*40
  with self.assertRaises(ValueError):validate(p)
  p=deepcopy(self.p);p["append_only_prefixes"][0]["blob"]="0"*40
  with self.assertRaises(ValueError):validate(p)
 def test_no_source_layer_or_riding_promotion(self):
  p=deepcopy(self.p);p["design_scope"]["source_roles"].remove("NEW_DESIGN")
  with self.assertRaises(ValueError):validate(p)
  p=deepcopy(self.p);p["design_scope"]["first_mount"]="ORIGINAL_TW10_CERTIFIED"
  with self.assertRaises(ValueError):validate(p)
 def test_reopen_policy_must_stay_narrow(self):
  p=deepcopy(self.p);p["reopen_policy"]["trigger"]="ANY_LATER_SERVER_NUMBER"
  with self.assertRaises(ValueError):validate(p)
if __name__=="__main__":
 unittest.main()
