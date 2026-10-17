"""Check full pre-change Git blob prefix plus source-verified resource crosswalk receipt."""
import json,unittest
from tools.stoneage_pet_asset_growth_catalog import ROOT,gitblob
from tools.stoneage_pet_asset_growth_catalog import inspect_repository_metadata
R=ROOT/"research/recovered/STONEAGE-PET-ASSET-GROWTH-CATALOG-ACCEPTANCE-R1.json"
C=ROOT/"research/recovered/STONEAGE-PET-ASSET-GROWTH-CATALOG-MATRIX-R1.json"
class ExactOldHistory(unittest.TestCase):
 def test_append_only_old_prefixes(self):
  m=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual(len(m["historical_exact_prefixes"]),2)
  for row in m["historical_exact_prefixes"]:
   with self.subTest(row["path"]):
    raw=(ROOT/row["path"]).read_bytes()
    self.assertGreater(len(raw),row["bytes"])
    self.assertEqual(gitblob(raw[:row["bytes"]]),row["blob"])
 def test_receipt_matches_real_source(self):
  receipt=json.loads(R.read_text(encoding="utf-8"))
  catalog=json.loads(C.read_text(encoding="utf-8"))
  self.assertEqual(gitblob(C.read_bytes()),receipt["resource_report_git_blob"])
  self.assertEqual(catalog["resource_report"],inspect_repository_metadata())
  self.assertEqual({x["run"] for x in receipt["independent_ci"]},{39024292573,39024503298})
  self.assertTrue(all(x["conclusion"]=="SUCCESS" for x in receipt["independent_ci"]))
  self.assertEqual(receipt["next"],"ORIGINAL-UI-LOGIN-AVATAR-REVIEW-01")
  for field in ("species_identity_crosswalk_complete","original_pet_growth_complete","original_client_render_runtime_executed","new_proprietary_payload_added","stage_b_started"):
   self.assertFalse(receipt[field])
  self.assertIn(receipt["archival_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
  self.assertIn(receipt["main_integration_ci"],("PENDING_NOT_CLAIMED","SUCCESS"))
if __name__=="__main__":unittest.main()
