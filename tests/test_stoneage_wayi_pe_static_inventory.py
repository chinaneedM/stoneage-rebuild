import hashlib
import struct
import unittest
from tools.stoneage_wayi_pe_static_inventory import inventory_pe, version_candidates, MAX_BYTES


def specimen(name=b'.text', content=b'ClientLogin\0CharLogin\0'):
    data = bytearray(512 + len(content))
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 64)
    data[64:68] = b'PE\0\0'
    struct.pack_into('<HHI', data, 68, 0x14c, 1, 1120651511)
    struct.pack_into('<H', data, 84, 224)
    struct.pack_into('<H', data, 88, 0x10b)
    data[312:320] = name.ljust(8, b'\0')
    struct.pack_into('<IIII', data, 320, len(content), 4096, len(content), 512)
    data[512:] = content
    return bytes(data)


def version_block(value='1, 0, 0, 1'):
    key = 'FileVersion\0'.encode('utf-16le')
    raw = (value+'\0').encode('utf-16le')
    body = key + b'\0'*((-(6+len(key))) % 4) + raw
    return struct.pack('<HHH', 6+len(body), len(value)+1, 1) + body


class StaticPEInventoryTests(unittest.TestCase):
    def test_response_hash_and_mutable_date_do_not_authenticate_release(self):
        data = specimen(); result = inventory_pe(data)
        self.assertEqual(result['response_sha256'], hashlib.sha256(data).hexdigest())
        self.assertEqual(result['coff_timestamp_utc_untrusted'], '2005-07-06T12:05:11+00:00')
        for flag in ('file_executed', 'release_version_proven', 'publisher_original_hash_verified', 'native_pet_runtime_verified'):
            self.assertFalse(result[flag])

    def test_login_markers_are_observations(self):
        result = inventory_pe(specimen())
        self.assertEqual([x['text'] for x in result['static_markers']], ['ClientLogin', 'CharLogin'])

    def test_utf16_updater_marker_detected(self):
        result = inventory_pe(specimen(content='SaUpdate\0'.encode('utf-16le')))
        self.assertEqual(result['static_markers'][0]['encoding'], 'utf-16le')

    def test_upx_sections_without_decompression(self):
        self.assertTrue(inventory_pe(specimen(name=b'UPX0'))['upx_section_names_present'])

    def test_version_block_value_and_offset(self):
        self.assertEqual(version_candidates(version_block()), [{'key':'FileVersion','value':'1, 0, 0, 1','block_file_offset':0}])

    def test_truncated_or_fake_resource_key_not_value(self):
        self.assertEqual(version_candidates(version_block()[:-2]), [])
        self.assertEqual(version_candidates('FileVersion\0fake\0'.encode('utf-16le')), [])

    def test_bad_dos_or_pe_offset(self):
        for data in (b'', b'<html>not a file', specimen()[:100], b'MZ'+b'x'*62):
            with self.subTest(size=len(data)), self.assertRaises(ValueError): inventory_pe(data)

    def test_raw_range_and_count_are_bounded(self):
        for field, fmt, value in ((332,'<I',999999),(328,'<I',999999),(70,'<H',97)):
            data=bytearray(specimen());struct.pack_into(fmt,data,field,value)
            with self.subTest(field=field), self.assertRaises(ValueError): inventory_pe(bytes(data))

    def test_x64_and_pe32plus_rejected(self):
        for field, value in ((68,0x8664),(88,0x20b)):
            data=bytearray(specimen());struct.pack_into('<H',data,field,value)
            with self.subTest(field=field), self.assertRaises(ValueError): inventory_pe(bytes(data))

    def test_payload_bound(self):
        with self.assertRaises(ValueError): inventory_pe(b'MZ'+b'\0'*MAX_BYTES)

if __name__ == '__main__': unittest.main()
