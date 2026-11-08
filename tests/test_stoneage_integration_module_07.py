"""INTEGRATION07 public-only original DAT 14-floor evidence audit."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from tools.stoneage_integration07_missing_dat_audit import (
    derive, sources, validate, OUTPUT,
)

class Integration07BoundedMapSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.published = json.loads(OUTPUT.read_text("utf8"))
        cls.summary, cls.rows = derive()
        cls.by_floor = {x["floor_id"]: x for x in cls.rows}
        cls.data = sources()

    def test_01_source_files_pinned_to_exact_git_blobs_and_full_598_refs(self):
        self.assertEqual(self.summary["source_QUEST05_total_CREATE_references"], 598)
        self.assertEqual(self.summary["source_QUEST05_total_distinct_floors"], 236)
        self.assertEqual(self.summary["source_QUEST05_unmatched_DAT_floor_count"], 14)

    def test_02_all_88_source_creates_conserved_without_fake_NPC_identity(self):
        self.assertEqual(self.summary["source_QUEST05_unmatched_DAT_CREATE_count"], 88)
        self.assertEqual(sum(len(x["quest05_CREATE_ref_indices"]) for x in self.rows), 88)
        seen = [i for x in self.rows for i in x["quest05_CREATE_ref_indices"]]
        self.assertEqual(len(seen), len(set(seen)))
        q = self.data["q"]["source_CREATE_references"]
        for x in self.rows:
            self.assertEqual(x["quest05_source_CREATE_count"], len(x["quest05_CREATE_ref_indices"]))
            self.assertTrue(all(q[i]["source_floor_id"] == x["floor_id"] for i in x["quest05_CREATE_ref_indices"]))

    def test_03_one_independently_qualified_DAT_not_overwritten_by_prior_RAR_failure(self):
        z = self.by_floor[1000]
        self.assertEqual(z["source_DAT_status"], "VERIFIED_INDEPENDENT_DAT")
        self.assertEqual(z["quest05_source_CREATE_count"], 19)
        self.assertEqual(z["other_independently_qualified_DAT"]["sha256"],
            self.data["alternate"]["source_three_floors"]["1000"]["dat_sha256"])
        self.assertEqual(len(z["source_DAT_original_read_errors"]), 1)
        self.assertEqual(z["source_DAT_original_read_errors"][0]["emitted_before_error"], 131072)

    def test_04_twelve_still_failed_and_830_unrecorded(self):
        cats = self.summary["selected_DAT_status"]
        self.assertEqual((cats["VERIFIED_INDEPENDENT_DAT"]["floor_count"],
                          cats["INDEXED_DAT_READ_ERROR"]["floor_count"],
                          cats["NO_SELECTED_DAT_MEMBER"]["floor_count"]), (1, 12, 1))
        self.assertEqual((cats["VERIFIED_INDEPENDENT_DAT"]["source_CREATE_count"],
                          cats["INDEXED_DAT_READ_ERROR"]["source_CREATE_count"],
                          cats["NO_SELECTED_DAT_MEMBER"]["source_CREATE_count"]), (19, 67, 2))
        self.assertEqual(self.summary["source_no_selected_DAT_record_floors"], [830])
        self.assertFalse(self.published["evidence_limits"]["original_830_DAT_proven_nonexistent"])

    def test_05_casefold_catches_saved_lowercase_200_and_3000_member_names(self):
        self.assertEqual(self.summary["lowercase_DAT_filename_error_floors"], [200, 3000])
        self.assertEqual(self.by_floor[200]["source_DAT_original_read_errors"][0]["original_filename"], "200.dat")
        self.assertEqual(self.by_floor[3000]["source_DAT_original_read_errors"][0]["original_filename"], "3000.dat")
        self.assertEqual(self.summary["original_DAT_error_record_floor_count"], 13)

    def test_06_MAP_original_source_copy_conflict_only_floor400(self):
        self.assertEqual(self.summary["source_MAP_different_SHA_floors"], [400])
        z = self.by_floor[400]
        self.assertEqual(len(z["source_MAP_full_original_rows"]), 2)
        self.assertEqual(len({r["source_sha256"] for r in z["source_MAP_full_original_rows"]}), 2)
        self.assertEqual(self.summary["selected_MAP_status"]["MAP_EXTRACTION_ERROR_ONLY"]["floor_count"], 5)
        self.assertEqual(self.summary["selected_MAP_status"]["TWO_MAP_COPIES_SAME_SHA"]["floor_count"], 7)

    def test_07_member_size_formula_not_real_DAT_decoding(self):
        self.assertEqual(self.summary["original_DAT_error_size_coherent_floors"], 13)
        self.assertFalse(self.published["evidence_limits"]["failed_member_partial_bytes_claimed_qualified"])
        self.assertFalse(self.published["evidence_limits"]["original_DAT_archive_corruption_proven"])

    def test_08_INTEGRATION06_1300_strict_count_and_source_hash_retained(self):
        row = self.by_floor[1300]
        prior = self.data["prior"]
        self.assertEqual(row["quest05_source_CREATE_count"], prior["source_counts"]["CREATE_rows"])
        self.assertEqual(row["source_MAP_full_original_rows"][0]["source_sha256"],
                         prior["original_MAP_rows"][0]["original_sha256"])
        self.assertEqual(row["source_DAT_original_read_errors"][0]["expected_member_bytes"], 60008)

    def test_09_no_wrong_deployment_or_native_world_promotion(self):
        b = self.published["evidence_limits"]
        for key in ("original_native_world_playable", "original_npc_created_at_runtime",
                    "early_official_same_deployment", "published_original_commercial_bytes"):
            self.assertFalse(b[key])
        self.assertEqual(self.published["status"], "SOURCE_BOUNDED_PARTIAL")
        self.assertIsNone(b["overall_percent"])

    def test_10_full_derived_snapshot_recomputes_exactly(self):
        self.assertEqual(validate(), self.summary)

if __name__ == "__main__":
    unittest.main()
