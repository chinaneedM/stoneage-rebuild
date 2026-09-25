import unittest
from tools.stoneage_sina_download_cgi_topology_census import map_row, directish, body_links

class SinaDownloadTopologyCensusTests(unittest.TestCase):
    def test_map_row(self):
        row={"original":"http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23223&filename=samap_1220.zip&size=1410"}
        got=map_row(row)
        self.assertIsNotNone(got)
        self.assertEqual(got["aid"],23223)
        self.assertEqual(got["filename"],"samap_1220.zip")

    def test_non_map_rejected(self):
        row={"original":"http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=demo&aid=1&filename=x.exe"}
        self.assertIsNone(map_row(row))

    def test_directish_excludes_login_gateway(self):
        self.assertFalse(directish("http://login.games.sina.com.cn/index.php?reurl=http%3A%2F%2Fx%2Ffoo.zip"))
        self.assertTrue(directish("http://down.example.com/maps/foo.zip"))
        self.assertTrue(directish("ftp://ftp.example.com/foo.exe"))

    def test_body_links(self):
        b=b'<a href="http://down.example.com/maps/foo.zip">x</a><a href="/help.html">h</a>'
        self.assertEqual(body_links(b,"http://games.sina.com.cn/"),("http://down.example.com/maps/foo.zip",))

if __name__=="__main__":
    unittest.main()
