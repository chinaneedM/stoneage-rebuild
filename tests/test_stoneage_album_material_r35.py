import copy
import json
import struct
import unittest
from tools import stoneage_album_material_r35 as r

class AlbumStateCandidates(unittest.TestCase):
 def sample(self):
  raw=bytearray(r.BLOCK_BYTES)
  start=16+2*80;name='乌力斯坦'.encode('gbk');raw[start:start+len(name)]=name
  struct.pack_into('<i',raw,start+76,1)
  # A deliberately nonsensical face value must never enter the name catalogue.
  struct.pack_into('<i',raw,start+36,123456789)
  return raw

 def test_only_recorded_name_fields_survive(self):
  d=r.observe_album(self.sample());self.assertEqual(len(d['observed_name_rows']),1)
  row=d['observed_name_rows'][0];self.assertEqual((row['album_slot'],row['observed_name_gbk']),(2,'乌力斯坦'))
  self.assertNotIn('face',row);self.assertFalse(row['face_stat_and_free_name_fields_interpreted'])

 def test_unflagged_random_text_is_not_a_species(self):
  raw=self.sample();struct.pack_into('<i',raw,16+2*80+76,0)
  self.assertEqual(r.observe_album(raw)['observed_name_rows'],[])

 def test_unknown_flags_are_not_photographs(self):
  raw=self.sample();struct.pack_into('<i',raw,16+2*80+76,2)
  with self.assertRaises(ValueError):r.observe_album(raw)

 def test_incomplete_block_never_padded_or_truncated(self):
  for raw in (self.sample()[:-1],self.sample()+b'\0',b''):
   with self.subTest(length=len(raw)),self.assertRaises(ValueError):r.observe_album(raw)

 def test_nonterminated_or_invalid_encoding_is_not_guessed(self):
  raw=self.sample();raw[176:193]=b'A'*17
  with self.assertRaises(ValueError):r.observe_album(raw)
  raw=self.sample();raw[176:193]=b'\x81\0'+b'\0'*15
  with self.assertRaises(UnicodeDecodeError):r.observe_album(raw)

class ActualArchiveBoundaries(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads((r.ROOT/r.REPORT).read_bytes())

 def test_actual_source_material(self):r.replay(self.report)

 def test_reject_name_change_even_with_unchanged_count(self):
  d=copy.deepcopy(self.report);d['album_material']['observed_name_rows'][0]['observed_name_gbk']='名称伪造'
  with self.assertRaises(ValueError):r.replay(d)

 def test_reject_duplicate_occurrence(self):
  d=copy.deepcopy(self.report);d['album_material']['observed_name_rows'][1]=copy.deepcopy(d['album_material']['observed_name_rows'][0])
  with self.assertRaises(ValueError):r.replay(d)

 def test_no_random_face_id_or_early_build_promotion(self):
  for key in ('random_face_or_stat_fields_promoted','same_build_species_to_graphic_binding_proven','account_keys_decoded'):
   d=copy.deepcopy(self.report);d['boundaries'][key]=True
   with self.subTest(key=key),self.assertRaises(ValueError):r.replay(d)
  d=copy.deepcopy(self.report);d['source_scope']='OFFICIAL_TW10_MASTER'
  with self.assertRaises(ValueError):r.replay(d)

if __name__=='__main__':unittest.main()
