import unittest
from tools.stoneage_waei_sa25_generation_retry import TARGET,url
class Sa25RetryTests(unittest.TestCase):
    def test_target(self): self.assertTrue(TARGET.endswith("/saupdate/sa_25.exe"))
    def test_exact(self): self.assertIn("matchType=exact",url())
if __name__=="__main__":unittest.main()
