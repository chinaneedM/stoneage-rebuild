import unittest
import urllib.parse

from tools.stoneage_sa25_distribution_carrier_probe import (
    DISCM_QUERIES,
    IA_QUERIES,
    discmaster_rows,
    discmaster_url,
    ia_docs,
    likely_stoneage,
)

class SA25DistributionCarrierProbeTests(unittest.TestCase):
    def test_queries_pin_version_and_carrier_surfaces(self):
        labels={x[0] for x in DISCM_QUERIES}
        self.assertIn("stoneage25-content",labels)
        self.assertIn("spirit-king-content",labels)
        ia_labels={x[0] for x in IA_QUERIES}
        self.assertIn("popular-software-2002",ia_labels)

    def test_discmaster_url_is_time_bounded(self):
        parsed=urllib.parse.urlparse(discmaster_url('"StoneAge 2.5"',"t"))
        q=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(q["tsMin"],["2000"])
        self.assertEqual(q["tsMax"],["2003"])

    def test_rows_and_relevance(self):
        value={"results":[
            {"itemid":"1","itemName":"disc","fileid":"x/StoneAge2.5/setup.exe"},
            {"itemid":"2","itemName":"disc","fileid":"x/other/setup.exe"},
        ]}
        rows=discmaster_rows(value)
        self.assertEqual(len(rows),2)
        self.assertTrue(likely_stoneage(rows[0]))
        self.assertFalse(likely_stoneage(rows[1]))

    def test_ia_docs(self):
        docs=ia_docs({"response":{"docs":[{"identifier":"x"}]}})
        self.assertEqual(docs[0]["identifier"],"x")

if __name__=="__main__":
    unittest.main()
