import unittest
from tools.stoneage_2000_sina_archived302_probe import substitute_filename, location

class Archived302ProbeTests(unittest.TestCase):
    def test_substitute_filename(self):
        u="http://download.example.com/maps/southisland_1228.zip"
        self.assertEqual(
            substitute_filename(u, "southisland_1228.zip"),
            "http://download.example.com/maps/samap_1220.zip",
        )

    def test_substitute_requires_source_filename(self):
        self.assertEqual(
            substitute_filename("http://download.example.com/maps/other.zip", "southisland_1228.zip"),
            "",
        )

    def test_location_case_insensitive(self):
        self.assertEqual(location({"Location": "http://example.com/x.zip"}), "http://example.com/x.zip")
        self.assertEqual(location({"location": "http://example.com/y.zip"}), "http://example.com/y.zip")

if __name__ == "__main__":
    unittest.main()
