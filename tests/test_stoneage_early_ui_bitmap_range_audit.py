import unittest
from tools.stoneage_early_ui_bitmap_range_audit import audit
class Early2001VisualRangeEvidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=audit()
  cls.r={x["id"]:x for x in cls.p["ranges"]}
 def test_original_adrn_complete_bitmap_envelope(self):
  self.assertEqual(self.p["tw10_adrn_bitmap_records"],125996)
  self.assertEqual(self.p["tw10_bitmap_range"],[0,125995])
  self.assertEqual(self.p["unclassified_tw10_ids"],[0,95879,95880,95881,95882])
 def test_2001_pet_and_avatar_claims_not_original_semantic_proof(self):
  for id,count in [("pet_portrait",121),("character_portrait",1200),("character_actions",73438),("pet_actions",30113)]:
   with self.subTest(id=id):
    self.assertEqual(self.r[id]["claimed_count"],count)
    self.assertEqual(self.r[id]["present_in_tw10_adrn"],count)
    self.assertFalse(self.r[id]["category_tw10_verified"])
 def test_later_mainland_login_is_outside_original_v1(self):
  self.assertFalse(self.p["external_mainland_login_image_126766_in_tw10"])
  self.assertEqual(self.r["later_ui_variants"]["present_in_tw10_adrn"],0)
 def test_character_compiled_fields_but_no_actual_ui(self):
  self.assertEqual(self.p["create_new_character_compiled_fields"],13)
  self.assertTrue(self.p["body_face_image_fields_verified"])
  self.assertFalse(self.p["tw10_actual_login_render_verified"])
  self.assertFalse(self.p["orig_v1_client_ui_rendering_complete"])
  self.assertIsNone(self.p["historic_pet_species_count"])
if __name__=="__main__":unittest.main()
