import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet25_official_release_query import select
class TestPET25OfficialRelease(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads((ROOT/"research/recovered/STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json").read_text(encoding="utf-8"))
 def test_release_count_not_species(self):
  d=self.d; a=d["confirmed_official_release_records"]
  self.assertEqual(len(a),24)
  self.assertIsNone(d["counts"]["strict_unique_species_global"])
  self.assertEqual(d["counts"]["named_pet_or_form_records"],19)
  self.assertEqual(d["counts"]["family_level_unsplit_records"],5)
  self.assertEqual(d["counts"]["original_native_runtime_pet_records_verified"],0)
  self.assertTrue(all(not x["counts_as_unique_global_species"] for x in a))
 def test_source_and_no_private_server(self):
  d=self.d; source={s["id"] for s in d["source_register"]}
  self.assertEqual(len(source),16)
  self.assertEqual(len({r["record_id"] for r in d["confirmed_official_release_records"]}),24)
  for r in d["confirmed_official_release_records"]:
   self.assertEqual(r["status"],"OFFICIAL_IN_GAME_RELEASE_DOCUMENTED")
   self.assertTrue(r["counts_as_operator_release_record"])
   self.assertFalse(r["source_is_user_private_server_only"])
   self.assertFalse(r["native_in_game_runtime_personally_verified"])
   self.assertTrue(r["source_ids"])
   self.assertTrue(set(r["source_ids"])<=source)
 def test_cross_region_and_product_independent(self):
  by=self.d["counts"]["per_product_line"]
  self.assertEqual(sorted(by.values()),[1,2,3,5,13])
  self.assertEqual(len(select(self.d,region="CN")),20)
  self.assertEqual(len(select(self.d,region="KR")),4)
  self.assertEqual(len(select(self.d,product="STONEAGE_CLASSIC_PC_CN_HUAYI")),5)
  self.assertEqual(len(select(self.d,name="机械萌龙")),4)
  self.assertEqual(len(select(self.d,name="机豹")),0)
  self.assertEqual(len(select(self.d,name="艾迪希洛")),1)
 def test_preview_and_server_name_not_in_official_roster(self):
  d=self.d; leads=d["remaining_unconfirmed_official_leads"]
  self.assertEqual(len(leads),4)
  self.assertEqual(len(select(d,only_leads=True,name="海胆")),1)
  self.assertEqual(len(select(d,name="海胆")),0)
  self.assertTrue(all(not x["counts_in_release_records"] for x in leads))
  self.assertTrue(all(x["status"]=="UNVERIFIED_RELEASE_OR_IDENTITY_NOT_COUNTED" for x in leads))
 def test_exact_issue_known_examples(self):
  d=self.d; r={x["record_id"]:x for x in d["confirmed_official_release_records"]}
  self.assertEqual(r["CN-PC-4-MECHLEOPARD"]["parent_pet_family_as_source_or_null"],"机豹")
  self.assertEqual(r["CN-PC-MONKEY-2003"]["official_name_as_written"],"蒙奇")
  self.assertEqual(r["CN-AWAKEN-2026-FATDRAGON"]["record_identity_kind"],"FAMILY_OR_CARD_SERIES")
  self.assertEqual(r["KR-WORLD-2020-PUGON"]["official_name_as_written"],"푸곤")
  self.assertIsNone(r["CN-PC-3-YEAR"]["first_qualifying_release_date_or_null"])
 def test_stable_current_state_and_earlier_web_snapshot(self):
  self.assertEqual(self.d["preserved_current_state_original_git_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(self.d["counts"]["official_web_positions_without_release_proof_from_PET24"],228)
  self.assertEqual(self.d["active_module"],"PET")
  self.assertEqual(self.d["stage_A"],"7_PARTIAL_2_OPEN")
if __name__=="__main__":unittest.main()
