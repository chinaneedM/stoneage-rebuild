import struct
import unittest

from tools.stoneage_mapexe_wayback_probe import CAPTURE_TS, TARGET, hget, pe_info


class MapExeWaybackProbeTests(unittest.TestCase):
    def test_exact_target_and_capture(self):
        self.assertEqual(TARGET,"http://www.wuxitianlong.com:80/sa/map.exe")
        self.assertEqual(CAPTURE_TS,"20030623234451")

    def test_header_lookup_is_case_insensitive(self):
        self.assertEqual(hget({"Content-range":"bytes 0-9/100"},"Content-Range"),"bytes 0-9/100")
        self.assertEqual(hget({"X-archive-orig-content-length":"123"},"X-Archive-Orig-Content-Length"),"123")

    def test_pe_parser(self):
        b=bytearray(256)
        b[:2]=b"MZ"
        struct.pack_into("<I",b,0x3c,128)
        b[128:132]=b"PE\x00\x00"
        struct.pack_into("<HHI",b,132,0x14c,3,1040955668)
        info=pe_info(bytes(b))
        self.assertEqual(info["machine"],0x14c)
        self.assertEqual(info["sections"],3)
        self.assertEqual(info["timestamp"],1040955668)


if __name__=="__main__":
    unittest.main()
