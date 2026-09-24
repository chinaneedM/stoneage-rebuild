import unittest
from tools.stoneage_sa25_wanfang_disc_probe import QUERIES,strict_match

class WanfangDiscProbeTests(unittest.TestCase):
    def test_exact_identifiers_present(self):
        self.assertIn("7-900096-07-8",QUERIES)
        self.assertIn("9787900096074",QUERIES)

    def test_isbn_is_strict(self):
        self.assertTrue(strict_match("ISBN 7-900096-07-8/Z.03"))

    def test_title_and_publisher_are_strict_together(self):
        self.assertTrue(strict_match("万方数据电子出版社 永远的石器时代2.5 精灵王传说"))
        self.assertFalse(strict_match("石器时代2.5 精灵王传说 私服客户端"))
        self.assertFalse(strict_match("万方数据电子出版社 其他软件"))

if __name__=="__main__":
    unittest.main()
