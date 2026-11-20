"""PET126C: public acceptance of independently re-read, authenticated TW1 private source."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
NEW = R / "STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json"
PRIOR = R / "STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
INVENTORY = R / "STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json"
YEAR = R / "STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json"


class Pet126CAuthenticatedBytesReaccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recheck = json.loads(NEW.read_text(encoding="utf-8"))
        cls.prior = json.loads(PRIOR.read_text(encoding="utf-8"))
        cls.inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        cls.year = json.loads(YEAR.read_text(encoding="utf-8"))

    def test_original_private_custody_matches_pinned_source(self):
        re = self.recheck["original_source"]
        tw = next(x for x in self.inventory["records"] if x["id"] == "TW_WAEI_JSS_1_0_RETAIL")
        self.assertEqual((re["archive_bytes"], re["archive_sha256"]),
                         (tw["size_bytes"], tw["zip_sha256"]))
        self.assertEqual((re["zip_member_count"], re["zip_members_sha256_rehashed_this_session"],
                          re["zip_members_full_read_crc_passed_this_session"],
                          re["source_original_member_count"],
                          re["source_original_members_sha256_rehashed_this_session"]),
                         (379, 379, 379, 375, 375))
        self.assertTrue(re["private_original_source_not_published"])
        self.assertEqual(re["source_grade"],
                         "ORIGINAL_RETAIL_SOURCE_VERIFIED_REACCESSED_THIS_SESSION")
        for key, p in self.recheck["source_file_pins"].items():
            old = self.prior["archive"]["files"][key]
            self.assertEqual((p["bytes"], p["sha256"], p["crc32"]),
                             (old["bytes"], old["sha256"], old["crc32"]))

    def test_independent_compiled_table_spr_and_rd_replay_no_species_promotion(self):
        t = self.recheck["independent_read_only_pet_album_recheck"]
        pt = self.prior["table"]
        self.assertEqual((t["original_binary_table_offset"], t["original_binary_table_rows"],
                          t["original_binary_table_stride_bytes"], t["original_binary_table_sha256"]),
                         (pt["file_offset"], pt["rows"], pt["stride"], pt["sha256"]))
        named = self.prior["records"]
        self.assertEqual((len(named),len(pt["placeholder_graphics"])),(124,57))
        self.assertEqual((t["same_build_named_graphic_spr_candidates"], t["table_placeholders"]),
                         (124,57))
        self.assertEqual(t["placeholders_with_spr_but_no_name"],
                         len(pt["placeholder_graphics_with_spr"]))
        self.assertEqual(t["same_build_named_spr_sequences"],
                         sum(r["source_sequences"] for r in named))
        self.assertEqual(t["same_build_named_spr_frame_references"],
                         sum(r["source_frame_positions"] for r in named))
        self.assertEqual(t["physical_original_portrait_rd_verified"],
                         sum(r["portrait_rd"] is not None for r in named))
        self.assertEqual(t["original_portrait_missing_graphic_numbers"],
                         [r["graphic_number"] for r in named if r["portrait_rd"] is None])
        self.assertEqual((t["source_spr_group_count_not_species"],
                          t["source_spr_animation_count_not_species"],
                          t["source_spr_frame_references_not_species"]),
                         (self.prior["client_spr"]["groups"],
                          self.prior["client_spr"]["sequences"],
                          self.prior["client_spr"]["frame_positions"]))
        self.assertEqual(t["new_pet_species_authenticated"], 0)
        self.assertFalse(t["live_pet_release_authenticated"])
        self.assertFalse(t["native_game_executed"])
        self.assertIsNone(t["historical_official_pet_species_count"])

    def test_2026_pc_only_year_and_module_remain_open(self):
        re = self.recheck
        self.assertEqual(re["active_module"],"PET")
        self.assertEqual(re["scope"],"OFFICIAL_ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual((re["working_year"],re["working_year_status"]),
                         (2026,"NOT_YEAR_AUDITED"))
        self.assertEqual(self.year["annual_review"]["yearly_research_gate"],"NOT_YEAR_AUDITED")
        self.assertTrue(re["evidence_limits"]["no_mobile_scope"])
        self.assertTrue(re["evidence_limits"]["only_hashes_counts_public"])
        self.assertTrue(re["evidence_limits"]["public_ci_does_not_claim_private_zip_reexecution"])
        g = re["module_gate"]
        self.assertEqual(g["current"],"SOURCE_BOUNDED_PARTIAL")
        for k in ("source_bounded_closed","historically_complete","native_runtime_verified",
                  "next_module_unlocked"):
            self.assertFalse(g[k])
        self.assertIsNone(g["overall_percent"])

    def test_historical_current_git_blob_unchanged(self):
        original = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(original),2709173)
        git_sha = hashlib.sha1(b"blob " + str(len(original)).encode() + bytes([0]) + original).hexdigest()
        self.assertEqual(git_sha, self.recheck["links"]["historical_current_blob"])
        self.assertEqual(git_sha,"c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
