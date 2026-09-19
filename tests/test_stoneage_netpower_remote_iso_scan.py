import struct
import unittest

from tools.stoneage_netpower_remote_iso_scan import (
    NEEDLE,
    candidate,
    decode_name,
    parse_directory,
    root_record,
)


def dir_record(name: bytes, lba: int, size: int, is_dir: bool = False) -> bytes:
    n = len(name)
    length = 33 + n + (1 if n % 2 == 0 else 0)
    rec = bytearray(length)
    rec[0] = length
    struct.pack_into("<I", rec, 2, lba)
    struct.pack_into(">I", rec, 6, lba)
    struct.pack_into("<I", rec, 10, size)
    struct.pack_into(">I", rec, 14, size)
    rec[25] = 0x02 if is_dir else 0
    rec[28:30] = (1).to_bytes(2, "little")
    rec[30:32] = (1).to_bytes(2, "big")
    rec[32] = n
    rec[33:33+n] = name
    return bytes(rec)


class NetPowerRemoteIsoScanTests(unittest.TestCase):
    def test_candidate_requires_korean_netpower_and_period(self):
        self.assertTrue(candidate({"title": "NetPower 2001.12 CD", "creator": "제우미디어"}))
        self.assertFalse(candidate({"title": "The Net Power CD August 1996"}))

    def test_decode_primary_and_joliet_names(self):
        self.assertEqual(decode_name(b"STONEAGE.EXE;1"), "STONEAGE.EXE")
        self.assertEqual(decode_name("스톤에이지".encode("utf-16-be"), True), "스톤에이지")

    def test_parse_directory_and_match(self):
        data = bytearray(2048)
        r1 = dir_record(b"STONEAGE", 40, 2048, True)
        r2 = dir_record(b"SA_DEMO.EXE;1", 41, 12345, False)
        data[0:len(r1)] = r1
        data[len(r1):len(r1)+len(r2)] = r2
        rows = parse_directory(bytes(data), False)
        self.assertEqual(rows[0], ("STONEAGE", 40, 2048, True))
        self.assertEqual(rows[1], ("SA_DEMO.EXE", 41, 12345, False))
        self.assertTrue(NEEDLE.search(rows[0][0]))
        self.assertTrue(NEEDLE.search(rows[1][0]))

    def test_root_record(self):
        vd = bytearray(2048)
        root = dir_record(b"\x00", 77, 4096, True)
        vd[156:156+len(root)] = root
        self.assertEqual(root_record(bytes(vd)), (77, 4096))


if __name__ == "__main__":
    unittest.main()
