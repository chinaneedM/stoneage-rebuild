"""Test metadata evidence boundaries without original proprietary DAT grids."""
from copy import deepcopy
import hashlib
import json
import unittest
from tools.stoneage_map110_original_archive_r32 import guard
from tools.stoneage_map110_actual_cells_r32 import TIMELINE,SOURCES,original_git_blob

def fixture():
 original=TIMELINE.read_bytes()
 keys=("june","dec")
 planes=[
  {"ordinal":i+1,"changed_cell_count":0 if i<2 else 3,
   "june_plane_sha256":("0"*64 if i<2 else "1"*64),
   "dec_plane_sha256":("0"*64 if i<2 else "2"*64),
   "old_nonzero_count":0,"new_nonzero_count":0,
   "changes":[] if i<2 else [
    {"index":5,"x_rowmajor_candidate":5,"y_rowmajor_candidate":0,"june_u16":1,"dec_u16":2},
    {"index":46,"x_rowmajor_candidate":0,"y_rowmajor_candidate":1,"june_u16":3,"dec_u16":4},
    {"index":2069,"x_rowmajor_candidate":45,"y_rowmajor_candidate":44,"june_u16":5,"dec_u16":6}
   ]} for i in range(3)]
 return {"schema":"stoneage.map110_archived_2003_original_cell_delta.r32",
         "timeline_git_blob":original_git_blob(original),
         "map_token":110,"map_original_path":"map/110.DAT",
         "source_packages":{k:{"capture":v["capture"],"container_sha256":v["container_sha256"],
                                "original_dat_sha256":v["file_sha256"]} for k,v in SOURCES.items()},
         "result":{"width":46,"height":45,"total_cells_per_plane":2070,
                   "total_actual_cells_compared":6210,"plane_diffs":planes},
         "no_named_map_or_quest_role":True,"no_map_grid_released":True,
         "event_plane_runtime_semantics_unverified":True,"world_coordinates_not_authenticated":True,
         "june_equals_preserved25_by_whole_file_prior_witness_only":True}

class TestGuardR32(unittest.TestCase):
 def setUp(self):
  self.o=fixture()
  self.timeline=TIMELINE.read_bytes()
 def check_rejected(self,alter):
  o=deepcopy(self.o);alter(o)
  with self.assertRaises(ValueError):guard(o,self.timeline)
 def test_good_synthetic(self):
  self.assertEqual(guard(self.o,self.timeline)["changed_ordinal_planes"],[0,0,3])
 def test_source_SHA_mismatch(self):
  self.check_rejected(lambda x:x["source_packages"]["june"].__setitem__("container_sha256","x"*64))
 def test_later_build_is_not_original_tw10(self):
  self.check_rejected(lambda x:x.__setitem__("world_coordinates_not_authenticated",False))
 def test_unproven_event_semantics(self):
  self.check_rejected(lambda x:x.__setitem__("event_plane_runtime_semantics_unverified",False))
 def test_extra_changed_cell(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][2]["changes"].append(
   dict(x["result"]["plane_diffs"][2]["changes"][0],index=6)))
 def test_changed_first_plane(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][0].__setitem__("changed_cell_count",1))
 def test_corrupt_rowmajor_xy(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][2]["changes"][1].__setitem__("x_rowmajor_candidate",46))
 def test_equal_old_new(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][2]["changes"][0].__setitem__("dec_u16",1))
 def test_spatial_collision(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][2]["changes"][1].__setitem__("index",5))
 def test_nonzero_balance(self):
  self.check_rejected(lambda x:x["result"]["plane_diffs"][2].__setitem__("new_nonzero_count",100))
 def test_timeline_digest(self):
  self.check_rejected(lambda x:x.__setitem__("timeline_git_blob","f"*40))

if __name__=="__main__":unittest.main()
