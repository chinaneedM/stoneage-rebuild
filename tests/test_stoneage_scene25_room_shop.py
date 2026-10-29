import copy,json,unittest
from tools.stoneage_scene25_room_shop import REPORT,R14,R24,FALSE,validate,validate_binding,validate_actual,draw_body,ROOT,render

class Scene25(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=json.loads(REPORT.read_bytes())
 def reject(self,f):
  r=copy.deepcopy(self.base);f(r)
  with self.assertRaises(ValueError):validate(r)
 def test_finite_integration(self):self.assertEqual(validate(self.base)['original_PNGs'],14)
 def test_historical_promotions_refused(self):
  for k in FALSE:
   with self.subTest(k=k):self.reject(lambda r:r.update({k:True}))
 def test_no_new_source_claim(self):self.reject(lambda r:r.update(scope='NEW_ORIGINAL_SHOP_UI_DISCOVERED'))
 def test_no_wrong_floor(self):self.reject(lambda r:r['binding'].update(floor=1000))
 def test_no_neighbor_cell(self):self.reject(lambda r:r['binding'].update(xy=[17,14]))
 def test_no_wrong_graphic(self):self.reject(lambda r:r['binding'].update(graphicname=16048))
 def test_zero_retained(self):self.assertEqual(self.base['items'][0]['id'],0)
 def test_zero_drop_refused(self):self.reject(lambda r:r['items'].pop(0))
 def test_original_order(self):self.reject(lambda r:r['items'].reverse())
 def test_literal_physical_namespace_refused(self):self.reject(lambda r:r['items'][0].update(candidate_bitmap=20033))
 def test_original_item_row_pinned(self):self.reject(lambda r:r['items'][0].update(source_row_sha256='0'*64))
 def test_original_png_pinned(self):self.reject(lambda r:r['items'][0].update(PNG_sha256='0'*64))
 def test_original_room_model_pinned(self):self.reject(lambda r:r.update(room_model_sha256='0'*64))
 def test_no_extra_stock_art(self):self.reject(lambda r:r.update(added_item_PNGs=17))
 def test_no_price_computation(self):self.reject(lambda r:r.update(computed_runtime_prices=[65,105,260]))
 def test_no_source_Action_claim(self):self.reject(lambda r:r.update(source_Action_run_id=123))
 def test_no_completion_claim(self):self.reject(lambda r:r.update(overall_completion_percent=100))
 def test_palette_candidate_remains_candidate(self):self.reject(lambda r:r.update(palette_candidate_is_native_active_palette=True))
 def test_parent_bytes_pinned(self):self.reject(lambda r:r['parents']['room_archive'].update(bytes=0))
 def test_draw_implementation_identical(self):self.assertEqual(draw_body((ROOT/'tools/stoneage_scene25_observer.html').read_text()),draw_body((ROOT/'tools/scene-room-shop-viewer-r14.html').read_text()))
 def test_changed_draw_hash_refused(self):self.reject(lambda r:r.update(world_draw_body_sha256='0'*64))
 def test_explicit_close_contract(self):self.reject(lambda r:r['reader_interactions'].remove('Escape'))
 def test_no_public_original_html(self):
  s=(ROOT/'tools/stoneage_scene25_observer.html').read_text();self.assertIn('"PRIVATE_PACK_PLACEHOLDER"',s);self.assertNotIn('iVBORw0KGgo',s)
 def test_html_embed_cannot_close_script(self):self.assertIn('\\u003c/script>',render({'marker':'</script>'}))
 def test_parent_source_mutation_refused(self):
  a=json.loads(R14.read_bytes());b=json.loads(R24.read_bytes());a['npc']['floor']=1000
  with self.assertRaises(ValueError):validate_binding({},a,b)
 def test_actual_replay_preserves_old_room(self):
  a=json.loads((ROOT/'research/recovered/STONEAGE-SCENE25-ACTUAL-PIXEL-REPLAY-R1.json').read_bytes());self.assertEqual(validate_actual(a,self.base)['old_room_frames'],4)
 def test_actual_replay_cannot_claim_browser(self):
  a=json.loads((ROOT/'research/recovered/STONEAGE-SCENE25-ACTUAL-PIXEL-REPLAY-R1.json').read_bytes());a['original_source_browser_verified']=True
  with self.assertRaises(ValueError):validate_actual(a,self.base)
 def test_actual_replay_cannot_change_pixels(self):
  a=json.loads((ROOT/'research/recovered/STONEAGE-SCENE25-ACTUAL-PIXEL-REPLAY-R1.json').read_bytes());a['references']['room'][0]['RGBA_sha256']='0'*64
  with self.assertRaises(ValueError):validate_actual(a,self.base)
if __name__=='__main__':unittest.main()
