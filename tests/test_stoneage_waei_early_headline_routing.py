import unittest
from tools.stoneage_waei_early_headline_routing import raw_tokens,visible
class T(unittest.TestCase):
    def test_tokens(self):
        x=raw_tokens('<a href="news.asp?id=12" onclick="go(12)">免費測試</a>')
        self.assertIn(("href","news.asp?id=12"),x)
    def test_visible(self): self.assertIn("免費測試",visible("<b>免費測試</b>"))
if __name__=="__main__":unittest.main()
