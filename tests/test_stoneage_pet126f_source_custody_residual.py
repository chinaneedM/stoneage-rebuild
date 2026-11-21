"""PET126F public cross-receipt audit; does not claim to run or publish private game media."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/recovered"


def rec(name):
    return json.loads((DIR / name).read_text(encoding="utf-8"))


class Pet126fCustodyAndSevenDimensionPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = rec("STONEAGE-PET126F-SOURCE-CUSTODY-SEVEN-DIMENSION-RESIDUAL-R1.json")
        cls.c = rec("STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json")
        cls.e = rec("STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json")
        cls.p15 = rec("STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json")
        cls.p19 = rec("STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json")
        cls.p20 = rec("STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json")
        cls.p25 = rec("STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json")
        cls.p26 = rec("STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json")

    def test_tw1_original_source_sha_members_and_five_core_files_are_exact(self):
        f = self.f
        original = f["private_custody_rechecked_this_session"]["tw1_original_archive"]
        earlier = self.c["original_source"]
        self.assertEqual((original["bytes"], original["sha256"]),
                         (earlier["archive_bytes"], earlier["archive_sha256"]))
        self.assertEqual(original["members"], earlier["zip_member_count"])
        self.assertEqual(original["source_members"], earlier["source_original_member_count"])
        self.assertTrue(original["crc_all_pass"])
        self.assertEqual(sum(original["source_extension_counts"].values()), original["source_members"])
        self.assertEqual(len(original["source_bin_data_filenames"]), 6)
        self.assertEqual(original["source_extension_counts"][".bin"], 6)
        self.assertFalse(original["standalone_file_named_official_pet_server_master_found_in_member_list"])
        self.assertTrue(original["negative_filename_inventory_only_not_embedded_data_exclusion"])
        source_members = self.p15["source_members"]
        self.assertEqual(len(original["verified_member_hashes"]), 5)
        for name, pin in original["verified_member_hashes"].items():
            key = Path(name).name
            self.assertIn(key, source_members)
            self.assertEqual([pin["bytes"], pin["sha256"]], source_members[key])
        self.assertFalse(original["source_original_executed_this_unit"])
        self.assertFalse(original["server_connection_this_unit"])

    def test_pet15_derived_replay_is_recovered_not_second_official_client(self):
        derived = self.f["private_custody_rechecked_this_session"]["pet15_derived_private_observer"]
        self.assertEqual(derived["bytes"], self.p15["private_zip_bytes"])
        self.assertEqual(derived["sha256"], self.p15["private_zip_sha256"])
        self.assertEqual(derived["zip_members"], 32157)
        self.assertTrue(derived["crc_all_pass"])
        self.assertEqual(derived["rendered_png_count"], self.p15["distinct_original_bitmaps"])
        self.assertEqual(derived["receipt_entry_count"], derived["rendered_png_count"])
        self.assertTrue(derived["png_id_set_exactly_matches_private_receipt_keys"])
        self.assertEqual(derived["png_sha256_against_private_receipts_verified"], 32155)
        self.assertEqual(derived["png_sha256_mismatches"], 0)
        self.assertEqual(self.p15["source_bitmap_statuses"]["strict"],
                         derived["strict_decode_receipt_count"])
        self.assertEqual(self.p15["source_bitmap_statuses"]["terminal_zero_outside_canvas"],
                         derived["bounded_terminal_zero_outside_canvas_count"])
        self.assertEqual(self.p15["bounded_bitmaps"],
                         derived["bounded_original_bitmap_numbers"])
        self.assertFalse(derived["private_rendered_pngs_are_original_game_binary"])
        self.assertFalse(derived["private_proprietary_images_published"])
        self.assertEqual(self.f["decision"]["prior_original_source_custody_reverified"], 1)
        self.assertEqual(self.f["decision"]["prior_private_derived_observer_reverified"], 1)
        self.assertEqual(self.f["decision"]["new_independent_original_client_carriers_acquired_this_unit"], 0)

    def test_no_species_count_from_web_positions_graphics_or_skill_references(self):
        f = self.f["field_coverage_preserved"]
        album = self.c["independent_read_only_pet_album_recheck"]
        values = {
            "tw1_pet_album_client_table_positions": "original_binary_table_rows",
            "tw1_pet_album_names_with_spr": "same_build_named_graphic_spr_candidates",
            "tw1_pet_album_placeholder_positions": "table_placeholders",
            "tw1_placeholder_positions_with_spr_but_no_name": "placeholders_with_spr_but_no_name",
            "tw1_album_named_spr_sequences": "same_build_named_spr_sequences",
            "tw1_album_named_frame_refs": "same_build_named_spr_frame_references",
            "tw1_album_portrait_source_rd_present": "physical_original_portrait_rd_verified",
            "tw1_album_portrait_source_rd_missing_ids": "original_portrait_missing_graphic_numbers",
        }
        for mine, original in values.items():
            self.assertEqual(f[mine], album[original])
        p20 = self.p20["source_coverage_observed"]
        self.assertEqual(f["pet16_mixed_source_rows_not_species"],
                         p20["PET16_namespaces_sum_NOT_species"])
        self.assertEqual(f["pet15_selected_graphic_groups_not_species"],
                         len(self.p15["groups"]))
        self.assertEqual(f["pet15_selected_sequences"], p20["TW10_original_animation_sequences"])
        self.assertEqual(f["pet15_selected_frame_positions"], self.p15["frame_positions"])
        self.assertEqual(f["pet15_distinct_original_bitmap_keys"], self.p15["distinct_original_bitmaps"])
        self.assertEqual(f["pet15_strict_bitmap_keys"], self.p15["source_bitmap_statuses"]["strict"])
        self.assertEqual(f["pet15_bounded_bitmap_keys"], self.p15["source_bitmap_statuses"]["terminal_zero_outside_canvas"])
        self.assertEqual(f["tw1_original_exe_s_k_status_pets_fields"], self.e["k_parser"]["field_count"])
        self.assertEqual(f["tw1_original_exe_pet_slot_count"], self.e["capture_join"]["count_total_slots"])
        self.assertEqual(f["official_cn_pet25_documentary_events_not_species"],
                         self.p25["counts"]["release_documentary_records"])
        self.assertEqual(f["official_jp_pet26_documentary_events_not_species"],
                         self.p26["counts"]["new_japan_release_events"])
        self.assertEqual(f["official_pc_documentary_events_not_species"],
                         self.p26["counts"]["combined_release_events_not_species"])
        self.assertIsNone(f["historically_confirmed_complete_global_pc_species_count"])

    def test_2016_and_mixed_skill_gaps_remain_in_source_namespaces(self):
        f = self.f["field_coverage_preserved"]
        totals = self.p19["totals"]
        a = totals["later2016"]
        b = totals["mixed25_primary"]
        c = totals["mixed25_alternative"]
        self.assertEqual(f["community2016_positive_skill_references"], a["positive_skill_slot_references"])
        self.assertEqual(f["community2016_skill_refs_missing_same_selected_table"], a["missing_in_selected_petskill2"])
        self.assertEqual(f["community2016_distinct_missing_skill_ids"], a["distinct_missing_skill_ids"])
        self.assertEqual(f["mixed25_main_positive_skill_refs"], b["positive_skill_slot_references"])
        self.assertEqual(f["mixed25_main_missing_same_source"], b["undefined_in_own_primary_skill_table"])
        self.assertEqual(f["mixed25_alt_positive_skill_refs"], c["positive_skill_slot_references"])
        self.assertEqual(f["mixed25_alt_missing_same_source"], c["missing_in_own_alternative_skill_table"])
        self.assertNotEqual(self.f["seven_dimensions"][4]["conclusion"], "CLOSED")

    def test_module_gates_are_unaltered_and_original_current_preserved(self):
        f, decision = self.f, self.f["decision"]
        self.assertEqual(f["scope"], "OFFICIAL_ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(f["active_module"], "PET")
        self.assertEqual(len(f["seven_dimensions"]), 7)
        self.assertEqual([x["id"] for x in f["seven_dimensions"]],
                         [x["id"] for x in self.p20["seven_pet_dimensions"]])
        self.assertTrue(all(not x["closed"] for x in f["seven_dimensions"]))
        self.assertEqual(decision["module"], "SOURCE_BOUNDED_PARTIAL")
        self.assertEqual(decision["year2026"], "NOT_YEAR_AUDITED")
        self.assertEqual(decision["all_six_regions_ytd"], "YTD_PARTIAL_OPEN")
        for key in ("source_bounded_closed", "historically_complete",
                    "native_runtime_verified", "release_roster_complete",
                    "may_request_user_switch_to_npc"):
            self.assertFalse(decision[key], key)
        self.assertEqual(decision["new_official_species_authenticated_this_unit"], 0)
        self.assertIsNone(decision["overall_completion_percent"])
        self.assertEqual(decision["stage_a"], "7_PARTIAL_2_OPEN")
        self.assertEqual(decision["stage_b_wiki"], "GATED")
        self.assertEqual(decision["r79"], "PAUSED_NON_BLOCKING")
        self.assertFalse(self.p20["source_bounded_closed"])
        self.assertEqual(len(f["priority_after_preflight"]), 3)
        source = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(source), 2709173)
        sha = hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + bytes([0]) + source).hexdigest()
        self.assertEqual(sha, f["historical_current_blob"])
        self.assertEqual(sha, "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
