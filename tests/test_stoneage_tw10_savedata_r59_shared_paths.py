"""Pure metadata R59 path witness tests and mutation controls."""
import copy
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_r59_shared_paths import (derive,read_source,ROOT,CALL,ERROR_FLAG,ALL_ONES)

SOURCE=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json"

class ThreeRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=read_source(SOURCE)
    def tamper(self,change):
        d=copy.deepcopy(self.source);c=next(x for x in d["contexts"] if x["root_candidate_rva"]==ROOT)
        change(c)
        with self.assertRaises(ValueError):derive(d)
    def test_three_structural_witnesses(self):
        d=derive(self.source)
        self.assertNotIn(CALL,d["structural_call_free_candidate_zero_return"])
        self.assertIn(CALL,d["structural_nested_call_without_error_flag_write"])
        self.assertNotIn(ERROR_FLAG,d["structural_nested_call_without_error_flag_write"])
        self.assertIn(ALL_ONES,d["structural_nested_call_with_error_flag_and_all_ones_return"])
    def test_no_runtime_or_persistence_promotion(self):
        d=derive(self.source)
        for key in ("actual_original_branch_feasibility_proven",
                    "opaque_nested_call_preserves_edi_esi_ebx_or_memory_proven",
                    "full_count_return_implies_native_write_executed",
                    "all_ones_is_original_native_error_convention_proven",
                    "actual_original_file_write_flush_close_or_persistence_proven",
                    "original_executable_or_native_api_executed"):
            self.assertIs(d[key],False)
    def test_reject_forged_native_target(self):
        self.tamper(lambda c:next(x for x in c["instruction_shapes"] if x["site_rva"]==CALL)["operands"][0].__setitem__("constant",0))
    def test_reject_missing_bypass_branch(self):
        self.tamper(lambda c:c["bounded_edges"].remove([0x4A66B,0x4A6A4]))
    def test_reject_changed_compare(self):
        self.tamper(lambda c:next(x for x in c["instruction_shapes"] if x["site_rva"]==0x4A68B)["operands"][1].__setitem__("register","esi"))
    def test_reject_fake_error_mask(self):
        self.tamper(lambda c:next(x for x in c["instruction_shapes"] if x["site_rva"]==ERROR_FLAG)["operands"][1].__setitem__("constant",0x10))
    def test_reject_fake_result_register(self):
        self.tamper(lambda c:next(x for x in c["instruction_shapes"] if x["site_rva"]==0x4A6AE)["operands"][1].__setitem__("register","edi"))
    def test_reject_unclosed_frontier(self):
        self.tamper(lambda c:c["graph"].__setitem__("frontier",[{"reason":"invented"}]))
if __name__=="__main__":
    unittest.main()
