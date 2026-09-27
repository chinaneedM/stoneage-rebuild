import unittest
from tools.stoneage_china2000_zhcn_download_residual import TS, ORIG, replay_url


class TestChinaComDownloadResidual(unittest.TestCase):
    def test_exact_target(self):
        self.assertEqual(TS, "20001219123000")
        self.assertEqual(ORIG, "http://game.china.com:80/zh_cn/download/pic/a_1.html")

    def test_replay(self):
        url=replay_url()
        self.assertIn(TS+"id_",url)
        self.assertIn("/zh_cn/download/pic/a_1.html",url)


if __name__=="__main__":
    unittest.main()
