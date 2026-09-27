import unittest
from tools.stoneage_waei_net_2000_trial_probe import (
    html_candidate,is_binary,relevant_url,score,semantics,target_link
)

class WaeiNet2000TrialProbeTests(unittest.TestCase):
    def test_relevant(self):
        self.assertTrue(relevant_url("http://www7.waei.net/wgs/stoneage/index.htm"))
        self.assertTrue(relevant_url("http://stoneage.waei.net/"))
        self.assertFalse(relevant_url("http://www7.waei.net/wgs/other/logo.gif"))

    def test_binary(self):
        self.assertTrue(is_binary("http://x/client.exe?mirror=1"))
        self.assertFalse(is_binary("http://x/index.asp"))

    def test_semantics_274(self):
        s,d,z,sem=semantics("<html>石器时代 试玩版 下载 274 MB</html>")
        self.assertTrue(s);self.assertTrue(d);self.assertTrue(z);self.assertTrue(sem)

    def test_score_prefers_trial_binary(self):
        good={"original":"http://www7.waei.net/wgs/stoneage/download/trial.exe","mimetype":"application/octet-stream","timestamp":"20010104000101"}
        bad={"original":"http://www7.waei.net/wgs/stoneage/images/logo.gif","mimetype":"image/gif","timestamp":"20010104000101"}
        self.assertGreater(score(good),score(bad))

    def test_target_link(self):
        self.assertTrue(target_link("http://x/sa_trial.zip","下载试玩版"))
        self.assertFalse(target_link("http://x/images/wallpaper.jpg","石器时代壁纸"))

if __name__=="__main__":
    unittest.main()
