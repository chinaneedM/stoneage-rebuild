"""PET09 rights-safe, exact-version pet graphic/reference acceptance gates."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json"
SOURCE = ROOT / "research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json"


class Pet09SourceMaterialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.records = cls.report["records"]
        cls.by_spr = {r["tw85_original_spr_no_not_official_pet_id"]: r for r in cls.records}

    def test_only_original_pc_and_no_species_or_runtime_upgrade(self):
        self.assertEqual(self.report["schema"], "stoneage.pet.high_first_09.tw85_source_visual_action_reference.r1")
        self.assertEqual(self.report["source_scope"], "PRESERVED_TW85_CLASSIC_PC_UNCERTIFIED_OFFICIAL_PRESSING")
        self.assertEqual(self.report["metrics"]["official_live_species_newly_verified"], 0)
        self.assertEqual(self.report["metrics"]["original_rd_pixels_rendered_in_this_work"], 0)
        self.assertTrue(self.report["boundaries"]["source_local_name_is_not_official_live_release"])
        self.assertTrue(self.report["boundaries"]["patch_alias_is_not_physical_rd_bitmapno"])
        self.assertTrue(self.report["boundaries"]["no_default_winner_for_duplicate_patch_or_adrn_records"])
        self.assertTrue(self.report["boundaries"]["raw_animation_indices_are_not_observed_gameplay_actions"])
        self.assertFalse(self.report["boundaries"]["full_original_program_execution_verified"])
        self.assertFalse(self.report["boundaries"]["original_private_pixels_in_public_report"])
        self.assertFalse(self.report["boundaries"]["historic_same_deployment_pet_master_skill_capture"])

    def test_exact_source_cardinality_and_conservation(self):
        m = self.report["metrics"]
        self.assertEqual((len(self.records), len(self.by_spr)), (550, 550))
        self.assertEqual(m["source_physical_sprite_occurrences"], 554)
        self.assertEqual(m["graphic_numbers_with_any_source_local_name"], 514)
        self.assertEqual(m["graphic_numbers_without_source_local_name"], 36)
        self.assertEqual(m["cross_executable_name_conflict_graphics"], 41)
        self.assertEqual(m["per_program_named_graphic_numbers"],
                         {"sa.exe": 508, "sb.exe": 497, "sc.exe": 227, "sd.exe": 464})
        s = m["source_physical_group_frame_metrics"]
        self.assertEqual(s["frame_occurrences"], 137211)
        self.assertEqual(s["mapped_frames"], 137192)
        self.assertEqual(s["sentinel_frames"], 19)
        self.assertEqual(s["missing_frames"], 0)
        self.assertEqual(s["missing_bitmap_ids"], 0)
        self.assertEqual(s["frame_occurrences"], s["mapped_frames"] + s["sentinel_frames"])
        self.assertEqual(
            sum(len(row["original_physical_sprite_occurrences"]) for row in self.records), 554
        )
        self.assertEqual(
            sum(x["frame_occurrences"] for row in self.records
                for x in row["original_physical_sprite_occurrences"]), 137211
        )

    def test_exact_four_program_original_source_identity_and_conflicts(self):
        for src in self.source["records"]:
            graphic = src["tw85_original_spr_number"]
            row = self.by_spr[graphic]
            self.assertEqual(row["cross_executable_name_conflict"],
                             src["graphic_has_conflicting_names_across_installer_programs"])
            for exe in ("sa.exe", "sb.exe", "sc.exe", "sd.exe"):
                a, b = src["program_routes"][exe], row["original_native_program_routes"][exe]
                self.assertEqual(a["local_album_slot"], b["local_album_slot"])
                self.assertEqual(a["record_source_status"], b["status"])
                self.assertEqual(a["original_name_cp950"], b["original_name_cp950"])
                self.assertEqual(a["original_album_row_sha256"], b["original_28b_record_sha256"])
                self.assertFalse(b["historical_official_live_release_verified"])
            self.assertFalse(row["native_runtime_action_semantics_verified"])
            self.assertIsNone(row["original_skill_stats_capture_birth_growth_and_release"])
            self.assertEqual(
                [v["original_source_group_index"] for v in row["original_physical_sprite_occurrences"]],
                [v["source_occurrence_index"] for v in src["source_spr_occurrences"]],
            )
            for v in row["original_physical_sprite_occurrences"]:
                self.assertTrue(v["all_frame_bitmap_references_qualified_in_same_saved_carrier"])
                self.assertEqual(len(v["ordered_frame_reference_sha256"]), 64)
                self.assertEqual(
                    sum(x["frame_positions"] for x in v["raw_animation_index_frame_counts"]),
                    v["frame_occurrences"],
                )

    def test_207_aliases_182_patch_proofs_25_open(self):
        m = self.report["metrics"]
        self.assertEqual(m["distinct_source_local_portrait_aliases"], 207)
        self.assertEqual(m["source_local_portrait_aliases_not_in_cn50_named_catalog"], 203)
        self.assertEqual(m["aliases_with_patch_records"], 182)
        self.assertEqual(m["aliases_not_in_patch"], 25)
        self.assertEqual(m["patch_candidate_rows"], 182)
        self.assertEqual(m["exact_native_record_candidates"], 182)
        portrait = self.report["portrait_alias_to_saved_tw85_native_rd_candidates"]
        self.assertEqual(len(portrait), 207)
        self.assertEqual(sum(not matches for matches in portrait.values()), 25)
        for alias, matches in portrait.items():
            self.assertTrue(alias.isdecimal())
            for row in matches:
                self.assertFalse(row["renderer_default_choice_proven"])
                self.assertEqual(row["patch_to_native_qualification"],
                                 "EXACT_NATIVE_RECORD_AND_RD_STRUCTURE")
                self.assertEqual(len(row["native_exact_candidates"]), 1)
                for native in row["native_exact_candidates"]:
                    self.assertEqual(native["rd_sha256"], row["saved_tw85_real_rd_sha256"])
                    self.assertEqual(native["bitmapno"], row["physical_bitmapno"])
                    self.assertEqual(len(native["rd_sha256"]), 64)
        self.assertEqual(self.by_spr[101501]["original_native_program_routes"]["sa.exe"]["original_name_cp950"],
                         "雷帝斯洛")
        self.assertEqual(self.by_spr[101669]["original_native_program_routes"]["sd.exe"]["original_name_cp950"],
                         "地人龍")
        self.assertEqual(len(self.by_spr[101866]["original_physical_sprite_occurrences"]), 3)


if __name__ == "__main__":
    unittest.main()
