import copy
import hashlib
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_application_r50 import derive,validate

class ConsumerInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=Path('research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R50-ORIGINAL.json').read_bytes()
        cls.contract=derive(cls.raw)
    def changed(self,mutate):
        d=json.loads(self.raw);mutate(d);raw=json.dumps(d).encode()
        return raw,hashlib.sha256(raw).hexdigest()
    def test_pinned_source(self):self.assertTrue(validate(self.contract,self.raw))
    def test_digest(self):
        with self.assertRaises(ValueError):derive(self.raw+b' ')
    def test_size(self):
        with self.assertRaises(ValueError):derive(b' '*500001)
    def test_schema(self):
        raw,sha=self.changed(lambda d:d.update(schema='other'))
        with self.assertRaises(ValueError):derive(raw,sha)
    def test_source_promotion(self):
        raw,sha=self.changed(lambda d:d.update(actual_savedata_record_field_framing_schema_or_checksum_proven=True))
        with self.assertRaises(ValueError):derive(raw,sha)
    def test_missing_inventory(self):
        raw,sha=self.changed(lambda d:d['caller_context']['literal_effect_input_shapes'].pop())
        with self.assertRaises(ValueError):derive(raw,sha)
    def test_duplicate_inventory(self):
        raw,sha=self.changed(lambda d:d['caller_context']['literal_effect_input_shapes'].append(d['caller_context']['literal_effect_input_shapes'][-1]))
        with self.assertRaises(ValueError):derive(raw,sha)
    def test_compare_literals(self):
        values=[o['constant'] for r in self.contract['post_processing_comparisons'] for o in r['operands'] if o['kind']=='immediate']
        self.assertEqual(values,[57,127])
    def test_widths_remain_distinct(self):
        rows=[m for m in self.contract['post_processing_memory_operands'] if (m['operand']['geometry']['displacement_region'] or {}).get('displacement_rva')==20954540]
        self.assertEqual([r['operand']['width_bytes'] for r in rows],[2,1,2])
    def test_processor_truncation(self):
        self.assertEqual(self.contract['processor_memory_control_sample'],{'total':36,'retained':32,'truncated':True})
    def test_stack_unknowns(self):
        self.assertTrue(all(r['unique_conditional_esp_delta'] is None and r['actual_original_esp_or_stack_contents_known'] is False for r in self.contract['caller_address_stack_unknowns']))
    def test_five_physical_slots(self):
        self.assertEqual([p['conditional_pre_call_esp_offset'] for p in self.contract['processing_physical_suffix']['pushes']],[0,4,8,12,16])
    def test_false_schema(self):
        c=copy.deepcopy(self.contract);c['actual_schema_length_tag_migration_or_buffer_alias_proven']=True
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_width_tamper(self):
        c=copy.deepcopy(self.contract);c['post_processing_memory_operands'][0]['operand']['width_bytes']=1
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_cap_tamper(self):
        c=copy.deepcopy(self.contract);c['processor_memory_control_sample']['truncated']=False
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_boolean_integer_confusion(self):
        c=copy.deepcopy(self.contract);c['static_only']=1
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_compare_constant_tamper(self):
        c=copy.deepcopy(self.contract);c['post_processing_comparisons'][0]['operands'][1]['constant']=128
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_store_offset_tamper(self):
        c=copy.deepcopy(self.contract)
        row=next(m for m in c['post_processing_memory_operands'] if (m['operand']['geometry']['displacement_region'] or {}).get('displacement_rva')==20954597)
        row['operand']['geometry']['displacement_region']['displacement_rva']=20954540
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_extra_inferred_meaning(self):
        c=copy.deepcopy(self.contract);c['version']=5
        with self.assertRaises(ValueError):validate(c,self.raw)

if __name__=='__main__':unittest.main()
