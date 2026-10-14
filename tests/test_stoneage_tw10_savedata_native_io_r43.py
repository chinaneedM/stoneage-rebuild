"""Invented prefix writes, symbolic tokens, multiply inputs and CALL cycles."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r43 import *
from tools.stoneage_tw10_savedata_native_io_r43_guard import validate
from tools.stoneage_tw10_savedata_native_io_r42 import derive as derive_r42
from tests.test_stoneage_tw10_savedata_native_io_r42 import setup as r42_setup


@lru_cache(maxsize=1)
def base_fixture():
    dec,sections,graph,old=r42_setup();raw=bytearray(dec.raw)
    def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
    for _,root,call,_,_ in WRAPPERS:
        # Real operand shape at documented sites, entirely invented instruction bytes.
        prolog=bytes.fromhex('5589e5515356578b7d0c0faf7d108b4508')
        put(root,prolog+b'\x90'*(33-len(prolog))+bytes.fromhex('8945fc8b7514'))
        put(root+39,b'\xe9'+struct.pack('<i',call-3-(root+39)-5))
        put(call+5,b'\xe9'+struct.pack('<i',call-3-(call+5)-5))
    dec=Decoder(bytes(raw),dec.lo,dec.base)
    prior=derive_r42(dec,sections,{},old,graph)
    return derive(dec,sections,prior)


def fixture():return copy.deepcopy(base_fixture())


def audit_last(d):
    c=d['contexts'][0];b=c['savedata_caller_token_contexts'][0];i=3
    return prefix_audit(c['root_candidate_rva'],c['prior_wrapper_evidence'],c['early_parameter_read_shapes'][i],
                        b['conditional_slot_bridges'][i],c['prefix_input_sources'])


class R43Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_prefix_symbols(self):
        for c in fixture()['contexts']:
            for b in c['savedata_caller_token_contexts']:
                self.assertTrue(all(a['conditional_caller_operand_to_register_symbol_candidate'] for a in b['prefix_token_audits'] if a['source_push_rva'] is not None))
                self.assertFalse(any(a['actual_original_contents_argument_value_alias_owner_proven'] for a in b['prefix_token_audits']))
    def test_two_unique_multiply_load_sources(self):
        self.assertTrue(all(c['conditional_multiply_source_link']['conditional_two_memory_operands_multiply_shape'] for c in fixture()['contexts']))
    def test_local_frame_write_is_disjoint(self):
        a=audit_last(fixture());writes=[w for w in a['modeled_prefix_write_candidates'] if w['kind']=='explicit_memory_write']
        self.assertEqual(writes[0]['entry_relative_start'],-8)
        self.assertTrue(a['no_bounded_prefix_overwrite_candidate'])
    def test_overlapping_frame_write_blocks_token(self):
        d=fixture();w=d['contexts'][0]['prior_wrapper_evidence']['prefix_explicit_write_shapes'][0]
        w['operands'][0]['geometry']['relative_field_offset']=20
        self.assertFalse(audit_last(d)['no_bounded_prefix_overwrite_candidate'])
    def test_unqualified_alias_blocks_token(self):
        d=fixture();w=d['contexts'][0]['prior_wrapper_evidence']['prefix_explicit_write_shapes'][0]
        w['operands'][0]['geometry']['base_register']='esi'
        self.assertFalse(audit_last(d)['conditional_caller_operand_to_register_symbol_candidate'])
    def test_unknown_prefix_instruction_blocks_token(self):
        d=fixture();e=d['contexts'][0]['prior_wrapper_evidence'];r=copy.deepcopy(e['prefix_explicit_write_shapes'][0]);r['mnemonic']='stosd'
        e['prefix_unmodeled_effect_shapes']=[r]
        self.assertFalse(audit_last(d)['conditional_caller_operand_to_register_symbol_candidate'])
    def test_frame_source_call_barrier_blocks_token(self):
        d=fixture();c=d['contexts'][0];site=c['prior_wrapper_evidence']['prefix_explicit_write_shapes'][0]['site_rva']
        q=next(q for q in c['prefix_input_sources']['queries'] if q['site_rva']==site and q['register']=='ebp')
        q['reaching_candidates']=[{'origin':'unknown_call','rva':c['root_candidate_rva'],'semantic':None}]
        self.assertFalse(audit_last(d)['no_bounded_prefix_overwrite_candidate'])
    def test_ambiguous_multiply_input_blocks_unique(self):
        d=fixture();c=d['contexts'][0];q=next(q for q in c['prefix_input_sources']['queries'] if q['site_rva']==c['multiply_shape']['site_rva'] and q['register']=='edi')
        q['reaching_candidates'].append({'origin':'entry','rva':c['root_candidate_rva'],'semantic':None})
        self.assertFalse(product_link(c['multiply_load_shape'],c['multiply_shape'],c['prefix_input_sources'])['unique_local_load_definition_to_imul_candidate'])
    def test_partial_multiply_shape_unqualified(self):
        c=fixture()['contexts'][0];c['multiply_shape']['operands'][0]['width_bytes']=2
        self.assertFalse(product_link(c['multiply_load_shape'],c['multiply_shape'],c['prefix_input_sources'])['conditional_two_memory_operands_multiply_shape'])
    def test_cycle_sources_retain_opaque_call(self):
        for c in fixture()['contexts']:
            self.assertTrue(any(r['source_origin']=='unknown_call' and r['same_structural_cycle_region_candidate'] for r in c['cycle_source_candidates']))
    def test_bad_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R43Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r42_exact_report_sha256='bad'))
    def test_prefix_clear(self):self.reject(lambda d:d['contexts'][0]['savedata_caller_token_contexts'][0]['prefix_token_audits'][0].update(no_bounded_prefix_overwrite_candidate=False))
    def test_prefix_binding(self):self.reject(lambda d:d['contexts'][0]['savedata_caller_token_contexts'][0]['prefix_token_audits'][0].update(actual_original_contents_argument_value_alias_owner_proven=True))
    def test_prefix_geometry(self):self.reject(lambda d:d['contexts'][0]['savedata_caller_token_contexts'][0]['conditional_slot_bridges'][0].update(caller_pre_call_esp_relative_offset=99))
    def test_product_value(self):self.reject(lambda d:d['contexts'][0]['conditional_multiply_source_link'].update(original_inputs_or_product_evaluated=True))
    def test_product_unique(self):self.reject(lambda d:d['contexts'][0]['conditional_multiply_source_link'].update(unique_local_load_definition_to_imul_candidate=False))
    def test_loop_cycle(self):self.reject(lambda d:d['contexts'][0]['cycle_source_candidates'][0].update(same_structural_cycle_region_candidate=True))
    def test_loop_execution(self):self.reject(lambda d:d['contexts'][0]['cycle_source_candidates'][0].update(actual_iteration_value_callee_effect_or_feasible_path_proven=True))
    def test_definition_count(self):self.reject(lambda d:d['contexts'][0].update(native_direct_definition_count=99))
    def test_definition_cap(self):self.reject(lambda d:d['contexts'][0].update(native_direct_definitions_truncated=True))
    def test_prior_gap(self):self.reject(lambda d:d['contexts'][0].update(prior_sampler_omitted_definition_rvas=[OMITTED]))
    def test_stack_summary(self):self.reject(lambda d:d['contexts'][0]['prior_wrapper_evidence']['frame_definition_esp_summaries'][0].update(unique_conditional_esp_delta=0))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
