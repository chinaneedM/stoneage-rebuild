import copy,json,unittest
from tools.stoneage_tw10_savedata_argtrace_r7_guard import validate,FLAGS,SCHEMA,STATUS,RUNTIME_SHA256,SAVEDATA_SHA256,SEED

def fixture():
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'seed_callee_rva':0x487ba,'seed':SEED,**{k:False for k in FLAGS},
            'trace':{'visited_states':10,'state_limit_hit':False,'gaps':{'call_return_summary_missing':1},
                     'calls':[{'rva':0x487ba,'target_rva':0x48800,'depth':0,'filename_stack_slots':[0]}],
                     'api_candidates':[],'CreateFileA_filename_slot0_candidate':False}}
class TestR7Guard(unittest.TestCase):
    def reject(self,d):
        with self.assertRaises(ValueError):validate(json.dumps(d))
    def test_valid(self): self.assertEqual(validate(json.dumps(fixture()))['calls'],1)
    def test_promotions(self):
        for k in FLAGS:
            d=fixture();d[k]=True;self.reject(d)
    def test_source_hash(self):
        d=fixture();d['savedata_sha256']='0'*64;self.reject(d)
    def test_unknown_payload(self):
        d=fixture();d['trace']['bytes']='raw';self.reject(d)
    def test_cap(self):
        d=fixture();d['trace']['visited_states']=2049;self.reject(d)
        d=fixture();d['trace']['state_limit_hit']=True;self.reject(d)
    def test_boolean_address(self):
        d=fixture();d['trace']['calls'][0]['rva']=True;self.reject(d)
    def test_slots_duplicates_bounds(self):
        for s in ([0,0],[16],[-1],[True],[2,1]):
            d=fixture();d['trace']['calls'][0]['filename_stack_slots']=s;self.reject(d)
    def test_duplicate_call(self):
        d=fixture();d['trace']['calls']*=2;self.reject(d)
    def test_unknown_gap(self):
        d=fixture();d['trace']['gaps']['proved_runtime']=1;self.reject(d)
    def test_false_api_promotion(self):
        d=fixture();d['trace']['CreateFileA_filename_slot0_candidate']=True;self.reject(d)
    def test_conditional_api_only(self):
        d=fixture();d['trace']['api_candidates']=[{'rva':0x4ed01,'api':'CreateFileA','depth':3,'filename_stack_slots':[0]}]
        d['trace']['CreateFileA_filename_slot0_candidate']=True
        v=validate(json.dumps(d));self.assertTrue(v['conditional_CreateFileA_filename_candidate']);self.assertFalse(v['complete_filename_api_link_proven'])
    def test_duplicate_json(self):
        s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
        with self.assertRaises(ValueError):validate(s)
    def test_oversized(self):
        with self.assertRaises(ValueError):validate(' '*24001)
if __name__=='__main__':unittest.main()
