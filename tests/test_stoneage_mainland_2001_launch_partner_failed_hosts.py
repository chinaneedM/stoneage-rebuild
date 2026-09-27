import unittest
from tools.stoneage_mainland_2001_launch_partner_failed_hosts import SURFACES, DAYS, score

class T(unittest.TestCase):
    def test_scope(self):
        self.assertEqual(len(SURFACES),3)
        self.assertEqual(DAYS[0],"20010115")
        self.assertEqual(DAYS[-1],"20010119")

    def test_failed_hosts_only(self):
        roots={r for _,r in SURFACES}
        self.assertEqual(roots,{
            "http://games.sina.com.cn/",
            "http://game.china.com/",
            "http://download.21cn.com/",
        })

    def test_score(self):
        s,h=score({"original":"http://games.sina.com.cn/shiqi/client.zip","redirect":""})
        self.assertGreaterEqual(s,70)
        self.assertIn("shiqi",h)
        self.assertIn("binary-ext",h)

if __name__=="__main__":
    unittest.main()
