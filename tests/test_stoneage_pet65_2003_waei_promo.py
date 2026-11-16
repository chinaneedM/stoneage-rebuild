"""PET65 tests: original TW1 SPR versus 2003 operator gift advertising."""
import unittest,json
from pathlib import Path
REC=Path(__file__).resolve().parents[1]/"research"/"recovered"
def get(name):return json.loads((REC/name).read_text(encoding="utf8"))
class TestPet65(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=get("STONEAGE-PET65-CN2003-WAEI-PET-PROMO-R1.json")
  cls.q=get("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.tw=get("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
  cls.c46=get("STONEAGE-PET46-TW1-ALBUM-NAME-2D-CROSSWALK-R1.json")
 def test_six_names_are_advertised_not_native_id(self):
  a=self.d["june_six"]
  self.assertEqual(a["names"],["佩露夏","蒙奇","帖拉所伊朵","邦诺斯娜","卡伊霍恩","鲁拉奇斯"])
  self.assertEqual(a["promoted_probability"],"100%")
  self.assertFalse(a["actual_redemptions_verified"])
  self.assertTrue(a["physical_sales_not_pet_count"])
 def test_two_different_draws(self):
  self.assertEqual([(x["name"],x["cards"]) for x in self.d["july_first"]["prizes"]],[("青龙",5),("白虎",4),("蒙奇",6),("帖拉所伊朵",9)])
  self.assertEqual([(x["name"],x["promoted_award_slots"]) for x in self.d["august_second"]["prizes"]],[("青龙",400),("蒙奇",600)])
  self.assertTrue(all(x["actual_awards"] is None for x in self.d["august_second"]["prizes"]))
  self.assertFalse(self.d["july_first"]["white_tiger_explicitly_named_Peluxia"])
  self.assertFalse(self.d["july17_change"]["original_native_claim_executed_verified"])
 def test_old_TW1_exact_SPR_only(self):
  a=self.d["TW1_exact_original_asset_name_candidates"]
  self.assertEqual(a["authentic_archive_sha256"],self.tw["archive"]["sha256"])
  self.assertEqual(len(a["rows"]),2)
  for v in a["rows"]:
   x=next(z for z in self.tw["records"] if z["name_as_written"]==v["name"])
   self.assertEqual(v["graphic"],x["graphic_number"])
   self.assertEqual(v["original_name_row_sha256"],x["source_row_sha256"])
   self.assertEqual(v["spr_sha256"],x["spr_original_segment_sha256"])
   self.assertEqual(v["rd_sha256"],x["portrait_rd"]["sha256"])
   y=next(z for z in self.c46["candidate_records"] if z["client_original_album_name"]==v["name"])
   self.assertEqual(v["spr_sha256"],y["pet07_original_whole_SPR_sha256"])
  self.assertFalse(a["CN_2003_same_original_SPR_proven"])
 def test_year_and_current_preserved(self):
  a,q=self.d,self.q
  self.assertEqual(q["current_frontier"]["year"],2003)
  self.assertGreaterEqual(int(q["current_frontier"]["latest_partial_root_review"].split("-")[0][3:]),65)
  self.assertRegex(q["current_frontier"]["next"],r"^PET[0-9]+:")
  self.assertEqual(q["yearly_work_queue"][4]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["yearly_work_queue"][4]["documentary_event_count_NOT_species"],1)
  self.assertEqual(sum(x["id"]==a["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(a["new_2003_original_client_bytes"],0)
  self.assertEqual(a["new_2003_official_live_awards_proven"],0)
  self.assertIsNone(a["global_2003_historical_pet_population"])
  self.assertTrue(a["historical_CURRENT_untouched"])
  self.assertTrue(a["no_paid_marketplace"])
  self.assertFalse(a["no_original_commercial_media_published"] is False)
  self.assertEqual(a["startup"]["CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
