import unittest
from tools import stoneage_jss1999_pet_source_census as census


class Pet31SourceCensus(unittest.TestCase):
    def test_unqualified_source_rejected(self):
        with self.assertRaises(ValueError):
            census.build(b"fake", census.URL)

    def test_unqualified_capture_rejected(self):
        with self.assertRaises(ValueError):
            census.build(b"fake", census.URL.replace("20010417162544", "20000101120000"))

    def test_no_auto_species_from_literal(self):
        self.assertIn("GAME_PET_NAME_URIURI", census.LABELS)
        self.assertIn("PET", census.LABELS)
        self.assertIn("プレゼント", census.LABELS.values())

    def test_same_1999_record_counts_separate_from_pet_species(self):
        self.assertEqual(census.SOURCE_BYTES, 11239)
        self.assertEqual(len(census.SHA), 64)


if __name__ == "__main__":
    unittest.main()
