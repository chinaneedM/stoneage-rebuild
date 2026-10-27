import copy
import json
import lzma
import unittest
from tools.stoneage_album_crossversion_r43 import ROOT, REPORT, build, project


def row(slot=0, face=28001, name='乌力', index=0):
 return {'album_slot':slot,'table_face_value':face,'name_gbk':name,'table_index':index}


def ref(profile='TW10', alias=28001, physical=7246, cid='a', index=0):
 return {'profile':profile,'logical_alias':str(alias),'physical_bitmapno':str(physical),
         'content_id':cid,'adrn_size':'20','source_index':str(index)}


class Projection(unittest.TestCase):
 def setUp(self):
  self.contents={'a':{'bytes':'20','rd_sha256':'a'*64},'b':{'bytes':'20','rd_sha256':'b'*64}}

 def test_physical_same_number_is_not_alias(self):
  result,_=project([row()], [ref(alias=0,physical=28001)], self.contents)
  self.assertEqual(result[0]['profiles']['TW10']['references'],[])

 def test_all_conflicting_candidates_retained(self):
  result,_=project([row()], [ref(),ref(cid='b',index=9)], self.contents)
  p=result[0]['profiles']['TW10']
  self.assertEqual(p['status'],'MULTIPLE_CONTENTS')
  self.assertEqual([r['source_index'] for r in p['references']],['0','9'])

 def test_repeated_same_content_keeps_both_positions(self):
  result,_=project([row()], [ref(),ref(index=9)], self.contents)
  self.assertEqual(result[0]['profiles']['TW10']['status'],'ONE_CONTENT')
  self.assertEqual(len(result[0]['profiles']['TW10']['references']),2)

 def test_profiles_do_not_fill_each_other(self):
  result,_=project([row()], [ref(profile='CN50')], self.contents)
  self.assertEqual(result[0]['profiles']['TW10']['status'],'MISSING_IN_FIXED_CATALOG')

 def test_holes_are_not_species(self):
  result,holes=project([row(-1,0,'无',4),row(index=5)],[],self.contents)
  self.assertEqual(holes,[4]);self.assertEqual(len(result),1)

 def test_invalid_placeholder_rejected(self):
  with self.assertRaises(ValueError):project([row(-1,28001)],[],self.contents)

 def test_missing_definition_rejected(self):
  with self.assertRaises(ValueError):project([row()],[ref(cid='missing')],self.contents)

 def test_wrong_rd_extent_rejected(self):
  bad=copy.deepcopy(self.contents);bad['a']['bytes']='21'
  with self.assertRaises(ValueError):project([row()],[ref()],bad)

 def test_unknown_profile_rejected(self):
  with self.assertRaises(ValueError):project([row()],[ref(profile='invented')],self.contents)

 def test_all_pinned_inputs_replay_exactly(self):
  actual=build();self.assertEqual(actual,json.loads(lzma.decompress((ROOT/REPORT).read_bytes())))
  self.assertEqual(actual['named_slots'],224)
  self.assertEqual(len(actual['placeholder_table_indices']),57)
  self.assertEqual(actual['profile_counts']['TW10']['slots_with_reference'],120)
  self.assertEqual(actual['profile_counts']['CN50']['statuses']['MULTIPLE_CONTENTS'],4)
  self.assertEqual(actual['boundaries']['official_tw10_names_authenticated'],0)
  self.assertFalse(actual['boundaries']['pixels_read_or_rendered'])

if __name__=='__main__':unittest.main()
