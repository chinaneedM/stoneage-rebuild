import unittest

from tools.stoneage_japan174a_gamania_mirror_probe import (
    GM_HTTP,
    GM_HTTPS,
    GM_PREFIX,
    parse_json_rows,
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
        self.assertEqual(GM_PREFIX, "file2.gamania.co.jp/sa/*")

    def test_parse_wayback_json_rows(self):
        body = (
            b'[['
            b'"timestamp","original","statuscode"],'
            b'["20031212000000","http://x/a.exe","200"]'
            b']'
        )
        rows = parse_json_rows(body)
        self.assertEqual(rows[0]["statuscode"], "200")
        self.assertEqual(rows[0]["original"], "http://x/a.exe")

    def test_parse_empty_rows(self):
        self.assertEqual(parse_json_rows(b"[]"), [])


if __name__ == "__main__":
    unittest.main()
