"""PET20 source-bounded pet closure matrix: no historic species-count or runtime promotion."""
import json
import unittest
from pathlib import Path

from tools.stoneage_preproduction_archive import APPROVED_LATER_SOURCE_BLOBS, gitblob

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class Pet20ClosureMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = read_json("research/recovered/STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json")
        cls.pet09 = read_json("research/recovered/STONEAGE-PET-MODULE-09-CROSSCARRIER-ORIGINAL-MATERIAL-RECEIPTS-R1.json")
        cls.pet12 = read_json("research/recovered/STONEAGE-PET-MODULE-12-TW85-SIX-CAPTURE-SPR-RD-BRIDGE-R1.json")
        cls.pet13 = read_json("research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json")
        cls.pet15 = read_json("research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json")
        cls.pet16 = read_json("research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
        cls.pet19 = read_json("research/recovered/STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json")
        cls.i87 = read_json("research/recovered/STONEAGE-INTEGRATION87-36-GETPET-TW10-SPR-2D-BRIDGE-R1.json")

    def test_all_source_git_blobs_match_actual_full_files(self):
        for key, pin in self.matrix["sources"].items():
            with self.subTest(key=key):
                observed = gitblob((ROOT / pin["path"]).read_bytes())
                if key == "growth":
                    revision = APPROVED_LATER_SOURCE_BLOBS[pin["path"]]
                    self.assertEqual(revision["historical_archive_blob"], pin["git_blob"])
                    self.assertIn(observed, (pin["git_blob"], revision["blob"]))
                    observed = gitblob(
                        (R / "STONEAGE-LEGACY-PET-GROWTH-CORE-R1-SOURCE-SNAPSHOT.md").read_bytes()
                    )
                self.assertEqual(observed, pin["git_blob"])

    def test_exact_pet16_namespace_rows_are_not_counted_as_species(self):
        m = self.matrix["source_coverage_observed"]
        by_namespace = {x: len(y) for x, y in self.pet16["datasets"].items()}
        self.assertEqual(m["PET16_namespace_records_NOT_species"], by_namespace)
        self.assertEqual(sum(by_namespace.values()), 2792)
        self.assertEqual(m["PET16_namespaces_sum_NOT_species"], 2792)
        self.assertFalse(self.matrix["historically_complete"])

    def test_pet15_original_tw10_motions_and_failure_boundary(self):
        m = self.matrix["source_coverage_observed"]
        self.assertEqual(m["TW10_selected_source_SPR_groups"], len(self.pet15["groups"]))
        self.assertEqual(m["TW10_selected_source_SPR_groups"], 131)
        self.assertEqual(m["TW10_original_animation_sequences"], 7672)
        self.assertEqual(m["TW10_original_frame_positions"], 73500)
        self.assertEqual(m["TW10_original_bitmap_keys"], 32155)
        self.assertEqual((m["TW10_strict_pixel_bits"], m["TW10_bounded_pixel_bits"]), (32150, 5))
        self.assertFalse(self.pet15["official_pet_identity_authenticated"])
        self.assertFalse(self.pet15["native_palette_or_frame_timing_verified"])

    def test_pet09_old_598_partition_not_confused_with_newer_131(self):
        old = self.matrix["source_coverage_observed"]["PET09_older_598_candidate_partition"]
        self.assertEqual(old, self.pet09["counts"])
        self.assertEqual(sum(old[k] for k in (
            "TW1_PET07_PRIVATE_PIXELS", "CN50_TW85_EXACT_ORIGINAL_SPR_ONLY",
            "TW85_R30_PRIOR_PRIVATE_PIXELS", "TW85_SPR_INDEX_ONLY", "NO_INDEX_FOUR_SAMPLES")), 598)
        self.assertEqual(old["TW1_PET07_PRIVATE_PIXELS"], 130)
        self.assertEqual(len(self.pet15["groups"]), 131)

    def test_pet12_six_source_indices_no_new_original_pixels(self):
        m = self.matrix["source_coverage_observed"]["PET12_source_index_qualified_TW85_six"]
        p = self.pet12["summary"]
        self.assertEqual(m["group_count"], p["group_occurrences"])
        self.assertEqual(m["sequences"], p["original_animation_sequences"])
        self.assertEqual(m["frame_positions"], p["original_frame_occurrences"])
        self.assertEqual(m["RD_source_index_refs"], p["distinct_referenced_original_same_carrier_bitmap_ids"])
        self.assertEqual((m["group_count"], m["sequences"], m["frame_positions"],
                          m["RD_source_index_refs"], m["original_new_pixels_in_PET12"]),
                         (6, 336, 2048, 1568, 0))
        self.assertEqual(m["graphic_numbers"], self.pet12["capture_candidate_graphics_six"])
        self.assertFalse(set(m["graphic_numbers"]).intersection(
            x["graphic_number"] for x in self.pet16["datasets"]["tw10_visual"]))

    def test_pet_capture_growth_and_skill_source_context_not_overstated(self):
        m = self.matrix["source_coverage_observed"]
        self.assertEqual(m["PET13_compiled_capture_static_rows"], self.pet13["summary"]["compiled_candidate_rows"])
        self.assertEqual(m["mixed25_GetPet_static_instance_ids"], self.i87["summary"]["source_getpet_unique_enemy_instance_ids"])
        self.assertEqual(m["PET19_missing_skill_totals"], self.pet19["totals"])
        self.assertEqual(m["PET19_missing_skill_totals"]["later2016"]["missing_in_selected_petskill2"], 102)
        self.assertEqual(m["PET19_missing_skill_totals"]["mixed25_alternative"]["missing_in_own_alternative_skill_table"], 12)
        self.assertTrue(self.matrix["provenance_not_reexecuted_in_this_pet20_work"])

    def test_seven_required_domains_and_open_gates(self):
        m = self.matrix
        self.assertEqual(m["active_module"], "PET")
        self.assertEqual(m["present_module_status"], "SOURCE_BOUNDED_PARTIAL")
        self.assertEqual(len(m["seven_pet_dimensions"]), 7)
        self.assertEqual(len({x["id"] for x in m["seven_pet_dimensions"]}), 7)
        taxonomy = set(m["evidence_taxonomy"])
        self.assertEqual(taxonomy, {"VERIFIED_SOURCE","CROSS_CARRIER_CANDIDATE",
                                    "MISSING_SOURCE","UNVERIFIED_RUNTIME"})
        for dimension in m["seven_pet_dimensions"]:
            self.assertTrue(set(dimension["evidence_statuses"]).issubset(taxonomy))
            self.assertTrue(dimension["witnessed"])
            self.assertTrue(dimension["missing"])
            self.assertTrue(dimension["reopen"])
            self.assertTrue(all(k in m["sources"] for k in dimension["source_keys"]))
        self.assertEqual(len(m["PET16_prior_gap_ids"]), 7)
        self.assertEqual([x["id"] for x in m["PET16_prior_gap_ids"]],
                         [x["id"] for x in self.pet16["coverage_gaps"]])
        self.assertFalse(m["source_bounded_closed"])
        self.assertFalse(m["historically_complete"])
        self.assertFalse(m["native_early_official_runtime_verified"])
        self.assertFalse(m["allowed_to_unlock_next_module"])
        self.assertIsNone(m["overall_completion_percent"])
        self.assertEqual(m["Stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(m["Stage_B_and_wiki"], "GATED")
        self.assertEqual(m["R79"], "PAUSED_NON_BLOCKING")
        self.assertEqual(m["historical_current_git_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")

    def test_future_reopening_requires_actual_source_evidence(self):
        self.assertEqual([x["id"] for x in self.matrix["next_intra_pet_work_priority"]],
                         ["PET21-01", "PET21-02", "PET21-03"])
        self.assertIn("Do not mark SOURCE_BOUNDED_CLOSED",
                      self.matrix["closure_review_required"])
        self.assertTrue(all(x["reason"] and x["stop"]
                            for x in self.matrix["next_intra_pet_work_priority"]))


if __name__ == "__main__":
    unittest.main()
