"""Invented x86 layout for R35: no original bytes or observed API semantics."""
import struct
import unittest

from tools.stoneage_tw10_savedata_native_io_r35 import *
from tools.stoneage_tw10_savedata_native_io_r35_guard import validate
from tools.stoneage_tw10_savedata_native_io_r31 import (
    caller_surface, helper_surface, SCHEMA as R31_SCHEMA, STATUS as R31_STATUS,
    PRIOR_SHA256 as R30_SHA, FLAGS as R31_FLAGS, PARENT_CALLER, API, HELPER,
)
from tools.stoneage_tw10_savedata_native_io_r32 import derive as derive_r32, INTERVENING
from tools.stoneage_tw10_savedata_native_io_r33 import derive as derive_r33
from tools.stoneage_tw10_savedata_native_io_r34 import derive as derive_r34, CMP
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate as validate_r31
from tools.stoneage_tw10_savedata_native_io_r32_guard import validate as validate_r32
from tools.stoneage_tw10_savedata_native_io_r33_guard import validate as validate_r33
from tools.stoneage_tw10_savedata_native_io_r34_guard import validate as validate_r34

BASE = 0x400000
SYNTHETIC_IAT = 0x52094

def fixture():
    lo = PARENT_CALLER
    raw = bytearray(b"\x90" * (0x4ed40 - lo))
    def put(at, blob):
        raw[at-lo:at-lo+len(blob)] = blob
    def near(at, target):
        return b"\xe8" + struct.pack("<i", target-at-5)
    put(PARENT_CALLER, near(PARENT_CALLER, PARENT))
    put(PARENT, b"\xe9" + struct.pack("<i", API-PARENT-5))
    put(API, b"\xff\x15" + struct.pack("<I", BASE+0x520a0))
    put(0x4ed07, bytes.fromhex("89c6"))
    put(CMP, bytes.fromhex("39fe"))
    put(0x4ed0b, bytes.fromhex("7412"))
    put(0x4ed0d, b"\x50") # invented PUSH EAX
    put(OPAQUE, b"\xff\x15" + struct.pack("<I", BASE+SYNTHETIC_IAT))
    put(TEST, bytes.fromhex("85c0"))
    put(0x4ed16, bytes.fromhex("751b"))
    put(0x4ed18, b"\x56")
    put(CLOSE, b"\xff\x15" + struct.pack("<I", BASE+0x520a8))
    put(INTERVENING, b"\xff\x15" + struct.pack("<I", BASE+0x5208c))
    put(0x4ed25, b"\x50")
    put(0x4ed26, near(0x4ed26, HELPER))
    put(0x4ed2b, b"\xc3")
    put(HELPER, bytes.fromhex("8b4c2404890d") + struct.pack("<I",BASE+0x172120c) + b"\xc3")
    dec = Decoder(bytes(raw), lo, BASE)
    sections = [
        dict(name=".rdata", rva=0x52000,vsize=4096,raw_size=4096,raw=0,
             characteristics=0x40000040),
        dict(name=".data",rva=0x1720000,vsize=65536,raw_size=0,raw=0,
             characteristics=0xc0000040),
    ]
    imports = {
        BASE+0x520a0: ("KERNEL32.dll", "CreateFileA"),
        BASE+0x520a8: ("KERNEL32.dll", "CloseHandle"),
        BASE+0x5208c: ("KERNEL32.dll", "GetLastError"),
        BASE+SYNTHETIC_IAT: ("SYNTHETIC.dll", "InventedCall"),
    }
    p31 = dict(
        schema=R31_SCHEMA, status=R31_STATUS,
        runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
        r30_exact_original_revalidated=True, r30_exact_report_sha256=R30_SHA,
        static_only=True, caller_capture=caller_surface(dec,sections,imports),
        helper_memory=helper_surface(dec,sections),
        **{k: False for k in R31_FLAGS},
    )
    validate_r31(p31)
    p32 = derive_r32(dec,sections,imports,p31);validate_r32(p32)
    p33 = derive_r33(dec,sections,imports,p32);validate_r33(p33)
    p34 = derive_r34(dec,sections,imports,p33);validate_r34(p34)
    return derive(dec,sections,imports,p34)

class R35Synthetic(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(fixture()))
    def test_callee_identity_is_only_static(self):
        d = fixture()["opaque_call_identity"]
        self.assertEqual(d["call_rva"], OPAQUE)
        self.assertEqual(d["import_identity"]["name"], "InventedCall")
        self.assertFalse(d["runtime_target_or_effects_proven"])
    def test_conditional_push(self):
        d = fixture()["opaque_call_push_candidates"]
        self.assertEqual(len(d),1)
        self.assertEqual(d[0]["site_rva"],0x4ed0d)
        self.assertEqual(d[0]["conditional_pre_call_esp_offset"],0)
        self.assertFalse(d[0]["actual_argument_role_or_value_proven"])
    def test_wrong_original_hash(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"bad",b"bad")

class R35Guard(unittest.TestCase):
    def reject(self,mutator):
        report = fixture()
        mutator(report)
        with self.assertRaises(ValueError):
            validate(report)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):
                self.reject(lambda d,flag=flag: d.update({flag:True}))
    def test_prior_digest(self):
        self.reject(lambda d:d.update(r34_exact_report_sha256="wrong"))
    def test_abi(self):
        self.reject(lambda d:d["opaque_call_pre_call_suffix"].update(abi_roles_applied=True))
    def test_return_effect(self):
        self.reject(lambda d:d["opaque_call_identity"].update(runtime_target_or_effects_proven=True))
    def test_argument(self):
        self.reject(lambda d:d["opaque_call_push_candidates"][0].update(actual_argument_role_or_value_proven=True))
    def test_input_value(self):
        self.reject(lambda d:d["register_sources_before_and_after_call"]["queries"][0].update(actual_register_value_known=True))
    def test_original_payload(self):
        self.reject(lambda d:d.update(raw_bytes="forbidden"))
    def test_fabricated_iat(self):
        self.reject(lambda d:d["opaque_call_identity"].update(import_slot_association_proven=False))

if __name__ == "__main__":
    unittest.main()
