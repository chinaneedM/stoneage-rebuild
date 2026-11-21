import unittest
from tools.stoneage_pet126q_cn50_helper_forward import (
    FORWARD,bounded_entry,check_forward,core_prefix
)
def synthetic(base,ins):
    return [{"address":base+i,"instruction":op} for i,op in enumerate(ins)]
class PET126Q(unittest.TestCase):
    def test_exact_bounded_forwarding(self):
        for _,(entry,target,pushes) in FORWARD.items():
            src=synthetic(entry,["nop",*pushes,"call   "+hex(target),"ret"])
            v=check_forward(src,entry,target,pushes)
            self.assertTrue(v["first_return_found"])
            self.assertFalse(v["C_runtime_symbol_proven"])
    def test_mismatched_target_or_argument_rejected(self):
        entry,target,pushes=FORWARD["read"]
        with self.assertRaises(ValueError):
            check_forward(synthetic(entry,[*pushes,"call   "+hex(target+1),"ret"]),entry,target,pushes)
        with self.assertRaises(ValueError):
            check_forward(synthetic(entry,["push   0x50",*pushes[1:],"call   "+hex(target),"ret"]),entry,target,pushes)
    def test_no_proof_from_bounded_core(self):
        seq=synthetic(0x45ed6c,["nop"]*40)
        r=core_prefix(seq,0x45ed6c)
        self.assertEqual(len(r["static_instruction_prefix"]),32)
        self.assertFalse(r["first_return_within_32"])
        self.assertFalse(r["C_runtime_symbol_proven"])
    def test_missing_source_entry_rejected(self):
        with self.assertRaises(ValueError):bounded_entry([],0x45ed40)
if __name__=="__main__":unittest.main()
