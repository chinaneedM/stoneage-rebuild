"""Check exact original index numeric intersections without semantic over-promotion."""
import unittest
from tools.stoneage_tw10_visual_category_spr_join import audit

class OriginalBitmapSPRRangeJoin(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=audit()
    def test_complete_original_indexes(self):
        d=self.data
        self.assertEqual(d["original_tw10_bitmap_ids"],[0,125995])
        self.assertEqual(d["original_tw10_bitmap_count"],125996)
        self.assertEqual(d["original_spr_group_count"],464)
        self.assertEqual(d["original_animation_count"],39065)
        self.assertEqual(d["original_frame_count"],242085)
        self.assertEqual(d["sentinel_frame_count"],3492)
        self.assertEqual(d["non_sentinel_frame_count"],238593)
    def test_category_reference_set_monotone_and_source_bounded(self):
        self.assertEqual(len(self.data["categories"]),7)
        ids={x["category_id"] for x in self.data["categories"]}
        self.assertIn("pet_portrait",ids)
        self.assertIn("pet_actions",ids)
        for item in self.data["categories"]:
            self.assertGreater(item["candidate_bitmap_ids_present_in_tw10"],0)
            self.assertLessEqual(item["original_distinct_bitmap_ids_referenced_by_spr"],item["candidate_bitmap_ids_present_in_tw10"])
            self.assertEqual(item["original_distinct_bitmap_ids_referenced_by_spr"]+item["original_distinct_bitmap_ids_not_referenced_by_spr"],item["candidate_bitmap_ids_present_in_tw10"])
            self.assertLessEqual(item["original_spr_groups_with_all_nonsentinel_frames_in_range"],item["original_spr_groups_touching_range"])
            self.assertLessEqual(item["original_spr_groups_touching_range"],464)
            self.assertFalse(item["historical_game_semantic_certified"])
            self.assertFalse(item["species_master_or_avatar_identity_certified"])
            self.assertFalse(item["original_render_selection_proven"])
    def test_negative_boundaries(self):
        d=self.data
        self.assertFalse(d["same_build_pet_master_available"])
        self.assertFalse(d["same_build_avatar_identity_available"])
        self.assertFalse(d["any_player_category_upgraded_to_original_semantic_fact"])
        self.assertFalse(d["original_client_render_execution_tested"])
        self.assertFalse(d["copyrighted_original_bitmaps_committed"])
        self.assertFalse(d["historical_quest_data_connected"])
        self.assertIsNone(d["historical_pet_species_total"])
if __name__=="__main__":unittest.main()
