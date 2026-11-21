"""PET126O static original helper call-target inspection (synthetic)."""
import unittest
from tools.stoneage_pet126o_cn50_bounded_helpers import direct_calls,entry_context,read_file_backed_cstring

class Pet126O(unittest.TestCase):
 def test_original_helper_call_extraction_is_exact_not_indirect(self):
  code=[{"address":0x401000,"instruction":"call   0x45f560","encoded_length":5},
        {"address":0x401005,"instruction":"call   0x430665","encoded_length":5},
        {"address":0x40100a,"instruction":"call   DWORD PTR [eax+0x45f560]","encoded_length":6}]
  self.assertEqual([x["caller_va"] for x in direct_calls(code,0x45f560)],[0x401000])
  self.assertEqual([x["caller_va"] for x in direct_calls(code,0x430665)],[0x401005])
 def test_function_is_bounded_not_implicitly_complete(self):
  code=[{"address":0x430665,"instruction":"push   ebp","encoded_length":1},
        {"address":0x430666,"instruction":"mov    ebp,esp","encoded_length":2},
        {"address":0x430668,"instruction":"ret","encoded_length":1}]
  got=entry_context(code,0x430665)
  self.assertTrue(got["decoded_entry"])
  self.assertEqual(got["first_return_va_within_window"],0x430668)
  self.assertTrue(got["limited_lookahead_not_complete_control_flow"])
  self.assertFalse(entry_context(code,0x432222)["decoded_entry"])
 def test_read_printable_static_cstring_not_virtual_only(self):
  img=bytearray(1024)
  img[300:307]=b"pet.dat"
  s=[{"virtual_rva":0x1000,"raw_offset":300,"raw_size":100}]
  got=read_file_backed_cstring(bytes(img),0x400000,s,0x401000)
  self.assertEqual(got["short_literal"],"pet.dat")
  self.assertTrue(got["ascii_printable"])
  self.assertFalse(read_file_backed_cstring(bytes(img),0x400000,s,0x405000)["file_backed"])

if __name__=="__main__":unittest.main()
