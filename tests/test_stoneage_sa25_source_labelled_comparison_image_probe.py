import json
import unittest

from tools.stoneage_sa25_source_labelled_comparison_image_probe import cdx_url, parse_cdx


class SourceLabelledComparisonImageProbeTests(unittest.TestCase):
    def test_parse_cdx(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20201222000000","http://example/x.jpg","200","image/jpeg","ABC","1234"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["timestamp"],"20201222000000")
        self.assertEqual(rows[0]["digest"],"ABC")

    def test_cdx_url_keeps_exact_target(self):
        u=cdx_url("https://example.com/a.jpg")
        self.assertIn("url=https%3A%2F%2Fexample.com%2Fa.jpg",u)
        self.assertIn("statuscode%3A200",u)


if __name__=="__main__":
    unittest.main()
