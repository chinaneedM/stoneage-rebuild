import unittest
from tools.stoneage_party_pet_realheader_audit import BODY,patch_source
class RealHeaderAdmissionTests(unittest.TestCase):
 def test_real_slots_and_ownership(self):
  for x in ("CHAR_initCharOneArray(&pet)","BATTLE_CreateVsEnemy(0,0,-1)","Entry[5]","CHAR_WORKPLAYERINDEX","CHAR_WORKGETEXP","searchObjectFromCharaIndex"):
   self.assertIn(x,BODY)
 def test_explicit_exit_gate(self):
  self.assertIn("Exit is intentionally not asserted",BODY)
 def test_patch_requires_actual_signature(self):
  with self.assertRaises(ValueError):patch_source("not an original source", "gavin")
 def test_scoped_profile_collectors(self):
  s="".join(f"if(charaindex!=0)abort();{c}++;" for c in ("ca_count","cd_count","status_count","skill_count"))
  s+='int getfdFromCharaIndex(int actor){if(actor!=0)abort();fd_count++;return -1;}'
  s+='void CHAR_sendWatchEvent(int index,int act,int *opt,int len,int mine){if(index!=0||act!=CHAR_ACTBATTLE||!opt||len!=3||mine!=1)abort();}'
  self.assertIn("index!=0&&index!=1",patch_source(s,"gavin"))
  self.assertIn("actor!=0&&actor!=1",patch_source(s,"gavin"))
  for c in ("ca_count","cd_count","status_count","skill_count"):
   self.assertIn("charaindex!=0&&charaindex!=1",patch_source(s,"gavin"))
if __name__=="__main__":unittest.main()
