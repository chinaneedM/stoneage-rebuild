"""Synthetic-only R21 static frontiers. No historic bytes."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r21 import (
    third_global_writer,heaprealloc_candidate_inputs,eax_alias_frontier,
    inspect_verified,THIRD_GLOBAL,FLAGS,
)
BASE=0x400000
ROOT=0x1000
def dec(raw):return Decoder(raw,ROOT,BASE)
class R21Synthetic(unittest.TestCase):
    def test_writer_source_not_value(self):
        raw=b"\xa3"+struct.pack("<I",BASE+THIRD_GLOBAL)+b"\xc3"
        d=third_global_writer(dec(raw),[],site=ROOT,anchors=(ROOT,))
        self.assertEqual(d["write"]["source_operand"]["register"],"eax")
        self.assertFalse(d["source_register_value_proven"])
        self.assertFalse(d["direct_store_executed_proven"])
    def test_wrong_writer_target_rejected(self):
        raw=b"\xa3"+struct.pack("<I",BASE+THIRD_GLOBAL+4)+b"\xc3"
        with self.assertRaises(ValueError):
            third_global_writer(dec(raw),[],site=ROOT,anchors=(ROOT,))
    def test_realloc_push_candidates_are_not_abi_slots(self):
        raw=b"\x50\x51\xff\x15"+struct.pack("<I",BASE+0x400)+b"\xc3"
        d=heaprealloc_candidate_inputs(dec(raw),[],{},root=ROOT,callsite=ROOT+2)
        self.assertEqual(len(d["pre_call_push_candidates"]),2)
        self.assertTrue(d["call_is_opaque_register_barrier"])
        self.assertTrue(d["post_call_eax_value_unknown"])
        self.assertFalse(d["stack_argument_slots_admitted"])
    def test_unreachable_call_rejected(self):
        with self.assertRaises(ValueError):
            heaprealloc_candidate_inputs(dec(bytes.fromhex("c3ffd0")),[],{},
                                         root=ROOT,callsite=ROOT+1)
    def test_eax_alias_is_not_object_ownership(self):
        d=eax_alias_frontier(dec(bytes.fromhex("894008c3")),[],site=ROOT,root=ROOT)
        self.assertTrue(d["same_syntactic_register_for_address_and_value"])
        self.assertFalse(d["real_object_base_or_alias_proven"])
        self.assertFalse(d["callee_return_or_caller_effect_admitted"])
    def test_alias_offset_change_rejected(self):
        with self.assertRaises(ValueError):
            eax_alias_frontier(dec(bytes.fromhex("894004c3")),[],site=ROOT,root=ROOT)
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"no original",b"no savedata")
    def test_no_original_io_promotion(self):
        self.assertIn("native_file_io_executed",FLAGS)
        self.assertIn("caller_resumption_admitted",FLAGS)
if __name__=="__main__":unittest.main()
