"""PET27 strict oldest-to-newest chronology without guessing original species counts."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet27_chronology import load,choose,validate
class TestChronology(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=load()
 def test_source_exact_28(self):
  self.assertTrue(validate(self.d))
  self.assertEqual(len(self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]),28)
  self.assertEqual(len(set(x["source_id"] for x in self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"])),28)
 def test_years_start_from_provisional_oldest_and_are_never_preclosed(self):
  d=self.d;years=d["yearly_work_queue"]
  self.assertEqual([y["year"] for y in years],list(range(1999,2027)))
  self.assertEqual(d["current_frontier"]["year"],1999)
  self.assertTrue(all(y["research_gate"]=="NOT_YEAR_AUDITED" for y in years))
  self.assertEqual(len(choose(d,year=1999)),0)
  self.assertEqual(len(choose(d,year=2000)),0)
 def test_28_events_order_and_2002_2026(self):
  d=self.d; e=d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
  self.assertEqual([x["chronology_date"] for x in e],sorted(x["chronology_date"] for x in e))
  self.assertEqual({y["year"]:y["documentary_event_count_NOT_species"] for y in d["yearly_work_queue"] if y["documentary_event_count_NOT_species"]},{2002:4,2003:1,2006:1,2008:1,2009:2,2020:2,2021:1,2026:16})
 def test_attestation_does_not_become_first_release(self):
  x={row["source_id"]:row for row in self.d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]}
  self.assertEqual(x["CN-PC-3-YEAR"]["date_kind"],"SOURCE_ATTESTATION_DATE_NOT_FIRST_RELEASE")
  self.assertEqual(x["KR-WORLD-2021-SHUI"]["date_kind"],"SOURCE_ATTESTATION_DATE_NOT_FIRST_RELEASE")
  self.assertEqual(x["CN-NEW-2026-HORSE-01"]["date_kind"],"OFFICIAL_REPORTED_RELEASE_DATE")
  self.assertTrue(all(not row["source_record_is_global_unique_species"] for row in x.values()))
 def test_country_version_claims_not_promoted_to_pet_release(self):
  milestones=self.d["version_milestone_date_claims_not_pet_release_proofs"]
  self.assertTrue(any(x["id"]=="TW-2000-1.0" for x in milestones))
  self.assertTrue(any(x["id"]=="CN-2001-1.0" for x in milestones))
  self.assertEqual(len(choose(self.d,region="TW")),0)
  self.assertEqual(len(choose(self.d,region="KR")),4)
  self.assertEqual(len(choose(self.d,region="JP")),4)
  self.assertTrue(all("verification" in x and "sources" in x for x in milestones))
 def test_private_art_and_original_current_protected(self):
  d=self.d
  self.assertFalse(d["private_server_only_species_included"])
  self.assertFalse(d["original_art_published"])
  self.assertEqual(d["baselines"]["current_state_historical_blob_unchanged"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
