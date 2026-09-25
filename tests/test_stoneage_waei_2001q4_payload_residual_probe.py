import unittest
from tools.stoneage_waei_2001q4_payload_residual_probe import WINDOWS,score

class Waei2001Q4PayloadResidualTests(unittest.TestCase):
    def test_residual_includes_november_exe(self):
        spans=[(s,e,x) for _,s,e,x in WINDOWS if x=="exe" and s.startswith("200111")]
        self.assertEqual(spans,[
          ("20011101","20011110","exe"),
          ("20011111","20011120","exe"),
          ("20011121","20011130","exe"),
        ])

    def test_scoring_exact_setup(self):
        self.assertGreater(score("http://www.waei.com.cn/a/stoneage2.0setup.exe"),20)
        self.assertEqual(score("http://www.waei.com.cn/a/logo.gif"),0)

if __name__=="__main__":
    unittest.main()
