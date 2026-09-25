import unittest
from tools.stoneage_sa40_discmaster_variant_probe import score
class VariantTests(unittest.TestCase):
    def test_scores_iso83(self):
        s,why=score({"fileid":"GAMES/SHIQI4UP.ZIP","size":3440*1024})
        self.assertGreaterEqual(s,15)
        self.assertIn("shiqi4",why)
if __name__=="__main__": unittest.main()
