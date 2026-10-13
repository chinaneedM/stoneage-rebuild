"""R32 invented x86 input and negative guards; no historical code bytes."""
import struct
import unittest
from tools.stoneage_tw10_savedata_native_io_r32 import *
from tools.stoneage_tw10_savedata_native_io_r32_guard import validate
from tools.stoneage_tw10_savedata_native_io_r31 import (
    caller_surface, helper_surface,
    SCHEMA as R31_SCHEMA, STATUS as R31_STATUS,
    PRIOR_SHA256 as R30_SHA, FLAGS as PRIOR_FLAGS,
    PARENT_CALLER, API
)
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate as validate_r31

BASE = 0x400000

def fixture():
    lo = PARENT_CALLER
    raw = bytearray(b"\x90" * (CALL + 16 - lo))
    def put(at, blob):
        raw[at-lo:at-lo+len(blob)] = blob
    def direct(at, target):
        return b"\xe8" + struct.pack("<i", target-at-5)
    put(PARENT_CALLER, direct(PARENT_CALLER, PARENT))
    put(PARENT, b"\xe9" + struct.pack("<i", API-PARENT-5))
    put(API, b"\xff\x15" + struct.pack("<I", BASE+0x520a0))
    put(POST, bytes.fromhex("89c6"))  # MOV ESI,EAX, not an actual handle.
    put(POST+2, bytes.fromhex("85f6"))  # TEST ESI,ESI.
    at = POST+4
    put(at, bytes.fromhex("0f84") + struct.pack("<i", INTERVENING-at-6))
    put(INTERVENING, direct(INTERVENING, 0x4c9ba))
    put(PUSH, bytes.fromhex("50"))
    put(CALL, direct(CALL, HELPER))
    put(CALL+5, bytes.fromhex("c3"))
    # Synthetic helper reads entry-relative [ESP+4], writes a fake global.
    put(HELPER, bytes.fromhex("8b4c2404890d") + struct.pack("<I", BASE+0x172120c) + b"\xc3")
    dec = Decoder(bytes(raw), lo, BASE)
    sections = [
        dict(name=".rdata", rva=0x52000, vsize=4096,
             raw_size=4096, raw=0, characteristics=0x40000040),
        dict(name=".data", rva=0x1720000, vsize=65536,
             raw_size=0, raw=0, characteristics=0xc0000040),
    ]
    imports = {BASE+0x520a0: ("KERNEL32.dll", "CreateFileA")}
    prior = dict(
        schema=R31_SCHEMA, status=R31_STATUS,
        runtime_sha256=RUNTIME_SHA256, savedata_sha256=SAVEDATA_SHA256,
        r30_exact_original_revalidated=True, r30_exact_report_sha256=R30_SHA,
        static_only=True,
        caller_capture=caller_surface(dec, sections, imports),
        helper_memory=helper_surface(dec, sections),
        **{k: False for k in PRIOR_FLAGS}
    )
    validate_r31(prior)
    return derive(dec, sections, imports, prior)

class R32Synthetic(unittest.TestCase):
    def test_valid_derived_fixture(self):
        self.assertTrue(validate(fixture()))
    def test_intervening_direct_call_is_not_api_return_proof(self):
        d = fixture()
        call = d["intervening_call_identity"]
        self.assertEqual(call["direct_target_rva"], 0x4c9ba)
        self.assertFalse(call["runtime_target_or_effects_proven"])
    def test_conditional_branch_candidate_has_two_paths(self):
        branches = fixture()["branch_candidates"]
        self.assertEqual(branches["count"], 1)
        row = branches["candidates"][0]
        self.assertTrue(row["target_structurally_reaches_helper_call"])
        self.assertTrue(row["fallthrough_structurally_reaches_helper_call"])
        self.assertFalse(row["branch_condition_or_actual_path_proven"])
    def test_stack_slot_is_geometry_only(self):
        slot = fixture()["conditional_slot"]
        self.assertTrue(slot["conditional_hardware_call_slot_candidate"])
        self.assertEqual((slot["caller_pre_call_esp_offset"],
                          slot["callee_entry_esp_relative_offset"]), (0, 4))
        self.assertFalse(slot["api_return_handle_link_proven"])
    def test_opaque_call_kills_push_eax(self):
        d = fixture()
        queries = d["parent_esi_eax_sources"]["queries"]
        q = next(q for q in queries if
                 (q["site_rva"], q["register"]) == (PUSH, "eax"))
        self.assertTrue(any(source["origin"] == "unknown_call" and
                            source["rva"] == INTERVENING
                            for source in q["reaching_candidates"]))
    def test_no_source_execution(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"not original", b"not original")

class R32Guard(unittest.TestCase):
    def reject(self, change):
        d = fixture()
        change(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_all_forbidden_promotions(self):
        for key in FLAGS:
            with self.subTest(key=key):
                self.reject(lambda d, k=key: d.update({k: True}))
    def test_original_prior_digest(self):
        self.reject(lambda d: d.update(r31_exact_report_sha256="invented"))
    def test_source_hash(self):
        self.reject(lambda d: d.update(runtime_sha256="invented"))
    def test_call_effects(self):
        self.reject(lambda d: d["intervening_call_identity"].update(runtime_target_or_effects_proven=True))
    def test_branch_condition(self):
        self.reject(lambda d: d["branch_candidates"]["candidates"][0].update(branch_condition_or_actual_path_proven=True))
    def test_branch_truncation(self):
        self.reject(lambda d: d["branch_candidates"].update(truncated=True))
    def test_historical_stack_binding(self):
        self.reject(lambda d: d["conditional_slot"].update(caller_callee_argument_binding_proven=True))
    def test_claimed_handle(self):
        self.reject(lambda d: d["conditional_slot"].update(api_return_handle_link_proven=True))
    def test_input_values(self):
        self.reject(lambda d: d["parent_esi_eax_sources"]["queries"][0].update(actual_register_value_known=True))
    def test_raw_payload(self):
        self.reject(lambda d: d.update(raw_bytes="must never export"))

if __name__ == "__main__":
    unittest.main()
