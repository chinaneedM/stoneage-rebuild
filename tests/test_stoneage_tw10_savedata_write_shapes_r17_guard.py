"""Independent synthetic tamper controls for strict original-derived R17 metadata."""
import copy
import unittest
from tools.stoneage_tw10_savedata_write_shapes_r17 import (
    SCHEMA, STATUS, WRITES, GAP, NESTED, GLOBAL, FLAGS,
    RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_write_shapes_r17_guard import validate

def specimen():
    return {
        "schema": SCHEMA, "status": STATUS, "runtime_sha256": RUNTIME_SHA256,
        "savedata_sha256": SAVEDATA_SHA256, "conditional_static_only": True,
        "r16_original_identity_revalidated": True,
        "writes": [{
            "site_rva": site, "actual_value_proven": False,
            "executed_write_proven": False, "effective_object_owner_proven": False,
            "write": {"expected_global_rva": GLOBAL,
                      "source_operand": {"kind": "register_input", "register": "eax"}},
            "local_source_frontier": {
                "anchor_is_verified_entry": False, "all_incoming_paths_proven": False,
                "value_known": False, "call_fallthrough_structural_only": True,
                "reaching_candidates": []
            }
        } for site in WRITES],
        "callee_memory_gap": {
            "site_rva": GAP, "r8_unsupported_memory_gap_retained": True,
            "effective_address_and_owner_proven": False, "callee_effect_summary_admitted": False,
            "operand_shapes": [{"kind":"memory", "width_bytes":4}]
        },
        "nested_callees": [{
            "root_rva": root, "caller_arguments_known": False,
            "effective_effects_admitted": False,
            "bounded_effects": {"root_rva": root, "original_helper_accepted": False,
                                "native_io_executed": False}
        } for root in NESTED],
        **{k:False for k in FLAGS},
    }

class TestStrictR17(unittest.TestCase):
    def test_valid_conditional_shape(self):
        self.assertTrue(validate(specimen()))

    def test_global_write_site_tamper_rejected(self):
        x=specimen(); x["writes"][0]["site_rva"]+=1
        with self.assertRaises(ValueError): validate(x)

    def test_effective_value_promotion_rejected(self):
        x=specimen(); x["writes"][0]["actual_value_proven"]=True
        with self.assertRaises(ValueError): validate(x)

    def test_anchor_promotion_rejected(self):
        x=specimen(); x["writes"][0]["local_source_frontier"]["anchor_is_verified_entry"]=True
        with self.assertRaises(ValueError): validate(x)

    def test_nested_effect_admission_rejected(self):
        x=specimen(); x["nested_callees"][0]["effective_effects_admitted"]=True
        with self.assertRaises(ValueError): validate(x)

    def test_native_io_promotion_rejected(self):
        x=specimen(); x["native_io_executed"]=True
        with self.assertRaises(ValueError): validate(x)

    def test_hidden_original_opcode_bytes_rejected(self):
        x=specimen(); x["writes"][1]["write"]["opcode_bytes"]="secret"
        with self.assertRaises(ValueError): validate(x)

    def test_callee_memory_gap_proof_rejected(self):
        x=specimen();x["callee_memory_gap"]["effective_address_and_owner_proven"]=True
        with self.assertRaises(ValueError): validate(x)

    def test_reaching_candidate_cap_enforced(self):
        x=specimen();x["writes"][0]["local_source_frontier"]["reaching_candidates"]=[{}]*25
        with self.assertRaises(ValueError):validate(x)

    def test_original_hash_guard(self):
        x=specimen();x["savedata_sha256"]="0"*64
        with self.assertRaises(ValueError):validate(x)

if __name__ == "__main__":
    unittest.main()
