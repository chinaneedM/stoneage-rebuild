import struct
import unittest
from tools.stoneage_wayi_pe_resource_directory import inspect, audit_pair


def fixture():
    b = bytearray(1024)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 60, 64)
    b[64:68] = b'PE\0\0'
    struct.pack_into('<HHI', b, 68, 0x14c, 1, 0)
    struct.pack_into('<H', b, 84, 224)
    struct.pack_into('<H', b, 88, 0x10b)
    struct.pack_into('<I', b, 180, 16)
    struct.pack_into('<II', b, 200, 4096, 256)
    b[312:320] = b'.rsrc\0\0\0'
    struct.pack_into('<IIII', b, 320, 512, 4096, 512, 512)
    for off, key, child in [(0, 16, 32), (32, 1, 64)]:
        struct.pack_into('<H', b, 512 + off + 14, 1)
        struct.pack_into('<II', b, 512 + off + 16, key, 0x80000000 | child)
    struct.pack_into('<H', b, 512 + 64 + 14, 1)
    struct.pack_into('<II', b, 512 + 64 + 16, 1028, 96)
    struct.pack_into('<IIII', b, 512 + 96, 4096 + 128, 4, 0, 0)
    b[640:644] = b'TEST'
    return b


class Resources(unittest.TestCase):
    def test_direct_payload_and_no_ui_promotion(self):
        r = inspect(fixture(), False)
        self.assertEqual(r['entries'][0]['path'], [16, 1, 1028])
        self.assertEqual(r['direct_payload_count'], 1)
        self.assertFalse(r['login_screen_recovered'])

    def test_source_identity_gate(self):
        with self.assertRaises(ValueError): inspect(fixture())

    def test_pair_rejects_synthetic_as_actual_source(self):
        with self.assertRaises(ValueError): audit_pair(fixture(), fixture())

    def test_cycle(self):
        b=fixture(); struct.pack_into('<I',b,532,0x80000000)
        with self.assertRaises(ValueError): inspect(b,False)

    def test_directory_escape(self):
        b=fixture(); struct.pack_into('<I',b,532,0x800000ff)
        with self.assertRaises(ValueError): inspect(b,False)

    def test_payload_outside_file(self):
        b=fixture(); struct.pack_into('<I',b,608,0x5000)
        with self.assertRaises(ValueError): inspect(b,False)

    def test_packed_directory_rejected(self):
        b=fixture();b[312:320]=b'UPX1\0\0\0\0'
        with self.assertRaises(ValueError): inspect(b,False)

    def test_packed_payload_has_no_raw_hash(self):
        b=fixture();struct.pack_into('<H',b,70,2)
        b[352:360]=b'UPX1\0\0\0\0'
        struct.pack_into('<IIII',b,360,64,8192,64,896)
        struct.pack_into('<I',b,608,8192)
        r=inspect(b,False)
        self.assertEqual(r['direct_payload_count'],0)
        self.assertIsNone(r['entries'][0]['payload_sha256'])

    def test_reserved_and_zero_length(self):
        for off,val in [(612,0),(620,1)]:
            b=fixture();struct.pack_into('<I',b,off,val)
            with self.assertRaises(ValueError):inspect(b,False)


if __name__=='__main__': unittest.main()
