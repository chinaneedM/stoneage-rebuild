import unittest
from tools.stoneage_waei_early_news_article_probe import ARTICLES,relevant
class T(unittest.TestCase):
    def test_ids(self): self.assertEqual([x[0] for x in ARTICLES],[416,469])
    def test_relevant(self): self.assertTrue(relevant("http://x/download.asp?fileid=1","下載"))
if __name__=="__main__":unittest.main()
