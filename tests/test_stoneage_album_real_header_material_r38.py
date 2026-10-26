import copy
import unittest
from tools.stoneage_album_real_header_material_r38 import validate,load,MAT,SRC,R37
class R38HeaderOnlyProvenance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.obj=(load(MAT),load(SRC),load(R37))
 def test_qualified_header_without_pixels(self):
  self.assertIs(validate(*self.obj)['pixels_verified'],False)
 def reject(self,i,fn):
  v=copy.deepcopy(self.obj);fn(v[i])
  with self.assertRaises(ValueError):validate(*v)
 def test_no_source_pixel_claim(self):self.reject(1,lambda z:z.__setitem__('original_REAL_payload_read',True))
 def test_false_RD_claim(self):self.reject(0,lambda z:z['qualification'].__setitem__('actual_RD_headers_verified',True))
 def test_alias_range_offset(self):self.reject(0,lambda z:z['three_adrn_byte_ranges'][0].__setitem__('offset',28001))
 def test_header_length(self):self.reject(1,lambda z:z['receipt']['candidates'][0].__setitem__('bytes',12345))
 def test_missing_header(self):self.reject(1,lambda z:z['receipt']['candidates'].clear())
 def test_invented_official_build(self):self.reject(0,lambda z:z['qualification'].__setitem__('official_same_build_authentication',True))
 def test_hidden_source_row(self):self.reject(2,lambda z:z['album_joins']['28001']['adrn_alias_rows'][0].__setitem__('adder',99))
 def test_source_range_sum(self):self.reject(1,lambda z:z['receipt'].__setitem__('actual_range_bytes',1))
 def test_no_unbounded_compression_promotion(self):self.reject(1,lambda z:z['receipt']['candidates'][0].__setitem__('compressed_bytes',1024))
if __name__=='__main__':unittest.main()
