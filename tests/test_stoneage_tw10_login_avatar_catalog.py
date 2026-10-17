import copy,json,unittest,hashlib
from tools.stoneage_tw10_login_avatar_catalog import ROOT,REPORT,build_catalog,validate_catalog
class CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=build_catalog()
 def test_immutable_derived_archive_replays(self):
  self.assertEqual(json.loads((ROOT/REPORT).read_text()),self.report)
 def test_source_custody_and_full_historical_prefixes(self):
  r=json.loads((ROOT/'research/recovered/STONEAGE-TW10-LOGIN-AVATAR-ACCEPTANCE-R1.json').read_text())
  for f,pin in r['continuity_prefixes'].items():
   b=(ROOT/f).read_bytes();self.assertGreater(len(b),pin['bytes']);self.assertEqual(hashlib.sha256(b[:pin['bytes']]).hexdigest(),pin['sha256'])
  for f,pin in r['reports'].items():
   b=(ROOT/f).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),pin['sha256'])
 def test_separate_login_envelopes(self):
  p={r['protocol']:r for r in self.report['protocols']}
  self.assertEqual((p['ClientLogin']['send']['string_fields'],p['ClientLogin']['recv']['string_fields']),(2,1))
  self.assertEqual((p['CreateNewChar']['send']['int_fields'],p['CreateNewChar']['send']['string_fields']),(12,1))
  self.assertEqual((p['CharList']['send']['int_fields'],p['CharList']['send']['string_fields']),(0,0))
 def reject(self,key,value):
  r=copy.deepcopy(self.report);r[key]=value
  with self.assertRaises(ValueError):validate_catalog(r)
 def test_prevent_roster_invention(self):self.reject('original_character_count',12)
 def test_prevent_visual_promotion(self):self.reject('original_screen_layout_verified',True)
 def test_prevent_fake_runtime_success(self):self.reject('original_server_login_success_verified',True)
 def test_body_and_face_not_automatic_same_image(self):
  fields=self.report['create_payload_fields'];self.assertNotEqual(fields[2]['static_operand_source']['address_rva'],fields[3]['static_operand_source']['address_rva'])
  r=copy.deepcopy(self.report);r['create_payload_fields'][2]['selected_spr_group']=100000
  with self.assertRaises(ValueError):validate_catalog(r)
if __name__=='__main__':unittest.main()
