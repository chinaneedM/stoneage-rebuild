import unittest
from tools.stoneage_jss_saupdate_manifest_record_probe import (
    ARRAY_META_END, ARRAY_META_START, ARRAY_TEXT_START, CHECKSUM_RVA, STRIDE,
)

class JssSaUpdateManifestRecordProbeTests(unittest.TestCase):
    def test_record_layout_constants(self):
        self.assertEqual(STRIDE,0x114)
        self.assertEqual(ARRAY_TEXT_START,0x407C50)
        self.assertEqual(ARRAY_META_START,0x407D50)
        self.assertEqual(ARRAY_META_END,0x857D50)
        self.assertEqual(CHECKSUM_RVA,0x3F20)

if __name__=="__main__":
    unittest.main()
