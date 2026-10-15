import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_writer_r54_audit import validate
P=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R54-ORIGINAL.json'
class AuditTests(unittest.TestCase):
    def setUp(self):self.d=json.loads(P.read_text())
    def test_accept(self):self.assertEqual(validate(self.d),201)
    def reject(self):self.assertRaises((ValueError,KeyError),validate,self.d)
    def test_false_entry_edge(self):self.d['normalization_call_edge_seen']=False;self.reject()
    def test_missing_original_support(self):self.d['prefix_direct_callee_contexts'][1]['entrygraph_call_edge_seen']=False;self.reject()
    def test_claim_inverse(self):self.d['actual_writer_inverse_proven']=True;self.reject()
    def test_missing_row(self):self.d['writer_context']['instruction_shapes'].pop();self.reject()
    def test_missing_call(self):self.d['writer_context']['call_contexts'].pop();self.reject()
    def test_edge_scope(self):self.d['writer_context']['bounded_edges'][0][1]=1;self.reject()
    def test_processor_target(self):self.d['prefix_direct_callee_contexts'][1]['root_candidate_rva']+=1;self.reject()
    def test_forged_stack(self):self.d['conditional_writer_analysis']['processor_surfaces'][1]['return_candidates'][0]['conditional_stack_delta_before_ret']=4;self.reject()
    def test_payload(self):self.d['raw_bytes']='abc';self.reject()
    def test_unreported_frontier(self):self.d['writer_context']['graph']['frontier']=[{'reason':'decode_gap','rva':0x40020}];self.reject()
    def test_normalization(self):self.d['normalization_shapes'][0]['mnemonic']='xor';self.reject()
if __name__=='__main__':unittest.main()
