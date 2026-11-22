"""PET-DETAIL23 original classic PC 124 private visual atlas public-source only acceptance.
No original proprietary pixel files or private browser are needed in CI.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT="research/pets/PET-DETAIL-EVIDENCE23-TW10-124-ORIGINAL-PRIVATE-VISUAL-ATLAS-R1.json"
SRC="research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
MOV="research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json"
REG="research/pets/PET-ID-REGISTRY-R1.json"
def data(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def git_blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class PrivateSourceAtlas23(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=data(OUT);cls.s=data(SRC);cls.m=data(MOV);cls.r=data(REG)
 def test_sha_pin_and_exact_historical_state(self):
  for path,sha in self.a["immutable_repository_evidence_git_blobs"].items():
   self.assertEqual(git_blob(path),sha,path)
  self.assertEqual(self.a["baseline_main_head"],"4c8e6b54ff372bc508b6d3d09c72b3bd96916e56")
  self.assertEqual(self.a["baseline_main_tree"],"ae6264a2458267a363901dfba37ee89f5992b77c")
 def test_124_original_client_names_and_portrait_gates(self):
  a=self.a
  self.assertEqual(len(a["profiles"]),124)
  self.assertEqual(a["current_work_replayed_original_181_compiled_album_entries"],181)
  self.assertEqual(a["current_work_replayed_placeholder_entries"],57)
  self.assertEqual(a["current_work_actual_original_alias_mapped_RD_faces_decoded"],120)
  self.assertEqual(a["current_work_missing_portraits"],4)
  groups={g["graphic"]:g for g in self.m["groups"]}
  for i,(v,s,reg) in enumerate(zip(a["profiles"],self.s["records"],self.r["catalog_entries"])):
   self.assertEqual(v["pet_id"],reg["catalog_pet_id"])
   self.assertEqual(v["pet_id"],"PET-"+str(i+1).zfill(6))
   self.assertEqual(v["source_observation_id"],reg["observations"][0])
   self.assertEqual(v["original_client_name"],s["name_as_written"])
   self.assertEqual(v["source_graphic_number"],s["graphic_number"])
   self.assertEqual(v["original_compiled_name_row_sha256"],s["source_row_sha256"])
   self.assertEqual(v["original_portrait_logical_alias"],s["portrait_logical_alias"])
   self.assertEqual(v["original_sprite_segment_sha256"],s["spr_original_segment_sha256"])
   g=groups[s["graphic_number"]]
   self.assertEqual(v["source_spr_group_index"],g["group_index"])
   self.assertEqual(v["original_source_frame_occurrences"],g["frame_positions"])
   self.assertEqual(v["original_source_distinct_motion_bitmaps"],g["distinct_bitmaps"])
   self.assertEqual(v["original_source_animation_sequences"],g["source_sequences"])
   self.assertEqual(v["original_source_animation_sequences"],56)
   if s["portrait_rd"]:
    self.assertEqual(v["original_album_RD"]["original_rd_sha256"],s["portrait_rd"]["sha256"])
    self.assertEqual(v["original_album_RD"]["original_rd_bitmap_number"],s["portrait_rd"]["bitmap_number"])
    self.assertEqual(v["original_album_RD"]["original_rd_bytes"],s["portrait_rd"]["bytes"])
   else:self.assertIsNone(v["original_album_RD"])
  self.assertEqual([v["pet_id"] for v in a["profiles"] if v["original_album_RD"] is None],
                   ["PET-000116","PET-000117","PET-000118","PET-000119"])
 def test_exact_original_motion_and_private_package_reference(self):
  a=self.a
  self.assertEqual(sum(x["original_source_animation_sequences"] for x in a["profiles"]),6944)
  self.assertEqual(sum(x["original_source_frame_occurrences"] for x in a["profiles"]),70236)
  self.assertEqual(a["current_work_original_spr_distinct_bitmaps_exported"],29891)
  self.assertEqual(a["private_delivery"]["private_pngs_total"],30011)
  self.assertEqual(a["private_delivery"]["private_original_spr_pngs"],29891)
  self.assertEqual(a["private_delivery"]["private_same_source_album_RD_pngs"],120)
  self.assertEqual(a["private_delivery"]["archive_bytes"],84213409)
  self.assertEqual(a["private_delivery"]["archive_sha256"],"b881be179f82f352d6018b391e4d1b8b1986d050fedf5ee36b964e0ee3761e12")
  self.assertEqual(a["private_delivery"]["browser_entrypoint"],"index.html")
  self.assertTrue(a["browser_acceptance"]["loaded_124_cards_in_dom"])
  self.assertTrue(a["browser_acceptance"]["original_image_pixels_from_browser_file_navigation_not_tested_due_to_environment_browser_admin_block"])
  self.assertFalse((ROOT/"StoneAge-PET23-TW10-124-original-private-atlas.zip").exists())
 def test_no_server_or_official_pet_promotion(self):
  z=self.a["source_boundaries"]
  self.assertEqual(z["original_proprietary_images_publicly_committed"],0)
  self.assertFalse(z["original_client_native_execution"])
  self.assertFalse(z["non_pet_modules_open"])
  self.assertEqual(z["official_live_pet_species_proven"],0)
  self.assertEqual(z["pet_profiles_historically_fully_verified"],0)
  self.assertIsNone(z["original_server_pet_base_stats"])
  self.assertIsNone(z["original_server_pet_skill_table"])
  self.assertIsNone(z["original_server_acquisition_map"])
  self.assertIsNone(z["all_pet_species_historical_total"])
  self.assertIsNone(z["overall_project_completion_percent"])
  self.assertEqual(z["stage_A"],"7_PARTIAL+2_OPEN")
  self.assertEqual(z["stage_B_wiki"],"GATED")
  self.assertEqual(z["r79"],"PAUSED_NON_BLOCKING")
  ix=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
  report=(ROOT/"docs/continuity/STONEAGE-PET-DETAIL23-TW10-124-ORIGINAL-PRIVATE-ATLAS-20261122.md").read_text(encoding="utf-8")
  self.assertIn("PET-DETAIL23",ix)
  self.assertIn("PET-DETAIL23",report)
  self.assertIn("PET-DETAIL23",(ROOT/"README.md").read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
