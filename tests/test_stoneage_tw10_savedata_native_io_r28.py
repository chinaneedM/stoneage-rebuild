"""Invented bounded CALL/CFG/register controls; no original runtime evidence."""
import struct,unittest
from tools.stoneage_tw10_savedata_native_io_r28 import *
from tools.stoneage_tw10_savedata_native_io_r28_guard import validate
BASE=0x400000

def fixture():
    lo=min(c for _,c,_,_ in CONTEXTS);hi=CONTEXTS[0][3][0]+16;raw=bytearray(b'\x90'*(hi-lo))
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    def jump(at,dst):put(at,b'\xe9'+struct.pack('<i',dst-at-5))
    sections=[dict(name='.idata',rva=0x52000,vsize=4096,raw_size=4096,raw=0,characteristics=0x40000040)]
    imports={BASE+0x52000+i*4:('KERNEL32.dll',c[0]) for i,c in enumerate(CONTEXTS)}
    prior={'nearby_direct_callers':{'samples':[]},'selected_api_details':[]}
    for index,(api,caller,root,sites) in enumerate(CONTEXTS):
        put(caller,b'\xe8'+struct.pack('<i',root-caller-5));jump(root,sites[0]-6)
        prior['nearby_direct_callers']['samples'].append(dict(site_rva=caller,target_rva=root))
        for n,at in enumerate(sites):
            put(at-6,b'\xb8'+struct.pack('<I',128));put(at-1,b'\x50')
            put(at,b'\xff\x15'+struct.pack('<I',BASE+0x52000+index*4))
            if n+1<len(sites):jump(at+6,sites[n+1]-6)
            else:put(at+6,b'\xc3')
            prior['selected_api_details'].append(dict(api=api,site_rva=at,linear_anchor_rva=at-6,
                suffix={'pushes':[dict(site_rva=at-1,conditional_pre_call_esp_offset=0,input=dict(kind='register',register='eax',width_bytes=4))]},
                registers_before_call={'eax':{'query_site_in_candidate_graph':False}}))
    dec=Decoder(bytes(raw),lo,BASE)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r27_exact_original_revalidated=True,r27_exact_report_sha256=PRIOR_SHA256,static_only=True,
                contexts=[context(dec,sections,imports,prior,*r) for r in CONTEXTS],
                third_writefile_and_early_createfile_detail_deferred=True,**{k:False for k in FLAGS})

class R28Synthetic(unittest.TestCase):
    def test_valid_fixture(self):self.assertTrue(validate(fixture()))
    def test_create_call_reached_beyond_old_span(self):
        c=fixture()['contexts'][0];self.assertGreater(c['api_sites'][0]['site_rva']-c['root_candidate_rva'],384)
        self.assertTrue(c['api_sites'][0]['site_in_candidate_graph'])
    def test_write_second_reached_from_call_root(self):
        c=fixture()['contexts'][2];self.assertFalse(c['api_sites'][1]['prior_graph_site_reached'])
        self.assertTrue(c['api_sites'][1]['site_in_candidate_graph'])
    def test_opaque_api_return(self):
        c=fixture()['contexts'][0];at=c['api_sites'][0]['conditional_post_call_rva']
        q=next(q for q in c['inputs']['queries'] if q['site_rva']==at and q['register']=='eax')
        self.assertEqual(q['reaching_candidates'],[dict(origin='unknown_call',rva=at-6,semantic=None)])
    def test_ret_blocks_reach(self):
        dec=Decoder(bytes.fromhex('c39090'),0x1000,BASE);nodes,edges,_,_=candidate_graph(dec,0x1000)
        q=input_surface(dec,[],nodes,edges,0x1000,[(0x1002,'eax')])['queries'][0]
        self.assertFalse(q['site_in_candidate_graph']);self.assertEqual(q['reaching_candidates'],[])
    def test_backward_external_edge(self):
        dec=Decoder(bytes.fromhex('ebfc'),0x1000,BASE);_,_,f,_=candidate_graph(dec,0x1000)
        self.assertIn(('out_of_window',0xffe),f)
    def test_node_cap(self):
        nodes,_,f,hit=candidate_graph(Decoder(b'\x90'*20,0x1000,BASE),0x1000,cap=3)
        self.assertEqual(len(nodes),3);self.assertTrue(hit);self.assertIn(('node_cap',3),f)
    def test_explicit_span_cap(self):
        with self.assertRaises(ValueError):candidate_graph(Decoder(b'\x90',0x1000,BASE),0x1000,span=769)
    def test_indirect_jump_barrier(self):
        _,_,f,_=candidate_graph(Decoder(bytes.fromhex('ffe090'),0x1000,BASE),0x1000)
        self.assertIn(('indirect_jump',0x1000),f)
    def test_dependency_memory_base(self):
        dec=Decoder(bytes.fromhex('b98000000089c88b0050c3'),0x1000,BASE);nodes,edges,_,_=candidate_graph(dec,0x1000)
        s=input_surface(dec,[],nodes,edges,0x1000,[(0x1009,'eax')]);q=next(q for q in s['queries'] if q['site_rva']==0x1009)
        self.assertEqual(q['dependency_queries'],[dict(site_rva=0x1007,register='eax')])
        self.assertTrue(any(q['dependency_depth']==2 and q['register']=='ecx' for q in s['queries']))
    def test_dependency_depth_bound(self):
        self.assertEqual(fixture()['contexts'][0]['inputs']['dependency_depth_limit'],2)
    def test_dependencies_exclude_esp_segment(self):self.assertEqual(dependencies({'register_inputs':['esp'],'memory_input':{'base_register':'ebp','index_register':'esi','segment_register':'fs'}}),['ebp','esi'])
    def test_register_query_cap(self):
        dec=Decoder(b'\x90'*100,0x1000,BASE);nodes,edges,_,_=candidate_graph(dec,0x1000)
        s=input_surface(dec,[],nodes,edges,0x1000,[(0x1000+n,'eax') for n in range(100)])
        self.assertEqual(len(s['queries']),64);self.assertTrue(s['query_limit_hit'])
    def test_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R28Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_prior(self):self.reject(lambda d:d.update(r27_exact_report_sha256='wrong'))
    def test_caller_target(self):self.reject(lambda d:d['contexts'][0]['caller_identity'].update(direct_target_rva=0))
    def test_entry(self):self.reject(lambda d:d['contexts'][0].update(entry_or_call_execution_proven=True))
    def test_graph_span(self):self.reject(lambda d:d['contexts'][0]['graph'].update(span_bytes=1024))
    def test_call_return(self):self.reject(lambda d:d['contexts'][0]['graph'].update(call_fallthrough_structural_only=False))
    def test_value(self):self.reject(lambda d:d['contexts'][0]['inputs']['queries'][0].update(actual_register_value_known=True))
    def test_memory_closure(self):self.reject(lambda d:d['contexts'][0]['inputs'].update(dependency_closure_or_memory_values_proven=True))
    def test_missing_call_query(self):self.reject(lambda d:d['contexts'][0]['inputs'].update(queries=[]))
    def test_offset(self):self.reject(lambda d:d['contexts'][0]['api_sites'][0]['push_candidates'][0].update(conditional_pre_call_esp_offset=4))
    def test_role(self):self.reject(lambda d:d['contexts'][0]['api_sites'][0]['push_candidates'][0].update(actual_argument_value_or_role_proven=True))
    def test_api_name(self):self.reject(lambda d:d['contexts'][0]['api_sites'][0]['identity']['import_identity'].update(name='ReadFile'))
    def test_external_return(self):self.reject(lambda d:d['contexts'][0]['api_sites'][0].update(actual_external_return_proven=True))
    def test_opaque_semantic(self):
        def edit(d):
            qs=d['contexts'][0]['inputs']['queries'];q=next(q for q in qs if q['reaching_candidates'] and q['reaching_candidates'][0]['origin']=='entry');q['reaching_candidates'][0]['semantic']={}
        self.reject(edit)
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
