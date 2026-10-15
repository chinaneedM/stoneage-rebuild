"""Invented graph controls exercise shape guards; no fake row is source evidence."""
import copy
import json
import unittest

from tools.stoneage_tw10_savedata_r67_tail_static import BASE, TAIL, neighborhood, priors, inspect_verified
from tools.stoneage_tw10_savedata_r67_guard import PINS, NEGATIVE, validate


def fixture():
    old = priors()
    native45 = next(c for c in old["r45"]["native_api_contexts"] if c["site_rva"] == 0x4C68C)
    nodes = native45["bounded_node_rvas"]
    edges = set(zip(nodes, nodes[1:]))
    edges.update((nodes[i], nodes[i+2]) for i in range(18))
    assert len(edges) == 156
    native44 = next(c for c in old["r44"]["native_contexts"] if c["native_root_candidate_rva"] == 0x4C5B4)
    known = {r["site_rva"]: r for s in old["r63"]["sites"] for r in s["decoded_instruction_rows"]}
    known.update({r["site_rva"]: r for r in native44["literal_esp_adjustment_or_unknown_shapes"]})
    def row(at):
        return copy.deepcopy(known.get(at, {"site_rva": at, "mnemonic": "nop", "operands": [],
                                           "decoder_read_registers": [], "decoder_written_registers": [],
                                           "input_query_registers": [], "actual_instruction_effect_or_value_known": False}))
    return {
        "schema": "tw10-r67-original-static-native-tail-operand-neighborhood",
        "runtime_sha256": old["r63"]["runtime_sha256"], "image_base": 4194304,
        "source_git_blobs": {k: v[1] for k, v in PINS.items()},
        "r63_exact_original_rederived_sha256": "91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd",
        "candidate_root_rva": 312756, "bounded_graph_node_rvas": nodes,
        "bounded_graph_edges": [list(e) for e in sorted(edges)],
        "bounded_graph_frontier": [], "bounded_graph_node_cap_hit": False,
        "originally_missing_operand_sites_rva": list(TAIL[:-2]), "requalified_epilogue_sites_rva": list(TAIL[-2:]),
        **neighborhood(nodes, edges, row), **{k: False for k in NEGATIVE},
    }


class R67Tests(unittest.TestCase):
    def test_fixture_has_only_structural_status(self):
        self.assertEqual(validate(fixture())["status"], "STRUCTURAL_DERIVED_METADATA_ONLY")

    def reject(self, f):
        d = fixture()
        f(d)
        with self.assertRaises(ValueError):
            validate(d)

    def test_all_native_promotion_flags_rejected(self):
        for k in NEGATIVE:
            with self.subTest(flag=k):
                self.reject(lambda d: d.__setitem__(k, True))

    def test_node_inventory_missing(self):
        self.reject(lambda d: d["bounded_graph_node_rvas"].pop())

    def test_duplicate_edges(self):
        self.reject(lambda d: d["bounded_graph_edges"].__setitem__(0, d["bounded_graph_edges"][1]))

    def test_wrong_runtime(self):
        self.reject(lambda d: d.__setitem__("runtime_sha256", "0"*64))

    def test_wrong_base(self):
        self.reject(lambda d: d.__setitem__("image_base", 0))

    def test_missing_operand_row(self):
        self.reject(lambda d: d["decoded_instruction_rows"].pop())

    def test_false_new_epilogue_discovery(self):
        self.reject(lambda d: d["originally_missing_operand_sites_rva"].append(0x4C760))

    def test_missing_predecessor(self):
        self.reject(lambda d: d["tail_predecessors"].__setitem__(str(TAIL[0]), []))

    def test_forged_successor(self):
        self.reject(lambda d: d["tail_successors"].__setitem__(str(TAIL[-1]), [TAIL[0]]))

    def test_wrong_prior_epilogue(self):
        def mutate(d):
            next(r for r in d["decoded_instruction_rows"] if r["site_rva"] == 0x4C760)["mnemonic"] = "nop"
        self.reject(mutate)

    def test_nested_raw_code(self):
        self.reject(lambda d: d["decoded_instruction_rows"][0]["operands"].append({"original_payload": "invented"}))

    def test_wrong_neighbor_row_selection(self):
        self.reject(lambda d: d["selected_node_rvas"].append(0x50000))

    def test_row_effect_promotion(self):
        self.reject(lambda d: d["decoded_instruction_rows"][0].__setitem__("actual_instruction_effect_or_value_known", True))

    def test_source_hash_checked_before_decoder_import(self):
        with self.assertRaisesRegex(ValueError, "original runtime SHA256"):
            inspect_verified(b"invented-not-a-client")

    def test_neighborhood_requires_all_tail_sites(self):
        with self.assertRaises(ValueError):
            neighborhood(set(TAIL[:-1]), set(), lambda _: {})

    def test_neighborhood_rejects_outside_edge(self):
        with self.assertRaises(ValueError):
            neighborhood(set(TAIL), {(TAIL[0], 0)}, lambda _: {})


if __name__ == "__main__":
    unittest.main()
