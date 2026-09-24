import json
import unittest
import urllib.parse

from tools.stoneage_waei_sa25_download_probe import (
    DATE_FROM,
    DATE_TO,
    PREFIX,
    extract_evidence,
    parse_cdx,
    select_replay_rows,
    url_score,
)

class WaeiSA25DownloadProbeTests(unittest.TestCase):
    def test_grounded_prefix_and_window(self):
        self.assertEqual(PREFIX,"http://www.waei.com.cn/zhuanqu/stoneage/")
        self.assertEqual(DATE_FROM,"20020101")
        self.assertEqual(DATE_TO,"20020315")

    def test_parse_cdx(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020201000000",PREFIX+"download.asp","200","text/html","ABC","123"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(rows[0]["timestamp"],"20020201000000")

    def test_url_score_prioritizes_download(self):
        self.assertGreater(url_score(PREFIX+"download.asp"),url_score(PREFIX+"foo.asp"))

    def test_extracts_25_terms_and_payload_href(self):
        body=(
            '<html><body>石器时代2.5 完整升级版 580兆 '
            '<a href="../down/sa25setup.exe">下载</a></body></html>'
        ).encode("gb18030")
        terms,hrefs=extract_evidence(body)
        self.assertIn("石器时代2.5",terms)
        self.assertIn("../down/sa25setup.exe",hrefs)

    def test_select_replays_is_bounded_and_prefers_download(self):
        rows=(
            {"timestamp":"1","original":PREFIX+"foo.asp","mimetype":"text/html"},
            {"timestamp":"2","original":PREFIX+"download.asp","mimetype":"text/html"},
        )
        selected=select_replay_rows(rows)
        self.assertTrue(selected[0]["original"].endswith("download.asp"))

if __name__=="__main__":
    unittest.main()
