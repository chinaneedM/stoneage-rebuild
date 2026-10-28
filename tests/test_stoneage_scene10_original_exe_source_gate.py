"""Offline verification of 43 private call descriptions and source-byte rejecting gate."""
import copy,json,struct,unittest
from tools.stoneage_scene10_original_exe_source_gate import validate_candidate,rel32_target,check_source,CANDIDATE,EXE_SHA
class BoundedSourceGate(unittest.TestCase):
 def setUp(self):self.c=json.loads(CANDIDATE.read_text())
 def test_candidate_only(self):self.assertEqual(validate_candidate(self.c),43)
 def test_swap_target_refused(self):
  c=copy.deepcopy(self.c);c['paths'][0]['direct_calls'][0]['target_va']=0
  with self.assertRaises(ValueError):validate_candidate(c)
 def test_drop_intervening_refused(self):
  c=copy.deepcopy(self.c);c['paths'][2]['direct_calls'].pop()
  with self.assertRaises(ValueError):validate_candidate(c)
 def test_outer_path_not_promoted(self):
  c=copy.deepcopy(self.c);c['paths'][0]['full_outer_path_executed']=True
  with self.assertRaises(ValueError):validate_candidate(c)
 def test_no_world_promotion(self):
  c=copy.deepcopy(self.c);c['original_world_entered']=True
  with self.assertRaises(ValueError):validate_candidate(c)
 def test_direct_relative_call(self):
  exe=bytearray(0x80000);at=0x44944a;t=0x42a924;off=at-0x400000;exe[off:off+5]=bytes([0xe8])+struct.pack('<i',t-(at+5))
  actual,digest=rel32_target(exe,at);self.assertEqual(actual,t);self.assertEqual(len(digest),64)
 def test_other_opcode_rejected(self):
  exe=bytearray(0x80000)
  with self.assertRaisesRegex(ValueError,'not direct'):rel32_target(exe,0x44944a)
 def test_bad_exe_sha_rejected(self):
  with self.assertRaisesRegex(ValueError,'SHA mismatch'):check_source(bytes(561152),self.c)
 def test_out_of_range_rejected(self):
  with self.assertRaisesRegex(ValueError,'outside'):rel32_target(bytearray(2),0x44944a)
 def test_no_source_assertion(self):self.assertFalse(self.c['original_exe_independently_qualified'])
if __name__=='__main__':unittest.main()
