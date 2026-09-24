import unittest
from tools.stoneage_japan2004_redump_probe import (
    MODERN_TARGETS,
    matching_rows,
    result_count,
)

class Japan2004RedumpProbeTests(unittest.TestCase):
    def test_identifiers_are_pinned(self):
        targets=dict(MODERN_TARGETS)
        self.assertEqual(targets["serial-model"]["serial"],"WR-04156")
        self.assertEqual(targets["serial-model"]["serial_exact"],"1")
        self.assertEqual(targets["barcode-jan"]["barcode"],"4988609011565")
        self.assertEqual(targets["barcode-jan"]["barcode_exact"],"1")

    def test_matching_rows(self):
        body=b"<table><tr><td>Other</td></tr><tr><td>StoneAge</td><td>WR-04156</td></tr></table>"
        self.assertEqual(len(matching_rows(body)),1)

    def test_result_count_legacy_shape(self):
        self.assertEqual(result_count("Displaying results 1 - 2 of 2"),2)

    def test_result_count_modern_shape(self):
        self.assertEqual(result_count("12 discs found"),12)

if __name__=="__main__":
    unittest.main()
