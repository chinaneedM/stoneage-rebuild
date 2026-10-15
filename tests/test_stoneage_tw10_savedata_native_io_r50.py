"""Invented savedata call, status path, processing call and application reads."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r50 import *
from tools.stoneage_tw10_savedata_native_io_r50_guard import validate


@lru_cache(maxsize=1)
def base_fixture():
    lo,hi,base=0x40000,0x49000,0x400000;raw=bytearray(b'\xcc'*(hi-lo))
    def put(a,b):raw[a-lo:a-lo+len(b)]=b
    def jump(a,b):put(a,b'\xe9'+struct.pack('<i',b-a-5))
    def call(a,b):put(a,b'\xe8'+struct.pack('<i',b-a-5))
    put(ROOT,b'\x68'+struct.pack('<I',base+0x63634));call(OPEN_CALL,0x487ba)
    put(0x4011f,bytes.fromhex('89c6'));jump(0x40121,0x40138)
    put(0x40138,bytes.fromhex('5668a00f00008d4424146a0150'));call(READ_CALL,READ_TARGET)
    put(0x4014a,bytes.fromhex('89c78a460c83c410a820741b56'))
    put(0x40157,b'\xc6\x05'+struct.pack('<I',base+0x1721000)+b'\x03');call(0x4015e,0x4856c);jump(0x40163,0x40177)
    put(0x40171,b'\x56');call(0x40172,0x4856c)
    put(0x40177,bytes.fromhex('8d4c240c8d5424105168')+struct.pack('<I',base+0x1722000)+bytes.fromhex('6a005752'))
    call(PROCESS,PROCESS_ROOT)
    put(PROCESS+5,bytes.fromhex('8b44242083c41483f8397416b93900000083e839'));jump(0x401a2,0x401c0)
    put(0x401b0,b'\xc6\x05'+struct.pack('<I',base+0x1721000)+b'\x01');jump(0x401b7,0x401c0)
    put(0x401c0,bytes.fromhex('8b01c3'))
    put(PROCESS_ROOT,bytes.fromhex('5589e58b75088b7d148b4d0c85c9740b'));call(PROCESS_ROOT+16,0x47200)
    put(PROCESS_ROOT+21,bytes.fromhex('880783c60149c9c3'));put(0x47200,b'\xc3')
    dec=Decoder(bytes(raw),lo,base)
    sections=[{'name':'.text','rva':lo,'vsize':hi-lo,'raw':0,'raw_size':hi-lo,'characteristics':0x60000020},
              {'name':'.data','rva':0x1720000,'vsize':0x10000,'raw':hi-lo,'raw_size':0,'characteristics':0xc0000040}]
    ns,es,front,cap=candidate_graph(dec,ROOT,span=192,cap=128)
    old={'filename_push_rva':ROOT,'bounded_node_rvas':sorted(ns),'bounded_edges':[list(e) for e in sorted(es)],
         'graph':{**graph_meta(ns,es,front,cap),'span_bytes':192,'node_cap':128},
         'continuation_calls':[{'site_rva':READ_CALL,'identity':call_identity(dec,READ_CALL,{},sections),'conditional_linear_push_suffix':local_push_suffix(dec,sections,ROOT,READ_CALL)}]}
    eg={'visited':{a:1 for a in (ROOT,OPEN_CALL,READ_CALL,READ_TARGET,PROCESS,PROCESS_ROOT)},'edges':{(READ_CALL,READ_TARGET),(PROCESS,PROCESS_ROOT)},'limit_hit':False}
    prior49={'schema':'tw10-r49-original-native-edi-overwrite-temporal-wrapper-division-slots'}
    return derive(dec,sections,{},prior49,{'caller_contexts':[old]},eg)


def fixture():return copy.deepcopy(base_fixture())


class R50Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_four_read_slots_and_literal_only(self):
        s=fixture()['caller_context']['read_call_context']['physical_push_suffix'];self.assertEqual(len(s['pushes']),4);self.assertEqual(s['pushes'][2]['input']['constant'],4000);self.assertFalse(s['actual_stack_values_known'])
    def test_opaque_read_return_before_copy(self):
        qs=fixture()['caller_context']['post_read_input_sources']['queries'];q=next(q for q in qs if q['site_rva']==READ_CALL+5 and q['register']=='eax');self.assertEqual([(t['origin'],t['rva']) for t in q['reaching_candidates']],[('unknown_call',READ_CALL)])
    def test_processing_five_physical_slots(self):self.assertEqual(len(fixture()['caller_context']['processing_call_context']['physical_push_suffix']['pushes']),5)
    def test_close_call_kills_length_register(self):
        q=next(q for q in fixture()['caller_context']['processing_call_context']['input_sources']['queries'] if q['site_rva']==PROCESS and q['register']=='edi')
        self.assertTrue(all(t['origin']=='unknown_call' for t in q['reaching_candidates']))
    def test_address_spellings_not_same_stack_proof(self):
        c=fixture()['caller_context'];self.assertEqual([r['operands'][1]['geometry']['relative_field_offset'] for r in c['address_shapes']],[20,12,16])
        self.assertTrue(all(q['unique_conditional_esp_delta'] is None and q['unknown_barrier_candidates'] for q in c['address_stack_state_queries']))
    def test_literal_cleanup_retains_call_barrier(self):
        c=fixture()['caller_context'];self.assertTrue(any(e['syntax_class']=='literal_esp_adjustment' and e['esp_delta']==16 for e in c['stack_effect_candidates']))
    def test_processor_body_is_only_candidate(self):self.assertFalse(fixture()['processing_entry_context']['actual_function_abi_decoding_compression_encryption_or_output_proven'])
    def test_application_literal57_retained(self):
        rows=fixture()['caller_context']['first_output_shapes'];self.assertTrue(any(r['mnemonic']=='cmp' and r['operands'][-1].get('constant')==57 for r in rows))
    def test_extended_graph_includes_old_scope(self):
        c=fixture()['caller_context'];self.assertTrue(set(c['prior_narrow_node_rvas'])<=set(c['bounded_node_rvas']))
    def test_bad_source(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R50Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):self.reject(lambda d,f=f:d.update({f:True}))
    def test_prior_digest(self):self.reject(lambda d:d.update(r49_exact_report_sha256='bad'))
    def test_r41_digest(self):self.reject(lambda d:d.update(r41_exact_report_sha256='bad'))
    def test_read_target(self):self.reject(lambda d:d['caller_context']['read_call_context']['identity'].update(direct_target_rva=1))
    def test_processor_target(self):self.reject(lambda d:d['caller_context']['processing_call_context']['identity'].update(direct_target_rva=1))
    def test_suffix_abi(self):self.reject(lambda d:d['caller_context']['processing_call_context']['physical_push_suffix'].update(abi_roles_applied=True))
    def test_esp_preserved(self):self.reject(lambda d:d['caller_context']['address_stack_state_queries'][0].update(unique_conditional_esp_delta=0))
    def test_esp_effect(self):self.reject(lambda d:d['caller_context']['stack_effect_candidates'][0].update(esp_delta=0))
    def test_output_count(self):self.reject(lambda d:d['caller_context'].update(first_output_shape_count=999))
    def test_branch_taken(self):self.reject(lambda d:d['caller_context']['post_read_zf_branch_contexts'][0].update(actual_flag_value_feasibility_or_taken_path_proven=True))
    def test_transfer_loop(self):self.reject(lambda d:d['caller_context']['post_processing_transfers'][0].update(actual_flags_taken_path_or_loop_count_proven=True))
    def test_processor_schema(self):self.reject(lambda d:d['processing_entry_context'].update(actual_function_abi_decoding_compression_encryption_or_output_proven=True))
    def test_processor_shape_count(self):self.reject(lambda d:d['processing_entry_context'].update(memory_control_shape_count=999))
    def test_cross_surface(self):self.reject(lambda d:d['caller_context']['first_output_shapes'][0].update(mnemonic='nop'))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
