import copy
import json
import unittest
from tools.stoneage_tw10_savedata_r74_modes_barriers import BASE,PINS,ALIASES,NEGATIVE,analyze,forward,reverse,qualify,invented_decisions
from tools.stoneage_tw10_savedata_r73_modes_static import retained_rows

def source_raws():return{k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()}
def controls():
 d={k:json.loads(v)for k,v in source_raws().items()};return retained_rows(d.values()),{tuple(e)for e in d['r73']['bounded_graph_edges']}
def row(m='nop',writes=()):return{'mnemonic':m,'decoder_written_registers':list(writes)}

class R74Tests(unittest.TestCase):
 def both(self,nodes,edges,rows,root,at,reg,expected):
  self.assertEqual(forward(nodes,edges,rows,root,at,reg),expected);self.assertEqual(reverse(nodes,edges,rows,root,at,reg),expected)
 def mutate(self,at,f):
  rs,e=controls();f(rs[at])
  with self.assertRaises(ValueError):qualify(rs,e)
 def test_exact_report(self):
  d=analyze(source_raws());self.assertEqual(d,json.loads((BASE/'STONEAGE-TW10-SAVEDATA-R74-MODES-BARRIERS-DERIVED.json').read_text()));self.assertEqual(d['decoded_graph_nodes'],139)
 def test_source_bitflip(self):
  d=source_raws();d['r73']+=b' '
  with self.assertRaisesRegex(ValueError,'immutable source'):analyze(d)
 def test_optional_call_kills_even_nondeclared_registers(self):
  self.both({0,1,2},[(0,1),(1,2)],{0:row('mov',['ebp']),1:row('call',['esp']),2:row()},0,2,'ebp',{('opaque_call',1)})
 def test_bypass_and_call_sources_both_retained(self):
  self.both({0,1,2},[(0,1),(0,2),(1,2)],{0:row('mov',['ebx']),1:row('call',['esp']),2:row()},0,2,'ebx',{('full_register_definition',0),('opaque_call',1)})
 def test_partial_register_is_not_full_value(self):
  self.both({0,1,2},[(0,1),(1,2)],{0:row('mov',['eax']),1:row('mov',['al']),2:row()},0,2,'eax',{('partial_register_unknown',1)})
 def test_unknown_instruction_barrier(self):
  self.both({0,1,2},[(0,1),(1,2)],{0:row('mov',['edi']),2:row()},0,2,'edi',{('unknown_instruction',1)})
 def test_loop_fixedpoint(self):
  self.both({0,1,2,3},[(0,1),(1,2),(2,1),(1,3)],{0:row('mov',['esi']),1:row(),2:row('call'),3:row()},0,3,'esi',{('full_register_definition',0),('opaque_call',2)})
 def test_unreachable_definition_does_not_invent_source(self):
  self.both({0,1,2},[(0,2),(1,2)],{0:row('mov',['eax']),1:row('mov',['eax']),2:row()},0,2,'eax',{('full_register_definition',0)})
 def test_entry_unknown(self):self.both({0},{}, {0:row()},0,0,'ebp',{('unknown_entry',0)})
 def test_mask32_is_not128(self):self.mutate(0x4c605,lambda r:r['operands'][1].__setitem__('constant',128))
 def test_byte_width(self):self.mutate(0x4c619,lambda r:r['operands'][0].__setitem__('width_bytes',4))
 def test_mask128_is_not32(self):self.mutate(0x4c619,lambda r:r['operands'][1].__setitem__('constant',32))
 def test_helper_target(self):self.mutate(0x4c60d,lambda r:r['operands'][0].__setitem__('constant',0x44c953))
 def test_stack_delta(self):self.mutate(0x4c612,lambda r:r['operands'][1].__setitem__('constant',8))
 def test_direct_flag_pred(self):self.mutate(0x4c619,lambda r:r.__setitem__('decoder_written_registers',[]))
 def test_table_byte_offset(self):self.mutate(0x4c619,lambda r:r['operands'][0]['geometry'].__setitem__('relative_field_offset',0))
 def test_literal_five(self):self.mutate(0x4c6bd,lambda r:r['operands'][0].__setitem__('constant',9))
 def test_first_byte_load_alias(self):self.mutate(0x4c5e5,lambda r:r['operands'][1]['geometry'].__setitem__('index_register','edi'))
 def test_global_store_is_absolute(self):self.mutate(0x4c6c5,lambda r:r['operands'][0]['geometry'].__setitem__('base_register','eax'))
 def test_literal_nine(self):self.mutate(0x4c6c5,lambda r:r['operands'][1].__setitem__('constant',5))
 def test_missing_optional_bypass(self):
  rs,e=controls();e.remove((0x4c607,0x4c615))
  with self.assertRaises(ValueError):qualify(rs,e)
 def test_separate_temporal_snapshots(self):
  self.assertEqual(invented_decisions(0,128),(False,True));self.assertEqual(invented_decisions(32,0),(True,False));self.assertEqual(invented_decisions(255,255),(True,True))
 def test_snapshot_domain(self):
  for a,b in[(True,0),(-1,0),(0,256),(0,'128')]:
   with self.subTest(a=a,b=b),self.assertRaises(ValueError):invented_decisions(a,b)
 def test_every_negative_flag_remains_false(self):
  d=analyze(source_raws());self.assertTrue(all(d[k]is False for k in NEGATIVE));self.assertEqual(len(d['opaque_calls']),6)

if __name__=='__main__':unittest.main()
