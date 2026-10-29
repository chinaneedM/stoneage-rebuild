import unittest
from tools.stoneage_scene18_graphic16048_adrn import rows,KEY,MAX_BYTES,MAX_REQUESTS
class Scene18IndependentBounds(unittest.TestCase):
 def test_exact_target_key(self):self.assertEqual(KEY,16048)
 def test_finite_http_byte_budget(self):self.assertLessEqual(MAX_BYTES,64*1024*1024)
 def test_finite_range_request_budget(self):self.assertLessEqual(MAX_REQUESTS,1024)
 def test_fake_adrn_rejected(self):
  with self.assertRaisesRegex(ValueError,"whole original ADRN15 hash"):rows(b"\x00"*80)
if __name__=="__main__":unittest.main()
