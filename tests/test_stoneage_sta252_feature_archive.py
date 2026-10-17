import hashlib,json,unittest
from pathlib import Path
from tools.stoneage_sta252_feature_witness import FEATURES
ROOT=Path(__file__).resolve().parents[1]
class ArchiveTests(unittest.TestCase):
 def test_source_and_code_custody(self):
  r=json.loads((ROOT/'research/recovered/STONEAGE-LEGACY-STA252-ACCEPTANCE-R1.json').read_text())
  for f,p in r['reports'].items():self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),p['sha256'])
 def test_requests_and_failed_observations_keep_their_status(self):
  r=json.loads((ROOT/'research/recovered/STONEAGE-LEGACY-STA252-FEATURES-R1.json').read_text())
  self.assertEqual({f['feature_id']:f['evidence_status']for f in r['features']},{a:b for a,b,_,_ in FEATURES})
  self.assertFalse(r['software_executed']);self.assertFalse(r['all_STA252_features_recovered'])
  self.assertTrue(all(not f['adoption_decided']and not f['implemented_in_rebuild']for f in r['features']))
if __name__=='__main__':unittest.main()
