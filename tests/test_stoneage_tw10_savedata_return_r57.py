import copy,unittest
from tools.stoneage_tw10_savedata_return_r57 import analyze

def row(a,m='nop',writes=(),reads=(),ops=None):return {'site_rva':a,'mnemonic':m,'decoder_written_registers':list(writes),'decoder_read_registers':list(reads),'operands':ops or []}
def c(rows,edges):return {'instruction_shapes':rows,'bounded_edges':edges,'root_candidate_rva':rows[0]['site_rva'],'bounded_node_rvas':[r['site_rva'] for r in rows]}
def sources(d):return d['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates']
class ReturnTests(unittest.TestCase):
 def test_direct_definition(self):self.assertEqual(sources(analyze(c([row(10,'mov',('eax',)),row(11,'ret')],[[10,11]]))),[{'origin':'definition','site_rva':10}])
 def test_opaque_call(self):self.assertEqual(sources(analyze(c([row(10,'call'),row(11,'ret')],[[10,11]]))),[{'origin':'unknown_call','site_rva':10}])
 def test_entry(self):self.assertEqual(sources(analyze(c([row(10,'ret')],[]))),[{'origin':'entry','site_rva':10}])
 def test_missing_inventory(self):
  d=c([row(10,'ret')],[]);d['bounded_node_rvas']=[11];self.assertRaises(ValueError,analyze,d)
 def test_bad_edge(self):self.assertRaises(ValueError,analyze,c([row(10,'ret')],[[10,11]]))
 def test_division_retained(self):self.assertEqual(len(analyze(c([row(10,'div',('eax','edx')),row(11,'ret')],[[10,11]]))['division_shapes']),1)
 def test_write_barrier(self):
  r=row(10,'mov',ops=[{'kind':'memory','decoder_write':True,'geometry':{}}]);self.assertEqual(len(analyze(c([r,row(11,'ret')],[[10,11]]))['explicit_memory_write_shapes']),1)
 def test_no_value_promotion(self):self.assertFalse(analyze(c([row(10,'ret')],[]))['actual_written_count_close_flush_or_persistence_proven'])
if __name__=='__main__':unittest.main()
