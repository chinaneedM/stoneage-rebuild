import unittest
from tools.stoneage_tw10_savedata_inputs_r11 import reaches,semantic,input_queries,inspect_verified
from tools.stoneage_tw10_savedata_provenance_r10 import graph
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
ROOT=0x1000;BASE=0x400000
def nodes(raw):
 d=Decoder(raw,ROOT,BASE);n,e=graph(d,ROOT);return d,n,e
class TestR11(unittest.TestCase):
 def test_eax_initial_zero_and_increment_loop(self):
  d,n,e=nodes(b'\x31\xc0\x40\x39\xd0\x7c\xfb\xc3')
  self.assertEqual(reaches(n,e,ROOT,'eax')[ROOT+3],{('definition',ROOT+2)})
  self.assertEqual(reaches(n,e,ROOT,'eax')[ROOT+2],{('definition',ROOT),('definition',ROOT+2)})
  self.assertEqual(semantic(n[ROOT],'eax',[],BASE)['constant'],0)
  self.assertEqual(semantic(n[ROOT+2],'eax',[],BASE)['constant'],1)
 def test_all_registers_havoc_at_call(self):
  d,n,e=nodes(b'\xe8\x00\x00\x00\x00\xc3')
  for reg in ('eax','ebx','ecx','edx','esi','edi','ebp'):self.assertEqual(reaches(n,e,ROOT,reg)[ROOT+5],{('unknown_call',ROOT)})
 def test_join_retains_both_definitions(self):
  d,n,e=nodes(b'\x74\x05\xbb\x01\x00\x00\x00\xc3')
  self.assertEqual(reaches(n,e,ROOT,'ebx')[ROOT+7],{('entry',ROOT),('definition',ROOT+2)})
 def test_partial_al_write_unknown_full_value(self):
  d,n,e=nodes(b'\xb0\x01\xc3');self.assertEqual(reaches(n,e,ROOT,'eax')[ROOT+2],{('definition',ROOT)})
  self.assertEqual(semantic(n[ROOT],'eax',[],BASE)['kind'],'unmodeled_write')
 def test_sub_self_is_zero(self):
  d,n,e=nodes(b'\x29\xd2\xc3');self.assertEqual(semantic(n[ROOT],'edx',[],BASE)['constant'],0)
 def test_decrement_is_signed_adjustment(self):
  d,n,e=nodes(b'\x4b\xc3');self.assertEqual(semantic(n[ROOT],'ebx',[],BASE)['constant'],-1)
 def test_new_edi_definition_replaces_call_barrier(self):
  d,n,e=nodes(b'\xe8\x00\x00\x00\x00\x89\xf7\xc3')
  self.assertEqual(reaches(n,e,ROOT,'edi')[ROOT+7],{('definition',ROOT+5)})
 def test_pointer_memory_input_stays_conditional(self):
  d,n,e=nodes(b'\x8b\x14\x83\xc3');rows=input_queries(d,n,e,[],((ROOT+3,'edx'),),ROOT)
  s=rows[0]['reaching_sources'][0]['semantic'];self.assertEqual(s['kind'],'memory_load');self.assertEqual(s['memory_input']['index_scale'],4);self.assertFalse(rows[0]['value_fully_known'])
 def test_unsupported_register_rejected(self):
  d,n,e=nodes(b'\xc3')
  with self.assertRaises(ValueError):reaches(n,e,ROOT,'esp')
 def test_wrong_original_identity(self):
  with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'')
if __name__=='__main__':unittest.main()
