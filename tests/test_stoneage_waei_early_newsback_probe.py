import unittest
from tools.stoneage_waei_early_newsback_probe import relevant,MONTHS
class T(unittest.TestCase):
    def test_months(self): self.assertIn((2000,12),MONTHS)
    def test_relevant(self): self.assertTrue(relevant("http://x/newsdetail.asp?id=1","免費測試石器時代"))
if __name__=="__main__":unittest.main()
