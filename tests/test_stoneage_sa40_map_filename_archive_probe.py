import json
import unittest
import urllib.parse

from tools.stoneage_sa40_map_filename_archive_probe import (
    BASENAME,
    PUBLISHED_DATE,
    SCOPES,
    WINDOWS,
    cdx_url,
    parse_cdx_json,
)


class SA40MapFilenameArchiveProbeTests(unittest.TestCase):
    def test_source_derived_basename_and_date_are_pinned(self):
        self.assertEqual(BASENAME,"shiqi4updatex_02_11_08.zip")
        self.assertEqual(PUBLISHED_DATE,"20021108")

    def test_scopes_are_bounded_to_historical_sina_download_domains(self):
        self.assertEqual(
            dict(SCOPES),
            {
                "games1-sina":"games1.sina.com.cn",
                "games-sina-domain":"games.sina.com.cn",
            },
        )

    def test_windows_partition_the_archive_period(self):
        self.assertEqual(WINDOWS[0],("2002-post","20021108","20021231"))
        self.assertEqual(WINDOWS[-1],("2005","20050101","20051231"))

    def test_cdx_query_uses_domain_match_and_exact_basename_filter(self):
        parsed=urllib.parse.urlparse(cdx_url("games1.sina.com.cn","20021108","20021231"))
        query=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["matchType"],["domain"])
        self.assertEqual(query["url"],["games1.sina.com.cn"])
        self.assertEqual(query["from"],["20021108"])
        self.assertEqual(query["to"],["20021231"])
        self.assertTrue(any("shiqi4updatex_02_11_08[.]zip" in value for value in query["filter"]))

    def test_parse_cdx_json(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20021109010203","http://games1.sina.com.cn/x/"+BASENAME,"200","application/zip","ABC","123"],
        ]).encode()
        rows=parse_cdx_json(body)
        self.assertEqual(rows[0]["timestamp"],"20021109010203")
        self.assertIn(BASENAME,rows[0]["original"])


if __name__=="__main__":
    unittest.main()
