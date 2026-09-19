import struct
import unittest

from tools.stoneage_tw10_pointer_callgraph_probe import pointer_chain


class TaiwanV10PointerCallgraphProbeTests(unittest.TestCase):
    def test_pointer_chain_follows_data_indirection(self):
        base = 0x400000
        data = bytearray(0x400)
        sections = [
            {"name": ".data", "raw": 0x100, "raw_size": 0x200, "rva": 0x3000, "vsize": 0x200},
        ]
        target_va = base + 0x3050
        ptr1_va = base + 0x3020
        ptr2_va = base + 0x3010

        # ptr1 location at raw 0x120 points to target, ptr2 at raw 0x110 points to ptr1.
        struct.pack_into("<I", data, 0x120, target_va)
        struct.pack_into("<I", data, 0x110, ptr1_va)

        layers = pointer_chain(bytes(data), base, sections, target_va, max_depth=3)
        self.assertGreaterEqual(len(layers), 2)
        self.assertEqual(layers[0][0]["va"], ptr1_va)
        self.assertEqual(layers[1][0]["va"], ptr2_va)

    def test_pointer_chain_stops_without_hits(self):
        base = 0x400000
        data = bytes(0x200)
        sections = [{"name": ".data", "raw": 0, "raw_size": 0x200, "rva": 0x3000, "vsize": 0x200}]
        layers = pointer_chain(data, base, sections, base + 0x3999, max_depth=3)
        self.assertEqual(layers, [[]])


if __name__ == "__main__":
    unittest.main()
