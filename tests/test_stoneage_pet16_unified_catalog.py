"""PET16 source-dimension invariants. All inputs are historical public derived records."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered"
def read(n):return json.loads((R/n).read_text(encoding="utf-8"))
class Pet16Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read("STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
  cls.p08=read("STONEAGE-PET-MODULE-08-VISUAL-STATS-SKILLS-SOURCE-CATALOG-R1.json")
  cls.p10=read("STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json")
  cls.p15=read("STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json")
  cls.jp=read("STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json")
  cls.cn=read("STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json")
 def test_source_namespace_counts(self):
  expect={"later2016_templates":1024,"later2016_graphics":598,
          "mixed25_main":495,"mixed25_alternative":316,
          "tw10_visual":131,"jp_official_web":124,"cn_official_web":104}
  self.assertEqual({k:len(v) for k,v in self.c["datasets"].items()},expect)
  self.assertEqual(self.c["metrics"]["source_namespace_row_counts_NOT_species"],expect)
  self.assertTrue(self.c["constraints"]["never_add_namespace_rows_as_species_count"])
 def test_late_source_every_row(self):
  for old,new in zip(self.p08["template_rows"],self.c["datasets"]["later2016_templates"]):
   self.assertEqual((new["original_row"],new["template_id"],new["graphic_number"],new["same_source_instance_references"]),(old[0],old[1],old[2],old[5]))
   self.assertEqual(list(new["stats_original_literals"].values()),old[3])
   self.assertEqual(new["skill_source_slots"],old[4])
   self.assertFalse(new["official_species_identity"])
 def test_mixed_original_static_and_hash(self):
  for file,group in [("enemybase.txt","mixed25_main"),("enemybase2.txt","mixed25_alternative")]:
   old=[x for x in self.p10["source_rows"][file] if x[3]==1]
   for x,y in zip(old,self.c["datasets"][group]):
    self.assertEqual((y["original_row"],y["template_id"],y["graphic_number"],y["original_fields_sha256"]),(x[0],x[1],x[2],x[16]))
    self.assertEqual(list(y["stats_original_literals"].values()),x[4:15])
    self.assertEqual(y["original_skill_slot_ids"],x[15])
    self.assertFalse(y["native_runtime_verified"])
 def test_tw10_complete_sequences(self):
  for x,y in zip(self.p15["groups"],self.c["datasets"]["tw10_visual"]):
   self.assertEqual((x["graphic"],x["group_index"],x["segment_sha256"],x["source_sequences"],x["frame_positions"],x["distinct_bitmaps"]),(y["graphic_number"],y["spr_group_index"],y["spr_original_segment_sha256"],y["source_sequences"],y["source_frame_positions"],y["source_bitmap_references"]))
   self.assertFalse(y["official_species_identity"])
  m=self.c["metrics"]
  self.assertEqual((m["tw10_spr_sequences"],m["tw10_spr_frame_positions"],m["tw10_strict_pixel_source_bitmaps"],m["tw10_terminal_zero_bounded_not_strict"]),(7672,73500,32150,5))
 def test_web_names_keep_unknown_ids(self):
  for group,old in [("jp_official_web",self.jp["records"]),("cn_official_web",self.cn["records"])]:
   cur=self.c["datasets"][group]
   self.assertEqual([(x["id"],x["name_as_written"]) for x in cur],[(x["record_id"],x["name_as_written"]) for x in old])
   self.assertTrue(all(x["actual_client_species_id"] is None for x in cur))
  self.assertEqual(self.c["metrics"]["cn_web_unknown_name_positions"],6)
 def test_hashed_qualified_names_and_gaps(self):
  ps=read("STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json")["templates"]
  named=[x for x in self.c["datasets"]["mixed25_main"] if x["name_as_written"]]
  self.assertEqual(len(named),10)
  for y in named:
   self.assertTrue(any(x["original_template_numeric_ID"]==y["template_id"] and x["original_56_column_normalized_sha256"]==y["original_fields_sha256"] and x["mixed25_configured_original_name"]==y["name_as_written"] and x["original_PETFLG"]==1 for x in ps))
  self.assertEqual(len(self.c["coverage_gaps"]),7)
  self.assertTrue(all(x["reopen_trigger"] for x in self.c["coverage_gaps"]))
  self.assertEqual(self.c["active_module"],"PET")
 def test_search_separate(self):
  import sys
  sys.path.insert(0,str(ROOT/"tools"))
  from stoneage_pet16_lookup import lookup
  self.assertTrue(lookup(self.c,"ウーリ","jp_official_web"))
  self.assertTrue(lookup(self.c,"朱利洛斯","cn_official_web"))
  self.assertTrue(any(x["dataset"]=="tw10_visual" for x in lookup(self.c,"100400",limit=999)))
  self.assertTrue(lookup(self.c,"卡特利奴","mixed25_main"))
if __name__=="__main__":
 unittest.main()
