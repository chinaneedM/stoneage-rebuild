import json
import unittest
import urllib.parse

from tools.stoneage_sa40_map_carrier_probe import (
    BASENAME,
    STEM,
    discmaster_url,
    discmaster_rows,
    exact_or_stem_hits,
    ia_url,
    ia_docs,
)

class SA40MapCarrierProbeTests(unittest.TestCase):
    def test_target_is_source_derived(self):
        self.assertEqual(BASENAME,"shiqi4updatex_02_11_08.zip")
        self.assertEqual(STEM,"shiqi4updatex_02_11_08")

    def test_discmaster_query_is_filename_scoped(self):
        parsed=urllib.parse.urlparse(discmaster_url(f'"{BASENAME}"'))
        query=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["qfields"],["name"])
        self.assertEqual(query["mode"],["deep"])

    def test_discmaster_exact_and_stem_classification(self):
        data={
            "results":[
                {"itemid":"1","fileid":"x/shiqi4updatex_02_11_08.zip","itemName":"disc"},
                {"itemid":"2","fileid":"x/shiqi4updatex_02_11_08_copy.zip","itemName":"disc2"},
            ]
        }
        rows=discmaster_rows(data)
        exact,stem=exact_or_stem_hits(rows)
        self.assertEqual(len(exact),1)
        self.assertEqual(len(stem),1)

    def test_ia_query_and_docs(self):
        parsed=urllib.parse.urlparse(ia_url(f'"{BASENAME}"'))
        query=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["output"],["json"])
        docs=ia_docs({"response":{"docs":[{"identifier":"x"}]}})
        self.assertEqual(docs[0]["identifier"],"x")

if __name__=="__main__":
    unittest.main()
