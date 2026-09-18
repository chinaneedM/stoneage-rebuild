import tempfile
import struct
import unittest
from pathlib import Path

from tools.stoneage_rd_validate import validate


def adrn_record(bitmapno, adder, size, width, height):
    return struct.pack("<IIIiiII", bitmapno, adder, size, 0, 0, width, height) + bytes(80 - 28)


class StoneAgeRDValidateTests(unittest.TestCase):
    def test_real_blocks_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adrn = root / "adrn.bin"
            real = root / "real.bin"

            blocks = []
            records = []
            offset = 0

            # raw 2x2
            pixels0 = bytes([1, 2, 3, 4])
            block0 = b"RD" + bytes([0, 0]) + struct.pack("<III", 2, 2, 0x12345678) + pixels0
            blocks.append(block0)
            records.append(adrn_record(10, offset, len(block0), 2, 2))
            offset += len(block0)

            # compressed 4x2 -> [1,2,3,3,3,0,0,0]
            enc = bytes([0x02, 1, 2, 0x83, 3, 0xC3])
            block1 = b"RD" + bytes([1, 0]) + struct.pack("<III", 4, 2, 16 + len(enc)) + enc
            blocks.append(block1)
            records.append(adrn_record(11, offset, len(block1), 4, 2))
            offset += len(block1)

            real.write_bytes(b"".join(blocks))
            adrn.write_bytes(b"".join(records))

            result = validate(adrn, real, prefix_count=10, stride=1, tail_count=10)
            self.assertEqual(result["record_count"], 2)
            self.assertEqual(len(result["successes"]), 2)
            self.assertEqual(len(result["failures"]), 0)
            self.assertEqual(result["flag0_indices"], [0])


if __name__ == "__main__":
    unittest.main()
