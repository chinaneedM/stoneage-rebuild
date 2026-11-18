"""PET80: 2009 five-region source-bounded first pass; exact named rewards and no inflated 229 roster."""
import json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
def read(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
class PET80Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=read("STONEAGE-PET80-YEAR2009-JP-KR-OFFICIAL-PET-PARTIAL-SOURCE-AUDIT-R1.json")
  cls.q=read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_annual_2009_open_and_both_append_only_receipts(self):
  a,q=self.a,self.q
  y=q["yearly_work_queue"][2009-1999]
  self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"],q["current_frontier"]["year"]),(2009,2009,2009,2009))
  self.assertEqual(y["research_gate"],"NOT_YEAR_AUDITED")
  self.assertFalse(a["historically_complete"])
  self.assertEqual(q["current_frontier"]["latest_partial_root_review"],a["id"])
  self.assertEqual(sum(r["id"]==a["id"] for r in y["partial_source_review_receipts"]),1)
  self.assertEqual(sum(r["id"]==a["id"] for r in q["root_source_census_receipts"]),1)
  self.assertEqual(len({r["id"] for r in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
  self.assertEqual(y["documented_release_event_ids_from_existing_PET25_PET26"],["JP-2009-HAKUEN","JP-2009-KOKUEN"])
 def test_operator_named_japanese_two_existing_and_distinct_gates(self):
  a=self.a;s={r['id']:r for r in a['sources']}
  self.assertEqual(s["JP2009-0428-HAKUEN"]["pet_name"],"ハクエン")
  self.assertEqual(s["JP2009-0629-KOKUEN"]["pet_name"],"コクエン")
  self.assertEqual(s["JP2009-0428-HAKUEN"]["pet_exchange_ticket"],"白炎交換チケット")
  self.assertEqual(s["JP2009-0629-KOKUEN"]["pet_exchange_ticket"],"黒炎交換チケット")
  self.assertEqual(s["JP2009-0629-KOKUEN"]["announced_new_pet_update_date"],"2009-06-23")
  self.assertEqual(s["JP2009-0629-KOKUEN"]["hangame_site_renewal_date"],"2009-06-25")
  self.assertEqual(s["JP2009-1007-229-OPERATOR-COUNT"]["japanese_2009_october_claimed_total_pets"],229)
  self.assertFalse(s["JP2009-1007-229-OPERATOR-COUNT"]["claims_net_29_new_2009_species"])
  self.assertEqual(s["JP2009-1013-TENTH-ANNIVERSARY-PET-BAG"]["later_named_evolved_saber_pets"],["ベガルガー","ゴッドサーベル","ベルロイガー","ギルシス"])
  self.assertEqual(s["JP2009-1013-TENTH-ANNIVERSARY-PET-BAG"]["paired_to_2008_4_saber_inputs_proven"],0)
 def test_2009_korean_period_named_quest_and_cross_game_guard(self):
  a=self.a;s={r['id']:r for r in a['sources']}
  self.assertEqual(s["KR2009-0728-PLATIUS-QUEST"]["original_korean_pet_name"],"플라티우스")
  self.assertTrue(s["KR2009-0728-PLATIUS-QUEST"]["announced_quest_NPC_presents_pet"])
  self.assertEqual(s["KR2009-0728-PLATIUS-QUEST"]["undersea_map_piece_count_not_pet_count"],6)
  self.assertFalse(s["KR2009-0728-PLATIUS-QUEST"]["global_first_species_2009_proven"])
  self.assertFalse(s["KR2009-0728-ZDNET-SUMMER-SAME-CJ"]["report_text_explicitly_names_platius"])
  self.assertTrue(s["CN2009-1016-STONEAGE2-DISTINCT"]["do_not_merge_sequel_pets_into_original"])
 def test_2009_future_announcements_not_executed_client_pets(self):
  a=self.a;s={r['id']:r for r in a['sources']}
  future=s["JP2009-1126-CLOSURE-FUTURE-PET-SCHEDULE"]
  self.assertEqual(future["planned_2009_anonymous_wild_pet_date"],"2009-12-01")
  self.assertEqual(future["planned_2009_anonymous_quest_reward_date"],"2009-12-22")
  self.assertEqual(future["planned_2009_anonymous_four_seasons_capturable_date"],"2009-12-29")
  self.assertEqual(future["planned_next_year_2010_capturable_dates"],["2010-01-12","2010-01-19"])
  self.assertTrue(future["all_plans_not_verified_completed"])
  self.assertTrue(all(a["evidence_gates"].values()))
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  for region in a['region_reviews'].values():
   self.assertIsNone(region["species_population"])
  self.assertEqual((a["raw_authenticated_2009_original_client_bytes_new"],a["original_native_2009_pet_ids_new"],a["actual_2009_original_server_grants_new"]),(0,0,0))
  self.assertIsNone(a["global_2009_official_species_population"])
 def test_historical_current_exact_git_blob_untouched(self):
  a=self.a
  raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertTrue(a["historical_CURRENT_untouched"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertTrue(a["no_paid_marketplace"])
if __name__ == '__main__':unittest.main()
