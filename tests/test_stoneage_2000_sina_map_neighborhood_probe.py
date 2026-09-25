import unittest
from tools.stoneage_2000_sina_map_neighborhood_probe import download_cgis,params

class Sina2000NeighborhoodTests(unittest.TestCase):
    def test_extract_cgi(self):
        page="https://games.sina.com.cn/downgames/map/x.shtml"
        body=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23681&filename=southisland_1228.zip&size=202">x</a>'
        got=download_cgis(page,body)
        self.assertEqual(len(got),1)
        p=params(got[0])
        self.assertEqual(p["aid"],"23681")
        self.assertEqual(p["filename"],"southisland_1228.zip")

if __name__=="__main__":unittest.main()
