import json,unittest
from tools.stoneage_tw10_savedata_frontier_r12_guard import validate
from tools.stoneage_tw10_savedata_frontier_r12 import SCHEMA,STATUS,ROOT,DELEGATE,CALL,QUERIES,GLOBALS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder

def fixture():
 return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'parent_nodes':50,'parent_edges':55,'structural_call_return_assumptions':1,
 'delegate_helper':summarize(Decoder(b'\xc3',DELEGATE,0x400000),DELEGATE),'input_queries':[{'site_rva':s,'register':r,'reaching_sources':[{'origin':'entry','rva':ROOT,'semantic':None}],'value_fully_known':False} for s,r in QUERIES],
 'call_identity':{'call_rva':CALL,'kind':'memory_indirect','register_target':None,'direct_target_rva':None,'memory_target':{'width_bytes':4,'base_register':None,'index_register':None,'index_scale':1,'segment_register':None,'relative_field_offset':None,'displacement_region':{'section':'.rdata','displacement_rva':0x53000,'raw_backed':True,'writable':False}},'import_identity':{'dll':'KERNEL32.dll','name':'TestImport','iat_rva':0x53000},'import_slot_association_proven':True,'runtime_target_or_effects_proven':False},
 'global_references':{'scope':'linear_text_decode_candidates_not_reachable_execution','decoded_instructions':40000,'decode_gap_bytes':0,'text_bytes':331776,'all_indirect_references_covered':False,'globals':[{'global_rva':r,'counts':{'read_candidate':1,'write_candidate':0,'address_candidate':0,'unknown_candidate':0},'samples':[{'rva':ROOT,'kind':'read_candidate'}],'samples_truncated':False,'runtime_initialization_proven':False} for r in GLOBALS]},**{k:False for k in FLAGS}}
class TestR12Guard(unittest.TestCase):
 def reject(self,d):
  with self.assertRaises(ValueError):validate(json.dumps(d))
 def test_valid_static_association(self):self.assertTrue(validate(json.dumps(fixture()))['import_slot_association_proven'])
 def test_promotions(self):
  for k in FLAGS:
   d=fixture();d[k]=True;self.reject(d)
 def test_unknown_payload(self):
  d=fixture();d['code']='original';self.reject(d)
 def test_wrong_source(self):
  d=fixture();d['runtime_sha256']='0'*64;self.reject(d)
 def test_false_import_flag(self):
  d=fixture();d['call_identity']['import_slot_association_proven']=False;self.reject(d)
 def test_segmented_iat_false_association(self):
  d=fixture();d['call_identity']['memory_target']['segment_register']='fs';self.reject(d)
 def test_based_iat_false_association(self):
  d=fixture();d['call_identity']['memory_target']['base_register']='eax';self.reject(d)
 def test_wrong_iat_region(self):
  d=fixture();d['call_identity']['import_identity']['iat_rva']+=4;self.reject(d)
 def test_runtime_target_promotion(self):
  d=fixture();d['call_identity']['runtime_target_or_effects_proven']=True;self.reject(d)
 def test_native_global_promotion(self):
  d=fixture();d['global_references']['globals'][0]['runtime_initialization_proven']=True;self.reject(d)
 def test_false_indirect_coverage(self):
  d=fixture();d['global_references']['all_indirect_references_covered']=True;self.reject(d)
 def test_missing_samples(self):
  d=fixture();d['global_references']['globals'][0]['samples']=[];self.reject(d)
 def test_false_truncation(self):
  d=fixture();d['global_references']['globals'][0]['samples_truncated']=True;self.reject(d)
 def test_wrong_global_order(self):
  d=fixture();d['global_references']['globals'].reverse();self.reject(d)
 def test_unmatched_slot_can_remain_unknown(self):
  d=fixture();d['call_identity'].update(import_identity=None,import_slot_association_proven=False);validate(json.dumps(d))
 def test_wrong_helper_root(self):
  d=fixture();d['delegate_helper']['root_rva']=ROOT;self.reject(d)
 def test_bad_scan_coverage(self):
  d=fixture();d['global_references']['decoded_instructions']=1;self.reject(d)
 def test_duplicate_json(self):
  s=json.dumps(fixture()).replace('"status":','"status":"native","status":',1)
  with self.assertRaises(ValueError):validate(s)
if __name__=='__main__':unittest.main()
