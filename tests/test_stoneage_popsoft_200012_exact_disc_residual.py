import unittest
from tools.stoneage_popsoft_200012_exact_disc_residual import HASHES,url

class T(unittest.TestCase):
 def test_hashes(self):
  self.assertEqual(len(HASHES),2)
  self.assertIn("1D674459E1EC61706A688AA73C94DFDC1802C074",{x[1] for x in HASHES})
  self.assertIn("97CF4340916C39D9AA56278C6B86615E8D486DEC",{x[1] for x in HASHES})
 def test_url(self):
  self.assertIn("qfields=t",url(HASHES[0][1]))
if __name__=="__main__":
 unittest.main()
