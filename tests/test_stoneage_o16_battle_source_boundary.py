import unittest,copy
from tools.stoneage_o16_battle_source_boundary import load,validate
class O16Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.org=load()
 def bad(self,mut):
  d=copy.deepcopy(self.org);mut(*d)
  with self.assertRaises((ValueError,AssertionError,KeyError,TypeError)):validate(*d)
 def test_true(self):self.assertEqual(validate(*self.org)['sabs'],218)
 def test_not_218_full_render(self):self.bad(lambda a,b,c:a['source_bitmap_coverage'].__setitem__('full_scene_source_RD_coverage',218))
 def test_rd_failed(self):self.bad(lambda a,b,c:a['source_bitmap_coverage'].__setitem__('source_rd_codec_open_count',0))
 def test_no_fake_pixel_completion(self):self.bad(lambda a,b,c:a['source_bitmap_coverage'].__setitem__('source_rd_decoded',2296))
 def test_native_offset(self):self.bad(lambda a,b,c:a['battle_sab_records'][201].__setitem__('packed_offset',201*804))
 def test_missing_sab(self):self.bad(lambda a,b,c:a['battle_sab_records'].pop())
 def test_duplicate_content_kept(self):self.bad(lambda a,b,c:a['source_bitmap_coverage'].__setitem__('duplicate_index_group',[]))
 def test_palette15_location(self):self.bad(lambda a,b,c:a['embedded_palette_records'][14].__setitem__('packed_offset',9999))
 def test_palette0_false(self):self.bad(lambda a,b,c:a['native_manifest'].__setitem__('palet0_in_container',True))
 def test_no_original_executed(self):self.bad(lambda a,b,c:a['evidence_boundaries'].__setitem__('original_executable_or_original_server_executed',True))
 def test_no_game_world(self):self.bad(lambda a,b,c:a['evidence_boundaries'].__setitem__('game_world_entered',True))
 def test_native_color_unknown(self):self.bad(lambda a,b,c:a['evidence_boundaries'].__setitem__('native_runtime_palette_selector_proven',True))
 def test_specific_region_unknown(self):self.bad(lambda a,b,c:a['evidence_boundaries'].__setitem__('official_specific_map_or_region_names_proven',True))
 def test_rd_failure_identity(self):self.bad(lambda a,b,c:a['source_bitmap_coverage'].__setitem__('source_rd_codec_open_id',6728))
 def test_invalid_sha(self):self.bad(lambda a,b,c:a['battle_sab_records'][65].__setitem__('sha256','0'*64))
 def test_prior_png(self):self.bad(lambda a,b,c:a['private_observer']['source_candidate_pngs']['0'].__setitem__('png_sha256','0'*64))
 def test_no_proprietary_public(self):self.bad(lambda a,b,c:a['private_observer'].__setitem__('source_pixels_in_public_git',True))
 def test_no_fake_100pct(self):self.bad(lambda a,b,c:a['evidence_boundaries'].__setitem__('restoration_percent',100))
 def test_r79_preserve(self):self.bad(lambda a,b,c:a['project_gates'].__setitem__('R79_paused_nonblocking',False))
if __name__=='__main__':unittest.main()
