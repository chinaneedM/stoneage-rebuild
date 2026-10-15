"""Invented overwrite bypass, two temporal slot writes and two DIV sites."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r49 import *
from tools.stoneage_tw10_savedata_native_io_r49_guard import validate


@lru_cache(maxsize=1)
def base_fixture():
    lo,hi,base=0x48000,0x4b000,0x400000;raw=bytearray(b'\xcc'*(hi-lo))
    def put(a,code):raw[a-lo:a-lo+len(code)]=code
    def jump(a,b):put(a,b'\xe9'+struct.pack('<i',b-a-5))
    def pad(a,b):put(a,b'\x90'*(b-a))
    put(READ_ROOT,bytes.fromhex('5589e583ec0c'));jump(READ_ROOT+6,READ_API)
    put(READ_API,b'\xff\x15'+struct.pack('<I',base+0x520d8));jump(READ_API+6,0x4a9a6)
    put(0x4a9a6,bytes.fromhex('8b55f40155f8'));jump(0x4a9ac,0x4a9b4)
    put(0x4a9b4,bytes.fromhex('a8800f84')+struct.pack('<i',RETURN_LOAD-(BYPASS+6)));jump(BYPASS+6,OVERWRITE-3)
    put(OVERWRITE-3,bytes.fromhex('2b7d0c897df88b45f8c3'))
    put(WRAPPER,bytes.fromhex('5589e583ec0c90'));put(SEEDS[0],bytes.fromhex('8b7d0c0faf7d10'))
    pad(0x4866e,0x48671);put(0x48671,bytes.fromhex('89f9'));pad(0x48673,0x48678)
    put(0x48678,bytes.fromhex('894d088b75148b4618'));jump(0x48681,0x4869d)
    put(0x4869d,bytes.fromhex('894514'));jump(0x486a0,0x486de)
    put(0x486de,bytes.fromhex('89c8909031d2f77514'));jump(0x486e7,NATIVE_CALL-3)
    put(NATIVE_CALL-3,bytes.fromhex('505153'));put(NATIVE_CALL,b'\xe8'+struct.pack('<i',READ_ROOT-NATIVE_CALL-5))
    put(NATIVE_CALL+5,bytes.fromhex('83c40c'));jump(NATIVE_CALL+8,0x48701)
    put(0x48701,bytes.fromhex('29450801c3'));jump(0x48706,0x48716)
    put(0x48716,bytes.fromhex('8b4618'));pad(0x48719,0x4871d)
    put(0x4871d,bytes.fromhex('894514837d080075b8'));jump(0x48726,0x4873c)
    put(0x48731,b'\xc3');put(0x4873c,bytes.fromhex('89f831d22b4508f7750c'));jump(0x48746,0x48731)
    dec=Decoder(bytes(raw),lo,base)
    sections=[{'name':'.text','rva':lo,'vsize':hi-lo,'raw':0,'raw_size':hi-lo,'characteristics':0x60000020},
              {'name':'.rdata','rva':0x52000,'vsize':0x1000,'raw':hi-lo,'raw_size':0x1000,'characteristics':0x40000040}]
    imports={base+0x520d8:('KERNEL32.dll','ReadFile')}
    n,e,_,_=candidate_graph(dec,READ_ROOT);wn,we,_,_=candidate_graph(dec,WRAPPER)
    prior={'schema':'tw10-r48-original-native-count-return-barriers-wrapper-loop-division',
           'native_count_return_context':{'bounded_node_rvas':sorted(n),'bounded_edges':[list(x) for x in sorted(e)],'return_memory_predecessor_shapes':[instruction_row(dec,sections,n,OVERWRITE)]},
           'wrapper_loop_division_context':{'bounded_node_rvas':sorted(wn),'bounded_edges':[list(x) for x in sorted(we)],'native_call_identity':call_identity(dec,NATIVE_CALL,imports,sections),'division_shapes':[instruction_row(dec,sections,wn,a) for a in DIVS]}}
    return derive(dec,sections,imports,prior)


def fixture():return copy.deepcopy(base_fixture())


class R49Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_unique_edi_sub_source(self):
        r=fixture()['native_overwrite_context']['conditional_overwrite_link'];self.assertEqual(r['unique_edi_definition_rva'],OVERWRITE-3);self.assertEqual(r['unique_edi_definition_shape']['mnemonic'],'sub')
    def test_bypass_and_overwrite_routes(self):
        c=fixture()['native_overwrite_context'];self.assertTrue(c['branch_target_to_return_avoiding_overwrite_candidate']);self.assertTrue(c['branch_fallthrough_to_overwrite_candidate']);self.assertTrue(c['overwrite_to_return_load_candidate'])
    def test_two_temporal_slot_writes(self):self.assertEqual([r['write_site_rva'] for r in fixture()['wrapper_temporal_slot_context']['frame_plus20_write_source_links']],[0x4869d,0x4871d])
    def test_slot_load_is_not_a_write(self):
        w=fixture()['wrapper_temporal_slot_context'];read=next(r for r in w['frame_plus20_shapes'] if r['mnemonic']=='mov' and r['operands'][0].get('kind')=='register')
        self.assertEqual(write_source_links([read],w['temporal_source_surface']),[])
    def test_field_load_source_syntax(self):self.assertTrue(all(r['unique_definition_has_esi_plus24_load_spelling_candidate'] for r in fixture()['wrapper_temporal_slot_context']['frame_plus20_write_source_links']))
    def test_partial_slot_width_is_retained_as_spelling_only(self):
        w=fixture()['wrapper_temporal_slot_context'];r=copy.deepcopy(w['frame_plus20_shapes'][0]);ref=slot_refs([r],20)[0];r['operands'][ref['operand_index']]['width_bytes']=1
        self.assertEqual(slot_refs([r],20)[0]['width_bytes'],1);self.assertFalse(slot_refs([r],20)[0]['actual_same_frame_contents_or_parameter_role_proven'])
    def test_edi_call_havoc_does_not_create_unique_source(self):
        c=fixture()['native_overwrite_context'];s=c['edi_source_surface'];q=next(q for q in s['input_sources']['queries'] if q['site_rva']==OVERWRITE and q['register']=='edi')
        q['reaching_candidates']=[{'origin':'unknown_call','rva':READ_API,'semantic':None}]
        self.assertIsNone(overwrite_link(c['overwrite_shape'],s)['unique_edi_definition_rva'])
    def test_numerators_and_divisors_separate(self):
        w=fixture()['wrapper_temporal_slot_context'];self.assertEqual([r['site_rva'] for r in w['division_shapes']],list(DIVS));self.assertEqual([a['division_site_rva'] for a in w['division_memory_boundary_audits']],list(DIVS))
    def test_first_div_temporal_matching_candidates(self):
        a=fixture()['wrapper_temporal_slot_context']['division_memory_boundary_audits'][0]['audit'];self.assertEqual(a['same_frame_spelling_write_candidate_sites'],[0x4869d,0x4871d])
    def test_final_div_retains_alias_barrier(self):
        a=fixture()['wrapper_temporal_slot_context']['division_memory_boundary_audits'][1]['audit'];self.assertTrue(any(t['kind']=='explicit_memory_write_alias_unknown' for t in a['terminal_candidates']))
    def test_source_caps_explicit(self):
        for s in [fixture()['native_overwrite_context']['edi_source_surface'],fixture()['wrapper_temporal_slot_context']['temporal_source_surface']]:self.assertEqual(s['source_expansion_rounds'],2);self.assertIn('source_expansion_pending_definition_rvas',s)
    def test_bad_source(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R49Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):self.reject(lambda d,f=f:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r48_exact_report_sha256='bad'))
    def test_edi_value(self):self.reject(lambda d:d['native_overwrite_context']['conditional_overwrite_link'].update(actual_edi_byte_count_conversion_alias_or_overwrite_value_proven=True))
    def test_unique_source(self):self.reject(lambda d:d['native_overwrite_context']['conditional_overwrite_link'].update(unique_edi_definition_rva=1))
    def test_native_path(self):self.reject(lambda d:d['native_overwrite_context'].update(branch_target_to_return_avoiding_overwrite_candidate=False))
    def test_source_count(self):self.reject(lambda d:d['wrapper_temporal_slot_context']['temporal_source_surface'].update(source_definition_count=999))
    def test_temporal_write_source(self):self.reject(lambda d:d['wrapper_temporal_slot_context']['frame_plus20_write_source_links'][0].update(actual_stream_buffer_capacity_owner_value_or_slot_binding_proven=True))
    def test_slot_read_write_flags(self):self.reject(lambda d:next(r for r in d['wrapper_temporal_slot_context']['frame_plus20_reference_candidates'] if r['decoder_write']).update(decoder_write=False))
    def test_memory_alias(self):self.reject(lambda d:d['wrapper_temporal_slot_context']['division_memory_boundary_audits'][0]['audit'].update(actual_same_address_contents_alias_or_return_count_proven=True))
    def test_missing_audit_shape(self):self.reject(lambda d:d['wrapper_temporal_slot_context']['division_memory_boundary_audits'][0]['predecessor_shapes'].pop())
    def test_division_order(self):self.reject(lambda d:d['wrapper_temporal_slot_context']['division_shapes'].reverse())
    def test_graph(self):self.reject(lambda d:d['native_overwrite_context']['bounded_edges'].append([1,2]))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
