import unittest
from types import SimpleNamespace
from tools.stoneage_album_real_header_r38 import selected_expected,classify_header,TARGET
class HeaderQualification(unittest.TestCase):
 def info(self,name,flags=0,size=200):
  return SimpleNamespace(filename=name,file_size=size,compress_size=120,flags=flags,compress_type=53,header_offset=123,data_offset=256,CRC=234)
 def test_preserved_independent_header(self):
  row=classify_header(self.info(TARGET));self.assertTrue(row['exact_expected_member_name'])
  self.assertTrue(row['is_independent_member']);self.assertEqual(row['bytes'],200)
 def test_split_solid_and_encrypted_are_not_independent(self):
  for mask in (1,2,4,16,17):
   with self.subTest(mask=mask):
    self.assertFalse(classify_header(self.info(TARGET,mask))['is_independent_member'])
 def test_unrelated_member_is_not_same_carrier_real(self):
  row=classify_header(self.info('stoneage2.5/data/real_158.bin'))
  self.assertFalse(row['exact_expected_member_name'])
 def test_three_expected_original_adrn_offsets_only(self):
  from tools.stoneage_album_adrn_material_r37 import read_all
  m,s,f,o=read_all();rows=selected_expected(m)
  self.assertEqual([(x['logical_alias'],x['physical_bitmapno'],x['offset'],x['size']) for x in rows],
   [(28001,7246,26119737,9521),(28002,7247,26129258,9678),(28003,7248,26138936,9304)])
if __name__=='__main__':unittest.main()
