"""Independent formulas on invented integers; no original savedata evaluation."""
import copy
import json
import unittest

from tools.stoneage_tw10_savedata_r70_conditional_returns import BASE, PINS, U32, analyze, qualify, execute_shape, reference


class R70Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raws = {k: (BASE / p).read_bytes() for k, (p, _) in PINS.items()}
        ds = {k: json.loads(r) for k, r in cls.raws.items()}
        cls.rows = {r["site_rva"]: r for p in [ds["r67"], *ds["r63"]["sites"], ds["r69"]] for r in p["decoded_instruction_rows"]}
        cls.edges = {tuple(e) for e in ds["r69"]["bounded_graph_edges"]}

    def test_actual_pinned_static_three_definitions_and_invented_models(self):
        d = analyze(self.raws)
        self.assertEqual(d["available_decoded_rows"], 103)
        self.assertEqual([r["site_rva"] for r in d["forward_reverse_direct_return_sources"]], [312830, 313155, 313177])
        self.assertEqual(d["invented_arithmetic_comparisons"], 1011)
        self.assertEqual(d["direct_return_source_unknown_barriers_remaining"], [])
        self.assertFalse(d["complete_full_function_operands_or_inputs_proven"])
        self.assertFalse(d["actual_native_bool_count_or_success_proven"])

    def test_each_raw_source_is_exactly_pinned(self):
        for k in self.raws:
            with self.subTest(source=k):
                d = dict(self.raws);d[k] += b'\n'
                with self.assertRaises(ValueError):
                    analyze(d)

    def test_zero_for_all_invented_input_edges(self):
        for x in [0, 1, 128, 2**31, U32]:
            self.assertEqual(execute_shape(self.rows[0x4C5FE], x, U32), 0)

    def test_all_ones_for_all_invented_input_edges(self):
        for x in [0, 1, 128, 2**31, U32]:
            self.assertEqual(execute_shape(self.rows[0x4C759], x, 0), U32)

    def test_subtraction_wraps_underflow(self):
        self.assertEqual(execute_shape(self.rows[0x4C743], 0, 1), U32)

    def test_subtraction_handles_high_bits(self):
        self.assertEqual(execute_shape(self.rows[0x4C743], 2**31, 1), 2**31-1)
        self.assertEqual(execute_shape(self.rows[0x4C743], 0, U32), 1)

    def test_invalid_invented_uint32_values_rejected(self):
        for x in [-1, 2**32, True, 1.5]:
            with self.subTest(value=x), self.assertRaises(ValueError):
                execute_shape(self.rows[0x4C743], x, 0)

    def reject(self, mutate):
        rows = copy.deepcopy(self.rows);edges = set(self.edges);mutate(rows, edges)
        with self.assertRaises(ValueError):
            qualify(rows, edges)

    def test_partial_xor_not_full_zero(self):
        self.reject(lambda r, e: r[0x4C5FE]["operands"][0].__setitem__("register", "ax"))

    def test_wrong_subtraction_frame_offset(self):
        self.reject(lambda r, e: r[0x4C743]["operands"][1]["geometry"].__setitem__("relative_field_offset", -8))

    def test_wrong_all_ones_literal(self):
        self.reject(lambda r, e: r[0x4C759]["operands"][1].__setitem__("constant", 255))

    def test_late_byte_marker_not_guessed(self):
        self.reject(lambda r, e: r[0x4C728]["operands"][1].__setitem__("constant", 0))

    def test_store_may_not_clobber_predicate_flags(self):
        self.reject(lambda r, e: r[0x4C5F9].__setitem__("decoder_written_registers", ["eflags"]))

    def test_both_early_entrances_required(self):
        self.reject(lambda r, e: e.remove((0x4C72B, 0x4C5FE)))

    def test_wrong_early_branch_condition(self):
        self.reject(lambda r, e: r[0x4C5FC].__setitem__("mnemonic", "je"))

    def test_missing_early_flag_definition(self):
        self.reject(lambda r, e: r[0x4C5F3].__setitem__("decoder_written_registers", []))

    def test_reference_rejects_unknown_profile(self):
        with self.assertRaises(ValueError):
            reference("success", 0, 0)


if __name__ == '__main__':
    unittest.main()
