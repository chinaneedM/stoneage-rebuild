import struct
import unittest

from tools.stoneage_rd_codec import RDDecodeError, decode_legacy_rle, decode_rd_block


class StoneAgeRDCodecTests(unittest.TestCase):
    def test_all_nine_rle_control_families(self):
        encoded = bytearray()
        encoded += bytes([0x03, 1, 2, 3])
        encoded += bytes([0x10, 0x10]) + bytes(range(16))
        encoded += bytes([0x20, 0x00, 0x11]) + bytes(range(17))
        encoded += bytes([0x84, 0x7A])
        encoded += bytes([0x90, 0x55, 0x10])
        encoded += bytes([0xA0, 0x33, 0x00, 0x11])
        encoded += bytes([0xC4])
        encoded += bytes([0xD0, 0x10])
        encoded += bytes([0xE0, 0x00, 0x11])

        expected = (
            bytes([1, 2, 3])
            + bytes(range(16))
            + bytes(range(17))
            + bytes([0x7A]) * 4
            + bytes([0x55]) * 16
            + bytes([0x33]) * 17
            + bytes(4)
            + bytes(16)
            + bytes(17)
        )
        self.assertEqual(decode_legacy_rle(bytes(encoded)), expected)

    def test_compressed_rd_block(self):
        encoded = bytes([0x02, 1, 2, 0x83, 3, 0xC3])
        size = 16 + len(encoded)
        block = b"RD" + bytes([1, 0]) + struct.pack("<III", 4, 2, size) + encoded
        header, pixels = decode_rd_block(block)
        self.assertEqual(header["flag"], 1)
        self.assertEqual(pixels, bytes([1, 2, 3, 3, 3, 0, 0, 0]))

    def test_raw_rd_uses_authoritative_container_size(self):
        pixels = bytes(range(8))
        block = b"RD" + bytes([0, 0]) + struct.pack("<III", 4, 2, 0x0083942C) + pixels
        header, decoded = decode_rd_block(block, authoritative_block_size=24)
        self.assertEqual(header["flag"], 0)
        self.assertEqual(decoded, pixels)

    def test_invalid_control_rejected(self):
        with self.assertRaises(RDDecodeError):
            decode_legacy_rle(bytes([0x70]))


if __name__ == "__main__":
    unittest.main()
