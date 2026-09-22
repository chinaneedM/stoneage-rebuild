import json
import unittest

from tools.stoneage_exact_mirror_arquivopt_cdx_probe import TARGETS, parse_rows, query_url


class ExactMirrorArquivoCdxProbeTests(unittest.TestCase):
    def test_parse_array_rows(self):
        data = json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20010101000000","http://x/sa.exe","200","application/octet-stream","ABC","123"],
        ]).encode()
        rows = parse_rows(data)
        self.assertEqual(rows[0]["original"], "http://x/sa.exe")
        self.assertEqual(rows[0]["length"], "123")

    def test_parse_cdxj(self):
        data = b'com,example)/ 20010101000000 {"url":"http://example.com/","timestamp":"20010101000000","status":"200"}\n'
        rows = parse_rows(data)
        self.assertEqual(rows[0]["url"], "http://example.com/")

    def test_query_url_contains_exact_original(self):
        url = query_url("http://stoneage.hananet.net/down/sa.exe")
        self.assertIn("stoneage.hananet.net", url)
        self.assertIn("from=2000", url)
        self.assertIn("to=2005", url)

    def test_gametime_payload_targets_registered(self):
        urls={url for _,url in TARGETS}
        self.assertIn("http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip", urls)
        self.assertIn("http://www.gametime.co.kr/images/Online/pds/2001/02/stone_demo.exe", urls)

    def test_japan_174a_payload_target_registered(self):
        urls={url for _,url in TARGETS}
        self.assertIn(
            "http://hangame.gamania.co.jp/stoneage/sa174hg.exe",
            urls,
        )


if __name__ == "__main__":
    unittest.main()
