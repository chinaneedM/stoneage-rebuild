"""Independent invented native/return/loop graphs; no inherited byte fixture mutation."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r48 import *
from tools.stoneage_tw10_savedata_native_io_r48_guard import validate


@lru_cache(maxsize=1)
def base_fixture():
    lo,hi,base=0x48000,0x4b000,0x400000;raw=bytearray(b'\xcc'*(hi-lo))
    def put(at,code):raw[at-lo:at-lo+len(code)]=code
    def jump(at,target):put(at,b'\xe9'+struct.pack('<i',target-at-5))
    put(READ_ROOT,bytes.fromhex('5589e583ec0c'));jump(READ_ROOT+6,READ_API)
    put(READ_API,b'\xff\x15'+struct.pack('<I',base+0x520d8))
    put(READ_API+6,bytes.fromhex('85c00f84')+struct.pack('<i',0x4aaa0-(READ_API+14)))
    jump(READ_API+14,COUNT_LOAD)
    put(COUNT_LOAD,bytes.fromhex('8b55f40155f8'));jump(ACCUM+3,RETURN_LOAD)
    put(0x4aaa0,bytes.fromhex('31c0'));jump(0x4aaa2,RETURN_LOAD+3)
    put(RETURN_LOAD,bytes.fromhex('8b45f8c3'))
    put(WRAPPER,bytes.fromhex('5589e583ec0c8b7d0c'));jump(WRAPPER+9,NATIVE_CALL-3)
    put(NATIVE_CALL-3,bytes.fromhex('505153'));put(NATIVE_CALL,b'\xe8'+struct.pack('<i',READ_ROOT-NATIVE_CALL-5))
    put(NATIVE_CALL+5,bytes.fromhex('83c40c85c0743683f8ff743f29450801c3eb18'))
    put(0x48720,bytes.fromhex('837d080075c7eb0a'))
    put(0x48732,bytes.fromhex('89f831d2f7750cc3'))
    put(0x48740,bytes.fromhex('83c8ffc3'))
    dec=Decoder(bytes(raw),lo,base)
    sections=[{'name':'.text','rva':lo,'virtual_size':hi-lo,'raw':0,'raw_size':hi-lo,'characteristics':0x60000020},
              {'name':'.rdata','rva':0x52000,'virtual_size':0x1000,'raw':hi-lo,'raw_size':0x1000,'characteristics':0x40000040}]
    imports={base+0x520d8:('KERNEL32.dll','ReadFile')}
    n,e,f,c=candidate_graph(dec,READ_ROOT);wn,we,wf,wc=candidate_graph(dec,WRAPPER)
    # Minimal synthetic prerequisite fields checked by derive; original custody is tested remotely.
    prior={'schema':'tw10-r47-original-byte-source-partial-geometry-local-results-wrapper-return',
           'read_byte_result_context':{'bounded_node_rvas':sorted(n),'bounded_edges':[list(x) for x in sorted(e)],
               'frame_reference_shapes':[instruction_row(dec,sections,n,a) for a in (COUNT_LOAD,ACCUM,RETURN_LOAD)]},
           'savedata_wrapper_return_context':{'native_call_identity':call_identity(dec,NATIVE_CALL,imports,sections),
               'bounded_node_rvas':sorted(wn),'bounded_edges':[list(x) for x in sorted(we)]}}
    return derive(dec,sections,imports,prior)


def fixture():return copy.deepcopy(base_fixture())


class R48Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_count_load_reaches_add(self):self.assertTrue(fixture()['native_count_return_context']['conditional_count_relation']['add_edx_unique_source_is_count_load_candidate'])
    def test_native_add_to_return_path(self):self.assertTrue(fixture()['native_count_return_context']['conditional_count_relation']['accumulation_to_return_load_structural_path_candidate'])
    def test_actual_count_never_evaluated(self):self.assertFalse(fixture()['native_count_return_context']['conditional_count_relation']['actual_transferred_prefix_total_or_return_count_evaluated'])
    def test_nearest_matching_frame_spelling_write(self):self.assertEqual(fixture()['native_count_return_context']['return_memory_boundary_audit']['same_frame_spelling_write_candidate_sites'],[ACCUM])
    def test_return_eax_alternatives(self):
        s=fixture()['native_count_return_context']['return_surface'];q=next(q for q in s['input_sources']['queries'] if q['site_rva']==RETURN_LOAD+3 and q['register']=='eax')
        self.assertEqual({t['rva'] for t in q['reaching_candidates']},{RETURN_LOAD,0x4aaa0})
    def test_opaque_native_call_consumers(self):self.assertTrue(fixture()['wrapper_loop_division_context']['conditional_consumer_relation']['four_consumers_have_only_opaque_native_call_eax_origin_candidate'])
    def test_wrapper_structural_loop(self):
        r=fixture()['wrapper_loop_division_context']['conditional_consumer_relation'];self.assertTrue(r['subtract_to_native_call_structural_loop_candidate']);self.assertTrue(r['buffer_advance_to_native_call_structural_loop_candidate'])
    def test_division_syntax(self):
        ds=fixture()['wrapper_loop_division_context']['division_shapes'];self.assertEqual(len(ds),1);self.assertEqual(ds[0]['mnemonic'],'div')
    def audit_with(self,kind):
        c=fixture()['native_count_return_context'];rows=copy.deepcopy(c['return_memory_predecessor_shapes']);r=next(r for r in rows if r['site_rva']==ACCUM)
        if kind=='call':r.update(mnemonic='call',operands=[],decoder_written_registers=[])
        elif kind=='push':r.update(mnemonic='push',operands=[],decoder_written_registers=['esp'])
        elif kind=='other_write':r['operands'][0]['geometry']['base_register']='edi'
        elif kind=='partial':r['operands'][0]['width_bytes']=1
        elif kind=='frame':r['decoder_written_registers']=['ebp']
        elif kind=='unmodeled':r.update(mnemonic='stosb',operands=[],decoder_written_registers=['edi'])
        return memory_audit({r['site_rva']:r for r in rows},c['bounded_edges'],READ_ROOT,RETURN_LOAD,c['count_shapes'][-1]['operands'][1])
    def test_call_memory_barrier(self):self.assertEqual(self.audit_with('call')['terminal_candidates'][0]['kind'],'opaque_call')
    def test_implicit_stack_alias_barrier(self):self.assertEqual(self.audit_with('push')['terminal_candidates'][0]['kind'],'implicit_stack_write_alias_unknown')
    def test_other_write_alias_barrier(self):self.assertEqual(self.audit_with('other_write')['terminal_candidates'][0]['kind'],'explicit_memory_write_alias_unknown')
    def test_partial_overlap_barrier(self):self.assertEqual(self.audit_with('partial')['terminal_candidates'][0]['kind'],'overlapping_frame_spelling_write')
    def test_frame_write_barrier(self):self.assertEqual(self.audit_with('frame')['terminal_candidates'][0]['kind'],'frame_register_write')
    def test_unmodeled_effect_barrier(self):self.assertEqual(self.audit_with('unmodeled')['terminal_candidates'][0]['kind'],'unmodeled_instruction_effect')
    def test_cycle_and_cap(self):
        c=fixture()['native_count_return_context'];rows={r['site_rva']:r for r in c['return_memory_predecessor_shapes']}
        a=memory_audit(rows,c['bounded_edges'],READ_ROOT,RETURN_LOAD,c['count_shapes'][-1]['operands'][1],limit=1);self.assertTrue(a['predecessor_limit_hit'])
    def test_bad_source(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')


class R48Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):self.reject(lambda d,f=f:d.update({f:True}))
    def test_prior(self):self.reject(lambda d:d.update(r47_exact_report_sha256='bad'))
    def test_fake_frame_source(self):self.reject(lambda d:d['native_count_return_context']['conditional_count_relation'].update(same_unique_graph_local_ebp_source_candidate=True))
    def test_memory_value(self):self.reject(lambda d:d['native_count_return_context']['return_memory_boundary_audit'].update(actual_same_address_contents_alias_or_return_count_proven=True))
    def test_memory_terminal(self):self.reject(lambda d:d['native_count_return_context']['return_memory_boundary_audit'].update(terminal_candidates=[]))
    def test_missing_audit_shape(self):self.reject(lambda d:d['native_count_return_context']['return_memory_predecessor_shapes'].pop())
    def test_return_definition_count(self):self.reject(lambda d:d['native_count_return_context']['return_surface'].update(direct_return_definition_count=999))
    def test_loop_claim(self):self.reject(lambda d:d['wrapper_loop_division_context']['conditional_consumer_relation'].update(actual_native_return_bytes_element_count_or_iteration_proven=True))
    def test_division_count(self):self.reject(lambda d:d['wrapper_loop_division_context'].update(division_count=0))
    def test_branch_value(self):self.reject(lambda d:d['wrapper_loop_division_context']['native_result_test_branches'][0].update(actual_flag_value_feasibility_or_taken_path_proven=True))
    def test_call_target(self):self.reject(lambda d:d['wrapper_loop_division_context']['native_call_identity'].update(direct_target_rva=1))
    def test_graph(self):self.reject(lambda d:d['native_count_return_context']['bounded_edges'].append([1,2]))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__=='__main__':unittest.main()
