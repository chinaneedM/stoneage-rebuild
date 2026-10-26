import struct
import unittest
from tools import stoneage_album_adrn_source_r37 as r

def record(bitmap,alias):
 b=bytearray(80);struct.pack_into('<IIIiiii',b,0,bitmap,1000+bitmap,50,-2,-4,32,36);struct.pack_into('<I',b,76,alias);return bytes(b)

class SourceRecordNamespaces(unittest.TestCase):
 def test_alias_and_same_number_are_independent(self):
  raw=record(7300,28001)+record(28001,100100)
  d=r.select_rows(raw);a=d['selected_logical_aliases']['28001'];b=d['physical_same_number_counterexamples']['28001']
  self.assertEqual(a[0]['bitmapno'],7300);self.assertEqual(b[0]['logical_alias'],100100)
  self.assertNotEqual(a[0]['record_sha256'],b[0]['record_sha256'])

 def test_all_duplicate_alias_and_physical_occurrences_survive(self):
  d=r.select_rows(record(1,28001)+record(2,28001)+record(28001,0)+record(28001,0))
  self.assertEqual(len(d['selected_logical_aliases']['28001']),2)
  self.assertEqual(len(d['physical_same_number_counterexamples']['28001']),2)
  self.assertEqual(d['nonzero_duplicate_alias_occurrences'],1)

 def test_incomplete_record_is_not_zero_padded(self):
  for b in [b'',record(1,28001)[:-1],record(1,28001)+b'\0']:
   with self.assertRaises(ValueError):r.select_rows(b)

 def test_zero_and_unselected_aliases_not_promoted(self):
  d=r.select_rows(record(0,0)+record(1,28004))
  self.assertTrue(all(v==[] for v in d['selected_logical_aliases'].values()))
  self.assertEqual(d['records_scanned'],2)

if __name__=='__main__':unittest.main()
