import json
import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_may2002_probe import (
    FROM, TO, IMAGE_URL, cdx_url, jpeg_size, page_id, parse_cdx
)


class SA2521CNMay2002ProbeTests(unittest.TestCase):
    def test_window_and_image(self):
        self.assertEqual(FROM,"20020514")
        self.assertEqual(TO,"20020520")
        self.assertTrue(IMAGE_URL.endswith("/sa25up.jpg"))

    def test_cdx_window(self):
        p=urllib.parse.urlparse(cdx_url("http://202.104.32.168/list.php?id="))
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["from"],[FROM])
        self.assertEqual(q["to"],[TO])

    def test_parse_numeric_id(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020517000000","http://202.104.32.168/list.php?id=20549","200","text/html","A","1"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(page_id(rows[0]["original"]),"20549")

    def test_jpeg_size(self):
        body=b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x64\x00\xc8"+b"\x03"+b"\x00"*12+b"\xff\xd9"
        self.assertEqual(jpeg_size(body)[:2],(200,100))


if __name__=="__main__":
    unittest.main()
