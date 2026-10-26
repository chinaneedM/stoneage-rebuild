import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools import stoneage_mixed25_data_prefix_r35 as r

class SelectedOriginalMembers(unittest.TestCase):
 def prepare(self,root):
  path=root/r.PREFIX/'test.dat';path.parent.mkdir(parents=True);path.write_bytes(b'synthetic-data')
  return path,{'test.dat':(14,hashlib.sha256(b'synthetic-data').hexdigest())}

 def test_exact_full_member_qualification(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);path,targets=self.prepare(root)
   with patch.object(r,'TARGETS',targets):self.assertEqual(r.original_members(root),{'test.dat':b'synthetic-data'})

 def test_wrong_hash_never_sealed(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);path,targets=self.prepare(root);path.write_bytes(b'synthetic-datb')
   with patch.object(r,'TARGETS',targets),self.assertRaises(ValueError):r.original_members(root)

 def test_wrong_namespace_is_not_selected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'test.dat').write_bytes(b'synthetic-data')
   with patch.object(r,'TARGETS',{'test.dat':(14,r.sha(b'synthetic-data'))}),self.assertRaises(ValueError):r.original_members(root)

 def test_duplicate_full_paths_under_two_roots_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);_,targets=self.prepare(root/'one');self.prepare(root/'two')
   with patch.object(r,'TARGETS',targets),self.assertRaises(ValueError):r.original_members(root)

 def test_fixed_bounded_source_not_full_client(self):
  self.assertEqual(r.LIMIT,16777216);self.assertEqual(set(r.TARGETS),{'AISetting.dat','album_4.dat','auto.dat'})
  self.assertEqual(sum(x[0] for x in r.TARGETS.values()),412046)

if __name__=='__main__':unittest.main()
