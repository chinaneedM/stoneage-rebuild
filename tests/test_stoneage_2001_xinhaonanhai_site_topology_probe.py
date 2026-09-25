import unittest
from tools.stoneage_2001_xinhaonanhai_site_topology_probe import same_domain,html_candidate,targetish,extract_urls

class XinhaonanhaiSiteTopologyTests(unittest.TestCase):
    def test_same_domain(self):
        self.assertTrue(same_domain("http://www.xinhaonanhai.com/a.htm"))
        self.assertTrue(same_domain("http://xinhaonanhai.com/a.htm"))
        self.assertFalse(same_domain("http://example.com/a.htm"))

    def test_html_candidate(self):
        self.assertTrue(html_candidate("http://www.xinhaonanhai.com/index.htm"))
        self.assertFalse(html_candidate("http://www.xinhaonanhai.com/a.zip"))

    def test_targetish(self):
        self.assertTrue(targetish("http://www.xinhaonanhai.com/stoneage/map.htm"))
        self.assertFalse(targetish("http://www.xinhaonanhai.com/about.htm"))

    def test_extract_frame_src(self):
        b=b'<frame src="stoneage/index.htm"><a href="download.htm">x</a>'
        r=extract_urls(b,"http://www.xinhaonanhai.com/")
        self.assertIn("http://www.xinhaonanhai.com/stoneage/index.htm",r)

if __name__=="__main__":
    unittest.main()
