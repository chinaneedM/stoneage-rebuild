"""Minimal O63 regression: strict source-only join and immutability guards."""
import unittest,copy
from tools.stoneage_o63_tiger_spr_join import derive,KEYS
class TestO63(unittest.TestCase):
 def test_exact_original_four_spr_content_from_metadata(self):
  r=derive();self.assertEqual([x["spr_no"] for x in r["groups"]],list(KEYS))
  self.assertEqual(len(set(x["original_tw10_full_segment_sha256"] for x in r["groups"])),4)
  self.assertEqual(sum(x["original_tw10_animation_count"] for x in r["groups"]),224)
  self.assertEqual(sum(x["original_tw10_frame_positions"] for x in r["groups"]),r["sum_original_tw10_frame_positions"])
  self.assertTrue(all(x["original_tw10_distinct_nonzero_bitmap_keys"]>0 for x in r["groups"]))
  self.assertEqual([x["saved_mixed25_index"] for x in r["groups"]],[301,302,303,304])
  self.assertTrue(all(len(x["original_tw10_first_frame_direction0_by_action"])>=1 for x in r["groups"]))
  for k in ("original_game_world_entered","original_sprites_published",
            "tw10_original_bitmap_pixels_read_this_run","tw10_and_mixed25_full_segment_byte_equality_proven"):
   self.assertIs(r[k],False)
  self.assertIsNone(r["overall_completion_percent"])
if __name__=="__main__":unittest.main()
