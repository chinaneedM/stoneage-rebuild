"""O21 source-only derived guard mutation tests. No original copyrighted payloads."""
import json, copy, unittest
from tools.stoneage_o21_encounter_two_named_pets import REPORT,validate
class O21SourceContracts(unittest.TestCase):
    def setUp(self):self.d=json.loads(REPORT.read_bytes())
    def test_positive_record(self):
        self.assertEqual(validate(self.d)["original_TW10_first_selected_frames_checked"],24)
    def test_negative_promotion_mutations(self):
        edits=[
          ("bounded_original_encounter","floor",1003),
          ("bounded_original_encounter","trigger_executed",True),
          ("bounded_original_encounter","two_selected_positive_group_weight_pairs",[[88,50],[91,0]]),
          ("original_pixel_replay","source_24_frame_ordered_canvas_digest","0"*64),
          ("original_pixel_replay","24_frame_pixels_all_same_actual_chromium_canvas",False),
          ("original_pixel_replay","user_local_file_navigation_verified",True),
          ("private_custody","private_zip_sha256","0"*64),
          ("private_custody","copyrighted_client_assets_in_public_Git",True),
          ("strict_boundaries","original_game_world_entered",True),
          ("strict_boundaries","TW10_official_named_species_identity_proven",True),
          ("strict_boundaries","historical_gameplay_encounter_executed",True),
          ("strict_boundaries","overall_completion_percent",100)
        ]
        for scope,key,val in edits:
            with self.subTest(scope=scope,key=key):
                x=copy.deepcopy(self.d);x[scope][key]=val
                with self.assertRaises(ValueError):validate(x)
    def test_numeric_template_and_sprite_namespace_mutations(self):
        for pos in (0,1):
            for key,value in (("enemybase_IMGNUMBER",100250),("TW10_SPR_group_index",999),("selected_frame_count",1),("selected_first_frame_bitmapno",1),("CP950_and_Big5_same",False)):
                with self.subTest(pos=pos,key=key):
                    x=copy.deepcopy(self.d);x["source_named_pet_links"][pos][key]=value
                    with self.assertRaises(ValueError):validate(x)
if __name__=="__main__":unittest.main()
