"""Pure invented operand controls; real source custody is a separate gate."""
import copy
import unittest

from tools.stoneage_tw10_savedata_r69_early_static import selection, priors, inspect_verified
from tools.stoneage_tw10_savedata_r69_guard import validate, NEGATIVE, PINS


def fixture():
    old = priors()
    r67 = old["r67"]
    known = {r["site_rva"]: r for s in old["r63"]["sites"] for r in s["decoded_instruction_rows"]}
    known.update({r["site_rva"]: r for r in r67["decoded_instruction_rows"]})
    def row(at):
        return copy.deepcopy(known.get(at, {"site_rva": at, "mnemonic": "nop", "operands": [],
                                           "decoder_read_registers": [], "decoder_written_registers": [],
                                           "input_query_registers": [], "actual_instruction_effect_or_value_known": False}))
    return {
        "schema": "tw10-r69-original-static-early-return-prefix-and-late-predicate",
        "runtime_sha256": r67["runtime_sha256"], "image_base": 4194304,
        "source_git_blobs": {k: v[1] for k, v in PINS.items()},
        "r67_exact_original_rederived_sha256": "8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50",
        "root_rva": 312756, "previously_undecoded_target_rva": 312830,
        "bounded_graph_node_rvas": r67["bounded_graph_node_rvas"], "bounded_graph_edges": r67["bounded_graph_edges"],
        "bounded_graph_frontier": [], "bounded_graph_node_cap_hit": False,
        **selection(r67["bounded_graph_node_rvas"], [tuple(e) for e in r67["bounded_graph_edges"]], row),
        **{k: False for k in NEGATIVE},
    }


class R69Tests(unittest.TestCase):
    def reject(self, mutate):
        d = fixture()
        mutate(d)
        with self.assertRaises(ValueError):
            validate(d)

    def test_synthetic_shape_does_not_assert_original_values(self):
        self.assertEqual(validate(fixture())["status"], "STRUCTURAL_DERIVED_METADATA_ONLY")

    def test_all_false_fields_enforced(self):
        for k in NEGATIVE:
            with self.subTest(flag=k):
                self.reject(lambda d: d.__setitem__(k, True))

    def test_missing_late_predecessor(self):
        self.reject(lambda d: d.__setitem__("target_direct_predecessors", [312828]))

    def test_missing_prefix_row(self):
        self.reject(lambda d: d["decoded_instruction_rows"].pop(0))

    def test_missing_late_predicate_row(self):
        self.reject(lambda d: d["focus_node_rvas"].remove(313131))

    def test_changed_graph_topology(self):
        self.reject(lambda d: d["bounded_graph_edges"].pop())

    def test_changed_old_overlap(self):
        def mutate(d):
            next(r for r in d["decoded_instruction_rows"] if r["site_rva"] == 0x4C600)["mnemonic"] = "nop"
        self.reject(mutate)

    def test_wrong_original_image_base(self):
        self.reject(lambda d: d.__setitem__("image_base", 0))

    def test_nested_raw_payload(self):
        self.reject(lambda d: d["decoded_instruction_rows"][0]["operands"].append({"original_payload": "invented"}))

    def test_actual_effect_promotion(self):
        self.reject(lambda d: d["decoded_instruction_rows"][0].__setitem__("actual_instruction_effect_or_value_known", True))

    def test_wrong_source_custody(self):
        self.reject(lambda d: d["source_git_blobs"].__setitem__("r67", "0"*40))

    def test_missing_complete_incidence(self):
        self.reject(lambda d: d["focus_predecessors"].__setitem__("312830", []))

    def test_runtime_hash_rejected_before_decoder_import(self):
        with self.assertRaisesRegex(ValueError, "original runtime SHA256"):
            inspect_verified(b'invented-source')


if __name__ == "__main__":
    unittest.main()
