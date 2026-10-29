import copy,json,unittest
from tools.stoneage_scene24_shop_images import REPORT,FALSE,validate,source_items
from pathlib import Path
class Scene24(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=json.loads(REPORT.read_bytes())
 def reject(self,f):
  r=copy.deepcopy(self.base);f(r)
  with self.assertRaises(ValueError):validate(r)
 def test_three_original_candidates(self):self.assertEqual(validate(self.base)['alias_candidate_bitmaps'],[6006,6005,5986])
 def test_all_boundary_promotions_rejected(self):
  for flag in FALSE:
   with self.subTest(flag=flag):self.reject(lambda r:r.update({flag:True}))
 def test_zero_is_valid_ID(self):self.assertEqual(self.base['items'][0]['id'],0)
 def test_zero_cannot_be_dropped(self):self.reject(lambda r:r['items'].pop(0))
 def test_original_order_not_sorted_by_name(self):self.reject(lambda r:r['items'].reverse())
 def test_source_imagenumber_not_physical_bitmap(self):self.reject(lambda r:r['items'][0]['alias_candidate'].update(bitmapno=20033))
 def test_literal_control_not_alias(self):self.reject(lambda r:r['items'][0]['literal_bitmap_control'].update(bitmapno=6006))
 def test_alias_multiplicity_not_guessed(self):self.reject(lambda r:r['items'][0]['alias_candidate'].update(alias_matches_in_full_mixed_ADRN=2))
 def test_physical_duplicate_not_last_wins(self):self.reject(lambda r:r['items'][0]['literal_bitmap_control'].update(physical_matches_in_full_mixed_ADRN=2))
 def test_distinct_namespace_values(self):
  for item in self.base['items']:self.assertNotEqual(item['alias_candidate']['RD_sha256'],item['literal_bitmap_control']['RD_sha256'])
 def test_wrong_original_row(self):self.reject(lambda r:r['items'][0]['source_row'].update(row_sha256='0'*64))
 def test_cost_not_runtime_price(self):self.reject(lambda r:r.update(computed_runtime_prices=[65,105,260]))
 def test_no_level_gate_guess(self):self.reject(lambda r:r['items'][0]['source_row']['numeric_fields'].update(level=10))
 def test_not_a_TW10_item_master(self):self.reject(lambda r:r.update(scope='TW10_OFFICIAL_ITEM_MASTER'))
 def test_old_prefix_bridge_required(self):self.reject(lambda r:r['prefix_bridge'].update(REAL_prefix_bytes=1000))
 def test_no_fake_mixed_REAL_read(self):self.reject(lambda r:r.update(current_mixed_REAL_bytes_read=763908374))
 def test_current_full_ADRN_prefix_required(self):self.reject(lambda r:r.update(current_full_mixed_ADRN_prefix_reverified=False))
 def test_wrong_source_record(self):self.reject(lambda r:r['items'][0]['alias_candidate'].update(record_sha256='0'*64))
 def test_original_RGBA_metadata_immutable(self):self.reject(lambda r:r['items'][0]['alias_candidate']['palette_candidates']['1'].update(RGBA_sha256='0'*64))
 def test_no_fake_Action(self):self.reject(lambda r:r.update(source_Action_run_id=123))
 def test_no_completion_percent(self):self.reject(lambda r:r.update(overall_completion_percent=100))
 def test_source_table_sha_required(self):self.reject(lambda r:r['source_members']['itemset.txt'].update(sha256='0'*64))
 def test_no_runtime_namespace_claim(self):self.reject(lambda r:r.update(source_namespace_grade='NATIVE_DRAW_PROVEN'))
 def test_bounded_six_images_not_just_three(self):self.reject(lambda r:r.update(selected_images=3))
if __name__=='__main__':unittest.main()
