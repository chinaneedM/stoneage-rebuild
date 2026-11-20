"""PET126C private TW1 original retail source: derived acceptance only.

CI never obtains or executes the private 372 MB original archive; this checks
the immutable published receipt against independently archived source metadata.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
RECEIPT = R / "STONEAGE-PET126C-TW10-PRIVATE-CLIENT-REACCESS-SOURCE-ROLE-R1.json"
P38 = R / "STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json"
P20 = R / "STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json"
Q = R / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
META = R / "tw10-resource-metadata/MANIFEST-R1.txt"
REPORT = ROOT / "docs/continuity/STONEAGE-PET126C-TW10-PRIVATE-CLIENT-REACCESS-AND-PET-IDENTITY-GATE-20261120.md"


class PET126CPrivateTW1Custody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(RECEIPT.read_text(encoding="utf-8"))
        cls.p38 = json.loads(P38.read_text(encoding="utf-8"))
        cls.p20 = json.loads(P20.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_exact_372mb_archive_custody_hash_members_crc(self):
        r = self.r["archive"]
        tw = next(x for x in self.p38["records"] if x["id"] == "TW_WAEI_JSS_1_0_RETAIL")
        self.assertEqual(r["private_original_filename"], tw["source_package_filename"])
        self.assertEqual(r["byte_size"], tw["size_bytes"])
        self.assertEqual(r["sha256"], tw["zip_sha256"])
        self.assertEqual(r["zip_members_total"], tw["zip_member_count"])
        self.assertEqual(r["zip_members_crc32_checked"], 379)
        self.assertTrue(r["zip_members_crc32_all_ok"])
        self.assertTrue(r["actual_raw_bytes_read_in_this_work_unit"])
        self.assertTrue(r["full_sha256_recomputed_in_this_work_unit"])
        self.assertEqual(r["zip_password_encrypted_members"], 0)
        self.assertEqual(r["original_client_source_members"], 375)
        self.assertEqual(r["prior_private_observer_members"], 4)
        self.assertEqual(r["original_client_source_members"] +
                         r["prior_private_observer_members"], 379)
        self.assertEqual(sum(r["original_member_extension_counts"].values()), 375)
        self.assertEqual(r["original_member_extension_counts"]["sab"], 218)
        self.assertEqual(r["original_member_extension_counts"]["wav"], 127)
        self.assertEqual(r["original_member_extension_counts"]["bin"], 6)
        self.assertEqual(r["original_member_extension_counts"]["sap"], 16)
        self.assertEqual(len(r["all_379_member_sorted_JSON_manifest_sha256"]), 64)
        self.assertEqual(len(r["original_375_member_sorted_JSON_manifest_sha256"]), 64)

    def test_original_same_source_pet_graphics_and_program_hashes(self):
        r = self.r["archive"]["original_member_full_sha256_and_zip_crc32"]
        self.assertEqual(len(r), 8)
        text = META.read_text(encoding="utf-8")
        for name in ("adrn_1.bin", "spr_1.bin", "spradrn_1.bin", "real_1.bin"):
            path = "source/data/" + name
            self.assertIn(path, r)
            row = r[path]
            self.assertIn("SOURCE|name=" + name + "|bytes=" + str(row["byte_size"]) +
                          "|sha256=" + row["sha256"], text)
            self.assertEqual(len(row["zip_crc32_hex"]), 8)
            self.assertEqual(len(row["sha256"]), 64)
        self.assertEqual(r["source/data/real_1.bin"]["byte_size"], 315842228)
        self.assertEqual(r["source/data/spr_1.bin"]["byte_size"], 2889630)
        self.assertEqual(r["source/sa_3.exe"]["byte_size"], 425984)
        self.assertEqual(r["source/StoneAge.exe"]["byte_size"], 409600)

    def test_absence_of_named_standalone_master_is_only_file_tree_negative(self):
        a = self.r["pet_source_role_audit"]
        self.assertTrue(a["directory_scan_exhaustive_source_member_names"])
        self.assertEqual(a["source_subtree_pet_monster_skill_master_named_file_count"], 0)
        self.assertFalse(a["standalone_same_build_pet_id_name_growth_skill_master_identified"])
        self.assertFalse(a["file_name_or_literal_nonmatch_proves_no_embedded_or_server_pet_master"])
        self.assertFalse(a["original_client_embedded_full_species_names_verified"])
        self.assertIsNone(a["original_original_pc_pet_species_master_count"])
        self.assertEqual([x["number_of_lines"] for x in a["original_text_files"]], [233, 114])
        self.assertTrue(all(x["pet_skill_capture_keyword_hits"] == 0
                            for x in a["original_text_files"]))
        self.assertTrue(a["client_local_graphic_asset_present"])
        self.assertFalse(a["actual_same_build_pet_name_to_sprite_identity_link_verified"])
        self.assertFalse(a["first_official_pet_release_proven_from_client"])
        self.assertFalse(a["original_client_native_runtime_executed_this_work_unit"])
        self.assertFalse(a["original_server_contacted_this_work_unit"])

    def test_no_recounted_pet_species_community_or_early_animated_graphics(self):
        r = self.r
        old = r["previous_verified_derivatives_reused_not_reexecuted"]
        source = self.p20["source_coverage_observed"]
        self.assertEqual(old["previous_selected_candidate_spr_groups"],
                         source["TW10_selected_source_SPR_groups"])
        self.assertEqual(old["previous_source_sequences"],
                         source["TW10_original_animation_sequences"])
        self.assertEqual(old["previous_source_frame_positions"],
                         source["TW10_original_frame_positions"])
        self.assertEqual(old["new_pet_species_proved_by_this_reaccess"], 0)
        self.assertEqual(old["new_pet_animations_extracted_by_this_reaccess"], 0)
        self.assertEqual(r["module_status"], "SOURCE_BOUNDED_PARTIAL")
        self.assertFalse(r["pet_module_source_bounded_closed"])
        self.assertIsNone(r["original_pc_global_pet_species_count"])
        self.assertIsNone(r["official_2026_first_release_species_count"])
        self.assertEqual(r["year_2026_status"], "NOT_YEAR_AUDITED")
        self.assertEqual(self.q["current_frontier"]["year"], 2026)
        self.assertEqual(next(y for y in self.q["yearly_work_queue"] if y["year"] == 2026)["research_gate"],
                         "NOT_YEAR_AUDITED")

    def test_ci_does_not_claim_372mb_execution_or_publish_original_art(self):
        r = self.r
        self.assertFalse(r["action_ci_full_private_archive_replay_possible"])
        self.assertTrue(r["rights_privacy"]["source_archive_in_personal_private_library"])
        self.assertFalse(r["rights_privacy"]["original_client_or_graphics_published_in_public_git"])
        self.assertFalse(r["rights_privacy"]["source_library_file_id_published"])
        self.assertFalse(r["rights_privacy"]["production_rights_cleared"])
        self.assertEqual(r["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(r["stage_B_wiki"], "GATED")
        self.assertEqual(r["r79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(r["overall_percent"])
        self.assertIn("PET126C", REPORT.read_text(encoding="utf-8"))

    def test_immutable_historical_current(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), self.r["historical_current_file_size"])
        git = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(git, self.r["historical_current_blob"])
        self.assertEqual(git, "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
