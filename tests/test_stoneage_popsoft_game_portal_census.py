import unittest
from tools.stoneage_popsoft_game_portal_census import FROM,TO,TARGETS,hint_score,is_binary
class PopsoftPortalTests(unittest.TestCase):
    def test_window(self):
        self.assertLessEqual(FROM,"20001215");self.assertGreaterEqual(TO,"20010112")
    def test_source_host(self):
        self.assertTrue(all("game.popsoft.com.cn" in u for _,u,_ in TARGETS))
    def test_hints(self):
        self.assertGreater(hint_score("http://game.popsoft.com.cn/download/stoneage/setup.exe"),2)
        self.assertTrue(is_binary("http://x/a.zip"))
if __name__=="__main__":unittest.main()
