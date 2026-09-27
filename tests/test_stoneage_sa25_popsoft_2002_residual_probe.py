import unittest
import urllib.parse

from tools.stoneage_sa25_popsoft_2002_residual_probe import (
    PINNED_IDENTIFIERS,
    advanced_search_url,
    archive_file,
    feb_2002_file,
    ia_docs,
    metadata_url,
    optical_file,
    period_relevant_file,
    source_original,
)


class SA25Popsoft2002ResidualProbeTests(unittest.TestCase):
    def test_query_is_exactly_bounded_to_2002(self):
        parsed = urllib.parse.urlparse(advanced_search_url('"大众软件" AND year:2002'))
        query = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["q"], ['"大众软件" AND year:2002'])
        self.assertEqual(query["rows"], ["100"])

    def test_known_scan_family_is_pinned(self):
        self.assertIn("popsoft-magazine_202403", PINNED_IDENTIFIERS)
        self.assertTrue(metadata_url("popsoft-magazine_202403").endswith("popsoft-magazine_202403"))

    def test_file_classifiers(self):
        optical = {"name": "disc/GAME.iso", "source": "original"}
        scan = {"name": "2002/大众软件-2002年02月B_djvu.txt", "source": "derivative"}
        archive = {"name": "2002-02-disc.7z", "source": "original"}
        self.assertTrue(optical_file(optical))
        self.assertTrue(source_original(optical))
        self.assertTrue(period_relevant_file(scan))
        self.assertTrue(feb_2002_file(scan))
        self.assertTrue(archive_file(archive))
        self.assertTrue(feb_2002_file(archive))

    def test_ia_docs_filters_non_dict_rows(self):
        docs = ia_docs({"response": {"docs": [{"identifier": "x"}, "bad"]}})
        self.assertEqual(docs, ({"identifier": "x"},))


if __name__ == "__main__":
    unittest.main()
