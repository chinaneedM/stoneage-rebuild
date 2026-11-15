import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/recovered/STONEAGE-PET37-TW2000-MINSHENG-PET-PRESS-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class PET37Tw2000News(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=json.loads(P.read_text(encoding="utf-8"));cls.q=json.loads(Q.read_text(encoding="utf-8"))
 def test_newspaper_date_mechanic_not_runtime(self):
  x=self.p
  self.assertEqual(x["source"]["original_date"],"2000-04-11")
  self.assertEqual(x["source"]["original_page"],"37版")
  self.assertFalse(x["source"]["original_page_scan_verified"])
  self.assertIsNone(x["source"]["original_source_bytes_sha256"])
  self.assertEqual(x["claims"][0]["event_date"],"2000-04-10")
  self.assertFalse(x["claims"][0]["exact_first_live_day_verified"])
  self.assertFalse(x["claims"][1]["native_mechanic_verified"])
  self.assertIsNone(x["claims"][1]["exact_loyalty_delta"])
  self.assertIsNone(x["claims"][1]["pet_id"])
 def test_book_version_conflict_not_species_count(self):
  z=self.p["cross_source_status"]
  self.assertEqual(z["catalogue_publication_date"],"2000-08-01")
  self.assertEqual(z["secondary_tw_two_zero_date"],"2001-08-01")
  self.assertTrue(z["catalogue_date_vs_version_conflict_unresolved"])
  self.assertFalse(z["original_colophon_verified"])
  self.assertFalse(z["original_disc_verified"])
  self.assertFalse(z["catalogue_pet_quantity_promoted_to_historical_count"])
  self.assertFalse(z["tw_2000_two_zero_live_verified"])
  self.assertEqual(self.p["new_qualified_original_2000_official_named_pet_release_records"],[])
  self.assertIsNone(self.p["historical_pet_species_count"])
 def test_persistent_year_receipt_and_original_current(self):
  q=self.q;x=self.p
  h=[r for r in q["root_source_census_receipts"] if r["id"]=="PET37-TW2000-MINSHENG-LOYALTY-20261115"]
  self.assertEqual(len(h),1)
  self.assertEqual(h[0]["year_frontier_before"],2000)
  self.assertEqual(h[0]["year_frontier_after"],2000)
  self.assertGreaterEqual(q["current_frontier"]["year"],2000)
  self.assertEqual(x["preserved_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertFalse(x["commercial_assets_publicly_committed"])
if __name__=="__main__":unittest.main()
