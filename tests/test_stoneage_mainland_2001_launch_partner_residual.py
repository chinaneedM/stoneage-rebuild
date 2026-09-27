import unittest
from tools.stoneage_mainland_2001_launch_partner_residual import SURFACES, FROM, TO, score

class T(unittest.TestCase):
    def test_window(self):
        self.assertEqual((FROM,TO),("20010115","20010119"))

    def test_narrow_hosts(self):
        roots={r for _,r,_,_ in SURFACES}
        self.assertIn("http://games.sina.com.cn/",roots)
        self.assertIn("http://game.china.com/",roots)
        self.assertIn("http://games.sohu.com/",roots)

    def test_score(self):
        s,h=score({"original":"http://games.sina.com.cn/stoneage/client.zip","redirect":""})
        self.assertGreaterEqual(s,70)
        self.assertIn("stoneage",h)
        self.assertIn("binary-ext",h)

if __name__=="__main__":
    unittest.main()
