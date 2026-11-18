import json
import hashlib
from unittest.mock import patch
from pathlib import Path
import unittest
from tools import stoneage_pet34_jss1999_beta_print_custody as p


class Pet34MagazineSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(Path("research/recovered/STONEAGE-PET34-JSS1999-SEPTEMBER-BETA-PRINT-SOURCE-R1.json").read_text(encoding="utf-8"))

    def test_source_fingerprint_and_not_an_original_official_disc(self):
        r=self.report
        self.assertEqual(r["source"]["sha256"],p.SHA256)
        self.assertEqual(r["source"]["bytes"],p.BYTES)
        self.assertEqual(r["source"]["page_count"],p.PAGES)
        self.assertFalse(r["source"]["native_japanese_text_reliable"])
        self.assertFalse(r["source"]["pdf_original_saved_in_public_repo"])
        self.assertFalse(r["source"]["manual_physical_copy_collation_proven"])
        self.assertTrue(r["preexisting_source_context"]["not_new_betatest_proof"])

    def test_unverified_bonus_not_assumed_to_be_pet_or_1999_release(self):
        r=self.report
        self.assertFalse(r["new_direct_audit"]["beta_bonus_was_pet_proven"])
        self.assertFalse(r["new_direct_audit"]["any_specific_1999_species_obtainable_proven"])
        self.assertFalse(r["new_direct_audit"]["original_beta_game_disc_or_executable_recovered"])
        self.assertEqual(r["new_direct_audit"]["new_qualified_named_pets"],[])
        self.assertIsNone(r["new_direct_audit"]["historical_1999_pet_population_count"])
        self.assertTrue(r["guardrails"]["unreadable_text_layer_does_not_prove_absence_of_pets"])
        self.assertEqual(r["guardrails"]["current_frontier_year"],1999)
        self.assertEqual(r["guardrails"]["active_module"],"PET")
        self.assertEqual(r["guardrails"]["year_review_status"],"NOT_YEAR_AUDITED")

    def test_wrong_bytes_redirect_and_page_count_rejected(self):
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong",p.URL,p.PAGES)
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong","https://fake.example/a.pdf",p.PAGES)
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong",p.URL,42)


    def test_bounded_fetch_retries_truncated_or_html_response_but_not_source_drift(self):
        # Synthetic bytes: tests the transport guard without downloading a copyrighted scan.
        valid = b"%PDF-1.5\\n" + b"example-original-test-bytes"
        class FakeResponse:
            def __init__(self, data, url=p.URL):
                self.data = data
                self.url = url
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                return False
            def read(self, n):
                return self.data[:n]
        attempts=[]
        pauses=[]
        def fetcher(request, timeout):
            attempts.append((request.full_url, timeout))
            if len(attempts) == 1:
                return FakeResponse(b"<html>temporary upstream error</html>")
            if len(attempts) == 2:
                return FakeResponse(valid[:8])
            return FakeResponse(valid)
        with patch.object(p, "BYTES", len(valid)), patch.object(p, "SHA256", hashlib.sha256(valid).hexdigest()):
            received, url = p.fetch_exact_magazine(max_attempts=3, fetcher=fetcher, pause=pauses.append)
        self.assertEqual(received, valid)
        self.assertEqual(url, p.URL)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(pauses, [1, 2])
        self.assertTrue(all(url == p.URL and timeout == 120 for url, timeout in attempts))

    def test_bounded_fetch_fails_closed_when_every_response_is_wrong_or_redirected(self):
        valid = b"%PDF-1.5\\n" + b"example-original-test-bytes"
        class FakeResponse:
            def __init__(self, data, url):
                self.data = data
                self.url = url
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, n):
                return self.data[:n]
        for raw, destination in [(b"<html>bad</html>", p.URL),
                                 (valid[:-1], p.URL),
                                 (valid, "https://invalid.example/file.pdf")]:
            calls=[]
            def bad_fetch(req, timeout):
                calls.append(req.full_url)
                return FakeResponse(raw, destination)
            with patch.object(p, "BYTES", len(valid)), patch.object(p, "SHA256", hashlib.sha256(valid).hexdigest()):
                with self.assertRaisesRegex(ValueError, "after retries"):
                    p.fetch_exact_magazine(max_attempts=2, fetcher=bad_fetch, pause=lambda n: None)
            self.assertEqual(len(calls), 2)

    def test_latest_1999_cursor_receipt(self):
        q=json.loads(Path("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(q["current_frontier"]["year"],1999)
        # Historical PET34 remains verifiable even when the next year starts.
        # Latest cursor advances with newer PET batches; PET34's verified
        # historical receipt must remain immutable and independently findable.
        records = [x for x in q["root_source_census_receipts"]
                   if x["id"] == "PET34-JSS1999-SEPTEMBER-BETA-PRINT-CUSTODY-20261115"]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["new_official_named_released_pets"], 0)
        self.assertIsNone(records[0]["historical_pet_population_count"])
        self.assertIn(q["current_frontier"]["latest_partial_root_review"],
                      [x["id"] for x in q["root_source_census_receipts"]])


if __name__=="__main__":
    unittest.main()
