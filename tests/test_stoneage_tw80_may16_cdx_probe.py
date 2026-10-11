"""Synthetic negative and positive controls for archive index metadata."""
import json
import unittest
from tools.stoneage_tw80_may16_cdx_probe import FIELDS,TARGET,build_url,classify,report

class CdxTests(unittest.TestCase):
    def row(self):
        return ["20050516010101",TARGET,"200","text/html","CDX_SHA_TOKEN"]
    def fake(self,*entries):
        return [FIELDS,*entries]
    def test_target_query(self):
        self.assertIn("page_3.html",build_url())
    def test_one_index_hit_not_page_content(self):
        d=report(raw=json.dumps(self.fake(self.row())))
        self.assertEqual(d["status"],"INDEX_HITS_UNAUTHENTICATED_CONTENT")
        self.assertFalse(d["original_client_binary_retrieved"])
        self.assertFalse(d["original_page_content_authenticated"])
    def test_empty_does_not_prove_absence(self):
        self.assertEqual(report(raw=json.dumps(self.fake()))["status"],"EMPTY_INDEX_NOT_PROOF_OF_ABSENCE")
    def test_network_not_absence(self):
        self.assertEqual(report(error="HTTPError")["status"],"NETWORK_INDETERMINATE")
    def test_invalid_json(self):
        self.assertEqual(report(raw="not json")["status"],"CDX_RESPONSE_INDETERMINATE")
    def test_bad_header(self):
        self.assertEqual(report(raw=json.dumps([["timestamp","statuscode"]]))["status"],"CDX_RESPONSE_INDETERMINATE")
    def test_future_year(self):
        r=self.row();r[0]="20240516010101"
        with self.assertRaises(ValueError):classify(self.fake(r))
    def test_other_operator_domain(self):
        r=self.row();r[1]="http://www.wayi.com.cn/stoneage/"
        with self.assertRaises(ValueError):classify(self.fake(r))
    def test_404_not_valid_200(self):
        r=self.row();r[2]="404"
        with self.assertRaises(ValueError):classify(self.fake(r))
    def test_invalid_timestamp(self):
        r=self.row();r[0]="2005-May"
        with self.assertRaises(ValueError):classify(self.fake(r))
    def test_too_many_rows(self):
        with self.assertRaises(ValueError):classify(self.fake(*[self.row() for _ in range(21)]))

if __name__=="__main__":
    unittest.main()
