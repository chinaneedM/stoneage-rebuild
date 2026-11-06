"""WORLD34 original source windows and original field-item row retention.

Replays previously published derived checks without shipping commercial binaries.
A private exact-image pass verified source windows; CI cannot independently
re-execute a proprietary EXE and must not claim that it did.
"""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD34-ORIGINAL-FIELD-PATH-SOURCE-R1.json"
W31 = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json"
W33 = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD33-BATTLE-ITEM-GATE-SOURCE-R1.json"


class OriginalFieldPathSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(R.read_bytes())
        cls.w31 = json.loads(W31.read_bytes())
        cls.w33 = json.loads(W33.read_bytes())

    def test_immutable_pinned_evidence(self):
        p = self.report
        for label, path in (("world31", W31), ("world33", W33)):
            raw = path.read_bytes()
            expected = p["previously_pinned_windows"]["pins_from_source_git_blobs"][label]
            actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(actual, expected)
        self.assertEqual(p["archive"]["sha256"], self.w31["archive_sha256"])
        self.assertEqual(p["archive"]["sha256"], self.w33["archive_sha256"])
        self.assertEqual(len(self.w31["program"]["emulator_source_windows"]), 6)
        self.assertEqual(len(self.w33["program"]["server_windows"]), 12)
        self.assertEqual(len(self.w33["program"]["client_windows"]), 5)
        self.assertTrue(p["previously_pinned_windows"]["all_23_window_sha256_matches"])

    def test_original_itemset_three_real_row_source(self):
        samples = {r["row"]["id"]: r for r in self.w33["source_class_witnesses"]}
        args = {1232: ("體600", 1, 2), 12530: ("體320", 0, 1),
                12555: ("氣20體185", 2, 1)}
        self.assertEqual(len(self.report["original_itemset_rows"]), 3)
        for r in self.report["original_itemset_rows"]:
            with self.subTest(id=r["id"]):
                raw_value, scene, target = args[r["id"]]
                expected = samples[r["id"]]
                self.assertEqual(r["original_recovery_argument"], raw_value)
                self.assertEqual(hashlib.sha256(raw_value.encode("cp950")).hexdigest(),
                                 r["original_argument_raw_cp950_sha256"])
                self.assertEqual((r["fieldtype"], r["target_type"]), (scene, target))
                self.assertEqual(r["item_type"], 20)
                self.assertEqual(r["original_row_sha256"], expected["row"]["row_sha256"])
                self.assertEqual(r["source_line_number"], expected["row"]["line"])
                self.assertEqual(r["client_field_gate_passed"],
                                 expected["client"]["field_use_gate_passed"])

    def test_static_original_forwarding_is_not_a_full_result(self):
        p = self.report
        self.assertEqual([x["start_va"] for x in p["newly_recovered_original_pe_windows"]],
                         [0x413130, 0x4746e0, 0x47489c, 0x4749f2])
        for w in p["newly_recovered_original_pe_windows"]:
            self.assertLess(w["start_va"], w["end_va_exclusive"])
            self.assertEqual(len(w["sha256"]), 64)
        self.assertEqual([x["site"] for x in p["compiled_field_call_sites"]],
                         [0x41324c, 0x4748a8, 0x474a00])
        self.assertEqual(p["compiled_field_call_sites"][-1]["local_ebp_disp"], -0x11c)
        self.assertEqual([x["role"] for x in p["callback_arguments_from_original_instructions"]],
                         ["caster_character_index", "resolved_field_target_character_or_pet_index",
                          "inventory_item_slot"])
        self.assertEqual(p["callback_arguments_from_original_instructions"][-1]["ordinal"], 2)

    def test_extraction_failure_and_unknown_effects_not_hidden(self):
        s = self.report["server_extraction"]
        self.assertEqual(s["actual_libarchive_data_prefix_bytes"], 1835008)
        self.assertFalse(s["whole_member_sha256_verified"])
        self.assertFalse(s["whole_member_crc_verified"])
        self.assertNotEqual(s["actual_libarchive_block_read_sha256"], s["expected_member_sha256"])
        for k, val in self.report["unproven"].items():
            with self.subTest(unproven=k):
                self.assertIs(val, True)
        self.assertFalse(self.report["source_semantics"]["item_attribute_key_4_or_5_read_before_callback_entry_in_prior_field_preflight"])


if __name__ == "__main__":
    unittest.main()
