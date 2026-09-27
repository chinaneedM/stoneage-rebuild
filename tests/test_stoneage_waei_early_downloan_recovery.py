import unittest
from tools.stoneage_waei_early_downloan_recovery import TARGETS,score,cdx_url
class DownLoanTests(unittest.TestCase):
    def test_target(self): self.assertTrue(all("wgs/stoneage/content/down_loan.htm" in x for x in TARGETS))
    def test_score(self): self.assertGreaterEqual(score("ftp://x/stoneage/setup.exe"),9)
    def test_exact(self): self.assertIn("matchType=exact",cdx_url(TARGETS[0]))
if __name__=="__main__":unittest.main()
