"""R16 synthetic-only helper effects and global read/write candidate tests."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_callee_global_r16 import (
    callee_frontiers,third_global_references,inspect_verified,GLOBAL,FLAGS
)
BASE=0x400000
ROOT=0x1000

def decoder(raw):
    return Decoder(raw,ROOT,BASE)

class TestR16Synthetic(unittest.TestCase):
    def test_small_clean_ret_is_only_model_summary(self):
        item=callee_frontiers(decoder(bytes.fromhex("c3")),[(ROOT,12)])[0]
        self.assertEqual(item["summary"]["return_paths"][0]["rva"],ROOT)
        self.assertTrue(item["summary"]["qualifies_modeled_return_effect_summary"])
        self.assertFalse(item["original_callee_effects_admitted"])
        self.assertFalse(item["calling_convention_proven"])

    def test_unsummarized_call_gap_retained(self):
        item=callee_frontiers(decoder(bytes.fromhex("e800000000c3")),[(ROOT,12)])[0]
        self.assertFalse(item["summary"]["qualifies_modeled_return_effect_summary"])
        self.assertEqual(item["summary"]["gaps"]["unsummarized_call"],1)

    def test_bounded_callee_hard_cap(self):
        with self.assertRaises(ValueError):
            callee_frontiers(decoder(bytes.fromhex("c3")),[(ROOT,161)])

    def test_duplicate_callee_rejected(self):
        with self.assertRaises(ValueError):
            callee_frontiers(decoder(bytes.fromhex("c3")),[(ROOT,1),(ROOT,1)])

    def test_separate_original_global_read_write(self):
        raw=(bytes.fromhex("a1")+struct.pack("<I",BASE+GLOBAL)
            +bytes.fromhex("a3")+struct.pack("<I",BASE+GLOBAL)
            +bytes.fromhex("c3"))
        scan=third_global_references(decoder(raw))
        self.assertEqual(scan["globals"][0]["counts"]["read_candidate"],1)
        self.assertEqual(scan["globals"][0]["counts"]["write_candidate"],1)
        self.assertEqual(scan["globals"][0]["counts"]["address_candidate"],0)
        self.assertFalse(scan["globals"][0]["runtime_initialization_proven"])
        self.assertFalse(scan["all_indirect_references_covered"])

    def test_global_byte_gap_not_discarded(self):
        scan=third_global_references(decoder(bytes.fromhex("0fc3")))
        self.assertEqual(scan["decode_gap_bytes"],1)

    def test_model_does_not_admit_runtime(self):
        self.assertIn("original_native_io_proven",FLAGS)
        self.assertIn("caller_context_equivalence_proven",FLAGS)

    def test_original_hash_guard(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not original",b"bad")

if __name__=="__main__":
    unittest.main()
