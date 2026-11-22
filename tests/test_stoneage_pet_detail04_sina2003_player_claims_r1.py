"""PET-DETAIL04: 15 dated player claims cannot become original PC master fields."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def normal(v):
 o={"地":None,"水":None,"火":None,"风":None}
 for k,n in v.items():o["风" if k=="風" else k]=n
 return o
class PETDetail04(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=read("research/pets/PET-DETAIL-EVIDENCE04-SINA2003-15-PLAYER-CLAIMS-R1.json")
  for p,sha in cls.r["source_pins"].items():assert blob(p)==sha
  cls.reg=read("research/pets/PET-ID-REGISTRY-R1.json")
  cls.cn=read("research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
  cls.waei=read("research/pets/PET-DETAIL-EVIDENCE01-WAEI2001-WITNESSES-R1.json")
 def test_exact_source_pairs_and_unfilled_original_stats(self):
  self.assertEqual(len(self.r["records"]),15)
  self.assertEqual(len(self.cn["records"]),362)
  for x in self.r["records"]:
   a=[t for t in self.reg["catalog_entries"] if t["display_name_simplified"]==x["name_2003"]]
   c=[t for t in self.cn["records"] if t["label_as_compiled_GB18030"]==x["name_2003"]]
   self.assertEqual((len(a),len(c)),(1,1))
   self.assertEqual(x["tw10_same_simplified_name_only"]["pet_id"],a[0]["catalog_pet_id"])
   self.assertEqual(x["cn50_later_preserved_compiled_literal_only"]["album_slot"],c[0]["ordinal"])
   self.assertEqual(x["cn50_later_preserved_compiled_literal_only"]["source_row_sha256"],c[0]["source_exe_row_sha256"])
   self.assertFalse(x["tw10_same_simplified_name_only"]["same_historical_2003_species_proven"])
   self.assertFalse(x["officially_released_original_species_confirmed_by_this_page"])
   for k in ("verified_native_pet_id","verified_original_elements","verified_original_skill","verified_original_growth","verified_original_lv1_stats","verified_original_capture_reward"):self.assertIsNone(x[k])
   profile=read(a[0]["machine_dossier_path"])
   self.assertTrue(all(v is None for v in profile["combat_stats"]["elements"].values()))
   self.assertIsNone(profile["skills"]["innate_at_acquisition"])
   self.assertIsNone(profile["growth"]["growth_rate"])
   self.assertIsNone(profile["actual_official_pet_identity"]["source_pet_id"])
   self.assertIn("CN2003-SINA-PLAYER-CLAIMS-15-FACTCHECK.md",(ROOT/a[0]["visible_dossier_path"]).read_text(encoding="utf-8"))
 def test_2001_documentary_recompute(self):
  c={"MATCHING_PLAYER_TEXT_NUMBERS":0,"CONFLICTING_PLAYER_TEXT_NUMBERS":0,"NO_2001_EXACT_PLAYER_ELEMENTS":0}
  for x in self.r["records"]:
   w=next(y for y in self.waei["entries"] if y["pet_id"]==x["tw10_same_simplified_name_only"]["pet_id"])
   raw=[s["player_submitted_four_element_claim_unverified"] for s in w["exact_original_printed_name_web_witnesses"] if s["player_submitted_four_element_claim_unverified"]]
   self.assertEqual(raw,[s["reported_elements"] for s in x["waei_2001_player_witnesses"]])
   want="NO_2001_EXACT_PLAYER_ELEMENTS" if not raw else "MATCHING_PLAYER_TEXT_NUMBERS" if any(normal(r)==x["source_elements"] for r in raw) else "CONFLICTING_PLAYER_TEXT_NUMBERS"
   self.assertEqual(want,x["comparison_to_2001_player_elements"])
   c[want]+=1
  self.assertEqual((c["MATCHING_PLAYER_TEXT_NUMBERS"],c["CONFLICTING_PLAYER_TEXT_NUMBERS"],c["NO_2001_EXACT_PLAYER_ELEMENTS"]),(10,1,4))
  f=self.r["unresolved_conflict"]
  self.assertEqual(f["pet_id"],"PET-000124")
  self.assertEqual(f["waei_2001_player_elements"],{"地":None,"水":5,"火":5,"风":None})
  self.assertEqual(f["sina_2003_player_elements"],{"地":None,"水":None,"火":5,"风":5})
 def test_preserve_history_and_source_tiers(self):
  self.assertEqual(blob("docs/CURRENT-STATE.md"),self.r["limitations"]["history_CURRENT_blob"])
  self.assertEqual(self.reg["counts"]["assigned_catalog_pet_ids"],124)
  self.assertEqual(self.r["counts"]["permanent_PET_id_added"],0)
  self.assertFalse(self.r["source"]["primary_2003_original_html_retrieved"])
  self.assertIsNone(self.r["source"]["primary_raw_html_sha256"])
  self.assertIn("CN2003-SINA-PLAYER-CLAIMS-15-FACTCHECK.md",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
