"""R99 101 real TW1.0 candidate image resource row joins and negative claims."""
import copy
import unittest
from tools.stoneage_tw10_npc_static_resource_r99 import audit,validate_report,check_saved

class R99ResourceJoin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.truth=audit()
    def broken(self,change):
        a=copy.deepcopy(self.truth)
        change(a)
        with self.assertRaises(ValueError):
            validate_report(a,self.truth)
    def test_two_original_map_resource_number_runs(self):
        rows=self.truth["rows"]
        self.assertEqual((rows[0]["bitmapno"],rows[73]["bitmapno"],rows[0]["map_number"],rows[73]["map_number"]),(5846,5919,16000,16073))
        self.assertEqual((rows[74]["bitmapno"],rows[100]["bitmapno"],rows[74]["map_number"],rows[100]["map_number"]),(5920,5946,16200,16226))
        self.assertEqual([rows[i+1]["map_number"]-rows[i]["map_number"] for i in range(100) if rows[i+1]["map_number"]-rows[i]["map_number"]!=1],[127])
    def test_full_original_join(self):
        self.assertTrue(validate_report(self.truth,self.truth))
    def test_saved_report_byte_exact(self):
        self.assertTrue(check_saved(self.truth))
    def test_bitmap_not_npc_id(self):
        self.broken(lambda d:d["rows"][0].update(original_npc_id=16000))
    def test_map_number_not_floor(self):
        self.broken(lambda d:d["rows"][0].update(world_floor_id=16000))
    def test_species_name_not_guessed(self):
        self.broken(lambda d:d["rows"][0].update(npc_name="卡坦"))
    def test_full_row_digest_evidence(self):
        self.broken(lambda d:d["rows"][8].update(rd_block_sha256="0"*64))
    def test_numeric_join_not_corrupted(self):
        self.broken(lambda d:d["rows"][100].update(map_number=16000))
    def test_original_index_order_preserved(self):
        self.broken(lambda d:d["rows"].reverse())
    def test_zero_frame_not_no_runtime_use(self):
        self.broken(lambda d:d["limits"].update(other_original_sprite_animation_paths_disproved_by_zero=True))
    def test_npc_server_table_not_claimed(self):
        self.broken(lambda d:d["measured"].update(same_build_original_server_NPC_table_obtained=True))
    def test_exact_pixel_not_committed(self):
        self.broken(lambda d:d["limits"].update(original_pixels_committed=True))
    def test_stage_a_still_open(self):
        self.broken(lambda d:d["limits"].update(stage_a_closed=True))
    def test_no_overall_percentage(self):
        self.broken(lambda d:d["limits"].update(overall_restoration_percent=100))
    def test_no_audience_assertion(self):
        self.broken(lambda d:d.update(verified_NPC_names=101))

if __name__=="__main__":unittest.main()
