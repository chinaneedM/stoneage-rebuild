import json, unittest, urllib.parse
from tools.stoneage_sa25_21cn_crawl_neighborhood_probe import FROM,TO,IMAGE_TS,cdx_url,classify,parse

class SA2521CNCrawlNeighborhoodTests(unittest.TestCase):
    def test_window(self):
        self.assertEqual(FROM,"20020517230000")
        self.assertEqual(TO,"20020518010000")
        self.assertEqual(IMAGE_TS,"20020517235842")
    def test_cdx(self):
        q=urllib.parse.parse_qs(urllib.parse.urlparse(cdx_url("http://download.21cn.com/")).query)
        self.assertEqual(q["from"],[FROM]); self.assertEqual(q["to"],[TO])
    def test_classify(self):
        self.assertEqual(classify("http://x/list.php?id=1"),"list")
        self.assertEqual(classify("http://x/downit.php?id=1"),"downit")
        self.assertEqual(classify("http://x/file/game/a.jpg"),"game-file")
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["20020517235842","http://x/a"]]).encode()
        self.assertEqual(parse(b)[0]["original"],"http://x/a")
if __name__=="__main__": unittest.main()
