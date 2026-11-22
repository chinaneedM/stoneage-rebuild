"""PET-DETAIL28 source-bound PC-grey-dragon stats and contradictory aliases."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def gh(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
class GreyDragon(unittest.TestCase):
 def test_100_levels_exact_mean(self):
  e=load("research/pets/PET-DETAIL-EVIDENCE28-2001-GREY-DRAGON-LV1-LV101-NAME-CONFLICT-R1.json");s=e["player_sample"];a,b=s["panels"]
  self.assertEqual(s["number_of_distinct_pets"],1)
  self.assertEqual((a["level"],b["level"]),(1,101))
  for x in s["average_deltas"]:
   self.assertEqual(x["numerator"],b[x["stat"]]-a[x["stat"]])
   self.assertEqual(x["denominator"],100)
   self.assertEqual(x["author_printed"],str(x["numerator"]/100))
  self.assertEqual([x["author_printed"] for x in s["average_deltas"]],["9.75","2.37","1.36","1.27"])
  self.assertFalse(s["theory_is_proven_original_pc_algorithm"])
  self.assertFalse(s["panels_are_authenticated_native_gameplay"])
 def test_conflict_cannot_be_silent_identity(self):
  e=load("research/pets/PET-DETAIL-EVIDENCE28-2001-GREY-DRAGON-LV1-LV101-NAME-CONFLICT-R1.json");c=e["alias_disagreement"]
  self.assertEqual(c["claims"],[{"source":"lili2002","grey":"邦浦洛斯","yellow":"布鲁顿"},{"source":"press2011","grey":"布鲁顿","yellow":"邦浦洛斯"}])
  self.assertFalse(c["same_original_game_build_proven"])
  self.assertFalse(c["official_corrected_name_proven"])
  self.assertFalse(e["separate_original_client"]["player_sample_can_be_assigned_to_this_profile"])
  self.assertFalse(e["sources"][0]["original_html_sha_verified"])
 def test_retail_original_local_name_and_null_official_stats(self):
  e=load("research/pets/PET-DETAIL-EVIDENCE28-2001-GREY-DRAGON-LV1-LV101-NAME-CONFLICT-R1.json");x=e["separate_original_client"];t=load(x["source_path"])
  self.assertEqual(gh(x["source_path"]),x["source_blob"])
  z=next(a for a in t["records"] if a["graphic_number"]==100289)
  self.assertEqual((z["name_as_written"],z["source_row_sha256"]),(x["local_name"],x["original_compiled_row_sha"]))
  p=load("research/pets/profiles/TW10-G100289.json")
  self.assertTrue(all(v is None for v in p["combat_stats"]["level_1"]["values"].values()))
  self.assertTrue(all(v is None for v in p["combat_stats"]["elements"].values()))
  for k in ("minimum","maximum"):self.assertTrue(all(v is None for v in p["combat_stats"]["initial_stat_ranges"][k].values()))
  for k in ("growth","skills","acquisition"):self.assertEqual(p[k]["status"],"OPEN_NOT_PROVEN")
 def test_gates(self):
  e=load("research/pets/PET-DETAIL-EVIDENCE28-2001-GREY-DRAGON-LV1-LV101-NAME-CONFLICT-R1.json");z=e["progress"]
  self.assertEqual(e["protected_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual((z["tw10_named_candidates"],z["tw10_partial_profiles"],z["tw10_complete_profiles"]),(124,124,0))
  self.assertEqual(z["new_official_live_pet_species"],0)
  self.assertIsNone(z["overall_percent"])
  self.assertEqual(z["pet_module_only"],True)
  self.assertIn("PET-DETAIL28",(ROOT/"README.md").read_text(encoding="utf-8"))
  self.assertIn("PET-DETAIL28",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
