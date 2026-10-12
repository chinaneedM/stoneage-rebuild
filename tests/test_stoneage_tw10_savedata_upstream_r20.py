"""R20 synthetic-only tests. No historical bytes in these fixtures."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r20 import (
    indirect_call_frontier,third_global_frontier,heapalloc_prefix,
    alias_gap_frontier,inspect_verified,THIRD_GLOBAL,FLAGS
)
BASE=0x400000
ROOT=0x1000
def dec(raw):return Decoder(raw,ROOT,BASE)

class TestR20Synthetic(unittest.TestCase):
    def test_mem_indirect_call_identity_is_not_runtime_proof(self):
        slot=BASE+0x400
        raw=b"\xff\x15"+struct.pack("<I",slot)+b"\xc3"
        d=indirect_call_frontier(dec(raw),[],{},site=ROOT,root=ROOT)
        self.assertEqual(d["call_identity"]["kind"],"memory_indirect")
        self.assertFalse(d["callee_effect_summary_admitted"])
        self.assertFalse(d["runtime_call_target_proven"])

    def test_register_indirect_call_source_candidate_only(self):
        d=indirect_call_frontier(dec(bytes.fromhex("b800100000ffd0c3")),[],{},
                                 site=ROOT+5,root=ROOT)
        self.assertEqual(d["target_register_sources"][0]["register"],"eax")
        self.assertFalse(d["target_register_sources"][0]["local_sources"]["value_known"])

    def test_unreachable_indirect_call_rejected(self):
        with self.assertRaisesRegex(ValueError,"not reached"):
            indirect_call_frontier(dec(bytes.fromhex("c39090")),[],{},ROOT+1,ROOT)

    def test_push_memory_global_reference_static_only(self):
        raw=b"\xff\x35"+struct.pack("<I",BASE+THIRD_GLOBAL)+b"\xc3"
        d=third_global_frontier(dec(raw),[],push_site=ROOT)
        self.assertEqual(d["source_operand"]["kind"],"memory")
        self.assertFalse(d["actual_heapalloc_argument_position_proven"])
        self.assertEqual(d["linear_references"]["globals"][0]["counts"]["read_candidate"],1)

    def test_wrong_push_global_identity_rejected(self):
        raw=b"\xff\x35"+struct.pack("<I",BASE+THIRD_GLOBAL+4)+b"\xc3"
        with self.assertRaisesRegex(ValueError,"target changed"):
            third_global_frontier(dec(raw),[],push_site=ROOT)

    def test_heap_prefix_push_never_becomes_abi_proof(self):
        # push eax ; call eax ; ret
        raw=bytes.fromhex("50ffd0c3")
        d=heapalloc_prefix(dec(raw),root=ROOT,call=ROOT+1)
        self.assertEqual(d["prefix_push_sites"],[ROOT])
        self.assertEqual(d["stop_reason"],"at_opaque_heapalloc_call")
        self.assertFalse(d["stack_argument_roles_proven"])

    def test_heap_prefix_branch_barrier(self):
        d=heapalloc_prefix(dec(bytes.fromhex("eb0190ffd0c3")),root=ROOT,call=ROOT+3)
        self.assertEqual(d["stop_reason"],"earlier_control_transfer_barrier")

    def test_alias_write_memory_shape_preserves_uncertainty(self):
        raw=bytes.fromhex("894804c3") # mov [eax+4], ecx ; ret
        d=alias_gap_frontier(dec(raw),[],site=ROOT,root=ROOT)
        self.assertEqual(d["operand_shapes"][0]["kind"],"memory")
        self.assertFalse(d["alias_effective_address_proven"])
        self.assertTrue(d["model_original_gap_present"])

    def test_missing_alias_gap_rejected(self):
        with self.assertRaisesRegex(ValueError,"memory-bearing"):
            alias_gap_frontier(dec(b"\xc3"),[],site=ROOT,root=ROOT)

    def test_original_hashes_gate(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"incorrect",b"also incorrect")

    def test_no_runtime_claims_are_possible(self):
        self.assertIn("native_file_io_executed",FLAGS)
        self.assertIn("allocation_pointer_ownership_proven",FLAGS)

if __name__=="__main__":unittest.main()
