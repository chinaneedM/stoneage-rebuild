import unittest
from tools.stoneage_waei_runtime_generation_census import GENERATIONS,original,cdx_url

class RuntimeGenerationCensusTests(unittest.TestCase):
    def test_grounded_generations(self):
        vals={n for _r,n in GENERATIONS}
        self.assertTrue({3,23,24,25,40,41,42}.issubset(vals))
    def test_path(self):
        self.assertEqual(original("stoneage.waei.net",24),"http://stoneage.waei.net/saupdate/sa_24.exe")
    def test_exact(self):
        self.assertIn("matchType=exact",cdx_url(original("stoneage.waei.net",24)))

if __name__=="__main__":unittest.main()
