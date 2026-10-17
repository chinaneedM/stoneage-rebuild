import unittest
from tools.stoneage_sta252_feature_witness import derive,FEATURES
class FeatureTests(unittest.TestCase):
 def doc(self):return '<div id="newsriqi">2002-03-10</div><div id="zhuozhe_left">☆阿仇☆</div>天使的外挂 sta2.52 '+ ' '.join(x[2]for x in FEATURES)+' 本文言论'
 def test_requests_not_available(self):
  r=derive(self.doc());p={f['feature_id']:f for f in r['features']};self.assertEqual(p['automatic_script_resume']['evidence_status'],'REQUESTED_NOT_VERIFIED_AVAILABLE');self.assertFalse(r['all_STA252_features_recovered'])
 def test_menu_is_not_working_behavior(self):
  p={f['feature_id']:f for f in derive(self.doc())['features']};self.assertEqual(p['special_character_action_conditions']['evidence_status'],'MENU_PRESENT_BEHAVIOR_UNVERIFIED')
 def test_unknown_release_date(self):self.assertIsNone(derive(self.doc())['version_release_date_verified'])
 def test_missing_claim_not_silently_invented(self):
  with self.assertRaises(ValueError):derive(self.doc().replace('自动恢复脚本',''))
if __name__=='__main__':unittest.main()
