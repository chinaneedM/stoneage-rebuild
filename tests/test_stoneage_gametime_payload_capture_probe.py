import unittest

from tools.stoneage_gametime_payload_capture_probe import (
    host_variants,
    signature,
)


class GameTimePayloadCaptureProbeTests(unittest.TestCase):
    def test_signature_detects_zip_and_pe(self):
        self.assertEqual(signature(b"PK\x03\x04rest"),"zip-local-header")
        self.assertEqual(signature(b"MZrest"),"pe-mz")

    def test_host_variants_toggle_www(self):
        rows=host_variants(
            "http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip"
        )
        self.assertEqual(len(rows),2)
        self.assertIn("www.gametime.co.kr",rows[0])
        self.assertIn("gametime.co.kr/images",rows[1])


if __name__=="__main__":
    unittest.main()
