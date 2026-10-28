import copy,json,unittest
from tools.stoneage_scene15_exit_observer import REPORT,validate,manual_step,transition,FALSE,map_view,validate_acceptance

class DoorwaySourceObserver(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_bytes());self.start={'floor':1001,'x':11,'y':15}
    def reject(self,change):
        r=copy.deepcopy(self.r);change(r)
        with self.assertRaises(ValueError):validate(r)
    def test_original_bounded_source(self):self.assertEqual(validate(self.r)['source_occurrences'],81)
    def test_no_warp_at_manual_start(self):
        with self.assertRaises(ValueError):transition(self.start,self.r['doorway_pair'])
    def test_exact_forward_and_return_pair(self):
        door=manual_step(self.start,-1,0);out=transition(door,self.r['doorway_pair']);self.assertEqual(out,{'floor':1000,'x':63,'y':99});self.assertEqual(transition(out,self.r['doorway_pair']),door)
    def test_second_neighboring_door_not_silently_substituted(self):
        with self.assertRaises(ValueError):transition({'floor':1001,'x':10,'y':16},self.r['doorway_pair'])
    def test_wrong_floor_not_current_door(self):
        with self.assertRaises(ValueError):transition({'floor':1000,'x':10,'y':15},self.r['doorway_pair'])
    def test_outside_viewport_is_only_modern_guard(self):
        with self.assertRaises(ValueError):manual_step({'floor':1001,'x':7,'y':15},-1,0)
    def test_diagonal_not_single_grid_step(self):
        with self.assertRaises(ValueError):manual_step(self.start,1,1)
    def test_boolean_is_not_grid_integer(self):
        with self.assertRaises(ValueError):manual_step(self.start,True,0)
    def test_fractional_source_position_refused(self):
        with self.assertRaises(ValueError):transition({'floor':1001,'x':10.0,'y':15},self.r['doorway_pair'])
    def test_ambiguous_source_door_refused(self):
        with self.assertRaises(ValueError):transition({'floor':1001,'x':10,'y':15},self.r['doorway_pair']*2)
    def test_destination_cannot_leave_fixed_original_pair(self):
        d=copy.deepcopy(self.r['doorway_pair']);d[0]['destination_floor']=9999
        with self.assertRaises(ValueError):transition({'floor':1001,'x':10,'y':15},d)
    def test_source_target_tuple_cannot_be_changed(self):self.reject(lambda r:r['doorway_pair'][0].update(destination_xy=[63,100]))
    def test_old_generic_link_not_new_world_closure(self):self.reject(lambda r:r.update(scope='ALL_WORLD_RESTORED'))
    def test_source_span_hash_cannot_be_changed(self):self.reject(lambda r:r['doorway_pair'][0]['source_block'].update(block_sha256='0'*64))
    def test_source_placement_occurrence_cannot_be_dropped(self):self.reject(lambda r:r['views'][0]['placements'].pop())
    def test_aliased_key_not_physical_bitmap(self):self.reject(lambda r:r['resources']['101'].update(bitmapno=101))
    def test_large_outdoor_original_image_not_silently_cropped(self):self.reject(lambda r:r['resources']['10139'].update(height=100))
    def test_native_order_witness_not_reused(self):self.reject(lambda r:r.update(scene_order='NATIVE_R6_R9_VERIFIED'))
    def test_no_original_collision_from_plane3(self):self.reject(lambda r:r.update(map_third_plane_interpreted_as_collision=True))
    def test_no_original_schedule_from_time_field(self):self.reject(lambda r:r.update(time_field_interpreted_as_warp_schedule=True))
    def test_no_runtime_or_official_promotion(self):
        for k in FALSE:
            with self.subTest(k=k):self.reject(lambda r:r.update({k:True}))
    def test_no_restoration_percentage(self):self.reject(lambda r:r.update(overall_completion_percent=80))
    def acceptance(self):return json.loads(REPORT.with_name('STONEAGE-SCENE15-ACCEPTANCE-R1.json').read_bytes())
    def test_archived_real_browser_and_source_acceptance(self):self.assertEqual(validate_acceptance(self.acceptance(),self.r)['all_integer_scale_canvas_matches'],11)
    def test_no_false_second_decoder_success(self):
        a=self.acceptance();a['independent_secondary_DAT1000_success']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_failed_7zip_cannot_be_rewritten_success(self):
        a=self.acceptance();a['sevenzip_secondary_DAT1000_failure']['returncode']=0
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_source_map_not_called_corrupt_after_tool_failure(self):
        a=self.acceptance();a['original_DAT1000_corrupt_claimed']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_browser_wrong_arrival_not_accepted(self):
        a=self.acceptance();a['browser']['frames'][3]['state']['y']=100
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_actual_journal_cannot_be_original_gameplay(self):
        a=self.acceptance();a['browser']['frames'][-1]['state']['journal'][0]['original_runtime_executed']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_pixel_hash_divergence_not_accepted(self):
        a=self.acceptance();a['browser']['frames'][0]['canvas_sha256']='0'*64
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_source_private_execution_not_invented_CI(self):
        a=self.acceptance();a['public_CI_reads_private_original_files']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_unqualified_source_map_refused(self):
        with self.assertRaises(ValueError):map_view(b'12345678',1000)
if __name__=='__main__':unittest.main()
