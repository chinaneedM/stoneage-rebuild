import json
import unittest
import urllib.parse

from tools.stoneage_sa25_discmaster_signature_probe import (
    SIGNATURES, exact_leaf, rows, search_url
)


class SA25DiscMasterSignatureProbeTests(unittest.TestCase):
    def test_verified_distinctive_signatures_registered(self):
        got={(name,kind) for _,name,kind in SIGNATURES}
        self.assertIn(("adrn_15.bin","distinctive"),got)
        self.assertIn(("real_15.bin","distinctive"),got)
        self.assertIn(("spradrn_5.bin","distinctive"),got)

    def test_query_uses_filename_field(self):
        p=urllib.parse.urlparse(search_url("adrn_15.bin"))
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["qfields"],["name"])
        self.assertEqual(q["mode"],["deep"])
        self.assertEqual(q["tsMin"],["2000"])
        self.assertEqual(q["tsMax"],["2006"])

    def test_exact_leaf(self):
        self.assertTrue(exact_leaf({"fileid":"x/data/ADRN_15.BIN"},"adrn_15.bin"))
        self.assertFalse(exact_leaf({"fileid":"x/data/old_adrn_15.bin"},"adrn_15.bin"))

    def test_rows_dedup(self):
        obj={"a":[
            {"itemid":"1","fileid":"x/a","filename":"a"},
            {"itemid":"1","fileid":"x/a","filename":"a"},
            {"itemid":"2","fileid":"x/a","filename":"a"},
        ]}
        self.assertEqual(len(rows(obj)),2)


if __name__=="__main__":
    unittest.main()
