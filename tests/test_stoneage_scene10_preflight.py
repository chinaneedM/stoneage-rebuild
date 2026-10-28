import copy,json,unittest
from tools.stoneage_scene10_preflight_guard import REPORT,validate
class PhasePreflight(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_text())
    def test_baseline(self):self.assertEqual(validate(self.r)['key_calls'],20)
    def fail_mut(self,fn):
        r=copy.deepcopy(self.r);fn(r)
        with self.assertRaises(ValueError):validate(r)
    def test_missing_path(self):self.fail_mut(lambda r:r['four_candidate_paths'].pop())
    def test_swap_targets(self):self.fail_mut(lambda r:r['four_candidate_paths'][0]['key_calls'].reverse())
    def test_modified_call(self):self.fail_mut(lambda r:r['four_candidate_paths'][1]['key_calls'][2].update(target_va=0))
    def test_unreplayed_not_zero(self):self.fail_mut(lambda r:r['four_candidate_paths'][3].update(unreplayed_intervening_count=0))
    def test_no_exe_authentication(self):self.fail_mut(lambda r:r.update(source_callsite_bytes_independently_verified=True))
    def test_no_full_frame(self):self.fail_mut(lambda r:r.update(full_original_frame_proven=True))
    def test_no_world_entry(self):self.fail_mut(lambda r:r.update(original_world_entered=True))
    def test_hash_lock(self):self.fail_mut(lambda r:r.update(private_viewer_sha256='0'*64))
    def test_copyright(self):self.fail_mut(lambda r:r.update(public_proprietary_assets_included=True))
if __name__=='__main__':unittest.main()
