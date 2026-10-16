import copy
import unittest
from tools.stoneage_tw10_savedata_r77_handle_static import priors,inventory,inspect_verified
from tools.stoneage_tw10_savedata_r77_guard import validate,NEGATIVE

def fixture():
 old=priors();root=321787
 row={'site_rva':root,'mnemonic':'ret','operands':[],'decoder_read_registers':[],'decoder_written_registers':[],'input_query_registers':[],'actual_instruction_effect_or_value_known':False}
 # Invented API-shaped structural fixture; no original callee evidence.
 caller={'call_rva':313230,'kind':'direct','direct_target_rva':root,'runtime_target_or_effects_proven':False}
 return {'schema':'tw10-r77-original-static-bounded-handle-source','runtime_sha256':old['r75']['runtime_sha256'],'image_base':4194304,'root_rva':root,'source_git_blobs':{'r75':'757c22945d7e18263b154e88f52376d0ab58d42c','preflight':'79d6afabc9477f945de449b2265a62a76ff1733b'},'r75_exact_original_rederived_sha256':'bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85','caller_identity':caller,'call_candidates':[],**inventory([root],[],[],False,lambda n:row),**{k:False for k in NEGATIVE}}

class R77Tests(unittest.TestCase):
 def reject(self,f):
  d=fixture();f(d)
  with self.assertRaises(ValueError):validate(d)
 def test_invented_fixture_only(self):self.assertEqual(validate(fixture())['decoded_rows'],1)
 def test_false_boundaries(self):
  for k in NEGATIVE:
   with self.subTest(k=k):self.reject(lambda d:d.__setitem__(k,True))
 def test_missing_row(self):self.reject(lambda d:d['decoded_instruction_rows'].pop())
 def test_duplicate_node(self):self.reject(lambda d:d['bounded_graph_node_rvas'].append(321787))
 def test_disconnected_node(self):self.reject(lambda d:d['bounded_graph_node_rvas'].append(321788))
 def test_unknown_terminal(self):self.reject(lambda d:d['decoded_instruction_rows'][0].__setitem__('mnemonic','nop'))
 def test_missing_call_identity(self):self.reject(lambda d:d['decoded_instruction_rows'][0].__setitem__('mnemonic','call'))
 def test_incomplete_frontier(self):self.reject(lambda d:d['bounded_graph_frontier'].append('invented'))
 def test_incomplete_cap(self):self.reject(lambda d:d.__setitem__('bounded_graph_node_cap_hit',True))
 def test_bad_parent(self):self.reject(lambda d:d.__setitem__('r75_exact_original_rederived_sha256','0'*64))
 def test_wrong_caller(self):self.reject(lambda d:d['caller_identity'].__setitem__('direct_target_rva',313683))
 def test_raw_nested(self):self.reject(lambda d:d['decoded_instruction_rows'][0]['operands'].append({'original_payload':'invented'}))
 def test_wrong_pin(self):self.reject(lambda d:d['source_git_blobs'].__setitem__('r75','0'*40))
 def test_bad_edge(self):self.reject(lambda d:d['bounded_graph_edges'].append([321787,999999]))
 def test_inventory_refuses_incomplete(self):
  with self.assertRaises(ValueError):inventory([321787],[],['gap'],False,lambda n:{})
 def test_hash_before_decoder(self):
  with self.assertRaisesRegex(ValueError,'original runtime SHA256'):inspect_verified(b'invented')
if __name__=='__main__':unittest.main()
