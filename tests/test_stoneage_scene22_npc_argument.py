import copy,json,unittest
from tools.stoneage_scene22_npc_argument import validate,REPORT,FALSE,byteshape,append_reader,private_html,source_report

class Scene22(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(REPORT.read_bytes())
 def reject(self,change):
  r=copy.deepcopy(self.report);change(r)
  with self.assertRaises(ValueError):validate(r)
 def test_archived_source(self):self.assertEqual(validate(self.report)['static_message_bytes'],143)
 def test_all_runtime_and_official_promotions_rejected(self):
  for k in FALSE:
   with self.subTest(k=k):self.reject(lambda r:r.update({k:True}))
 def test_missing_and_duplicate_input(self):
  self.reject(lambda r:r['source_inputs'].pop());self.reject(lambda r:r['source_inputs'].append(r['source_inputs'][0]))
 def test_wrong_dialogue_file(self):self.reject(lambda r:r['target'].update(exact_file_reference='npc/genout/msg_1000_63_104'))
 def test_wrong_template(self):self.reject(lambda r:r['target'].update(functionset='ItemShop'))
 def test_neighbor_coordinate(self):self.reject(lambda r:r['target'].update(xy=[63,102]))
 def test_forged_block(self):self.reject(lambda r:r['target'].update(create_block_sha256='0'*64))
 def test_forged_parent(self):self.reject(lambda r:r['custody'].update(parent_sha256='0'*64))
 def test_forged_original_file(self):self.reject(lambda r:r['message'].update(sha256='0'*64))
 def test_prose_does_not_create_branches(self):self.reject(lambda r:r['interpretation'].update(descendant_comma_split_candidate_count=4))
 def test_false_transaction_proof(self):self.reject(lambda r:r['interpretation'].update(hint_is_not_transaction_runtime_proof=False))
 def test_descendant_not_same_server(self):self.reject(lambda r:r['interpretation'].update(descendant_rule_is_same_server_certification=True))
 def test_not_all_other_messages(self):self.reject(lambda r:r['interpretation'].update(all_other_NPC_messages_exhausted=True))
 def test_no_fake_action(self):self.reject(lambda r:r.update(source_action_run_id=123))
 def test_no_completion_percentage(self):self.reject(lambda r:r.update(overall_completion_percent=100))
 def test_decode_cannot_be_asserted(self):self.reject(lambda r:r['message'].update(Big5_decode_equal=False))
 def test_single_decompressor_stated(self):self.reject(lambda r:r['custody'].update(second_decompressor_executed=True))
 def test_header_witness_not_decompressor(self):self.reject(lambda r:r['custody'].update(header_parser_is_not_second_decompressor=False))
 def test_full_header_walk_required(self):self.reject(lambda r:r['custody'].update(all_file_headers_scanned=1))
 def test_source_pins_before_parser(self):
  with self.assertRaises(ValueError):source_report(b'NPCCREATE\n',b'',b'',b'')
 def test_wrong_base_observer_not_patched(self):
  with self.assertRaises(ValueError):private_html('<html></html>',b'',b'')
 def test_unqualified_encoding_rejected(self):
  with self.assertRaises(UnicodeDecodeError):byteshape(b'\xff')
 def test_text_escaped_and_no_source_event_injection(self):
  base='<main></main><html></html>';s=append_reader(base,'<x>','</pre><script>attack()</script>')
  self.assertIn('&lt;script&gt;attack()',s);self.assertNotIn('<script>attack()',s)
 def test_original_CJK_punctuation_not_ASCII_delimiter(self):
  s=byteshape('甲，乙。\n'.encode('cp950'));self.assertEqual(s['ASCII_comma_count'],0);self.assertEqual(s['LF_count'],1)
if __name__=='__main__':unittest.main()
