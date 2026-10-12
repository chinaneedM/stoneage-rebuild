import copy
import json
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6_guard import validate,FLAGS
from tools.stoneage_tw10_savedata_dataflow_r6 import SCHEMA,STATUS,RUNTIME_SHA256,SAVEDATA_SHA256,WORD_RVAS

def fixture():
    p={'stop':'call','transfer_rva':0,'direct_target_rva':0x3000,'import_api':None,
       'filename_stack_slot':0,'stack_tracking_precise':True,'prefix_nodes':2}
    surface={'visited_states':3,'node_limit_hit':False,'depth_limit_stops':0,
             'unresolved_indirect_transfers':0,'api_events':[{'rva':0x3000,'api':'ReadFile','min_call_depth':0}]}
    sites=[]
    for word in WORD_RVAS:
        row={'word_rva':word,'push_rva':word-1,'first_transfer':copy.deepcopy(p),'cross_callee':copy.deepcopy(surface)}
        row['first_transfer']['transfer_rva']=word+4; sites.append(row)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,
            'savedata_sha256':SAVEDATA_SHA256,'sites':sites,**{k:False for k in FLAGS}}
class TestR6Guard(unittest.TestCase):
    def reject(self,r):
        with self.assertRaises(ValueError): validate(json.dumps(r))
    def test_valid(self): self.assertEqual(validate(json.dumps(fixture()))['api_events'],4)
    def test_native_promotions(self):
        for k in FLAGS:
            r=fixture(); r[k]=True; self.reject(r)
    def test_schema_and_payload(self):
        r=fixture(); r['bytes']='raw'; self.reject(r)
    def test_hash_identity(self):
        r=fixture(); r['runtime_sha256']='0'*64; self.reject(r)
    def test_wrong_site_and_boolean_rva(self):
        for v in (True,0x40066):
            r=fixture(); r['sites'][0]['word_rva']=v; self.reject(r)
    def test_duplicate_json_key(self):
        s=json.dumps(fixture()).replace('"schema":','"schema":"fake","schema":',1)
        with self.assertRaises(ValueError): validate(s)
    def test_unbounded_states(self):
        r=fixture(); r['sites'][0]['cross_callee']['visited_states']=4097; self.reject(r)
    def test_false_limit(self):
        r=fixture(); r['sites'][0]['cross_callee']['node_limit_hit']=True; self.reject(r)
    def test_api_and_event_duplicates(self):
        r=fixture(); r['sites'][0]['cross_callee']['api_events'][0]['api']='Unknown'; self.reject(r)
        r=fixture(); e=r['sites'][0]['cross_callee']['api_events']; e.append(copy.deepcopy(e[0])); self.reject(r)
    def test_stack_slot_consistency(self):
        for values in ({'filename_stack_slot':2},{'stack_tracking_precise':False},{'stop':'branch'}):
            r=fixture(); r['sites'][0]['first_transfer'].update(values); self.reject(r)
    def test_callee_required(self):
        r=fixture(); r['sites'][0]['cross_callee']=None; self.reject(r)
    def test_import_and_direct_exclusive(self):
        r=fixture(); r['sites'][0]['first_transfer']['import_api']='CreateFileA'; self.reject(r)
    def test_unknown_stack_and_no_callee(self):
        r=fixture()
        for s in r['sites']:
            s['first_transfer'].update(direct_target_rva=None,filename_stack_slot=None,stack_tracking_precise=False)
            s['cross_callee']=None
        self.assertEqual(validate(json.dumps(r))['api_events'],0)
    def test_oversized(self):
        with self.assertRaises(ValueError): validate(' '*24001)
if __name__=='__main__': unittest.main()
