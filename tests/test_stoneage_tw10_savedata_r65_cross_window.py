"""Adversarial metadata controls; mutated inputs never become historical evidence."""
import copy
import json
import unittest

from tools.stoneage_tw10_savedata_r65_cross_window import BASE, SOURCES, derive, inspect_raw
from tools.stoneage_tw10_savedata_r65_independent_guard import NEGATIVE, validate


class R65Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raws = {k: (BASE / v[0]).read_bytes() for k, v in SOURCES.items()}
        cls.original = {k: json.loads(v) for k, v in cls.raws.items()}

    def test_archived_source_replay_and_separate_acceptance(self):
        d = inspect_raw(self.raws)
        self.assertEqual(validate(d, self.raws)["guard"], "PASS_STATIC_METADATA_ONLY")
        self.assertFalse(d["branches"][0]["taken_edge_retained_in_one_r63_window"])
        self.assertEqual(d["branches"][0]["target_window_indices"], [1])

    def test_each_immutable_source_rejects_whitespace_change(self):
        for key in SOURCES:
            with self.subTest(source=key):
                raws = dict(self.raws)
                raws[key] += b"\n"
                with self.assertRaises(ValueError):
                    inspect_raw(raws)
                with self.assertRaises(ValueError):
                    validate(inspect_raw(self.raws), raws)

    def test_independent_guard_rejects_every_promotion(self):
        for key in NEGATIVE:
            with self.subTest(flag=key):
                d = inspect_raw(self.raws)
                d[key] = True
                with self.assertRaises(ValueError):
                    validate(d, self.raws)

    def test_report_mutations_rejected(self):
        changes = [
            lambda d: d.__setitem__("image_base", 0),
            lambda d: d.__setitem__("runtime_sha256", "0" * 64),
            lambda d: d["branches"][0].__setitem__("normalized_taken_target_rva", 0x44C6D9),
            lambda d: d["branches"][0].__setitem__("taken_edge_retained_in_one_r63_window", True),
            lambda d: d["branches"][0].__setitem__("actual_branch_taken", True),
            lambda d: d["branches"][1].__setitem__("target_window_indices", [0]),
            lambda d: d["branches"][0].__setitem__("retained_local_predecessors", []),
            lambda d: d["branches"][0].__setitem__("taken_target_indirect_slot_rva", 0x520A4),
            lambda d: d["operand_derived_rejoins"][0].__setitem__("operand_derived_edge_only", False),
            lambda d: d["conditional_count_pointer_prefixes"][0].__setitem__("same_runtime_memory_address_proven", True),
            lambda d: d["conditional_count_pointer_prefixes"][1].__setitem__("memory_output_count_or_pointer_contents_known", True),
            lambda d: d["conditional_count_pointer_prefixes"][1].__setitem__("conditional_pre_call_esp_offset", 8),
            lambda d: d["conditional_count_pointer_prefixes"][0].__setitem__("lea_to_push_retained_path", [312953, 312958]),
            lambda d: d["conditional_count_pointer_prefixes"][0].__setitem__("barriers", []),
            lambda d: d.__setitem__("union_instruction_rows", 139),
            lambda d: d["source_git_blobs"].__setitem__("r41", "0" * 40),
        ]
        for n, mutate in enumerate(changes):
            with self.subTest(mutation=n):
                d = inspect_raw(self.raws)
                mutate(d)
                with self.assertRaises(ValueError):
                    validate(d, self.raws)

    def test_unpinned_semantic_source_mutations_rejected(self):
        # Bypass cryptographic custody deliberately to exercise semantic guards.
        def row(d, at):
            return next(x for s in d["r63"]["sites"] for x in s["decoded_instruction_rows"] if x["site_rva"] == at)
        changes = [
            lambda d: d["r41"].__setitem__("image_base", 0x500000),
            lambda d: d["r41"].__setitem__("native_io_executed", True),
            lambda d: d["r41"].__setitem__("runtime_sha256", "0" * 64),
            lambda d: row(d, 0x4C694)["operands"][0].__setitem__("constant", 0x4C6D9),
            lambda d: row(d, 0x4C6D9)["operands"][0]["geometry"]["displacement_region"].__setitem__("displacement_rva", 0x520A4),
            lambda d: row(d, 0x4C6E4)["operands"][1]["geometry"].__setitem__("relative_field_offset", -8),
            lambda d: row(d, 0x4C6FB)["operands"][1]["geometry"].__setitem__("base_register", "esp"),
            lambda d: row(d, 0x4C6E7).__setitem__("decoder_written_registers", ["esp", "ecx"]),
            lambda d: d["r63"]["sites"][0]["bounded_local_edges"].append([0x4C67F, 0x4C694]),
            lambda d: row(d, 0x4C6E2)["operands"][0].__setitem__("constant", 0x44C6AD),
        ]
        for n, mutate in enumerate(changes):
            with self.subTest(mutation=n):
                d = copy.deepcopy(self.original)
                mutate(d)
                with self.assertRaises(ValueError):
                    derive(*(d[k] for k in ("r28", "r41", "r63", "r64")))

    def test_missing_source_inventory(self):
        raws = dict(self.raws)
        del raws["r41"]
        with self.assertRaises(ValueError):
            inspect_raw(raws)


if __name__ == "__main__":
    unittest.main()
