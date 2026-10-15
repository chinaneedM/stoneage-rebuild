"""R60 source-custody, structural predicate and non-promotion mutations."""
import copy
import unittest
from pathlib import Path

from tools.stoneage_tw10_savedata_r60_close_predicates import (
    derive, inspect_raw, CLOSE_CALL, ERROR_CALL, ZERO, ONES,
)

BASE = Path(__file__).resolve().parents[1] / "research/recovered"


class ClosePredicates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw28 = (BASE / "STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json").read_bytes()
        cls.raw58 = (BASE / "STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json").read_bytes()
        cls.base = __import__("json").loads(cls.raw28), __import__("json").loads(cls.raw58)

    def mutated(self, change):
        a, b = copy.deepcopy(self.base)
        change(a, b)
        with self.assertRaises(ValueError):
            derive(a, b)

    def close(self, report):
        return next(x for x in report["contexts"] if x["root_candidate_rva"] == 0x4A53E)

    def row(self, report, at):
        return next(x for x in self.close(report)["instruction_shapes"] if x["site_rva"] == at)

    def test_source_custody_and_four_structural_routes(self):
        d = inspect_raw(self.raw28, self.raw58)
        w = d["close_structural_candidate_routes"]
        self.assertEqual(len(w), 4)
        for seq in w.values():
            self.assertEqual((seq[0], seq[-1]), (0x4A53E, 0x4A5F0))
        self.assertNotIn(CLOSE_CALL, w["early_range_guard_all_ones_without_native_close"])
        self.assertNotIn(ERROR_CALL, w["close_handle_nonzero_test_shape_skips_getlasterror_and_zero_return"])
        self.assertIn(ERROR_CALL, w["close_handle_zero_test_shape_getlasterror_then_zero_return"])
        self.assertIn(0x4A5CC, w["close_handle_zero_test_shape_getlasterror_nonzero_error_helper_all_ones"])

    def test_source_custody_bit_flip(self):
        raw = bytearray(self.raw58)
        raw[100] ^= 1
        with self.assertRaises(ValueError):
            inspect_raw(self.raw28, bytes(raw))

    def test_native_postcall_result_unresolved(self):
        d = derive(*self.base)
        self.assertEqual([x["eax_reaching_source"] for x in d["writefile_postcall_eax_provenance"]],
                         ["unknown_call", "unknown_call"])
        self.assertEqual([x["prior_graph_site_reached"] for x in d["writefile_postcall_eax_provenance"]],
                         [True, False])
        for key in ("closehandle_or_getlasterror_original_result_known",
                    "test_or_jump_native_success_error_mapping_proven",
                    "getlasterror_is_original_savedata_error_code_proven",
                    "original_writefile_bytecount_or_success_proven",
                    "original_close_flush_disk_persistence_proven",
                    "original_executable_payload_or_native_api_executed"):
            self.assertIs(d[key], False)

    def test_reject_forged_writefile_postcall_value(self):
        def tamper(a, b):
            w = next(x for x in a["contexts"] if x["api"] == "WriteFile")
            q = next(x for x in w["inputs"]["queries"] if x["site_rva"] == 0x4C692 and x["register"] == "eax")
            q["actual_register_value_known"] = True
        self.mutated(tamper)

    def test_reject_forged_writefile_second_prior_coverage(self):
        self.mutated(lambda a, b: next(x for x in a["contexts"] if x["api"] == "WriteFile")["api_sites"][1].__setitem__("prior_graph_site_reached", True))

    def test_reject_changed_closehandle_import(self):
        self.mutated(lambda a, b: next(x for x in self.close(b)["call_contexts"] if x["site_rva"] == CLOSE_CALL)["identity"]["import_identity"].__setitem__("name", "WriteFile"))

    def test_reject_changed_getlasterror_import(self):
        self.mutated(lambda a, b: next(x for x in self.close(b)["call_contexts"] if x["site_rva"] == ERROR_CALL)["identity"]["import_identity"].__setitem__("iat_rva", 0))

    def test_reject_missing_closehandle_skip_edge(self):
        self.mutated(lambda a, b: self.close(b)["bounded_edges"].remove([0x4A5AB, 0x4A5B7]))

    def test_reject_missing_getlasterror_path_edge(self):
        self.mutated(lambda a, b: self.close(b)["bounded_edges"].remove([0x4A5AB, ERROR_CALL]))

    def test_reject_missing_error_zero_branch(self):
        self.mutated(lambda a, b: self.close(b)["bounded_edges"].remove([0x4A5C9, ZERO]))

    def test_reject_forged_test_register(self):
        self.mutated(lambda a, b: self.row(b, 0x4A5C7)["operands"][1].__setitem__("register", "eax"))

    def test_reject_forged_error_transfer_register(self):
        self.mutated(lambda a, b: self.row(b, 0x4A5B3)["operands"][0].__setitem__("register", "edi"))

    def test_reject_forged_zero_or_ones_return(self):
        self.mutated(lambda a, b: self.row(b, ZERO)["operands"][1].__setitem__("register", "ebx"))
        self.mutated(lambda a, b: self.row(b, ONES)["operands"][1].__setitem__("constant", 1))

    def test_reject_nonempty_frontier(self):
        self.mutated(lambda a, b: self.close(b)["graph"].__setitem__("frontier", [{"unknown": True}]))

    def test_reject_native_execution_promotion(self):
        self.mutated(lambda a, b: b.__setitem__("native_code_executed", True))


if __name__ == "__main__":
    unittest.main()
