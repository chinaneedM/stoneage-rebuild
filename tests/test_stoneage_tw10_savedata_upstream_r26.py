"""Invented R26 x86 and arithmetic controls; no original state evaluation."""
import copy,struct,unittest
from tools.stoneage_tw10_savedata_upstream_r26 import *
from tools.stoneage_tw10_savedata_upstream_r26_guard import validate
BASE=0x400000

def fixture():
    lo=BINDINGS[0][0];hi=0x4a0c8;raw=bytearray(b'\x90'*(hi-lo))
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    for site,root in BINDINGS:put(site,b'\xe8'+struct.pack('<i',root-site-5))
    put(CREATE_ROOT,bytes.fromhex('31c039c8'))
    put(SETE,bytes.fromhex('0f94c050ffd0c3'))
    put(REALLOC_ROOT,b'\xb8'+struct.pack('<I',0))
    put(0x4a0a1,b'\xb9'+struct.pack('<I',1))
    put(COMPARE,bytes.fromhex('39c8'))
    put(LEA,bytes.fromhex('8d448950'))
    put(SHIFT,bytes.fromhex('c1e00250'))
    put(0x4a0c4,bytes.fromhex('ffd0c3'))
    dec=Decoder(bytes(raw),lo,BASE)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r25_exact_original_revalidated=True,r25_exact_report_sha256=PRIOR_SHA256,static_only=True,
                caller_bindings=[dict(call_rva=site,target_candidate_rva=root,identity=call_identity(dec,site,{},[]),supported_by_r25_original_scan=True,runtime_entry_or_call_effect_admitted=False) for site,root in BINDINGS],
                create_context=create_context(dec,[]),realloc_context=realloc_context(dec,[]),**{k:False for k in FLAGS})

class R26Synthetic(unittest.TestCase):
    def test_partial_mask_preserves_upper_bits(self):
        self.assertEqual(eval_sete_model(0xdeadbeef,False),0xdeadbe00)
        self.assertEqual(eval_sete_model(0xdeadbeef,True),0xdeadbe01)
    def test_zero_input_choices(self):
        self.assertEqual([eval_sete_model(0,z) for z in (False,True)],[0,1])
    def test_arithmetic_wrap(self):self.assertEqual(eval_sete_model(0x1ffffffff,True),0xffffff01)
    def test_unknown_input_has_no_finite_full_eax_claim(self):
        s=fixture()['create_context']['eax_before_sete'];s['reaching_candidates']=[{'origin':'entry','rva':CREATE_ROOT,'semantic':None}]
        self.assertIsNone(conditional_sete_model(s)['conditional_possible_values'])
    def test_join_blocks_unique_zero_claim(self):
        s=fixture()['create_context']['eax_before_sete'];s['reaching_candidates']*=2
        self.assertFalse(conditional_sete_model(s)['pre_eax_unique_zero_candidate'])
    def test_zero_partial_width_does_not_qualify_full_eax(self):
        s=fixture()['create_context']['eax_before_sete'];s['reaching_candidates'][0]['semantic']['width_bits']=8
        self.assertIsNone(conditional_sete_model(s)['conditional_possible_values'])
    def test_affine_composition(self):
        m=fixture()['realloc_context']['conditional_affine_model']
        self.assertEqual((m['multiplier'],m['bias'],m['shift_count']),(20,320,2))
        self.assertEqual((m['multiplier']*0xffffffff+m['bias'])%m['modulus'],300)
        self.assertIsNone(m['evaluated_original_result'])
    def test_affine_join_unqualified(self):
        r=fixture()['realloc_context'];source=r['inputs'][3]['candidate_source'];source['reaching_candidates']*=2
        m=affine_model(r['lea_shape'],r['shift_shape'],source)
        self.assertEqual(m['kind'],'unqualified_composition');self.assertIsNone(m['multiplier'])
    def test_affine_wrong_register_not_expression(self):
        r=fixture()['realloc_context'];r['lea_shape']['operands'][1]['geometry']['base_register']='edx'
        self.assertEqual(affine_model(r['lea_shape'],r['shift_shape'],r['inputs'][3]['candidate_source'])['kind'],'unqualified_composition')
    def test_create_root_must_reach_partial_write(self):
        with self.assertRaises(ValueError):create_context(Decoder(bytes.fromhex('c30f94c050'),CREATE_ROOT,BASE),[],root=CREATE_ROOT,site=CREATE_ROOT+1,push=CREATE_ROOT+4)
    def test_valid_invented_fixture(self):self.assertTrue(validate(fixture()))
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R26Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_runtime_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_hash(self):self.reject(lambda d:d.update(runtime_sha256='wrong'))
    def test_prior(self):self.reject(lambda d:d.update(r25_exact_report_sha256='wrong'))
    def test_call_target(self):self.reject(lambda d:d['caller_bindings'][0]['identity'].update(direct_target_rva=0x499c0))
    def test_caller_effect(self):self.reject(lambda d:d['caller_bindings'][1].update(runtime_entry_or_call_effect_admitted=True))
    def test_graph_entry(self):self.reject(lambda d:d['create_context']['graph'].update(entry_or_executed_path_proven=True))
    def test_sete_mask(self):self.reject(lambda d:d['create_context']['conditional_model'].update(preserved_mask=0))
    def test_sete_runtime_result(self):self.reject(lambda d:d['create_context']['conditional_model'].update(whole_runtime_value_known=True))
    def test_sete_finite_values_tamper(self):self.reject(lambda d:d['create_context']['conditional_model'].update(conditional_possible_values=[2,3]))
    def test_actual_flag(self):self.reject(lambda d:d['create_context'].update(actual_flag_value_known=True))
    def test_affine_multiplier(self):self.reject(lambda d:d['realloc_context']['conditional_affine_model'].update(multiplier=128))
    def test_affine_bias(self):self.reject(lambda d:d['realloc_context']['conditional_affine_model'].update(bias=128))
    def test_affine_runtime_evaluation(self):self.reject(lambda d:d['realloc_context']['conditional_affine_model'].update(evaluated_original_result=128))
    def test_affine_abi_size(self):self.reject(lambda d:d['realloc_context']['conditional_affine_model'].update(allocation_size_or_abi_role_proven=True))
    def test_input_actual_value(self):self.reject(lambda d:d['realloc_context']['inputs'][0].update(actual_value_known=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
