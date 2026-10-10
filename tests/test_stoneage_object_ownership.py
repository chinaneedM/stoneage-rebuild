import json
import unittest
from tools.stoneage_object_ownership_audit import (
    ObjectModel, cycle_oracle, PIN_PATH, BIRTH_DATA, BIRTH_WORK,
)


class ObjectOwnershipTests(unittest.TestCase):
    def test_zero_is_a_valid_live_world_object_index(self):
        m=ObjectModel();self.assertEqual(m.add(0),0)
        self.assertEqual(m.search(0),0);self.assertEqual(m.slots[0],[1,0,1,1,1])

    def test_enemy_zero_work_value_does_not_establish_owner_identity(self):
        m=ObjectModel();m.add(0);enemy_index=4;enemy_work=0
        self.assertNotEqual(m.slots[enemy_work][1],enemy_index)
        self.assertEqual(m.search(enemy_index),-1)

    def test_full_object_table_does_not_replace_existing_owner(self):
        m=ObjectModel();m.add(0);m.add(1);before=m.state()
        self.assertEqual(m.add(6),-1);self.assertEqual(m.state(),before)

    def test_multiple_world_objects_share_one_cell_in_insertion_order(self):
        m=ObjectModel();m.add(0);m.add(1)
        self.assertEqual(m.links[3],[0,1]);self.assertEqual(m.links[:3],[[],[],[]])

    def test_object_release_unlinks_but_retains_other_named_object_fields(self):
        m=ObjectModel();m.add(0);m.add(1);m.remove(0)
        self.assertEqual(m.slots[0],[0,0,1,1,1]);self.assertEqual(m.links[3],[1])
        self.assertEqual(m.search(0),-1);self.assertEqual(m.reclaimed,1)

    def test_reused_object_appends_at_tail_without_reordering_neighbor(self):
        m=ObjectModel();m.add(0);m.add(1);m.remove(0)
        self.assertEqual(m.add(0),0);self.assertEqual(m.links[3],[1,0])

    def test_map_rejection_advances_allocator_cursor_without_object_copy(self):
        m=ObjectModel();self.assertEqual(m.add(0,floor=99),-1)
        self.assertEqual(m.cursor,1);self.assertEqual(m.slots,[[0]*5,[0]*5])
        self.assertEqual(m.add(1),1)

    def test_duplicate_map_link_rejects_candidate_without_silent_overwrite(self):
        m=ObjectModel();m.links[3]=[0]
        self.assertEqual(m.add(8),-1);self.assertEqual(m.slots[0],[0]*5)
        self.assertEqual(m.links[3],[0])

    def test_invalid_release_index_preserves_existing_storage(self):
        m=ObjectModel();m.add(0);before=m.state()
        m.remove(-1);m.remove(2);self.assertEqual(m.state(),before)
        with self.assertRaises(ValueError):ObjectModel(0)

    def test_char_release_is_distinct_from_explicit_object_release(self):
        states,seqs,nextseq=cycle_oracle(100);width=34
        before=states[:width];char_released=states[4*width:5*width]
        self.assertEqual(char_released[1:4],[0,1,1])
        self.assertEqual(before[7:],char_released[7:])
        object_released=states[6*width:7*width]
        self.assertEqual(object_released[7],-1)
        self.assertEqual(seqs,[102,103]);self.assertEqual(nextseq,106)

    def test_native_domains_pin_actual_object_map_and_release_functions(self):
        pins=json.loads(PIN_PATH.read_text())
        self.assertEqual(set(pins['profiles']),{'gavin','bismarck'})
        for p,i in pins['profiles'].items():
            for name in ('CHAR_createCharacter','_initObjectOne','initObjectArray',
                         'MAP_addNewObj','MAP_appendTailObj','MAP_removeObj',
                         'searchObjectFromCharaIndex','CHAR_endCharData','_ITEM_endExistItemsOne'):
                self.assertIn(name,i['functions'])
            self.assertFalse(i['original_freeMemory_executed'])
            self.assertFalse(i['uninitialized_object_fields_observed'])
            self.assertEqual(i['object_fields_observed'],['type','index','floor','x','y'])
            self.assertEqual(len(i['adapters']),3)
            self.assertTrue(any(path.endswith('/object.h') for path in i['header_dependency_closure']))
            self.assertTrue(any(path.endswith('/readmap.h') for path in i['header_dependency_closure']))

    def test_persistent_cursor_rotates_owners_and_failed_world_copy_resets_work(self):
        states,_seqs,_next=cycle_oracle(0,1);width=34
        self.assertEqual(states[7:12],[1,0,-1,1,0])
        self.assertEqual(states[12:17],[1,1,1,1,1])
        failed=states[5*width:6*width];self.assertEqual(failed[10:12],[0,0])
        reused=states[7*width:8*width];self.assertEqual(reused[10:12],[1,0])

    def test_preserved_input_and_birth_field_boundaries_remain_explicit(self):
        pins=json.loads(PIN_PATH.read_text());s=pins['preserved_specimen']
        self.assertTrue(s['gavin_own_configured_specimen']);self.assertTrue(s['bismarck_cross_profile_bytes_not_own_historical_data'])
        self.assertIn('OPEN',pins['iris_execution'])
        self.assertEqual(BIRTH_WORK[:3],('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX'))
        self.assertIn('CHAR_WHICHTYPE',BIRTH_DATA)


if __name__=='__main__':unittest.main()
