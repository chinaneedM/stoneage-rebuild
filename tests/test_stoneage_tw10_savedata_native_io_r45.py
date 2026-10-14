"""Invented optional decrement branch, API pushes and opaque write helper."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r45 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import validate
from tools.stoneage_tw10_savedata_native_io_r44 import derive as derive_r44
from tests import test_stoneage_tw10_savedata_native_io_r44 as r44


@lru_cache(maxsize=1)
def base_fixture():
    captured={}
    def capture(dec,sections,imports,previous):
        raw=bytearray(dec.raw)
        def put(at,code):raw[at-dec.lo:at-dec.lo+len(code)]=code
        def pad(a,b):
            n=b-a;put(a,bytes.fromhex('0f1f840000000000')*(n//8)+b'\x90'*(n%8))
        prolog=bytes.fromhex('5589e583ec0c538b75088b7d0c8b4d10')
        put(READ_ROOT,prolog);pad(READ_ROOT+len(prolog),0x4a935)
        put(0x4a935,bytes.fromhex('85c07405'));pad(0x4a939,DEC)
        put(DEC,bytes.fromhex('ff4d10'));pad(DEC+3,0x4a954)
        put(0x4a954,bytes.fromhex('6a00509090ff751051ff3430'))
        put(APIS[0][2],b'\xff\x15'+struct.pack('<I',dec.base+APIS[0][4])+b'\xc3')
        put(WRITE_ROOT,prolog);pad(WRITE_ROOT+len(prolog),BARRIER)
        put(BARRIER,b'\xe8'+struct.pack('<i',0x49990-BARRIER-5))
        put(BARRIER+5,bytes.fromhex('83c40c'));pad(BARRIER+8,BUFFER_READ)
        put(BUFFER_READ,bytes.fromhex('8b7d0c'));pad(BUFFER_READ+3,0x4c67c)
        put(0x4c67c,bytes.fromhex('6a00508d45fc90909057509090ff3430'))
        put(APIS[1][2],b'\xff\x15'+struct.pack('<I',dec.base+APIS[1][4])+b'\xc3')
        dec=Decoder(bytes(raw),dec.lo,dec.base);imports=dict(imports)
        for name,_,_,_,slot in APIS:imports[dec.base+slot]=('KERNEL32.dll',name)
        prior=derive_r44(dec,sections,imports,previous)
        captured['report']=derive(dec,sections,imports,prior)
        return prior
    r44.base_fixture.cache_clear()
    try:
        with patch.object(r44,'derive',capture):r44.fixture()
    finally:r44.base_fixture.cache_clear()
    return captured['report']


def fixture():return copy.deepcopy(base_fixture())


class R45Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_optional_decrement_has_bypass(self):
        x=fixture()['read_count_context']['conditional_count_relationship']
        self.assertTrue(x['decrement_to_push_structural_path_candidate'])
        self.assertTrue(x['root_to_push_path_avoiding_decrement_candidate'])
        self.assertFalse(x['decrement_on_all_bounded_root_to_push_paths_candidate'])
    def test_shared_count_syntax_and_frame_source_only(self):
        x=fixture()['read_count_context']['conditional_count_relationship']
        self.assertTrue(x['same_four_byte_count_slot_spelling_candidate'])
        self.assertTrue(x['same_graph_local_frame_source_candidate'])
        self.assertFalse(x['actual_same_address_contents_modified_count_or_taken_path_proven'])
    def test_single_path_requires_decrement(self):
        self.assertTrue(path_without([[1,2],[2,3]],1,3))
        self.assertFalse(path_without([[1,2],[2,3]],1,3,2))
    def test_cycle_does_not_invent_bypass(self):
        self.assertFalse(path_without([[1,2],[2,3],[3,2]],1,3,2))
    def test_disconnected_push_not_dominance(self):
        d=fixture();c=d['read_count_context'];r=count_relationship(READ_ROOT,[],c['decrement_shape'],c['count_push_shape'],c['count_frame_input_sources'])
        self.assertFalse(r['decrement_on_all_bounded_root_to_push_paths_candidate'])
    def test_partial_width_count_does_not_qualify(self):
        d=fixture();c=d['read_count_context'];c['count_push_shape']['operands'][0]['width_bytes']=1
        self.assertFalse(count_relationship(READ_ROOT,c['bounded_edges'],c['decrement_shape'],c['count_push_shape'],c['count_frame_input_sources'])['same_four_byte_count_slot_spelling_candidate'])
    def test_frame_havoc_blocks_same_source(self):
        d=fixture();c=d['read_count_context'];q=next(q for q in c['count_frame_input_sources']['queries'] if q['site_rva']==COUNT_PUSH and q['register']=='ebp')
        q['reaching_candidates']=[{'origin':'unknown_call','rva':READ_ROOT,'semantic':None}]
        self.assertFalse(count_relationship(READ_ROOT,c['bounded_edges'],c['decrement_shape'],c['count_push_shape'],c['count_frame_input_sources'])['same_graph_local_frame_source_candidate'])
    def test_two_exact_api_imports_and_five_pushes(self):
        for a,s in zip(fixture()['native_api_contexts'],APIS):
            self.assertEqual(a['identity']['import_identity']['name'],s[0]);self.assertEqual(len(a['physical_push_suffix']['pushes']),5)
    def test_conditional_branch_zf_source(self):
        b=fixture()['read_count_context']['zf_branch_contexts'][0]
        self.assertEqual(b['source_candidates'][0]['shape']['mnemonic'],'test')
    def test_delayed_frame_source_retains_unknown_call(self):
        w=fixture()['delayed_write_context'];q=next(q for q in w['input_sources']['queries'] if q['site_rva']==BUFFER_READ and q['register']=='ebp')
        self.assertTrue(any(t['origin']=='unknown_call' and t['rva']==BARRIER for t in q['reaching_candidates']))
    def test_bad_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R45Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r44_exact_report_sha256='bad'))
    def test_forced_all_paths(self):self.reject(lambda d:d['read_count_context']['conditional_count_relationship'].update(decrement_on_all_bounded_root_to_push_paths_candidate=True))
    def test_branch_actual_value(self):self.reject(lambda d:d['read_count_context']['zf_branch_contexts'][0].update(actual_flag_value_feasibility_or_taken_path_proven=True))
    def test_graph_path(self):self.reject(lambda d:d['read_count_context']['bounded_edges'].append([1,2]))
    def test_import_identity(self):self.reject(lambda d:d['native_api_contexts'][0]['identity']['import_identity'].update(name='WriteFile'))
    def test_api_abi(self):self.reject(lambda d:d['native_api_contexts'][0]['physical_push_suffix'].update(abi_roles_applied=True))
    def test_definition_count(self):self.reject(lambda d:d['native_api_contexts'][0].update(direct_definition_count=99))
    def test_frame_preservation(self):self.reject(lambda d:d['delayed_write_context'].update(same_bound_frame_source_after_call_proven=True))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
