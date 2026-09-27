import unittest
from tools.stoneage_17173_launch_download_archive_probe import (
    EXACT_URLS, PREFIX_URLS, FROM, TO, cdx_url,
)

class Test17173LaunchDownloadArchiveProbe(unittest.TestCase):
    def test_launch_window_and_anchor(self):
        self.assertEqual(FROM,"20001201")
        self.assertEqual(TO,"20010228")
        self.assertIn("http://www.17173.com/shiqi/xiazai/xiazai.htm",EXACT_URLS)
    def test_prefixes(self):
        self.assertIn("http://www.17173.com/shiqi/xiazai/",PREFIX_URLS)
        q=cdx_url(EXACT_URLS[0],"exact")
        self.assertIn("matchType=exact",q)

if __name__=="__main__":
    unittest.main()
