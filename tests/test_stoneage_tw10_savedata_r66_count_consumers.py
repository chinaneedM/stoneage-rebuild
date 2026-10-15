import copy
import json
import unittest

from tools.stoneage_tw10_savedata_r66_count_consumers import BASE, analyze, collect, consumer_contract


class R66Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((BASE / "STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json").read_bytes())

    def test_exact_retained_scope_and_tail_gaps(self):
        d = analyze(BASE)
        self.assertEqual(d["report_count"], 34)
        self.assertEqual(d["r62_prior_scope_report_count"], 32)
        self.assertEqual(d["missing_tail_decoded_sites"],
                         [313137, 313147, 313153, 313155, 313158, 313160, 313167,
                          313177, 313180, 313181, 313182])
        self.assertEqual([(r["site_rva"], r["mnemonic"]) for r in d["retained_epilogue_decoded_rows"]],
                         [(313183, "leave"), (313184, "ret")])
        self.assertFalse(d["stage_b_started"])
        self.assertFalse(d["actual_native_bool_count_frame_alias_or_persistence_proven"])

    def test_independent_consumer_numeric_paths(self):
        d = consumer_contract(self.source)
        self.assertEqual(d["first_count_read_accumulate_compare_path"], [312982, 312985, 312988, 312990])
        self.assertEqual(d["second_count_read_assign_path"], [313083, 313086, 313089, 313092])
        self.assertEqual(d["common_accumulator_read_compare_path"], [313005, 313008, 313010])
        self.assertTrue(d["second_rejoin_bypasses_zero_edi_instruction"])
        self.assertFalse(d["edi_zero_on_all_rejoins_proven"])
        self.assertFalse(d["actual_output_count_or_return_value_known"])
        self.assertFalse(d["frame_offsets_are_savedata_fields"])

    def test_classifier_does_not_merge_different_objects(self):
        x = {"a": {"site_rva": 0x4C743, "mnemonic": "mov"}, "b": {"operands": []}}
        hits = collect(x)[str(0x4C743)]
        self.assertEqual(len(hits), 1)
        self.assertFalse(hits[0]["decoded_mnemonic_and_operands"])

    def test_classifier_same_object_accepts_ret_without_operands(self):
        x = {"site_rva": 0x4C760, "mnemonic": "ret", "operands": []}
        self.assertTrue(collect(x)[str(0x4C760)][0]["decoded_mnemonic_and_operands"])

    def test_classifier_rejects_numeric_string_and_boolean_as_addresses(self):
        self.assertEqual(collect({"site_rva": "313155", "mnemonic": "mov", "operands": []})["313155"], [])
        self.assertEqual(collect({"site_rva": True, "mnemonic": "ret", "operands": []}, (1,))["1"], [])

    def test_classifier_does_not_treat_empty_mnemonic_as_instruction(self):
        self.assertFalse(collect({"site_rva": 0x4C743, "mnemonic": "", "operands": []})["313155"][0]["decoded_mnemonic_and_operands"])

    def test_classifier_counts_multiple_reports_separately(self):
        x = [{"site_rva": 0x4C743, "mnemonic": "mov", "operands": []}] * 2
        self.assertEqual(len(collect(x)["313155"]), 2)

    def test_classifier_nested_limit(self):
        x = {}
        for _ in range(46):
            x = {"next": x}
        with self.assertRaises(ValueError):
            collect(x)

    def reject(self, mutate):
        d = copy.deepcopy(self.source)
        mutate(d)
        with self.assertRaises(ValueError):
            consumer_contract(d)

    @staticmethod
    def row(d, at):
        return next(r for s in d["sites"] for r in s["decoded_instruction_rows"] if r["site_rva"] == at)

    def test_count_load_wrong_frame(self):
        self.reject(lambda d: self.row(d, 0x4C696)["operands"][1]["geometry"].__setitem__("base_register", "esp"))

    def test_count_accumulate_wrong_width(self):
        self.reject(lambda d: self.row(d, 0x4C699)["operands"][0].__setitem__("width_bytes", 1))

    def test_signed_comparison_is_not_unsigned(self):
        self.reject(lambda d: self.row(d, 0x4C69E).__setitem__("mnemonic", "jb"))

    def test_signed_target_wrong_va(self):
        self.reject(lambda d: self.row(d, 0x4C69E)["operands"][0].__setitem__("constant", 0x4C6AB))

    def test_second_assignment_wrong_slot(self):
        self.reject(lambda d: self.row(d, 0x4C701)["operands"][0]["geometry"].__setitem__("relative_field_offset", -12))

    def test_result_store_wrong_register(self):
        self.reject(lambda d: self.row(d, 0x4C70C)["operands"][1].__setitem__("register", "edi"))

    def test_consumer_path_missing_edge(self):
        self.reject(lambda d: d["sites"][1]["bounded_local_edges"].remove([0x4C6FB, 0x4C6FE]))

    def test_actual_instruction_effect_promotion(self):
        self.reject(lambda d: self.row(d, 0x4C6B0).__setitem__("actual_instruction_effect_or_value_known", True))


if __name__ == "__main__":
    unittest.main()
