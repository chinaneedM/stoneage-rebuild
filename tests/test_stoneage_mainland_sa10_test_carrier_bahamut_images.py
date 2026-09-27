import unittest
from tools.stoneage_mainland_sa10_test_carrier_bahamut_images import PAGE, ANCHORS, article_images, image_dimensions

class T(unittest.TestCase):
    def test_target(self):
        self.assertIn("snA=81396", PAGE)
        self.assertTrue(any("測試說明書" in a for a in ANCHORS))

    def test_image_extraction(self):
        raw='<img src="https://truth.bahamut.com.tw/s01/202009/example.JPG">'
        rows=article_images(raw)
        self.assertEqual(len(rows),1)
        self.assertIn("truth.bahamut.com.tw",rows[0][1])

    def test_png_dimensions(self):
        body=b"\x89PNG\r\n\x1a\n"+b"\x00"*8+(12).to_bytes(4,"big")+(34).to_bytes(4,"big")
        w,h,fmt=image_dimensions(body)
        self.assertEqual((w,h,fmt),(12,34,"png"))

if __name__=="__main__":
    unittest.main()
