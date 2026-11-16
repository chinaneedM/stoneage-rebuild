"""PET63 official-only chronology and regional source boundaries."""
import json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"research"/"recovered"
def f(n):return json.loads((P/n).read_text(encoding="utf-8"))
class TestPET63(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=f("STONEAGE-PET63-TW2002-WAEI-DUANWU-SOURCE-R1.json")
  cls.q=f("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.r=f("STONEAGE-CN2003-PET-GROWTH-PLAYER-CLAIMS-SOURCE-R1.json")
 def test_source_and_marketing_not_live(self):
  d=self.d;p=d["taiwan_promo"]
  self.assertEqual(d["sources"][0]["date"],"2002-06-27")
  self.assertEqual(d["sources"][0]["direct_http"],"403")
  self.assertIsNone(d["sources"][0]["original_html_sha256"])
  self.assertEqual((p["planned_first_sale"],p["puman_name"],p["advertised_max_pets"]),("2002-06-29","撲滿烏力",300))
  self.assertFalse(p["actual_server_rewards_verified"])
  self.assertTrue(d["exclusion_guards"]["models_not_live_species"])
 def test_four_later_names_not_2002_pet_ids(self):
  d=self.d;a={x["name"]:x for x in d["duanwu_text_candidates"]}
  self.assertEqual(set(a),{"卡恩法尔","卡恩修比","卡恩格登","卡恩米兹"})
  self.assertEqual({x["sina_list_no"] for x in a.values()},{233,234,235,236})
  self.assertEqual((a["卡恩格登"]["element"],a["卡恩格登"]["r92_element"]),("地3水7","地7水3"))
  self.assertTrue(a["卡恩格登"]["conflict_unresolved"])
  self.assertEqual(a["卡恩米兹"]["r92_original_corrupted"],"卡恩米��")
  self.assertIn("卡恩米",self.r["missing_evidence"][2])
  self.assertTrue(d["exclusion_guards"]["sina_numbers_are_not_native_ids"])
 def test_state_and_receipt(self):
  d=self.d;q=self.q
  self.assertGreaterEqual(q["current_frontier"]["year"],2002)
  self.assertEqual(q["yearly_work_queue"][3]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertIn(d["id"],[x["id"] for x in q["root_source_census_receipts"]])
  self.assertRegex(q["current_frontier"]["next"], r"^PET[0-9]+:")
  self.assertEqual(sum(x["id"]==d["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(q["yearly_work_queue"][3]["documentary_event_count_NOT_species"],4)
  self.assertEqual((d["new_2002_original_client_bytes"],d["new_2002_native_pet_ids"],d["new_2002_official_live_awards"]),(0,0,0))
  self.assertIsNone(d["worldwide_2002_pet_population"])
  self.assertFalse(d["original_state_changed"])
  self.assertFalse(d["paid_seller_search"])
  self.assertEqual(d["original_state_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
