import unittest

from tools.stoneage_japan174a_gamania_mirror_probe import (
    GM_HTTP,
    GM_HTTPS,
    decode_discuz_aid,
    parse_cdx,
)


class T(unittest.TestCase):
    def test_exact_gamania_targets(self):
        self.assertEqual(
            GM_HTTP,
            "http://file2.gamania.co.jp/sa/sa174gm.exe",
        )
        self.assertEqual(
            GM_HTTPS,
            "https://file2.gamania.co.jp/sa/sa174gm.exe",
        )

    def test_discuz_aid_decode(self):
        href = (
            "forum.php?aid=Njc1fGE2NjQ3M2Q2fDE3OTAxMzU3Mzd8MHwxNjY3MQ%3D%3D"
            "&mod=attachment"
        )
        self.assertEqual(
            decode_discuz_aid(href),
            "675|a66473d6|1790135737|0|16671",
        )

    def test_parse_cdx(self):
        body = (
            b'[['
            b'"timestamp","original","statuscode"],'
            b'["20031212000000","http://x/a.exe","200"]'
            b']'
        )
        rows = parse_cdx(body)
        self.assertEqual(rows[0]["statuscode"], "200")
        self.assertEqual(rows[0]["original"], "http://x/a.exe")


if __name__ == "__main__":
    unittest.main()
