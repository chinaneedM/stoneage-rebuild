"""R19 synthetic-only second global, HeapAlloc and CALL barrier cases."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r19 import (
    second_global_writes, heapalloc_argument_candidates,
    ebx_callee_frontier, imul_call_contexts, inspect_verified, FLAGS,
    SECOND_GLOBAL
)
BASE=0x400000
ROOT=0x1000
def decoder(raw):return Decoder(raw,ROOT,BASE)

class TestR19(unittest.TestCase):
    def test_second_global_absolute_store_no_initialization(self):
        raw=b"\xa3"+struct.pack("<I",BASE+SECOND_GLOBAL)+b"\xc3"
        row=second_global_writes(decoder(raw),[],writes=(ROOT,),anchors={ROOT:ROOT})[0]
        self.assertEqual(row["write"]["source_operand"]["register"],"eax")
        self.assertFalse(row["initialized_global_proven"])
        self.assertFalse(row["actual_executed_write_proven"])

    def test_other_global_rejected(self):
        raw=b"\xa3"+struct.pack("<I",BASE+SECOND_GLOBAL+4)+b"\xc3"
        with self.assertRaises(ValueError):
            second_global_writes(decoder(raw),[],writes=(ROOT,),anchors={ROOT:ROOT})

    def test_push_candidates_never_become_argument_slots(self):
        # push 4; call [iat]; ret
        slot=BASE+0x520f8
        raw=b"\x6a\x04\xff\x15"+struct.pack("<I",slot)+b"\xc3"
        ins=decoder(raw)
        result=heapalloc_argument_candidates(ins,[],{slot:("KERNEL32.dll","HeapAlloc")},
                       call_site=ROOT+2,anchor=ROOT)
        self.assertEqual(result["syntactic_pre_call_push_candidates"][0]["site_rva"],ROOT)
        self.assertFalse(result["argument_count_and_slots_proven"])
        self.assertFalse(result["return_pointer_proven"])

    def test_heapalloc_wrong_import_rejected(self):
        slot=BASE+0x520f8
        raw=b"\xff\x15"+struct.pack("<I",slot)+b"\xc3"
        with self.assertRaisesRegex(ValueError,"HeapAlloc"):
            heapalloc_argument_candidates(decoder(raw),[],{slot:("KERNEL32.dll","VirtualAlloc")},
                                          call_site=ROOT,anchor=ROOT)

    def test_ebx_call_qualified_syntactic_ret_never_admitted(self):
        # call direct ret; ret
        raw=b"\xe8\x01\x00\x00\x00\xc3\xc3"
        item=ebx_callee_frontier(decoder(raw),[],{},site=ROOT,target=ROOT+6)
        self.assertTrue(item["callee_summary"]["qualifies_modeled_return_effect_summary"])
        self.assertFalse(item["caller_resume_admitted"])
        self.assertFalse(item["original_source_ebx_after_call_known"])

    def test_imul_caller_context_does_not_claim_ownership(self):
        raw=b"\xe8\x01\x00\x00\x00\xc3\xc3"
        item=imul_call_contexts(decoder(raw),[],{},call_sites=(ROOT,),expected_target=ROOT+6)[0]
        self.assertFalse(item["caller_argument_ownership_proven"])
        self.assertTrue(item["callee_model_entry_esp_plus8_not_actual_argument"])

    def test_duplicate_writes_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            second_global_writes(decoder(b"\xc3"),[],writes=(ROOT,ROOT),anchors={ROOT:ROOT})

    def test_no_native_promotion_possible(self):
        self.assertIn("native_io_executed",FLAGS)
        self.assertIn("heapalloc_return_value_or_allocation_proven",FLAGS)

    def test_pinned_hash_gate_rejects_unknown_original(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not-original",b"not-savedata")

if __name__=="__main__":unittest.main()
