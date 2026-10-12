import json,unittest
from tools.stoneage_tw10_savedata_inputs_r11_guard import validate
from tools.stoneage_tw10_savedata_inputs_r11 import SCHEMA,STATUS,ROOT,DELEGATE,QUERIES,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder

def fixture():
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'parent_nodes':50,'parent_edges':55,'structural_call_return_assumptions':1,
            'delegate_helper':summarize(Decoder(b'\xc3',DELEGATE,0x400000),DELEGATE),
            'input_queries':[{'site_rva':site,'register':reg,'reaching_sources':[{'origin':'entry','rva':ROOT,'semantic':None}],'value_fully_known':False} for site,reg in QUERIES],**{k:False for k in FLAGS}}
class TestR11Guard(unittest.TestCase):
    def reject(self,d):
        with self.assertRaises(ValueError):validate(json.dumps(d))
    def test_valid_unresolved_inputs(self):self.assertEqual(validate(json.dumps(fixture()))['input_queries'],8)
    def test_every_promotion(self):
        for k in FLAGS:
            d=fixture();d[k]=True;self.reject(d)
    def test_unknown_payload(self):
        d=fixture();d['bytes']='original';self.reject(d)
    def test_wrong_source_hash(self):
        d=fixture();d['savedata_sha256']='0'*64;self.reject(d)
    def test_reordered_query(self):
        d=fixture();d['input_queries'].reverse();self.reject(d)
    def test_missing_query(self):
        d=fixture();d['input_queries'].pop();self.reject(d)
    def test_full_value_promotion(self):
        d=fixture();d['input_queries'][0]['value_fully_known']=True;self.reject(d)
    def test_call_barrier_semantic(self):
        d=fixture();s=d['input_queries'][0]['reaching_sources'][0];s.update(origin='unknown_call',semantic={});self.reject(d)
    def test_duplicate_source(self):
        d=fixture();d['input_queries'][0]['reaching_sources']*=2;self.reject(d)
    def test_wrong_register_increment(self):
        d=fixture();s=d['input_queries'][0]['reaching_sources'][0];s.update(origin='definition',semantic={'kind':'register_offset_adjustment','register_inputs':['eax'],'memory_input':None,'constant':1,'width_bits':32});self.reject(d)
    def test_valid_ebx_increment(self):
        d=fixture();s=d['input_queries'][0]['reaching_sources'][0];s.update(origin='definition',semantic={'kind':'register_offset_adjustment','register_inputs':['ebx'],'memory_input':None,'constant':1,'width_bits':32});validate(json.dumps(d))
    def test_false_helper_qualification(self):
        d=fixture();d['delegate_helper']['qualifies_modeled_return_effect_summary']=False;self.reject(d)
    def test_wrong_helper_root(self):
        d=fixture();d['delegate_helper']['root_rva']=ROOT;self.reject(d)
    def test_boolean_count(self):
        d=fixture();d['parent_nodes']=True;self.reject(d)
    def test_duplicate_json_key(self):
        s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
        with self.assertRaises(ValueError):validate(s)
if __name__=='__main__':unittest.main()
