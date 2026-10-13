"""Invented mask/shift and writer discovery controls; never original values."""
import copy,struct,unittest
from tools.stoneage_tw10_savedata_native_io_r30 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import validate
from tools.stoneage_tw10_savedata_native_io_r29 import eval_synthetic
BASE=0x400000

def fixture():
    lo=0x48000;hi=WRITER+32;raw=bytearray(b'\x90'*(hi-lo));prior={'contexts':[]}
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    for api,root,site,shift in MASKS:
        put(site,bytes.fromhex('83e61f'));put(shift,bytes.fromhex('c1e603'));put(shift+3,b'\xc3')
    root=WRITER-24;caller=lo+16
    put(caller,b'\xe8'+struct.pack('<i',root-caller-5))
    put(WRITER-5,b'\xe8'+struct.pack('<i',0x51000-WRITER))
    put(WRITER,b'\xa3'+struct.pack('<I',BASE+SHARED));put(WRITER+5,b'\xc3')
    dec=Decoder(bytes(raw),lo,BASE);sections=[dict(name='.data',rva=SHARED,vsize=4096,raw_size=0,raw=0,characteristics=0xc0000040)]
    for api,r,site,shift in MASKS:
        nodes,_,_,_=candidate_graph(dec,r)
        prior['contexts'].append(dict(api=api,root_candidate_rva=r,inputs={'queries':[dict(site_rva=shift,register='esi',reaching_candidates=[dict(origin='definition',rva=site)])]},scalar_definitions=[dict(site_rva=shift,shape=shape_at(dec,sections,nodes,shift))]))
    dis=discover_writer(dec)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r29_exact_original_revalidated=True,r29_exact_report_sha256=PRIOR_SHA256,static_only=True,
                mask_contexts=[mask_context(dec,sections,prior,*r) for r in MASKS],
                writer_discovery=dis,writer_inputs=writer_context(dec,sections,{},dis),**{k:False for k in FLAGS})

class R30Synthetic(unittest.TestCase):
    def test_valid_invented_fixture(self):self.assertTrue(validate(fixture()))
    def test_conditional_mask_then_shift(self):
        c=fixture()['mask_contexts'][0];self.assertEqual((c['composition']['mask'],c['composition']['left_shift_count']),(31,3))
        first=eval_synthetic(c['mask_model'],{'esi':0xdeadbeef});second=eval_synthetic(scalar_model(c['shift_shape'],'esi'),{'esi':first})
        self.assertEqual(second,120);self.assertIsNone(c['composition']['evaluated_original_result'])
    def test_join_blocks_composition(self):
        c=fixture()['mask_contexts'][0];q=next(q for q in c['inputs']['queries'] if q['site_rva']==MASKS[0][3] and q['register']=='esi')
        q['reaching_candidates']*=2;self.assertEqual(composition(c['mask_shape'],c['shift_shape'],q)['kind'],'unqualified_composition')
    def test_truncation_blocks_composition(self):
        c=fixture()['mask_contexts'][0];q=next(q for q in c['inputs']['queries'] if q['site_rva']==MASKS[0][3] and q['register']=='esi');q['candidates_truncated']=True
        self.assertFalse(composition(c['mask_shape'],c['shift_shape'],q)['unique_mask_to_shift_candidate'])
    def test_partial_width_unqualified(self):
        c=fixture()['mask_contexts'][0];c['mask_shape']['operands'][0]['width_bytes']=2;q=next(q for q in c['inputs']['queries'] if q['site_rva']==MASKS[0][3] and q['register']=='esi')
        self.assertEqual(composition(c['mask_shape'],c['shift_shape'],q)['kind'],'unqualified_composition')
    def test_opaque_store_source(self):
        w=fixture()['writer_inputs'];q=next(q for q in w['contexts'][0]['inputs']['queries'] if q['site_rva']==WRITER)
        self.assertEqual(q['reaching_candidates'],[dict(origin='unknown_call',rva=WRITER-5,semantic=None)])
    def test_no_direct_support_no_context_claim(self):
        dec=Decoder(b'\x90'*64,0x1000,BASE);d=discover_writer(dec,site=0x1030)
        self.assertEqual(d['selected_root_candidates'],[]);self.assertFalse(d['complete_indirect_callers_or_real_entries_proven'])
    def test_mid_instruction_target_excluded(self):
        raw=bytearray(b'\x90'*100);raw[:5]=b'\xe8'+struct.pack('<i',0x1022-0x1005);raw[32:37]=b'\xb8'+struct.pack('<I',128)
        d=discover_writer(Decoder(bytes(raw),0x1000,BASE),site=0x1050)
        self.assertEqual(d['caller_count'],1);self.assertEqual(d['selected_root_candidates'],[])
    def test_root_count_and_order(self):
        raw=bytearray(b'\x90'*100)
        for n,target in enumerate((0x1040,0x1042,0x1044,0x1046)):
            at=0x1000+5*n;raw[at-0x1000:at-0x1000+5]=b'\xe8'+struct.pack('<i',target-at-5)
        d=discover_writer(Decoder(bytes(raw),0x1000,BASE),site=0x1050)
        self.assertEqual([r['root_rva'] for r in d['selected_root_candidates']],[0x1046,0x1044,0x1042])
    def test_jump_not_caller_support(self):
        dec=Decoder(bytes.fromhex('eb02909090c3'),0x1000,BASE);d=discover_writer(dec,site=0x1004)
        self.assertEqual(d['caller_count'],0)
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R30Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_prior(self):self.reject(lambda d:d.update(r29_exact_report_sha256='wrong'))
    def test_mask_value(self):self.reject(lambda d:d['mask_contexts'][0]['composition'].update(mask=255))
    def test_shift_value(self):self.reject(lambda d:d['mask_contexts'][0]['composition'].update(left_shift_count=7))
    def test_result(self):self.reject(lambda d:d['mask_contexts'][0]['composition'].update(evaluated_original_result=128))
    def test_handle_role(self):self.reject(lambda d:d['mask_contexts'][0]['composition'].update(actual_index_range_or_handle_role_proven=True))
    def test_source_value(self):self.reject(lambda d:d['mask_contexts'][0]['inputs']['queries'][0].update(actual_register_value_known=True))
    def test_root_entry(self):self.reject(lambda d:d['writer_discovery']['selected_root_candidates'][0].update(actual_entry_proven=True))
    def test_root_alignment(self):self.reject(lambda d:d['writer_discovery']['selected_root_candidates'][0].update(full_linear_scan_boundary_candidate=False))
    def test_caller_target(self):self.reject(lambda d:d['writer_inputs']['contexts'][0]['caller_identity'].update(direct_target_rva=0))
    def test_complete_callers(self):self.reject(lambda d:d['writer_discovery'].update(complete_indirect_callers_or_real_entries_proven=True))
    def test_store_execution(self):self.reject(lambda d:d['writer_inputs']['store_candidate'].update(executed_write_proven=True))
    def test_store_global(self):self.reject(lambda d:d['writer_inputs']['store_candidate'].update(expected_global_rva=0))
    def test_store_owner(self):self.reject(lambda d:d['writer_inputs']['contexts'][0].update(actual_store_value_owner_or_initialization_proven=True))
    def test_unreachable_sources(self):self.reject(lambda d:d['writer_inputs']['contexts'][0].update(writer_site_in_candidate_graph=False))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
