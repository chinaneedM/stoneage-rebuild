import unittest
from tools.stoneage_jss_login_manual_probe import derive,linked_manual01,creation_contract
class ManualTests(unittest.TestCase):
 def test_real_capture_not_request_date(self):
  r=derive('<a name="100"><p>キャラクター 作成</p><img src="c.gif" width="640">'.encode('shift_jis'),'https://web.archive.org/web/20010501000000id_/http://www.titan.co.jp/stoneage/manual01.html','manual01.html')
  self.assertEqual(r['actual_capture'],'20010501000000');self.assertFalse(r['historical_layout_verified'])
  self.assertEqual(r['image_references'][0]['original_url'],'http://www.titan.co.jp/stoneage/c.gif')
 def test_fragment_is_same_manual_document(self):
  self.assertEqual(linked_manual01(['http://www.titan.co.jp/stoneage/manual01.html#2015']),'http://www.titan.co.jp/stoneage/manual01.html')
 def test_other_origin_rejected(self):
  with self.assertRaises(ValueError):derive(b'anything','https://example.com/manual01.html','manual01.html')
 def test_html_dimensions_are_not_image_byte_dimensions(self):
  r=derive(b'<img src="x.gif" width="999">','https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html','manual02.html')
  self.assertEqual(r['image_references'][0]['html_width'],'999');self.assertFalse(r['image_references'][0]['image_bytes_acquired'])
class CreationContractTests(unittest.TestCase):
 def sections(self):return {'1010':'ID NUMBER パスワード 太陽 月 別の世界','1020':'全角８文字 能力値20ポイント 属性値10ポイント 三属性以上 できません 方向 カラー 顔 出身村','1040':'削除確認 OK'}
 def test_source_version_is_separate(self):
  r=creation_contract(self.sections());self.assertEqual(r['initial_stat_allocation_points'],20);self.assertFalse(r['same_rules_proven_in_tw10'])
 def test_changed_number_requires_requalification(self):
  s=self.sections();s['1020']=s['1020'].replace('20ポイント','30ポイント')
  with self.assertRaises(ValueError):creation_contract(s)
 def test_no_max_two_from_silent_source(self):
  s=self.sections();s['1020']=s['1020'].replace('三属性以上','')
  with self.assertRaises(ValueError):creation_contract(s)
if __name__=='__main__':unittest.main()
