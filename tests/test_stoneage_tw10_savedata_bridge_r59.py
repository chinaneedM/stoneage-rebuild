"""Synthetic R59 cross-report adversarial controls; no original media loaded."""
import copy
import unittest
from tools.stoneage_tw10_savedata_bridge_r59 import derive, require

def fixture():
    ident = lambda kind, target=None, name=None, iat=None: {
        "kind": kind, "direct_target_rva": target,
        "import_slot_association_proven": name is not None,
        "runtime_target_or_effects_proven": False,
        "import_identity": None if name is None else {"name": name, "iat_rva": iat}}
    write = {
        "api": "WriteFile", "root_candidate_rva": 0x4c5b4, "caller_rva": 0x48c5e,
        "entry_or_call_execution_proven": False, "caller_identity": ident("direct", 0x4c5b4),
        "graph": {"nodes": 139, "edges": 156, "frontier": [], "node_limit_hit": False,
                  "all_incoming_paths_proven": False},
        "api_sites": [
            {"site_rva": a, "identity": ident("memory_indirect", name="WriteFile", iat=0x520a4),
             "site_in_candidate_graph": True, "actual_external_return_proven": False}
            for a in (0x4c68c, 0x4c6f1)]}
    bridge = lambda root, a, target: {"wrapper_root_rva": root,
                                     "call_site_rva": a, "target_rva": target}
    shared = {
        "root_candidate_rva": 0x4a657, "bounded_graph_complete": True,
        "actual_path_or_callee_effects_proven": False,
        "r57_caller_bridges": [bridge(0x48bbc, 0x48c38, 0x4a657),
                               bridge(0x4856c, 0x48586, 0x4a657)],
        "call_contexts": [{"site_rva": 0x4a683, "identity": ident("direct", 0x4c5b4)}]}
    close = {
        "root_candidate_rva": 0x4a53e, "bounded_graph_complete": True,
        "actual_path_or_callee_effects_proven": False,
        "r57_caller_bridges": [bridge(0x4856c, 0x48596, 0x4a53e)],
        "call_contexts": [
            {"site_rva": 0x4a5a3, "identity": ident("memory_indirect", name="CloseHandle", iat=0x520a8)},
            {"site_rva": 0x4a5ad, "identity": ident("memory_indirect", name="GetLastError", iat=0x5208c)}]}
    r28 = {"schema": "tw10-r28-original-call-supported-native-api-input-candidates",
           "runtime_sha256": "invented", "savedata_sha256": "invented",
           "contexts": [write], "caller_return_effects_admitted": False,
           "native_io_executed": False, "original_bytes_published": False}
    r58 = {"schema": "tw10-r58-original-rooted-shared-close-helper-static-inventory",
           "runtime_sha256": "invented", "savedata_sha256": "invented",
           "contexts": [shared, close], "actual_native_flush_close_or_persistence_proven": False,
           "actual_helper_result_or_error_convention_proven": False,
           "native_code_executed": False, "original_bytes_published": False}
    return r28, r58

class R59CrossReportTests(unittest.TestCase):
    def test_synthetic_witness(self):
        r28, r58 = fixture()
        v = derive(r28, r58)
        self.assertEqual(len(v["writefile_import_sites"]), 2)
        self.assertEqual(len(v["close_path_import_sites"]), 2)
        self.assertFalse(v["actual_savedata_written_bytes_flush_close_or_persistence_proven"])
    def test_wrong_native_subcall_rejected(self):
        a, b = fixture()
        b["contexts"][0]["call_contexts"][0]["identity"]["direct_target_rva"] = 0x4c5b5
        with self.assertRaises(ValueError): derive(a, b)
    def test_wrong_import_identity_rejected(self):
        a, b = fixture()
        b["contexts"][1]["call_contexts"][0]["identity"]["import_identity"]["name"] = "WriteFile"
        with self.assertRaises(ValueError): derive(a, b)
    def test_wrong_iat_rejected(self):
        a, b = fixture()
        a["contexts"][0]["api_sites"][1]["identity"]["import_identity"]["iat_rva"] += 4
        with self.assertRaises(ValueError): derive(a, b)
    def test_unchanged_graph_not_execution(self):
        a, b = fixture()
        a["contexts"][0]["entry_or_call_execution_proven"] = True
        with self.assertRaises(ValueError): derive(a, b)
    def test_refuse_native_success_promotion(self):
        a, b = fixture()
        b["actual_native_flush_close_or_persistence_proven"] = True
        with self.assertRaises(ValueError): derive(a, b)
    def test_refuse_cross_version_source(self):
        a, b = fixture()
        a["savedata_sha256"] = "different"
        with self.assertRaises(ValueError): derive(a, b)
    def test_rootless_r28_rejected(self):
        a, b = fixture()
        a["contexts"][0]["graph"]["frontier"] = [["window_limit", 0x4c800]]
        with self.assertRaises(ValueError): derive(a, b)

if __name__ == "__main__":
    unittest.main()
