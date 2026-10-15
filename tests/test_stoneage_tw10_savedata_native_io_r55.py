import copy,hashlib,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_writer_r55_model import WriterModel,ModelError,ENTRY_ESP,INPUT,OUTLEN
from tools.stoneage_tw10_savedata_writer_r55_reference import reference
from tools.stoneage_tw10_savedata_native_io_r55 import derive,validate,verify_fixtures
from tools.stoneage_tw10_savedata_transform_r53_model import NumericModel,seed_zero_fixture_inverse
P=Path(__file__).resolve().parents[1]/'research/recovered'
RAW=[(P/('STONEAGE-TW10-SAVEDATA-NATIVE-IO-'+x+'.json')).read_bytes() for x in ('R54-ORIGINAL','R51-ORIGINAL','R52-DERIVED','R53-SPEC')]
W=next(x for x in json.loads(RAW[0])['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x47010)
R=json.loads(RAW[1]);RR=R['processor_instruction_shapes'];RE=R['r50_snapshot']['processing_entry_context']['bounded_edges']
def run(data=b'\x01\x02\x03',seed=0,capacity=4000):return WriterModel(data,seed,capacity).run(W['instruction_shapes'],W['bounded_edges'])
class NumericWriterTests(unittest.TestCase):
    def test_single_byte_all_values_hand_relation(self):
        for v in range(256):self.assertEqual(run(bytes([v]))['output'],bytes([v,255]))
    def test_hand_vector(self):
        r=run(b'\x01\x02\x03');self.assertEqual(r['output'],bytes([6,4,26,8]));self.assertEqual(r['mutated_input'],bytes([254,2,252]))
    def test_high_bit_accumulation(self):self.assertEqual(run(bytes([255,128,127]))['output'],reference(bytes([255,128,127]))['output'])
    def test_wrap_key(self):self.assertEqual(run(bytes([255,1]))['output'][0],0)
    def test_key_before_not(self):self.assertEqual(run(bytes([1]))['output'][0],1)
    def test_input_mutates(self):self.assertNotEqual(run(b'abc')['mutated_input'],b'abc')
    def test_scratch_ecx_overlap(self):self.assertEqual(run(b'abc')['returned_ecx'],((sum(b'abc')&255)<<24)|0x579bdf)
    def test_zero_capacity(self):self.assertEqual(run(b'abc',capacity=0)['output'],b'')
    def test_capacity_below(self):
        r=run(b'abc',capacity=2);self.assertEqual(r['output'],b'ab');self.assertEqual(r['mutated_input'],b'abc')
    def test_capacity_equals_count(self):self.assertEqual(run(b'abc',capacity=3)['output'],b'abc')
    def test_capacity_plus_one(self):self.assertEqual(run(b'abc',capacity=4)['output'],reference(b'abc',4)['output'])
    def test_empty_fallback(self):self.assertEqual(run(b'',capacity=0)['output'],b'')
    def test_empty_division(self):self.assertRaisesRegex(ModelError,'division by zero',run,b'',capacity=1)
    def test_empty_reference_division(self):self.assertRaises(ValueError,reference,b'',1)
    def test_negative_capacity(self):self.assertRaises(ModelError,WriterModel,b'abc',capacity=-1)
    def test_large_capacity(self):self.assertRaises(ModelError,WriterModel,b'abc',capacity=4001)
    def test_bool_capacity(self):self.assertRaises(ModelError,WriterModel,b'abc',capacity=True)
    def test_over_count(self):self.assertRaises(ModelError,WriterModel,bytes(4000))
    def test_nonbytes(self):self.assertRaises(ModelError,WriterModel,bytearray(b'ab'))
    def test_bool_seed(self):self.assertRaises(ModelError,WriterModel,b'abc',seed=True)
    def test_outside_seed(self):self.assertRaises(ModelError,WriterModel,b'abc',seed=1<<31)
    def test_step_bound(self):self.assertRaisesRegex(ModelError,'step limit',WriterModel(b'abc').run,W['instruction_shapes'],W['bounded_edges'],1)
    def test_undefined_jg(self):self.assertRaises(ModelError,WriterModel(b'abc').condition,'jg')
    def test_signed_jg_boundaries(self):
        for a in (-2147483648,-1,0,1,2147483647):
            for b in (-2147483648,-1,0,1,2147483647):
                m=WriterModel(b'a');m.arithmetic_flags(a,b,a-b,32,True);self.assertEqual(m.condition('jg'),a>b)
    def test_wrong_arbitrary_key_counterexample(self):
        self.assertNotEqual(run(b'abc')['output'],seed_zero_fixture_inverse(b'abc',(sum(b'abc')+1)&255))
    def test_no_not_counterexample(self):
        data=b'abc';key=sum(data)&255;wrong=bytes([key])+bytes((v+((j+1)**2%7)*key)&255 for j,v in enumerate(data));self.assertNotEqual(run(data)['output'],wrong)
    def test_wrong_divisor_counterexample(self):
        data=b'abcdefg';key=sum(data)&255;t=reference(data)['mutated_input'];wrong=bytes([key])+bytes((v+((j+1)**2%3)*key)&255 for j,v in enumerate(t));self.assertNotEqual(run(data)['output'],wrong)
    def test_count127_roundtrip(self):
        data=bytes(range(127));w=run(data);self.assertEqual(w['output_length'],128);self.assertEqual(NumericModel(w['output']).run(RR,RE)['output'],data)
    def test_negative_seed_roundtrip(self):
        data=bytes(range(16));w=run(data,-17);self.assertEqual(NumericModel(w['output'],-17).run(RR,RE)['output'],data)
    def test_unsupported_call(self):
        rows=copy.deepcopy(W['instruction_shapes']);rows[0]['mnemonic']='call';self.assertRaises(ModelError,WriterModel(b'abc').run,rows,W['bounded_edges'])
    def test_missing_root(self):self.assertRaises(ModelError,WriterModel(b'abc').run,W['instruction_shapes'][1:],W['bounded_edges'])
    def test_range(self):self.assertRaises(ModelError,WriterModel(b'abc').memory,INPUT+4,1)
    def test_output_input_alias_rejected(self):
        m=WriterModel(b'abc');m.memory(ENTRY_ESP+16,4,INPUT);self.assertRaises(ModelError,m.run,W['instruction_shapes'],W['bounded_edges'])
    def test_length_input_alias_rejected(self):
        m=WriterModel(b'abcdef');m.memory(ENTRY_ESP+20,4,INPUT);self.assertRaises(ModelError,m.run,W['instruction_shapes'],W['bounded_edges'])
    def test_count_mismatch_rejected(self):
        m=WriterModel(b'abc');m.memory(ENTRY_ESP+8,4,4);self.assertRaises(ModelError,m.run,W['instruction_shapes'],W['bounded_edges'])
    def test_reference_reject_bool(self):self.assertRaises(ValueError,reference,b'abc',True)
    def test_missing_not_shape_counterexample(self):
        rows=copy.deepcopy(W['instruction_shapes']);r=next(r for r in rows if r['site_rva']==0x470c2);r['mnemonic']='mov';r['operands']=[r['operands'][0],copy.deepcopy(r['operands'][0])]
        actual=WriterModel(b'abc').run(rows,W['bounded_edges']);self.assertNotEqual(actual['output'],reference(b'abc')['output'])
class SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=derive(*RAW)
    def test_replay(self):self.assertTrue(validate(self.d,*RAW))
    def test_raw_tamper(self):self.assertRaises(ValueError,derive,RAW[0]+b' ',*RAW[1:])
    def test_prior_tamper(self):self.assertRaises(ValueError,derive,*RAW[:3],RAW[3]+b' ')
    def test_promote_schema(self):
        d=copy.deepcopy(self.d);d['actual_schema_checksum_migration_or_cross_version_proven']=True;self.assertRaises(ValueError,validate,d,*RAW)
    def test_bool_type(self):
        d=copy.deepcopy(self.d);d['application_candidate']['conditional_output_length']=True;self.assertRaises(ValueError,validate,d,*RAW)
    def test_missing_shape(self):
        d=copy.deepcopy(self.d);d['complete_writer_instruction_shapes'].pop();self.assertRaises(ValueError,validate,d,*RAW)
    def test_coverage_exclusions(self):self.assertEqual(self.d['invented_fixture_verification']['union_writer_covered_instruction_count'],126)
    def test_all_keys(self):self.assertTrue(self.d['invented_fixture_verification']['all_256_derived_key_values_covered'])
    def test_cache_isolation(self):
        d=copy.deepcopy(self.d);d['invented_fixture_verification']['zero_seed_writer_covered_rvas'].clear();self.assertTrue(derive(*RAW)['invented_fixture_verification']['zero_seed_writer_covered_rvas'])
if __name__=='__main__':unittest.main()
