import unittest
from tools.stoneage_pet126p_cn50_album_io import (
 bounded_instructions,source_call_context,short_entry,exact_global_literal_sites,infer_numeric_layout_only
)
class PET126P(unittest.TestCase):
 def test_call_context_and_target_range(self):
  i=[{"address":0x430665,"encoded_length":1,"instruction":"push ebp"},
     {"address":0x430666,"encoded_length":3,"instruction":"push 0x485830"},
     {"address":0x430669,"encoded_length":5,"instruction":"call   0x45f182"},
     {"address":0x43066e,"encoded_length":2,"instruction":"add esp,8"},
     {"address":0x430670,"encoded_length":1,"instruction":"ret"}]
  self.assertEqual(len(bounded_instructions(i,0x430665,0x430671)),5)
  context=source_call_context(i,radius=2)
  self.assertEqual(len(context),1)
  self.assertEqual([x["instruction"] for x in context[0]["nearest_previous"]],["push ebp","push 0x485830"])
  self.assertEqual(exact_global_literal_sites(i,0x485830)[0]["va"],0x430666)
  self.assertTrue(short_entry(i,0x430669)["decoded"])
  self.assertFalse(short_entry(i,0x420000)["decoded"])
 def test_bounded_source_does_not_allow_empty_or_missing(self):
  with self.assertRaises(ValueError):bounded_instructions([],0x430665,0x430750)
  with self.assertRaises(ValueError):bounded_instructions([{"address":0x430666,"encoded_length":2,"instruction":"ret"}],0x430665,0x430750)
  with self.assertRaises(ValueError):bounded_instructions([],0x430750,0x430665)
 def test_305_times_80_plus_16_arithmetic_is_not_alone_disk_evidence(self):
  rows=[{"raw_i32":k} for k in [0,1,-1,305,361]]
  observed=infer_numeric_layout_only(rows)
  self.assertTrue(observed["block_stride_equals_16_plus_305_times_80"])
  self.assertEqual(observed["first_i32_values_greater_equal_305"],2)
  self.assertTrue(observed["compiled_slot_number_to_per_account_file_offset_unverified"])

if __name__=="__main__":unittest.main()
