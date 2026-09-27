import unittest
from tools.stoneage_china2001_jan5_mailorder_route_probe import DATES, HOSTS, prefix, cdx_url, score


class TestChinaJan5MailorderRoute(unittest.TestCase):
    def test_date_window(self):
        self.assertEqual(DATES,("20010104","20010105","20010106"))

    def test_proven_route_family(self):
        p=prefix("game.china.com","20010105")
        self.assertEqual(p,"http://game.china.com/zh_cn/news/news1/444/20010105/")
        self.assertIn("matchType=prefix",cdx_url("game.china.com","20010105"))

    def test_target_scoring(self):
        self.assertGreaterEqual(score("中华网游戏频道 石器时代 邮购 试玩版赠送"),20)


if __name__=="__main__":
    unittest.main()
