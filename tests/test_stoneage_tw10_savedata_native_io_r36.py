"""Invented graph with a fake API and synthetic stores; no original byte payload."""
import unittest
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r36 import *
from tools.stoneage_tw10_savedata_native_io_r36_guard import validate
from tests import test_stoneage_tw10_savedata_native_io_r35 as r35

# Keep the inherited synthetic fixture construction, with no duplicate original
# layout or API assumptions. Save the real function before patching its binding.
def fixture():
    captured = {}
    real_derive = r35.derive
    def capture(dec, sections, imports, prior):
        raw = bytearray(dec.raw)
        raw[CONTINUATION-dec.lo:CONTINUATION-dec.lo+3] = b"\x89\x33\xc3"
        dec = Decoder(bytes(raw), dec.lo, dec.base)
        previous = real_derive(dec, sections, imports, prior)
        captured["report"] = derive(dec, sections, imports, previous)
        return previous
    with patch.object(r35, "derive", capture):
        r35.fixture()
    return captured["report"]

class R36Synthetic(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(fixture()))
    def test_symbolic_only(self):
        p = fixture()["conditional_predicate"]
        self.assertEqual(p["symbolic_direct_edge_condition"], "u32(EAX_at_TEST) != 0")
        self.assertFalse(p["original_eax_or_zf_evaluated"])
    def test_branch_exits(self):
        rows = fixture()["routes"]
        self.assertFalse(rows[0]["structurally_reachable_in_bounded_graph"])
        self.assertTrue(rows[3]["structurally_reachable_in_bounded_graph"])
        self.assertIn(CLOSE, rows[4]["opaque_call_barrier_rvas"])
    def test_esi_barrier(self):
        q = next(q for q in fixture()["input_sources"]["queries"]
                 if (q["site_rva"], q["register"]) == (0x4ed18, "esi"))
        self.assertEqual(q["reaching_candidates"], [{"origin": "unknown_call", "rva": OPAQUE, "semantic": None}])
    def test_invented_push_spelling_differs(self):
        self.assertFalse(fixture()["push_spelling_comparison"]["same_single_register_operand_shape"])
    def test_continuation_store(self):
        stores = fixture()["continuation_memory_stores"]
        self.assertEqual(stores["count"], 1)
        self.assertEqual(stores["samples"][0]["source_registers"], ["esi"])
        self.assertFalse(stores["samples"][0]["actual_store_value_or_handle_owner_proven"])
    def test_route_cycles_and_absence(self):
        t = {"node_rvas": [1, 2, 3, 4], "edges": [[1,2], [2,3], [3,2], [3,4]]}
        self.assertEqual(route(t, [2,4], 1, 4)["opaque_call_barrier_rvas"], [2])
        self.assertFalse(route(t, [2], 4, 1)["structurally_reachable_in_bounded_graph"])
        self.assertFalse(route(t, [], 9, 9)["structurally_reachable_in_bounded_graph"])
    def test_low_byte_projection_and_address_inputs(self):
        ops = [{"geometry": {"base_register": "ecx", "index_register": "esi"}},
               {"kind": "register", "register": "al", "width_bytes": 1}]
        projections, addresses = store_register_queries(ops)
        self.assertEqual(addresses, ["ecx", "esi"])
        self.assertEqual(projections, [{"operand_register": "al", "query_register": "eax",
                                       "operand_width_bytes": 1, "actual_projected_value_known": False}])
    def test_wrong_hash(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"bad", b"bad")

class R36Tamper(unittest.TestCase):
    def reject(self, change):
        d = fixture()
        change(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):
                self.reject(lambda d, f=flag: d.update({f: True}))
    def test_digest(self):
        self.reject(lambda d:d.update(r35_exact_report_sha256="wrong"))
    def test_predicate(self):
        self.reject(lambda d:d["conditional_predicate"].update(symbolic_direct_edge_condition="success"))
    def test_actual_branch(self):
        self.reject(lambda d:d["conditional_predicate"].update(original_eax_or_zf_evaluated=True))
    def test_edge_absence(self):
        self.reject(lambda d:d["bounded_topology"]["edges"].remove([BRANCH,CONTINUATION]))
    def test_route_truth(self):
        self.reject(lambda d:d["routes"][0].update(structurally_reachable_in_bounded_graph=True))
    def test_route_calls(self):
        self.reject(lambda d:d["routes"][4].update(opaque_call_barrier_rvas=[]))
    def test_route_preservation(self):
        self.reject(lambda d:d["routes"][0].update(actual_feasible_path_or_register_preservation_proven=True))
    def test_push_value_binding(self):
        self.reject(lambda d:d["push_spelling_comparison"].update(actual_value_binding_or_callee_preservation_proven=True))
    def test_push_spelling(self):
        self.reject(lambda d:d["push_spelling_comparison"].update(same_single_register_operand_shape=True))
    def test_store_value(self):
        self.reject(lambda d:d["continuation_memory_stores"]["samples"][0].update(actual_store_value_or_handle_owner_proven=True))
    def test_store_count(self):
        self.reject(lambda d:d["continuation_memory_stores"].update(count=2))
    def test_source_ref(self):
        self.reject(lambda d:d["continuation_memory_stores"]["samples"][0].update(source_registers=[]))
    def test_projection_value(self):
        self.reject(lambda d:d["continuation_memory_stores"]["samples"][0]["source_register_projections"][0].update(actual_projected_value_known=True))
    def test_address_ref(self):
        self.reject(lambda d:d["continuation_memory_stores"]["samples"][0].update(address_registers=[]))
    def test_flag_link(self):
        self.reject(lambda d:d["branch_flag_sources"]["candidates"][0].update(site_rva=OPAQUE))
    def test_opaque_effect(self):
        self.reject(lambda d:d["opaque_calls"][0].update(runtime_target_or_effects_proven=True))
    def test_node_duplicates(self):
        self.reject(lambda d:d["bounded_topology"]["node_rvas"].append(TEST))
    def test_payload(self):
        self.reject(lambda d:d.update(raw_bytes="forbidden"))

if __name__ == "__main__":
    unittest.main()
