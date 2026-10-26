import copy
import json
import struct
import unittest
from tools import stoneage_native_album_material_r36 as r

class NativeAlbumEvidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=json.loads((r.ROOT/r.REPORT).read_bytes())

 def test_exact_permanent_report_and_actual_source(self):
  self.assertEqual(r.sha((r.ROOT/r.REPORT).read_bytes()),r.REPORT_SHA);r.replay(self.d)

 def test_internal_holes_do_not_end_the_table(self):
  rows=self.d['table']['rows'];self.assertEqual(rows[49]['album_slot'],-1)
  self.assertEqual(rows[280]['album_slot'],223)
  self.assertEqual(len({a['album_slot'] for a in rows if a['album_slot']>=0}),224)

 def test_281_lookup_rows_not_224_saved_records(self):
  d=copy.deepcopy(self.d);d['table']['compiled_rows']=224
  with self.assertRaises(ValueError):r.replay(d)
  d=copy.deepcopy(self.d);d['table']['rows']=d['table']['rows'][:49]
  with self.assertRaises(ValueError):r.replay(d)

 def test_reject_trimmed_original_name(self):
  d=copy.deepcopy(self.d);d['table']['rows'][223]['name_gbk']='梅尔顿'
  with self.assertRaises(ValueError):r.replay(d)

 def test_reject_face_value_substitution(self):
  d=copy.deepcopy(self.d);d['table']['rows'][0]['table_face_value']=7246
  with self.assertRaises(ValueError):r.replay(d)

 def test_reject_wrong_saved_name_slot_or_random_face_join(self):
  for key,value in [('album_slot',223),('saved_face_or_stat_fields_used',True)]:
   d=copy.deepcopy(self.d);d['saved_names_to_native_table'][0][key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):r.replay(d)

 def test_reject_collapsed_program_variants(self):
  d=copy.deepcopy(self.d);d['programs'].pop()
  with self.assertRaises(ValueError):r.replay(d)

 def test_reject_unproved_resource_build_or_execution_promotion(self):
  for key in ['physical_bitmap_or_spr_binding_proven','official_build_authenticated','original_program_executed','saved_file_created_by_these_programs_proven','server_species_master_recovered']:
   d=copy.deepcopy(self.d);d['boundaries'][key]=True
   with self.subTest(key=key),self.assertRaises(ValueError):r.replay(d)

 def test_va_translation_rejects_zero_fill_and_cross_section(self):
  pe={'image_base':0x400000,'sections':[{'rva':0x1000,'raw_offset':16,'raw_bytes':8}]}
  self.assertEqual(r.at_va(b'A'*24,pe,0x401002,3),(18,b'AAA'))
  for va,size in [(0x401008,1),(0x401006,3),(0x400fff,1)]:
   with self.subTest(va=va),self.assertRaises(ValueError):r.at_va(b'A'*24,pe,va,size)

 def test_compiled_photograph_face_transfer_is_required(self):
  d=copy.deepcopy(self.d)
  for i in d['static_code_windows']['photograph_name_and_table_face']['instructions']:
   if i['operands']=='dword ptr [edi + 0x2ad3bac], eax':i['operands']='dword ptr [edi + 0x2ad3bac], ecx'
  with self.assertRaises(ValueError):r.replay(d)

if __name__=='__main__':unittest.main()
