"""PET21 durable original-archive image SHA receipt; PET16 identity boundaries."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import operator_image_trace

REC = ROOT / "research/recovered"


class Pet21ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(
            (REC / "STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json")
            .read_text(encoding="utf-8"))
        cls.c = json.loads(
            (REC / "STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
            .read_text(encoding="utf-8"))

    def test_run_provenance_and_source_bounds(self):
        r = self.a
        self.assertEqual(r["probe_exact_candidate_head_sha"],
                         "d3db47d6bec6a1f114161252e2b63f75ea6a85c4")
        self.assertEqual(r["probe_workflow_run_id"], 43693853890)
        self.assertEqual(r["probe_job_id"], 132749981173)
        self.assertEqual(r["original_frozen_catalogue_git_blob"],
                         "fdb7d9aade2df62d1a1e06b2d2f9e383693ed980")
        self.assertEqual(len(r["records"]), 23)
        self.assertTrue(r["source_boundaries"]["source_web_image_does_not_prove_official_client_sprite_or_pet_ID"])
        self.assertTrue(r["source_boundaries"]["network_timeout_or_unreadable_not_archival_absence"])
        self.assertFalse(r["source_boundaries"]["source_bounded_closed"])
        self.assertFalse(r["source_boundaries"]["allowed_to_switch_content_module"])
        self.assertTrue(r["source_boundaries"]["no_automatic_publication_or_new_game_asset_use_rights"])

    def test_exact_23_operator_positions_source_and_page_SHA(self):
        ids = set()
        for item in self.a["records"]:
            group = item["source_namespace"]
            origin = [
                row for row in self.c["datasets"][group]
                if row["web_ordinal"] == item["web_ordinal"]
            ]
            self.assertEqual(len(origin), 1)
            src = origin[0]
            self.assertEqual(src["id"], item["original_record_id"])
            self.assertEqual(src["image_reference_url"], item["operator_image_reference_url"])
            self.assertEqual(src["name_as_written"], item["name_as_written_or_null"])
            self.assertEqual(src["source_refs"][0]["sha256"],
                             item["operator_original_page_bytes_sha256"])
            self.assertEqual(src["source_refs"][0]["capture"],
                             item["operator_page_archive_capture"])
            self.assertIsNone(src["actual_client_species_id"])
            self.assertFalse(item["source_image_pixel_bytes_retained_in_private_library_now"])
            self.assertFalse(item["original_client_species_id_proved"])
            self.assertFalse(item["contemporaneous_image_with_operator_page_archive_proven"])
            self.assertFalse(item["rights_for_public_redistribution_or_new_game_proven"])
            ids.add(item["original_record_id"])
        self.assertEqual(len(ids), 23)
        self.assertEqual(sum(x["source_namespace"] == "jp_official_web"
                             for x in self.a["records"]), 11)
        self.assertEqual(sum(x["source_namespace"] == "cn_official_web"
                             for x in self.a["records"]), 12)

    def test_exact_nine_original_archived_bytes_one_prior_eight_new_JP(self):
        found = [x for x in self.a["records"]
                 if x["probe_status"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"]
        self.assertEqual(len(found), 9)
        self.assertTrue(all(x["source_namespace"] == "jp_official_web" for x in found))
        self.assertEqual(len([x for x in found if x["source_catalogue_prior_image_sha256_or_null"]]), 1)
        self.assertEqual(self.a["observed"]["jp_original_archived_image_bytes_newly_hashed"], 8)
        self.assertEqual(self.a["observed"]["new_artwork_persistently_stored"], 0)
        self.assertEqual([x["web_ordinal"] for x in found],
                         [1, 2, 3, 44, 45, 46, 89, 91, 123])
        for item in found:
            self.assertRegex(item["returned_original_media_image_sha256_or_null"],
                             r"^[a-f0-9]{64}$")
            self.assertRegex(item["observed_image_archive_capture_or_null"],
                             r"^\d{14}$")
            self.assertEqual(item["observed_image_type_or_null"], "GIF")
            self.assertEqual(item["observed_image_dimensions_or_null"], [60, 65])
            self.assertGreater(item["observed_image_bytes_or_null"], 3000)
            self.assertTrue(item["archive_original_binary_url"].startswith(
                            "https://web.archive.org/web/"))
        jp1 = found[0]
        self.assertEqual(jp1["returned_original_media_image_sha256_or_null"],
                         jp1["source_catalogue_prior_image_sha256_or_null"])
        self.assertEqual(jp1["observed_image_archive_capture_or_null"], "20060604065927")
        # The third page HTML was captured 2004, but the recovered image may
        # have a 2003 timestamp. This is NOT same-instant web page evidence.
        jp91 = [x for x in found if x["web_ordinal"] == 91][0]
        self.assertEqual(jp91["operator_page_archive_capture"], "20040220221717")
        self.assertEqual(jp91["observed_image_archive_capture_or_null"], "20031214163657")

    def test_CN_unreadable_not_absent(self):
        blocked = [x for x in self.a["records"]
                   if x["source_namespace"] == "cn_official_web"]
        self.assertTrue(all(x["returned_original_media_image_sha256_or_null"] is None
                            for x in blocked))
        self.assertTrue(all(x["probe_status"] in (
            "ARCHIVED_URL_NOT_READABLE_NOW", "NOT_RETRIEVED_NETWORK_OR_INDEX_BLOCKED")
                            for x in blocked))
        self.assertEqual(self.a["observed"]["cn_unreadable_now"], 12)
        self.assertEqual(self.a["observed"]["original_2D_game_client_sprite_records_added"], 0)

    def test_lookup_in_single_catalogue_no_silent_identity_merge(self):
        found = operator_image_trace(self.c, self.a, "jp", 2)
        self.assertEqual(found["pet21_probe_status"], "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED")
        self.assertEqual(found["original_catalogue_record_or_null"]["name_as_written"], "ウリウリ")
        self.assertEqual(found["pet21_source_receipt_or_null"]["observed_image_archive_capture_or_null"],
                         "20060604065940")
        self.assertFalse(found["image_custody_verified_private"])
        self.assertFalse(found["original_official_client_species_ID_proven"])
        unprobed = operator_image_trace(self.c, self.a, "jp", 25)
        self.assertEqual(unprobed["pet21_probe_status"], "NOT_IN_PET21_SAMPLE")
        self.assertIsNone(unprobed["pet21_source_receipt_or_null"])
        no_position = operator_image_trace(self.c, self.a, "cn", 9999)
        self.assertEqual(no_position["pet21_probe_status"], "NO_SOURCE_POSITION")
        self.assertIsNone(no_position["original_catalogue_record_or_null"])
        unknown = operator_image_trace(self.c, self.a, "cn", 1)
        self.assertIsNone(unknown["original_catalogue_record_or_null"]["name_as_written"])
        self.assertEqual(unknown["pet21_probe_status"], "ARCHIVED_URL_NOT_READABLE_NOW")

    def test_invalid_websource_and_ordinal(self):
        for bad in ("tw10", "", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                operator_image_trace(self.c, self.a, bad, 1)
        for bad in (0, -2, True, "2", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                operator_image_trace(self.c, self.a, "jp", bad)


if __name__ == "__main__":
    unittest.main()
