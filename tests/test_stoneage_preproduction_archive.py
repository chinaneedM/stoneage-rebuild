"""Adversarial checks: catalogs are not completed gameplay, no bogus UI or website."""
import unittest,json,copy
from tools.stoneage_preproduction_archive import PATH,validate
class PreproductionCoverageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=json.loads(PATH.read_text(encoding="utf-8"))
 def invalid(self,change):
  v=copy.deepcopy(self.p);change(v)
  with self.assertRaises(ValueError):validate(v)
 def test_valid(self):
  r=validate(self.p);self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["domains"],22);self.assertEqual(r["versions"],7)
  self.assertEqual(r["web_collections"],19)
 def test_no_premature_completeness(self):
  for flag in ("all_historical_quests_complete","all_historical_pets_complete","all_login_and_ui_frames_complete","all_external_helper_functions_complete","website_implementation_started"):
   with self.subTest(flag):self.invalid(lambda v,flag=flag:v["status"].__setitem__(flag,True))
 def test_no_mistaking_bitmaps_for_pets(self):
  self.invalid(lambda v:v["tw10_asset_census"].__setitem__("species_count",125996))
 def test_no_mistaking_descendant_template_for_original(self):
  self.invalid(lambda v:v["descendant_pet_probe"].__setitem__("original_v1_species_count",988))
 def test_no_forged_original_rendering(self):
  self.invalid(lambda v:v["tw10_ui_structural_sources"][0].__setitem__("renderVerified",True))
 def test_unproven_crosswalk_kept_unproven(self):
  self.invalid(lambda v:v["relationship_requirements"][0].__setitem__("same_build_runtime_verified",True))
 def test_no_undocumented_helper_exhaustion(self):
  self.invalid(lambda v:v["legacy_helper_corpus"].__setitem__("all_features_semantically_reconstructed",True))
 def test_historical_source_must_remain_versioned(self):
  self.invalid(lambda v:v["version_profiles"][3].__setitem__("can_backfill",True))
 def test_rights_approval_explicit(self):
  self.invalid(lambda v:v["future_website"]["record_contract"]["export_rules"].remove("Public release only when rights_status=RELEASE_APPROVED"))
 def test_missing_major_domain_rejected(self):
  self.invalid(lambda v:v["domains"].pop(1))
 def test_missing_wiki_collection_rejected(self):
  self.invalid(lambda v:v["future_website"]["required_collections"].remove("screens"))
 def test_built_website_is_false(self):
  self.invalid(lambda v:v["future_website"].__setitem__("website_development_started",True))
if __name__=="__main__":unittest.main()
