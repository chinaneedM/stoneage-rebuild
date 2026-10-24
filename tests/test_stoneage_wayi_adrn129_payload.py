import csv
import gzip
from pathlib import Path
import struct
import tempfile
import unittest
from tools.stoneage_wayi_adrn129_payload import export_index, safe_members, source_contract
from tools.stoneage_tw10_resource_metadata import parse_adrn_record


def record(bitmap=1, address=0, width=10):
    return struct.pack('<IIIiiii', bitmap, address, 18, -2, -3, width, 12)+bytes(52)


class IndexPayloadTests(unittest.TestCase):
    def test_exact_record_identity_and_changed_address_are_distinct(self):
        raw = record()
        parsed = parse_adrn_record(raw)
        key = (*[parsed[k] for k in ('bitmapno','adder','size','xoff','yoff','width','height')], parsed['attr_sha256'])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'index.gz'
            metrics = export_index(raw+record(2, 18), path, {'same': {1:key}, 'changed': {1:(1, 9, *key[2:])}})
            self.assertEqual(metrics['records'], 2)
            self.assertEqual(metrics['comparisons_by_bitmap_id']['same']['counts'], {'ABSENT_ID':1,'EXACT_HEADER_AND_ATTR_HASH':1})
            self.assertEqual(metrics['comparisons_by_bitmap_id']['changed']['counts'], {'ABSENT_ID':1,'CHANGED_INDEX_METADATA':1})
            with gzip.open(path,'rt') as f:
                rows=list(csv.DictReader(f,delimiter='\t'))
            self.assertEqual(len(rows),2)
            self.assertNotIn('rd_block_sha256',rows[0])

    def test_duplicates_and_special_dimensions_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            r=export_index(record(width=-1)*2,Path(temp)/'x.gz',{})
            self.assertEqual(r['duplicate_bitmap_occurrences'],1)
            self.assertEqual(r['special_dimensions_preserved'],2)
            self.assertEqual(r['unique_record_hashes'],1)

    def test_empty_and_remainder_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            for raw in (b'',record()[:-1],record()+b'!'):
                with self.assertRaises(ValueError):export_index(raw,Path(temp)/'x.gz',{})

    def test_unsafe_member_and_excessive_unpacked_size_rejected(self):
        for path,size in [('../x',5),('C:/x',5),('x',300*1024*1024)]:
            with self.assertRaises(ValueError):
                safe_members('----------\nPath = '+path+'\nSize = '+str(size)+'\nAttributes = A\n')

    def test_current_parent_byte_contract(self):
        self.assertEqual(source_contract()['response_bytes'],3983427)


if __name__ == '__main__':unittest.main()
