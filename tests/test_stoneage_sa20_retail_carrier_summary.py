import unittest
from tools.stoneage_sa20_retail_carrier_summary import summarize

class SA20RetailCarrierSummaryTests(unittest.TestCase):
    def test_keeps_only_audit_rows(self):
        src="""StoneAge 2.0 retail client-disc preservation census — R1
SCOPE|x
IA_QUERY|label=x|rows=2
IA_HIT|label=x|strict=0|identifier=noise
IA_HIT|label=x|strict=1|identifier=target
DM_HIT|q=x|strict=1|itemid=1
COUNT|ia_strict_items|1
ERROR|scope=x|kind=Timeout
RESOLUTION|STRICT_RETAIL_CARRIER_CANDIDATE_FOUND|x
EVIDENCE_BOUNDARY|x
"""
        out=summarize(src)
        self.assertIn("strict=1|identifier=target",out)
        self.assertIn("DM_HIT|q=x|strict=1",out)
        self.assertNotIn("strict=0",out)
        self.assertNotIn("IA_QUERY",out)
        self.assertIn("COUNT|ia_strict_items|1",out)
        self.assertIn("ERROR|",out)

if __name__=="__main__":
    unittest.main()
