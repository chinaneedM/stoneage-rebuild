"""R63 synthetic structural controls; never treat a fake instruction as original."""
import unittest
from tools.stoneage_tw10_savedata_r63_postcall_static import window

class R63Window(unittest.TestCase):
    def setUp(self):
        self.call=0x4C68C
        self.post=0x4C692
        self.nodes={self.call:object(),self.post:object(),0x4C694:object(),0x4C698:object()}
        self.edges={(self.call,self.post),(self.post,0x4C694),(0x4C694,0x4C698)}
    def row(self,at):
        return {"site_rva":at,"mnemonic":"call" if at==self.call else "test",
                "operands":[{"kind":"register","register":"eax"}],
                "actual_instruction_effect_or_value_known":False}
    def test_valid_window_is_nonexecuting(self):
        x=window(self.nodes,self.edges,self.call,self.post,self.row)
        self.assertEqual(x["postcall_instruction"]["site_rva"],self.post)
        self.assertEqual(len(x["decoded_instruction_rows"]),4)
        self.assertEqual(x["bounded_local_edges"][0],[self.call,self.post])
        self.assertFalse(x["actual_eax_return_register_value_proven"])
        self.assertFalse(x["actual_flags_or_branch_feasibility_proven"])
    def test_missing_postcall_rejected(self):
        nodes=dict(self.nodes)
        nodes.pop(self.post)
        with self.assertRaises(ValueError):
            window(nodes,self.edges,self.call,self.post,self.row)
    def test_missing_call_fallthrough_edge_rejected(self):
        edges=set(self.edges)
        edges.remove((self.call,self.post))
        with self.assertRaises(ValueError):
            window(self.nodes,edges,self.call,self.post,self.row)
    def test_false_effect_promotion_rejected(self):
        def forged(at):
            r=self.row(at)
            r["actual_instruction_effect_or_value_known"]=at==self.post
            return r
        with self.assertRaises(ValueError):
            window(self.nodes,self.edges,self.call,self.post,forged)
    def test_original_binary_content_rejected(self):
        def forged(at):
            r=self.row(at)
            r["bytes"]=b"\x90"
            return r
        with self.assertRaises(ValueError):
            window(self.nodes,self.edges,self.call,self.post,forged)
    def test_incomplete_rows_rejected(self):
        def forged(at):
            r=self.row(at)
            if at==self.post:
                r.pop("operands")
            return r
        with self.assertRaises((ValueError,KeyError)):
            window(self.nodes,self.edges,self.call,self.post,forged)
    def test_upper_row_cap_rejected(self):
        nodes={self.call:object(),self.post:object()}
        for i in range(50):
            nodes[self.call-32+i]=object()
        with self.assertRaises(ValueError):
            window(nodes,self.edges,self.call,self.post,self.row)
    def test_address_bounds_exclude_unrelated_code(self):
        nodes=dict(self.nodes)
        nodes[0x50000]=object()
        x=window(nodes,self.edges,self.call,self.post,self.row)
        self.assertEqual(len(x["decoded_instruction_rows"]),4)

if __name__=="__main__":
    unittest.main()
