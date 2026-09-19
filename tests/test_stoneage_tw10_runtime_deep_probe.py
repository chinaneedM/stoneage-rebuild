import tempfile
import unittest
from pathlib import Path

from tools.stoneage_tw10_runtime_deep_probe import (
    first_diff,
    rva_from_file_offset,
)


class TaiwanV10RuntimeDeepProbeTests(unittest.TestCase):
    def test_first_diff(self):
        self.assertEqual(first_diff(b"abc", b"abc"), -1)
        self.assertEqual(first_diff(b"abc", b"axc"), 1)
        self.assertEqual(first_diff(b"abc", b"abcd"), 3)

    def test_rva_mapping(self):
        pe = {
            "sections": [
                {"raw_ptr": 0x400, "raw_size": 0x200, "virtual_addr": 0x1000, "name": ".text"},
                {"raw_ptr": 0x600, "raw_size": 0x100, "virtual_addr": 0x3000, "name": ".rdata"},
            ]
        }
        self.assertEqual(rva_from_file_offset(pe, 0x420), (0x1020, ".text"))
        self.assertEqual(rva_from_file_offset(pe, 0x650), (0x3050, ".rdata"))
        self.assertEqual(rva_from_file_offset(pe, 0x100), (None, ""))


if __name__ == "__main__":
    unittest.main()
