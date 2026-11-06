"""PET12 public original-source replay: six TW85 groups vs original RD and CN5 evidence."""
import json
import unittest
from pathlib import Path
from tools.stoneage_pet12_tw85_capture_spr_rd_bridge import derive, KEYS, need

ROOT=Path(__file__).resolve().parents[1]
ARCHIVED=ROOT/"research/recovered/STONEAGE-PET-MODULE-12-TW85-SIX-CAPTURE-SPR-RD-BRIDGE-R1.json"

class PET12ExactSourceReconstruction(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.public=json.loads(ARCHIVED.read_text(encoding="utf-8"))
  cls.rebuilt=derive()
 def test_full_immutable_replay(self):
  self.assertEqual(self.rebuilt,self.public)
 def test_all_six_original_animation_rd_source_membership(self):
  r=self.public
  self.assertEqual(tuple(r["capture_candidate_graphics_six"]),KEYS)
  self.assertEqual(r["summary"]["group_occurrences"],6)
  self.assertEqual(r["summary"]["original_animation_sequences"],336)
  self.assertEqual(r["summary"]["original_frame_occurrences"],2048)
  self.assertEqual(r["summary"]["original_sentinel_frame_occurrences"],0)
  self.assertEqual(r["summary"]["original_nonsentinel_frame_occurrences"],2048)
  self.assertEqual(r["summary"]["distinct_referenced_original_same_carrier_bitmap_ids"],1568)
  self.assertEqual(r["summary"]["same_carrier_source_qualified_original_RD_bitmap_ids"],1568)
  self.assertEqual(r["summary"]["distinct_original_direction0_first_frame_bitmap_ids"],36)
  self.assertEqual(r["summary"]["actually_new_original_pixels_decoded_in_this_work_unit"],0)
  expect={
   101279:(328,264,True),
   101280:(240,232,True),
   101281:(256,248,True),
   101564:(312,264,False),
   101736:(456,280,False),
   101737:(456,280,False)}
  self.assertEqual({g["graphic_no"]:(g["tw85_original_frame_positions"],g["tw85_distinct_same_carrier_bitmap_numbers"],g["cn50_same_id_and_entire_spr_segment_sha_verified_in_R28"])for g in r["groups"]},expect)
  self.assertEqual(sum(g["tw85_distinct_same_carrier_bitmap_numbers"]for g in r["groups"]),1568)
  self.assertTrue(all(g["tw85_original_animation_sequences"]==56 and g["source_petflag"]==1 for g in r["groups"]))
 def test_actions_and_original_pixel_limits(self):
  r=self.public
  for g in r["groups"]:
   self.assertEqual(sum(g["action_sequence_counts"].values()),56)
   self.assertEqual(sum(g["direction_sequence_counts"].values()),56)
   self.assertEqual(g["tw85_unique_original_rd_bitmap_refs"],g["tw85_original_frame_positions"])
   self.assertEqual(len(g["direction0_first_qualified_original_frames"]),g["sample_direction0_first_frame_count"])
   for a in g["direction0_first_qualified_original_frames"]:
    src=a["same_carrier_original_RD"]
    self.assertEqual(len(src["RD_original_sha256"]),64)
    self.assertGreater(src["RD_original_bytes"],16)
    self.assertGreater(src["width"],0);self.assertGreater(src["height"],0)
  limits=r["negative_boundaries"]
  for k in ("original_tw85_REAL_bytes_reacquired_this_turn","original_tw85_RD_pixels_recovered_now","official_TW85_clean_build_certified","mixed25_and_TW85_same_deployed_build_proven","capture_entity_species_join_native_runtime_proven","original_fps_or_duration_units_authenticated","original_animation_action_meanings_authenticated","CN50_only_matching_ID_implies_same_payload","TW10_source_species_identity_from_other_build","original_client_or_server_executed","proprietary_source_payloads_published"):
   self.assertIs(limits[k],False,k)
  self.assertIsNone(limits["overall_percent"])
  self.assertEqual((limits["stage_a"],limits["stage_b_wiki"],limits["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
 def test_source_scopes_no_cross_version_promotion(self):
  r=self.public
  self.assertIn("UNVERIFIED",r["source_grade"])
  self.assertEqual(r["summary"]["groups_with_CN50_exact_full_SPR_bytes"],3)
  self.assertEqual(r["summary"]["groups_not_in_CN50_source"],3)
  self.assertEqual(r["summary"]["groups_with_TW1_source_index"],0)
  self.assertEqual(r["summary"]["groups_with_mixed25_source_index"],0)
  self.assertTrue(all(g["tw10_original_spr_index"] is None and g["mixed25_original_spr_index"] is None for g in r["groups"]))
 def test_tamper_guard_does_not_silently_accept_mismatch(self):
  with self.assertRaises(ValueError):need(False,"test mismatch")
  patched=dict(self.public["summary"],distinct_referenced_original_same_carrier_bitmap_ids=1569)
  self.assertNotEqual(patched,self.rebuilt["summary"])

if __name__=="__main__":unittest.main()
