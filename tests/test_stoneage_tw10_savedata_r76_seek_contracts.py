import copy
import json
import unittest
from tools.stoneage_tw10_savedata_r76_seek_contracts import BASE,PINS,CLEANUPS,NEGATIVE,analyze,qualify,paths_to_return,stack_ledger,delta_reference

def raws():return{k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()}
def controls():
 g=json.loads(raws()['r75']);return{r['site_rva']:r for r in g['decoded_instruction_rows']},set(g['bounded_graph_node_rvas']),{tuple(e)for e in g['bounded_graph_edges']}

class R76Tests(unittest.TestCase):
 def mutate(self,n,f):
  r,_,e=controls();f(r[n])
  with self.assertRaises(ValueError):qualify(r,e)
 def test_exact_canonical(self):
  d=analyze(raws());self.assertEqual(d,json.loads((BASE/'STONEAGE-TW10-SAVEDATA-R76-SEEK-CONTRACTS-DERIVED.json').read_text()));self.assertEqual(d['structural_root_to_ret_paths'],7)
 def test_source_custody(self):
  r=raws();r['r75']+=b' '
  with self.assertRaisesRegex(ValueError,'immutable source'):analyze(r)
 def test_all_seven_conditional_restore_paths(self):
  r,n,e=controls()
  for path in paths_to_return(n,e,r):
   x=stack_ledger(path,r);self.assertEqual(x['esp_before_ret'],0);self.assertEqual(x['restored_registers'],['ebx','esi','edi']);self.assertEqual(delta_reference(path,r,CLEANUPS),0)
 def test_cleanup_is_a_necessary_premise(self):
  r,n,e=controls();bad={**CLEANUPS,0x4c7b0:12};paths=[p for p in paths_to_return(n,e,r)if 0x4c7b0 in p]
  self.assertTrue(all(stack_ledger(p,r,bad)['esp_before_ret']!=0 for p in paths))
 def test_alias_nonclobber_is_a_necessary_premise(self):
  r,n,e=controls();p=next(p for p in paths_to_return(n,e,r)if 0x4c7b0 in p)
  self.assertEqual(stack_ledger(p,r,clobber_saved=True)['restored_registers'],[])
 def test_ebp_cannot_be_inferred_preserved(self):
  r,n,e=controls();p=next(p for p in paths_to_return(n,e,r)if 0x4c7b0 in p);self.assertFalse(stack_ledger(p,r)['ebp_entry_token_preserved'])
 def test_argument_physical_geometry(self):
  r,n,e=controls();args=[stack_ledger(p,r)['seek_argument_tokens_if_reached']for p in paths_to_return(n,e,r)if 0x4c7b0 in p]
  self.assertEqual(args,[['opaque_eax_after_313230',0,0,2]]*4)
 def test_wrong_save_register(self):self.mutate(0x4c765,lambda r:r['operands'][0].__setitem__('register','eax'))
 def test_wrong_restore_register(self):self.mutate(0x4c7f7,lambda r:r['operands'][0].__setitem__('register','esi'))
 def test_ret_immediate(self):self.mutate(0x4c7fa,lambda r:r.__setitem__('operands',[{'kind':'immediate','constant':4,'width_bytes':4}]))
 def test_esp_slot24(self):self.mutate(0x4c7a5,lambda r:r['operands'][0]['geometry'].__setitem__('relative_field_offset',20))
 def test_esp_slot28(self):self.mutate(0x4c7ab,lambda r:r['operands'][0]['geometry'].__setitem__('relative_field_offset',24))
 def test_null_high_pointer(self):self.mutate(0x4c7a9,lambda r:r['operands'][0].__setitem__('constant',1))
 def test_api_slot(self):self.mutate(0x4c7b0,lambda r:r['operands'][0]['geometry']['displacement_region'].__setitem__('displacement_rva',0x5208c))
 def test_getlast_error_slot(self):self.mutate(0x4c7bd,lambda r:r['operands'][0]['geometry']['displacement_region'].__setitem__('displacement_rva',0x520cc))
 def test_mask253(self):self.mutate(0x4c7d6,lambda r:r['operands'][1].__setitem__('constant',251))
 def test_table_byte_geometry(self):self.mutate(0x4c7d6,lambda r:r['operands'][0]['geometry'].__setitem__('index_register','edi'))
 def test_local_esp_write_not_ignored(self):self.mutate(0x4c7db,lambda r:r.__setitem__('decoder_written_registers',['esp']))
 def test_missing_saved_return_edge(self):
  r,n,e=controls();e.remove((0x4c7f9,0x4c7fa))
  with self.assertRaises(ValueError):qualify(r,e)
 def test_cycle_rejected_for_path_ledger(self):
  r,n,e=controls();e.add((0x4c7f7,0x4c761))
  with self.assertRaisesRegex(ValueError,'acyclic'):paths_to_return(n,e,r)
 def test_missing_cleanup_not_assumed(self):
  r,n,e=controls();p=next(p for p in paths_to_return(n,e,r)if 0x4c7b0 in p)
  with self.assertRaisesRegex(ValueError,'cleanup premise'):stack_ledger(p,r,{})
 def test_all_negative_scope_guards(self):
  d=analyze(raws());self.assertTrue(all(d[k]is False for k in NEGATIVE));self.assertTrue(d['does_not_establish_global_snapshot_identity'])

if __name__=='__main__':unittest.main()
