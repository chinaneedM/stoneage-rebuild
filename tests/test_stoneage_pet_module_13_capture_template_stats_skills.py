"""PET13: 11 source original compiled capture candidates to original mixed25 numeric template and skill rows."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from tools.stoneage_pet13_capture_template_stats_skills import derive, check, blobsha

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json"

class PET13ExactOriginalSourceRelationships(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.saved=json.loads(REPORT.read_text(encoding="utf-8"))
  cls.rebuilt=derive()
 def test_immutable_source_replay(self):
  self.assertEqual(self.saved,self.rebuilt)
  self.assertEqual(self.saved["source_git_blobs"]["WORLD37_R2B3"],"0e80e5a62dd59542c3e1ede18460d92e17927a30")
  self.assertEqual(self.saved["source_git_blobs"]["PET10"],"25a37aeb134fb180e322e7dc335029b7374452d8")
 def test_conserve_all_original_capture_candidate_keys(self):
  s=self.saved["summary"]; self.assertEqual(s["compiled_candidate_rows"],11)
  self.assertEqual((s["PETFLG_1_count"],s["PETFLG_0_count"]),(10,1))
  self.assertEqual((s["distinct_template_IDs"],s["distinct_original_graphic_numbers"]),(11,11))
  self.assertEqual(s["all_literal_level_up_words"],"4.50")
  self.assertEqual((s["compiled_capture_required_item_references"],s["distinct_capture_required_item_IDs"]),(13,12))
  self.assertEqual((s["distinct_positive_source_skill_IDs"],s["positive_original_skill_slot_occurrences"]),(5,25))
  self.assertIs(s["all_skill_references_defined_in_same_source_master"],True)
  expected={524:100329,961:101280,953:101281,962:101279,777:100872,796:100891,812:100907,1105:101564,8:100355,145:101737,146:101736}
  self.assertEqual({x["compiled_capture_key53"]:x["original_graphic_numeric_ID"] for x in self.saved["templates"]},expected)
  self.assertEqual([x["original_template_numeric_ID"] for x in self.saved["templates"]],list(expected))
  for row in self.saved["templates"]:
   self.assertEqual(row["original_template_numeric_ID"],row["compiled_capture_key53"])
   self.assertEqual(len(row["original_seven_skill_slots_nullable"]),7)
   self.assertEqual(len(row["original_physical_line_including_newline_sha256"]),64)
   self.assertEqual(len(row["original_56_column_normalized_sha256"]),64)
   self.assertIs(row["original_compiled_runtime_key_to_template_loader_verified"],False)
   self.assertIs(row["original_actual_capturable_pets_species_verified"],False)
  self.assertEqual([x["compiled_capture_key53"] for x in self.saved["templates"] if x["original_PETFLG"]==0],[8])
 def test_native_skill_definition_scope(self):
  self.assertEqual({x["skill_id"]:x["source_short_name"] for x in self.saved["same_source_original_petskill_short_labels_private_verified"]},
    {1:"攻擊",2:"防禦",60:"毒攻擊",90:"混亂攻擊",110:"催眠攻擊"})
  wanted={1,2,60,90,110}
  for row in self.saved["templates"]:
   nums=[x for x in row["original_seven_skill_slots_nullable"] if x is not None and x>0]
   linked=[x["source_pet_skill_id"] for x in row["same_archive_original_skill_links"]]
   self.assertEqual(nums,linked)
   self.assertTrue(set(linked)<=wanted)
   self.assertEqual(sum(map(int,row["original_earth_water_fire_wind_literals"].values())),100)
   self.assertEqual(row["original_lvup_literal"],"4.50")
 def test_no_version_identity_or_actual_capture_promoted(self):
  r=self.saved
  self.assertIn("COMMUNITY",r["original_scope"])
  self.assertEqual(r["original_same_archive_member_sha256"]["enemybase.txt"],"1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7")
  self.assertEqual(r["original_same_archive_member_sha256"]["petskill.txt"],"f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4")
  for key,value in r["bounds"].items():
   if key.startswith("stage_") or key=="r79" or key=="overall_percent":continue
   self.assertIs(value,False,key)
  self.assertEqual((r["bounds"]["stage_a"],r["bounds"]["stage_b_wiki"],r["bounds"]["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(r["bounds"]["overall_percent"])
 def test_tampering_fails_public_source_condition(self):
  with self.assertRaises(ValueError): check(False,"negative test original source tampering")
  fake=dict(self.saved["summary"],PETFLG_0_count=0)
  self.assertNotEqual(fake,self.rebuilt["summary"])

if __name__=="__main__": unittest.main()
