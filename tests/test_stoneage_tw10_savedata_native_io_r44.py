"""Invented native slots, explicit ESP arithmetic and two slot-rewrite sources."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r44 import *
from tools.stoneage_tw10_savedata_native_io_r44_guard import validate
from tools.stoneage_tw10_savedata_native_io_r42 import derive as derive_r42
from tools.stoneage_tw10_savedata_native_io_r43 import derive as derive_r43
from tests.test_stoneage_tw10_savedata_native_io_r42 import setup as r42_setup


@lru_cache(maxsize=1)
def base_fixture():
    dec,sections,graph,old=r42_setup();raw=bytearray(dec.raw)
    raw.extend(b'\xcc'*(0x4c5b4+800-dec.lo-len(raw)))
    def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
    for _,root,call,native,_ in WRAPPERS:
        buf=bytes.fromhex('8b4508') if root==0x48bbc else bytes.fromhex('8b5d08')
        prolog=bytes.fromhex('5589e5515356578b7d0c0faf7d10')+buf
        put(root,prolog+b'\x90'*(36-len(prolog))+bytes.fromhex('8b7514'))
        if root==0x48bbc:put(0x48bd2,bytes.fromhex('894508'))
        else:
            put(0x48671,bytes.fromhex('89f9'));put(0x48678,bytes.fromhex('894d08'))
        put(root+39,b'\xe9'+struct.pack('<i',call-3-(root+39)-5))
        put(call+5,b'\xe9'+struct.pack('<i',call-3-(call+5)-5))
        # Callee frame, stack reservation and three four-byte input positions.
        put(native,bytes.fromhex('5589e583ec0c538b75088b7d0c8b4d10837df800ff4d10c3'))
    dec=Decoder(bytes(raw),dec.lo,dec.base);sections=copy.deepcopy(sections);sections[0]['raw_size']=sections[0]['vsize']=len(raw)
    previous=derive_r42(dec,sections,{},old,graph)
    previous=derive_r43(dec,sections,previous)
    return derive(dec,sections,{},previous)


def fixture():return copy.deepcopy(base_fixture())


def literal_row(name='sub',constant=12,width=4,register='esp'):
    return {'site_rva':1,'mnemonic':name,'operands':[{'kind':'register','register':register,'width_bytes':width},
            {'kind':'immediate','constant':constant,'width_bytes':width}]}


def inherited(kind='unknown_esp_write'):
    return {'site_rva':1,'syntax_class':kind,'esp_delta':None,'operand_width_bytes':None,'conditional_32bit_stack_address_only':True}


class R44Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_three_native_slots(self):
        for c in fixture()['native_contexts']:
            bs=c['conditional_native_slot_bridges'][:3]
            self.assertEqual([b['caller_pre_call_esp_relative_offset'] for b in bs],[0,4,8])
            self.assertTrue(all(b['conditional_whole_slot_geometry_candidate'] for b in bs))
    def test_literal_sub_is_qualified(self):
        e=literal_effect(literal_row(),inherited());self.assertEqual(e['esp_delta'],-12);self.assertEqual(e['syntax_class'],'literal_esp_adjustment')
    def test_literal_add_and_negative_immediate(self):
        self.assertEqual(literal_effect(literal_row('add',16),inherited())['esp_delta'],16)
        self.assertEqual(literal_effect(literal_row('sub',-8),inherited())['esp_delta'],8)
    def test_partial_esp_or_large_literal_stays_unknown(self):
        for row in [literal_row(width=2),literal_row(register='sp'),literal_row(constant=4097)]:
            self.assertIsNone(literal_effect(row,inherited())['esp_delta'])
    def test_call_is_never_restored_by_literal_model(self):
        self.assertEqual(literal_effect(literal_row(),inherited('opaque_call')),inherited('opaque_call'))
    def test_postcall_add_retains_unknown_barrier(self):
        a=literal_effect(literal_row('add',12),inherited());a['site_rva']=3
        neutral=dict(inherited(),site_rva=4,syntax_class='neutral',esp_delta=0)
        effects=[dict(inherited('opaque_call'),site_rva=2),a,neutral]
        states,_,limit=stack_states(effects,[[2,3],[3,4]],2)
        self.assertIsNone(state_summary(states,4,limit)['unique_conditional_esp_delta'])
    def test_prefix_pushes_and_local_write_do_not_overlap_inputs(self):
        for c in fixture()['native_contexts']:
            self.assertTrue(all(a['no_bounded_prefix_overwrite_candidate'] for a in c['native_prefix_token_audits'][:3]))
    def test_same_slot_copy_write_candidate(self):
        x=fixture()['mutable_wrapper_slots'][0]['conditional_rewrite_source_link']
        self.assertTrue(x['unique_load_from_same_slot_then_rewrite_candidate'])
        self.assertFalse(x['actual_same_runtime_address_contents_buffer_or_count_proven'])
    def test_second_slot_copy_from_imul_candidate(self):
        x=fixture()['mutable_wrapper_slots'][1]['conditional_rewrite_source_link']
        self.assertTrue(x['unique_register_copy_from_imul_source_candidate'])
        self.assertFalse(x['original_values_or_product_evaluated'])
    def test_mutable_source_closure_no_pending(self):
        self.assertTrue(all(not c['source_expansion_pending_definition_rvas'] for c in fixture()['mutable_wrapper_slots']))
    def test_wrong_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R44Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r43_exact_report_sha256='bad'))
    def test_literal_delta(self):self.reject(lambda d:d['native_contexts'][0]['qualified_prefix_evidence']['stack_effect_candidates'][2].update(esp_delta=-16))
    def test_adjustment_shape(self):self.reject(lambda d:d['native_contexts'][0]['literal_esp_adjustment_or_unknown_shapes'][0]['operands'][1].update(constant=16))
    def test_slot_geometry(self):self.reject(lambda d:d['native_contexts'][0]['conditional_native_slot_bridges'][0].update(caller_pre_call_esp_relative_offset=8))
    def test_slot_abi(self):self.reject(lambda d:d['native_contexts'][0]['conditional_native_slot_bridges'][0].update(actual_argument_contents_abi_alias_or_owner_binding_proven=True))
    def test_prefix_clear(self):self.reject(lambda d:d['native_contexts'][0]['native_prefix_token_audits'][0].update(no_bounded_prefix_overwrite_candidate=False))
    def test_stack_summary(self):self.reject(lambda d:d['native_contexts'][0]['qualified_prefix_evidence']['frame_definition_esp_summaries'][0].update(unique_conditional_esp_delta=0))
    def test_native_identity(self):self.reject(lambda d:d['native_contexts'][0]['caller_identity'].update(direct_target_rva=1))
    def test_rewrite_same_address(self):self.reject(lambda d:d['mutable_wrapper_slots'][0]['conditional_rewrite_source_link'].update(actual_same_runtime_address_contents_buffer_or_count_proven=True))
    def test_rewrite_product(self):self.reject(lambda d:d['mutable_wrapper_slots'][1]['conditional_rewrite_source_link'].update(unique_register_copy_from_imul_source_candidate=False))
    def test_rewrite_route(self):self.reject(lambda d:d['mutable_wrapper_slots'][0].update(structural_store_to_native_call_candidate=False))
    def test_source_scope(self):self.reject(lambda d:d['mutable_wrapper_slots'][0].update(source_definition_count=99))
    def test_source_expansion(self):self.reject(lambda d:d['mutable_wrapper_slots'][0].update(source_expansion_rounds=99))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
