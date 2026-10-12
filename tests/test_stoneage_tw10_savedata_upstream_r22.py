"""R22 synthetic-only call, candidate push paths and back-edge checks."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r22 import (
    writer_call_frontier, realloc_push_flow, alias_cycle_frontier,
    inspect_verified, FLAGS,
)
BASE=0x400000
ROOT=0x1000
def dec(raw):return Decoder(raw,ROOT,BASE)
class R22Synthetic(unittest.TestCase):
    def test_direct_writer_call_target_is_not_return_effect(self):
        # MOV EAX,1 ; CALL next; MOV [abs],EAX ; RET
        raw=b"\xb8\x01\x00\x00\x00\xe8\x00\x00\x00\x00\xa3"+struct.pack("<I",BASE+0x700)+b"\xc3"
        d=writer_call_frontier(dec(raw),[],{},root=ROOT,site=ROOT+5,writer=ROOT+10)
        self.assertEqual(d["call_identity"]["kind"],"direct")
        self.assertTrue(d["call_to_writer_structural_path_exists"])
        self.assertFalse(d["actual_callee_return_or_register_effect_known"])
        self.assertFalse(d["writer_value_after_call_known"])
    def test_call_must_be_actual_call(self):
        with self.assertRaises(ValueError):
            writer_call_frontier(dec(b"\x90\xc3"),[],{},root=ROOT,site=ROOT,writer=ROOT+1)
    def test_call_and_target_graph_required(self):
        with self.assertRaisesRegex(ValueError,"outside bounded graph"):
            writer_call_frontier(dec(b"\xc3\xe8\x00\x00\x00\x00\xc3"),[],{},
                                 root=ROOT,site=ROOT+1,writer=ROOT+6)
    def test_push_graph_paths_only(self):
        raw=b"\x50\x57\xff\xd0\xc3"
        d=realloc_push_flow(dec(raw),[],root=ROOT,site=ROOT+2)
        self.assertEqual(len(d["push_flow_candidates"]),2)
        self.assertTrue(all(p["syntactic_cfg_path_to_call"] for p in d["push_flow_candidates"]))
        self.assertTrue(all(p["original_stack_position_or_abi_role_proven"] is False
                            for p in d["push_flow_candidates"]))
        self.assertFalse(d["heaprealloc_stack_signature_applied"])
    def test_return_without_call_unreachable(self):
        with self.assertRaises(ValueError):
            realloc_push_flow(dec(bytes.fromhex("c3ffd0")),[],root=ROOT,site=ROOT+1)
    def test_loop_edge_not_execution(self):
        # MOV [EAX+8],EAX; INC EAX; JMP back. Synthetic control only.
        d=alias_cycle_frontier(dec(bytes.fromhex("89400840ebfa")),[],root=ROOT,site=ROOT)
        self.assertTrue(d["backward_edges"])
        self.assertTrue(d["reverse_rva_source_does_not_prove_linear_order"])
        self.assertFalse(d["runtime_cycle_taken_known"])
        self.assertFalse(d["return_to_caller_admitted"])
    def test_missing_alias_site_rejected(self):
        with self.assertRaises(ValueError):
            alias_cycle_frontier(dec(b"\xc3"),[],root=ROOT,site=ROOT+1)
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not original",b"not original")
    def test_no_runtime_promotion_flag(self):
        self.assertIn("native_file_io_executed",FLAGS)
        self.assertIn("writer_call_return_effect_admitted",FLAGS)
if __name__=="__main__":unittest.main()
