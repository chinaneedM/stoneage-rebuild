import copy, json, unittest
from tools.stoneage_scene17_derived_acceptance import REPORT, validate

class TestSource17Actual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=json.loads(REPORT.read_bytes())
 def mutate(self,fn):
  b=copy.deepcopy(self.base);fn(b)
  with self.assertRaises(ValueError):validate(b)
 def test_source_report_actual_replay(self):
  self.assertEqual(validate(self.base)["authored_NPC_at_63_103"],1)
 def test_false_official_build_promotion(self):
  self.mutate(lambda r:r.update(official_tw10_NPC_identity_authenticated=True))
 def test_false_original_game_entered(self):
  self.mutate(lambda r:r.update(original_client_world_entered=True))
 def test_wrong_candidate_graphic(self):
  self.mutate(lambda r:r["source_qualification"]["matched_candidates"][0]["numeric_source_fields"].update(graphicname=16049))
 def test_neighbor_coordinate_not_allowed(self):
  self.mutate(lambda r:r["source_qualification"]["matched_candidates"][0].update(borncorner=[63,102,63,102]))
 def test_wrong_template_function(self):
  self.mutate(lambda r:r["source_qualification"]["matched_candidates"][0].update(functionset_token="ItemShop"))
 def test_duplicate_candidate_not_promoted(self):
  self.mutate(lambda r:r["source_qualification"].update(matched_count=2))
 def test_uncertified_original_member(self):
  self.mutate(lambda r:r["receipt"]["two_original_members"][0].update(sha256="0"*64))
 def test_second_decoder_failure_not_turned_success(self):
  self.mutate(lambda r:r["receipt"]["two_original_members"][1].update(dual_decompressor_byte_equal=False))
 def test_missing_range_witness(self):
  self.mutate(lambda r:r["receipt"]["range_receipts"].pop())
 def test_range_duplicate_rejected(self):
  self.mutate(lambda r:r["receipt"]["range_receipts"][1].update(start=r["receipt"]["range_receipts"][0]["start"],part=r["receipt"]["range_receipts"][0]["part"]))
 def test_source_ban_publishing_proprietary_scripts(self):
  self.mutate(lambda r:r["receipt"].update(original_NPC_scripts_uploaded=True))
 def test_source_name_is_fingerprint_only(self):
  self.mutate(lambda r:r["source_qualification"]["matched_candidates"][0].update(original_dialogue="invented"))
 def test_source_http_bytes_conserved(self):
  self.mutate(lambda r:r["receipt"].update(http206_bytes=12013837))
 def test_cannot_replace_source_with_public_simulation(self):
  self.mutate(lambda r:r.update(original_member_hashes_verified=False))
if __name__=="__main__":unittest.main()
