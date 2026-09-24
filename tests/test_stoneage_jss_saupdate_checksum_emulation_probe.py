import unittest
import zlib

from tools.stoneage_jss_saupdate_checksum_emulation_probe import candidate_values


class JssSaUpdateChecksumEmulationProbeTests(unittest.TestCase):
    def test_candidate_values(self):
        out=candidate_values(b"abc")
        self.assertEqual(out["sum32"],294)
        self.assertEqual(out["crc32"],zlib.crc32(b"abc")&0xffffffff)
        self.assertEqual(out["len"],3)


if __name__=="__main__":
    unittest.main()
