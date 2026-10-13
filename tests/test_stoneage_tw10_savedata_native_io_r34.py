"""Invented R34 conditional x86 input fixtures; originals never executed."""
import struct,unittest
from tools.stoneage_tw10_savedata_native_io_r34 import *
from tools.stoneage_tw10_savedata_native_io_r34_guard import validate
from tools.stoneage_tw10_savedata_native_io_r31 import (
    caller_surface, helper_surface, SCHEMA as R31_SCHEMA, STATUS as R31_STATUS,
    PRIOR_SHA256 as R30_SHA, FLAGS as R31_FLAGS, PARENT_CALLER, API, HELPER,
)
from tools.stoneage_tw10_savedata_native_io_r32 import derive as derive_r32,INTERVENING
from tools.stoneage_tw10_savedata_native_io_r33 import derive as derive_r33
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate as validate_r31
from tools.stoneage_tw10_savedata_native_io_r32_guard import validate as validate_r32
from tools.stoneage_tw10_savedata_native_io_r33_guard import validate as validate_r33
BASE=0x400000

def fixture():
    lo=PARENT_CALLER; raw=bytearray(b'\x90'*(0x4ed40-lo))
    def put(at, b):raw[at-lo:at-lo+len(b)]=b
    def near(at,target):return b'\xe8'+struct.pack('<i',target-at-5)
    put(PARENT_CALLER,near(PARENT_CALLER,PARENT))
    put(PARENT,b'\xe9'+struct.pack('<i',API-PARENT-5))
    put(API,b'\xff\x15'+struct.pack('<I',BASE+0x520a0))
    put(0x4ed07,bytes.fromhex('89c6'))
    put(CMP,bytes.fromhex('39fe')) # cmp esi,edi, invented
    put(0x4ed0b,bytes.fromhex('7412'))
    put(0x4ed14,bytes.fromhex('85c0'))
    put(0x4ed16,bytes.fromhex('751b'))
    put(0x4ed18,bytes.fromhex('56')) # push esi
    put(CALL,b'\xff\x15'+struct.pack('<I',BASE+0x520a8))
    put(INTERVENING,b'\xff\x15'+struct.pack('<I',BASE+0x5208c))
    put(0x4ed25,bytes.fromhex('50'))
    put(0x4ed26,near(0x4ed26,HELPER))
    put(0x4ed2b,b'\xc3')
    put(HELPER,bytes.fromhex('8b4c2404890d')+struct.pack('<I',BASE+0x172120c)+b'\xc3')
    dec=Decoder(bytes(raw),lo,BASE)
    secs=[dict(name='.rdata',rva=0x52000,vsize=4096,raw_size=4096,raw=0,characteristics=0x40000040),
          dict(name='.data',rva=0x1720000,vsize=65536,raw_size=0,raw=0,characteristics=0xc0000040)]
    imports={BASE+0x520a0:('KERNEL32.dll','CreateFileA'),
             BASE+0x520a8:('KERNEL32.dll','CloseHandle'),
             BASE+0x5208c:('KERNEL32.dll','GetLastError')}
    r31=dict(schema=R31_SCHEMA,status=R31_STATUS,
             runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
             r30_exact_original_revalidated=True,r30_exact_report_sha256=R30_SHA,static_only=True,
             caller_capture=caller_surface(dec,secs,imports),
             helper_memory=helper_surface(dec,secs),
             **{k:False for k in R31_FLAGS})
    validate_r31(r31)
    r32=derive_r32(dec,secs,imports,r31)
    validate_r32(r32)
    r33=derive_r33(dec,secs,imports,r32)
    validate_r33(r33)
    return derive(dec,secs,imports,r33)

class R34Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_close_push_is_only_geometry(self):
        d=fixture();p=d['closehandle_push_candidates']
        self.assertEqual(len(p),1)
        self.assertEqual(p[0]['site_rva'],0x4ed18)
        self.assertEqual(p[0]['input']['register'],'esi')
        self.assertEqual(p[0]['conditional_pre_call_esp_offset'],0)
        self.assertFalse(p[0]['actual_argument_role_or_value_proven'])
    def test_cmp_test_static(self):
        d=fixture();self.assertEqual([x['mnemonic'] for x in d['predicate_operands']],['cmp','test'])
        self.assertTrue(all(not x['actual_inputs_or_predicate_value_proven'] for x in d['predicate_operands']))
    def test_wrong_original_hash(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'bad',b'bad')

class R34Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d,k=k:d.update({k:True}))
    def test_prior_digest(self):self.reject(lambda d:d.update(r33_exact_report_sha256='wrong'))
    def test_predicate_value(self):self.reject(lambda d:d['predicate_operands'][0].update(actual_inputs_or_predicate_value_proven=True))
    def test_close_alias(self):self.reject(lambda d:d['closehandle_push_candidates'][0].update(actual_argument_role_or_value_proven=True))
    def test_stack_abi(self):self.reject(lambda d:d['closehandle_pre_call_suffix'].update(abi_roles_applied=True))
    def test_original_input_value(self):self.reject(lambda d:d['register_sources']['queries'][0].update(actual_register_value_known=True))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
