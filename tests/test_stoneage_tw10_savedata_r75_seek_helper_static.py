import copy
import unittest
from tools.stoneage_tw10_savedata_r75_seek_helper_static import priors,selection,inspect_verified
from tools.stoneage_tw10_savedata_r73_modes_static import retained_rows
from tools.stoneage_tw10_savedata_r75_guard import PINS,NEGATIVE,validate

def fixture():
 old=priors();g=old['r46']['write_helper_context'];known=retained_rows([old['r46'],old['r37']])
 def row(n):
  r=copy.deepcopy(known.get(n,{'site_rva':n,'mnemonic':'nop','operands':[],'decoder_read_registers':[],'decoder_written_registers':[]}));r.update(actual_instruction_effect_or_value_known=False,input_query_registers=[]);return r
 return {'schema':'tw10-r75-original-static-bounded-seek-helper-effects','runtime_sha256':old['r73']['runtime_sha256'],'image_base':4194304,'root_rva':313185,'source_git_blobs':{k:v[1]for k,v in PINS.items()},'r73_exact_original_rederived_sha256':'5cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d','r46_r37_helper_surface_exactly_revalidated':True,'bounded_graph_node_rvas':g['bounded_node_rvas'],'bounded_graph_edges':g['bounded_edges'],'bounded_graph_frontier':[],'bounded_graph_node_cap_hit':False,'previously_missing_selected_sites':old['preflight']['missing_decoded_node_rvas'],**selection(g['bounded_node_rvas'],[tuple(e)for e in g['bounded_edges']],row),**{k:False for k in NEGATIVE}}

class R75Tests(unittest.TestCase):
 def reject(self,f):
  d=fixture();f(d)
  with self.assertRaises(ValueError):validate(d)
 def test_invented_fixture_only_inventory(self):self.assertEqual(validate(fixture())['decoded_rows'],51)
 def test_false_flags(self):
  for k in NEGATIVE:
   with self.subTest(k=k):self.reject(lambda d:d.__setitem__(k,True))
 def test_missing_exit(self):self.reject(lambda d:d['decoded_instruction_rows'].pop())
 def test_changed_graph(self):self.reject(lambda d:d['bounded_graph_edges'].pop())
 def test_changed_entry(self):self.reject(lambda d:d['decoded_instruction_rows'][0].__setitem__('mnemonic','xor'))
 def test_missing_effect_node(self):self.reject(lambda d:d['selected_node_rvas'].pop())
 def test_bad_parent_digest(self):self.reject(lambda d:d.__setitem__('r73_exact_original_rederived_sha256','0'*64))
 def test_false_surface_replay(self):self.reject(lambda d:d.__setitem__('r46_r37_helper_surface_exactly_revalidated',False))
 def test_prior_gap_changed(self):self.reject(lambda d:d['previously_missing_selected_sites'].pop())
 def test_payload_in_nested_operand(self):self.reject(lambda d:d['decoded_instruction_rows'][0]['operands'].append({'original_payload':'invented'}))
 def test_bad_prior_blob(self):self.reject(lambda d:d['source_git_blobs'].__setitem__('r46','0'*40))
 def test_hash_before_decoder(self):
  with self.assertRaisesRegex(ValueError,'original runtime SHA256'):inspect_verified(b'invented')
if __name__=='__main__':unittest.main()
