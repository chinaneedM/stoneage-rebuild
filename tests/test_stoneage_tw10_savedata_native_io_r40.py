"""Invented framed callee, source gaps and address spellings; no retail bytes."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r40 import *
from tools.stoneage_tw10_savedata_native_io_r40_guard import validate
from tests import test_stoneage_tw10_savedata_native_io_r39 as r39

@lru_cache(maxsize=1)
def base_fixture():
    captured={}
    def capture(dec,sections,imports,previous):
        lo=READ_ROOT
        raw=bytearray(b'\xcc'*(dec.lo-lo)+dec.raw)
        def put(at,code):raw[at-lo:at-lo+len(code)]=code
        def jump(at,target):put(at,b'\xe9'+struct.pack('<i',target-at-5))
        def pad(start,end):
            n=end-start;put(start,bytes.fromhex('0f1f840000000000')*(n//8)+b'\x90'*(n%8))
        put(READ_ROOT,bytes.fromhex('5589e583ec105356578b45088b750c8b4d1083f901'))
        jump(READ_ROOT+21,APIS[0][1])
        put(APIS[0][1],bytes.fromhex('6a008d45fc506a018b4d0c518b450850'))
        pad(APIS[0][1]+16,APIS[0][0])
        put(APIS[0][0],b'\xff\x15'+struct.pack('<I',dec.base+0x520d8))
        jump(APIS[0][0]+6,APIS[1][1])
        put(APIS[1][1],bytes.fromhex('6a008d45fc506a018b4d0c518b450850'))
        pad(APIS[1][1]+16,APIS[1][0])
        put(APIS[1][0],b'\xff\x15'+struct.pack('<I',dec.base+0x520d8)+b'\xc3')
        # Invented postcall comparison/branch uses an equal address spelling.
        put(READ_CALL+5,bytes.fromhex('85c07409807dff1a7503c39090c3'))
        dec=Decoder(bytes(raw),lo,dec.base);imports=dict(imports)
        imports[dec.base+0x520d8]=('KERNEL32.dll','ReadFile')
        prior=derive_r39(dec,sections,imports,previous)
        captured['report']=derive(dec,sections,imports,prior)
        return prior
    r39.base_fixture.cache_clear()
    try:
        with patch.object(r39,'derive',capture):r39.fixture()
    finally:r39.base_fixture.cache_clear()
    return captured['report']

def fixture():return copy.deepcopy(base_fixture())

def bridge(d,index=0):
    c=d['native_read_context']
    return frame_bridge(c['early_frame_read_shapes'][index],c['frame_input_sources'],c['frame_definition_shapes'],
                        c['frame_definition_esp_summaries'],c['prior_caller_pushes'])

class R40Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_three_slots(self):
        bs=fixture()['native_read_context']['conditional_frame_slot_bridges']
        self.assertEqual([b['caller_pre_call_esp_relative_offset'] for b in bs[:3]],[0,4,8])
        self.assertTrue(all(b['conditional_whole_slot_geometry_candidate'] for b in bs))
        self.assertFalse(any(b['actual_argument_contents_abi_alias_or_owner_binding_proven'] for b in bs))
    def test_saved_frame_delta(self):
        c=fixture()['native_read_context'];self.assertEqual(c['frame_definition_esp_summaries'][0]['unique_conditional_esp_delta'],-4)
    def test_call_kills_frame_source(self):
        d=fixture();c=d['native_read_context'];q=next(q for q in c['frame_input_sources']['queries'] if q['site_rva']==c['early_frame_read_shapes'][0]['site_rva'] and q['register']=='ebp')
        q['reaching_candidates']=[{'origin':'unknown_call','rva':READ_ROOT,'semantic':None}]
        self.assertFalse(bridge(d)['unique_frame_geometry_qualified'])
    def test_ambiguous_frame_sources(self):
        d=fixture();c=d['native_read_context'];q=next(q for q in c['frame_input_sources']['queries'] if q['site_rva']==c['early_frame_read_shapes'][0]['site_rva'] and q['register']=='ebp')
        q['reaching_candidates'].append({'origin':'entry','rva':READ_ROOT,'semantic':None})
        self.assertFalse(bridge(d)['conditional_whole_slot_geometry_candidate'])
    def test_unknown_esp_before_establishment(self):
        d=fixture();d['native_read_context']['frame_definition_esp_summaries'][0]['unique_conditional_esp_delta']=None
        self.assertFalse(bridge(d)['unique_frame_geometry_qualified'])
    def test_partial_slot_is_not_argument(self):
        d=fixture();d['native_read_context']['early_frame_read_shapes'][0]['operands'][1]['width_bytes']=1
        self.assertFalse(bridge(d)['conditional_whole_slot_geometry_candidate'])
    def test_index_or_segment_blocks_slot(self):
        for key,val in [('index_register','eax'),('segment_register','fs')]:
            d=fixture();d['native_read_context']['early_frame_read_shapes'][0]['operands'][1]['geometry'][key]=val
            self.assertFalse(bridge(d)['unique_frame_geometry_qualified'])
    def test_input_cap_blocks_frame_qualification(self):
        d=fixture();d['native_read_context']['frame_input_sources']['query_limit_hit']=True
        self.assertFalse(bridge(d)['unique_frame_geometry_qualified'])
    def test_address_spelling_does_not_prove_preservation(self):
        ps=fixture()['postcall_context']['buffer_address_spelling_pairs']
        self.assertTrue(ps[0]['same_address_spelling_candidate'])
        self.assertFalse(ps[0]['actual_same_effective_address_frame_memory_or_buffer_proven'])
    def test_address_displacement_mismatch(self):
        d=fixture();p=d['postcall_context'];p['prior_postcall_compare_shapes'][1]['operands'][0]['geometry']['relative_field_offset']=-2
        self.assertFalse(address_pairs(p['prior_push_definition_shapes'],p['prior_postcall_compare_shapes'])[0]['same_address_spelling_candidate'])
    def test_predicate_sources(self):
        bs=fixture()['postcall_context']['postcall_branch_contexts'];self.assertEqual(len(bs),2)
        self.assertEqual([b['source_candidates'][0]['shape']['mnemonic'] for b in bs],['test','cmp'])
    def test_later_api_frame_is_opaque(self):
        a=fixture()['native_read_context']['read_api_contexts'][1]
        q=next(q for q in a['input_sources']['queries'] if q['site_rva']==APIS[1][0] and q['register']=='ebp')
        self.assertTrue(any(s['origin']=='unknown_call' for s in q['reaching_candidates']))
    def test_api_suffix_is_coherent(self):
        for a in fixture()['native_read_context']['read_api_contexts']:
            self.assertTrue(a['physical_push_suffix']['linear_call_boundary_reached'])
            self.assertEqual(len(a['physical_push_suffix']['pushes']),5)
    def test_wrong_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')

class R40Tamper(unittest.TestCase):
    def reject(self,f):
        d=fixture();f(d)
        with self.assertRaises(ValueError):validate(d)
    def test_all_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r39_exact_report_sha256='wrong'))
    def test_slot_arithmetic(self):self.reject(lambda d:d['native_read_context']['conditional_frame_slot_bridges'][0].update(caller_pre_call_esp_relative_offset=8))
    def test_slot_runtime_binding(self):self.reject(lambda d:d['native_read_context']['conditional_frame_slot_bridges'][0].update(actual_argument_contents_abi_alias_or_owner_binding_proven=True))
    def test_frame_source(self):self.reject(lambda d:d['native_read_context']['conditional_frame_slot_bridges'][0].update(frame_definition_candidate_rva=1))
    def test_stack_summary(self):self.reject(lambda d:d['native_read_context']['frame_definition_esp_summaries'][0].update(unique_conditional_esp_delta=0))
    def test_stack_effect_width(self):self.reject(lambda d:d['native_read_context']['stack_effect_candidates'][0].update(operand_width_bytes=2))
    def test_topology(self):self.reject(lambda d:d['native_read_context']['bounded_edges'].append([1,2]))
    def test_api_import(self):self.reject(lambda d:d['native_read_context']['read_api_contexts'][0]['identity']['import_identity'].update(name='WriteFile'))
    def test_api_abi(self):self.reject(lambda d:d['native_read_context']['read_api_contexts'][0]['physical_push_suffix'].update(abi_roles_applied=True))
    def test_frame_conditions(self):self.reject(lambda d:d['native_read_context']['conditional_frame_slot_bridges'][0].update(requires_32bit_stack_address_and_near_call_geometry=False))
    def test_buffer_binding(self):self.reject(lambda d:d['postcall_context']['buffer_address_spelling_pairs'][0].update(actual_same_effective_address_frame_memory_or_buffer_proven=True))
    def test_address_equality(self):self.reject(lambda d:d['postcall_context']['buffer_address_spelling_pairs'][0].update(same_address_spelling_candidate=False))
    def test_branch_truth(self):self.reject(lambda d:d['postcall_context']['postcall_branch_contexts'][0].update(actual_zf_value_feasible_or_taken_path_proven=True))
    def test_original_bytes(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))

if __name__=='__main__':unittest.main()
