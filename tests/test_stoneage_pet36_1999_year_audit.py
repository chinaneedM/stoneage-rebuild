import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-PET36-1999-SOURCE-BOUNDED-YEAR-AUDIT-R1.json"
QUEUE=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"

class Pet36YearBoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))
    def test_review_is_not_full_history_or_species_zero(self):
        r=self.r;q=self.q
        self.assertEqual(r["year"],1999)
        self.assertEqual(r["review_status"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(r["historically_complete"])
        self.assertIsNone(r["official_pet_population"])
        self.assertEqual(r["new_named_official_live_pet_proofs"],0)
        self.assertEqual(q["yearly_work_queue"][0]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(q["yearly_work_queue"][0]["historically_complete"])
        self.assertIsNone(q["yearly_work_queue"][0]["historical_species_count"])
    def test_originals_and_regional_unknowns_preserved(self):
        r=self.r
        sources={x["id"]:x for x in r["previous_verified_sources"]}
        self.assertEqual(sources["PET31"]["dated_blocks"],15)
        self.assertEqual(sources["PET31"]["clauses"],65)
        self.assertEqual(sources["PET34"]["original_bytes"],31915180)
        self.assertEqual(set(r["region_source_reviews"]),{"JP","TW","KR","CN","OTHER"})
        self.assertTrue(all(x["pet_population"] is None for x in r["region_source_reviews"].values()))
        self.assertTrue(all(x["reopen"] for x in r["access_blockers"]))
        self.assertEqual(r["current_original_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertFalse(r["commercial_assets_published"])
    def test_year_transition_has_historic_receipt_and_future_reopen(self):
        q=self.q
        rows=[x for x in q["root_source_census_receipts"] if x["id"]=="PET36-1999-SOURCE-BOUNDED-YEAR-AUDIT-20261115"]
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["year_frontier_before"],1999)
        self.assertEqual(rows[0]["year_frontier_after"],2000)
        self.assertTrue(rows[0]["reopen_on_new_original_1999_source"])
        self.assertGreaterEqual(q["current_frontier"]["year"],2000)
        self.assertGreater(len(q["yearly_work_queue"][0]["residual_reopen_triggers"]),0)

if __name__=="__main__": unittest.main()
