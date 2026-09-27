import unittest
from tools.stoneage_yegame_product_image_probe import CODE,URLS,cdx_url
class ImageProbeTests(unittest.TestCase):
    def test_code(self): self.assertEqual(CODE,"EN0ZGKJ0002")
    def test_source_path(self):
        self.assertTrue(any("/product_images/EN0ZGKJ0002.jpg" in u for u in URLS))
        self.assertTrue(any("/product_images2/EN0ZGKJ0002.jpg" in u for u in URLS))
    def test_exact(self): self.assertIn("matchType=exact",cdx_url(URLS[0]))
if __name__=="__main__": unittest.main()
