import struct
import unittest
import zlib

from tools.stoneage_inium_swf_probe import tokens, unpack_swf


class IniumSwfProbeTests(unittest.TestCase):
    def test_unpack_fws(self):
        payload = b"hello download/client.zip"
        data = b"FWS" + bytes([5]) + struct.pack("<I", 8 + len(payload)) + payload
        sig, version, declared, body = unpack_swf(data)
        self.assertEqual(sig, "FWS")
        self.assertEqual(version, 5)
        self.assertEqual(declared, len(data))
        self.assertEqual(body, data)

    def test_unpack_cws(self):
        payload = b"abc http://stoneage.enium.co.kr/download.html"
        declared = 8 + len(payload)
        data = b"CWS" + bytes([5]) + struct.pack("<I", declared) + zlib.compress(payload)
        sig, _, _, body = unpack_swf(data)
        self.assertEqual(sig, "CWS")
        self.assertTrue(body.startswith(b"FWS"))
        self.assertIn(b"download.html", body)

    def test_token_extraction(self):
        found = tokens(b"xxx http://stoneage.enium.co.kr/down/setup.exe yyy")
        values = {v for _, v in found}
        self.assertTrue(any("setup.exe" in v for v in values))


if __name__ == "__main__":
    unittest.main()
