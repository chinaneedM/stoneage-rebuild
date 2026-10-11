"""Synthetic Arquivo.pt API regression tests: index metadata != historical source bytes."""
import json
import unittest
from tools.stoneage_tw80_arquivo_pt_index_probe import (
    ORIGINAL_URL, MAX_ITEMS, build_query, parse_index, summarize_response,
)

class ArquivoPtIndexTests(unittest.TestCase):
    def sample(self):
        return {
            "originalURL": ORIGINAL_URL,
            "tstamp": "20050608010101",
            "digest": "ARCHIVED_DIGEST_TOKEN",
            "mimeType": "text/html",
            "linkToArchive": "https://arquivo.pt/wayback/20050608010101/" + ORIGINAL_URL,
        }

    def test_exact_url_is_query_target(self):
        self.assertIn("versionHistory=", build_query())
        self.assertIn("page_3.html", build_query())

    def test_strict_three_year_window(self):
        self.assertIn("from=2005", build_query())
        self.assertIn("to=2007", build_query())
        self.assertIn("maxItems=12", build_query())

    def test_valid_index_hit_is_not_original_publisher_page(self):
        x = summarize_response(json.dumps({"response_items": [self.sample()]}))
        self.assertEqual(x["probe_status"], "INDEX_METADATA_FOUND_PAGE_UNVERIFIED")
        self.assertFalse(x["original_page_body_obtained"])
        self.assertFalse(x["original_2005_taiwan_installer_obtained"])

    def test_index_digest_is_not_installer_sha(self):
        x = summarize_response(json.dumps({"response_items": [self.sample()]}))
        self.assertEqual(x["index_records"][0]["archive_index_digest"], "ARCHIVED_DIGEST_TOKEN")
        self.assertFalse(x["publisher_binary_sha256_verified"])

    def test_empty_not_global_absence(self):
        self.assertEqual(
            summarize_response(json.dumps({"response_items": []}))["probe_status"],
            "EMPTY_INDEX_NOT_PROOF_OF_ABSENCE",
        )

    def test_timeout_not_404(self):
        self.assertEqual(summarize_response(error="TimeoutError")["probe_status"], "NETWORK_INDETERMINATE")

    def test_wrong_provider_json(self):
        self.assertEqual(summarize_response("{}")["probe_status"], "INVALID_OR_UNEXPECTED_INDEX_RESPONSE")

    def test_malformed_json(self):
        self.assertEqual(summarize_response("error")["probe_status"], "INVALID_OR_UNEXPECTED_INDEX_RESPONSE")

    def test_unrelated_original_url(self):
        x = self.sample()
        x["originalURL"] = "http://cdl.wayi.com.cn/sa8_8016.rar"
        with self.assertRaises(ValueError):
            parse_index({"response_items": [x]})

    def test_future_archive_capture_rejected(self):
        x = self.sample()
        x["tstamp"] = "20180608010101"
        with self.assertRaises(ValueError):
            parse_index({"response_items": [x]})

    def test_2004_capture_rejected(self):
        x = self.sample()
        x["tstamp"] = "20040608010101"
        with self.assertRaises(ValueError):
            parse_index({"response_items": [x]})

    def test_untrusted_redirect_to_binary_rejected(self):
        x = self.sample()
        x["linkToArchive"] = "https://evil.example.com/Stoneage80.exe"
        with self.assertRaises(ValueError):
            parse_index({"response_items": [x]})

    def test_overlarge_index_rejected(self):
        with self.assertRaises(ValueError):
            parse_index({"response_items": [self.sample() for _ in range(MAX_ITEMS + 1)]})

    def test_malformed_timestamp(self):
        x = self.sample()
        x["tstamp"] = "20050230010101"
        with self.assertRaises(ValueError):
            parse_index({"response_items": [x]})

    def test_header_metadata_cannot_be_client_runtime(self):
        x = summarize_response(json.dumps({"response_items": [self.sample()]}))
        self.assertFalse(x["native_pet_equipment_runtime_verified"])

    def test_missing_digest_allowed_without_fabrication(self):
        x = self.sample()
        x.pop("digest")
        got = parse_index({"response_items": [x]})
        self.assertIsNone(got[0]["archive_index_digest"])

    def test_nonlist_response_rejected(self):
        with self.assertRaises(ValueError):
            parse_index({"response_items": {}})

if __name__ == "__main__":
    unittest.main()
