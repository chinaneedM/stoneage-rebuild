import unittest
from tools.stoneage_mainland_2001_launch_partner_census import PORTALS, FROM, TO, score

class T(unittest.TestCase):
    def test_window(self):
        self.assertEqual(FROM,"20010115")
        self.assertEqual(TO,"20010119")

    def test_confirmed_domains(self):
        domains={d for _,d in PORTALS}
        for d in ("sina.com.cn","163.com","sohu.com","china.com","21cn.com","enet.com.cn","21vianet.com","yesky.com"):
            self.assertIn(d,domains)

    def test_stoneage_scoring(self):
        s,h=score({"original":"http://x/game/stoneage/download/client.exe","mimetype":"application/octet-stream","redirect":""})
        self.assertGreaterEqual(s,60)
        self.assertIn("stoneage",h)
        self.assertIn("binary-ext",h)

if __name__=="__main__":
    unittest.main()
