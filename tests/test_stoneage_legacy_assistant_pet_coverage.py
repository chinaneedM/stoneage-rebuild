import copy,json,unittest
from tools.stoneage_legacy_assistant_pet_coverage import MANIFEST,validate
class Catalog(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=json.loads(MANIFEST.read_text(encoding="utf-8"))
 def check(self,fn):
  x=copy.deepcopy(self.p);fn(x)
  with self.assertRaises(ValueError):validate(x)
 def test_good(self):self.assertEqual(validate(self.p)["status"],"PASS")
 def test_false_all_pet_assertions(self):
  for k in ("original_1999_tool_comprehensive_listing","all_original_pets_identified","all_original_pet_images_mapped","original_pet_growth_table_complete","original_quests_complete","new_game_assistant_production_started","stage_a_bounded_review_reversed"):
   with self.subTest(k=k):self.check(lambda x,k=k:x.__setitem__(k,True))
 def test_resource_not_pet_count(self):self.check(lambda x:x["pet_resource_claim"].__setitem__("pet_species_count",125996))
 def test_late_rows_not_original(self):self.check(lambda x:x["later_enemybase_derived_count"].__setitem__("all_are_unique_1999_pet_species",True))
 def test_unattributed_tool(self):self.check(lambda x:x["assistant_tools"][0].__setitem__("source",["UNKNOWN"]))
 def test_duplicate_lineage(self):self.check(lambda x:x["assistant_tools"][1].__setitem__("id","speedgear"))
 def test_exploit_never_normal(self):self.check(lambda x:x["game_integrated_functions"][-1].__setitem__("decision","HIGH_PRIORITY"))
 def test_scripts_not_auto_approved(self):self.check(lambda x:x["game_integrated_functions"][8].__setitem__("decision","APPROVED_IN_ENGINE"))
 def test_evidence_not_cross_version(self):self.check(lambda x:x["source_layers"].remove("LATER_RECOVERED"))
 def test_source_custody(self):self.check(lambda x:x["external_sources"][0].__setitem__("url","invalid"))
 def test_no_automatic_stage_a_reversal(self):self.check(lambda x:x.__setitem__("conditional_stage_a_reopen","ALL_STAGE_A_REVOKED"))
if __name__=="__main__":unittest.main()
