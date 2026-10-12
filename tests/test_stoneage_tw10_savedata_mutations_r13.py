"""Synthetic-only R13 site-geometry regression tests; never needs original media."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_mutations_r13 import (
    write_candidate, linear_window, inspect_verified, FLAGS,
)
BASE = 0x400000
ROOT = 0x1000
GLOBAL = 0x1721884
ABS = BASE + GLOBAL

def decoder(data):
    return Decoder(data, ROOT, BASE)

class TestR13StoreCandidates(unittest.TestCase):
    def test_absolute_register_write(self):
        ins = b"\xa3" + struct.pack("<I", ABS)
        item = write_candidate(decoder(ins), ROOT, [], GLOBAL)
        self.assertEqual(item["destination"]["write_width_bytes"], 4)
        self.assertEqual(item["source_operand"]["register"], "eax")
        self.assertEqual(item["address_inputs"], [])
        self.assertIsNone(item["destination_relative_field_offset"])
        self.assertFalse(item["executed_write_proven"])
        self.assertFalse(item["register_inputs_resolved"])

    def test_frame_relative_memory_store(self):
        item = write_candidate(decoder(b"\x89\x45\x08"), ROOT, [])
        self.assertEqual(item["destination"]["base_register"], "ebp")
        self.assertEqual(item["destination"]["write_width_bytes"], 4)
        self.assertEqual(item["address_inputs"], ["ebp"])
        self.assertEqual(item["destination_relative_field_offset"], 8)
        self.assertIsNone(item["destination"]["absolute_effective_rva"])
        self.assertFalse(item["named_caller_effect_admitted"])

    def test_alias_based_store(self):
        item = write_candidate(decoder(b"\x89\x18"), ROOT, [])
        self.assertEqual(item["address_inputs"], ["eax"])
        self.assertEqual(item["source_operand"]["register"], "ebx")
        self.assertFalse(item["effective_object_proven"])

    def test_immediate_global_write(self):
        item = write_candidate(decoder(
            b"\xc7\x05" + struct.pack("<I", ABS) + struct.pack("<I", 23)
        ), ROOT, [], GLOBAL)
        self.assertEqual(item["source_operand"]["kind"], "immediate_input")
        self.assertEqual(item["source_operand"]["immediate"], 23)

    def test_arithmetic_is_read_modify_write(self):
        item = write_candidate(decoder(b"\x83\x45\x08\x01"), ROOT, [])
        self.assertTrue(item["previous_destination_value_required"])
        self.assertIn("destination_memory", item["value_input_registers"])

    def test_load_is_not_write(self):
        with self.assertRaises(ValueError):
            write_candidate(decoder(b"\xa1" + struct.pack("<I", ABS)), ROOT, [])

    def test_wrong_global_raises(self):
        with self.assertRaises(ValueError):
            write_candidate(decoder(b"\xa3" + struct.pack("<I", ABS)),
                            ROOT, [], 0x17228a0)

    def test_segmented_rejected(self):
        with self.assertRaises(ValueError):
            write_candidate(decoder(b"\x64\xa3" + struct.pack("<I", ABS)),
                            ROOT, [])

    def test_unsupported_opcode_rejected(self):
        with self.assertRaises(ValueError):
            write_candidate(decoder(b"\x90"), ROOT, [])

    def test_linear_window_is_not_reachable_path(self):
        row = linear_window(decoder(b"\x90\x74\x01\x90\xc3"), ROOT, ROOT+4)
        self.assertEqual(row["jump_sites"], [ROOT+1])
        self.assertFalse(row["same_executed_path_proven"])
        self.assertFalse(row["function_boundary_proven"])

    def test_decode_gap_rejected(self):
        with self.assertRaises(ValueError):
            linear_window(decoder(b"\x0f"), ROOT, ROOT)

    def test_window_cap_enforced(self):
        with self.assertRaises(ValueError):
            linear_window(decoder(b"\x90"*70), ROOT, ROOT+65)

    def test_never_promote_unknown_flags(self):
        self.assertIn("global_write_paths_proven", FLAGS)
        self.assertIn("heapalloc_size_or_ownership_proven", FLAGS)

    def test_original_bytes_hash_gate(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"not-an-original-executable", b"bad")

if __name__ == "__main__":
    unittest.main()
