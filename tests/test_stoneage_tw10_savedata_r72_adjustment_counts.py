import copy
import unittest
from tools.stoneage_tw10_savedata_r72_adjustment_counts import BASE,PINS,U32,analyze,qualify,model,full_write_relation,independent_reference
from tools.stoneage_tw10_savedata_r71_adjustment_static import retained_rows
import json

def sources():return {k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()}
def controls():
 d={k:json.loads(v)for k,v in sources().items()};return retained_rows(d.values()),{tuple(e)for e in d['r71']['bounded_graph_edges']}

class R72Tests(unittest.TestCase):
 def mutate(self,at,f):
  rows,edges=controls();f(rows[at])
  with self.assertRaises(ValueError):qualify(rows,edges)
 def test_exact_canonical_replay(self):
  d=analyze(sources());self.assertEqual(d,json.loads((BASE/'STONEAGE-TW10-SAVEDATA-R72-ADJUSTMENT-COUNTS-DERIVED.json').read_text()));self.assertEqual(d['available_decoded_graph_nodes'],128)
 def test_bitflipped_custody(self):
  raws=sources();raws['r71']+=b' '
  with self.assertRaisesRegex(ValueError,'immutable source'):analyze(raws)
 def test_byte_match_literal(self):self.mutate(0x4c64e,lambda r:r['operands'][1].__setitem__('constant',13))
 def test_inserted_literal(self):self.mutate(0x4c656,lambda r:r['operands'][1].__setitem__('constant',10))
 def test_adjustment_offset(self):self.mutate(0x4c653,lambda r:r['operands'][0]['geometry'].__setitem__('relative_field_offset',-12))
 def test_adjustment_width(self):self.mutate(0x4c653,lambda r:r['operands'][0].__setitem__('width_bytes',1))
 def test_adjustment_access(self):self.mutate(0x4c653,lambda r:r['operands'][0].__setitem__('decoder_write',False))
 def test_signed_unsigned_not_interchangeable(self):
  for at,m in ((0x4c644,'jge'),(0x4c66d,'jb')):
   with self.subTest(at=at):self.mutate(at,lambda r:r.__setitem__('mnemonic',m))
 def test_direct_flag_source(self):self.mutate(0x4c64e,lambda r:r.__setitem__('decoder_written_registers',[]))
 def test_wrong_branch_target(self):self.mutate(0x4c651,lambda r:r['operands'][0].__setitem__('constant',0x44c653))
 def test_counter_initialization(self):self.mutate(0x4c5f1,lambda r:r.__setitem__('mnemonic','or'))
 def test_nonunit_frame_index_scale(self):self.mutate(0x4c635,lambda r:r['operands'][1]['geometry'].__setitem__('index_scale',2))
 def test_missing_adjustment_bypass_edge(self):
  rows,e=controls();e.remove((0x4c651,0x4c65a))
  with self.assertRaisesRegex(ValueError,'witnesses|predicate edges'):qualify(rows,e)
 def test_wrong_post_store_threshold(self):self.mutate(0x4c667,lambda r:r['operands'][1].__setitem__('constant',1023))
 def test_invented_octet_expansion(self):
  self.assertEqual(independent_reference([0,10,13,255]),[0,13,10,13,255]);self.assertEqual(full_write_relation([0,10,13,255]),(5,1,[5]))
 def test_poststore_threshold_overshoot(self):
  self.assertEqual(full_write_relation([65]*1023+[10]),(1025,1,[1025]));self.assertEqual(full_write_relation([10]*513),(1026,513,[1024,2]))
 def test_partial_write_is_not_general_prefix_count(self):
  d=analyze(sources());c=d['invented_partial_write_counterexample'];self.assertNotEqual(c['uint32_subtraction'],c['completed_input_tokens_in_output_prefix']);self.assertEqual(d['invented_partial_write_prefixes'][0]['uint32_subtraction'],U32)
 def test_empty_invented_sequence(self):self.assertEqual(model([]),[]);self.assertEqual(full_write_relation([]),(0,0,[]))
 def test_reject_non_octet_or_boolean(self):
  for seq in ([True],[-1],[256],b'\x0a'):
   with self.subTest(seq=seq),self.assertRaises(ValueError):model(seq)
 def test_reject_invalid_model_threshold(self):
  for n in (True,0,1025):
   with self.subTest(n=n),self.assertRaises(ValueError):model([10],n)

if __name__=='__main__':unittest.main()
