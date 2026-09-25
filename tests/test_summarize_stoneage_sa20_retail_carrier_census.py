import unittest
from tools.summarize_stoneage_sa20_retail_carrier_census import parse

class RetailCarrierSummaryTests(unittest.TestCase):
    def test_parse_strict_and_resolution(self):
        s="\n".join([
          "TARGET|x=1",
          "IA_HIT|label=a|strict=1|identifier=good",
          "IA_HIT|label=b|strict=0|identifier=noise",
          "DM_HIT|q=x|strict=1|itemid=7",
          "ERROR|scope=x|kind=Timeout",
          "COUNT|ia_strict_items|1",
          "RESOLUTION|STRICT_RETAIL_CARRIER_CANDIDATE_FOUND|inspect",
        ])
        r=parse(s)
        self.assertEqual(len(r["strict_ia"]),1)
        self.assertEqual(len(r["strict_dm"]),1)
        self.assertEqual(len(r["errors"]),1)
        self.assertEqual(len(r["resolutions"]),1)

if __name__=="__main__":
    unittest.main()
