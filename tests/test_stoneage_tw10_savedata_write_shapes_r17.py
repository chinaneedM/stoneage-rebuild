"""R17 synthetic decoder-level tests. They do not authenticate original PE bytes."""
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_write_shapes_r17 import (
    operand_shape, candidate_sources, inspect_static, inspect_verified, FLAGS)

BASE = 0x400000
ROOT = 0x1000
GLOBAL = 0x172186c

class TestR17Synthetic(unittest.TestCase):
    def test_absolute_global_register_store_source_is_only_syntactic(self):
        raw = b"\xa3" + struct.pack("<I", BASE + GLOBAL) + b"\xc3"
        dec = Decoder(raw, ROOT, BASE)
        result = inspect_static(dec, [], writes=(ROOT,), gap=ROOT,
                                nested=(), anchors={ROOT: ROOT}, global_rva=GLOBAL)
        write = result["writes"][0]
        self.assertEqual(write["write"]["source_operand"]["register"], "eax")
        self.assertEqual(write["write"]["source_operand"]["width_bytes"], 4)
        self.assertFalse(write["actual_value_proven"])
        self.assertFalse(write["local_source_frontier"]["anchor_is_verified_entry"])

    def test_static_constant_store_does_not_claim_runtime_value(self):
        raw = b"\xc7\x05" + struct.pack("<I", BASE + GLOBAL) + struct.pack("<I", 0x55) + b"\xc3"
        dec = Decoder(raw, ROOT, BASE)
        result = inspect_static(dec, [], writes=(ROOT,), gap=ROOT,
                                nested=(), anchors={ROOT: ROOT}, global_rva=GLOBAL)
        write = result["writes"][0]
        self.assertEqual(write["write"]["source_operand"]["immediate"], 0x55)
        self.assertFalse(write["actual_value_proven"])
        self.assertFalse(write["executed_write_proven"])

    def test_read_from_global_is_not_global_write(self):
        raw = b"\xa1" + struct.pack("<I", BASE + GLOBAL) + b"\xc3"
        dec = Decoder(raw, ROOT, BASE)
        with self.assertRaises(ValueError):
            inspect_static(dec, [], writes=(ROOT,), gap=ROOT,
                           nested=(), anchors={ROOT:ROOT}, global_rva=GLOBAL)

    def test_unverified_memory_gap_keeps_shape_and_ownership_unknown(self):
        raw = bytes.fromhex("8b00c3")
        dec = Decoder(raw, ROOT, BASE)
        ins = dec.at(ROOT)
        op = operand_shape(ins, ins.operands[1], [], BASE)
        self.assertEqual(op["kind"], "memory")
        self.assertEqual(op["geometry"]["base_register"], "eax")

    def test_anchor_missing_site_is_not_asserted_reachable(self):
        dec = Decoder(bytes.fromhex("c39090"), ROOT, BASE)
        item = candidate_sources(dec, ROOT+2, "eax", [], ROOT)
        self.assertFalse(item["query_site_in_candidate_graph"])
        self.assertFalse(item["value_known"])

    def test_duplicate_write_sites_rejected(self):
        dec = Decoder(b"\xc3", ROOT, BASE)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            inspect_static(dec, [], writes=(ROOT,ROOT),gap=ROOT,nested=(),
                           anchors={ROOT:ROOT},global_rva=GLOBAL)

    def test_unbounded_ownership_flags_remain_false(self):
        self.assertIn("caller_resumption_admitted", FLAGS)
        self.assertIn("native_io_executed", FLAGS)
        self.assertIn("original_save_format_proven", FLAGS)

    def test_original_hash_required(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"wrong original",b"wrong savedata")

if __name__ == "__main__":
    unittest.main()
