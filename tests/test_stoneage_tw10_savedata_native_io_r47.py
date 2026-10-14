"""Invented partial load, reset, local frame and opaque native-return boundary."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r47 import *
from tools.stoneage_tw10_savedata_native_io_r47_guard import validate
from tools.stoneage_tw10_savedata_native_io_r46 import derive as derive_r46
from tests import test_stoneage_tw10_savedata_native_io_r46 as r46


@lru_cache(maxsize=1)
def base_fixture():
    captured={}
    def capture(dec,sections,imports,previous):
        raw=bytearray(dec.raw)
        def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
        def pad(a,b):
            n=b-a;put(a,bytes.fromhex('0f1f840000000000')*(n//8)+b'\x90'*(n%8))
        pad(READ_ROOT+15,0x4a90d)
        put(0x4a90d,bytes.fromhex('8d0431'));pad(0x4a910,INIT)
        put(INIT,bytes.fromhex('8365f800'))
        put(LOAD,bytes.fromhex('8a4005'))
        put(RELOAD,bytes.fromhex('8b03'))
        put(MARKER,bytes.fromhex('c745f801000000'))
        put(RESET,bytes.fromhex('c64430050a'))
        # Full-width source before AL write. Remaining prolog/frame syntax stays invented.
        put(0x4a90d,bytes.fromhex('8d0431'))
        put(READ_API+6,bytes.fromhex('85c0750a8b45f40345f8c39090908b45f8c3'))
        dec=Decoder(bytes(raw),dec.lo,dec.base)
        prior=derive_r46(dec,sections,imports,previous)
        captured['report']=derive(dec,sections,imports,prior)
        return prior
    r46.base_fixture.cache_clear()
    try:
        with patch.object(r46,'derive',capture):r46.fixture()
    finally:r46.base_fixture.cache_clear()
    return captured['report']


def fixture():return copy.deepcopy(base_fixture())


class R47Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_byte_load_to_store(self):
        r=fixture()['read_byte_result_context']['conditional_byte_relation']
        self.assertTrue(r['one_byte_eax_plus5_load_syntax_candidate']);self.assertTrue(r['store_al_unique_parent_definition_is_load_candidate'])
    def test_partial_parent_mask(self):
        m=fixture()['read_byte_result_context']['conditional_byte_relation']['partial_register_slice_model']
        self.assertTrue(m['qualified_partial_write_syntax']);self.assertEqual(m['slice_width_bits'],8);self.assertEqual(m['preserved_parent_bits_mask'],0xffffff00)
    def test_separate_reload_not_alias(self):
        r=fixture()['read_byte_result_context']['conditional_byte_relation']
        self.assertTrue(r['reset_eax_unique_definition_is_reload_candidate']);self.assertTrue(r['load_eax_and_reset_eax_distinct_local_definition_candidates']);self.assertFalse(r['actual_byte_value_same_address_reset_or_text_role_proven'])
    def test_wrong_reset_immediate(self):
        c=fixture()['read_byte_result_context'];next(r for r in c['byte_shapes'] if r['site_rva']==RESET)['operands'][1]['constant']=11
        self.assertFalse(byte_relation(c['byte_shapes'],c['byte_source_surface']['source_definition_shapes'],c['byte_source_surface']['input_sources'])['reset_byte_eax_esi_plus5_literal10_syntax_candidate'])
    def test_wrong_load_width(self):
        c=fixture()['read_byte_result_context'];next(r for r in c['byte_shapes'] if r['site_rva']==LOAD)['operands'][0]['width_bytes']=4
        r=byte_relation(c['byte_shapes'],c['byte_source_surface']['source_definition_shapes'],c['byte_source_surface']['input_sources']);self.assertFalse(r['one_byte_eax_plus5_load_syntax_candidate']);self.assertFalse(r['partial_register_slice_model']['qualified_partial_write_syntax'])
    def test_reload_call_havoc(self):
        c=fixture()['read_byte_result_context'];s=c['byte_source_surface'];q=next(q for q in s['input_sources']['queries'] if q['site_rva']==RESET and q['register']=='eax')
        q['reaching_candidates']=[{'origin':'unknown_call','rva':READ_ROOT,'semantic':None}]
        self.assertFalse(byte_relation(c['byte_shapes'],s['source_definition_shapes'],s['input_sources'])['reset_eax_unique_definition_is_reload_candidate'])
    def test_same_offset_different_width_not_paired(self):
        refs=[{'site_rva':1,'frame_offset':-8,'width_bytes':4,'decoder_write':True,'decoder_read':False,'address_only_lea_candidate':False},{'site_rva':2,'frame_offset':-8,'width_bytes':1,'decoder_write':False,'decoder_read':True,'address_only_lea_candidate':False}]
        self.assertEqual(frame_pairs(refs),[])
    def test_marker_initialization_and_write_retained(self):
        refs=fixture()['read_byte_result_context']['frame_reference_candidates'];self.assertTrue(any(r['site_rva']==INIT and r['decoder_write'] for r in refs));self.assertTrue(any(r['site_rva']==MARKER and r['decoder_write'] for r in refs))
    def test_post_api_frame_source_retains_unknown_call(self):
        c=fixture()['read_byte_result_context'];q=next(q for q in c['post_api_and_frame_input_sources']['queries'] if q['site_rva']==READ_API+10 and q['register']=='ebp')
        self.assertTrue(any(t['origin']=='unknown_call' and t['rva']==READ_API for t in q['reaching_candidates']))
    def test_wrapper_return_eax_keeps_native_call(self):
        w=fixture()['savedata_wrapper_return_context'];self.assertTrue(any(t['origin']=='unknown_call' and t['rva']==NATIVE_CALL for q in w['input_sources']['queries'] for t in q['reaching_candidates']))
    def test_bad_source(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R47Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):self.reject(lambda d,f=f:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r46_exact_report_sha256='bad'))
    def test_partial_mask(self):self.reject(lambda d:d['read_byte_result_context']['conditional_byte_relation']['partial_register_slice_model'].update(preserved_parent_bits_mask=0))
    def test_reset_role(self):self.reject(lambda d:d['read_byte_result_context']['conditional_byte_relation'].update(actual_byte_value_same_address_reset_or_text_role_proven=True))
    def test_source_count(self):self.reject(lambda d:d['read_byte_result_context']['byte_source_surface'].update(source_definition_count=999))
    def test_source_rounds(self):self.reject(lambda d:d['read_byte_result_context']['byte_source_surface'].update(source_expansion_rounds=0))
    def test_tail_count(self):self.reject(lambda d:d['read_byte_result_context'].update(post_api_shape_count=0))
    def test_frame_pair(self):self.reject(lambda d:d['read_byte_result_context']['equal_frame_spelling_pairs'][0].update(actual_frame_alias_contents_preservation_or_api_effect_proven=True))
    def test_api_identity(self):self.reject(lambda d:d['read_byte_result_context']['first_read_api_identity']['import_identity'].update(name='WriteFile'))
    def test_wrapper_identity(self):self.reject(lambda d:d['savedata_wrapper_return_context']['native_call_identity'].update(direct_target_rva=1))
    def test_wrapper_return_binding(self):self.reject(lambda d:d['savedata_wrapper_return_context'].update(actual_native_return_value_abi_frame_or_wrapper_count_binding_proven=True))
    def test_graph(self):self.reject(lambda d:d['read_byte_result_context']['bounded_edges'].append([1,2]))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
