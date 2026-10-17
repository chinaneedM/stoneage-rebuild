import unittest
from tools.stoneage_world_npc_quest_join_probe import exact_name,mentions,numeric_items,typed_events,geometry
class JoinTests(unittest.TestCase):
 def test_name_mention_is_not_exact_identity(self):
  self.assertTrue(mentions('向日美子問好'.encode('big5')));self.assertEqual(exact_name('向日美子問好'.encode('gb18030')),[])
 def test_exact_big5_name(self):self.assertEqual(exact_name('日美子'.encode('big5'))[0]['query_role'],'HIMIKO')
 def test_partial_numeric_id_rejected(self):self.assertIsNone(numeric_items(b'123abc'))
 def test_quantity_not_silently_lost(self):self.assertEqual(numeric_items(b'12*3,45'),[{'id':12,'quantity':3},{'id':45,'quantity':1}])
 def test_events_not_joined_across_delimiter(self):
  r=typed_events(b'EVENT:ITEM=12|DelItem:12|EventEnd|GetItem:45|EventEnd')
  self.assertEqual(len(r),2);self.assertEqual(r[0]['actions'][0]['role'],'REMOVE_ITEM_CONFIG');self.assertEqual(r[1]['actions'][0]['role'],'GIVE_ITEM_CONFIG')
 def test_coordinates_remain_spawn_geometry(self):
  r=geometry([(b'borncorner',b'1,2,3,4')]);self.assertFalse(r[0]['actual_spawn_or_fixed_tile_verified'])
if __name__=='__main__':unittest.main()
