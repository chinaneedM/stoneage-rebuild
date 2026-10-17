import unittest
import importlib.util
from tools.stoneage_tw10_login_avatar_probe import push_source
from tools.stoneage_tw10_login_avatar_probe import select_calls,inspect_runtime
class ScopeTests(unittest.TestCase):
 def test_wrong_version_rejected_before_decoding(self):
  with self.assertRaisesRegex(ValueError,'SHA256'):inspect_runtime(b'later client')
 def test_candidate_bounds_not_nearest_function_claim(self):
  rows=[{'target_rva':v} for v in [99,100,131,132,133]]
  self.assertEqual(select_calls(rows,132),rows[1:4])
 def test_empty_does_not_invent_entry(self):self.assertEqual(select_calls([],100),[])
@unittest.skipUnless(importlib.util.find_spec('capstone'), 'capstone available in original-source CI')
class RegisterSourceTests(unittest.TestCase):
 def source(self,raw):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
  ins=list(md.disasm(bytes.fromhex(raw),0x401000))
  return push_source(ins,len(ins)-1,0x400000)
 def test_absolute_load(self):
  x=self.source('a10000500050')
  self.assertEqual((x['kind'],x['address_rva'],x['width_bytes']),('absolute_memory_load',0x100000,4))
 def test_clobber_is_not_old_load(self):self.assertEqual(self.source('a10000500031c050')['kind'],'unresolved')
 def test_partial_clobber_is_not_full_register_source(self):self.assertEqual(self.source('a10000500066b8010050')['kind'],'unresolved')
 def test_call_breaks_source_chain(self):self.assertEqual(self.source('a100005000e80000000050')['kind'],'unresolved')
 def test_indexed_memory_is_not_fixed_selector(self):self.assertEqual(self.source('8b04055000500050')['kind'],'unresolved')
if __name__=='__main__':unittest.main()
