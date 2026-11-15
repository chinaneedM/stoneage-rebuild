"""PET22 exact 124 original operator image-reference source archive byte audit."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import operator_image_trace


class PET22SourceReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(
            (R / "STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
            .read_text(encoding="utf-8"))
        cls.old = json.loads(
            (R / "STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json")
            .read_text(encoding="utf-8"))
        cls.audit = json.loads(
            (R / "STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json")
            .read_text(encoding="utf-8"))

    def test_all_124_records_and_six_nonidentical_web_source_boundaries(self):
        a = self.audit
        self.assertEqual(a["original_exact_runner_commit"],
                         "cd6c6034c43ee52026ae79ccf24fd2ab8d92886f")
        self.assertEqual(a["workflow_run_id"], 43694793122)
        self.assertEqual([g["job_id"] for g in a["workflow_groups"]],
                         [132752851878, 132752852047, 132752851995])
        self.assertEqual(len(a["records"]), 124)
        self.assertEqual([r["web_ordinal"] for r in a["records"]], list(range(1, 125)))
        self.assertEqual(len(self.catalog["datasets"]["jp_official_web"]), 124)
        self.assertEqual(len(self.catalog["datasets"]["cn_official_web"]), 104)
        self.assertEqual([g["original_web_positions"] for g in a["workflow_groups"]],
                         [45, 45, 34])
        for r in a["records"]:
            item = self.catalog["datasets"]["jp_official_web"][r["web_ordinal"] - 1]
            self.assertEqual(r["original_operator_web_record_id"], item["id"])
            self.assertEqual(r["original_image_url"], item["image_reference_url"])
            self.assertEqual(r["name_as_written"], item["name_as_written"])
            self.assertEqual(r["parent_page_capture"], item["source_refs"][0]["capture"])
            self.assertEqual(r["parent_page_sha256"], item["source_refs"][0]["sha256"])
            self.assertFalse(r["authenticated_early_client_sprite_or_species_id"])
            self.assertFalse(r["commercial_image_durably_saved_in_this_pet22_batch"])
            self.assertFalse(r["commercial_image_release_or_game_license_verified"])

    def test_actual_run_raw_byte_counts_and_combined_independent_source_observations(self):
        a = self.audit
        counts = a["count_summary"]
        self.assertEqual(counts["original_jp_official_web_positions"], 124)
        self.assertEqual(counts["actual_archived_GIF_byte_responses_PET22"], 24)
        self.assertEqual(counts["previously_PET21_confirmed_image_positions"], 9)
        self.assertEqual(counts["independent_same_SHA_repeats_from_PET21"], 5)
        self.assertEqual(counts["PET21_previously_hashed_but_currently_not_retrievable"], 4)
        self.assertEqual(counts["newly_identified_distinct_image_positions_after_PET21"], 19)
        self.assertEqual(counts["cumulative_distinct_web_positions_with_verified_archived_image_SHA"], 28)
        self.assertEqual(counts["web_positions_with_no_verified_image_bytes_in_either_PET21_or_PET22"], 96)
        self.assertEqual(counts["within_PET22_not_retrieved_this_run"], 100)
        self.assertEqual(counts["conflicting_prior_archived_image_SHA_at_same_position"], 0)
        self.assertEqual(counts["original_media_GIFs_persistently_saved_privately_in_PET22"], 0)
        self.assertEqual(counts["original_media_GIFs_published_to_GitHub"], 0)
        group_summaries = [g["network_result_counts"]
                           for g in a["workflow_groups"]]
        self.assertEqual([g["ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"]
                          for g in group_summaries], [10, 5, 9])
        self.assertEqual(sum(g["ARCHIVED_URL_NOT_READABLE_NOW"]
                             for g in group_summaries), 92)
        self.assertEqual(sum(g["NOT_RETRIEVED_NETWORK_OR_INDEX_BLOCKED"]
                             for g in group_summaries), 8)

    def test_source_is_not_silently_rewritten_after_failed_replay(self):
        prior = {
            r["web_ordinal"]: r for r in self.old["records"]
            if r["source_namespace"] == "jp_official_web" and
               r["probe_status"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"
        }
        self.assertEqual(len(prior), 9)
        records = {r["web_ordinal"]: r for r in self.audit["records"]}
        confirmed = 0
        repeated = 0
        prior_only = 0
        after = 0
        for ordinal, r in records.items():
            now = r["PET22_probe"]["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"
            old = ordinal in prior
            if now:
                confirmed += 1
                self.assertEqual(r["PET22_probe"]["image_type_or_null"], "GIF")
                self.assertEqual(r["PET22_probe"]["image_dimensions_or_null"], [60, 65])
                self.assertRegex(r["PET22_probe"]["image_sha256_or_null"], "^[a-f0-9]{64}$")
                self.assertGreater(r["PET22_probe"]["gif_bytes_or_null"], 3000)
            if old and now:
                repeated += 1
                self.assertEqual(r["PET22_probe"]["image_sha256_or_null"],
                                 prior[ordinal]["returned_original_media_image_sha256_or_null"])
                self.assertEqual(r["comparison_with_PET21"],
                                 "SAME_SHA_INDEPENDENT_RUN")
            if old and not now:
                prior_only += 1
                self.assertEqual(r["best_archival_observation_sha256_or_null"],
                                 prior[ordinal]["returned_original_media_image_sha256_or_null"])
                self.assertEqual(r["comparison_with_PET21"],
                                 "PRIOR_PROVEN_SHA_PRESERVED_CURRENT_NETWORK_UNREADABLE")
            if now and not old:
                after += 1
            if r["best_archival_observation_sha256_or_null"]:
                self.assertRegex(r["best_archival_observation_sha256_or_null"],
                                 "^[a-f0-9]{64}$")
                self.assertTrue(r["source_url_for_private_future_sha_verify_or_null"]
                                .startswith("https://web.archive.org/web/"))
        self.assertEqual((confirmed, repeated, prior_only, after), (24, 5, 4, 19))
        self.assertEqual(len([x for x in records.values()
                              if x["best_archival_observation_sha256_or_null"]]), 28)
        self.assertEqual(records[44]["PET22_probe"]["kind"], "ARCHIVED_URL_NOT_READABLE_NOW")
        self.assertEqual(records[44]["best_archival_observation_sha256_or_null"],
                         prior[44]["returned_original_media_image_sha256_or_null"])

    def test_unified_lookup_exposes_new_archival_sha_without_game_identity(self):
        v4 = operator_image_trace(self.catalog, self.old, "jp", 4, self.audit)
        self.assertIsNotNone(v4["best_observed_operator_archived_image_sha256_or_null"])
        self.assertIsNotNone(v4["pet22_source_receipt_or_null"])
        self.assertIsNone(v4["pet21_source_receipt_or_null"])
        self.assertTrue(v4["operator_web_image_is_not_authenticated_game_sprite"])
        self.assertFalse(v4["original_official_client_species_ID_proven"])
        v44 = operator_image_trace(self.catalog, self.old, "jp", 44, self.audit)
        self.assertEqual(v44["pet22_source_receipt_or_null"]["PET22_probe"]["kind"],
                         "ARCHIVED_URL_NOT_READABLE_NOW")
        self.assertIsNotNone(v44["best_observed_operator_archived_image_sha256_or_null"])
        v100 = operator_image_trace(self.catalog, self.old, "jp", 100, self.audit)
        self.assertIsNone(v100["best_observed_operator_archived_image_sha256_or_null"])
        cn = operator_image_trace(self.catalog, self.old, "cn", 1, self.audit)
        self.assertIsNone(cn["pet22_source_receipt_or_null"])
        self.assertIsNone(cn["original_catalogue_record_or_null"]["name_as_written"])
        missing = operator_image_trace(self.catalog, self.old, "jp", 10000, self.audit)
        self.assertEqual(missing["pet21_probe_status"], "NO_SOURCE_POSITION")
        self.assertIsNone(missing["pet22_source_receipt_or_null"])

    def test_chronology_and_nonclosure(self):
        r = self.audit["records"][90]
        self.assertEqual(r["web_ordinal"], 91)
        self.assertEqual(r["parent_page_capture"], "20040220221717")
        self.assertEqual(r["best_archival_observation_capture_or_null"], "20031214163657")
        self.assertTrue(all(self.audit["evidence_guards"].values()))
        self.assertEqual(self.audit["historical_current_git_blob_unchanged"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
