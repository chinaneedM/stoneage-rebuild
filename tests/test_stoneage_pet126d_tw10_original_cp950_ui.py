"""PET126D: independently reproducible CP950 literal digests with TW1 static/nonruntime limits."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
DERIVED = R / "STONEAGE-PET126D-TW10-ORIGINAL-CLIENT-PET-UI-CP950-LITERALS-R1.json"
PRIOR = R / "STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json"
ALBUM = R / "STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
QUEUE = R / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET126D-TW10-BIG5-ORIGINAL-PET-UI-STATIC-SOURCE-20261120.md"


class PET126DOriginalCP950StaticPetText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DERIVED.read_text(encoding="utf-8"))
        cls.prior = json.loads(PRIOR.read_text(encoding="utf-8"))
        cls.album = json.loads(ALBUM.read_text(encoding="utf-8"))
        cls.queue = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_original_same_source_exe_hash_only_no_private_binary_in_ci(self):
        d = self.d
        p = self.prior["source_file_pins"]["source/sa_3.exe"]
        self.assertEqual(d["origin"]["original_exe_zip_member"], "source/sa_3.exe")
        self.assertEqual(d["origin"]["exe_sha256"], p["sha256"])
        self.assertEqual(d["origin"]["exe_size_bytes"], p["bytes"])
        self.assertEqual(d["origin"]["original_client_archive_sha256"],
                         self.prior["original_source"]["archive_sha256"])
        self.assertTrue(d["origin"]["original_exe_bytes_re_read_private_work_unit"])
        self.assertFalse(d["origin"]["original_exe_publicly_committed"])
        self.assertTrue(d["origin"]["not_second_independent_client"])
        self.assertEqual(d["origin"]["baseline_merged_main"],
                         "0698eaab1020a909d14166beefbc2eb59f47a282")
        self.assertEqual(d["origin"]["original_archive_receipt"],
                         "research/recovered/STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json")

    def test_exact_short_literal_byte_digests_and_offsets_not_native_action(self):
        d = self.d
        rows = d["rows"]
        self.assertEqual(d["encoding"], "cp950_big5")
        self.assertEqual(len(rows), 9)
        self.assertEqual(d["row_count"], 9)
        self.assertEqual(d["total_byte_pattern_occurrences"], 10)
        self.assertEqual(len({r["id"] for r in rows}), 9)
        self.assertEqual(sum(r["original_byte_match_count"] for r in rows), 10)
        for r in rows:
            b = r["short_original_ui_literal"].encode("cp950", "strict")
            self.assertEqual(r["byte_length"], len(b))
            self.assertEqual(r["cp950_literal_sha256"], hashlib.sha256(b).hexdigest())
            self.assertEqual(len(r["original_file_offset_zero_based"]),
                             r["original_byte_match_count"])
            self.assertTrue(all(0 <= o <= d["origin"]["exe_size_bytes"] - len(b)
                                for o in r["original_file_offset_zero_based"]))
            self.assertEqual(r["source_status"],
                             "TW10_CLIENT_LITERAL_PRESENT_SOURCE_BYTES_VERIFIED_ONLY")
            self.assertTrue(r["not_a_pet_species_identity"])
            self.assertTrue(r["not_native_action_executed"])

    def test_offsets_and_substring_not_reclassified_as_two_ui_actions(self):
        d = {r["id"]: r for r in self.d["rows"]}
        self.assertEqual(d["capture_command"]["original_file_offset_zero_based"], [352000])
        self.assertEqual(d["capture_capacity_text"]["original_file_offset_zero_based"], [352008])
        self.assertEqual(d["pet_switch_command"]["original_file_offset_zero_based"], [352128])
        self.assertEqual(d["use_skill_command"]["original_file_offset_zero_based"], [352180])
        self.assertEqual(d["pet_choice_prompt"]["original_file_offset_zero_based"], [366255, 366334])
        self.assertEqual(d["pet_or_teammate_prompt"]["original_file_offset_zero_based"], [366334])
        self.assertEqual(d["pet_mail_notification"]["original_file_offset_zero_based"], [379308])
        sub = self.d["substring_guard"]
        self.assertTrue(sub["two_offsets_due_to_substring_at_start_of_longer_literal"])
        self.assertTrue(sub["not_two_independent_menu_actions_proved"])

    def test_no_species_or_runtime_promotion(self):
        d = self.d
        self.assertTrue(all(d["negative_boundary"].values()))
        self.assertFalse(d["observed_qualification"]["pet_command_action_runtime_invoked"])
        self.assertFalse(d["observed_qualification"]["pet_capture_success_or_server_result_verified"])
        self.assertFalse(d["observed_qualification"]["species_name_id_graphic_in_same_build_verified"])
        self.assertFalse(d["observed_qualification"]["original_pet_skill_effect_learning_rule_verified"])
        self.assertFalse(d["observed_qualification"]["any_new_pet_species_discovered"])
        self.assertFalse(d["source_bounded_close"])
        self.assertEqual(self.prior["independent_read_only_pet_album_recheck"]
                         ["same_build_named_graphic_spr_candidates"], 124)
        self.assertEqual(self.queue["current_frontier"]["year"], 2026)
        year = next(x for x in self.queue["yearly_work_queue"] if x["year"] == 2026)
        self.assertEqual(year["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(d["year_2026"], "NOT_YEAR_AUDITED")
        self.assertEqual((d["stage_A"], d["stage_B_wiki"], d["r79"], d["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))
        self.assertIn("PET126D", REPORT.read_text(encoding="utf-8"))

    def test_current_state_full_historical_blob_still_exact(self):
        b = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(b), 2709173)
        h = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()
        self.assertEqual(h, self.d["historical_current_blob"])
        self.assertEqual(h, "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
