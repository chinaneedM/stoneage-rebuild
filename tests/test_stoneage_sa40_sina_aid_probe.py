import json
import unittest
import urllib.parse

from tools.stoneage_sa40_sina_aid_probe import (
    AID,
    BASENAME,
    CGI_PREFIX,
    SOURCE_URL,
    cgi_cdx_url,
    href_candidates,
    relevant_cgi,
)

class SA40SinaAidProbeTests(unittest.TestCase):
    def test_source_identifiers_are_pinned(self):
        self.assertEqual(AID,"61620")
        self.assertEqual(BASENAME,"shiqi4updatex_02_11_08.zip")
        self.assertTrue(SOURCE_URL.endswith("11084599.shtml"))
        self.assertTrue(CGI_PREFIX.endswith("/download.pl"))

    def test_cgi_probe_is_prefix_scoped(self):
        parsed=urllib.parse.urlparse(cgi_cdx_url("20021108","20021231"))
        query=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["matchType"],["prefix"])
        self.assertEqual(query["url"],[CGI_PREFIX])

    def test_relevant_cgi_accepts_aid_or_filename(self):
        rows=(
            {"original":"http://x/download.pl?foo=1&aid=61620"},
            {"original":"http://x/download.pl?filename=shiqi4updatex_02_11_08.zip"},
            {"original":"http://x/download.pl?aid=1"},
        )
        self.assertEqual(len(relevant_cgi(rows)),2)

    def test_href_candidates(self):
        body=(
            '<a href="http://x/download.pl?aid=61620">a</a>'
            '<a href="x?filename=shiqi4updatex_02_11_08.zip">b</a>'
            '<a href="x?aid=1">c</a>'
        ).encode("gb18030")
        self.assertEqual(len(href_candidates(body)),2)

if __name__=="__main__":
    unittest.main()
