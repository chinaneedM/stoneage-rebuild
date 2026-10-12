import json,struct,unittest
from tools.stoneage_tw10_savedata_helper_frontier_r9_guard import validate,FLAGS
from tools.stoneage_tw10_savedata_helper_frontier_r9 import SCHEMA,STATUS,ROOT,NESTED,STORE,RUNTIME_SHA256,SAVEDATA_SHA256,structural_surface,store_geometry
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder

def fixture():
    section=[{'name':'.data','rva':0x60000,'raw_size':16,'vsize':256,'characteristics':0x80000000}]
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'r8_verified_helper_states':44,
            'nested_helper':summarize(Decoder(b'\xc3',NESTED,0x400000),NESTED),
            'store':store_geometry(Decoder(b'\x89\x04\x9d'+struct.pack('<I',0x460008),STORE,0x400000),STORE,section),
            'structural_parent':structural_surface(Decoder(b'\x90\x75\xfd\xc3',ROOT,0x400000),ROOT),**{k:False for k in FLAGS}}
class TestR9Guard(unittest.TestCase):
    def reject(self,d):
        with self.assertRaises(ValueError):validate(json.dumps(d))
    def test_valid_indexed_store_and_conditional_loop(self):
        r=validate(json.dumps(fixture()));self.assertFalse(r['store_absolute_address_known']);self.assertEqual(r['structural_loops'],1);self.assertFalse(r['native_io_executed'])
    def test_promotions(self):
        for k in FLAGS:
            d=fixture();d[k]=True;self.reject(d)
    def test_unknown_payload(self):
        d=fixture();d['code']='original';self.reject(d)
    def test_wrong_source(self):
        d=fixture();d['runtime_sha256']='0'*64;self.reject(d)
    def test_indexed_address_not_fully_known(self):
        d=fixture();d['store']['effective_address_fully_known']=True;self.reject(d)
    def test_ownership_not_admitted(self):
        d=fixture();d['store']['table_or_object_ownership_proven']=True;self.reject(d)
    def test_false_topology_runtime(self):
        d=fixture();d['structural_parent']['runtime_loop_conditions_proven']=True;self.reject(d)
    def test_duplicate_loop(self):
        d=fixture();d['structural_parent']['loops']*=2;self.reject(d)
    def test_bad_condition(self):
        d=fixture();d['structural_parent']['loops'][0]['conditional_branches'][0]['condition']='runtime_true';self.reject(d)
    def test_bad_gap_counts(self):
        d=fixture();d['nested_helper']['gaps']['unsummarized_call']=1;self.reject(d)
    def test_false_register_intersection(self):
        d=fixture();d['nested_helper']['common_preserved_registers']=[];self.reject(d)
    def test_boolean_count(self):
        d=fixture();d['structural_parent']['nodes']=True;self.reject(d)
    def test_duplicate_json(self):
        s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
        with self.assertRaises(ValueError):validate(s)
if __name__=='__main__':unittest.main()
