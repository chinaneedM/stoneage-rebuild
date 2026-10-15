"""Independent bounded invented-graph and pinned original-derived guards."""
import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_r59_cfg_witness import load,derive,path
SRC=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json"
class CFGTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=SRC.read_bytes();cls.d=json.loads(cls.raw)
 def test_original_graph_witnesses(self):
  x=load(self.raw)
  self.assertIn(0x4a683,x["shared_path_through_native_call"])
  self.assertNotIn(0x4a683,x["shared_path_bypassing_native_call"])
  self.assertFalse(x["native_WriteFile_called_result_flush_close_persistence_proven"])
  self.assertTrue(x["close_path_bypassing_both_indirect_calls"])
 def test_wrong_digest_rejected(self):
  with self.assertRaises(ValueError):load(self.raw+b" ")
 def test_mutated_target_rejected(self):
  d=copy.deepcopy(self.d);d["contexts"][0]["call_contexts"][0]["identity"]["direct_target_rva"]=0
  with self.assertRaises(ValueError):derive(d)
 def test_reachable_return_removed_rejected(self):
  d=copy.deepcopy(self.d);c=d["contexts"][0]
  c["bounded_edges"]=[e for e in c["bounded_edges"] if e[1]!=0x4a6b2]
  c["graph"]["edges"]=len(c["bounded_edges"])
  with self.assertRaises(ValueError):derive(d)
 def test_indirect_kind_mutated_rejected(self):
  d=copy.deepcopy(self.d);c=d["contexts"][1]
  next(x for x in c["call_contexts"] if x["site_rva"]==0x4a5a3)["identity"]["kind"]="direct"
  with self.assertRaises(ValueError):derive(d)
 def test_fake_graph_control(self):
  c={"root_candidate_rva":10,"bounded_node_rvas":[10,11,12],"bounded_edges":[[10,12],[11,12]]}
  self.assertEqual(path(c,12,excluded=(11,)),[10,12])
  self.assertIsNone(path(c,12,required=(11,)))
 def test_bad_edge_guard(self):
  c={"root_candidate_rva":10,"bounded_node_rvas":[10,11],"bounded_edges":[[10,999]]}
  with self.assertRaises(ValueError):path(c,11)
 def test_native_promotion_rejected(self):
  d=copy.deepcopy(self.d);d["actual_native_flush_close_or_persistence_proven"]=True
  with self.assertRaises(ValueError):derive(d)
if __name__=="__main__":unittest.main()
