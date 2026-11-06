"""Source-bound WORLD37-R1 crosswalk regression: never claim binary execution."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD37-CAPTURE-EXIT-DESCENDANT-SOURCE-R1.json"
WORLD36 = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD36-CAPTURE-ROSTER-SOURCE-R1.json"

class World37DescendantSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.world36 = json.loads(WORLD36.read_text(encoding="utf-8"))

    def test_provenance_is_nine_fixed_blob_pins(self):
        r=self.receipt
        self.assertEqual(r["source_scope"], "THREE_PINNED_DESCENDANT_C_SOURCE_FUNCTION_CHAIN_NO_ORIGINAL_MIXED25_EXECUTION")
        self.assertEqual(r["starting_remote"]["original_current_state_bytes"], 2709173)
        self.assertEqual(len(r["fixed_lineages"]), 3)
        self.assertEqual(len({s["lineage"] for s in r["fixed_lineages"]}), 3)
        for source in r["fixed_lineages"]:
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")
            for key in ("capture","battle_exit","char_end"):
                f=source[key]
                self.assertRegex(f["blob"], r"^[0-9a-f]{40}$")
                self.assertTrue(f["path"].endswith(".c"))
                self.assertEqual(len(f["lines"]), 2)
                self.assertLess(f["lines"][0], f["lines"][1])
        self.assertEqual(self.receipt["negative_boundaries"]["conjecture_count"], 0)

    def test_original_world36_is_not_a_wild_exit_replay(self):
        for name, obj in self.world36["cases"].items():
            with self.subTest(name=name):
                self.assertTrue(obj["trace"]["wild_record_unchanged"])
        self.assertFalse(self.world36["battle_removal_or_save_executed"])
        self.assertFalse(self.world36["original_process_started"])

    def test_descendant_success_order_has_separate_count_and_enemy_exit(self):
        ops=self.receipt["ordered_success_only_operations"]
        self.assertEqual(len(ops),len(set(ops)))
        self.assertLess(ops.index("create_pet_and_attach_owner"),ops.index("increment_capturer_get_pet_count"))
        self.assertLess(ops.index("increment_capturer_get_pet_count"),ops.index("exit_captured_wild_from_battle"))
        self.assertLess(ops.index("exit_captured_wild_from_battle"),ops.index("normalize_captured_pet_state"))
        effects=self.receipt["source_qualified_exit_effects"]
        self.assertIn("entry.character_index_is_set_to_minus_one",effects)
        self.assertIn("CHAR_endCharData_sets_record_use_false",effects)

    def test_no_fabricated_original_mixed25_execution(self):
        bounds=self.receipt["negative_boundaries"]
        for key in ("mixed25_original_binary_post_roster_execution_observed",
                    "mixed25_original_binary_capture_counter_field_verified",
                    "mixed25_original_binary_wild_exit_executed",
                    "mixed25_original_binary_condition_item_table_verified",
                    "mixed25_original_binary_compiled_condition_macros_verified",
                    "original_tw10_official_server_behaviour_verified",
                    "historical_save_or_network_delivery_verified"):
            self.assertIs(bounds[key],False)
        self.assertIs(bounds["source_lineage_identity_is_not_deployment_identity"],True)
        self.assertEqual(self.receipt["status"], "WORLD37-R1_DESCENDANT_SOURCE_QUALIFIED_MIXED25_NATIVE_OPEN")

    def test_condition_items_preserve_precheck_consumption_variant(self):
        variants=self.receipt["condition_item_variants"]
        self.assertIn("CAPTURE_FREES_plus_NEED_ITEM_ENEMY_with_getDelNeedItem_nonzero",variants)
        self.assertIn("even_if_capture_later_fails",variants["CAPTURE_FREES_plus_NEED_ITEM_ENEMY_with_getDelNeedItem_nonzero"])
        self.assertIn("do_not_assume_single_copy",variants["CAPTURE_FREES"])
        self.assertIn("not_canonical_TW1",variants["DEL_NOT_25_NEED_ITEM_and_WOLF_TAKE_AXE"])

    def test_failure_cases_do_not_claim_enemy_exit(self):
        cases=self.receipt["control_cases"]
        self.assertEqual({c["name"] for c in cases},
                         {"required_item_absent","probability_rejected_after_item_gate",
                          "capacity_or_pool_failure_after_score_success","successful_capture"})
        for case in cases:
            if case["pet_created"]:
                self.assertTrue(case["count_increment"])
                self.assertTrue(case["wild_exit"])
            else:
                self.assertFalse(case["count_increment"])
                self.assertFalse(case["wild_exit"])

if __name__=="__main__":
    unittest.main()
