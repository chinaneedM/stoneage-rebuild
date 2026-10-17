"""Verify concrete original Taiwan v1 collision source map numbers, but no world-content claim."""
import unittest
from tools.stoneage_tw10_map_content_collision_crosswalk import audit
class OriginalWorldMapCollisionSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=audit()
 def test_orig_collision_number_space(self):
  d=self.d
  self.assertEqual(d["original_collision_unique_map_numbers"],9286)
  self.assertEqual(d["original_source_order_duplicate_map_numbers"],3)
  self.assertEqual(d["original_bitmap_number_max"],125995)
  self.assertEqual(len(d["partition_rows"]),4)
  self.assertEqual(sum(x["original_tw10_collision_map_numbers"] for x in d["partition_rows"]),9286)
  self.assertEqual(sum(x["count"] for x in d["original_map_number_hit_flag_counts"]),9286)
  self.assertEqual([x["id"] for x in d["partition_rows"]],
                   ["tiles_small","tiles_large","npc_candidate","not_in_player_terrain_object_ranges"])
  for row in d["partition_rows"]:
   self.assertFalse(row["actual_early_village_or_region_membership_verified"])
   self.assertFalse(row["concrete_field_map_dat_payload_acquired"])
   self.assertFalse(row["original_v1_server_spawn_or_event_records_verified"])
 def test_server_delivered_and_no_fake_v1_map(self):
  d=self.d
  self.assertEqual(d["tw10_retail_disc_concrete_field_map_files"],0)
  self.assertTrue(d["v1_message_M_to_map_cache_write_path_verified"])
  self.assertTrue(d["v1_message_MC_to_map_cache_read_check_path_verified"])
  self.assertEqual(d["v1_cache_filename"],"map\\%d.dat")
  self.assertTrue(d["source_layer_only_not_world_map_restoration"])
  self.assertFalse(d["unverified_later_compatible_map_promoted_to_tw10"])
  self.assertFalse(d["original_server_npc_encounter_reward_data_connected"])
  self.assertFalse(d["stage_b_production_started"])
  self.assertEqual(d["next"],"TW10-AUDIO-EVENT-SOURCE-GATE-01")
if __name__=="__main__":unittest.main()
