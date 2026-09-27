import unittest
from tools.stoneage_computer_news_2001_issue1_article_probe import URL,TOKENS,visible

class T(unittest.TestCase):
    def test_target(self):
        self.assertIn("/2001/01/63220.html",URL)
    def test_tokens(self):
        self.assertIn("石器时代",TOKENS)
        self.assertIn("光盘",TOKENS)
    def test_visible(self):
        self.assertEqual(visible("<p>石器时代</p>"),"石器时代")

if __name__=="__main__":
    unittest.main()
