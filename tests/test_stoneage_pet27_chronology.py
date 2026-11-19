"""PET27 strict oldest-to-newest chronology without guessing original species counts."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet27_chronology import load,choose,validate
class TestChronology(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=load()
 def test_source_exact_pc_9(self):
  self.assertTrue(validate(self.d))
  self.assertEqual(len(self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]),9)
  self.assertEqual(len(set(x["source_id"] for x in self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"])),9)
 def test_years_advance_only_after_source_bounded_review(self):
  d=self.d;years=d["yearly_work_queue"]
  self.assertEqual([y["year"] for y in years],list(range(1999,2027)))
  self.assertEqual(years[0]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(years[0]["historically_complete"])
  self.assertIsNone(years[0]["historical_species_count"])
  self.assertGreater(len(years[0]["residual_reopen_triggers"]),0)
  self.assertEqual(d["current_frontier"]["year"],next(x["year"] for x in years if x["research_gate"]=="NOT_YEAR_AUDITED"))
  self.assertGreaterEqual(d["current_frontier"]["year"],2000)
  self.assertEqual(len(choose(d,year=1999)),0)
  self.assertEqual(len(choose(d,year=2000)),0)
 def test_9_pc_events_order(self):
  d=self.d; e=d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
  self.assertEqual([x["chronology_date"] for x in e],sorted(x["chronology_date"] for x in e))
  self.assertEqual({y["year"]:y["documentary_event_count_NOT_species"] for y in d["yearly_work_queue"] if y["documentary_event_count_NOT_species"]},{2002:4,2003:1,2006:1,2008:1,2009:2})
 def test_attestation_does_not_become_first_release(self):
  x={row["source_id"]:row for row in self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]}
  self.assertEqual(x["CN-PC-3-YEAR"]["date_kind"],"SOURCE_ATTESTATION_DATE_NOT_FIRST_RELEASE")
  self.assertEqual(x["JP-2009-KOKUEN"]["year"],2009)
  self.assertTrue(all("CLASSIC_PC" in v["product_line"] for v in x.values()))
  self.assertTrue(all(not row["source_record_is_global_unique_species"] for row in x.values()))
 def test_country_version_claims_not_promoted_to_pet_release(self):
  milestones=self.d["version_milestone_date_claims_not_pet_release_proofs"]
  self.assertTrue(any(x["id"]=="TW-2000-1.0" for x in milestones))
  self.assertTrue(any(x["id"]=="CN-2001-1.0" for x in milestones))
  self.assertEqual(len(choose(self.d,region="TW")),0)
  self.assertEqual(len(choose(self.d,region="KR")),0)
  self.assertEqual(len(choose(self.d,region="JP")),4)
  self.assertTrue(all("verification" in x and "sources" in x for x in milestones))
 def test_private_art_and_original_current_protected(self):
  d=self.d
  self.assertFalse(d["private_server_only_species_included"])
  self.assertFalse(d["original_art_published"])
  self.assertEqual(d["baselines"]["current_state_historical_blob_unchanged"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
