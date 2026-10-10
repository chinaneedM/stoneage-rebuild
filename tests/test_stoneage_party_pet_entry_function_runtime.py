import unittest
from tools.stoneage_party_pet_entry_function_runtime import PROFILES,NAMES,FEATURES,C_HEAD,C_CASES
class PartyPetNativeHarnessTests(unittest.TestCase):
 def test_source_scope(self):
  self.assertEqual(PROFILES,("gavin","bismarck"))
  self.assertEqual(len(NAMES),3)
  self.assertEqual(len(FEATURES),2)
 def test_explicit_stubs(self):
  self.assertIn("typedef struct",C_HEAD)
  self.assertIn("int BATTLE_NewEntry",C_HEAD)
 def test_negative_coverage(self):
  for t in ("dead selected pet rejected","zero hp selected pet rejected","pet NewEntry failure masked","leader error early return","busy member and pet excluded","unrelated party roster exp unchanged"):
   self.assertIn(t,C_CASES)
 def test_no_runtime_overclaim(self):
  self.assertIn("integrated_battle=OPEN",C_CASES)
  self.assertIn("#ifdef AUDIT_BISMARCK",C_CASES)
if __name__=="__main__":unittest.main()
