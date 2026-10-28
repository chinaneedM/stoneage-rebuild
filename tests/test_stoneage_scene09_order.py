import copy,json,unittest
from tools.stoneage_scene09_evidence_guard import REPORT,validate
from tools.stoneage_private_scene_actor_order_r9 import reference_list

class SourceOrder(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_text())
    def test_original_trace(self):self.assertEqual(validate(self.r)['cases'],48)
    def test_world_or_full_phase_promotions_rejected(self):
        for k in ['original_world_entered','native_GPU_blit_executed','complete_original_frame_phase_order_proven','official_species_identity_authenticated']:
            r=copy.deepcopy(self.r);r[k]=True
            with self.subTest(k=k),self.assertRaisesRegex(ValueError,'promotion'):validate(r)
    def test_injected_state_cannot_be_described_as_live_capture(self):
        for k in ['actor_structures_and_coordinates_injected','actor_then_parts_phase_order_injected','source_ADRN_array_injected']:
            r=copy.deepcopy(self.r);r[k]=False
            with self.subTest(k=k),self.assertRaisesRegex(ValueError,'injected'):validate(r)
    def test_duplicate_bitmap_instances_cannot_be_deduplicated(self):
        r=copy.deepcopy(self.r);r['original_parts'].pop(1)
        with self.assertRaisesRegex(ValueError,'occurrences'):validate(r)
    def test_native_relative_order_cannot_be_replaced_with_always_front(self):
        r=copy.deepcopy(self.r);r['cases'][4]['native_draw_tokens']=list(reversed(range(30)))+['human','pet']
        with self.assertRaisesRegex(ValueError,'consumption'):validate(r)
    def test_unsupported_footprint_refused(self):
        actors=copy.deepcopy(self.r['cases'][0]['actors']);parts=copy.deepcopy(self.r['original_parts']);parts[0]['footprint']=[2,1]
        with self.assertRaisesRegex(ValueError,'footprint'):reference_list(actors,parts)
    def test_metadata_getter_stubs_refused(self):
        r=copy.deepcopy(self.r);r['native_functions_stubbed']=['ADRN_getter']
        with self.assertRaisesRegex(ValueError,'stubs'):validate(r)
    def test_equal_screen_anchor_keeps_actor_in_front_after_reverse(self):
        c=self.r['cases'][12];self.assertEqual(c['anchor'],[15,15]);self.assertEqual(c['native_draw_tokens'][-2:],['human','pet'])
    def test_raw_instruction_or_private_asset_absent(self):
        for needle in ['data:image','base64','PRIVATE KEY','library_file_id']:self.assertNotIn(needle,REPORT.read_text())

if __name__=='__main__':unittest.main()
