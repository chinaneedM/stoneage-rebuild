"""R18 synthetic-only CALL, independent .data, bounded CFG and stack tests."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_upstream_r18 import (
    upstream_call, global_alias_probe, candidate_ebx_graph,
    imul_stack_prefix, inspect_verified, SECOND_GLOBAL, FLAGS,
)

BASE=0x400000
ROOT=0x1000

def decoder(raw):
    return Decoder(raw, ROOT, BASE)

class TestR18Synthetic(unittest.TestCase):
    def test_call_identity_no_return_value_proof(self):
        dec=decoder(bytes.fromhex("e80100000090c3"))
        r=upstream_call(dec, {}, [], call_rva=ROOT, root=ROOT, query_site=ROOT+5)
        self.assertEqual(r["call_identity"]["kind"], "direct")
        self.assertFalse(r["eax_after_call_known"])
        self.assertFalse(r["callee_summary_admitted"])

    def test_missing_call_and_write_path_is_rejected(self):
        dec=decoder(bytes.fromhex("c3"))
        with self.assertRaisesRegex(ValueError, "not in bounded"):
            upstream_call(dec, {}, [], call_rva=ROOT, root=ROOT, query_site=ROOT+2)

    def test_global_load_is_distinct_and_uninitialized(self):
        # mov ecx, [absolute VA]; ret
        raw=b"\x8b\x0d"+struct.pack("<I",BASE+SECOND_GLOBAL)+b"\xc3"
        r=global_alias_probe(decoder(raw), [], read_site=ROOT)
        self.assertEqual(r["global_reference_candidates"]["globals"][0]["counts"]["read_candidate"],1)
        self.assertFalse(r["runtime_initialized"])
        self.assertFalse(r["same_object_as_primary_global_proven"])

    def test_global_load_wrong_identity_rejected(self):
        raw=b"\x8b\x0d"+struct.pack("<I",BASE+SECOND_GLOBAL+4)+b"\xc3"
        with self.assertRaisesRegex(ValueError, "changed"):
            global_alias_probe(decoder(raw), [], read_site=ROOT)

    def test_conditional_ebx_origin_remains_unproved(self):
        # mov ebx,1; mov [global],ebx; ret
        raw=bytes.fromhex("bb01000000891dcafebc41c3")
        site=ROOT+5
        r=candidate_ebx_graph(decoder(raw), [], root=ROOT, site=site)
        self.assertTrue(r["reached_in_R14_helper_graph"])
        self.assertFalse(r["actual_function_entry_proven"])
        self.assertFalse(r["feasible_path_proven"])

    def test_unreachable_ebx_write_retains_unknown(self):
        r=candidate_ebx_graph(decoder(b"\xc3\x90\x90"), [], root=ROOT, site=ROOT+2)
        self.assertFalse(r["reached_in_R14_helper_graph"])
        self.assertEqual(r["source_candidates"],[])

    def test_imul_syntactic_stack_offset_only(self):
        # push esi; imul esi, [esp+0x14]; ret
        raw=bytes.fromhex("566b74241401c3")
        r=imul_stack_prefix(decoder(raw), root=ROOT, site=ROOT+1)
        self.assertTrue(r["stopped_at_original_memory_gap"])
        self.assertEqual(r["modeled_stack_offset_of_memory_operand"],16)
        self.assertFalse(r["real_esp_or_caller_frame_proven"])

    def test_imul_prefix_interrupt_stops_without_claim(self):
        dec=decoder(bytes.fromhex("e8000000006b742414c3"))
        r=imul_stack_prefix(dec,root=ROOT,site=ROOT+5)
        self.assertFalse(r["stopped_at_original_memory_gap"])
        self.assertEqual(r["halt_reason"],"control_transfer_barrier")

    def test_uncertainty_flags_remain_explicit(self):
        self.assertIn("native_save_io_executed",FLAGS)
        self.assertIn("caller_resumption_admitted",FLAGS)

    def test_wrong_original_hash_rejected(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not-original",b"not-savedata")

if __name__=="__main__":
    unittest.main()
