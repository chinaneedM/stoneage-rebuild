import unittest
from tools.stoneage_2000_sina_host_alias_probe import HOSTS, relevant, params

class HostAliasProbeTests(unittest.TestCase):
    def test_hosts(self):
        self.assertIn("games.sina.com.cn",HOSTS)
        self.assertIn("games1.sina.com.cn",HOSTS)

    def test_relevant_by_aid(self):
        self.assertTrue(relevant({"original":"http://games.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23223"}))

    def test_relevant_by_filename(self):
        self.assertTrue(relevant({"original":"http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?filename=samap_1220.zip"}))

    def test_params(self):
        p=params("http://x/download.pl?aid=1&col=map")
        self.assertEqual(p["col"],"map")

if __name__=="__main__":
    unittest.main()
