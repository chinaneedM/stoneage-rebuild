import json
import unittest
import urllib.parse
import zipfile
import io

from tools.stoneage_sa25_21cn_mirror_recovery_probe import (
    TARGETS, candidate_row, cdx_url, inventory_zip
)


class SA2521CNMirrorRecoveryTests(unittest.TestCase):
    def test_evidence_derived_targets(self):
        urls={u for _,u in TARGETS}
        self.assertIn("http://images.21cn.com/download/file/game/maoxian/sa25up.zip",urls)
        self.assertIn("http://dg.download.21cn.com/file1_21cn/game/maoxian/sa25up.zip",urls)
        self.assertIn("http://dg.download.21cn.com/file1xzm/game/maoxian/sa25up.zip",urls)

    def test_cdx_exact(self):
        u=cdx_url(TARGETS[0][1])
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
        self.assertEqual(q["matchType"],["exact"])
        self.assertEqual(q["from"],["2002"])
        self.assertEqual(q["to"],["2006"])

    def test_candidate_size(self):
        self.assertTrue(candidate_row({"statuscode":"200","length":"8473000"}))
        self.assertFalse(candidate_row({"statuscode":"404","length":"8473000"}))
        self.assertFalse(candidate_row({"statuscode":"200","length":"12000"}))

    def test_inventory_zip(self):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,"w") as z:
            z.writestr("x.txt",b"abc")
        rows=inventory_zip(buf.getvalue())
        self.assertEqual(rows[0]["name"],"x.txt")
        self.assertEqual(rows[0]["size"],3)


if __name__=="__main__":
    unittest.main()
