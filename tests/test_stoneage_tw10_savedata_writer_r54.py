import copy,unittest
from tools.stoneage_tw10_savedata_writer_r54 import analyze

def row(a,m='nop',ops=None,writes=None):
    return {'site_rva':a,'mnemonic':m,'operands':ops or [],'decoder_written_registers':writes or []}
def fixture():
    call={'site_rva':0x40022,'identity':{'direct_target_rva':0x47000},'physical_push_suffix':{'pushes':[]}}
    c={'root_candidate_rva':0x40020,'instruction_shapes':[row(0x40020),row(0x40022,'call'),row(0x40027,'ret')],'bounded_node_rvas':[0x40020,0x40022,0x40027],'bounded_edges':[[0x40020,0x40022],[0x40022,0x40027]],'call_contexts':[call]}
    p={'caller_site_rva':0x40022,'root_candidate_rva':0x47000,'instruction_shapes':[row(0x47000,'ret')],'bounded_node_rvas':[0x47000],'bounded_edges':[]}
    return c,[p]
class WriterTests(unittest.TestCase):
    def test_normal_ret_and_opaque_caller(self):
        c,p=fixture();r=analyze(c,p);self.assertEqual(r['processor_surfaces'][0]['return_candidates'][0]['conditional_stack_delta_before_ret'],0);self.assertFalse(r['historical_writer_equals_r53_invented_inverse_proven'])
    def test_inventory_missing(self):
        c,p=fixture();c['instruction_shapes'].pop();self.assertRaises(ValueError,analyze,c,p)
    def test_call_missing(self):
        c,p=fixture();c['call_contexts']=[];self.assertRaises(ValueError,analyze,c,p)
    def test_target_substitution(self):
        c,p=fixture();p[0]['root_candidate_rva']+=1;self.assertRaises(ValueError,analyze,c,p)
    def test_duplicate(self):
        c,p=fixture();p.append(copy.deepcopy(p[0]));self.assertRaises(ValueError,analyze,c,p)
    def test_processor_missing(self):
        c,p=fixture();p[0]['instruction_shapes']=[];self.assertRaises(ValueError,analyze,c,p)
    def test_edge_outside(self):
        c,p=fixture();p[0]['bounded_edges']=[[0x47000,0x47001]];self.assertRaises(ValueError,analyze,c,p)
    def test_stack_push(self):
        c,p=fixture();r=p[0];r['instruction_shapes']=[row(0x47000,'push',[{'kind':'register','register':'ebx','width_bytes':4}]),row(0x47001,'ret')];r['bounded_node_rvas']=[0x47000,0x47001];r['bounded_edges']=[[0x47000,0x47001]]
        self.assertEqual(analyze(c,p)['processor_surfaces'][0]['return_candidates'][0]['conditional_stack_delta_before_ret'],-4)
if __name__=='__main__':unittest.main()
