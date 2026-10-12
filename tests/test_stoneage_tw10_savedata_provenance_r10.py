import struct,unittest
from capstone.x86 import X86_REG_ESI,X86_REG_EFLAGS
from tools.stoneage_tw10_savedata_provenance_r10 import graph,reaches,semantic_definition,inspect_verified
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
BASE=0x400000;ROOT=0x1000

def nodes(raw):
 d=Decoder(raw,ROOT,BASE);n,e=graph(d,ROOT);return d,n,e
class TestR10(unittest.TestCase):
 def test_esi_constant_definition(self):
  d,n,e=nodes(b'\xbe'+struct.pack('<I',0x460000)+b'\x89\x06\xc3')
  self.assertEqual(reaches(n,e,ROOT,X86_REG_ESI)[ROOT+5],{('definition',ROOT)})
  self.assertEqual(semantic_definition(n[ROOT],X86_REG_ESI,[],BASE)['kind'],'constant_assignment')
 def test_unknown_call_clobber_not_silently_preserved(self):
  d,n,e=nodes(b'\xbe'+struct.pack('<I',0x460000)+b'\xe8\x00\x00\x00\x00\x89\x06\xc3')
  self.assertEqual(reaches(n,e,ROOT,X86_REG_ESI)[ROOT+10],{('unknown_call',ROOT+5)})
  self.assertEqual(reaches(n,e,ROOT,X86_REG_ESI,False)[ROOT+10],{('definition',ROOT)})
 def test_new_definition_after_call_replaces_barrier(self):
  d,n,e=nodes(b'\xe8\x00\x00\x00\x00\x89\xce\x89\x06\xc3')
  self.assertEqual(reaches(n,e,ROOT,X86_REG_ESI)[ROOT+7],{('definition',ROOT+5)})
 def test_branch_join_keeps_both_sources(self):
  raw=b'\x74\x05\xbe\x01\x00\x00\x00\x89\x06\xc3';d,n,e=nodes(raw)
  self.assertEqual(reaches(n,e,ROOT,X86_REG_ESI)[ROOT+7],{('entry',ROOT),('definition',ROOT+2)})
 def test_flags_have_exact_cmp_source(self):
  d,n,e=nodes(b'\x83\xfb\x14\x7c\xfb\xc3')
  self.assertEqual(reaches(n,e,ROOT,X86_REG_EFLAGS)[ROOT+3],{('definition',ROOT)})
  p=semantic_definition(n[ROOT],X86_REG_EFLAGS,[],BASE);self.assertEqual(p['kind'],'comparison');self.assertEqual(p['constant'],20);self.assertEqual(p['register_inputs'],['ebx'])
 def test_zero_test_descriptor(self):
  d,n,e=nodes(b'\x85\xf6\x74\x00\xc3')
  p=semantic_definition(n[ROOT],X86_REG_EFLAGS,[],BASE);self.assertEqual(p['kind'],'register_zero_test');self.assertEqual(p['constant'],0)
 def test_flags_call_barrier(self):
  d,n,e=nodes(b'\x85\xf6\xe8\x00\x00\x00\x00\x74\x00\xc3')
  self.assertEqual(reaches(n,e,ROOT,X86_REG_EFLAGS)[ROOT+7],{('unknown_call',ROOT+2)})
 def test_partial_si_write_is_not_full_constant_assignment(self):
  d,n,e=nodes(b'\x66\xbe\x01\x00\xc3');self.assertEqual(semantic_definition(n[ROOT],X86_REG_ESI,[],BASE)['kind'],'unmodeled_write')
 def test_memory_mask_is_derived_predicate(self):
  d,n,e=nodes(b'\xf6\x46\x0c\x83\xc3');p=semantic_definition(n[ROOT],X86_REG_EFLAGS,[],BASE)
  self.assertEqual(p['kind'],'masked_test');self.assertEqual(p['memory_input']['relative_field_offset'],12);self.assertEqual(p['constant'],131)
 def test_wrong_original_identity(self):
  with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'')
if __name__=='__main__':unittest.main()
