"""PET-DETAIL05: original PC7 operator offer and first-person battle news stay source-scoped."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
class PetDetail05(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=load("research/pets/PET-DETAIL-EVIDENCE05-CN70-2003-2004-OPERATOR-LIVE-COMBAT-R1.json")
  cls.tw=load("research/pets/PET-ID-REGISTRY-R1.json")
  cls.cn=load("research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
 def test_two_old_client_catalogues_are_bounded_and_pinned(self):
  for p,h in self.d["git_source_catalogue_pins"].items():self.assertEqual(blob(p),h)
  self.assertEqual(len(self.tw["catalog_entries"]),124)
  self.assertEqual(len(self.cn["records"]),362)
  for name in self.d["source_name_check"]["exact_names_checked"]:
   self.assertFalse([x for x in self.tw["catalog_entries"] if x["display_name_simplified"]==name])
   self.assertFalse([x for x in self.cn["records"] if x["label_as_compiled_GB18030"]==name])
  self.assertTrue(self.d["source_name_check"]["this_is_only_a_bounded_literal_gap_not_proof_of_nonrelease"])
 def test_2003_offer_2004_report_are_distinct_not_server_table(self):
  a,b,c,d=self.d["records"]
  self.assertEqual(len(self.d["sources"]),3)
  self.assertEqual(len(set(x["id"] for x in self.d["records"])),4)
  self.assertEqual(a["advertised_price_RMB"],198)
  self.assertEqual(a["advertised_quantity_of_pet"],1)
  self.assertTrue(a["advertised_elements_random"])
  self.assertIsNone(a["original_element_random_distribution"])
  self.assertFalse(a["proof_of_actual_retail_account_redemption"])
  self.assertEqual(b["reported_first_round_pet_skill"],"巨毒")
  self.assertEqual(b["reported_opponent_water_wolf_level"],140)
  self.assertFalse(b["same_wolf_as_2003_premium_award_verified"])
  self.assertFalse(b["fire_to_earth_is_base_element_change_proof"])
  self.assertEqual(c["reported_skill_C_set"],["狂暴攻击","沉默","闪避","巨毒","净化"])
  self.assertTrue(c["skill_set_is_individual_report_not_species_innate"])
  self.assertIsNone(c["original_skill_ids"])
  self.assertFalse(d["all_labels_correspond_to_native_species_verified"])
  self.assertFalse(self.d["period_connections"]["same_native_build_and_pet_master_verified"])
  self.assertTrue(self.d["period_connections"]["official_source_7_client_cannot_login_older_182_20_60_servers"])
 def test_no_native_field_species_or_pet_id_promoted(self):
  self.assertEqual(blob("docs/CURRENT-STATE.md"),self.d["fresh_start"]["current_original_git_blob"])
  self.assertEqual(self.tw["counts"]["assigned_catalog_pet_ids"],124)
  for k in ("original_version_verified_native_pet_ids_added","verified_actual_original_official_pet_server_master_rows_added","new_permanent_PET_IDs","additional_official_species_confirmed","official_pet_full_historical_profiles_complete","original_2003_2004_PC_client_bytes_recovered"):self.assertEqual(self.d["counts"][k],0,k)
  self.assertTrue(self.d["additional_2003_operator_advertised_pet_system"]["those_are_player_profession_not_pet_innate_skills"])
  self.assertTrue(self.d["boundaries"]["PET_only_module"])
  self.assertTrue(self.d["boundaries"]["mobile_excluded"])
  t=(ROOT/"docs/pets/CN70-DOUBLEWOLF-PACK-AND-TOURNAMENT-2003-2004.md").read_text(encoding="utf-8")
  self.assertIn("属性随机",t)
  self.assertIn("红肥龙",t)
  self.assertIn("2004-06-18",t)
  self.assertIn("CN70-DOUBLEWOLF-PACK-AND-TOURNAMENT-2003-2004.md",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
