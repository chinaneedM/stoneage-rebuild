"""Evidence boundary: 25 actual private pixel comparisons are NOT original client runtime."""
import json,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/recovered/STONEAGE-SCENE10-PRIVATE-PIXEL-ACCEPTANCE-R1.json'
S=ROOT/'research/recovered/STONEAGE-SCENE10-SOURCE-RANGE-RESULT-R1.json'
C=ROOT/'research/recovered/STONEAGE-SCENE10-SOURCE-CUSTODY-R1.json'
R9=ROOT/'research/recovered/STONEAGE-SCENE09-INDEPENDENT-PIXELS-R9.json'
def validate(p,s,c,r9):
 def need(ok,msg):
  if not ok:raise ValueError(msg)
 need(p['schema']=='stoneage.scene10.private_pixel_projection_acceptance.r1','schema')
 need(p['private_viewer_sha256']=='00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4','private viewer identity')
 need(p['private_source_png_total']==p['private_source_room_png']+p['private_source_actor_png']==218,'source PNG number')
 need(p['source_sha256_per_png_verified'] is True and p['room_map_placements']==30,'private observation')
 grid=p['pixels_changed_by_row_y13_to_y17']
 need(len(grid)==5 and all(len(row)==5 for row in grid),'5x5 cases')
 need(p['per_axis_x']==list(range(13,18)) and p['per_axis_y']==list(range(13,18)),'source anchors')
 need(sum(map(sum,grid))==p['total_changed_RGBA_pixel_positions']==7117884,'pixel conservation')
 need(p['all_positions_changed']==sum(x>0 for row in grid for x in row)==25,'all positions changed')
 need(p['canvas']==[960,720] and p['real_browser_js_errors']==0,'browser canvas')
 need(p['real_browser_pngs_loaded']==218 and p['real_browser_and_independent_pillow_pixels_identical'] is True,'independent pixels')
 need(len(p['real_browser_samples'])==3 and all(x['matches_independent_pillow'] for x in p['real_browser_samples']),'3 browser frame samples')
 prior=next(x for x in r9['position_cases'] if x['anchor']==[15,15])
 need(p['r9_unshifted_sha256']==prior['candidate_RGBA_sha256'],'actual R9 anchor')
 need(p['r9_unshifted_sha256']!=p['r10_shifted_independent_sha256'],'actual changed image')
 need(s['status']=='PREFIX_DOES_NOT_PROVE_EXE_AVAILABILITY' and s['native_exe_source_verified'] is False,'negative source result')
 need(s['fetch_metadata']['prefix_bytes']==16777216 and s['fetch_metadata']['list_returncode']==2,'range boundary')
 need(c['artifact']['zip_sha256']=='6d0dfe2d9291781f066db1fb990a7599a22b82a9dc6438fb82f5bb20890f38c8','artifact digest')
 need(c['corrected_source_run']['source_result_status']==s['status'],'source custody')
 for flag in ['original_exe_bytes_verified_this_work_unit','original_map_x_offset_native_authenticated','original_world_entered','original_GPU_occlusion_authenticated','original_species_identity_authenticated','private_assets_in_public_git']:
  need(p[flag] is False,'historical/runtime promotion: '+flag)
 need(p['overall_restoration_percent'] is None,'not a percentage')
 return {'anchors':25,'changed_pixels':7117884,'private_browser_match_cases':3,'original_exe_verified':False}
class TestR10Evidence(unittest.TestCase):
 def setUp(self):
  self.p=json.loads(P.read_text());self.s=json.loads(S.read_text());self.c=json.loads(C.read_text());self.r9=json.loads(R9.read_text())
 def test_snapshot(self):self.assertEqual(validate(self.p,self.s,self.c,self.r9)['anchors'],25)
 def altered(self,change):
  p=copy.deepcopy(self.p);s=copy.deepcopy(self.s);c=copy.deepcopy(self.c);change(p,s,c)
  with self.assertRaises(ValueError):validate(p,s,c,self.r9)
 def test_prevent_original_pixel_promotion(self):self.altered(lambda p,s,c:p.update(original_map_x_offset_native_authenticated=True))
 def test_prevent_world_promotion(self):self.altered(lambda p,s,c:p.update(original_world_entered=True))
 def test_prevent_exe_qualified(self):self.altered(lambda p,s,c:p.update(original_exe_bytes_verified_this_work_unit=True))
 def test_negative_source_wont_pass_as_positive(self):self.altered(lambda p,s,c:s.update(status='ORIGINAL_EXE_VERIFIED'))
 def test_detect_pixel_mutation(self):self.altered(lambda p,s,c:p['pixels_changed_by_row_y13_to_y17'][0].__setitem__(0,0))
 def test_detect_omitted_position(self):self.altered(lambda p,s,c:p['pixels_changed_by_row_y13_to_y17'].pop())
 def test_detect_browser_mismatch(self):self.altered(lambda p,s,c:p['real_browser_samples'][1].update(matches_independent_pillow=False))
 def test_detect_unsafe_git(self):self.altered(lambda p,s,c:p.update(private_assets_in_public_git=True))
 def test_no_source_binary_fields(self):
  for v in [self.p,self.s,self.c]:self.assertFalse(any(key in v for key in ('raw_original_exe','raw_sprite_bytes','original_image_base64','library_file_id')))
if __name__=='__main__':unittest.main()
