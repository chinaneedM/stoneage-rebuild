import struct
import unittest
import zlib
from tools import stoneage_native_album_source_r36 as r

class SparseOriginalRead(unittest.TestCase):
 def setup_reader(self,**kw):
  parts=[b'0123456789',b'abcdefghijk'];calls=[]
  def fetch(p,s,e):calls.append((p,s,e));return parts[p][s:e+1]
  return r.SparseParts(fetch,sizes=[10,11],chunk=4,**kw),calls

 def test_cross_part_boundary_and_cache_keep_bytes(self):
  reader,calls=self.setup_reader();reader.seek(8);self.assertEqual(reader.read(7),b'89abcde')
  before=len(calls);reader.seek(8);self.assertEqual(reader.read(7),b'89abcde');self.assertEqual(len(calls),before)
  self.assertEqual(reader.fetched,10)

 def test_budget_rejects_before_next_request(self):
  reader,calls=self.setup_reader(max_bytes=4);self.assertEqual(reader.read(4),b'0123')
  with self.assertRaises(ValueError):reader.read(1)
  self.assertEqual(calls,[(0,0,3)])

 def test_no_implicit_full_archive_read_or_invalid_seek(self):
  reader,calls=self.setup_reader()
  for f in (lambda:reader.read(),lambda:reader.seek(-1),lambda:reader.seek(22)):
   with self.assertRaises(ValueError):f()
  self.assertEqual(calls,[]);reader.seek(0,2);self.assertEqual(reader.read(9),b'')

 def test_bad_range_length_fails(self):
  reader=r.SparseParts(lambda p,s,e:b'',sizes=[4],chunk=4)
  with self.assertRaises(ValueError):reader.read(1)

class IndependentMemberCarrier(unittest.TestCase):
 def header(self):
  b=bytearray(40);b[2]=0x74;struct.pack_into('<H',b,5,40);struct.pack_into('<I',b,7,3);return bytes(b)

 def test_solid_encrypted_and_split_are_not_silently_extracted(self):
  for flag in [1,2,4,16,17]:
   with self.subTest(flag=flag),self.assertRaises(ValueError):r.isolated_rar(self.header(),b'abc',flag)

 def test_exact_member_bytes_and_valid_envelope_crc(self):
  h=self.header();out=r.isolated_rar(h,b'abc',0);main,end=r.original_main_and_end()
  self.assertEqual(out,main+h+b'abc'+end)
  for block in (main[7:],end):self.assertEqual(int.from_bytes(block[:2],'little'),zlib.crc32(block[2:])&65535)
  with self.assertRaises(ValueError):r.isolated_rar(h,b'ab',0)

if __name__=='__main__':unittest.main()
