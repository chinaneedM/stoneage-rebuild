"""R33 invented original-like x86 fixture and strict refusal tests."""
import struct
import unittest
from tools.stoneage_tw10_savedata_native_io_r33 import *
from tools.stoneage_tw10_savedata_native_io_r33_guard import validate
from tools.stoneage_tw10_savedata_native_io_r31 import (
    caller_surface, helper_surface,
    SCHEMA as R31_SCHEMA, STATUS as R31_STATUS,
    PRIOR_SHA256 as R30_DIGEST, FLAGS as R31_FLAGS,
    PARENT_CALLER, API, HELPER
)
from tools.stoneage_tw10_savedata_native_io_r32 import (
    derive as derive_r32, INTERVENING, PUSH
)
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate as validate_r31
from tools.stoneage_tw10_savedata_native_io_r32_guard import validate as validate_r32

BASE = 0x400000

def fixture():
    lo = PARENT_CALLER
    raw = bytearray(b"\x90" * (CALL + 16 - lo))
    def put(at, code):
        raw[at-lo:at-lo+len(code)] = code
    def call(at, to):
        return b"\xe8" + struct.pack("<i", to-at-5)
    put(PARENT_CALLER, call(PARENT_CALLER, PARENT))
    put(PARENT, b"\xe9" + struct.pack("<i", API-PARENT-5))
    put(API, b"\xff\x15" + struct.pack("<I", BASE+0x520a0))
    put(POST, bytes.fromhex("89c6"))     # invented MOV ESI,EAX
    put(POST+2, bytes.fromhex("85f6"))   # invented TEST ESI,ESI
    put(BRANCHES[0], bytes.fromhex("7412")) # JE 0x4ed1f
    put(0x4ed14, bytes.fromhex("85c0"))  # invented TEST EAX,EAX
    put(BRANCHES[1], bytes.fromhex("751b")) # JNE 0x4ed33
    put(SECONDARY, b"\xff\x15" + struct.pack("<I", BASE+0x52084))
    put(INTERVENING, b"\xff\x15" + struct.pack("<I", BASE+0x5208c))
    put(PUSH, bytes.fromhex("50"))
    put(CALL, call(CALL, HELPER))
    put(CALL+5, bytes.fromhex("c3"))
    put(HELPER, bytes.fromhex("8b4c2404890d") + struct.pack("<I", BASE+0x172120c) + b"\xc3")
    dec = Decoder(bytes(raw), lo, BASE)
    sections = [
        dict(name=".rdata", rva=0x52000, vsize=4096,
             raw_size=4096, raw=0, characteristics=0x40000040),
        dict(name=".data", rva=0x1720000, vsize=65536,
             raw_size=0, raw=0, characteristics=0xc0000040)
    ]
    imports = {
        BASE+0x520a0: ("KERNEL32.dll", "CreateFileA"),
        BASE+0x52084: ("KERNEL32.dll", "CloseHandle"),
        BASE+0x5208c: ("KERNEL32.dll", "GetLastError")
    }
    r31 = dict(
        schema=R31_SCHEMA, status=R31_STATUS,
        runtime_sha256=RUNTIME_SHA256, savedata_sha256=SAVEDATA_SHA256,
        r30_exact_original_revalidated=True, r30_exact_report_sha256=R30_DIGEST,
        static_only=True, caller_capture=caller_surface(dec, sections, imports),
        helper_memory=helper_surface(dec, sections),
        **{k: False for k in R31_FLAGS}
    )
    validate_r31(r31)
    r32 = derive_r32(dec, sections, imports, r31)
    validate_r32(r32)
    return derive(dec, sections, imports, r32)

class R33Synthetic(unittest.TestCase):
    def test_good_fixture(self):
        self.assertTrue(validate(fixture()))
    def test_two_branches(self):
        d = fixture()
        self.assertEqual([x["branch_site_rva"] for x in d["branch_flag_contexts"]], list(BRANCHES))
    def test_flag_sources_are_candidate_only(self):
        d = fixture()
        for branch in d["branch_flag_contexts"]:
            self.assertGreaterEqual(branch["source_count"], 1)
            self.assertFalse(branch["actual_predicate_value_or_feasible_path_proven"])
            self.assertTrue(any(s["kind"] == "zf_write" and s["mnemonic"] == "test"
                                for s in branch["source_candidates"]))
    def test_api_name_does_not_mean_execution(self):
        d = fixture()
        self.assertEqual(d["secondary_call_identity"]["import_identity"]["name"], "CloseHandle")
        self.assertFalse(d["secondary_call_identity"]["runtime_target_or_effects_proven"])
    def test_prior_actual_bytes_rejected(self):
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            inspect_verified(b"not historical", b"not historical")

class R33Guard(unittest.TestCase):
    def reject(self, fn):
        d = fixture()
        fn(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_promotions(self):
        for key in FLAGS:
            with self.subTest(key=key):
                self.reject(lambda d, k=key: d.update({k: True}))
    def test_prior_hash(self):
        self.reject(lambda d: d.update(r32_exact_report_sha256="invented"))
    def test_pinned_hash(self):
        self.reject(lambda d: d.update(runtime_sha256="invented"))
    def test_call_effect(self):
        self.reject(lambda d: d["secondary_call_identity"].update(runtime_target_or_effects_proven=True))
    def test_branch_predicate(self):
        self.reject(lambda d: d["branch_flag_contexts"][0].update(actual_predicate_value_or_feasible_path_proven=True))
    def test_source_value(self):
        self.reject(lambda d: d["branch_flag_contexts"][0]["source_candidates"][0].update(candidate_actual_flag_value_known=True))
    def test_source_count(self):
        self.reject(lambda d: d["branch_flag_contexts"][0].update(source_count=999))
    def test_source_input(self):
        self.reject(lambda d: d["flag_operand_input_surface"]["queries"][0].update(actual_register_value_known=True))
    def test_payload(self):
        self.reject(lambda d: d.update(raw_bytes="proprietary"))

if __name__ == "__main__":
    unittest.main()
