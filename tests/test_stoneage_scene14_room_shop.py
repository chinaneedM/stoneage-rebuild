import copy,json,unittest
from pathlib import Path
from tools.stoneage_scene14_room_shop import REPORT,validate,blocks,FALSE,derive,MEMBERS,sha,validate_acceptance
from unittest.mock import patch

class RoomShopSources(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_bytes())
    def reject(self,mutate):
        r=copy.deepcopy(self.r);mutate(r)
        with self.assertRaises(ValueError):validate(r)
    def test_real_source_chain(self):self.assertEqual(validate(self.r)['listed_item_ids'],17)
    def test_id_zero_is_preserved(self):self.reject(lambda r:r['listed_item_ids'].pop(0))
    def test_stock_order_preserved(self):self.reject(lambda r:r['listed_item_ids'].reverse())
    def test_filename_cannot_replace_authored_coordinate(self):self.reject(lambda r:r['npc'].update(borncorner=[17,15,17,15]))
    def test_other_shop_parameter_rejected(self):self.reject(lambda r:r['npc'].update(argument_file='genout/ss_1001_17_15'))
    def test_wrong_template_rejected(self):self.reject(lambda r:r['npc'].update(functionset='Healer'))
    def test_source_graphic_not_physical_bitmap(self):self.reject(lambda r:r['candidate_graphic'].update(bitmapno=16017))
    def test_duplicate_alias_not_silently_selected(self):self.reject(lambda r:r['candidate_graphic'].update(binding='LAST_WINS'))
    def test_source_cost_is_not_actual_sale_price(self):self.reject(lambda r:r.update(computed_runtime_prices=[65,105,260]))
    def test_map_third_plane_not_assumed_walkability(self):self.reject(lambda r:r['map'].update(third_plane_semantics='BLOCKED'))
    def test_same_size_changed_source_rejected(self):self.reject(lambda r:r['source_members']['npc/genout/shop_m.create'].update(sha256='0'*64))
    def test_selected_original_row_not_interchangeable(self):self.reject(lambda r:r['selected_items'][1].update(physical_line=1))
    def test_genuine_source_rate_rejected_if_changed(self):self.reject(lambda r:r['rates_raw'].update(special_rate='1.0'))
    def test_whole_original_world_not_restored(self):
        for key in FALSE:
            with self.subTest(key=key):self.reject(lambda r:r.update({key:True}))
    def test_no_guessed_completion(self):self.reject(lambda r:r.update(overall_completion_percent=50))
    def test_raw_dialogue_not_public(self):self.reject(lambda r:r.update(original_welcome_or_dialogue_published=True))
    def test_parser_retains_source_order_and_byte_span(self):
        b=b'NPCCREATE\n# note\n{\nfloorid=1001\nborncorner=17,13,17,13\n}\n'
        z=blocks(b,b'NPCCREATE')[0];self.assertEqual(b[z['byte_start']:z['byte_end']],b'{\nfloorid=1001\nborncorner=17,13,17,13\n}');self.assertEqual(list(z['fields']),['floorid','borncorner'])
    def test_duplicate_config_keys_refused(self):
        with self.assertRaises(ValueError):blocks(b'NPCCREATE\n{\na=1\na=2\n}\n',b'NPCCREATE')
    def test_truncated_block_after_valid_block_refused(self):
        with self.assertRaises(ValueError):blocks(b'NPCCREATE\n{\na=1\n}\n{\na=2\n',b'NPCCREATE')
    def test_wrong_config_magic_refused(self):
        with self.assertRaises(ValueError):blocks(b'NPCTEMPLATE\n{\na=1\n}\n',b'NPCCREATE')
    def test_local_source_and_browser_acceptance(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes());self.assertEqual(validate_acceptance(a,self.r)['exact_integer_scale_full_canvas_matches'],4)
    def test_fractional_pixel_success_not_invented(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes());a['independent_replay']['fractional_scale_full_pixel_match']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_browser_missing_source_inspection_refused(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes());a['source_inspector_opened_by_button_and_image_click']=False
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_changed_canvas_hash_refused(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes());a['browser_states'][0]['canvas_sha256']='0'*64
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_viewer_has_no_purchase_path(self):
        s=Path('tools/scene-room-shop-viewer-r14.html').read_text();self.assertIn("connect-src 'none'",s);self.assertNotIn('fetch(',s);self.assertIn('没有计算实际买卖价',s)
if __name__=='__main__':unittest.main()
