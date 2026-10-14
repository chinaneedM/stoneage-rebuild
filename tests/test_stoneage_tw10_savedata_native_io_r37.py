"""Invented helper/store geometry, never original bytes or runtime values."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r37 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import validate
from tools.stoneage_tw10_savedata_native_io_r36 import derive as derive_r36
from tests import test_stoneage_tw10_savedata_native_io_r36 as r36

@lru_cache(maxsize=1)
def base_fixture():
    captured = {}
    def capture(dec, sections, imports, previous):
        raw = bytearray(dec.raw)
        raw.extend(b"\x90" * max(0, 0x4ee00 - dec.lo - len(raw)))
        def put(at, blob):
            raw[at-dec.lo:at-dec.lo+len(blob)] = blob
        def near(at, target):
            return b"\xe8" + struct.pack("<i", target-at-5)
        put(CONTINUATION, b"\xe9" + struct.pack("<i", 0x4ed48-CONTINUATION-5))
        put(0x4ed48, b"\x56")
        put(HELPERS[0][0], near(*HELPERS[0]))
        put(PARTIAL_SITES[0], bytes.fromhex("0c02"))  # OR AL,2
        put(PARTIAL_SITES[1], bytes.fromhex("8a4d0b"))  # MOV CL,[EBP+11]
        put(PARTIAL_SITES[2], bytes.fromhex("6689fe"))  # MOV SI,DI
        put(STORE_SITES[0], bytes.fromhex("88450b"))
        put(STORE_SITES[1], bytes.fromhex("88443104"))
        put(0x4ed86, b"\x50")
        put(HELPERS[1][0], near(*HELPERS[1]))
        put(STORE_SITES[2], bytes.fromhex("8945f0c3"))
        put(HELPERS[0][1], bytes.fromhex("8b4c2404884104c3"))
        put(HELPERS[1][1], bytes.fromhex("8b442404a3") + struct.pack("<I", dec.base+SHARED) + b"\xc3")
        dec = Decoder(bytes(raw), dec.lo, dec.base)
        previous = derive_r36(dec, sections, imports, previous)
        captured["result"] = derive(dec, sections, imports, previous)
        return previous
    with patch.object(r36, "derive", capture):
        r36.fixture()
    return captured["result"]

def fixture():
    return copy.deepcopy(base_fixture())

class R37Synthetic(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(fixture()))
    def test_original_hash_failure(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"bad", b"bad")
    def test_partial_masks_and_widths(self):
        rows = fixture()["partial_definition_shapes"]
        self.assertEqual([r["conditional_partial_model"]["preserved_parent_bits_mask"] for r in rows],
                         [0xffffff00, 0xffffff00, 0xffff0000])
        self.assertEqual([r["conditional_partial_model"]["slice_operation"] for r in rows], ["or", "mov", "mov"])
    def test_partial_never_evaluated(self):
        for r in fixture()["partial_definition_shapes"]:
            self.assertIsNone(r["conditional_partial_model"]["evaluated_original_value_or_result"])
    def test_high_byte_geometry(self):
        row = fixture()["partial_definition_shapes"][0]
        row["operands"][0]["register"] = "ah"
        model = partial_model(row)
        self.assertEqual(model["slice_lsb_bit"], 8)
        self.assertEqual(model["preserved_parent_bits_mask"], 0xffff00ff)
    def test_wrong_subregister_width_is_unqualified(self):
        row = fixture()["partial_definition_shapes"][0]
        row["operands"][0]["width_bytes"] = 2
        self.assertFalse(partial_model(row)["qualified_partial_write_syntax"])
    def test_unsupported_opcode_is_unqualified(self):
        row = fixture()["partial_definition_shapes"][0]
        row["mnemonic"] = "shld"
        self.assertFalse(partial_model(row)["qualified_partial_write_syntax"])
    def test_full_width_shift_distinct_from_partial(self):
        row = fixture()["partial_definition_shapes"][0]
        row["mnemonic"] = "sar"
        row["operands"][0].update(register="ecx", width_bytes=4)
        row["operands"][1].update(constant=5)
        model = full_width_model(row)
        self.assertFalse(partial_model(row)["qualified_partial_write_syntax"])
        self.assertEqual(model["operation"], "sar")
        self.assertTrue(model["sar_uses_signed_reinterpretation"])
        self.assertEqual(model["rhs"], {"kind":"shift_count", "constant":5})
        self.assertIsNone(model["evaluated_original_result"])
    def test_full_width_left_shift(self):
        row = fixture()["partial_definition_shapes"][0]
        row["mnemonic"] = "shl"
        row["operands"][0].update(register="esi", width_bytes=4)
        row["operands"][1].update(constant=3)
        self.assertEqual(full_width_model(row)["operation"], "shl")
    def test_byte_is_not_full_width_scalar(self):
        row = fixture()["partial_definition_shapes"][0]
        self.assertEqual(full_width_model(row)["kind"], "unqualified_scalar")
    def test_direct_call_supported_helpers(self):
        hs = fixture()["helper_candidates"]
        self.assertEqual([h["caller_call_identity"]["direct_target_rva"] for h in hs], [r for _, r in HELPERS])
        self.assertTrue(all(h["supported_by_exact_r36_original_call"] for h in hs))
    def test_helper_stack_spelling_not_parameter(self):
        hs = fixture()["helper_candidates"]
        refs = [r for h in hs for r in h["callee_context"]["memory_references"]
                if r["stack_or_frame_spelling_candidate"]]
        self.assertEqual(len(refs), 2)
        self.assertTrue(all(not r["actual_effective_address_value_owner_or_parameter_proven"] for r in refs))
    def test_shared_address_not_owner(self):
        refs = fixture()["helper_candidates"][1]["callee_context"]["memory_references"]
        self.assertEqual(sum(r["shared_displacement_reference_candidate"] for r in refs), 1)
    def test_push_is_physical_suffix(self):
        hs = fixture()["helper_candidates"]
        self.assertEqual(hs[0]["push_candidates"][0]["input"]["register"], "esi")
        self.assertFalse(hs[0]["actual_caller_callee_stack_or_value_binding_proven"])
    def test_boundary_candidates_not_entry(self):
        bs = fixture()["helper_boundary_candidates"]["roots"]
        self.assertTrue(all(b["linear_boundary_candidate"] for b in bs))
        self.assertFalse(any(b["true_function_entry_or_executed_alignment_proven"] for b in bs))

class R37Tamper(unittest.TestCase):
    def reject(self, mutator):
        d = fixture()
        mutator(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_promotions(self):
        for f in FLAGS:
            with self.subTest(flag=f):
                self.reject(lambda d,f=f:d.update({f:True}))
    def test_digest(self):
        self.reject(lambda d:d.update(r36_exact_report_sha256="bad"))
    def test_partial_mask(self):
        self.reject(lambda d:d["partial_definition_shapes"][0]["conditional_partial_model"].update(preserved_parent_bits_mask=0))
    def test_partial_value(self):
        self.reject(lambda d:d["partial_definition_shapes"][0]["conditional_partial_model"].update(evaluated_original_value_or_result=1))
    def test_scalar_value(self):
        self.reject(lambda d:d["partial_definition_shapes"][0]["conditional_full_width_model"].update(evaluated_original_result=1))
    def test_missing_definition_source(self):
        self.reject(lambda d:d["partial_definition_shapes"][0].update(input_query_registers=[]))
    def test_wrong_helper_target(self):
        self.reject(lambda d:d["helper_candidates"][0]["caller_call_identity"].update(direct_target_rva=1))
    def test_actual_binding(self):
        self.reject(lambda d:d["helper_candidates"][0].update(actual_caller_callee_stack_or_value_binding_proven=True))
    def test_stack_suffix_abi(self):
        self.reject(lambda d:d["helper_candidates"][0]["pre_call_suffix"].update(abi_roles_applied=True))
    def test_push_slot(self):
        self.reject(lambda d:d["helper_candidates"][0]["push_candidates"][0].update(conditional_pre_call_esp_offset=4))
    def test_memory_owner(self):
        self.reject(lambda d:d["helper_candidates"][0]["callee_context"]["memory_references"][0].update(actual_effective_address_value_owner_or_parameter_proven=True))
    def test_false_shared_match(self):
        self.reject(lambda d:d["helper_candidates"][0]["callee_context"]["memory_references"][0].update(shared_displacement_reference_candidate=True))
    def test_reference_cap(self):
        self.reject(lambda d:d["helper_candidates"][0]["callee_context"].update(memory_reference_count=49))
    def test_entry_promotion(self):
        self.reject(lambda d:d["helper_boundary_candidates"]["roots"][0].update(true_function_entry_or_executed_alignment_proven=True))
    def test_runtime_cfg(self):
        self.reject(lambda d:d["helper_boundary_candidates"].update(complete_runtime_alignment_or_cfg_proven=True))
    def test_payload(self):
        self.reject(lambda d:d.update(raw_bytes="forbidden"))

if __name__ == "__main__":
    unittest.main()
