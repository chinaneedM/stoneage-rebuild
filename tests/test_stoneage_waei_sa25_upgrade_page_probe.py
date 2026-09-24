import json, unittest, urllib.parse
from tools.stoneage_waei_sa25_upgrade_page_probe import TARGETS,extract,cdx_url,parse_cdx
class T(unittest.TestCase):
    def test_target(self):
        self.assertTrue(all(x.lower().endswith("/stoneage2/tyro/upgrade.asp") for x in TARGETS))
    def test_cdx(self):
        q=urllib.parse.parse_qs(urllib.parse.urlparse(cdx_url(TARGETS[0])).query)
        self.assertEqual(q["from"],["20020115"])
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["20020201","x"]]).encode()
        self.assertEqual(parse_cdx(b)[0]["timestamp"],"20020201")
    def test_extract(self):
        b='<body>石器时代2.5 完整升级版580兆 <a href="http://x/sa25.exe">下载</a></body>'.encode("gb18030")
        terms,hrefs,ex=extract(b,TARGETS[0])
        self.assertIn("石器时代2.5",terms); self.assertEqual(hrefs[0][1],"http://x/sa25.exe"); self.assertTrue(ex)
if __name__=="__main__": unittest.main()
