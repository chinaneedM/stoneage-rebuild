import json,unittest
from tools.stoneage_tw10_savedata_provenance_r10_guard import validate,FLAGS
from tools.stoneage_tw10_savedata_provenance_r10 import SCHEMA,STATUS,ROOT,STORE,DELEGATE,BRANCHES,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder

def fixture():
    unknown=[{'origin':'unknown_call','rva':ROOT+4,'semantic':None}]
    source=[{'origin':'definition','rva':ROOT+8,'semantic':{'kind':'comparison','register_inputs':['edi'],'memory_input':None,'constant':20,'width_bits':32}}]
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'parent_nodes':50,'parent_edges':55,
            'delegate_helper':summarize(Decoder(b'\xc3',DELEGATE,0x400000),DELEGATE),
            'provenance':{'structural_call_return_assumptions':1,'esi_at_store':{'store_rva':STORE,'conservative_sources':unknown,'syntax_candidates_ignoring_call_clobbers':[{'origin':'entry','rva':ROOT,'semantic':None}],'effective_target_proven':False},
            'loop_predicates':[{'branch_rva':rva,'condition':cond,'flag_sources':source,'unique_conditional_flag_definition':True,'runtime_branch_outcome_proven':False} for rva,cond in zip(BRANCHES,('je','je','jl'))]},**{k:False for k in FLAGS}}
class TestR10Guard(unittest.TestCase):
    def reject(self,d):
        with self.assertRaises(ValueError):validate(json.dumps(d))
    def test_valid_conditional_report(self):self.assertEqual(validate(json.dumps(fixture()))['loop_predicates'],3)
    def test_all_promotions(self):
        for k in FLAGS:
            d=fixture();d[k]=True;self.reject(d)
    def test_unknown_payload(self):
        d=fixture();d['bytes']='original';self.reject(d)
    def test_wrong_source(self):
        d=fixture();d['runtime_sha256']='0'*64;self.reject(d)
    def test_bad_graph(self):
        d=fixture();d['parent_nodes']=True;self.reject(d)
    def test_call_barrier_cannot_have_semantic(self):
        d=fixture();d['provenance']['esi_at_store']['conservative_sources'][0]['semantic']={};self.reject(d)
    def test_effective_target_promotion(self):
        d=fixture();d['provenance']['esi_at_store']['effective_target_proven']=True;self.reject(d)
    def test_missing_predicate(self):
        d=fixture();d['provenance']['loop_predicates'].pop();self.reject(d)
    def test_wrong_branch_condition(self):
        d=fixture();d['provenance']['loop_predicates'][0]['condition']='jne';self.reject(d)
    def test_duplicate_source(self):
        d=fixture();d['provenance']['loop_predicates'][0]['flag_sources']*=2;self.reject(d)
    def test_false_unique_claim(self):
        d=fixture();d['provenance']['loop_predicates'][0]['unique_conditional_flag_definition']=False;self.reject(d)
    def test_runtime_outcome(self):
        d=fixture();d['provenance']['loop_predicates'][0]['runtime_branch_outcome_proven']=True;self.reject(d)
    def test_bad_memory_geometry(self):
        d=fixture();d['provenance']['loop_predicates'][0]['flag_sources'][0]['semantic']['memory_input']={};self.reject(d)
    def test_wrong_helper_root(self):
        d=fixture();d['delegate_helper']['root_rva']=ROOT;self.reject(d)
    def test_false_helper_intersection(self):
        d=fixture();d['delegate_helper']['common_preserved_registers']=[];self.reject(d)
    def test_duplicate_json(self):
        s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
        with self.assertRaises(ValueError):validate(s)
if __name__=='__main__':unittest.main()
