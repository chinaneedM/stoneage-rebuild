"""Verify archived exact executed TW1.0 resource-matrix rows from source gzip tables."""
from __future__ import annotations
import copy,json
import unittest
from pathlib import Path
from tools.stoneage_pet_asset_growth_catalog import inspect_repository_metadata,gitblob
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered/STONEAGE-PET-ASSET-GROWTH-CATALOG-MATRIX-R1.json"
class ArchivedSourceRows(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(REC.read_text(encoding="utf-8"))
  cls.real=inspect_repository_metadata()
 def test_recorded_report_exact_match(self):
  self.assertEqual(self.r["resource_report"],self.real)
 def test_fixed_historical_source_blob(self):
  for path,expected in self.r["source_git_blobs"].items():
   self.assertEqual(gitblob((ROOT/path).read_bytes()),expected,path)
 def test_true_action_result_and_no_false_game_proof(self):
  self.assertEqual(self.r["executed_action"]["id"],39024292573)
  self.assertEqual(self.r["executed_action"]["job"],117372109124)
  self.assertEqual(self.r["executed_action"]["conclusion"],"SUCCESS")
  self.assertEqual(self.r["resource_report"]["record_counts"]["frames_without_adrn_or_sentinel"],0)
  self.assertEqual(self.r["resource_report"]["record_counts"]["frames_joined_to_original_adrn"],238593)
  self.assertEqual(self.r["resource_report"]["record_counts"]["sentinel_frames"],3492)
  for k in ("original_pets_complete","game_runtime_rendering_verified","modern_render_assets_built","original_service_data_acquired"):
   self.assertFalse(self.r[k],k)
  self.assertIsNone(self.r["original_pet_species_count"])
 def test_100410_all_sentinel_not_species(self):
  target=next(x for x in self.r["resource_report"]["sample_groups"] if x["spr_no"]==100410)
  self.assertEqual(target["frame_records"],352)
  self.assertEqual(target["adrn_bitmap_references"],0)
  self.assertEqual(target["sentinel_frames"],352)
  self.assertIsNone(target["species_identity"])
if __name__=="__main__":unittest.main()
