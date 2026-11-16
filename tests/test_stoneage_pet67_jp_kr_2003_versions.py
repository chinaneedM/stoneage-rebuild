"""PET67 source-boundary contract: JP 1.74a and KR operator reset in 2003."""
import unittest,json
from pathlib import Path
REC=Path(__file__).resolve().parents[1]/"research"/"recovered"
class TestPet67(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads((REC/"STONEAGE-PET67-2003-JPKR-OPERATOR-CLIENT-BOUNDARY-R1.json").read_text(encoding="utf8"))
  cls.q=json.loads((REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf8"))
 def src(self,name):
  return next(z for z in self.d["source_records"] if z["id"]==name)
 def test_JP_original_betabuild_period_source_not_acquired(self):
  d=self.d
  a=self.src("JP_20031212_BETA_DOWNLOAD")
  b=self.src("JP_20031217_ACTUAL_BETA_AND_BUILD")
  self.assertEqual(a["planned_beta_start"],"2003-12-16")
  self.assertEqual(b["reported_beta_start"],"2003-12-16")
  self.assertEqual((b["printed_version"],b["version_date"]),("1.74a","2003-12-12"))
  self.assertTrue(b["then_free_distribution"])
  self.assertTrue(b["actual_file_name_unknown"])
  self.assertEqual(b["original_archive_bytes_obtained"],0)
  self.assertIsNone(b["native_pet_name_count_proven"])
  self.assertEqual(self.src("JP_20040520_2004_FORMAL_BOUNDARY")["formal_service_planned"],"2004-06-03")
  self.assertTrue(self.src("JP_20040520_2004_FORMAL_BOUNDARY")["do_not_count_2004_formal_service_as_2003_actual_release"])
 def test_KR_operator_reset_not_continuity_of_pets(self):
  x=self.src("KR_20030625_CONTRACT_PROSPECT")
  self.assertFalse(x["operator_change_contract_signed_confirmed_on_this_day"])
  x=self.src("KR_20030715_INIUM_STOP")
  self.assertEqual(x["in_situ_inium_shutdown_claim"],"2003-07-05")
  self.assertFalse(x["old_deployment_new_deployment_identity_proven"])
  x=self.src("KR_20030721_QUOTED_OFFICIAL_PLAN")
  self.assertEqual((x["printed_version"],x["planned_start"]),("1.74","2003-07-28"))
  self.assertTrue(x["source_is_reposted_not_original_operator_page"])
  self.assertFalse(x["install_binary_obtained"])
  self.assertEqual(self.d["explicit_version_carriers"][0]["relation_to_INIUM_5_0_content"],"UNKNOWN")
 def test_closed_source_boundaries_still_open_year(self):
  d,q=self.d,self.q
  self.assertEqual(d["year"],2003)
  self.assertEqual(d["year_gate_after"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["current_frontier"]["year"],2003)
  self.assertGreaterEqual(int(q["current_frontier"]["latest_partial_root_review"].split("-")[0][3:]),67)
  self.assertRegex(q["current_frontier"]["next"],r"^PET[0-9]+:")
  y=next(z for z in q["yearly_work_queue"] if z["year"]==2003)
  self.assertEqual(y["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(y["documentary_event_count_NOT_species"],1)
  self.assertEqual(sum(z["id"]==d["id"] for z in q["root_source_census_receipts"]),1)
  self.assertEqual(sum(z["id"]==d["id"] for z in y["partial_source_review_receipts"]),1)
  self.assertEqual(d["actual_new_original_2003_pet_asset_bytes"],0)
  self.assertEqual(d["newly_verified_same_build_native_pet_ids"],0)
  self.assertIsNone(d["historical_2003_pet_population"])
  self.assertTrue(d["historical_CURRENT_untouched"])
  self.assertTrue(d["no_original_commercial_files_public"])
  self.assertEqual(d["startup"]["CURRENT_original_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
