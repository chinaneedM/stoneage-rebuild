import struct
import unittest

from tools.stoneage_tw10_exact_xref_probe import raw_text_pointer_hits


class TaiwanV10ExactXrefProbeTests(unittest.TestCase):
    def test_raw_text_pointer_hits(self):
        base = 0x400000
        target = 0x45984C
        data = bytearray(0x200)
        sections = [
            {"name": ".text", "raw": 0x40, "raw_size": 0x80, "rva": 0x1000, "vsize": 0x80},
        ]
        struct.pack_into("<I", data, 0x55, target)
        hits = raw_text_pointer_hits(bytes(data), base, sections, target)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["ptr_file_offset"], 0x55)
        self.assertEqual(hits[0]["ptr_rva"], 0x1015)

    def test_limits_are_bounded(self):
        from tools.stoneage_tw10_exact_xref_probe import MAX_DEPTH, MAX_NODES, MAX_NODE_BYTES
        self.assertLessEqual(MAX_DEPTH, 5)
        self.assertLessEqual(MAX_NODES, 120)
        self.assertLessEqual(MAX_NODE_BYTES, 0x1800)


if __name__ == "__main__":
    unittest.main()
