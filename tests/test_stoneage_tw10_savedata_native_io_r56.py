import copy,hashlib,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_frame_r56_model import helper,caller,Machine,Storage,ModelError,S,MARKER
from tools.stoneage_tw10_savedata_native_io_r56 import derive,validate,conditions
from tools.stoneage_tw10_savedata_writer_r55_reference import reference
P=Path(__file__).resolve().parents[1]/'research/recovered'
A=(P/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R54-ORIGINAL.json').read_bytes();B=(P/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R55-SPEC.json').read_bytes();D=json.loads(A);C=D['writer_context'];H=next(x for x in D['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x49160);W=next(x for x in D['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x47010)
def hp(n,**kw):return helper(H['instruction_shapes'],H['bounded_edges'],n,**kw)
def cp(**kw):return caller(C,H,W,bytes(range(127)),**kw)
class HelperTests(unittest.TestCase):
    def test_zero(self):self.assertEqual(hp(0)['caller_esp'],S)
    def test_one(self):self.assertEqual(hp(1)['caller_esp'],S-1)
    def test_page_minus_one(self):self.assertEqual([a-S for a in hp(4095)['probe_addresses']],[-4095])
    def test_exact_page_duplicate(self):self.assertEqual([a-S for a in hp(4096)['probe_addresses']],[-4096,-4096])
    def test_4132(self):
        r=hp(4132);self.assertEqual(r['caller_esp'],S-4132);self.assertEqual([a-S for a in r['probe_addresses']],[-4096,-4132])
    def test_multi_page(self):self.assertEqual(hp(65536)['caller_esp'],S-65536)
    def test_marker(self):self.assertEqual(hp(4132,marker=0xabcdef12)['returned_marker'],0xabcdef12)
    def test_ecx(self):self.assertEqual(hp(4132,ecx=0xffffffff)['regs']['ecx'],0xffffffff)
    def test_negative(self):self.assertRaises(ModelError,hp,-1)
    def test_too_large(self):self.assertRaises(ModelError,hp,65537)
    def test_bool(self):self.assertRaises(ModelError,hp,True)
    def test_step_limit(self):self.assertRaises(ModelError,hp,4132,max_steps=1)
    def test_probe_failure(self):
        class Fail(Storage):
            def get(self,a,w):
                if a==S-4096:raise ModelError('invented failed probe')
                return super().get(a,w)
        self.assertRaisesRegex(ModelError,'failed probe',hp,4132,mem=Fail())
    def test_wrong_return_load(self):
        rs=copy.deepcopy(H['instruction_shapes']);r=next(r for r in rs if r['site_rva']==0x4918a);r['operands'][1]['geometry']['relative_field_offset']=0
        self.assertRaises(ModelError,helper,rs,H['bounded_edges'],4132)
    def test_unsupported_helper_call(self):
        rs=copy.deepcopy(H['instruction_shapes']);rs[0]['mnemonic']='call';self.assertRaises(ModelError,helper,rs,H['bounded_edges'],4132)
    def test_no_native_memory(self):self.assertRaises(ModelError,Storage().get,0x1234,4)
class CallerTests(unittest.TestCase):
    def test_request(self):self.assertEqual(cp()['request_slots'],[S-4000,1,128,0x11111111])
    def test_contents(self):self.assertEqual(cp()['request_bytes'],reference(bytes(range(127)))['output'])
    def test_open_zero(self):
        r=cp(open_return=0);self.assertEqual(r['return_value'],0);self.assertIsNone(r['request_slots']);self.assertNotIn(0x400ac,r['calls'])
    def test_short_write(self):
        r=cp(write_return=127);self.assertEqual(r['return_value'],0);self.assertFalse(r['close_stub_seen'])
    def test_complete(self):self.assertEqual(cp(write_return=128)['return_value'],1)
    def test_larger(self):self.assertTrue(cp(write_return=129)['close_stub_seen'])
    def test_unsigned_high_bit(self):self.assertEqual(cp(write_return=0xffffffff)['return_value'],1)
    def test_close_return_ignored(self):self.assertEqual(cp(close_return=0xffffffff)['return_value'],1)
    def test_length_clobber(self):self.assertEqual(cp(length_clobber=127)['request_slots'][2],127)
    def test_output_clobber(self):self.assertNotEqual(cp(output_clobber=True)['request_bytes'],cp()['request_bytes'])
    def test_unknown_direction(self):self.assertRaises(ModelError,cp,direction=None)
    def test_backward_direction(self):self.assertRaises(ModelError,cp,direction=1)
    def test_unknown_segment(self):self.assertRaises(ModelError,cp,flat_segments=None)
    def test_bool_return(self):self.assertRaises(ModelError,cp,write_return=True)
    def test_input_count(self):self.assertRaises(ModelError,caller,C,H,W,bytes(128))
    def test_caller_step_limit(self):self.assertRaises(ModelError,cp,max_steps=1)
    def test_conditional_offsets(self):
        r=cp()['entry_relative_stack_before_sites'];self.assertEqual([r[a] for a in (0x4005a,0x40069,0x40080,0x40090,0x40095)],[-4164,-4172,-4140,-4156,-4156])
class ContractTests(unittest.TestCase):
    def test_unknown(self):self.assertIsNone(conditions()['conditional_write_request_count'])
    def test_qualified(self):self.assertEqual(conditions(True,0,True,True,True)['conditional_write_request_count'],128)
    def test_unknown_memory(self):
        r=conditions(True,0,True,True,None);self.assertTrue(r['post_open_geometry_qualified']);self.assertFalse(r['output_content_and_count_binding_qualified'])
    def test_unknown_stack(self):
        r=conditions(True,0,True,None,True);self.assertTrue(r['prefix_frame_geometry_qualified']);self.assertFalse(r['post_open_geometry_qualified'])
    def test_bool_direction(self):self.assertFalse(conditions(True,False,True,True,True)['snapshot_copy_qualified'])
class SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=derive(A,B)
    def test_replay(self):self.assertTrue(validate(self.d,A,B))
    def test_raw_custody(self):self.assertRaises(ValueError,derive,A+b' ',B)
    def test_prior_custody(self):self.assertRaises(ValueError,derive,A,B+b' ')
    def test_promotion(self):
        d=copy.deepcopy(self.d);d['actual_native_write_flush_close_or_persistence_proven']=True;self.assertRaises(ValueError,validate,d,A,B)
    def test_missing_shape(self):
        d=copy.deepcopy(self.d);d['complete_helper_instruction_shapes'].pop();self.assertRaises(ValueError,validate,d,A,B)
    def test_type_confusion(self):
        d=copy.deepcopy(self.d);d['binding_under_explicit_model_conditions']['conditional_write_request_count']=True;self.assertRaises(ValueError,validate,d,A,B)
    def test_coverage(self):
        v=self.d['invented_verification'];self.assertEqual(len(v['helper_covered_rvas']),17);self.assertEqual(len(v['caller_covered_rvas']),55)
    def test_cache_isolation(self):
        d=copy.deepcopy(self.d);d['invented_verification']['helper_covered_rvas'].clear();self.assertEqual(len(derive(A,B)['invented_verification']['helper_covered_rvas']),17)
if __name__=='__main__':unittest.main()
