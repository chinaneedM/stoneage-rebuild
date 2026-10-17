import unittest
from tools.stoneage_jss_login_manual_probe import derive
class ManualTests(unittest.TestCase):
 def test_real_capture_not_request_date(self):
  r=derive('<a name="100"><p>キャラクター 作成</p><img src="c.gif" width="640">'.encode('shift_jis'),'https://web.archive.org/web/20010501000000id_/http://www.titan.co.jp/stoneage/manual01.html','manual01.html')
  self.assertEqual(r['actual_capture'],'20010501000000');self.assertFalse(r['historical_layout_verified'])
  self.assertEqual(r['image_references'][0]['original_url'],'http://www.titan.co.jp/stoneage/c.gif')
 def test_other_origin_rejected(self):
  with self.assertRaises(ValueError):derive(b'anything','https://example.com/manual01.html','manual01.html')
 def test_html_dimensions_are_not_image_byte_dimensions(self):
  r=derive(b'<img src="x.gif" width="999">','https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html','manual02.html')
  self.assertEqual(r['image_references'][0]['html_width'],'999');self.assertFalse(r['image_references'][0]['image_bytes_acquired'])
if __name__=='__main__':unittest.main()
