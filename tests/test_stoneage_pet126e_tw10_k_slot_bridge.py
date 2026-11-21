"""PET126E public regression: metadata agreement; does not read private original game bytes."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered/STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json"
D = ROOT / "research/recovered/STONEAGE-PET126D-TW10-CLIENT-CAPTURE-FIVE-SLOT-STATIC-R1.json"
S = ROOT / "research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json"


class OriginalTW1SKEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(R.read_text(encoding="utf-8"))
        cls.d = json.loads(D.read_text(encoding="utf-8"))
        cls.s = json.loads(S.read_text(encoding="utf-8"))

    def test_original_archive_and_exe_are_same_as_prior_source(self):
        r, d = self.r, self.d
        o, p = r["original_source"], d["source"]
        self.assertEqual(o["archive_size"], p["archive_bytes"])
        self.assertEqual(o["archive_sha256"], p["archive_sha256"])
        self.assertEqual(o["exe_size"], p["pe_member_bytes"])
        self.assertEqual(o["exe_sha256"], p["pe_member_sha256"])
        self.assertEqual(o["exe_member"], p["pe_member"])
        self.assertEqual(o["zip_crc_reverified_count"], 379)
        self.assertEqual(o["zip_crc_bad_count"], 0)
        self.assertFalse(o["original_exe_executed"])
        self.assertFalse(o["original_server_contacted"])
        self.assertFalse(o["published_original_payload"])

    def test_status_schema_has_exactly_twenty_fields_with_separate_semantic_grade(self):
        r = self.r
        k = r["k_parser"]
        prior = self.s["records"]["status_pet_full"]
        self.assertEqual(prior["transport"]["protocol"], "S")
        self.assertEqual(prior["transport"]["category"], "K")
        self.assertEqual(int(prior["transport"]["callback_rva"], 16), int(k["callback_rva"], 16))
        self.assertEqual(prior["transport"]["slot_prefix"], k["prefix"])
        self.assertEqual(prior["full_record_width"], 21)
        self.assertEqual(k["field_count"], 20)
        self.assertEqual(k["full_field_mask_count"], 20)
        self.assertEqual(len(k["field_map"]), 20)
        self.assertEqual(prior["fields"][0]["name"], "update_mask")
        for index, field in enumerate(k["field_map"]):
            source_field = prior["fields"][index + 1]
            self.assertEqual(field["token"], index + 2)
            self.assertEqual(source_field["position"], index + 2)
            self.assertEqual(field["name_from_early_lineage"], source_field["name"])
            self.assertEqual(field["semantic_evidence"], "EARLY_LINEAGE")
            self.assertEqual(field["position_and_address_evidence"], "TW1_EXE_DIRECT")
            self.assertEqual(field["delta_bit"], 1 << (index + 1))

    def test_full_and_partial_destination_layout_nonoverlap(self):
        k = self.r["k_parser"]
        base = int(k["slot_struct_base_va"], 16)
        self.assertEqual(k["stride"], 108)
        self.assertEqual(k["membership_flag_offset"], 104)
        self.assertEqual(k["secondary_flag_offset"], 106)
        self.assertEqual(int(k["membership_flag_va"], 16), base + 104)
        self.assertEqual(k["membership_flag_width"], 2)
        spans = []
        for index, field in enumerate(k["field_map"]):
            expected_start = (4 * index if index < 17
                              else 106 if index == 17
                              else 70 if index == 18 else 87)
            expected_width = 4 if index < 17 else 2 if index == 17 else 17
            self.assertEqual(field["struct_offset"], expected_start)
            self.assertEqual(field["source_width"], expected_width)
            self.assertLessEqual(expected_start + expected_width, 108)
            spans.append((expected_start, expected_start + expected_width))
            self.assertNotEqual(field["full_address_immediate_offset"],
                                field["delta_address_immediate_offset"])
        # Both text buffers and both word flags fit around exactly 17 DWORDs.
        spans += [(104, 106)]
        for i, (start, end) in enumerate(spans):
            for j, (other_start, other_end) in enumerate(spans):
                if i != j:
                    self.assertTrue(end <= other_start or other_end <= start)
        self.assertEqual(len(k["flag_address_immediate_positions"]), 2)

    def test_capture_count_is_linked_to_status_presence_flag_not_server_accept(self):
        r = self.r
        c, k, d = r["capture_join"], r["k_parser"], self.d
        self.assertEqual(c["count_va"], d["slot_counter"]["function_va"])
        self.assertEqual(c["count_total_slots"], d["slot_counter"]["slot_count"])
        self.assertEqual(c["count_predicate"], "16_BIT_FLAG_EQUALS_1")
        self.assertEqual(c["gate_va"], d["capture_gate"]["source_va"])
        self.assertEqual(c["second_gate_va"], d["second_counter_comparison"]["source_va"])
        self.assertEqual(c["count_threshold"], d["capture_gate"]["compare_count_against"])
        self.assertEqual(c["ui_loop_stride"], k["stride"])
        self.assertEqual(int(c["ui_loop_end_exclusive_va"], 16),
                         int(k["membership_flag_va"], 16) + 5 * 108)
        self.assertFalse(c["server_capture_accepted_proven"])
        self.assertFalse(c["account_storage_cap_proven"])
        self.assertFalse(k["slot_digit_range_validation_proven"])

    def test_byte_windows_are_pinned_but_public_ci_is_not_private_replay(self):
        w = self.r["source_windows"]
        self.assertEqual(len(w), 6)
        for item in w:
            self.assertGreater(item["end"], item["start"])
            self.assertEqual(len(item["sha256"]), 64)
            int(item["sha256"], 16)
        self.assertEqual(w[-1]["sha256"], self.d["source_code_windows"][0]["sha256"])
        self.assertEqual(self.r["evidence_grade"],
                         "SOURCE_VERIFIED_TW1_CLIENT_STATIC_S_K_STATE_TO_CAPTURE_GATE")

    def test_active_pet_scope_cannot_promote_or_change_historical_current(self):
        r = self.r
        self.assertEqual((r["active_module"], r["scope"]),
                         ("PET", "OFFICIAL_CLASSIC_PC_ONLY"))
        self.assertEqual((r["year"], r["year_status"]), (2026, "NOT_YEAR_AUDITED"))
        self.assertEqual(r["new_official_species_proven"], 0)
        self.assertFalse(r["official_pets_complete"])
        self.assertFalse(r["source_bounded_closed"])
        self.assertFalse(r["historically_complete"])
        self.assertFalse(r["native_runtime_verified"])
        self.assertEqual(r["stage_a"], "7_PARTIAL_2_OPEN")
        self.assertEqual(r["stage_b_wiki"], "GATED")
        self.assertEqual(r["r79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(r["overall_completion_percent"])
        data = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(data), 2709173)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()
        self.assertEqual(blob, r["historical_current_git_blob"])
        self.assertEqual(blob, "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
