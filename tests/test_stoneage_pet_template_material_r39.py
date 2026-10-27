import copy
import json
import unittest
from tools.stoneage_pet_template_material_r39 import SOURCE,validate

class ArchivedTemplateTests(unittest.TestCase):
 def setUp(self):self.report=json.loads(SOURCE.read_text())
 def test_actual_source_seven_occurrences_and_four_same_name_variants(self):
  material=validate(self.report)
  self.assertEqual([(r['template_number_column_7'],r['graphic_field_column_37'],r['pet_flag_column_38']) for r in material['selected_rows']],
   [(1,100250,1),(2,100251,1),(3,100252,1),(6,100252,1),(586,100252,1),(678,100252,0),(1061,100251,1)])
  self.assertEqual(len([r for r in material['selected_rows'] if r['name']=='烏力斯坦']),4)
 def test_no_false_official_or_runtime_promotion(self):
  paths=[('original_payload_published',),('original_program_executed',),('new_official_clients',),
   *[('material',k) for k in ('same_client_server_build_proven','client_sprite_binding_proven','official_species_master_authenticated','original_server_executed')]]
  for keys in paths:
   bad=copy.deepcopy(self.report);node=bad
   for k in keys[:-1]:node=node[k]
   node[keys[-1]]=True
   with self.assertRaises(ValueError,msg=str(keys)):validate(bad)
 def test_missing_position_wrong_source_name_and_budget_rejected(self):
  mutations=[lambda r:r['material']['selected_rows'].append(r['material']['selected_rows'][0]),
   lambda r:r['receipt']['members'][0].update(sha256='0'*64),
   lambda r:r['material']['selected_rows'][0].update(name='其他'),
   lambda r:r['receipt'].update(actual_range_bytes=20*1024*1024),
   lambda r:r['material'].update(distinct_name_tokens=988),
   lambda r:r['material'].update(unmatched_name_queries=['烏力'])]
  for mutate in mutations:
   bad=copy.deepcopy(self.report);mutate(bad)
   with self.assertRaises(ValueError):validate(bad)
if __name__=='__main__':unittest.main()
