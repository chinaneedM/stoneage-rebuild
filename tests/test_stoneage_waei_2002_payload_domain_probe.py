import json,unittest,urllib.parse
from tools.stoneage_waei_2002_payload_domain_probe import WINDOWS,EXTENSIONS,cdx_url,parse,score
class T(unittest.TestCase):
    def test_partition(self):
        self.assertEqual(len(WINDOWS),3); self.assertIn("exe",EXTENSIONS)
    def test_domain_query(self):
        q=urllib.parse.parse_qs(urllib.parse.urlparse(cdx_url("20020201","20020228","exe")).query)
        self.assertEqual(q["matchType"],["domain"]); self.assertEqual(q["url"],["waei.com.cn"])
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["1","http://x/a.exe"]]).encode()
        self.assertEqual(parse(b)[0]["original"],"http://x/a.exe")
    def test_score(self):
        a={"original":"http://down.waei.com.cn/stoneage/sa25setup.exe","mimetype":"application/octet-stream","length":"9000000"}
        b={"original":"http://product.waei.com.cn/qqskin/160.zip","mimetype":"application/zip","length":"1000"}
        self.assertGreater(score(a),score(b))
if __name__=="__main__": unittest.main()
