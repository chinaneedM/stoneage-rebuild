"""PET74: 2006 five-region partial-only official PET evidence gate (no roster inflation)."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
def rd(p): return json.loads(p.read_text(encoding="utf-8"))
class PET74Boundaries(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=rd(DATA/"STONEAGE-PET74-YEAR2006-CN-TW-JP-KR-PARTIAL-R1.json")
  cls.q=rd(DATA/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_stays_2006_partial(self):
  a,q=self.a,self.q
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2006,2006))
  self.assertEqual((q["current_frontier"]["year"],q["yearly_work_queue"][2006-1999]["year"]),(2006,2006))
  self.assertEqual(q["yearly_work_queue"][2006-1999]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertFalse(a["historically_complete"])
  self.assertTrue(q["current_frontier"]["next"].startswith("PET75:"))
  self.assertIsNone(a["confirmed_2006_global_official_species_count"])
 def test_five_regions_and_product_separation(self):
  a=self.a
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(len(a["source_records"]),7)
  self.assertTrue(all(not s["in_game_release_eligible"] for s in a["source_records"]))
  self.assertEqual(a["region_reviews"]["CN"]["operator_marketing_pet_count_not_species_census"],2298)
  self.assertEqual(a["region_reviews"]["KR"]["operator_claimed_pet_number_not_species_census"],146)
  self.assertEqual(a["region_reviews"]["JP"]["nov_21_unnamed_pet_announcement"],2)
  self.assertTrue(all(a["excluded_evidence"].values()))
  self.assertTrue(a["region_reviews"]["JP"]["stoneage2_does_not_merge_with_original"])
  self.assertTrue(all(v["historical_species_count"] is None for v in a["region_reviews"].values()))
 def test_no_original_invention_or_paid_sources(self):
  a=self.a
  self.assertEqual((a["new_original_2006_client_bytes"],a["new_same_build_native_pet_ids"],a["new_native_reward_delivery_logs"]),(0,0,0))
  self.assertEqual(a["accessible_client_search"]["source_status"],"NOT_DOWNLOADED_NOT_AUTHENTICATED")
  self.assertIsNone(a["accessible_client_search"]["original_installer_sha256"])
  self.assertTrue(a["no_paid_marketplace"])
  self.assertTrue(a["historical_current_blob_unchanged"])
  self.assertEqual(a["startup"]["current_state_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"] ),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
 def test_receipt_added_once_without_erasing_old_2006_event(self):
  q,a=self.q,self.a
  self.assertEqual(sum(r["id"]==a["id"] for r in q["root_source_census_receipts"]),1)
  self.assertEqual(len({r["id"] for r in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
  y=q["yearly_work_queue"][7]
  self.assertIn("JP-2006-TWO-MYSTERY",y["documented_release_event_ids_from_existing_PET25_PET26"])
  self.assertEqual(y["documentary_event_count_NOT_species"],1)
  self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
if __name__=="__main__": unittest.main()
