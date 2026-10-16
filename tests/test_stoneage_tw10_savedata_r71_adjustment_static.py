"""Invented placeholders cannot qualify source semantics; custody is separate."""
import copy
import unittest
from tools.stoneage_tw10_savedata_r71_adjustment_static import priors,retained_rows,selection,inspect_verified
from tools.stoneage_tw10_savedata_r71_guard import validate,PINS,NEGATIVE

def fixture():
 old=priors();g=old['r69'];known=retained_rows([old[k]for k in ('r44','r45','r63','r69')])
 def row(n):
  r=copy.deepcopy(known.get(n,{'site_rva':n,'mnemonic':'nop','operands':[],'decoder_read_registers':[],'decoder_written_registers':[]}))
  r.update(actual_instruction_effect_or_value_known=False,input_query_registers=[]);return r
 return {'schema':'tw10-r71-original-static-adjustment-loop-neighborhood','runtime_sha256':g['runtime_sha256'],'image_base':4194304,'root_rva':312756,'source_git_blobs':{k:v[1]for k,v in PINS.items()},'r69_exact_original_rederived_sha256':'26ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe','bounded_graph_node_rvas':g['bounded_graph_node_rvas'],'bounded_graph_edges':g['bounded_graph_edges'],'bounded_graph_frontier':[],'bounded_graph_node_cap_hit':False,'previously_missing_selected_sites':old['preflight']['selected_missing_decoded_sites'],**selection(g['bounded_graph_node_rvas'],[tuple(e)for e in g['bounded_graph_edges']],row),**{k:False for k in NEGATIVE}}

class R71Tests(unittest.TestCase):
 def reject(self,f):
  d=fixture();f(d)
  with self.assertRaises(ValueError):validate(d)
 def test_invented_fixture_bounded_only(self):self.assertEqual(validate(fixture())['decoded_rows'],29)
 def test_nonpromotion(self):
  for k in NEGATIVE:
   with self.subTest(k=k):self.reject(lambda d:d.__setitem__(k,True))
 def test_missing_operand(self):self.reject(lambda d:d['decoded_instruction_rows'].pop())
 def test_changed_graph(self):self.reject(lambda d:d['bounded_graph_edges'].pop())
 def test_changed_focus(self):self.reject(lambda d:d['focus_node_rvas'].pop())
 def test_changed_incidence(self):self.reject(lambda d:d['focus_predecessors'].__setitem__('312915',[]))
 def test_wrong_prior_gap(self):self.reject(lambda d:d['previously_missing_selected_sites'].pop())
 def test_bad_source_pin(self):self.reject(lambda d:d['source_git_blobs'].__setitem__('r44','0'*40))
 def test_original_overlap_mutation(self):
  self.reject(lambda d:next(r for r in d['decoded_instruction_rows']if r['site_rva']==0x4c653).__setitem__('mnemonic','dec'))
 def test_raw_nested(self):self.reject(lambda d:d['decoded_instruction_rows'][0]['operands'].append({'raw_binary':'invented'}))
 def test_runtime_hash_before_decoder(self):
  with self.assertRaisesRegex(ValueError,'original runtime SHA256'):inspect_verified(b'invented')
 def test_retained_conflict(self):
  a={'site_rva':1,'mnemonic':'nop','operands':[],'decoder_read_registers':[],'decoder_written_registers':[]};b=copy.deepcopy(a);b['mnemonic']='ret'
  with self.assertRaisesRegex(ValueError,'overlapping'):retained_rows([a,b])

if __name__=='__main__':unittest.main()
