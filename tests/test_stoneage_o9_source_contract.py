"""Source-only O9 acceptance: never mistake original art pixels for original gameplay."""
import copy
import json
import unittest
from tools.stoneage_o9_source_contract import R,validate
class O9Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=json.loads(R.read_text(encoding="utf-8"))
    def test_public_derived_pass(self):self.assertEqual(validate(self.d)["new_placements"],103)
    def mutate(self,path,bad):
        d=copy.deepcopy(self.d);o=d
        for key in path[:-1]:o=o[key]
        o[path[-1]]=bad
        with self.assertRaises(ValueError):validate(d)
    def test_bad_original_SHA(self):self.mutate(["source_sha256","tw1_REAL"],"0"*64)
    def test_fake_original_runtime(self):self.mutate(["status","original_game_world_entered"],True)
    def test_fake_tw1_map(self):self.mutate(["status","official_TW1_map_deployment_verified"],True)
    def test_false_palette(self):self.mutate(["image","native_palette_and_draw_order_authenticated"],True)
    def test_collision_not_proven(self):self.mutate(["room","third_plane_collision_proven"],True)
    def test_too_few_tiles(self):self.mutate(["room","visible_appearances"],132)
    def test_wrong_o8_overlap(self):self.mutate(["o8_overlap","new_outside_o8"],104)
    def test_missing_one_image(self):self.mutate(["map_graphic_ids"],self.d["map_graphic_ids"][:-1])
    def test_wrong_private_zip(self):self.mutate(["private","zip_sha256"],"0"*64)
    def test_wrong_private_zip_member_count(self):self.mutate(["private","members"],327)
    def test_false_file_open(self):self.mutate(["browser","user_local_file_verified"],True)
    def test_original_assets_not_public(self):self.mutate(["status","private_art_in_public_git"],True)
    def test_percent_never_invented(self):self.mutate(["status","overall_completion_percent"],100)
if __name__=="__main__":unittest.main()
