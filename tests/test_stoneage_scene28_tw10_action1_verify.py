import copy,json,unittest,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'tools/stoneage_scene28_tw10_action1_verify.py'
spec=importlib.util.spec_from_file_location('scene28',p)
scene28=importlib.util.module_from_spec(spec);spec.loader.exec_module(scene28)
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(scene28.PUBLISHED.read_text());cls.old=scene28.load_prior()
 def test_public_provenance(self):self.assertTrue(scene28.published_gate(self.report,self.old))
 def test_source_version_not_promoted(self):
  r=copy.deepcopy(self.report);r['historical_source_scope']='JSS_1999';
  with self.assertRaisesRegex(ValueError,'source identity'):scene28.published_gate(r,self.old)
 def test_distinct_bitmap_not_duplicated(self):
  r=copy.deepcopy(self.report);r['TW10_actual_adrn_real_pixel_receipts'][0]['bitmapno']=r['TW10_actual_adrn_real_pixel_receipts'][1]['bitmapno'];
  with self.assertRaisesRegex(ValueError,'missing/duplicate'):scene28.published_gate(r,self.old)
 def test_wrong_golden_spr_segment(self):
  r=copy.deepcopy(self.report);r['same_segment_as_R40_preserved_mixed25'][0]['whole_spr_segment_sha256']='f'*64;
  with self.assertRaisesRegex(ValueError,'cross-build'):scene28.published_gate(r,self.old)
 def test_false_original_world_run(self):
  r=copy.deepcopy(self.report);r['evidence_limits']['original_game_world_entered']=True
  with self.assertRaisesRegex(ValueError,'unproven'):scene28.published_gate(r,self.old)
 def test_undecoded_bitmap_mask_rejected(self):
  r=copy.deepcopy(self.report);r['actual_source_replay_results']['RD_decode_count']=47
  with self.assertRaisesRegex(ValueError,'actual direct pixel'):scene28.published_gate(r,self.old)
 def test_actual_file_length_altered(self):
  r=copy.deepcopy(self.report);r['exact_original_source_files']['spr_1.bin']['bytes']+=1
  with self.assertRaisesRegex(ValueError,'full-file'):scene28.published_gate(r,self.old)
 def test_original_pixel_sha_format(self):
  r=copy.deepcopy(self.report);r['TW10_actual_adrn_real_pixel_receipts'][0]['index_pixels_sha256']='fake'
  with self.assertRaisesRegex(ValueError,'hash format'):scene28.published_gate(r,self.old)
 def test_source_pixel_count_must_stay_exact(self):
  r=copy.deepcopy(self.report);r['TW10_actual_adrn_real_pixel_receipts'][0]['visible_index_pixels']+=1
  with self.assertRaisesRegex(ValueError,'pixel occupancy total'):scene28.published_gate(r,self.old)
 def test_RD_decoding_literal_and_repeat_and_zero(self):
  from struct import pack
  # Literal [1,2], repeat 3 twice, zero once: 5 pixels total
  raw=b'RD'+bytes([1,0])+pack('<III',5,1,0)+bytes([0x02,1,2,0x82,3,0xc1])
  self.assertEqual(scene28.rd_index_pixels(raw)[:3],(5,1,bytes([1,2,3,3,0])))
 def test_RD_control_negative(self):
  from struct import pack
  raw=b'RD'+bytes([1,0])+pack('<III',1,1,0)+bytes([0xff])
  with self.assertRaises(ValueError):scene28.rd_index_pixels(raw)
if __name__=='__main__':unittest.main()