"""Synthetic bounded editing, terminator and source-profile controls."""
import json
from pathlib import Path
import unittest
from tools.stoneage_wayi_input_editor import (login_char_allowed,insert_byte,
 insert_pair,callback_plan,click_submit_condition,settings_factory,validate,probe)


def backing(text):return text+b'\0'*(260-len(text))


class InputEditorTests(unittest.TestCase):
 def report(self):return json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-WAYI-INPUT-EDITOR-R1.json').read_text())

 def test_all_256_login_byte_filters_independent_set(self):
  allowed=set(b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
  self.assertEqual({c for c in range(256)if login_char_allowed(c)},allowed)

 def test_insert_preserves_existing_terminator_in_middle(self):
  b,n,c,ok=insert_byte(backing(b'ABC'),3,1,ord('7'))
  self.assertEqual((b[:5],n,c,ok),(b'A7BC\0',4,2,True))

 def test_insertion_at_beginning_and_end(self):
  for cursor,expected in((0,b'7ABC\0'),(3,b'ABC7\0')):
   result=insert_byte(backing(b'ABC'),3,cursor,ord('7'))
   self.assertEqual(result[0][:5],expected)

 def test_each_cursor_position_has_independent_slice_oracle(self):
  text=b'Ab09XY'
  for cursor in range(len(text)+1):
   b,n,c,ok=insert_byte(backing(text),len(text),cursor,ord('7'))
   expected=text[:cursor]+b'7'+text[cursor:]
   self.assertEqual((b[:n+1],c,ok),(expected+b'\0',cursor+1,True))

 def test_exact_twelve_byte_login_limit(self):
  b=backing(b'');n=c=0
  for char in b'ABCDEFGHIJKLM':b,n,c,ok=insert_byte(b,n,c,char)
  self.assertEqual((b[:13],n,c,ok),(b'ABCDEFGHIJKL\0',12,12,False))

 def test_punctuation_and_high_bytes_rejected_in_login(self):
  for char in(b'_-@ !\xff'):
   self.assertFalse(insert_byte(backing(b'ABC'),3,3,char)[3])

 def test_nul_control_byte_rejected(self):
  for char in range(32):self.assertFalse(insert_byte(backing(b'A'),1,1,char,login=False)[3])

 def test_nonlogin_printable_punctuation_remains_separate_scope(self):
  self.assertTrue(insert_byte(backing(b'A'),1,1,ord('_'),login=False)[3])

 def test_two_byte_login_insertion_rejected(self):
  self.assertFalse(insert_pair(backing(b'A'),1,1,b'\xa4\xa4')[3])

 def test_nonlogin_pair_preserves_terminator_and_count(self):
  b,n,c,ok=insert_pair(backing(b'AB'),2,1,b'\xa4\xa4',login=False)
  self.assertEqual((b[:5],n,c,ok),(b'A\xa4\xa4B\0',4,3,True))

 def test_pair_capacity_boundary(self):
  self.assertTrue(insert_pair(backing(b'ABCDEFGHIJ'),10,10,b'\xa4\xa4',login=False)[3])
  self.assertFalse(insert_pair(backing(b'ABCDEFGHIJK'),11,11,b'\xa4\xa4',login=False)[3])

 def test_invalid_cursor_and_missing_nul_model_guards(self):
  for b,n,c in((backing(b'ABC'),3,4),(b'A'*260,3,3),(backing(b'A\0B'),3,1)):
   with self.assertRaises(ValueError):insert_byte(b,n,c,ord('7'))

 def test_short_backing_not_inferred_safe(self):
  with self.assertRaises(ValueError):insert_byte(b'A\0',1,1,ord('7'))

 def test_callback_ascii_budget(self):
  self.assertEqual(len(callback_plan([b'A']*100)),86)

 def test_callback_complete_pair_can_cross_iteration_budget(self):
  rows=callback_plan([b'A']*85+[b'\xa4\xa4'])
  self.assertEqual(rows[-1],{'start':85,'helper_width':2,'past_loop_budget':True})

 def test_callback_dangling_pair_not_invented(self):
  with self.assertRaises(ValueError):callback_plan([b'ABC'])

 def test_empty_second_field_not_modernized_in_bounded_click_branch(self):
  self.assertTrue(click_submit_condition(b'R1',b''))
  self.assertFalse(click_submit_condition(b'',b'R1'))

 def test_source_string_is_terminated_before_condition(self):
  self.assertFalse(click_submit_condition(b'\0R1',b'R1'))

 def test_settings_constructor_reserved_region_is_zero_in_synthetic_factory(self):
  result=settings_factory(1,20,30,bytes(range(16)))
  self.assertEqual(len(result),127);self.assertEqual(result[:2],b'\x06\x00')
  self.assertEqual(result[2:26],b'\0'*24)
  self.assertEqual(result[36:39],bytes([1,20,30]));self.assertEqual(result[39:55],bytes(range(16)))
  self.assertEqual(result[56:58],b'\x0a\x03')

 def test_settings_input_width_rejected(self):
  with self.assertRaises(ValueError):settings_factory(256,1,1,b'\0'*16)

 def test_accepted_evidence(self):validate(self.report())

 def test_letter_guard_mutation(self):
  r=self.report();r['probe']['anchors']['0x11478']['operands'][1]['value']=95
  with self.assertRaises(ValueError):validate(r)

 def test_codepage_assumption_rejected(self):
  r=self.report();r['probe']['dbcs_classifier_import'][1]='IsDBCSLeadByteEx'
  with self.assertRaises(ValueError):validate(r)

 def test_savedata_size_mutation(self):
  r=self.report();r['probe']['anchors']['0x806e6']['operands'][0]['value']=128
  with self.assertRaises(ValueError):validate(r)

 def test_native_promotion(self):
  r=self.report();r['probe']['real_savedata_opened']=True
  with self.assertRaises(ValueError):validate(r)

 def test_wrong_specimen_rejected(self):
  with self.assertRaises(ValueError):probe(b'MZ')
