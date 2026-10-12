"""R16 strict derived-only original report and tamper regression tests."""
import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_callee_global_r16_guard import validate
PATH=Path("research/recovered/STONEAGE-TW10-SAVEDATA-CALLEE-GLOBAL-R16-ORIGINAL.json")
class TestOriginalR16Guard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content=PATH.read_text()
        cls.sample=json.loads(cls.content)
    def corrupt(self,fn):
        other=copy.deepcopy(self.sample);fn(other)
        with self.assertRaises(ValueError):validate(json.dumps(other))
    def test_approved_original_conditional_only(self):
        info=validate(self.content)
        self.assertEqual(info["global_write_candidates"],3)
        self.assertEqual(info["original_qualified_callees"],0)
    def test_native_io_promotion(self):
        self.corrupt(lambda x:x.update(original_native_io_proven=True))
    def test_caller_promotion(self):
        self.corrupt(lambda x:x.update(callee_effects_admitted=True))
    def test_heap_ownership_promotion(self):
        self.corrupt(lambda x:x.update(heapalloc_ownership_proven=True))
    def test_false_direct_source(self):
        self.corrupt(lambda x:x["r15_source_call_sites"][0].__setitem__(1,0))
    def test_misreport_value_source(self):
        self.corrupt(lambda x:x.update(r15_upstream_global_rva=0))
    def test_clear_unsupported_memory(self):
        self.corrupt(lambda x:x["callee_frontiers"][0]["summary"].update(gaps={}))
    def test_false_return(self):
        self.corrupt(lambda x:x["callee_frontiers"][0]["summary"].update(return_paths=[{"rva":1}]))
    def test_drop_control_flow_cycle(self):
        self.corrupt(lambda x:x["callee_frontiers"][3]["summary"].update(control_flow_cycle=False))
    def test_wrong_global_write_count(self):
        self.corrupt(lambda x:x["third_global_references"]["globals"][0]["counts"].update(write_candidate=4))
    def test_wrong_global_site(self):
        self.corrupt(lambda x:x["third_global_references"]["globals"][0]["samples"][0].update(rva=0))
    def test_false_runtime_initialization(self):
        self.corrupt(lambda x:x["third_global_references"]["globals"][0].update(runtime_initialization_proven=True))
    def test_unmodeled_indirect_coverage_promotion(self):
        self.corrupt(lambda x:x["third_global_references"].update(all_indirect_references_covered=True))
    def test_added_unaccepted_field(self):
        self.corrupt(lambda x:x.update(fully_restored=True))
    def test_duplicate_field(self):
        with self.assertRaises(ValueError):validate('{"schema":"a","schema":"b"}')
    def test_oversized_report(self):
        with self.assertRaises(ValueError):validate(" "*65001)
if __name__=="__main__":
    unittest.main()
