import unittest
from tools.stoneage_sa25_smzdm_disc_order_probe import section, records

class T(unittest.TestCase):
    def test_order(self):
        s="游戏安装光盘 2.0<img src='https://x/20.jpg'> 接着是2.5<img src='https://x/25.jpg'>游戏说明书"
        seg,_,_=section(s)
        r=records(seg)
        self.assertEqual([x[0] for x in r],["https://x/20.jpg","https://x/25.jpg"])
        self.assertIn("接着是2.5",r[1][1])

if __name__=="__main__":
    unittest.main()
