import copy
import unittest
from tools.stoneage_album_adrn_material_r37 import check,read_all
class OriginalAlbumAliasContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.obj=read_all()
 def test_positive(self):self.assertEqual(check(*self.obj)['alias_joins'],3)
 def fails(self,index,mutate):
  args=copy.deepcopy(self.obj);mutate(args[index])
  with self.assertRaises(ValueError):check(*args)
 def test_first_failure_not_reclassified(self):self.fails(2,lambda o:o.__setitem__('status','ORIGINAL_ADRN_FULL_HASH_MATCH'))
 def test_logic_not_same_physical(self):self.fails(0,lambda o:o['album_joins']['28001']['adrn_alias_rows'][0].__setitem__('bitmapno',28001))
 def test_name_cannot_change(self):self.fails(0,lambda o:o['album_joins']['28002']['program'].__setitem__('name','wrong'))
 def test_original_sha_pin(self):self.fails(1,lambda o:o['source_member'].__setitem__('sha256','0'*64))
 def test_adrn_source_field_mutation(self):self.fails(1,lambda o:o['selected_metadata']['selected_logical_aliases']['28003'][0].__setitem__('bitmapno',28003))
 def test_duplicate_count(self):self.fails(1,lambda o:o['selected_metadata'].__setitem__('nonzero_duplicate_alias_occurrences',0))
 def test_no_pixel_claim(self):self.fails(0,lambda o:o['unproven'].__setitem__('original_real_pixel_payload_read',True))
 def test_r36_table_cannot_be_revised(self):self.fails(3,lambda o:o['table']['rows'][0].__setitem__('name_gbk','wrong'))
if __name__=='__main__':unittest.main()
