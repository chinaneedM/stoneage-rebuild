"""O20 public derived-only negative guards; never open proprietary originals in CI."""
import copy,json,unittest
from tools.stoneage_o20_source_guard import REPORT,check
class O20SourceGuardTests(unittest.TestCase):
    def setUp(self):self.original=json.loads(REPORT.read_bytes())
    def test_accepted(self):
        self.assertEqual(check(self.original)["physical_bitmap"],5884)
    def test_24_mutations_rejected(self):
        changes=[
          ("source_main_head",None,"old"),
          ("preserved_current_blob",None,"0"*40),
          ("source_create","xy",[13,12]),
          ("source_create","logical_graphic_name",5884),
          ("source_create","selected_original_block_sha256","0"*64),
          ("original_TW10_graphic","aliased_record_index",16038),
          ("original_TW10_graphic","bitmapno",16038),
          ("original_TW10_graphic","rd_sha256","0"*64),
          ("original_TW10_graphic","decoded_index_sha256","0"*64),
          ("original_TW10_graphic","RD_flag",0),
          ("original_TW10_graphic","wh",[40,80]),
          ("original_TW10_graphic","physical_record_16038_is_different",False),
          ("original_TW10_graphic","independent_decoders_match",False),
          ("visual_observer","NPC_canvas_left_top",[0,0]),
          ("visual_observer","source_background_RGBA_SHA256","0"*64),
          ("visual_observer","scene_with_NPC_RGBA_SHA256","0"*64),
          ("visual_observer","actual_browser_original_png_canvas_match_two_states",False),
          ("visual_observer","actual_mixed25_ADRN_REAL_original_bytes_revalidated_this_turn",True),
          ("visual_observer","original_RGBA_palette_runtime_proven",True),
          ("visual_observer","browser_external_requests",1),
          ("private_custody","original_assets_committed_public_Git",True),
          ("private_custody","zip_full_CRC_and_original_replay_verified",False),
          ("limits","original_game_world_entered",True),
          ("limits","overall_percent",100)]
        for section,field,val in changes:
            with self.subTest(section=section,field=field):
                x=copy.deepcopy(self.original)
                if field is None:x[section]=val
                else:x[section][field]=val
                with self.assertRaises(ValueError):check(x)
if __name__=="__main__":unittest.main()
