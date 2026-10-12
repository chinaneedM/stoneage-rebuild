"""Synthetic-only reachability, branch joins, opaque CALL and unknown inputs."""
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_reachdefs_r14 import (
    bounded_graph, probe_region, inspect_verified, FLAGS,
)
BASE = 0x400000
ROOT = 0x1000

def decoder(raw):
    return Decoder(raw, ROOT, BASE)

class TestBoundedR14(unittest.TestCase):
    def test_conditional_join_retains_two_sources(self):
        # mov eax,1; test ebx,ebx; jz +5; mov eax,2; mov [ebp+8],eax; ret
        code = bytes.fromhex("b80100000085db7405b802000000894508c3")
        row = probe_region(decoder(code), ROOT, [(ROOT+14,"eax")], [])
        self.assertEqual(row["branch_sites"], [ROOT+7])
        origins = {(x["origin"], x["rva"]) for x in row["inputs"][0]["reaching_sources"]}
        self.assertEqual(origins, {("definition",ROOT), ("definition",ROOT+9)})
        self.assertFalse(row["inputs"][0]["register_value_known"])

    def test_unknown_call_is_register_barrier(self):
        # mov eax,7; call +0; mov [ebp+8],eax; ret
        code=bytes.fromhex("b807000000e800000000894508c3")
        row=probe_region(decoder(code),ROOT,[(ROOT+10,"eax")],[])
        self.assertEqual(row["call_barrier_sites"],[ROOT+5])
        self.assertEqual(row["inputs"][0]["reaching_sources"],
                         [{"origin":"unknown_call","rva":ROOT+5,"semantic":None}])
        self.assertTrue(row["call_fallthrough_is_structural_only"])

    def test_no_automatic_predecessor_before_anchor(self):
        row=probe_region(decoder(bytes.fromhex("894508c3")),ROOT,[(ROOT,"eax")],[])
        self.assertEqual(row["inputs"][0]["reaching_sources"],
                         [{"origin":"entry","rva":ROOT,"semantic":None}])
        self.assertFalse(row["anchor_is_verified_function_entry"])

    def test_out_of_window_kept_as_gap(self):
        code=bytes.fromhex("e9ff010000")
        row=probe_region(decoder(code),ROOT,[(ROOT,"eax")],[])
        self.assertIn({"reason":"out_of_window","rva":ROOT+516},row["frontier"])
        self.assertFalse(row["all_incoming_edges_proven"])

    def test_site_missing_not_misreported_as_known(self):
        row=probe_region(decoder(bytes.fromhex("c3")),ROOT,[(ROOT+1,"ebx")],[])
        self.assertFalse(row["inputs"][0]["reachable_in_bounded_graph"])
        self.assertEqual(row["inputs"][0]["reaching_sources"],[])

    def test_bounded_parameter_checks(self):
        with self.assertRaises(ValueError):
            bounded_graph(decoder(bytes.fromhex("90")),ROOT,max_nodes=193)
        with self.assertRaises(ValueError):
            bounded_graph(decoder(bytes.fromhex("90")),ROOT,max_span=385)

    def test_output_scope_flags(self):
        self.assertIn("global_initialization_proven",FLAGS)
        self.assertIn("native_io_executed",FLAGS)

    def test_original_sha_gate(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not-original-executable",b"not-original-savedata")

if __name__ == "__main__":
    unittest.main()
