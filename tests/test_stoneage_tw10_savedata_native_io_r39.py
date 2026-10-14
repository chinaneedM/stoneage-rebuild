"""Invented read caller and masked index; no original values or asset bytes."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r39 import *
from tools.stoneage_tw10_savedata_native_io_r39_guard import validate
from tools.stoneage_tw10_savedata_native_io_r38 import derive as derive_r38
from tests import test_stoneage_tw10_savedata_native_io_r38 as r38

@lru_cache(maxsize=1)
def base_fixture():
    captured={}
    def capture(dec,sections,imports,previous):
        raw=bytearray(dec.raw)
        def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
        for at,hexcode in ((0x4ed4e,'660f1f840000000000'),(0x4ed5c,'0f1f00'),
                           (0x4ed62,'0f1f8000000000'),(0x4ed6c,'660f1f440000'),
                           (0x4ed76,'0f1f8400000000000f1f840000000000'),(0x4ed8c,'660f1f440000')):
            put(at,bytes.fromhex(hexcode))
        put(0x4ed95,b'\xe9'+struct.pack('<i',0x4eda5-0x4ed95-5))
        put(0x4ed9a,bytes.fromhex('0f1f8400000000000f1f00'))
        put(0x4eda5,bytes.fromhex('6a018d45ff50530f1f4000'))
        put(READ_CALL,b'\xe8'+struct.pack('<i',READ_ROOT-READ_CALL-5))
        put(READ_CALL+5,bytes.fromhex('83f801807dff1ac3'))
        dec=Decoder(bytes(raw),dec.lo,dec.base)
        previous=derive_r38(dec,sections,imports,previous)
        captured['report']=derive(dec,sections,imports,previous)
        return previous
    r38.base_fixture.cache_clear()
    try:
        with patch.object(r38,'derive',capture):r38.fixture()
    finally:r38.base_fixture.cache_clear()
    return captured['report']

def fixture():return copy.deepcopy(base_fixture())

class R39Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_mask_shift_geometry(self):
        m=fixture()['helper_mask_and_tokens']['conditional_composition']
        self.assertEqual(m['mask'],31);self.assertEqual(m['left_shift_count'],3)
        self.assertTrue(m['unique_mask_to_shift_candidate'])
        self.assertFalse(m['original_input_or_result_known'])
    def test_symbolic_register_tokens(self):
        a=fixture()['helper_mask_and_tokens']['prefix_token_audits']
        self.assertEqual([(x['source_caller_register_symbol'],x['destination_callee_register_symbol']) for x in a],
                         [('ebx','eax'),('esi','ebx')])
        self.assertFalse(any(x['actual_original_contents_argument_value_alias_owner_proven'] for x in a))
    def test_three_pushes_below_parameter_slot(self):
        a=fixture()['helper_mask_and_tokens']['prefix_token_audits'][1]
        self.assertEqual([w['entry_relative_start'] for w in a['modeled_prefix_write_candidates']],[-4,-8,-12])
        self.assertEqual(a['overlapping_write_sites'],[])
    def test_explicit_overwrite_blocks_token(self):
        h=fixture()['helper_mask_and_tokens']
        row=h['prior_stack_read_shapes'][1];b=h['prior_slot_bridges'][1]
        writes=[dict(site_rva=ROOT+8,operand={'width_bytes':4,'geometry':{'base_register':'esp','index_register':None,
                     'segment_register':None,'relative_field_offset':20}})]
        a=prefix_audit(h['prior_stack_evidence'],row,b,writes)
        self.assertFalse(a['conditional_symbolic_register_token_candidate'])
    def test_unknown_alias_blocks_token(self):
        h=fixture()['helper_mask_and_tokens'];row=h['prior_stack_read_shapes'][1];b=h['prior_slot_bridges'][1]
        writes=[dict(site_rva=ROOT+8,operand={'width_bytes':4,'geometry':{'base_register':'eax','index_register':None,
                      'segment_register':None,'relative_field_offset':0}})]
        self.assertFalse(prefix_audit(h['prior_stack_evidence'],row,b,writes)['conditional_symbolic_register_token_candidate'])
    def test_read_suffix_literals_and_buffer_address(self):
        r=fixture()['native_read_caller'];ps=r['push_candidates']
        self.assertEqual(len(ps),3)
        self.assertEqual(ps[2]['input']['constant'],1)
        self.assertTrue(any(x['mnemonic']=='lea' for x in r['push_definition_shapes']))
        self.assertFalse(r['actual_callee_abi_buffer_payload_length_or_return_proven'])
    def test_post_read_comparison_syntax_only(self):
        r=fixture()['native_read_caller']
        self.assertEqual(r['postcall_compare_count'],2)
        self.assertFalse(any(x['actual_instruction_effect_or_value_known'] for x in r['postcall_compare_shapes']))
    def test_wrong_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')

class R39Tamper(unittest.TestCase):
    def reject(self,f):
        d=fixture();f(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior(self):self.reject(lambda d:d.update(r38_exact_report_sha256='wrong'))
    def test_mask_composition(self):self.reject(lambda d:d['helper_mask_and_tokens']['conditional_composition'].update(mask=7))
    def test_token_binding(self):
        self.reject(lambda d:d['helper_mask_and_tokens']['prefix_token_audits'][0].update(actual_original_contents_argument_value_alias_owner_proven=True))
    def test_token_symbol(self):self.reject(lambda d:d['helper_mask_and_tokens']['prefix_token_audits'][1].update(source_caller_register_symbol='eax'))
    def test_prefix_write_overlap(self):self.reject(lambda d:d['helper_mask_and_tokens']['prefix_token_audits'][1].update(overlapping_write_sites=[ROOT]))
    def test_stack_conditions(self):self.reject(lambda d:d['helper_mask_and_tokens']['prior_slot_bridges'][0].update(conditional_32bit_stack_address_required=False))
    def test_read_abi(self):self.reject(lambda d:d['native_read_caller']['pre_call_suffix'].update(abi_roles_applied=True))
    def test_read_buffer_role(self):self.reject(lambda d:d['native_read_caller'].update(actual_callee_abi_buffer_payload_length_or_return_proven=True))
    def test_read_push_value(self):self.reject(lambda d:d['native_read_caller']['push_candidates'][0].update(actual_abi_role_value_or_buffer_length_proven=True))
    def test_read_target(self):self.reject(lambda d:d['native_read_caller']['read_context_call_identity'].update(direct_target_rva=1))
    def test_compare_truth(self):self.reject(lambda d:d['native_read_caller']['postcall_compare_shapes'][0].update(actual_instruction_effect_or_value_known=True))
    def test_counts(self):self.reject(lambda d:d['native_read_caller'].update(postcall_compare_count=100))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))

if __name__=='__main__':unittest.main()
