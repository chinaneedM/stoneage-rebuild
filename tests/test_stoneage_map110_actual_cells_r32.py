"""R32 adversarial original map cell extraction tests on synthetic grids."""
import hashlib
import struct
import unittest
from tools.stoneage_map110_actual_cells_r32 import parse_dat, compare, verify_timeline, original_git_blob

def fake(w,h,planes):
 return struct.pack("<II",w,h)+b"".join(struct.pack("<"+"H"*len(p),*p) for p in planes)

class TestR32(unittest.TestCase):
 def test_parser_exact_shape(self):
  p=fake(46,45,[[0]*2070 for _ in range(3)])
  self.assertEqual(parse_dat(p)[:2],(46,45))

 def test_three_changed_positions(self):
  a=[[0]*2070 for _ in range(3)]
  b=[p.copy() for p in a]
  for index,value in [(0,13),(46,22),(2069,35)]:b[2][index]=value
  out=compare(fake(46,45,a),fake(46,45,b))
  self.assertEqual([x["changed_cell_count"] for x in out["plane_diffs"]],[0,0,3])
  self.assertEqual(out["plane_diffs"][2]["changes"][-1]["x_rowmajor_candidate"],45)
  self.assertEqual(out["plane_diffs"][2]["changes"][-1]["y_rowmajor_candidate"],44)

 def test_reject_other_plane_change(self):
  a=[[0]*2070 for _ in range(3)]
  b=[p.copy() for p in a]
  b[0][0]=1
  for i in (12,13,14):b[2][i]=1
  with self.assertRaises(ValueError):compare(fake(46,45,a),fake(46,45,b))

 def test_reject_insufficient_differences(self):
  a=[[0]*2070 for _ in range(3)]
  b=[p.copy() for p in a];b[2][7]=55
  with self.assertRaises(ValueError):compare(fake(46,45,a),fake(46,45,b))

 def test_reject_wrong_dimensions(self):
  a=[[0]*2070 for _ in range(3)]
  b=[p.copy() for p in a]
  for i in (0,1,2):b[2][i]=i+1
  with self.assertRaises(ValueError):compare(fake(45,46,a),fake(46,45,b))

 def test_reject_truncated(self):
  with self.assertRaises(ValueError):parse_dat(b"\x00"*7)
  with self.assertRaises(ValueError):parse_dat(fake(46,45,[[0]*2070]*3)[:-2])

 def test_reject_fabricated_witness(self):
  from tools.stoneage_map110_actual_cells_r32 import TIMELINE
  raw=TIMELINE.read_text()
  verify_timeline(raw)
  with self.assertRaises(ValueError):
   verify_timeline(raw.replace("jd_event_diff=3","jd_event_diff=5"))

 def test_git_sha_blob_different_than_file_sha(self):
  raw=b"synthetic source"
  self.assertNotEqual(original_git_blob(raw),hashlib.sha256(raw).hexdigest())

if __name__=="__main__":unittest.main()
