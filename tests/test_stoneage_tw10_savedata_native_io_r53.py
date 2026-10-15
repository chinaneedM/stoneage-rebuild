"""Conditional numeric model, independent formula and source corruption controls."""
import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_transform_r53_model import *
from tools.stoneage_tw10_savedata_native_io_r53 import derive,validate,FLAGS
RAW51=Path('research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ORIGINAL.json').read_bytes()
RAW52=Path('research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R52-DERIVED.json').read_bytes()
P=json.loads(RAW51);ROWS=P['processor_instruction_shapes'];EDGES=P['r50_snapshot']['processing_entry_context']['bounded_edges']
class ModelArchitecture(unittest.TestCase):
    def test_signed_byte(self):self.assertEqual([signed(127,8),signed(128,8),signed(255,8)],[127,-128,-1])
    def test_signed_division_negative_numerator(self):self.assertEqual(signed_divide(-7,3),(-2,-1))
    def test_signed_division_negative_divisor(self):self.assertEqual(signed_divide(7,-3),(-2,1))
    def test_signed_division_both_negative(self):self.assertEqual(signed_divide(-7,-3),(2,-1))
    def test_divide_zero(self):
        with self.assertRaises(ModelError):signed_divide(7,0)
    def test_divide_overflow(self):
        with self.assertRaises(ModelError):signed_divide(-(1<<31),-1)
    def test_partial_register_preserves_parent(self):
        m=NumericModel(b'\x01\x02');m.register('eax',0xabcd1234);m.register('al',128);self.assertEqual(m.register('eax'),0xabcd1280);m.register('ax',65535);self.assertEqual(m.register('eax'),0xabcdffff)
    def test_signed_compare_overflow_flag(self):
        m=NumericModel(b'\x01\x02');m.arithmetic_flags(0x80000000,1,0x7fffffff,32,True);self.assertTrue(m.condition('jl'));self.assertFalse(m.condition('jge'))
    def test_byte_subtraction_flags(self):
        m=NumericModel(b'\x01\x02');m.arithmetic_flags(1,2,-1,8,True);self.assertTrue(m.condition('jl'));self.assertFalse(m.condition('je'))
    def test_undefined_flags(self):
        with self.assertRaises(ModelError):NumericModel(b'\x01\x02').condition('je')
    def test_input_readonly(self):
        with self.assertRaises(ModelError):NumericModel(b'\x01\x02').memory(INPUT,1,0)
    def test_out_of_bounds(self):
        with self.assertRaises(ModelError):NumericModel(b'\x01\x02').memory(OUTPUT+1,1)
    def test_segment_override_rejected(self):
        with self.assertRaises(ModelError):NumericModel(b'\x01\x02').address({'geometry':{'segment_register':'fs','relative_field_offset':0}})
    def test_short_and_empty_count_rejected(self):
        for b in (b'',b'\x01'):
            with self.assertRaises(ModelError):NumericModel(b)
    def test_count_bound(self):
        with self.assertRaises(ModelError):NumericModel(bytes(4001))
    def test_input_type(self):
        with self.assertRaises(ModelError):NumericModel(bytearray([1,2]))
    def test_seed_domain(self):
        for s in (True,1<<31,-(1<<31)-1):
            with self.assertRaises(ModelError):NumericModel(b'\x01\x02',s)
class ConditionalFormula(unittest.TestCase):
    def compare(self,data):
        r=NumericModel(data).run(ROWS,EDGES);self.assertEqual(r['output'],seed_zero_reference(data));self.assertEqual(r['output_length'],len(data)-1);return r['output']
    def test_hand_worked_two_bytes(self):self.assertEqual(self.compare(bytes([2,10])),bytes([247]))
    def test_hand_worked_four_bytes(self):self.assertEqual(self.compare(bytes([1,10,20,30])),bytes([246,16,227]))
    def test_high_bit_key_255(self):self.assertEqual(self.compare(bytes([255,0,0])),bytes([254,4]))
    def test_high_bit_key_128(self):self.assertEqual(self.compare(bytes([128,0,0])),bytes([127,0]))
    def test_zero_key_only_predicate_changes(self):
        data=bytes([0,10,20,30,40,50,60]);self.assertEqual(self.compare(data),bytes([245,20,225,40,205,195]))
    def test_seed_not_generalized(self):
        with self.assertRaises(ModelError):seed_zero_reference(b'\x01\x02',1)
    def test_inverse_is_invented_generator(self):
        for key in (0,1,127,128,255):
            output=bytes((i*29+4)&255 for i in range(127));data=seed_zero_fixture_inverse(output,key);self.assertEqual(self.compare(data),output)
    def test_target_length_fixtures(self):
        for n in (57,127):
            output=bytes([4 if n==57 else 5,0])+bytes((i*17)&255 for i in range(n-2));self.assertEqual(self.compare(seed_zero_fixture_inverse(output,193)),output)
    def test_alias_outlen_input_rejected(self):
        m=NumericModel(bytes(range(8)));m.memory(ENTRY_ESP+20,4,INPUT,record=False)
        with self.assertRaises(ModelError):m.run(ROWS,EDGES)
    def test_alias_output_input_rejected(self):
        m=NumericModel(bytes(range(8)));m.memory(ENTRY_ESP+16,4,INPUT,record=False)
        with self.assertRaises(ModelError):m.run(ROWS,EDGES)
    def test_step_bound(self):
        with self.assertRaises(ModelError):NumericModel(bytes(range(8))).run(ROWS,EDGES,10)
    def test_unsupported_call_rejected(self):
        rows=copy.deepcopy(ROWS);rows[0]['mnemonic']='call'
        with self.assertRaises(ModelError):NumericModel(bytes(range(8))).run(rows,EDGES)
    def test_wrong_remainder_divisor_counterexample(self):
        rows=copy.deepcopy(ROWS);r=next(r for r in rows if r['site_rva']==0x471e5);r['operands'][1]['constant']=3;data=bytes(range(1,9));self.assertNotEqual(NumericModel(data).run(rows,EDGES)['output'],seed_zero_reference(data))
    def test_missing_not_counterexample(self):
        rows=copy.deepcopy(ROWS);next(r for r in rows if r['site_rva']==0x47258)['mnemonic']='inc';data=bytes(range(1,9));self.assertNotEqual(NumericModel(data).run(rows,EDGES)['output'],seed_zero_reference(data))
    def test_invalid_branch_edge(self):
        es=[e for e in EDGES if e!=[0x47190,0x47192]]
        with self.assertRaises(ModelError):NumericModel(bytes(range(8))).run(ROWS,es)
class PinnedSpecification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=derive(RAW51,RAW52)
    def reject(self,fn):
        p=copy.deepcopy(self.report);fn(p)
        with self.assertRaises(ValueError):validate(p,RAW51,RAW52)
    def test_exact_replay(self):self.assertTrue(validate(self.report,RAW51,RAW52))
    def test_r51_digest(self):
        with self.assertRaises(ValueError):derive(RAW51+b' ',RAW52)
    def test_r52_digest(self):
        with self.assertRaises(ValueError):derive(RAW51,RAW52+b' ')
    def test_all_key_fixtures(self):self.assertEqual(self.report['invented_fixture_verification']['invented_seed_zero_fixture_count'],1029)
    def test_conditional_coverage_exclusions(self):self.assertEqual(self.report['invented_fixture_verification']['domain_excluded_negative_index_fixup_rvas'],[0x4723a,0x4723b,0x4723e])
    def test_coverage_domain_not_fabricated(self):self.reject(lambda p:p['invented_fixture_verification'].update(domain_excluded_negative_index_fixup_rvas=[]))
    def test_no_promotion(self):
        for k in FLAGS:self.reject(lambda p,k=k:p.update({k:True}))
    def test_formula_offset_tamper(self):self.reject(lambda p:p['seed_zero_symbolic_relations'].update(source_to_output_index='i = j'))
    def test_reference_domain_tamper(self):self.reject(lambda p:p['preconditions'].update(source_destination_length_pointer_and_stack_regions_disjoint=False))
    def test_original_read_size_tamper(self):self.reject(lambda p:p['preconditions'].update(domain_4000_is_model_bound_not_actual_read_size_proof=False))
    def test_invalid_scalar_type(self):self.reject(lambda p:p.update(no_original_archive_redownload=1))
    def test_historical_inverse_tamper(self):self.reject(lambda p:p['seed_zero_symbolic_relations'].update(fixture_inverse_is_not_a_historical_savedata_write_path=False))
    def test_model_cache_isolation(self):
        p=derive(RAW51,RAW52);p['invented_fixture_verification']['all_256_key_values_lengths'].append(99);self.assertEqual(derive(RAW51,RAW52)['invented_fixture_verification']['all_256_key_values_lengths'],[2,3,4,8])
if __name__=='__main__':unittest.main()
