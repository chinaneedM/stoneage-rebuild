"""Invented adjustment bundle and opaque helper; no original binary fixtures."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r46 import *
from tools.stoneage_tw10_savedata_native_io_r46_guard import validate
from tools.stoneage_tw10_savedata_native_io_r45 import derive as derive_r45
from tests import test_stoneage_tw10_savedata_native_io_r45 as r45


@lru_cache(maxsize=1)
def base_fixture():
    captured={}
    def capture(dec,sections,imports,previous):
        raw=bytearray(dec.raw)
        def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
        def pad(a,b):
            n=b-a;put(a,bytes.fromhex('0f1f840000000000')*(n//8)+b'\x90'*(n%8))
        pad(READ_ROOT+15,0x4a91f)
        put(0x4a91f,bytes.fromhex('8b7d0c'));pad(0x4a922,COPY)
        put(COPY,bytes.fromhex('89f9'));pad(COPY+2,0x4a92f)
        put(0x4a92f,bytes.fromhex('f6c248741d8a0780f80a7416ff4d10880790908d4f01'))
        pad(SHIFT+3,0x4a954)
        put(BARRIER,b'\xe8'+struct.pack('<i',HELPER-BARRIER-5))
        put(HELPER,bytes.fromhex('8b4424045356'));pad(HELPER+6,0x4c78e)
        put(0x4c78e,b'\xe8'+struct.pack('<i',0x49990-0x4c78e-5))
        pad(0x4c793,0x4c7a5)
        put(0x4c7a5,bytes.fromhex('ff7424186a00ff74241c50'))
        pad(0x4c7af,SEEK_API)
        put(SEEK_API,b'\xff\x15'+struct.pack('<I',dec.base+SEEK_IAT)+b'\xc3')
        dec=Decoder(bytes(raw),dec.lo,dec.base);imports=dict(imports);imports[dec.base+SEEK_IAT]=('KERNEL32.dll','SetFilePointer')
        prior=derive_r45(dec,sections,imports,previous)
        captured['report']=derive(dec,sections,imports,prior)
        return prior
    r45.base_fixture.cache_clear()
    try:
        with patch.object(r45,'derive',capture):r45.fixture()
    finally:r45.base_fixture.cache_clear()
    return captured['report']


def fixture():return copy.deepcopy(base_fixture())


class R46Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_optional_bundle(self):
        c=fixture()['read_adjustment_context'];self.assertEqual(c['root_first_api_paths']['reachable_seen_marker_masks'],[0,7])
        r=c['conditional_adjustment_relation'];self.assertTrue(r['both_adjusted_and_bypass_structural_paths_candidate']);self.assertTrue(r['decrement_store_plus_one_cooccur_on_all_bounded_first_api_paths_candidate'])
    def test_store_and_shared_buffer_syntax(self):
        r=fixture()['read_adjustment_context']['conditional_adjustment_relation']
        self.assertTrue(r['byte_store_edi_al_syntax_candidate']);self.assertTrue(r['buffer_plus_one_lea_syntax_candidate']);self.assertEqual(r['shared_unique_edi_definition_rva'],0x4a91f)
    def test_exact_copy_or_shift_sources(self):self.assertTrue(fixture()['read_adjustment_context']['conditional_adjustment_relation']['first_api_buffer_push_has_exact_copy_or_plus_one_sources_candidate'])
    def test_branch_target_bypasses_bundle(self):
        for b in fixture()['read_adjustment_context']['bypass_branch_arms']:self.assertEqual(b['target_arm_paths']['reachable_seen_marker_masks'],[0])
    def test_last_fallthrough_requires_bundle(self):self.assertEqual(fixture()['read_adjustment_context']['bypass_branch_arms'][1]['fallthrough_arm_paths']['reachable_seen_marker_masks'],[7])
    def test_cycle_terminates(self):
        x=signatures([[1,2],[2,1],[2,3]],1,3,(2,));self.assertEqual(x['reachable_seen_marker_masks'],[1]);self.assertFalse(x['state_limit_hit'])
    def test_stop_at_first_goal(self):self.assertEqual(signatures([[1,2],[2,3],[3,2]],1,2,(3,))['reachable_seen_marker_masks'],[0])
    def test_disconnected_goal(self):self.assertEqual(signatures([[1,2]],1,3,(2,))['reachable_seen_marker_masks'],[])
    def test_partial_bundle_rejected_as_cooccurrence(self):
        c=fixture()['read_adjustment_context'];p=signatures([[1,DEC],[DEC,READ_API]],1,READ_API)
        self.assertFalse(bundle_relation(c['window_shapes'],c['input_sources'],p)['decrement_store_plus_one_cooccur_on_all_bounded_first_api_paths_candidate'])
    def test_path_cap_blocks_positive_pairing(self):
        c=fixture()['read_adjustment_context'];p=signatures(c['bounded_edges'],READ_ROOT,READ_API,limit=1)
        self.assertTrue(p['state_limit_hit']);self.assertFalse(bundle_relation(c['window_shapes'],c['input_sources'],p)['both_adjusted_and_bypass_structural_paths_candidate'])
    def test_byte_width_mismatch(self):
        c=fixture()['read_adjustment_context'];next(r for r in c['window_shapes'] if r['site_rva']==STORE)['operands'][0]['width_bytes']=4
        self.assertFalse(bundle_relation(c['window_shapes'],c['input_sources'],c['root_first_api_paths'])['byte_store_edi_al_syntax_candidate'])
    def test_unknown_call_source_blocks_exact_pair(self):
        c=fixture()['read_adjustment_context'];q=next(q for q in c['input_sources']['queries'] if q['site_rva']==BUFFER_PUSH and q['register']=='ecx');q['reaching_candidates'].append({'origin':'unknown_call','rva':READ_ROOT,'semantic':None})
        self.assertFalse(bundle_relation(c['window_shapes'],c['input_sources'],c['root_first_api_paths'])['first_api_buffer_push_has_exact_copy_or_plus_one_sources_candidate'])
    def test_entry_slot_matches_conditional_caller_zero(self):
        b=fixture()['write_helper_context']['conditional_caller_slot_bridges'][0];self.assertTrue(b['conditional_hardware_slot_candidate']);self.assertEqual(b['caller_pre_call_esp_relative_offset'],0)
    def test_late_seek_slots_keep_call_barrier(self):
        w=fixture()['write_helper_context'];self.assertEqual(len(w['conditional_caller_slot_bridges']),3)
        for b,s in zip(w['conditional_caller_slot_bridges'][1:],w['stack_state_queries'][1:]):
            self.assertFalse(b['conditional_hardware_slot_candidate']);self.assertTrue(s['unknown_barrier_candidates'])
    def test_bad_source(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R46Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):self.reject(lambda d,f=f:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r45_exact_report_sha256='bad'))
    def test_r37_hash(self):self.reject(lambda d:d.update(r37_exact_report_sha256='bad'))
    def test_fake_path_mask(self):self.reject(lambda d:d['read_adjustment_context']['root_first_api_paths'].update(reachable_seen_marker_masks=[7]))
    def test_false_bundle_claim(self):self.reject(lambda d:d['read_adjustment_context']['conditional_adjustment_relation'].update(actual_same_buffer_byte_count_text_role_or_execution_proven=True))
    def test_arm_swap(self):self.reject(lambda d:d['read_adjustment_context']['bypass_branch_arms'][1].update(target_arm_paths=d['read_adjustment_context']['bypass_branch_arms'][1]['fallthrough_arm_paths']))
    def test_missing_shape(self):self.reject(lambda d:d['read_adjustment_context']['window_shapes'].pop())
    def test_graph_edge(self):self.reject(lambda d:d['read_adjustment_context']['bounded_edges'].append([1,2]))
    def test_stack_summary(self):self.reject(lambda d:d['write_helper_context']['stack_state_queries'][1].update(unique_conditional_esp_delta=0))
    def test_late_slot_binding(self):self.reject(lambda d:d['write_helper_context']['conditional_caller_slot_bridges'][1].update(conditional_hardware_slot_candidate=True))
    def test_helper_target(self):self.reject(lambda d:d['write_helper_context']['caller_identity'].update(direct_target_rva=1))
    def test_seek_import(self):self.reject(lambda d:d['write_helper_context']['seek_api_identity']['import_identity'].update(name='ReadFile'))
    def test_seek_abi(self):self.reject(lambda d:d['write_helper_context']['seek_physical_push_suffix'].update(abi_roles_applied=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
