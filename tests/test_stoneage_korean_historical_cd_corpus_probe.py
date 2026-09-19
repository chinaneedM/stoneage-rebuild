import unittest

from tools.stoneage_korean_historical_cd_corpus_probe import (
    carrier_files,
    likely_period_korean,
)


class KoreanHistoricalCdCorpusProbeTests(unittest.TestCase):
    def test_carrier_files_filters_disc_images(self):
        rows=carrier_files([
            {"name":"disc1.iso","size":"123"},
            {"name":"cover.jpg","size":"456"},
            {"name":"track01.bin","size":"789"},
        ])
        self.assertEqual([x["name"] for x in rows],["disc1.iso","track01.bin"])

    def test_period_korean_candidate(self):
        self.assertTrue(likely_period_korean({
            "title":"NetPower Korea 2000-10 CD-ROM",
            "date":"2000-10-01",
        }))

    def test_unrelated_item_rejected(self):
        self.assertFalse(likely_period_korean({
            "title":"Japanese demo disc",
            "date":"2000-10-01",
        }))


if __name__=="__main__":
    unittest.main()
