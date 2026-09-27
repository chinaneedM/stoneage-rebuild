import unittest
from tools.stoneage_waei_subdomain_launch_census import TARGETS,LAUNCH_FROM,LAUNCH_TO,score,is_binary
class WaeiSubdomainTests(unittest.TestCase):
    def test_host(self):self.assertTrue(all("stoneage.waei.net" in u for _,u,*_ in TARGETS))
    def test_window(self):
        self.assertLessEqual(LAUNCH_FROM,"20010104");self.assertGreaterEqual(LAUNCH_TO,"20010104")
    def test_source_paths(self):
        urls=[x[1] for x in TARGETS]
        self.assertTrue(any("/saupdate/" in u for u in urls))
        self.assertTrue(any("newest.txt" in u for u in urls))
    def test_classify(self):
        self.assertTrue(is_binary("http://x/sa_3.exe"))
        self.assertGreater(score("http://x/saupdate/newest.txt"),1)
if __name__=="__main__":unittest.main()
