import unittest

from tools.stoneage_stoneage5_msi_probe import MAX_MSI_BYTES, find_entry


class Stoneage5MsiProbeTests(unittest.TestCase):
    def test_msi_bound_is_small_relative_to_disc(self):
        self.assertEqual(MAX_MSI_BYTES, 2 * 1024 * 1024)

    def test_find_entry_is_case_insensitive(self):
        rows = [
            {"name": "README.TXT", "size": 1},
            {"name": "STA5.MSI", "size": 782908},
        ]
        self.assertEqual(find_entry(rows, "sta5.msi")["size"], 782908)
        self.assertIsNone(find_entry(rows, "missing.msi"))


if __name__ == "__main__":
    unittest.main()
