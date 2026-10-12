import json,unittest,copy
from tools.stoneage_tw10_savedata_helper_original_r8_guard import validate,FLAGS,SCHEMA,STATUS,ROOT,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder

def fixture(code=b'\xc3'):
    h=summarize(Decoder(code,ROOT,0x400000),ROOT)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r7_caller_rva':0x4879a,'r7_verified_trace_states':136,'helper':h,**{k:False for k in FLAGS}}
class TestR8Guard(unittest.TestCase):
    def reject(self,d):
        with self.assertRaises(ValueError):validate(json.dumps(d))
    def test_valid_leaf_model_without_native_admission(self):
        v=validate(json.dumps(fixture()));self.assertTrue(v['qualifies_modeled_summary']);self.assertFalse(v['original_helper_resumption_admitted'])
    def test_valid_call_stop(self):
        v=validate(json.dumps(fixture(b'\xe8\x00\x00\x00\x00\xc3')));self.assertFalse(v['qualifies_modeled_summary']);self.assertEqual(v['gap_sites'],1)
    def test_history_promotions(self):
        for k in FLAGS:
            d=fixture();d[k]=True;self.reject(d)
        d=fixture();d['helper']['original_helper_accepted']=True;self.reject(d)
    def test_qualification_promotion(self):
        d=fixture(b'\xe8\x00\x00\x00\x00');d['helper']['qualifies_modeled_return_effect_summary']=True;self.reject(d)
    def test_unknown_payload(self):
        d=fixture();d['bytes']='original';self.reject(d)
    def test_hash(self):
        d=fixture();d['runtime_sha256']='0'*64;self.reject(d)
    def test_gap_count_mismatch(self):
        d=fixture(b'\xe8\x00\x00\x00\x00');d['helper']['gaps']['unsummarized_call']=2;self.reject(d)
    def test_duplicate_gap_and_return(self):
        d=fixture(b'\xe8\x00\x00\x00\x00');d['helper']['gap_sites']*=2;self.reject(d)
        d=fixture();d['helper']['return_paths']*=2;self.reject(d)
    def test_false_return_stack(self):
        d=fixture();d['helper']['return_paths'][0]['pre_ret_stack_delta']=4;self.reject(d)
    def test_false_register_intersection(self):
        d=fixture();d['helper']['common_preserved_registers']=[];self.reject(d)
    def test_cycle_prevents_summary(self):
        d=fixture();d['helper']['control_flow_cycle']=True;self.reject(d)
    def test_boolean_integer(self):
        d=fixture();d['helper']['visited_states']=True;self.reject(d)
    def test_duplicate_json_key(self):
        s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
        with self.assertRaises(ValueError):validate(s)
    def test_caller_write_gap_is_valid_nonqualification(self):
        v=validate(json.dumps(fixture(b'\x89\x44\x24\x04\xc3')));self.assertFalse(v['qualifies_modeled_summary'])
if __name__=='__main__':unittest.main()
