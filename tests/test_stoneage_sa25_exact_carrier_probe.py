import unittest
from tools.stoneage_sa25_exact_carrier_probe import TARGETS,strict_match,target_tokens,interesting_files

class ExactCarrierTests(unittest.TestCase):
    def test_source_targets_cover_products_and_periodicals(self):
        labels={x[0] for x in TARGETS}
        self.assertIn("newbie-pack",labels)
        self.assertIn("spring-pack",labels)
        self.assertIn("longevity-pack",labels)
        self.assertIn("popular-games",labels)
        self.assertIn("tengtu-guide",labels)
        self.assertIn("bombing-chicken-game",labels)
        bombing=next(x for x in TARGETS if x[0]=="bombing-chicken-game")
        self.assertIn("哇靠轰炸鸡",bombing[1])
        self.assertIn("2001C226 哇靠轰炸鸡",bombing[1])

    def test_product_strict_matching(self):
        self.assertTrue(strict_match("spring-pack",("石器时代2.5春满钱坤包",),"product","石器时代2.5 春满钱坤包 客户端光盘"))
        self.assertFalse(strict_match("spring-pack",("石器时代2.5春满钱坤包",),"product","春满花开"))

    def test_periodical_strict_matching(self):
        qs=("家庭电脑世界 2002年2月","家庭电脑世界 2002")
        self.assertTrue(strict_match("home-computer-world",qs,"periodical","家庭电脑世界 2002年2月 光盘"))
        self.assertFalse(strict_match("home-computer-world",qs,"periodical","家庭电脑世界 2004年"))

    def test_crosspromo_strict_matching(self):
        qs=("轰炸鸡","轰炸鸡 华义","Chicken Shoot Waei")
        self.assertTrue(strict_match("bombing-chicken-game",qs,"crosspromo","北京华义 轰炸鸡 石器时代 促销光盘"))
        self.assertTrue(strict_match("bombing-chicken-game",qs,"crosspromo","Waei Chicken Shoot StoneAge bonus disc"))
        self.assertFalse(strict_match("bombing-chicken-game",qs,"crosspromo","Chicken Shoot 2002 Lithuanian CD"))
        self.assertFalse(strict_match("bombing-chicken-game",qs,"crosspromo","2001C226 哇靠轰炸鸡完美中文版 华议国际"))

    def test_interesting_disc_files(self):
        meta={"files":[{"name":"disc.iso"},{"name":"cover.jpg"},{"name":"setup.exe"}]}
        names=[x["name"] for x in interesting_files(meta)]
        self.assertEqual(names,["disc.iso","setup.exe"])

if __name__=="__main__": unittest.main()
