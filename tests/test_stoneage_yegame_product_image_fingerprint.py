import unittest
from tools.stoneage_yegame_product_image_fingerprint import ORIG,TS,jpeg_size
class FingerprintTests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TS,"20010828031151")
        self.assertIn("EN0ZGKJ0002.jpg",ORIG)
    def test_nonjpeg(self): self.assertIsNone(jpeg_size(b"not-jpeg"))
if __name__=="__main__":unittest.main()
