import unittest
from tools.stoneage_waei_2001q4_payload_domain_probe import WINDOWS,EXTS,score

class Waei2001Q4PayloadTests(unittest.TestCase):
    def test_window_and_extensions(self):
        self.assertEqual(WINDOWS[0][1],"20011001")
        self.assertEqual(WINDOWS[-1][2],"20011231")
        self.assertEqual(set(EXTS),{"exe","zip","cab","rar"})

    def test_scoring_prefers_exact_setup(self):
        exact=score("http://download.waei.com.cn/stoneage/stoneage2.0setup.exe")
        generic=score("http://games.waei.com.cn/accessories/download/foo.exe")
        self.assertGreater(exact,generic)
        self.assertGreater(score("http://www.waei.com.cn/zhuanqu/stoneage2/update/sa20.exe"),0)

if __name__=="__main__":
    unittest.main()
