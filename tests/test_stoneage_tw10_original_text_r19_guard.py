import copy,json,unittest
from tools.stoneage_tw10_original_text_r19_guard import REPORT,verify,WITNESSES
class R19SourceAcceptance(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.data=json.loads(REPORT.read_text(encoding="utf-8"))
 def test_original_witnesses(self): self.assertTrue(verify(self.data))
 def test_all_sampled_tags_are_provenance_only(self):
  self.assertEqual(sum(len(w) for w in WITNESSES.values()),7)
  self.assertTrue(all(r["entity_id"] is None for x in self.data["executable_observations"].values() for r in x["candidates"]))
 def test_tamper_is_detected(self):
  d=copy.deepcopy(self.data);d["original_npc_pet_quest_identity_mappings_proven"]=1
  with self.assertRaises(AssertionError):verify(d)
if __name__=="__main__":unittest.main()
