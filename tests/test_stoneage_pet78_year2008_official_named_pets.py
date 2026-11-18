"""PET78: 2008 DigiPark contemporaneous named pet evidence without species inflation."""
import json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"/"recovered"
def get(name): return json.loads((R/name).read_text(encoding="utf-8"))
class TestPet78(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=get("STONEAGE-PET78-2008-JP-NAMED-PET-POOL-AND-SOURCE-GATES-R1.json")
  cls.q=get("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.p=get("STONEAGE-PET77-YEAR2008-OFFICIAL-PET-PARTIAL-SOURCE-AUDIT-R1.json")
 def test_year_remains_2008_and_two_receipts_unique(self):
  a,q=self.a,self.q;year=q["yearly_work_queue"][9]
  # PET78 snapshot remains a 2008 source review after the next year starts.
  self.assertEqual((a["year"],a["current_cursor_after"]),(2008,2008))
  self.assertGreaterEqual(q["current_frontier"]["year"],2008)
  self.assertEqual(year["research_gate"],"NOT_YEAR_AUDITED" if q["current_frontier"]["year"]==2008 else "SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(a["historically_complete"])
  self.assertEqual(sum(x["id"]==a["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(sum(x["id"]==a["id"] for x in year["partial_source_review_receipts"]),1)
  self.assertEqual(sum(x["id"]==self.p["id"] for x in q["root_source_census_receipts"]),1)
  ids=[x["id"] for x in q["root_source_census_receipts"]]
  self.assertEqual(len(ids),len(set(ids)))
 def test_original_japanese_nine_exact_names_vs_korea_and_2007(self):
  a=self.a;names=["ナイトゲイル","クロウテール","ウロボス","コギラス","ペイン","ガンジャー","スネイル","ギガロス","ギガンボス"]
  self.assertEqual(a["japan_2008_random_pool_names_ordered"],names)
  self.assertEqual(a["japan_2008_nine_pool_overlap_previous_2007"],["ウロボス"])
  s={x["id"]:x for x in a["source_records"]}
  self.assertEqual(s["JP2008-0922-FUKAE_NINE_NAMED_POOL"]["random_pet_pool_ordered"],names)
  self.assertEqual(s["JP2008-0922-FUKAE_NINE_NAMED_POOL"]["source_named_entry_count"],9)
  self.assertEqual(s["KR2008-0114-ICECASTLE_RECHECK"]["verified_original_korean_pet_names"],0)
  self.assertEqual(s["JP2008-0707-RIMFY-OFFICIAL_RELEASE"]["pet_name"],"リムフィ")
  self.assertEqual(s["JP2008-0707-RIMFY-OFFICIAL_RELEASE"]["other_story_character_name_not_proven_obtainable"],"リムファン")
 def test_2009_later_evolution_named_but_no_backdating(self):
  a=self.a;s={x["id"]:x for x in a["source_records"]}
  old=s["JP2008-1111-INPUT_EVOLUTION_CROSS_YEAR"]
  new=s["JP2009-1013-EVOLVED_NAMES_LATER_SOURCE"]
  self.assertEqual(old["input_pet_names"],["ベルガー","ベルイガー","ゴルシス","キングサーベル"])
  self.assertEqual(new["evolved_pet_names_ordered"],["ベガルガー","ゴッドサーベル","ベルロイガー","ギルシス"])
  self.assertEqual(new["attestation_year"],2009)
  self.assertFalse(new["source_2008_first_appearance_proven"])
  self.assertEqual(new["input_output_pairings_proven"],0)
 def test_year_2008_unknown_population_and_boundaries(self):
  a=self.a
  self.assertTrue(all(a["source_boundaries"].values()))
  self.assertEqual(set(a["region_status"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual((a["counts_and_limits"]["raw_original_2008_client_bytes_new"],a["counts_and_limits"]["original_2008_native_pet_ids_new"],a["counts_and_limits"]["original_2008_server_grant_logs_new"]),(0,0,0))
  self.assertIsNone(a["counts_and_limits"]["worldwide_2008_species_population_verified"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
 def test_historical_current_git_blob_preserved(self):
  raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
