"""Synthetic initializer/width/domain controls and ledger mutations.

Positive DES math tests are independently rederived from pinned source maps and
121 public vectors in the workflow's separate real-source step.
"""
import json
from pathlib import Path
import unittest
from tools.stoneage_wayi_login_input import (parse_array,table_bytes,rotate,
    key_schedule,des_block,rounded_length,transform,wrapper_return,probe,validate)


class LoginInputTests(unittest.TestCase):
 def report(self):
  return json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-WAYI-LOGIN-INPUT-R1.json').read_text())

 def test_numeric_array_literal_and_symbolic_sums(self):
  self.assertEqual(parse_array('static uchar a[]={C + 20,D + 4,0x10,1,};','a'),[48,4,16,1])

 def test_nested_numeric_array(self):
  self.assertEqual(parse_array('ulong a[2][2]={{0x10,0x20},{1,2}};','a'),[16,32,1,2])

 def test_missing_or_ambiguous_array_rejected(self):
  for s in ('char b[]={1};','char a[]={1};char a[]={2};'):
   with self.assertRaises(ValueError):parse_array(s,'a')

 def test_code_expression_not_evaluated(self):
  for token in ('1<<4','run()','-1','C*2','0;malicious','007'):
   with self.assertRaises(ValueError):parse_array('char a[]={'+token+'};','a')

 def test_empty_or_unterminated_array_rejected(self):
  for s in ('char a[]={};','char a[]={1,2'):
   with self.assertRaises(ValueError):parse_array(s,'a')

 def test_little_endian_dword_table(self):
  self.assertEqual(table_bytes([0x01020304],4),b'\x04\x03\x02\x01')

 def test_table_width_and_boolean_bounds(self):
  for v,w in (([256],1),([-1],4),([True],1),([1],2)):
   with self.assertRaises(ValueError):table_bytes(v,w)

 def test_word_rotation_masks_to_32bit(self):
  self.assertEqual(rotate(0x80000000,1,32),1)
  self.assertEqual(rotate(0xfffffffff,0,32),0xffffffff)

 def test_28bit_key_rotation(self):
  self.assertEqual(rotate(1<<27,1,28),1)

 def test_rotation_domain(self):
  for n,bits in ((-1,32),(32,32),(1,64),(True,32)):
   with self.assertRaises(ValueError):rotate(1,n,bits)

 def test_round_up_existing_backing_requirement(self):
  self.assertEqual([rounded_length(n)for n in (0,1,7,8,9,16,31,32)],[0,8,8,8,16,16,32,32])
  with self.assertRaises(ValueError):transform(b'R1-key!!',b'xxxxxxx',7,0,{})

 def test_length_domain(self):
  for n in (-1,4097,True,1.0):
   with self.assertRaises(ValueError):rounded_length(n)

 def test_wrapper_mode_return_is_separate_from_work(self):
  self.assertEqual([wrapper_return(m)for m in range(4)],[1,1,0,0])

 def test_key_rejects_non_eight_bytes(self):
  for key in (b'',b'1234567',b'123456789','12345678'):
   with self.assertRaises(ValueError):key_schedule(key,{})

 def test_block_length_and_direction_domain(self):
  for block,d in ((b'123',False),(b'12345678',1)):
   with self.assertRaises(ValueError):des_block(b'R1-key!!',block,{},d)

 def test_zero_length_does_not_invent_padding(self):
  self.assertEqual(transform(b'R1-key!!',b'unchanged',0,0,{}),b'unchanged')

 def test_accepted_static_evidence(self):
  self.assertEqual(len(validate(self.report())['tables']),9)

 def test_changed_table_hash_rejected(self):
  r=self.report();r['probe']['tables'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):validate(r)

 def test_32byte_flow_must_not_be_promoted_to16(self):
  r=self.report();r['probe']['anchors']['0x2098d']['operands'][0]['value']=16
  with self.assertRaises(ValueError):validate(r)

 def test_current18_not_substituted_for_compiled12(self):
  r=self.report();r['probe']['anchors']['0x20baa']['operands'][0]['value']=18
  with self.assertRaises(ValueError):validate(r)

 def test_native_promotion_rejected(self):
  for component,key in (('probe','native_login_verified'),('crosscheck','original_program_executed')):
   r=self.report();r[component][key]=True
   with self.assertRaises(ValueError):validate(r)

 def test_linux_ulong64_not_inferred_from_32bit_agreement(self):
  r=self.report();r['crosscheck']['word_width_bits']=64
  with self.assertRaises(ValueError):validate(r)

 def test_original_program_specimen_required(self):
  with self.assertRaises(ValueError):probe(b'MZ')
