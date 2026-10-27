import copy
import hashlib
import json
import unittest
from tools.stoneage_item_shop_material_r44 import ROOT, REPORT, REPORT_SHA, replay, verify_custody

class ActualSourceContract(unittest.TestCase):
 def setUp(self):self.d=json.loads((ROOT/REPORT).read_bytes())
 def rejected(self,change):
  d=copy.deepcopy(self.d);change(d)
  with self.assertRaises(ValueError):replay(d)
 def test_exact_successful_source_and_six_occurrences(self):
  self.assertTrue(verify_custody())
  self.assertEqual(hashlib.sha256((ROOT/REPORT).read_bytes()).hexdigest(),REPORT_SHA)
  self.assertEqual(replay(self.d)['named_occurrences'],6)
  self.assertEqual(len({r['names']['name']['text_cp950_big5'] for r in self.d['material']['selected_items']}),2)
 def test_first_green_workflow_is_not_successful_material(self):
  d=json.loads((ROOT/'research/recovered/STONEAGE-PRESERVED-ITEM-SHOP-SOURCE-ATTEMPT1-R44.json').read_bytes())
  self.assertEqual(len(d['receipt']['members']),3)
  self.assertEqual(d['status'],'NOT_ACQUIRED')
  with self.assertRaises(ValueError):replay(d)
 def test_source_sha_mutation(self):
  self.rejected(lambda d:d['receipt']['members'][0].update(sha256='0'*64))
 def test_same_named_templates_not_collapsed(self):
  self.rejected(lambda d:d['material']['selected_items'].pop(0))
 def test_truncated34th_not_visible(self):
  self.rejected(lambda d:d['material']['inventory']['descendant_model_visible_occurrences'].extend(d['material']['inventory']['descendant_model_truncated_occurrences']))
 def test_source_name_trim_or_relabel_rejected(self):
  self.rejected(lambda d:d['material']['selected_items'][0]['names']['name'].update(text_cp950_big5='合成兜'))
 def test_id_namespace_mutation(self):
  self.rejected(lambda d:d['material']['selected_items'][0]['numeric_fields'].update(id=21543))
 def test_rate_changed_to_final_price_rejected(self):
  self.rejected(lambda d:d['material']['rate_fields']['buy_rate'].update(raw_decimal='0.2'))
 def test_runtime_price_inference_rejected(self):
  self.rejected(lambda d:d['material'].update(computed_runtime_prices=[1000]*6))
 def test_official_or_execution_promotion_rejected(self):
  self.rejected(lambda d:d.update(official_tw10_items_authenticated=6))
  self.rejected(lambda d:d.update(original_server_executed=True))
 def test_whole_archive_hash_claim_rejected(self):
  self.rejected(lambda d:d['receipt'].update(whole_archive_or_parts_rehashed=True))
 def test_unexpected_raw_payload_rejected(self):
  self.rejected(lambda d:d['material'].update(raw_script='synthetic forbidden payload'))

if __name__=='__main__':unittest.main()
