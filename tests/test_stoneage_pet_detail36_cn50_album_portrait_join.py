"""PET36: one original-source-byte lineage, one explicitly non-native collision projection."""
import unittest
from tools.stoneage_pet_detail36_cn50_album_portrait_join import audit,SEVEN

class SourceJoin(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=audit()
 def test_source_conservation(self):
  a=self.a
  self.assertEqual((a["counts"]["all_album_slots"],a["counts"]["named_album_rows"]),(362,305))
  self.assertEqual(a["counts"]["named_aliases_with_last_record_projection"]+
                   a["counts"]["named_aliases_without_last_record_projection"],305)
  self.assertEqual(a["counts"]["distinct_named_aliases"],305)
  for x in a["records"]:
   self.assertEqual(x["same_CAB_ADRN_last_record_projection_present"],x["same_CAB_rd_block_sha256"] is not None)
   self.assertFalse(x["actual_native_renderer_selection_verified"])
   self.assertFalse(x["historical_official_live_release_verified_by_this_join"])
   self.assertFalse(x["duplicate_original_ADRN_candidates_ruled_out"])
 def test_historical_seven_names_and_egg_negative_control(self):
  self.assertEqual(set(self.a["seven_historical_name_source_checks"]),set(SEVEN))
  self.assertTrue(self.a["known_collision_negative_control"]["one_record_projection_is_not_original_full_candidate_list"])
  self.assertTrue(self.a["known_collision_negative_control"]["last_in_ADRN_is_not_proven_game_display_choice"])
  self.assertFalse(self.a["claims"]["album_name_is_an_actually_issued_live_pet"])
  self.assertEqual(self.a["counts"]["live_pet_issuance_newly_verified"],0)
  self.assertTrue(any(x["client_compiled_name"]=="宠物蛋" for x in self.a["records"]))
 def test_source_and_rights(self):
  self.assertEqual(self.a["active_module"],"PET")
  self.assertEqual(self.a["scope"],"CLASSIC_PC_ONLY")
  self.assertFalse(self.a["claims"]["saved_CAB_independently_certified_official_distribution"])
  self.assertFalse(self.a["source_safety"]["raw_commercial_images_binaries_published"])
  self.assertIsNone(self.a["source_safety"]["overall_percent"])

if __name__=="__main__":
 unittest.main()
