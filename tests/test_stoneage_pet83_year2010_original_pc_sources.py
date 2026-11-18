"""PET83 2010 source-bounded original PC pet roster: test reward != promotional pet != original native ID."""
import unittest,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"research"/"recovered"
def load(n): return json.loads((DATA/n).read_text(encoding="utf-8"))
class PET83(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=load("STONEAGE-PET83-YEAR2010-CN85-ORIGINAL-CLIENT-MERMAID-WHALES-OTHER-REGION-BOUNDARIES-R1.json")
  cls.q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_cursor_and_append_only_receipts(self):
  a,q=self.a,self.q; y=q["yearly_work_queue"][2010-1999]
  self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"],q["current_frontier"]["year"]),(2010,2010,2010,2010))
  self.assertEqual(y["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["current_frontier"]["latest_partial_root_review"],a["id"])
  self.assertFalse(a["historically_complete"])
  self.assertEqual(sum(x["id"]==a["id"] for x in y["partial_source_review_receipts"]),1)
  self.assertEqual(sum(x["id"]==a["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
  self.assertEqual(y["documented_release_event_ids_from_existing_PET25_PET26"],[])
 def test_client_md5_source_not_native_file(self):
  a=self.a;s={r["id"]:r for r in a["sources"]}
  cli=s["CN2010-1111-85-FIRST-TEST-INSTALLER-MD5"]
  self.assertEqual(cli["stated_md5"],"cd0ac0c0bc26bcfefdd08957d8d86e7c")
  self.assertEqual(cli["stated_size"],"1.19G")
  self.assertFalse(cli["md5_observed_in_original_bytes"])
  self.assertEqual(cli["installer_original_bytes_acquired"],0)
  self.assertNotEqual(cli["stated_md5"],cli["different_later_2012_download_md5"])
 def test_mermaid_test_vs_whales_only_promo(self):
  a=self.a;s={r["id"]:r for r in a["sources"]}
  test=s["CN2010-1113-85-FIRST-TEST-MERMAID"]
  self.assertEqual((test["advertised_pet_name"],test["event_start"],test["event_end"]),("人鱼","2010-11-13","2010-11-17"))
  self.assertFalse(test["first_in_live_production_verified"])
  self.assertIsNone(test["native_pet_id"])
  five=s["CN2010-1222-85-FIVE-WHALE-PROMO"]
  names=[x["caption_name"] for x in five["names_properties"]]
  self.assertEqual(names,["夏克","夏莫","夏波","夏基","夏乐地"])
  self.assertEqual([x["literal_element"] for x in five["names_properties"]],["水","风","地","火","地水"])
  self.assertEqual(five["names_properties"][1]["body_name_variant"],"下莫")
  self.assertTrue(five["source_article_says_non_deletion_test_still_upcoming"])
  self.assertFalse(five["actual_live_release_verified"])
  self.assertEqual((a["new_named_official_test_reward_labels"],a["new_named_operator_promo_visual_candidates"]),(1,5))
  self.assertIsNone(a["confirmed_2010_first_new_species"])
 def test_regional_version_and_stage_guards(self):
  a=self.a;s={r["id"]:r for r in a["sources"]}
  self.assertFalse(s["TW2010-TAOZHU-DIGIPARK-OPERATOR-AGREEMENT"]["server_live_2010_verified"])
  self.assertEqual(s["TW2010-TAOZHU-DIGIPARK-OPERATOR-AGREEMENT"]["contract_sign_date"],"2010-10-12")
  self.assertFalse(s["JP2010-012-019-PLANNED-MAPS-PETS"]["applied_updates_verified"])
  self.assertEqual(s["KR2010-1216-CJ-NEW-SKY-SERVER"]["new_server_name"],"하늘")
  self.assertEqual(s["KR2010-1216-CJ-NEW-SKY-SERVER"]["pet_species_count_from_level_cap"],0)
  self.assertIsNone(s["KR2010-1223-CJ-UNNAMED-EVENT-PET-BOX"]["event_pet_original_name"])
  self.assertEqual(s["KR-LATER-PLAYER-2010-CHRONOLOGY-UNVERIFIED"]["count_as_2010_first_releases"],0)
  self.assertTrue(all(a["evidence_gates"].values()))
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertTrue(all(v["species_population"] is None for v in a["region_reviews"].values()))
  self.assertEqual((a["new_authenticated_2010_client_bytes"],a["new_native_2010_pet_ids"],a["new_actual_original_server_reward_logs"]),(0,0,0))
  self.assertTrue(a["no_paid_sellers"] and a["no_proprietary_assets_in_git"])
 def test_current_original_blob_unchanged(self):
  raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),self.a["startup"]["full_original_current_git_blob"])
  self.assertEqual((self.a["stage_A"],self.a["stage_B_wiki"],self.a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
if __name__=="__main__":unittest.main()
