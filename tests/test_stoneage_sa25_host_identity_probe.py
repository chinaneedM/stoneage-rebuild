import unittest

from tools.stoneage_sa25_host_identity_probe import (
    PAGES, declared_charset, hostnames, replay_url, title
)


class SA25HostIdentityProbeTests(unittest.TestCase):
    def test_root_capture_pinned(self):
        self.assertEqual(PAGES[0][1],"20011227124446")
        self.assertEqual(PAGES[0][2],"http://202.104.32.168:80/")

    def test_replay_raw(self):
        self.assertIn("20011227124446id_",replay_url(PAGES[0][1],PAGES[0][2]))

    def test_declared_charset(self):
        self.assertEqual(
            declared_charset(b'<meta http-equiv="Content-Type" content="text/html; charset=gb2312">'),
            "gb2312",
        )

    def test_title(self):
        self.assertEqual(title("<title>软件下载中心</title>"),"软件下载中心")

    def test_hostnames(self):
        hs=hostnames('<a href="http://example.com/a">x</a><img src="http://202.104.32.168/x.gif">')
        self.assertIn("example.com",hs)
        self.assertIn("202.104.32.168",hs)


if __name__=="__main__":
    unittest.main()
