import copy
import json
import unittest
from tools.stoneage_original_observation_source_guard import REPORT,verify
class OriginalObservationSourceGuard(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.data=json.loads(REPORT.read_text(encoding="utf-8"))
 def test_actual_raw_source(self): self.assertTrue(verify(self.data))
 def test_no_identity_promotion(self):
  self.assertEqual(self.data["verified_link_to_original_named_npc_pet_quest"],0)
  self.assertTrue(all(not x["original_colors_reproduced"] for x in self.data["original_image_preview_records"]))
 def test_original_bytes_altered_rejected(self):
  d=copy.deepcopy(self.data)
  d["original_image_preview_records"][0]["decoded_palette_index_sha256"]="0"*64
  with self.assertRaises(AssertionError): verify(d)
 def test_no_false_original_game_boot(self):
  d=copy.deepcopy(self.data);d["original_executable_run_observed"]=True
  with self.assertRaises(AssertionError):verify(d)
if __name__=="__main__":unittest.main()
