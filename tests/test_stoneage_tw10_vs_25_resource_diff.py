import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_tw10_vs_25_resource_diff import common_prefix_bytes, parse_adrn


class TaiwanV10Vs25ResourceDiffTests(unittest.TestCase):
    def test_common_prefix(self):
        self.assertEqual(common_prefix_bytes(b"abc", b"abc"), 3)
        self.assertEqual(common_prefix_bytes(b"abcdef", b"abcXYZ"), 3)
        self.assertEqual(common_prefix_bytes(b"", b"x"), 0)

    def test_parse_adrn(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"a.bin"
            rec=bytearray(80)
            struct.pack_into("<IIIiiii",rec,0,7,100,20,-1,-2,64,48)
            p.write_bytes(rec)
            rows=parse_adrn(p)
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]["bitmapno"],7)
            self.assertEqual(rows[0]["adder"],100)
            self.assertEqual(rows[0]["width"],64)
            self.assertEqual(rows[0]["height"],48)


if __name__=="__main__":
    unittest.main()
