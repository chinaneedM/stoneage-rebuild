import json
import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_hostname_probe import (
    TARGETS, PREFIXES, cdx_url, parse_cdx
)


class SA2521CNHostnameProbeTests(unittest.TestCase):
    def test_download_hostname_target(self):
        urls={u for _,u in TARGETS}
        self.assertIn("http://download.21cn.com/file/game/maoxian/sa25up.zip",urls)

    def test_prefix_registered(self):
        self.assertIn(("download-maoxian","http://download.21cn.com/file/game/maoxian/"),PREFIXES)

    def test_cdx_exact(self):
        p=urllib.parse.urlparse(cdx_url(TARGETS[0][1],"exact",None,200))
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["matchType"],["exact"])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2005"])

    def test_parse(self):
        b=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20020101000000",TARGETS[0][1],"200","application/zip","A","10",""],
        ]).encode()
        self.assertEqual(parse_cdx(b)[0]["statuscode"],"200")


if __name__=="__main__":
    unittest.main()
