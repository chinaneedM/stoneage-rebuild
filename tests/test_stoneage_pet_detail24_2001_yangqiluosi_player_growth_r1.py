"""PET-DETAIL24: eight player-reported PC pet stats, original name byte join, no TW10 official backfill."""
import hashlib
import json
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R="research/pets/PET-DETAIL-EVIDENCE24-2001-YANGQILUOSI-SINGLE-PET-LV1-LV71-R1.json"
P="research/pets/profiles/TW10-G100288.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class Original2001PlayerPetGrowth(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=load(R);cls.p=load(P)
  cls.early=load("research/pets/PET-DETAIL-EVIDENCE07-CN2001-LEVEL1-20-NUMERIC-SOURCE-CLAIMS-R1.json")
  cls.tw=load("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
 def test_pins_and_unaltered_2709173_byte_historical_state(self):
  self.assertEqual(self.r["baseline_main_sha"],"52b54f95acf995d050d327d5a77d88d07b92704c")
  for path,digest in self.r["source_pins_current_git"].items():self.assertEqual(blob(path),digest,path)
  self.assertEqual(blob(R),self.p["historical_player_measurement_evidence"]["source_evidence_git_blob"])
 def test_actual_native_client_name_and_separate_web_player_identity(self):
  x=self.r["original_client_cross_reference"]
  row=next(x for x in self.tw["records"] if x["graphic_number"]==100288)
  self.assertEqual((x["catalog_pet_id"],x["verified_original_name"],row["name_as_written"]),("PET-000039","揚奇洛斯","揚奇洛斯"))
  self.assertEqual(x["compiled_row_offset"],row["source_file_offset"])
  self.assertEqual(x["compiled_row_sha256"],row["source_row_sha256"])
  self.assertEqual(bytes.fromhex(x["compiled_original_cp950_row_hex"])[4:12].decode("cp950"),"揚奇洛斯")
  self.assertEqual(hashlib.sha256(bytes.fromhex(x["compiled_original_cp950_row_hex"])).hexdigest(),x["compiled_row_sha256"])
  self.assertFalse(x["same_official_deployment_as_player_testimony_proven"])
  self.assertFalse(self.r["new_source"]["original_2001_HTML_bytes_authenticated"])
  self.assertEqual(self.r["new_source"]["byline_as_current_page"],"唐歌")
 def test_eight_rows_and_all_twenty_eight_decimal_averages_recomputed(self):
  rows=self.r["reported_one_pet_level_observations"]
  self.assertEqual([a["level"] for a in rows],[1,11,21,31,41,51,61,71])
  self.assertEqual(rows[0]["reported_panel_values"],{"hp":61,"attack":13,"defense":8,"agility":6})
  self.assertEqual(rows[-1]["reported_panel_values"],{"hp":791,"attack":172,"defense":108,"agility":92})
  count=0
  for row in rows[1:]:
   for key in ("hp","attack","defense","agility"):
    f=row["computed_cumulative_average_exact_rationals"][key]
    self.assertEqual(f["numerator"],row["reported_panel_values"][key]-rows[0]["reported_panel_values"][key])
    self.assertEqual(f["denominator"],row["level"]-1)
    num=Decimal(f["numerator"])/Decimal(f["denominator"])
    scale=Decimal("0.1") if key=="hp" else Decimal("0.01")
    self.assertEqual(str(num.quantize(scale,rounding=ROUND_HALF_UP)),row["article_printed_cumulative_average_per_level"][key])
    count+=1
  self.assertEqual(count,28)
  self.assertEqual(self.r["growth_calculation_contract"]["source_reported_averages_rechecked"],28)
  self.assertTrue(self.r["growth_calculation_contract"]["all_28_reported_averages_agree_with_computation"])
  self.assertFalse(self.r["growth_calculation_contract"]["observed_not_official_formula"] is False)
 def test_only_player_bounds_concordance_not_official_range(self):
  cross=self.r["independent_player_range_crosscheck"]
  prev=next(x for x in self.early["records"] if x["obs_id"]=="OBS-CN2001-MILK-LV1-0006")
  self.assertEqual(prev["pet_name_as_2001_player_page"],"蓝龙人")
  self.assertEqual(prev["numeric_slots_bounds_without_stat_labels"],cross["four_unlabeled_source_numeric_slots"])
  self.assertEqual(cross["tangge_one_sample_first_level_slot_values"],[61,13,8,6])
  self.assertEqual([v["min"]<=a<=v["max"] for v,a in zip(cross["four_unlabeled_source_numeric_slots"],cross["tangge_one_sample_first_level_slot_values"])],[True]*4)
  self.assertFalse(cross["source_page_four_slots_have_verified_official_column_labels"])
  self.assertFalse(cross["source_games_same_server_proven"])
 def test_legacy_dossier_core_stats_and_stages_still_unproven(self):
  p=self.p;g=self.r["evidence_guards"]
  self.assertEqual(p["profile_id"],"PET-000039")
  self.assertEqual(p["profile_stage"],"PARTIAL_EVIDENCE_PROFILE")
  self.assertEqual(p["combat_stats"]["status"],"OPEN_NOT_PROVEN")
  self.assertTrue(all(x is None for x in p["combat_stats"]["level_1"]["values"].values()))
  self.assertTrue(all(x is None for x in p["combat_stats"]["elements"].values()))
  for scope in ("minimum","maximum"):
   self.assertTrue(all(x is None for x in p["combat_stats"]["initial_stat_ranges"][scope].values()))
  for key in ("growth","skills","acquisition"):
   self.assertEqual(p[key]["status"],"OPEN_NOT_PROVEN")
  self.assertFalse(p["historical_player_measurement_evidence"]["verified_official_pet_birth_or_growth_formula"])
  self.assertEqual((g["tw10_source_named_profiles_partial"],g["tw10_fully_historically_verified_profiles"],g["new_official_live_species_authenticated"]),(124,0,0))
  self.assertIsNone(g["official_level1_min_max_or_birth_sampling"])
  self.assertIsNone(g["official_growth_algorithm"])
  self.assertIsNone(g["official_skill_loadout"])
  self.assertIsNone(g["overall_completion_percent"])
  self.assertEqual(g["only_active_module"],"PET")
  self.assertIn("PET-DETAIL24",(ROOT/"docs/pets/TW10-G100288.md").read_text(encoding="utf-8"))
  self.assertIn("PET-DETAIL24",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
  self.assertIn("PET-DETAIL24",(ROOT/"README.md").read_text(encoding="utf-8"))

if __name__=="__main__":unittest.main()
