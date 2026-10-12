import struct
import unittest

from tools.stoneage_tw10_savedata_instruction_probe import (
    WORD_RVAS, RUNTIME_SHA256, SAVEDATA_SHA256,
    candidate_instructions, validate_word, verify_hash, linear_overlap
)
from capstone import Cs, CS_ARCH_X86, CS_MODE_32


class TestTw10SavedataInstructionProbe(unittest.TestCase):
    def test_pinned_baseline_and_four_distinct_words(self):
        self.assertEqual(len(WORD_RVAS), 4)
        self.assertEqual(len(set(WORD_RVAS)), 4)
        self.assertEqual(len(RUNTIME_SHA256), 64)
        self.assertEqual(len(SAVEDATA_SHA256), 64)

    def test_hash_guard(self):
        import hashlib
        verify_hash(b"synthetic", hashlib.sha256(b"synthetic").hexdigest(), "sample")
        with self.assertRaises(ValueError):
            verify_hash(b"synthetic", "0" * 64, "sample")

    def test_synthetic_push_immediate_alt_alignment(self):
        target = 0x463634
        raw = b"\x90" * 16 + b"\x68" + struct.pack("<I", target) + b"\xc3"
        matches = candidate_instructions(raw, 0x400000, 0x1000, 0x1011, target)
        self.assertTrue(any(x["start"] == 0x1010 and x["mnemonic"] == "push" for x in matches))
        self.assertTrue(all(x["start"] <= 0x1011 < x["end"] for x in matches))

    def test_synthetic_indirect_memory_operand(self):
        target = 0x463634
        raw = b"\x8b\x0d" + struct.pack("<I", target) + b"\xc3"
        matches = candidate_instructions(raw, 0x400000, 0x1000, 0x1002, target)
        self.assertTrue(any(x["start"] == 0x1000 and x["mnemonic"] == "mov" for x in matches))

    def test_non_opcode_word_does_not_prove_reference(self):
        raw = struct.pack("<I", 0x463634)
        self.assertEqual(candidate_instructions(raw, 0x400000, 0x1000, 0x1000, 0x463634), ())

    def test_word_cannot_cross_raw_boundary(self):
        with self.assertRaises(ValueError):
            candidate_instructions(b"\x90" * 4, 0x400000, 0x1000, 0x1001, 0x463634)

    def test_exact_word_and_no_virtual_padding(self):
        sec = [{"name": ".text", "rva": 0x1000, "vsize": 0x100, "raw_size": 8, "raw": 0}]
        raw = b"\x90" * 2 + struct.pack("<I", 0x463634) + b"\x90" * 2
        self.assertEqual(validate_word(raw, sec, 0x1002, 0x463634), 2)
        with self.assertRaises(ValueError):
            validate_word(raw, sec, 0x1006, 0x463634)
        with self.assertRaises(ValueError):
            validate_word(raw, sec, 0x1002, 0x463635)

    def test_linear_overlap_is_not_instruction_proof(self):
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        insns = list(md.disasm(b"\x90\x68\x34\x36\x46\x00\xc3", 0x401000))
        self.assertEqual(linear_overlap(insns, 0x400000, 0x1002), (1, 1, 0))


if __name__ == "__main__":
    unittest.main()
