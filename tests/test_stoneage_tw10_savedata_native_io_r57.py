import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r57_guard import validate
P=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R57-ORIGINAL.json'
class PrimaryTests(unittest.TestCase):
 def setUp(self):self.d=json.loads(P.read_text())
 def bad(self):self.assertRaises((ValueError,KeyError),validate,self.d)
 def test_accept(self):self.assertTrue(validate(self.d))
 def test_missing_row(self):self.d['contexts'][0]['instruction_shapes'].pop();self.bad()
 def test_duplicate_row(self):self.d['contexts'][0]['instruction_shapes'].append(self.d['contexts'][0]['instruction_shapes'][-1]);self.bad()
 def test_edge_scope(self):self.d['contexts'][1]['bounded_edges'][0][1]=1;self.bad()
 def test_missing_call(self):self.d['contexts'][0]['call_contexts'].pop();self.bad()
 def test_promote(self):self.d['actual_native_write_count_close_flush_or_persistence_proven']=True;self.bad()
 def test_missing_entry_support(self):self.d['contexts'][1]['entrygraph_caller_edge_seen']=False;self.bad()
 def test_source_hash(self):self.d['r54_exact_original_report_sha256']='0'*64;self.bad()
 def test_source_forgery(self):self.d['contexts'][1]['return_analysis']['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates']=[];self.bad()
 def test_payload(self):self.d['raw_bytes']='abc';self.bad()
if __name__=='__main__':unittest.main()
