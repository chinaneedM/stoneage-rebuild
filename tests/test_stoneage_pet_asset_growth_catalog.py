"""Validate actual metadata crosswalk; no animation group may be silently called a pet species."""
import copy
import unittest
from tools.stoneage_pet_asset_growth_catalog import inspect_repository_metadata
class RealMetadataTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.report=inspect_repository_metadata()
 def test_source_graphics_joins(self):
  c=self.report["record_counts"]
  self.assertEqual(c["adrn_bitmap_records"],125996)
  self.assertEqual((c["spr_groups"],c["animations"],c["frames"]),(464,39065,242085))
  self.assertEqual(c["frames_joined_to_original_adrn"]+c["frames_without_adrn_or_sentinel"]+c["sentinel_frames"],242085)
 def test_selected_groups_are_real_resource_rows(self):
  self.assertEqual([r["group_index"] for r in self.report["sample_groups"]],[0,1,2,3,4,5,102,373,463])
  for r in self.report["sample_groups"]:
   self.assertEqual(r["frame_records"],r["adrn_bitmap_references"]+r["sentinel_frames"]+r["missing_bitmap_references"])
   self.assertTrue(r["segment_sha256"] if "segment_sha256" in r else r["animation_records"]>=0)
   self.assertEqual(r["status"],"TW10_ASSET_IDENTITY_AND_FRAME_JOIN_ONLY_NOT_PET_IDENTITY")
 def test_no_unverified_pet_identity_or_growth(self):
  self.assertEqual(self.report["historical_pet_identity_verified_count"],0)
  self.assertFalse(self.report["version_promotion"])
  for r in self.report["sample_groups"]:
   self.assertIsNone(r["species_identity"])
   self.assertIsNone(r["original_growth_config"])
   self.assertIsNone(r["original_encounter_map"])
   self.assertIsNone(r["original_pet_graphic_id"])
 def test_later_enemybase_does_not_become_tw10_pet_roster(self):
  self.assertEqual(self.report["later_enemybase_status"]["active_rows"],988)
  self.assertEqual(self.report["later_enemybase_status"]["source_name_hashes_distinct"],662)
  self.assertIsNone(self.report["later_enemybase_status"]["pet_species_count_original"])
if __name__ == "__main__":unittest.main()
