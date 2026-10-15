import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_return_r57_contract import derive,validate,route
from tools.stoneage_tw10_savedata_return_r57_guard import audit
P=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R57-ORIGINAL.json';RAW=P.read_bytes();D=json.loads(RAW)
class ContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=derive(RAW)
 def test_custody(self):self.assertRaises(ValueError,derive,RAW+b' ')
 def test_replay(self):self.assertTrue(validate(self.d,RAW))
 def test_reverse(self):self.assertEqual([audit(c) for c in D['contexts']],[14,6])
 def test_bypass_excludes_native(self):self.assertNotIn(0x48c5e,self.d['buffer_copy_path_without_direct_native_context_call']['path_rvas'])
 def test_bypass_includes_copy(self):self.assertIn(0x48c1a,self.d['buffer_copy_path_without_direct_native_context_call']['path_rvas'])
 def test_bypass_all_edges(self):
  p=self.d['buffer_copy_path_without_direct_native_context_call']['path_rvas'];es=set(map(tuple,D['contexts'][0]['bounded_edges']));self.assertTrue(all((a,b) in es for a,b in zip(p,p[1:])))
 def test_direct_eax_sources(self):self.assertEqual([x['site_rva'] for x in self.d['direct_return_source_surfaces'][0]['direct_eax_source_candidates']],[0x48bd9,0x48caa,0x48cc1])
 def test_close_sources(self):self.assertEqual([x['site_rva'] for x in self.d['direct_return_source_surfaces'][1]['direct_eax_source_candidates']],[0x4857c,0x485b9])
 def test_no_promote(self):
  d=copy.deepcopy(self.d);d['actual_buffering_api_ownership_native_count_flush_close_or_persistence_proven']=True;self.assertRaises(ValueError,validate,d,RAW)
 def test_bool_confusion(self):
  d=copy.deepcopy(self.d);d['write_conditional_frame']['entry_ebp_offset_after_push_ebp_and_mov_ebp_esp']=False;self.assertRaises(ValueError,validate,d,RAW)
 def test_route_cut(self):self.assertIsNone(route([[1,2],[2,3]],1,3,[2]))
 def test_route_cycle(self):self.assertEqual(route([[1,2],[2,1],[2,3]],1,3),[1,2,3])
if __name__=='__main__':unittest.main()
