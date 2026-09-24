import unittest
from tools.stoneage_japan2004_redump_probe import TARGETS, matching_rows, result_count

class Japan2004RedumpProbeTests(unittest.TestCase):
    def test_identifiers_are_pinned(self):
        paths=dict(TARGETS)
        self.assertIn("WR-04156",paths["model"])
        self.assertIn("4988609011565",paths["barcode"])

    def test_matching_rows(self):
        body=b"<table><tr><td>Other</td></tr><tr><td>StoneAge</td><td>WR-04156</td></tr></table>"
        self.assertEqual(len(matching_rows(body)),1)

    def test_result_count(self):
        self.assertEqual(result_count("Displaying results 1 - 2 of 2"),2)

if __name__=="__main__":
    unittest.main()
