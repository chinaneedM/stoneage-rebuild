"""O10 source-contract mutations: reject imaginary historic-game execution."""
import copy,json,unittest
from tools.stoneage_o10_source_contract import REPORT,validate
class TestO10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_text(encoding="utf-8"))
    def test_accept_actual_source_derived(self):self.assertEqual(validate(self.data)["actual_placements"],492)
    def reject(self,path,value):
        d=copy.deepcopy(self.data);node=d
        for p in path[:-1]:node=node[p]
        node[path[-1]]=value
        with self.assertRaises(ValueError):validate(d)
    def test_reject_wrong_original_map_SHA(self):self.reject(["original_source_pins","MAP","sha256"],"0"*64)
    def test_reject_missing_RD_alias(self):self.reject(["material_delta","source_graphic_ids"],self.data["material_delta"]["source_graphic_ids"][:-1])
    def test_reject_false_1000_deployed_TW1(self):self.reject(["historical_guards","official_TW1_or_JSS1999_deployment_map_verified"],True)
    def test_reject_world_executed(self):self.reject(["historical_guards","original_native_client_map_world_entered"],True)
    def test_reject_collision(self):self.reject(["historical_guards","original_collision_or_walkability_verified"],True)
    def test_reject_wrong_viewport(self):self.reject(["material_delta","source_view_inclusive"],[60,96,66,106])
    def test_reject_invented_new_128_count(self):self.reject(["material_delta","additional_distinct_graphic_ids_vs_O4"],129)
    def test_reject_wrong_492_count(self):self.reject(["material_delta","actual_map_tile_and_parts_appearances"],491)
    def test_reject_wrong_RGBA(self):self.reject(["candidate_visual","full_pixel_rgba_sha256"],"0"*64)
    def test_reject_scene_native_claim(self):self.reject(["candidate_visual","scene_native_draw_or_palette_proven"],True)
    def test_reject_browser_local_success(self):self.reject(["browser","end_user_file_open_verified"],True)
    def test_reject_library_upload_false_claim(self):self.reject(["private_custody","persistent_library_upload_completed"],True)
    def test_reject_public_private_original_content(self):self.reject(["historical_guards","original_proprietary_assets_committed_to_public_git"],True)
    def test_reject_audio_event_claim(self):self.reject(["historical_guards","original_audio_event_association_verified"],True)
    def test_reject_fake_overall_completion(self):self.reject(["historical_guards","overall_completion_percent"],100)
if __name__=="__main__":unittest.main()
