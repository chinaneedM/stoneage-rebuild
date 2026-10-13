"""Invented API capture/helper stores, not original handle/runtime proof."""
import struct,unittest
from tools.stoneage_tw10_savedata_native_io_r31 import *
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate
BASE=0x400000

def fixture():
    lo=PARENT_CALLER;hi=CALL+16;raw=bytearray(b'\x90'*(hi-lo))
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    put(PARENT_CALLER,b'\xe8'+struct.pack('<i',PARENT-PARENT_CALLER-5))
    put(PARENT,b'\xe9'+struct.pack('<i',API-PARENT-5))
    put(API,b'\xff\x15'+struct.pack('<I',BASE+0x520a0));put(POST,bytes.fromhex('89c7'))
    put(CALL-2,bytes.fromhex('5753'));put(CALL,b'\xe8'+struct.pack('<i',HELPER-CALL-5));put(CALL+5,b'\xc3')
    put(HELPER,bytes.fromhex('8b4424048b5424088910c3'))
    dec=Decoder(bytes(raw),lo,BASE)
    secs=[dict(name='.idata',rva=0x52000,vsize=4096,raw_size=4096,raw=0,characteristics=0x40000040)]
    imports={BASE+0x520a0:('KERNEL32.dll','CreateFileA')}
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r30_exact_original_revalidated=True,r30_exact_report_sha256=PRIOR_SHA256,static_only=True,
                caller_capture=caller_surface(dec,secs,imports),helper_memory=helper_surface(dec,secs),**{k:False for k in FLAGS})

class R31Synthetic(unittest.TestCase):
    def test_valid_fixture(self):self.assertTrue(validate(fixture()))
    def test_opaque_api_copy(self):
        c=fixture()['caller_capture']['register_copy_candidates'][0]
        self.assertEqual((c['destination']['register'],c['source']['register']),('edi','eax'))
        self.assertTrue(c['opaque_api_token_input_candidate']);self.assertFalse(c['actual_api_return_or_handle_value_proven'])
    def test_push_geometry_only(self):
        ps=fixture()['caller_capture']['push_candidates'];self.assertEqual([p['conditional_pre_call_esp_offset'] for p in ps],[0,4])
        self.assertTrue(all(not p['actual_value_or_api_parameter_role_proven'] for p in ps))
    def test_helper_store_scope(self):
        h=fixture()['helper_memory'];self.assertEqual(h['store_count'],1)
        self.assertFalse(h['store_candidates'][0]['caller_value_or_api_handle_binding_proven'])
    def test_stack_load_candidates_not_binding(self):
        h=fixture()['helper_memory'];self.assertEqual(h['stack_reference_count'],2)
        self.assertEqual([r['operand']['geometry']['relative_field_offset'] for r in h['stack_reference_candidates']],[4,8])
    def test_unknown_call_at_other_site_not_api_capture(self):
        q=dict(site_in_candidate_graph=True,candidates_truncated=False,reaching_candidates=[dict(origin='unknown_call',rva=CALL,semantic=None)])
        self.assertFalse(opaque_api_source(q))
    def test_join_not_unique_api_capture(self):
        q=dict(site_in_candidate_graph=True,candidates_truncated=False,reaching_candidates=[dict(origin='unknown_call',rva=API,semantic=None)]*2)
        self.assertFalse(opaque_api_source(q))
    def test_truncated_not_api_capture(self):
        q=dict(site_in_candidate_graph=True,candidates_truncated=True,reaching_candidates=[dict(origin='unknown_call',rva=API,semantic=None)])
        self.assertFalse(opaque_api_source(q))
    def test_unknown_semantic_only(self):
        q=dict(site_in_candidate_graph=True,candidates_truncated=False,reaching_candidates=[dict(origin='unknown_call',rva=API,semantic={})])
        self.assertFalse(opaque_api_source(q))
    def test_unreachable_not_capture(self):
        q=dict(site_in_candidate_graph=False,candidates_truncated=False,reaching_candidates=[dict(origin='unknown_call',rva=API,semantic=None)])
        self.assertFalse(opaque_api_source(q))
    def test_ret_blocks_helper_later_store(self):
        h=helper_surface(Decoder(bytes.fromhex('c38910c3'),HELPER,BASE),[])
        self.assertEqual(h['store_count'],0);self.assertFalse(h['all_alias_writes_or_actual_call_effect_proven'])
    def test_implicit_push_not_explicit_store_proof(self):
        h=helper_surface(Decoder(bytes.fromhex('50c3'),HELPER,BASE),[])
        self.assertEqual(h['store_count'],0)
    def test_segmented_store_excluded(self):
        h=helper_surface(Decoder(bytes.fromhex('648910c3'),HELPER,BASE),[])
        self.assertEqual(h['store_count'],0)
    def test_helper_store_cap(self):
        h=helper_surface(Decoder(bytes.fromhex('8910')*20+b'\xc3',HELPER,BASE),[])
        self.assertEqual(h['store_count'],20);self.assertEqual(len(h['store_candidates']),12);self.assertTrue(h['stores_truncated'])
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R31Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_prior(self):self.reject(lambda d:d.update(r30_exact_report_sha256='wrong'))
    def test_parent_call(self):self.reject(lambda d:d['caller_capture']['supporting_parent_call'].update(direct_target_rva=0))
    def test_api_name(self):self.reject(lambda d:d['caller_capture']['api_identity']['import_identity'].update(name='ReadFile'))
    def test_helper_target(self):self.reject(lambda d:d['caller_capture']['helper_call_identity'].update(direct_target_rva=0))
    def test_copy_token(self):self.reject(lambda d:d['caller_capture']['register_copy_candidates'][0].update(opaque_api_token_input_candidate=False))
    def test_copy_return(self):self.reject(lambda d:d['caller_capture']['register_copy_candidates'][0].update(actual_api_return_or_handle_value_proven=True))
    def test_copy_width(self):self.reject(lambda d:d['caller_capture']['register_copy_candidates'][0]['source'].update(width_bytes=1))
    def test_stack_offset(self):self.reject(lambda d:d['caller_capture']['push_candidates'][0].update(conditional_pre_call_esp_offset=4))
    def test_stack_abi(self):self.reject(lambda d:d['caller_capture']['local_push_suffix'].update(abi_roles_applied=True))
    def test_call_frame_binding(self):self.reject(lambda d:d['caller_capture'].update(callee_entry_or_stack_binding_proven=True))
    def test_helper_parameter_binding(self):self.reject(lambda d:d['helper_memory']['stack_reference_candidates'][0].update(actual_frame_owner_or_parameter_binding_proven=True))
    def test_store_execution(self):self.reject(lambda d:d['helper_memory']['store_candidates'][0]['write'].update(executed_write_proven=True))
    def test_store_caller_binding(self):self.reject(lambda d:d['helper_memory']['store_candidates'][0].update(caller_value_or_api_handle_binding_proven=True))
    def test_source_value(self):self.reject(lambda d:d['helper_memory']['inputs']['queries'][0].update(actual_register_value_known=True))
    def test_alias_completeness(self):self.reject(lambda d:d['helper_memory'].update(all_alias_writes_or_actual_call_effect_proven=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
