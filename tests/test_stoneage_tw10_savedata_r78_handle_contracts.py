import copy
import json
import unittest
from tools.stoneage_tw10_savedata_r78_handle_contracts import BASE,PINS,analyze,qualify,geometry,reference_geometry

class R78Tests(unittest.TestCase):
 def setUp(self):
  self.raws={k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()};d=json.loads(self.raws['r77']);self.rows={r['site_rva']:r for r in d['decoded_instruction_rows']};self.edges=set(map(tuple,d['bounded_graph_edges']))
 def reject(self,fn):
  fn(self.rows,self.edges)
  with self.assertRaises(ValueError):qualify(self.rows,self.edges)
 def test_retained_replay(self):
  r=analyze(self.raws);self.assertEqual((r['graph_nodes'],r['graph_edges'],r['call_count']),(16,16,0));self.assertFalse(r['actual_handle_or_table_values_proven'])
 def test_unsigned_range(self):self.reject(lambda r,e:r[0x4e905].__setitem__('mnemonic','jge'))
 def test_signed_shift_required(self):self.reject(lambda r,e:r[0x4e90c].__setitem__('mnemonic','shr'))
 def test_wrong_slot_scale(self):self.reject(lambda r,e:r[0x4e916]['operands'][0]['geometry'].__setitem__('index_scale',4))
 def test_wrong_slot_flag_offset(self):self.reject(lambda r,e:r[0x4e916]['operands'][0]['geometry'].__setitem__('relative_field_offset',0))
 def test_wrong_flag_mask(self):self.reject(lambda r,e:r[0x4e916]['operands'][1].__setitem__('constant',2))
 def test_lea_must_preserve_flags(self):self.reject(lambda r,e:r[0x4e91b]['decoder_written_registers'].append('eflags'))
 def test_wrong_pointer_table(self):self.reject(lambda r,e:r[0x4e90f]['operands'][1]['geometry']['displacement_region'].__setitem__('displacement_rva',24254560))
 def test_wrong_return_load(self):self.reject(lambda r,e:r[0x4e920]['operands'][1]['geometry'].__setitem__('relative_field_offset',4))
 def test_untouched_ebp_control(self):self.reject(lambda r,e:r[0x4e907]['decoder_written_registers'].append('ebp'))
 def test_wrong_ret_cleanup(self):self.reject(lambda r,e:r[0x4e922]['operands'].append({'kind':'immediate','constant':4}))
 def test_guard_edge_deleted(self):self.reject(lambda r,e:e.remove((0x4e905,0x4e923)))
 def test_success_edge_changed(self):self.reject(lambda r,e:e.add((0x4e905,0x4e920)))
 def test_raw_pin_mutation(self):
  self.raws['r77']+=b' '
  with self.assertRaises(ValueError):analyze(self.raws)
 def test_signed_boundary(self):
  self.assertEqual(geometry(0x80000000),(-67108864,0));self.assertEqual(geometry(0xffffffff),(-1,248));self.assertEqual(geometry(31),(0,248));self.assertEqual(geometry(32),(1,0))
 def test_invented_wrap_and_signed_reference(self):
  for n in[-2**40,-33,-32,-1,0,1,31,32,2**31-1,2**31,2**32-1,2**40+17]:self.assertEqual(geometry(n),reference_geometry(n))
if __name__=='__main__':unittest.main()
